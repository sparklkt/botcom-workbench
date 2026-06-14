#!/usr/bin/env python3
"""BotCom status bridge for Feishu / WeCom webhooks.

This script is intentionally dependency-free and local-first. It reads only
allowlisted media-ops status files, never prints webhook values, and sends a
compact approval/status digest to configured group bots.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BOTCOM_HOME = Path(os.getenv("BOTCOM_HOME", str(Path.home() / "BotCom"))).expanduser()
MEDIA_OPS = Path(os.getenv("BOTCOM_MEDIA_OPS_ROOT", str(BOTCOM_HOME / "media-ops"))).expanduser()
WORKBENCH = Path(os.getenv("BOTCOM_WORKBENCH_ROOT", str(BOTCOM_HOME / "AI-Workbench"))).expanduser()
ENV_FILES = [MEDIA_OPS / ".env", ROOT / ".env"]


def read_env_files() -> dict[str, str]:
    values: dict[str, str] = {}
    for path in ENV_FILES:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return {**values, **os.environ}


def read_json(path: Path, default: Any) -> Any:
    try:
      return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
      return default


def read_queue() -> list[dict[str, str]]:
    path = MEDIA_OPS / "database" / "approval_queue.csv"
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count_by(rows: list[dict[str, str]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        value = row.get(key) or "unknown"
        out[value] = out.get(value, 0) + 1
    return out


def pid_status(name: str) -> str:
    path = MEDIA_OPS / "runtime" / "pids" / f"{name}.json"
    data = read_json(path, {})
    pid = int(data.get("pid") or 0)
    if not pid:
        return "stopped"
    try:
        os.kill(pid, 0)
        return f"running(pid={pid})"
    except OSError:
        return f"stale(pid={pid})"


def mobile_url() -> str:
    text_path = MEDIA_OPS / "runtime" / "mobile_entry.md"
    if not text_path.exists():
        return ""
    match = re.search(r"https?://[^\s<>\"]+", text_path.read_text(encoding="utf-8", errors="replace"))
    return match.group(0) if match else ""


def redact_tokens(text: str) -> str:
    return re.sub(r"([?&]token=)[^&\s<>\"]+", r"\1<redacted>", text)


def build_digest() -> str:
    launch = read_json(MEDIA_OPS / "reports" / "launch_readiness.json", {})
    growth = read_json(MEDIA_OPS / "reports" / "growth_snapshot.json", {})
    manifest = read_json(WORKBENCH / "_indexes" / "workbench_manifest.json", {})
    rows = read_queue()
    blockers: list[str] = []
    for section in launch.get("sections", []):
        for item in section.get("items", []):
            if item.get("status") == "block":
                blockers.append(f"- {item.get('label', item.get('id', 'block'))}: {item.get('next_step', item.get('detail', ''))}")
    recs = growth.get("recommendations", [])[:3]
    queue_status = ", ".join(f"{k}={v}" for k, v in count_by(rows, "status").items()) or "none"
    queue_platforms = ", ".join(f"{k}={v}" for k, v in count_by(rows, "platform").items()) or "none"
    url = mobile_url()

    lines = [
        "BotCom OS 状态摘要",
        f"- 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 上线状态: {launch.get('overall', 'unknown')} / counts={launch.get('counts', {})}",
        f"- 审核队列: {len(rows)} 条 / {queue_status} / {queue_platforms}",
        f"- 服务: review={pid_status('review')}; worker={pid_status('worker')}",
        f"- 工作台资产: {len(manifest.get('items', []))} 项",
    ]
    if url:
        lines.append(f"- 手机审核: {url}")
    if blockers:
        lines.append("\n当前阻塞:")
        lines.extend(blockers[:6])
    if recs:
        lines.append("\n增长建议:")
        lines.extend(f"- {item}" for item in recs)
    return "\n".join(lines)


def post_json(url: str, payload: dict[str, Any]) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return 200 <= resp.status < 300, body[:500]
    except urllib.error.HTTPError as exc:
        return False, exc.read().decode("utf-8", errors="replace")[:500]
    except Exception as exc:
        return False, str(exc)


def feishu_payload(text: str, env: dict[str, str]) -> dict[str, Any]:
    payload: dict[str, Any] = {"msg_type": "text", "content": {"text": text}}
    secret = env.get("FEISHU_BOT_SECRET") or env.get("LARK_BOT_SECRET")
    if secret:
        ts = str(int(time.time()))
        sign = base64.b64encode(hmac.new(f"{ts}\n{secret}".encode(), b"", hashlib.sha256).digest()).decode()
        payload["timestamp"] = ts
        payload["sign"] = sign
    return payload


def send(channel: str, text: str, env: dict[str, str], dry_run: bool) -> dict[str, Any]:
    if channel == "feishu":
        url = env.get("FEISHU_BOT_WEBHOOK") or env.get("LARK_BOT_WEBHOOK")
        payload = feishu_payload(text, env)
    elif channel == "wechat":
        url = env.get("WECHAT_WORK_BOT_WEBHOOK") or env.get("WECHAT_BOT_WEBHOOK") or env.get("WECHAT_WEBHOOK")
        payload = {"msgtype": "markdown", "markdown": {"content": text}}
    else:
        raise ValueError(f"unknown channel: {channel}")

    if not url:
        return {"channel": channel, "configured": False, "sent": False, "error": "webhook missing"}
    if dry_run:
        return {"channel": channel, "configured": True, "sent": False, "dry_run": True}
    ok, body = post_json(url, payload)
    return {"channel": channel, "configured": True, "sent": ok, "response": body}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true", help="send BotCom status digest")
    parser.add_argument("--channel", choices=["all", "feishu", "wechat"], default="all")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.status:
        parser.error("currently only --status is supported")

    env = read_env_files()
    text = build_digest()
    display_text = redact_tokens(text)
    channels = ["feishu", "wechat"] if args.channel == "all" else [args.channel]
    result = {
        "ok": True,
        "dry_run": args.dry_run,
        "channels": [send(ch, text, env, args.dry_run) for ch in channels],
        "message_preview": display_text if args.dry_run else display_text.splitlines()[:8],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["channels"]:
            print(f"{item['channel']}\tconfigured={item['configured']}\tsent={item['sent']}")
        if args.dry_run:
            print("\n" + display_text)
    return 0 if all((not x["configured"]) or x["sent"] or args.dry_run for x in result["channels"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
