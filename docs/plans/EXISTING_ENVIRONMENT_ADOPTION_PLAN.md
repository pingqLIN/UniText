# Existing Environment Adoption Plan

> Status: proposed adoption baseline
> Audience: operators bringing UniText into an already-working local environment

## Purpose

Let a user adopt UniText without forcing an all-at-once migration.

This plan answers two questions:

1. how to attach UniText to an existing working environment smoothly
2. when a newly introduced skill or MCP should stay local, stay project-local, or be promoted into the governed UniText registry

Default rule:

- start with the lightest lane that preserves the user's current environment
- promote into shared registry only after the asset proves reusable, reviewable, and share-safe

## Lane Selection

Every incoming asset should be assigned to exactly one lane before any tracked change is made.

| Lane | Use when | Primary landing surface | Do not do |
|---|---|---|---|
| `Lane A: local-only overlay` | the asset is machine-specific, user-specific, experimental, or not yet review-ready | user host config, active CLI skills dir, ignored local notes, local drafts | do not add it to `registry/` or `runtime/` |
| `Lane B: project-local MCP / project companion` | the asset is useful for one repo or one delivery context but not yet a shared UniText baseline | target project `.mcp.json`, target project docs, repo-local companion notes | do not present it as shared canonical truth |
| `Lane C: governed registry promotion` | the asset is reusable across projects or operators and can survive review as template-safe shared knowledge | `registry/skills/<id>/` or `registry/mcp/<id>/`, then rebuilt `runtime/` | do not skip review, provenance, or verify |

## Recommended Adoption Sequence

### Phase 1: Intake the current environment

Capture the current state before changing anything:

- active CLIs and where they currently read skills or MCP config
- existing project-local MCP files
- machine-specific paths, callback URLs, secrets, author accounts, and private wrappers
- which existing skills or MCPs are already relied on in day-to-day work

If an asset contains machine paths, personal accounts, or host-only wiring, default it to `Lane A` until proven otherwise.

### Phase 2: Choose the smallest viable lane

Use these defaults:

- if the user only wants to try UniText in their current machine workflow, start with `Lane A`
- if the asset only belongs to one active project, use `Lane B`
- only use `Lane C` after the asset has passed review and can be described without local-only values

### Phase 3: Dry-run before mutation

Use the existing repo control flow before tracked delivery:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/verify-bootstrap.py
```

For `Lane B`, also inspect the target project's local MCP surface before writing anything.

### Phase 4: Deliver through the chosen lane

- `Lane A`
  - install or wire locally only
  - keep notes in local-only surfaces when needed
  - do not create tracked registry entries yet
- `Lane B`
  - keep the asset attached to the target project
  - separate machine-local values from tracked project files
  - treat it as a project companion, not a shared UniText baseline
- `Lane C`
  - adopt into `registry/`
  - rebuild `runtime/`
  - run bootstrap / verify
  - keep the diff reviewable and provenance-visible

## Promotion Gate For New Skills And MCPs

A new skill or MCP can move from `Lane A` or `Lane B` into `Lane C` only when all of the following are true:

- the asset is reusable outside one machine or one temporary experiment
- no required value depends on plaintext secrets, private callback URLs, or personal absolute paths
- a canonical `id` and source/provenance can be stated clearly
- the content can be reviewed as template-safe shared knowledge
- the asset passes `local/docs/ADOPTION_CHECKLIST.md`
- the placement matches `DOCUMENT_PLACEMENT_POLICY.md`

If any item is false or unclear:

- keep it out of `registry/`
- stop at review instead of guessing

## Commit Boundaries

Keep adoption work reviewable by separating:

1. lane-selection or governance-doc updates
2. actual registry adoption of a new skill or MCP
3. runtime rebuild and delivery verification

Do not mix a broad intake sweep, a new canonical resource, and unrelated UI or bootstrap work into the same commit.
