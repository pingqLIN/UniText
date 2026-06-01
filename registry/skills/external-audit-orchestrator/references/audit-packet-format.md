---
---

# Audit Packet Format

The audit packet is the handoff artifact between the developer agent and the external reviewer.

Use this shape:

1. `Audit Goal`
2. `Scope`
3. `Project Context`
4. `Change Evidence`
5. `Checks Already Run`
6. `Questions For Reviewer`
7. `Reference Inputs`
8. `Expected Output Format`

## Scope examples

- `working-tree`
- `staged`
- `commit-range: abc123..def456`
- `path: src/auth`
- `manual-question: review deployment plan only`

## Change evidence

Prefer real evidence:

- `git status --short --branch`
- `git diff`
- `git diff --staged`
- file paths
- test outputs
- lint outputs

## Questions for reviewer

Keep them concrete:

- Are there blocking bugs or regressions?
- Are there security concerns?
- Is the rollback path obvious?
- Did we borrow patterns from another project incorrectly?

## Expected output format

Require:

- findings ordered by severity
- file/path references when possible
- explicit assumptions
- `Reference Inputs` acknowledgment when relevant
