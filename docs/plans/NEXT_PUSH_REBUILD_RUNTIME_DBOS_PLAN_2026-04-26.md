# Next Push Rebuild, Runtime Generator, and DBOS Adoption Plan — 2026-04-26

> Scope: next-stage task plan for `Q:\UniText`.
> Status: planning document only; no push, rebuild, DBOS adoption, or remote publication is authorized by this document.

## 0. Current Decision Summary

1. The next push is expected to be a direct rebuild-oriented push.
2. `build-runtime-layer.py --write` must be discussed and evaluated again before it is used as a normal write path.
3. `Q:\Projects\dbos-ai-evaluation-poc` remains an adjacent isolated PoC; the adoption depth into UniText must be decided explicitly.

Current repo state at planning time:

- `Q:\UniText` branch: `main`
- Remote state: `main...origin/main [ahead 58]`
- No remote push has been performed.
- UniText runtime/bootstrap/test health is currently good, but runtime generator write behavior is not yet a safe routine operation.

## 1. Next Push Strategy: Direct Rebuild Track

### Goal

Prepare the next push as a rebuild-oriented publication batch instead of a small incremental sync.

### Meaning of "Direct Rebuild"

For the next push, treat the remote update as a rebuilt baseline candidate:

- verify the complete local state, not only the latest commit
- regenerate or validate release-facing artifacts intentionally
- confirm no local-only, DBOS state, secret, ops history, or machine-specific files are crossing the publish boundary
- produce an explicit push suitability report before any remote action

### Required Pre-Push Gates

Run these before push discussion:

```powershell
git status --short --branch
python local/scripts/verify-bootstrap.py
python -m unittest discover -s tests -p "test*.py"
pwsh -NoProfile -File Q:\Projects\skills-governance\scripts\sg.ps1 scan
```

Then run the repo-local publication checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\get-publishability-report.ps1
```

If rebuild/export artifacts are part of the push package, also run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-rebuild-project.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-rebuild-project.ps1
```

### Stop Conditions

Do not push if any of these are true:

- `git status` is dirty with unexplained changes
- `verify-bootstrap.py` does not return `ok = true`
- `skills-governance` reports any hard failures
- publishability or workspace boundary checks identify local-only content in tracked shared surfaces
- DBOS secrets, DBOS state files, local `.env`, sqlite state, or unreviewed PoC files appear in the push set

## 2. Runtime Generator Rebuild Assessment

### Current Problem

`build-runtime-layer.py --write` is currently a destructive full projection writer:

- it deletes `runtime/skills`
- it deletes `runtime/agents`
- it deletes `runtime/workflow`
- it rebuilds those folders from `registry/`
- it refreshes `runtime/catalog.json`

This is conceptually valid for a generated runtime layer, but current tracked runtime contents and current generator output are not fully aligned. Running `--write` during a small skill fix produced a very large runtime deletion/rewrite diff, so it is not safe to treat it as a routine post-edit command yet.

### Assessment Questions

Before enabling routine `--write`, answer:

1. Is `runtime/` intended to be fully generated from `registry/`, with no tracked runtime-only files?
2. If yes, what tracked runtime files currently exist that the generator does not reproduce?
3. If no, which runtime-only files are authoritative and must be preserved?
4. Should `build-runtime-layer.py` become idempotent against the tracked baseline?
5. Should `--write` support a dry-run diff report before writing?
6. Should small registry edits update only matching runtime projections instead of full rebuild?

### Proposed Evaluation Steps

1. Run dry summary only:

```powershell
python local/scripts/build-runtime-layer.py
```

2. Generate into a temporary output or scratch worktree instead of overwriting tracked `runtime/`.

Required implementation option:

- add `--output-dir <path>` or equivalent dry-run materialization mode
- compare generated output against tracked `runtime/`
- classify differences into:
  - expected projection changes
  - missing generator coverage
  - stale tracked runtime files
  - line-ending/noise-only changes

3. Add a test that proves `--write` or the new materialization mode is idempotent for the current baseline.

4. Only after the diff is understood, decide whether to:

- update the generator
- update the tracked runtime baseline
- add preserve rules
- split full rebuild from single-resource projection

### Acceptance Criteria

Runtime generator work is complete when:

- generated runtime output can be compared without modifying tracked files
- expected vs unexpected drift is machine-readable
- full rebuild produces a reviewable diff
- `verify-bootstrap.py` still reports `ok = true`
- tests cover the new behavior

## 3. DBOS Adoption Depth Evaluation

### Current Boundary

`Q:\Projects\dbos-ai-evaluation-poc` is not currently part of UniText runtime.

It is:

- an adjacent isolated PoC
- referenced only in UniText status planning docs
- not in `runtime/catalog.json`
- not in `registry/skills`
- not in `registry/mcp`
- not in `local/config/integration-surfaces.json`
- not part of `bootstrap.py` or `verify-bootstrap.py`

### Why DBOS Might Matter

DBOS may be useful if UniText needs durable, recoverable workflows for:

- long-running agent development loops
- rebuild/export package pipelines
- review package generation
- human-gated governance workflows
- crash/restart recovery for multi-step automation

DBOS is not justified for:

- short stateless scripts
- simple validation commands
- routine local-only checks that can safely restart from the beginning

### Adoption Levels

#### Level 0: Keep Isolated

DBOS remains only in `Q:\Projects\dbos-ai-evaluation-poc`.

Use when:

- crash/restart behavior is not proven
- side-effect idempotency is not proven
- dependencies or secrets are still under evaluation

#### Level 1: Documented Candidate

UniText documents DBOS as a candidate runtime option, but no code imports it.

Allowed changes:

- docs only
- status report
- decision record
- candidate workflow list

#### Level 2: Optional Adapter

UniText adds an optional DBOS-backed runner path for one workflow.

Constraints:

- no default dependency on DBOS
- no bootstrap requirement
- feature flag or separate command
- existing runner remains unchanged
- state path is local/ignored
- secrets stay outside tracked repo

Candidate workflow:

- rebuild/export pipeline with durable checkpoints

#### Level 3: Managed Runtime Surface

DBOS becomes an official runtime integration surface.

This requires:

- explicit approval
- dependency policy
- state storage policy
- Postgres or other production-ready state decision
- security review
- migration/rollback plan

### DBOS Go / No-Go Gates

Before moving beyond Level 1, prove in the PoC:

- SQLite local run works
- crash/restart recovery works
- completed steps do not rerun unexpectedly
- one real side-effect step is idempotent
- OpenAI/API secrets stay out of tracked files
- DBOS state files are ignored/local-only
- tests pass in `Q:\Projects\dbos-ai-evaluation-poc`

## 4. Recommended Next Task Order

1. Freeze the current UniText push set for review.
2. Produce a push suitability report for the `ahead 58` local commits.
3. Add a runtime generator evaluation mode that can materialize output to a scratch folder.
4. Compare generated runtime output against tracked `runtime/`.
5. Decide whether direct rebuild means updating generator, updating tracked runtime, or both.
6. Keep DBOS at Level 0 until its PoC proves crash/restart and side-effect safety.
7. Revisit DBOS Level 1 documentation only after the runtime generator question is no longer blocking the next push.

## 5. Working Rule For The Next Session

Do not run:

```powershell
python local/scripts/build-runtime-layer.py --write
```

as a casual repair command.

Instead, first implement or simulate a scratch-output comparison path, review the generated diff, and only then decide whether to rebuild tracked `runtime/`.

