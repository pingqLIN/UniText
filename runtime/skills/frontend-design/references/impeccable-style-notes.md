---
runtime_projection: true
source_of_truth: registry/skills/frontend-design/references/impeccable-style-notes.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/frontend-design/references/impeccable-style-notes.md`
> Source of truth: `registry/skills/frontend-design/references/impeccable-style-notes.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Impeccable Style Notes

Purpose: distilled notes from reviewing `https://impeccable.style/` so `frontend-design` can absorb the useful parts without breaking registry compatibility.

## Compatibility Decision

- Upstream positions `impeccable` as the upgrade path and rename for `frontend-design`
- UniText keeps the skill id `frontend-design` for compatibility with existing shortlist, catalog, and references
- The registry absorbs the stronger workflow ideas instead of renaming the skill immediately
- Trigger coverage should still recognize `impeccable` and `impeccable.style` through `SKILL.md` description language

## High-Signal Ideas To Keep

- Design quality improves when the model gathers context before composing UI
- A deliberate anti-attractor step prevents reflexive AI UI patterns
- Reviewing existing UI through critique, polish, and hardening passes is as important as greenfield generation
- The best results come from a named aesthetic thesis, not from "make it modern"

## Anti-Pattern Clusters

Watch for these recurring failure modes:

- safe-default typography with no point of view
- purple/cyan startup palette by reflex
- centered hero plus two CTAs plus shallow social-proof strip
- repeated feature-card grids with icon tile above heading
- nested cards, nested shadows, and low-signal glassmorphism
- gradient text or glow accents used as decoration instead of hierarchy
- weak spacing rhythm with everything feeling evenly padded
- motion that is everywhere but says nothing
- dark mode chosen as a shortcut to "designed"
- mobile layouts that merely stack desktop blocks without recomposition

## Useful Mental Modes

The site frames several modes as separate commands. For UniText, treat them as internal passes rather than separate skills:

- `impeccable`: full generation or redesign pass
- `critique`: identify generic patterns, weak hierarchy, and layout drift
- `polish`: refine spacing, typography, rhythm, and visual cohesion
- `harden`: check responsiveness, interaction states, accessibility, and implementation realism
- `teach`: explain why the design decisions work

## When To Consult These Notes

Load these notes when:

- the user explicitly references `impeccable` or `impeccable.style`
- the current concept feels template-like or "AI generated"
- the task is a redesign or critique of an existing frontend
- the user asks for a stronger, more authored visual point of view
