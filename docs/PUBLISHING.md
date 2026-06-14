# Publishing

## Pre-release gate

Run:

```bash
npm run release:check
```

This checks:

- JavaScript/Python syntax smoke;
- production dependency audit;
- privacy keyword scan;
- legacy brand scan;
- local API smoke with example operating adapters;
- AI profile API does not leak raw secrets.

Build the macOS DMG:

```bash
npm run dist
```

The DMG is written to:

```text
dist/BotCom Workbench-0.1.0-arm64.dmg
```

## GitHub publishing

Use `gh auth login` or a personal access token. Do not use or share your GitHub password.

Create and push a public repository:

```bash
gh repo create botcom-workbench --public --source=. --remote=origin --push
```

If the repository already exists:

```bash
git remote add origin git@github.com:<owner>/botcom-workbench.git
git push -u origin main
```

## Release notes checklist

- Confirm `npm run release:check` passes.
- Confirm the installed app starts and `GET /api/botcom/status` returns `ok: true`.
- Confirm the UI has no legacy product branding outside license/attribution.
- Confirm no `.env`, credentials, private queues, generated media, or personal project files are tracked.
- Upload the DMG only after verifying it was built from the committed source.
