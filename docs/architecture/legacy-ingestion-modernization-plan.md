# Legacy Ingestion / Modernization Plan

> Status: proposed follow-on plan
> Date: 2026-04-20
> Relationship to runtime-reset: separate stream

## Purpose

Treat every legacy repo or pre-UniText workspace as a new input source.

Do not fold legacy cleanup into the runtime-reset baseline path. The new baseline is already the target platform. Legacy work should be a separate intake, extraction, rebuild, and verification flow.

## Non-Goals

- do not reopen the runtime-reset architecture decision
- do not let legacy path quirks redefine the new baseline
- do not bulk-import old repo structure directly into `registry/` or `runtime/`
- do not skip review gates just because a legacy repo already “worked before”

## Operating Boundary

Use this split:

- `runtime-reset baseline`
  - defines the target operating model
  - already owns `runtime/`, runtime-first docs, bootstrap, and verify
- `legacy ingestion`
  - inspects old repos as external inputs
  - extracts reusable assets
  - rebuilds them against the new baseline

The legacy stream should fail closed. If classification is unclear, stop at review instead of guessing.

## Phase 1: Intake Scan

Goal:

- understand what the legacy repo contains before adopting anything

Checklist:

- detect repo root, branch, worktree cleanliness, and active Git state
- inventory languages, package managers, scripts, CI files, infra files, and `.env` patterns
- identify candidate reusable assets:
  - skills
  - MCP servers
  - agents
  - workflow docs
  - governance docs
- flag sensitive or local-only material:
  - machine paths
  - local callback URLs
  - author accounts
  - secrets or secret-bearing examples

Expected outputs:

- `ops/reports/legacy-intake/<repo-slug>/inventory.json`
- `ops/reports/legacy-intake/<repo-slug>/classification.md`

## Phase 2: Classify

Every legacy artifact must be assigned to one of these buckets:

- `canonical-candidate`
  - reusable shared knowledge worth extracting into `registry/`
- `runtime-only-candidate`
  - useful consumer-facing guidance that should become a runtime projection or runtime doc after canonical extraction
- `local-only`
  - machine-specific wiring, host notes, personal baselines
- `ops-only`
  - evidence, logs, migration transcripts
- `reject`
  - stale, duplicated, or unsafe material

Gate:

- nothing moves forward without explicit classification
- ambiguous items stop in review

## Phase 3: Extract

Rules:

- extract content into a staging area first
- preserve provenance back to the legacy source repo and path
- normalize names, frontmatter, and link structure before adoption

Preferred staging artifacts:

- `ops/reports/legacy-intake/<repo-slug>/candidate-map.json`
- `ops/reports/legacy-intake/<repo-slug>/source-provenance.md`

## Phase 4: Rebuild Against The New Baseline

Rebuild, do not retrofit.

Typical actions:

- turn accepted skills into proper `registry/skills/<id>/SKILL.md`
- turn reusable MCP definitions into `registry/mcp/<id>/`
- rewrite docs to match current placement and boundary policy
- regenerate `runtime/` through `build-runtime-layer.py`
- keep machine-local delivery in `local/` only

Success condition:

- the extracted asset reads like a native UniText resource, not a pasted legacy fragment

## Phase 5: Verify

Minimum verify set for each modernization batch:

- `python local/scripts/build-runtime-layer.py --write`
- `python local/scripts/bootstrap.py --dry-run`
- `python local/scripts/verify-bootstrap.py`
- targeted boundary check for sensitive metadata
- targeted acceptance-task replay for any changed runtime route

If the change touches startup, routing, or source hygiene:

- replay the relevant tasks from `runtime/validation/tasks.md`
- write evidence to `ops/reports/agent-runtime-eval/<timestamp>/`

## Phase 6: Review And Promote

Promotion rules:

- each modernization batch should have a small, reviewable diff
- provenance must be visible
- low-confidence extractions stay out
- publishability and template-safety checks happen before any release-oriented commit boundary

## Suggested Execution Slice

Process legacy repos in this order:

1. smallest repo with the clearest reusable asset shape
2. repo with the highest runtime overlap
3. repo with the most boundary risk only after the flow has already been rehearsed on easier inputs

This keeps the first modernization cycle short and teaches the intake model before higher-risk repos arrive.

## Commit Boundaries For The Current Worktree

Recommended order:

1. `runtime-reset core`
   - `RUNTIME.md`
   - `runtime/**`
   - `local/scripts/build-runtime-layer.py`
   - `local/scripts/bootstrap.py`
   - `local/scripts/verify-bootstrap.py`
   - `local/scripts/sync-skills.ps1`
   - `README.md`
   - `INDEX.md`
   - `OPERATIONS.md`
   - `local/scripts/README.md`
   - `local/docs/CLI_COMPAT_MATRIX.md`
2. `runtime boundary and seed hygiene`
   - `SECRET_HANDLING_GUIDELINES.md`
   - `TEMPLATE_RELEASE_CHECKLIST.md`
   - `AGENT_GOVERNANCE_LAYERING.md`
   - `registry/mcp/claude-project-mcp-seed/**`
   - `template/examples/local/README.md`
3. `runtime-reset architecture record`
   - `docs/architecture/agent-runtime-reset/**`
   - `MILESTONES.md`
   - `PROJECT_STATUS_REPORT_2026-03-23.md`
4. `post-cutover follow-up planning`
   - `docs/architecture/legacy-ingestion-modernization-plan.md`
   - any future full acceptance-run evidence summary intended to be tracked

## Acceptance For This Plan

The plan is ready to execute when:

- the runtime-reset baseline stays unchanged while legacy work is scoped
- the first target legacy repo is named
- intake outputs are defined before extraction starts
- commit boundaries remain small enough that runtime-reset and legacy work can still be reviewed independently
