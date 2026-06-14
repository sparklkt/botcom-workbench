# Architecture

```text
Electron shell
  -> localhost Node backend
    -> local file system cockpit
    -> embedded terminal bridge
    -> BotCom status API
    -> one-person company dashboard
    -> localhost review / queue proxy
      -> media-ops review server
    -> notification bridge
      -> Feishu / Lark / WeCom webhook
```

## Main modules

```text
electron/main.js        Electron app wrapper and terminal bridge
server.js               Local HTTP backend
public/                 Browser UI
botcom/comms_bridge.py  Feishu / WeCom status bridge
```

## Runtime state

BotCom Workbench stores its local app state under:

```text
~/.botcom-workbench
```

Optional media-ops state is outside this repository and controlled by:

```text
BOTCOM_MEDIA_OPS_ROOT
```

## Dashboard flow

1. UI opens the BotCom OS panel.
2. UI calls `GET /api/botcom/status`.
3. UI calls `GET /api/botcom/review-state`.
4. Backend reads local reports, asset summaries, service status, and queue summaries.
5. UI renders the one-person company operating map plus the active content/acquisition adapter.
6. User clicks approve / reject / publish-prep.
7. UI sends `POST /api/botcom/review-action`.
8. Backend validates allowlists and proxies to the local review server.

The current queue adapter is media-oriented. Future adapters can expose CRM follow-ups, delivery approvals, revenue checks, or asset review items through the same local-only pattern.

## Non-goals

This repository does not implement:

- platform scraping;
- automated engagement farming;
- credential sharing;
- cloud-hosted account operations;
- generated media storage.
