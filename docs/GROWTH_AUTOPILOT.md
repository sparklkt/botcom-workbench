# Growth Autopilot

Growth Autopilot is BotCom Workbench's operating loop for AI-assisted social growth. It is designed for one-person companies that want AI workers to run the heavy work while the owner only reviews high-risk decisions.

The goal is not to clone a scheduler. The loop covers the full operating chain:

```text
trend signals
  -> positioning and experiment hypothesis
  -> platform-specific drafts
  -> image/video asset factory
  -> quality and compliance gates
  -> owner approval queue
  -> publish-prep or approved publishing connector
  -> metric capture
  -> next experiment
```

## Public benchmark posture

BotCom compares the local workflow against public reference products and workflow patterns:

- Postiz-style open-source AI social scheduling;
- n8n-style automation graphs and social templates;
- Buffer-style creator scheduling and analytics;
- Publer-style bulk scheduling and recurring content workflows.

Those systems are useful references, but most of them are scheduler-centric. BotCom's differentiator is the company-level loop: strategy, agent roles, content matrix, asset generation, quality gate, approval UX, connectors, metrics, and the next experiment are evaluated together.

## Local reports

When a compatible `media-ops` workspace is present, the BotCom OS dashboard reads:

```text
$BOTCOM_MEDIA_OPS_ROOT/reports/growth_autopilot.json
$BOTCOM_MEDIA_OPS_ROOT/reports/growth_autopilot.md
$BOTCOM_MEDIA_OPS_ROOT/research/latest_public_benchmark.md
```

The desktop UI shows:

- BotCom loop score;
- best public reference score;
- margin;
- capability matrix;
- missing credentials or login steps;
- recent loop findings;
- buttons to rerun the loop or open reports.

The score is an architectural and readiness benchmark. Real growth performance still depends on live credentials, platform permissions, publishing cadence, and 24-hour / 72-hour metric feedback.

## Owner approval model

Growth Autopilot should keep irreversible or reputation-sensitive actions behind owner approval:

- account connection;
- platform publishing;
- paid API usage above local thresholds;
- external messages to customers or communities;
- monetization offers;
- policy-sensitive content.

Safe local steps can run automatically:

- research summarization;
- draft generation;
- image/video draft generation;
- formatting;
- queue creation;
- quality checks;
- report generation;
- metric analysis after import.

## Credential slots

Keep real credentials out of Git. Use local `.env`, the operating system keychain, or an approved secret manager.

Common variables:

```text
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
OPENAI_API_KEY=
OPENAI_IMAGE_MODEL=gpt-image-1
SEEDANCE_API_TOKEN=
VOLCENGINE_ACCESS_KEY_ID=
VOLCENGINE_SECRET_ACCESS_KEY=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_REFRESH_TOKEN=
FEISHU_BOT_WEBHOOK=
WECHAT_WORK_BOT_WEBHOOK=
MEDIA_OPS_BROWSER_PROFILE_DIR=$HOME/BotCom/browser-profile
```

## Platform connector stance

- **X**: prefer official API for posting and public metrics.
- **Reddit**: prefer official OAuth API for trend ingestion and approved posting.
- **TikTok / Douyin**: prefer official content posting APIs where account permissions allow it; use local browser-assisted steps only when explicitly approved by the operator and allowed by the platform/account context.
- **Xiaohongshu**: treat direct publishing as a connector slot. Use official partner/open-platform paths when available; otherwise keep publishing in owner-reviewed browser or service-provider workflows.

## Extending the loop

A new connector or generator should expose:

1. `status`: ready, blocked, missing credentials, last successful run;
2. `inputs`: accepted local files or queue fields;
3. `actions`: dry-run, prepare, publish, collect metrics;
4. `evidence`: local logs, request IDs, generated files, metric snapshots;
5. `risk`: whether owner approval is required.

This keeps the product usable for non-technical operators while preserving auditability for advanced users.
