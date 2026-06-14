#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== BotCom release gate =="

echo "== syntax / smoke =="
npm run botcom:smoke

echo "== production dependency audit =="
npm audit --omit=dev

echo "== privacy scan =="
if rg -n "/Users/|Documents/焦|192\\.168|j2Q50|新加坡|Mac mini|Harmes|Armis|Valut|Deepseek V4|DeepSeek V4|open-apis/bot/v2/hook/[0-9a-zA-Z-]+|qyapi\\.weixin\\.qq\\.com/cgi-bin/webhook/send\\?key=[0-9a-zA-Z-]+|sk-[A-Za-z0-9_-]{20,}" -S --hidden -g '!node_modules' -g '!dist' -g '!.git' -g '!public/vendor' -g '!scripts/release_gate.sh' .; then
  echo "Privacy scan found potential private data." >&2
  exit 1
fi

echo "== brand scan =="
brand_hits="$(rg -n "FanBox|fanbox|FANBOX|翻箱|\\.fanbox|application/x-fanbox|Welcome to FanBox|欢迎用 FanBox|fb-dark|fb-paper|fb-editorial|fb_" -S --hidden -g '!node_modules' -g '!dist' -g '!.git' -g '!scripts/release_gate.sh' . || true)"
unexpected="$(printf '%s\n' "$brand_hits" | grep -vE '^(\./)?(NOTICE.md|README.md|CHANGELOG.md|LICENSE):' || true)"
if [[ -n "$unexpected" ]]; then
  printf '%s\n' "$unexpected" >&2
  echo "Unexpected legacy brand references found." >&2
  exit 1
fi

echo "== local API smoke =="
tmp_home="$(mktemp -d)"
server_log="$(mktemp)"
status_json="$(mktemp)"
ai_json="$(mktemp)"
cleanup() {
  if [[ -n "${server_pid:-}" ]]; then
    kill "$server_pid" 2>/dev/null || true
    wait "$server_pid" 2>/dev/null || true
  fi
  rm -rf "$tmp_home" "$server_log" "$status_json" "$ai_json"
}
trap cleanup EXIT
mkdir -p "$tmp_home/adapters"
cp examples/adapters/*.json "$tmp_home/adapters/"
port="$(node - <<'NODE'
const net = require('net');
const s = net.createServer();
s.listen(0, '127.0.0.1', () => {
  console.log(s.address().port);
  s.close();
});
NODE
)"
BOTCOM_HOME="$tmp_home" BOTCOM_NO_OPEN=1 BOTCOM_WORKBENCH_PORT="$port" node server.js >"$server_log" 2>&1 &
server_pid=$!
for _ in $(seq 1 80); do
  if curl -fsS "http://127.0.0.1:$port/api/botcom/status" >"$status_json" 2>/dev/null; then break; fi
  sleep 0.25
done
curl -fsS "http://127.0.0.1:$port/api/botcom/ai-profiles" >"$ai_json"
node - "$status_json" "$ai_json" <<'NODE'
const fs = require('fs');
const status = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ai = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
if (!status.ok) throw new Error('status not ok');
if (!ai.ok) throw new Error('ai profiles not ok');
if ((status.operatingAdapters && status.operatingAdapters.count) !== 3) throw new Error('adapter smoke failed');
const raw = JSON.stringify(ai);
if (/sk-test|ANTHROPIC_API_KEY=|OPENAI_API_KEY=/.test(raw)) throw new Error('ai profile leaked raw secret');
console.log('api ok: adapters=' + status.operatingAdapters.count + ' profiles=' + ai.profiles.length);
NODE

echo "== release gate passed =="
