---
runtime_projection: true
source_of_truth: registry/skills/conversation-memo/references/conversation-memo-handoff-schema.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/conversation-memo/references/conversation-memo-handoff-schema.md`
> Source of truth: `registry/skills/conversation-memo/references/conversation-memo-handoff-schema.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Conversation Memo Handoff Schema

## Purpose

`conversation-memo-handoff` is the bridge artifact between:

- `conversation-memo`
- downstream adapters such as `obsidian-index-adapter`

It preserves the completed memo state in a structured form so downstream adapters do not need to scrape prose documents.

## Schema identifier

```json
"schemaVersion": "conversation-memo-handoff/v1"
```

## Required fields

```json
{
  "schemaVersion": "conversation-memo-handoff/v1",
  "createdAt": "2026-04-19T08:00:00+08:00",
  "source": {
    "rawArchivePath": "<raw-archive-path>",
    "summaryMemoPath": "<summary-memo-path>"
  },
  "memo": {
    "topic": "<topic-slug>",
    "project": "<project-name>",
    "tags": [
      "agents",
      "memo",
      "<topic-tag>"
    ],
    "candidateFormalOutputs": [
      "<formal-output-1>",
      "<formal-output-2>"
    ]
  }
}
```

## Intent

The handoff should carry:

- the authoritative raw archive path
- the authoritative summary memo path
- enough metadata to seed a downstream index note or adapter payload
- likely formal outputs without forcing them into canonical state too early

## Downstream rules

The handoff does not include vault authority by default.

Downstream adapters should still require explicit inputs such as:

- `vault_name`
- `vault_root`
- `note_type`
- `target_path`

This keeps vault control separate from memo capture.

## Current recommended flow

1. Preserve raw archive
2. Write summary memo
3. Write `conversation-memo-handoff` when downstream automation needs a stable machine-friendly bridge
4. Feed that handoff to a downstream adapter such as `obsidian-index-adapter`
