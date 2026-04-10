# AGENTS.md

## No-Publish Rule

This repository contains materials that may remain private unless the user gives explicit permission.

Agents operating in this repository MUST follow these rules:

1. Do not push commits to any remote unless the user explicitly asks for that push.
2. Do not upload repository content to GitHub, social platforms, cloud docs, paste sites, or any other network service unless the user explicitly asks for that upload.
3. Treat the following as especially sensitive by default:
   - social post drafts
   - project comparison notes
   - cross-project collaboration discussions
   - review notes
   - strategic planning documents
4. If the user asks for publishing, push, upload, or posting, only publish the specific content the user approved.
5. When in doubt, keep content local and ask before publishing.

## Scope Note

This policy applies even when:

- a remote already exists
- the repository is private
- the content appears ready for publication

Private repository does not equal automatic permission to publish.

## Git Startup

For a new development session in this repository, prefer:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\git-startup.ps1
```

This helper resolves the canonical base branch from `origin/HEAD` first, then falls back to local `main` or `master` only when needed. It also enforces a clean working tree, fetches `origin --prune`, fast-forwards explicitly against the resolved base branch, and refuses to reuse an existing feature branch name.
