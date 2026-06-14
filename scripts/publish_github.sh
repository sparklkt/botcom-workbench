#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OWNER="${GITHUB_OWNER:-sparklkt}"
REPO="${GITHUB_REPO:-botcom-workbench}"
VISIBILITY="${GITHUB_VISIBILITY:-public}"

if [[ "$VISIBILITY" != "public" && "$VISIBILITY" != "private" ]]; then
  echo "GITHUB_VISIBILITY must be public or private." >&2
  exit 2
fi

echo "== BotCom GitHub publish =="
echo "target: ${OWNER}/${REPO} (${VISIBILITY})"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required. Install it first." >&2
  exit 1
fi

if ! gh auth status -h github.com >/dev/null 2>&1; then
  cat >&2 <<'EOF'
GitHub is not authenticated.

Use one of these safe methods:

  gh auth login -h github.com -p https -w

or set GH_TOKEN/GITHUB_TOKEN to a personal access token.

Do not use a GitHub password. GitHub does not support password auth for Git/gh,
and putting passwords in commands can leak them into shell history and logs.
EOF
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree is not clean. Commit or stash changes before publishing." >&2
  git status --short >&2
  exit 1
fi

echo "== release gate =="
npm run release:check

current_branch="$(git branch --show-current)"
if [[ "$current_branch" != "main" ]]; then
  echo "Expected branch main, got ${current_branch}." >&2
  exit 1
fi

if ! gh repo view "${OWNER}/${REPO}" >/dev/null 2>&1; then
  if [[ "$VISIBILITY" == "public" ]]; then
    gh repo create "${OWNER}/${REPO}" --public --source=. --remote=origin --push
  else
    gh repo create "${OWNER}/${REPO}" --private --source=. --remote=origin --push
  fi
else
  if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "https://github.com/${OWNER}/${REPO}.git"
  fi
  git push -u origin main
fi

echo "published: https://github.com/${OWNER}/${REPO}"

