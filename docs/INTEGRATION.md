# Integration

BotCom Workbench can operate as a standalone local file cockpit. The BotCom OS panel becomes more useful when connected to local adapters for content, acquisition, CRM, delivery, revenue, assets, automation, and metrics.

The first adapter contract included here is a media-ops review server for content and acquisition queues.

## Expected media-ops review server

The server should bind locally and expose:

```text
GET  /api/state
POST /api/approve
POST /api/reject
POST /api/publish
POST /api/retry
```

Authentication should use one of:

```text
X-Media-Ops-Token: <token>
Authorization: Bearer <token>
?token=<token>
```

BotCom Workbench itself only calls the review server through `127.0.0.1`.

## State shape

`GET /api/state` should return JSON similar to:

```json
{
  "rows": [
    {
      "day": "day01",
      "platform": "x",
      "content_id": "day01-x",
      "status": "review",
      "last_error": ""
    }
  ],
  "days": {
    "day01": {
      "x": { "short_post": "..." },
      "xiaohongshu": { "note": "..." },
      "douyin": { "caption": "..." }
    }
  }
}
```

## Action body

BotCom Workbench sends:

```json
{
  "day": "day01",
  "platform": "x",
  "publisher": "smart",
  "notes": "BotCom Workbench desktop review",
  "auto_publish_after_approve": false
}
```

## Allowed values

Actions:

```text
approve
reject
publish
retry
```

Days:

```text
day01 ... day07
```

Platforms:

```text
x
xiaohongshu
douyin
all
```

Publishers:

```text
smart
mock
x-api
x-api-short
x-api-thread
x-api-video-text
douyin-browser
xiaohongshu-browser
```

## File layout for content queue shortcuts

The dashboard opens local files using this convention:

```text
$BOTCOM_MEDIA_OPS_ROOT/publish_queue/day01/x/
$BOTCOM_MEDIA_OPS_ROOT/publish_queue/day01/xhs/
$BOTCOM_MEDIA_OPS_ROOT/publish_queue/day01/douyin/
$BOTCOM_MEDIA_OPS_ROOT/publish_queue/day01/assets/
```

This layout is optional but recommended.

## Future adapter pattern

Additional one-person company adapters should follow the same local-first pattern:

1. bind to localhost or write local JSON/CSV reports;
2. expose compact status, counts, blockers, and next actions;
3. expose reviewable queue items only when human approval is needed;
4. keep credentials and private account data outside this repository;
5. make all irreversible actions explicit and allowlisted.

## Local operating adapter JSON

For simple integrations, no server is required. Put one JSON file per module under:

```text
$BOTCOM_ADAPTERS_ROOT
```

Default:

```text
~/BotCom/adapters
```

Example:

```json
{
  "id": "crm-lite",
  "name": "CRM Lite",
  "module": "customer",
  "tone": "warn",
  "metric": "12 leads",
  "description": "Simple customer follow-up tracker exported from a spreadsheet.",
  "next": "Follow up with 3 leads older than 48 hours.",
  "updated_at": "2026-06-14T12:00:00Z",
  "counts": {
    "leads": 12,
    "needs_reply": 3
  },
  "queue": {
    "rows": 12,
    "review": 3,
    "blocked": 0
  },
  "warnings": [
    "No owner reply SLA is configured."
  ],
  "next_actions": [
    "Create a daily follow-up review queue."
  ],
  "links": [
    {
      "label": "Local CRM export",
      "path": "~/BotCom/crm/leads.csv"
    }
  ]
}
```

Allowed modules:

```text
positioning
acquisition
content
customer
delivery
revenue
assets
automation
```

Allowed tones:

```text
good
warn
bad
```

BotCom only returns a safe allowlist of fields from adapter JSON. Do not put raw API keys or account passwords in adapter files.
