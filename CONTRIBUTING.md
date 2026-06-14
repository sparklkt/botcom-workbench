# Contributing

Contributions are welcome.

## Development setup

```bash
npm ci
npm run rebuild
npm run botcom:smoke
npm run app
```

## Pull request checklist

- Keep the backend local-first unless there is a clear reason not to.
- Do not commit `.env`, credentials, review tokens, generated queues, or media outputs.
- Run `npm run botcom:smoke`.
- If changing Electron or native modules, run `npm run rebuild`.
- If changing packaging metadata, run `npm run dist` on macOS when possible.
- Update documentation for new environment variables or API behavior.

## Code style

- Prefer small, reviewable changes.
- Keep secrets and account-specific state outside the repository.
- Avoid broad dependencies for simple local operations.
- Keep platform-specific automation behind explicit user configuration.

## Security-sensitive changes

Open an issue or private advisory before changing:

- localhost access controls;
- token handling;
- review action allowlists;
- file-system write APIs;
- terminal / process spawning behavior.
