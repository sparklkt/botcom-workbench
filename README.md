# BotCom Workbench

BotCom Workbench is a local-first desktop operating cockpit for one-person companies.

It is designed for a founder/operator who uses AI workers for research, content, automation, delivery support, and review preparation, while keeping the human in the final approval loop.

It combines:

- a local file workbench;
- an embedded terminal for coding agents and command-line operators;
- a BotCom OS dashboard for one-person company operations;
- optional Feishu / WeCom status notifications;
- a safe localhost proxy for approve / reject / publish-prep actions.

The first packaged module is a content and acquisition operations layer for X, Douyin, Xiaohongshu, and other review-driven channels. The architecture is intentionally modular so operators can add CRM, delivery, revenue, asset-library, and automation adapters later.

## What it is for

BotCom Workbench is designed for a workflow where AI workers prepare work and the human operator only performs final review:

```text
strategy / research / content / delivery preparation
  -> local operating queues
  -> human approve / reject
  -> publish-prep / delivery / follow-up worker
  -> metrics and evidence collection
  -> growth and operating review
```

The repository contains the desktop cockpit and integration points. It does not include any private account data, platform credentials, content calendar, or generated media assets.

Core operating modules:

1. positioning and offers;
2. acquisition and growth;
3. content and distribution;
4. customer and community follow-up;
5. delivery and project execution;
6. revenue and monetization;
7. asset and knowledge management;
8. automation and review loops.

## Features

- Desktop app built with Electron.
- Local-only backend bound to `127.0.0.1`.
- File browser, previewer, editor, and embedded terminal.
- BotCom OS dashboard in the sidebar:
  - operating-state snapshot;
  - eight-module one-person company map;
  - local operating adapters for CRM, delivery, revenue, assets, and automation;
  - approval queues and mobile approval links;
  - service health, blockers, next actions, and review suggestions.
- AI beginner guide explaining agents, skills, models, API keys, context, and approval queues.
- Model / API profile panel for Claude Code, Codex, Anthropic, OpenAI-compatible, and DeepSeek-style setups.
- First-run setup wizard that creates a local one-person company workspace and example operating adapters without overwriting existing files.
- Review queue API integration:
  - `GET /api/botcom/status`
  - `GET /api/botcom/review-state`
  - `POST /api/botcom/review-action`
- Safe action allowlists for day, platform, action, and publisher.
- Feishu / Lark custom bot and WeCom webhook status bridge.
- Offline vendored frontend assets.
- macOS DMG build target.

## Quick start

Requirements:

- macOS or a desktop OS supported by Electron;
- Node.js 18+;
- Python 3 for the optional notification bridge.

Install dependencies:

```bash
npm ci
npm run rebuild
```

Run the local web app:

```bash
npm start
```

Run the Electron app:

```bash
npm run app
```

Build a macOS DMG:

```bash
npm run dist
```

Run smoke checks:

```bash
npm run botcom:smoke
```

Run the full release gate:

```bash
npm run release:check
```

Publish to GitHub after authenticating `gh`:

```bash
gh auth login -h github.com -p https -w
npm run release:github
```

## Configuration

BotCom Workbench is local-first. By default it uses:

```text
BOTCOM_HOME=~/BotCom
BOTCOM_MEDIA_OPS_ROOT=~/BotCom/media-ops
BOTCOM_WORKBENCH_ROOT=~/BotCom/AI-Workbench
BOTCOM_ADAPTERS_ROOT=~/BotCom/adapters
BOTCOM_WORKBENCH_PORT=4570
```

You can override them:

```bash
BOTCOM_HOME="$HOME/BotCom" \
BOTCOM_MEDIA_OPS_ROOT="$HOME/BotCom/media-ops" \
BOTCOM_WORKBENCH_ROOT="$HOME/BotCom/AI-Workbench" \
npm run app
```

See `.env.example` and `docs/CONFIGURATION.md`.

## First-run setup

Open the desktop app and click **One-click setup**. It creates:

- `~/BotCom/AI-Workbench` with beginner-friendly strategy, content, customer, delivery, revenue, asset, and automation starter files;
- `~/BotCom/adapters` with example CRM, delivery, and revenue adapters;
- no cloud account and no credential files.

Existing files are kept unchanged.

## AI tools and model profiles

The in-app **Model / API** panel detects local `claude` and `codex` commands, stores local model profiles, and can load a selected profile into the embedded terminal.

Profiles are stored under `~/.botcom-workbench` and raw API keys are not returned by the dashboard API.

Claude Code's official path uses Anthropic credentials. DeepSeek and other OpenAI-compatible providers can be configured as terminal profiles for tools or proxies that support `OPENAI_API_KEY` and `OPENAI_BASE_URL`.

## Optional media-ops integration

The BotCom OS panel can integrate with a local `media-ops` workspace if it exposes a token-protected review server compatible with:

```text
GET  /api/state
POST /api/approve
POST /api/reject
POST /api/publish
POST /api/retry
```

BotCom Workbench only proxies to `127.0.0.1`; it does not accept arbitrary backend URLs from the browser.

See `docs/INTEGRATION.md`.

For the broader product model, see `docs/ONE_PERSON_COMPANY_OS.md`.

## Notifications

Configure Feishu / Lark or WeCom webhooks in `.env`:

```text
FEISHU_BOT_WEBHOOK=
FEISHU_BOT_SECRET=
WECHAT_WORK_BOT_WEBHOOK=
```

Preview without sending:

```bash
npm run botcom:status
```

Send:

```bash
npm run botcom:notify
```

Dry-run output redacts review tokens. Real notifications keep the review URL intact so an approved operator can open it from mobile.

## Security model

- Backend binds to `127.0.0.1`.
- Host header is restricted to localhost addresses.
- POST requests are protected by origin checks.
- Review actions are allowlisted.
- Review tokens are read locally and not exposed through the dashboard API.
- Webhook secrets are read from local environment files and not printed.
- Build artifacts, runtime files, `.env`, `node_modules`, and `dist` are ignored.
- GitHub publishing uses `gh` OAuth or `GH_TOKEN`; passwords are not supported and should not be used.

See `docs/SECURITY.md`.

## Documentation

- `docs/ARCHITECTURE.md`
- `docs/CONFIGURATION.md`
- `docs/INTEGRATION.md`
- `docs/ONE_PERSON_COMPANY_OS.md`
- `docs/PUBLISHING.md`
- `docs/SECURITY.md`
- `docs/ROADMAP.md`
- `CONTRIBUTING.md`

## Public repository hygiene

This repository intentionally excludes:

- personal workspace paths;
- private project files;
- platform credentials;
- generated review tokens;
- account-specific publishing queues;
- generated media outputs;
- packaged DMG files.

## Attribution

BotCom Workbench is derived from FanBox by alchaincyf, licensed under MIT.

See `NOTICE.md` and `LICENSE`.
