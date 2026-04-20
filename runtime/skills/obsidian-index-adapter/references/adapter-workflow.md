---
runtime_projection: true
source_of_truth: registry/skills/obsidian-index-adapter/references/adapter-workflow.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/obsidian-index-adapter/references/adapter-workflow.md`
> Source of truth: `registry/skills/obsidian-index-adapter/references/adapter-workflow.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Adapter Workflow

## Position in the pipeline

`obsidian-index-adapter` runs only after:

1. a raw archive exists
2. a summary memo exists

Default lifecycle:

- raw archive
- summary memo
- formalization candidates
- optional Obsidian index note

## Required inputs

Every invocation must provide:

- `vault_name`
- `vault_root`
- `note_type`
- `target_path`
- `raw_archive_path`
- `summary_memo_path`

Optional inputs:

- `topic`
- `project`
- `formal_outputs`
- `tags`

## Recommended implementation order

Build capabilities in this order:

1. `create-index-note`
2. `link-formal-output`
3. `create-topic-note`
4. `refresh-index-status`

Do not add freeform vault writing in v1.

## Invocation posture

Prefer a wrapper or adapter layer that normalizes and validates inputs before any Obsidian CLI call.

Recommended posture:

- install upstream Obsidian skills if needed
- do not expose upstream freeform vault writing directly in the memo pipeline
- always require explicit vault and path inputs
