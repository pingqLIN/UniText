---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/references/source-attribution-policy.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/references/source-attribution-policy.md`
> Source of truth: `registry/skills/external-audit-orchestrator/references/source-attribution-policy.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
﻿---
---

# Source Attribution Policy

Every audit output must include a `Reference Inputs` section when any external or cross-project material affected the work.

## When attribution is required

Attribution is required if any of these happened:

- another local project was inspected
- an external repository or skill page influenced the recommendation
- official vendor docs affected the audit mode or procedure
- copied or adapted prompt structure, reviewer template, or execution policy came from an obvious reference

## Required format

Use flat bullets:

- `local-project`: `<path>` - `<reason>`
- `official-doc`: `<url>` - `<reason>`
- `public-skill`: `<url or repo>` - `<reason>`

## Good examples

- `local-project`: `<tb2-project-root>\README.md` - reused TB2 runtime command shape for external audit routing
- `official-doc`: `https://code.claude.com/docs/en/sub-agents` - used project subagent placement and read-only reviewer pattern

## Bad examples

- `参考了 TB2`
- `用了官方文件`
- `some GitHub repo`

Those are too vague. The user needs a path or URL and the specific reason.

## Output rule

Do not hide provenance inside appendix-only notes. Put `Reference Inputs` in the main audit report body.
