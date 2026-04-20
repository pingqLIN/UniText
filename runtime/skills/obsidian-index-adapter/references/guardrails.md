---
runtime_projection: true
source_of_truth: registry/skills/obsidian-index-adapter/references/guardrails.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/obsidian-index-adapter/references/guardrails.md`
> Source of truth: `registry/skills/obsidian-index-adapter/references/guardrails.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Guardrails

## Core restrictions

The adapter must:

- fail if `vault_name` is missing
- fail if `vault_root` is missing
- fail if `target_path` is outside the whitelist
- fail if `raw_archive_path` does not exist
- fail if `summary_memo_path` does not exist

The adapter must not:

- write the first copy of the discussion into Obsidian
- treat the vault as the only source of truth
- rely on the last-focused vault as implicit context
- freely append to arbitrary existing notes
- inline the full raw transcript by default

## Allowed note types

Initial allowed note types:

- `conversation-index-note`
- `topic-index-note`
- `project-memo-index-note`

Reject anything else until the policy is expanded.

## Path whitelist

Allowed vault locations in v1:

- `Inbox/Agent Memos/`
- `Indexes/Conversations/`
- `Projects/<project>/Memos/`

Do not allow freeform writes outside the whitelist.
