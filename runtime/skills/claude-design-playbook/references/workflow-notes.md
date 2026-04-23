---
runtime_projection: true
source_of_truth: registry/skills/claude-design-playbook/references/workflow-notes.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/claude-design-playbook/references/workflow-notes.md`
> Source of truth: `registry/skills/claude-design-playbook/references/workflow-notes.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Workflow Notes

## Recommended chaining

- `family-picker` -> `brand-to-design-md`
- `brand-to-design-md` -> `audit-live-site-against-design-md`
- `brand-to-design-md` + `brand-to-design-md` -> `remix-two-brands`

## Evidence-first rules

- If the user gives a URL, prioritize rendered evidence.
- If the user gives screenshots only, stay conservative about motion and hidden states.
- If the user gives an existing `DESIGN.md`, audit against it instead of regenerating it unless asked.

## Remix notes

- A useful remix usually keeps one parent's typography and one parent's accent, not both from both.
- The strongest remixes come from families with productive tension:
  - `Editorial Minimalism` x `Warm Editorial`
  - `Terminal-Core` x `Data-Dense Pro`
  - `Glass / Soft-Futurism` x `Cinematic Dark`

## Implementation handoff

When the user wants real frontend code after the system is chosen:

1. summarize the chosen family or `DESIGN.md` into 5-8 implementation constraints
2. preserve key token rules and rejection cues
3. hand off to `frontend-design`

## Anti-slop bridge

- Keep anti-slop guidance tied to the selected family or system.
- For broader prompt craft, refer to Anthropic's frontend aesthetics cookbook.
- For implementation-phase aesthetics and production UI code, refer to `frontend-design`.
