---
runtime_projection: true
source_of_truth: registry/skills/obsidian-index-adapter/references/note-schema.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/obsidian-index-adapter/references/note-schema.md`
> Source of truth: `registry/skills/obsidian-index-adapter/references/note-schema.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Note Schema

## Frontmatter

Minimum frontmatter for a `conversation-index-note`:

```yaml
---
type: conversation-index-note
status: indexed
date: 2026-04-19
topic: <topic-slug>
project: <project-name>
raw_archive: "<raw-archive-path>"
summary_memo: "<summary-memo-path>"
formal_outputs: []
tags:
  - agents
  - memo
  - <topic-tag>
---
```

## Body template

Minimum body:

```md
# <Topic Title>

## Summary
- Brief memo summary.

## Source Links
- Raw archive: `...`
- Summary memo: `...`

## Candidate Formal Outputs
- reference doc
- implementation assessment

## Formalization Status
- pending
```

## Output intent

The note should be:

- index-oriented
- concise
- source-linked
- safe to regenerate from upstream artifacts

It should not replace the memo or the formal document.
