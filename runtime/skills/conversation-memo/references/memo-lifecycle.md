---
runtime_projection: true
source_of_truth: registry/skills/conversation-memo/references/memo-lifecycle.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/conversation-memo/references/memo-lifecycle.md`
> Source of truth: `registry/skills/conversation-memo/references/memo-lifecycle.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Memo Lifecycle

## Raw archive comes first

For memo-worthy discussions, preserve the full raw conversation before summarizing.

Default raw archive root:

- `C:\Users\miles\.agents\.little_talks`

Suggested filename:

- `YYYY-MM-DD_<topic-slug>.md`

Examples:

- `2026-04-19_obsidian-indexing-architecture.md`
- `2026-04-19_control-layering-discussion.md`

## Minimum raw archive expectations

- complete chronological transcript when available
- explicit note if the capture is partial
- no summary-only replacement of the raw source

## Memo requirements

Every memo should include:

1. purpose or background
2. key distilled points
3. preferred direction or decision tendency
4. unresolved issues
5. candidate formal outputs
6. raw archive path or link

## Optional downstream handoff

When the memo will feed downstream automation, add a structured handoff artifact alongside the prose memo.

Suggested handoff contents:

1. schema identifier
2. creation timestamp
3. raw archive path
4. summary memo path
5. topic or project metadata
6. candidate formal outputs

This handoff is not a substitute for the memo. It is a machine-friendly bridge for later adapters.

## Memo is not formal output

The memo is the reasoning bridge between raw discussion and later formalization.

It should not silently become:

- policy
- specification
- implementation note
- code change

Those are downstream outputs and should be named separately.

## Placement guidance

- if the repo has document-placement policy, follow it
- if the note is still exploratory, keep it in an authoring / working-notes layer
- only promote it after rewriting it into sanitized, canonical form
