# UniText Project Status Report — 2026-04-26

> Scope: local development status, related worktree impact, and adjacent project risk review.
> Publication: local-only until explicitly approved by the user.

## Current Repo State

- Repo: `Q:\UniText`
- Branch: `main`
- Remote state: `main...origin/main [ahead 52]`
- Worktree before this report: clean
- Worktree after this report: local tracked changes only; no push performed

The project is currently on the runtime-first baseline:

- `RUNTIME.md` and `runtime/START.md` are the consumer-agent startup surface.
- `registry/` remains the canonical authoring source.
- `runtime/` is the tracked read model used by consumer agents.
- `local/` owns machine-local wiring and delivery targets.

## Verification Run

Commands run from `Q:\UniText`:

```powershell
python local/scripts/verify-bootstrap.py
python -m unittest discover -s tests -p "test*.py"
```

Results:

- `verify-bootstrap.py`: `ok = true`
- `unittest discover`: `68 tests`, `OK`, `skipped=1`
- Known warning: Git reports line-ending warnings for some tracked text files when touched; this did not fail the test gate.

## Related Project Check

### `Q:\Projects\skills-governance`

Observed state:

- Branch: `main`
- Latest commit: `929a077 Bootstrap skills-governance`
- Git ownership requires one-off safe-directory reads from the current Windows user.

Impact on UniText:

- This project is configured to scan `Q:\UniText\registry\skills`.
- It must remain a read-only governance/reporting tool by default.
- It should not directly mutate UniText registry contents unless a specific change workflow is approved.

Validation:

```powershell
pwsh -NoProfile -File scripts/sg.ps1 scan
```

Initial result:

- `total=54 ok=53 fail=1 warn=54`
- Failure: `registry/skills/azure-aigateway/SKILL.md` had top-level `compatibility` frontmatter.

Fix applied in UniText:

- Moved `compatibility` under `metadata.compatibility` in:
  - `registry/skills/azure-aigateway/SKILL.md`
  - `runtime/skills/azure-aigateway/SKILL.md`

Post-fix result:

- `total=54 ok=54 fail=0 warn=54`

The remaining warnings are governance quality warnings, not hard failures.

### `Q:\UniText-wt-bugfix`

Observed state:

- Branch: `fix/revamp-regressions`
- Status: `ahead 1, behind 17` relative to `origin/main`
- Unique local commit: `646847f fix: align bootstrap with runtime bundle baseline`

Impact:

- This worktree should not be used for new edits until its relationship to current `main` is reviewed.
- It may contain a narrow bootstrap/runtime fix that is not an ancestor of current `main`.

Recommended next action:

- Compare `646847f` against current `main`.
- Either cherry-pick the still-relevant fix into `main`, or archive the branch if current `main` already supersedes it.

### `Q:\UniText-wt-dev`

Observed state:

- Detached HEAD at `d6774e1`
- That commit is an ancestor of current `main`.

Impact:

- Treat as a read-only historical/dev checkout until it is reattached or retired.
- Do not commit new work there while detached.

Recommended next action:

- Retire or rebase into a named branch only if there is a concrete task requiring it.

### `Q:\UniText-wt-ui`

Observed state:

- Branch: `feature/interface-console`
- Unique commits:
  - `9e33762 feat: polish governance console controls`
  - `3cce79d Refine project map tone previews`
  - `c548818 Refine project map browse workspace`
  - `8f6c726 Refine governance workspace and structured rules`

Impact:

- UI/governance console work may still contain useful commits outside current `main`.
- Current `main` has newer runtime-first and registry governance work, so direct merge should be reviewed carefully.

Recommended next action:

- Review the four unique UI commits against current project-map runtime code.
- Cherry-pick only still-relevant UI improvements after running `node --check local/scripts/project-map-runtime.js` and project-map output tests.

### `Q:\Projects\dbos-ai-evaluation-poc`

Observed state:

- Branch: `main`
- Git ownership requires one-off safe-directory reads from the current Windows user.
- Dirty state: untracked `tests/conftest.py` and `tests/test_agent_poc.py`
- Test result: `7 passed`

Impact on UniText:

- This is already present as an isolated PoC; it should not be installed into or merged with UniText directly.
- Primary risks are dependency installation, secret handling, DBOS state files, and durable workflow side effects.
- The PoC depends on `dbos`, `dbos-openai-agents`, and `openai-agents`.
- Runtime secrets must remain in environment variables or local ignored files; do not copy `.env` or DBOS state into UniText.

Recommended boundary:

- Keep DBOS evaluation in `Q:\Projects\dbos-ai-evaluation-poc`.
- If UniText later adopts DBOS-backed workflows, add a separate optional runner or workflow adapter rather than changing the runtime-first baseline.
- Candidate UniText use cases are long-running agent loops, review package exports, rebuild package verification, and human-gated governance workflows.

## Next Development Priorities

1. Review the `ahead 52` local commit batch before any push or publication.
2. Decide whether `fix/revamp-regressions` commit `646847f` is still needed on `main`.
3. Review `feature/interface-console` unique UI commits for selective adoption.
4. Keep `skills-governance` as a read-only quality gate and add it to the regular verification path once warning policy is defined.
5. Keep DBOS isolated until the PoC proves crash/restart recovery and side-effect idempotency.

