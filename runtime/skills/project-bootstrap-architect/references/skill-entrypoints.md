---
runtime_projection: true
source_of_truth: registry/skills/project-bootstrap-architect/references/skill-entrypoints.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/project-bootstrap-architect/references/skill-entrypoints.md`
> Source of truth: `registry/skills/project-bootstrap-architect/references/skill-entrypoints.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Skill Entrypoints and Consolidation

Use this reference when a new project needs skill selection, skill creation, or skill-governance setup.

## Current Entrypoint Types

| Entry | Type | Meaning | Recommended use |
| --- | --- | --- | --- |
| `skill-creator` `[Plugin] Plugin - skills` | plugin bundle | A plugin package that contributes one or more skills and possibly support tooling. It is a distribution surface, not the authoring workflow by itself. | Keep as packaging/provenance metadata. Do not use as the primary authoring decision point. |
| `Skill Creator` `[Skill] Create or update a skill` | UI display name | Human-facing label for the current Codex-oriented `skill-creator` skill. | Use as the default authoring entry when creating or updating a skill. |
| `Skill Installer` `[Skill] Install curated skills from openai/skills or other repos` | installer skill | Fetches and installs skills from curated or external sources. | Use only when the task is installation/adoption, not skill design. |
| `skill-creator` `[Skill] Guide for creating effective skills...` | canonical skill id | The actual skill name/id used for authoring workflows. In this environment, prefer the `.system` Codex-oriented copy when present. | Default for new skill authoring and normal updates. |
| `skill-creator (skill-crea...)` `[Skill] Create new skills, modify... measure performance...` | plugin-provided advanced skill | Skill-creator plugin route with broader evaluation, measurement, and optimization language. | Use for advanced eval, benchmark, or performance-improvement work after the basic skill exists. |

## Consolidation Recommendation

Use one visible primary route:

- Primary authoring id: `skill-creator`
- UI display name: `Skill Creator`
- Installer stays separate: `skill-installer`
- Plugin entry stays as provenance/package surface, not a user-facing duplicate route
- Advanced eval/benchmark features should be linked as an explicit advanced path from the primary `skill-creator`

## Execution Model

1. For a new skill, start with `skill-creator`.
2. If the task is "install this existing skill", use `skill-installer`.
3. If the task is "improve skill performance" or "run evals", route to the plugin-era advanced path.
4. If the skill must be shared through UniText, place it in `Q:\UniText\registry\skills\<skill-id>`.
5. If the skill must be locally `$` discoverable, also install or project it into the active local skills path. Registry placement alone is not enough.

## New Project Bootstrap Rule

When bootstrapping a new project that will define AI-agent workflow, record:

- which skill is the project entrypoint
- whether it is shared registry, local-only, or both
- whether runtime projection is required
- whether installer support is needed
- whether eval/benchmark support is needed
