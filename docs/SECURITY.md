# Security

BotCom Workbench is designed as a local-first desktop tool. It is not a hosted multi-tenant service.

## Local binding

The backend binds to:

```text
127.0.0.1
```

It is intended to be reached only by the local browser or Electron shell.

## Host and origin checks

The server rejects non-localhost Host headers and rejects cross-origin POST requests.

Allowed hosts:

```text
localhost
127.0.0.1
::1
[::1]
```

## Review proxy

The BotCom review proxy:

- calls only `127.0.0.1`;
- does not accept arbitrary URLs from the frontend;
- allowlists actions, days, platforms, and publishers;
- reads review tokens locally;
- does not return review tokens to the browser.

## Secrets

Secrets should be stored in untracked `.env` files or process environment variables.

Never commit:

- platform API keys;
- platform access tokens;
- GitHub personal access tokens;
- passwords;
- webhook URLs;
- review server tokens;
- generated mobile review links.

GitHub no longer supports password authentication for Git or `gh` publishing. Use browser OAuth via:

```bash
gh auth login -h github.com -p https -w
```

or a short-lived `GH_TOKEN`/`GITHUB_TOKEN`. Do not paste account passwords into shell commands, documentation, issues, or chat logs.

## AI profile storage

Model/API profiles are stored locally under:

```text
~/.botcom-workbench/ai-profiles.json
~/.botcom-workbench/ai-env/
```

The dashboard API returns only `apiKeySet` and a short masked preview. Raw keys are used only inside local env scripts with `0600` permissions.

## Desktop distribution

The default build is unsigned/ad-hoc signed and intended for local use. Public distribution should add:

- Apple Developer ID signing;
- notarization;
- release checksums;
- reproducible release notes.

## Reporting vulnerabilities

For now, open a private security advisory or contact the repository maintainer. Do not publish working exploit details before a fix is available.
