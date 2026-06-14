# One-person company OS

BotCom Workbench is not only a social media publishing helper. It is a local operating cockpit for a one-person company: AI workers prepare, execute, summarize, and hand off decisions; the operator reviews the few decisions that carry business or reputation risk.

## Design principles

- **Owner-as-approver**: the operator should approve strategy, spend, publishing, client commitments, and irreversible actions.
- **AI-workers-as-staff**: agents can research, draft, classify, summarize, generate media, prepare delivery artifacts, and propose next actions.
- **Local-first control**: credentials, tokens, account data, generated assets, and operating history stay outside the public repository.
- **Auditability**: queues, reports, commands, and notifications should leave inspectable local evidence.
- **Adapter architecture**: social platforms, CRM systems, spreadsheets, payment records, and project systems are integrations, not hard-coded assumptions.

## Operating modules

| Module | Purpose | First visible implementation |
| --- | --- | --- |
| Positioning / Offers | niche, ICP, promise, product ladder, constraints | workbench asset library |
| Acquisition / Growth | channel strategy, trend capture, experiments, lead flow | content acquisition queue |
| Content / Distribution | topics, scripts, images, videos, approval, publish-prep | media-ops review adapter |
| Customer / Community | comments, private messages, tags, follow-ups, support | planned CRM adapter |
| Delivery / Projects | client work, SOPs, checklists, acceptance evidence | workbench project files |
| Revenue / Monetization | products, affiliate/commerce/service revenue, costs | planned P&L adapter |
| Assets / Knowledge | prompts, templates, cases, media assets, datasets | AI-Workbench roots and indexes |
| Automation / Review | workers, notifications, metrics collection, retrospectives | local service status and growth review |

## Product boundary

BotCom Workbench should remain an operating cockpit, not an all-in-one SaaS clone.

It should:

- show what matters now;
- route work to the right local agent or adapter;
- make approval fast on desktop or mobile;
- preserve enough evidence to debug and improve;
- avoid locking users into one platform, one model provider, or one workflow tool.

It should not:

- hide credentials or irreversible actions from the operator;
- automate spam, fake engagement, or unauthorized account operations;
- require private project files to be committed to the public repo;
- assume every one-person company is only a creator account.

## Default workflow

```text
research / signals
  -> strategy and offer hypothesis
  -> content or outreach candidates
  -> local approval queue
  -> human approve / revise / reject
  -> publish-prep, delivery, or follow-up worker
  -> metrics and evidence
  -> growth and operating review
  -> next experiment
```

## Extension points

Adapters should be added as small, auditable integrations:

- `status` provider: exposes current module health, blockers, counts, and next actions.
- `queue` provider: exposes reviewable items and safe actions.
- `asset` provider: exposes local files or indexed work products.
- `notification` provider: pushes concise approval/status messages to Feishu, WeCom, or another channel.
- `metrics` provider: imports platform, CRM, revenue, or delivery data for retrospectives.

The public repository includes the desktop cockpit, local API, notification bridge, and the first content-operations adapter contract.
