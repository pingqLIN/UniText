---
runtime_projection: true
source_of_truth: registry/skills/ai-first-readiness-review/references/report-template.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/ai-first-readiness-review/references/report-template.md`
> Source of truth: `registry/skills/ai-first-readiness-review/references/report-template.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Report Template

Use this structure for a formal AI-first readiness review.

## Scope

- Target:
- In-scope paths or systems:
- Assumptions:

## Current-State Summary

- What the system is trying to do
- How operators currently interact with it
- Where AI-first strengths already exist

## Findings

### [Severity] Title

- Evidence:
- Why it matters for AI-first operation:
- Why it matters for human operators:
- Recommended change:

Repeat for each finding, ordered from highest to lowest severity.

## Readiness By Dimension

- Agent comprehension:
- Document retrieval and reading ergonomics:
- Tool operability:
- Vendor-neutral abstraction:
- Human-AI-process communication:

Use short judgments such as `strong`, `adequate`, `fragile`, or `failing`.

## Recommended Plan

### Now

- Smallest changes needed to unblock reliable AI operation

### Next

- Structural improvements that increase speed, clarity, and portability

### Later

- Experience, compression, and optimization work

## Communication Layer Decision

- Is the current human-AI-process communication baseline sufficient?
- If no, what platform or layer should be added?
- What minimum records or messages must it carry?

## Residual Risks

- What remains risky after the proposed changes
- Which assumptions still need confirmation
