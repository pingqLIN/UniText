---
runtime_projection: true
source_of_truth: registry/skills/claude-design-playbook/references/prompt-packs.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/claude-design-playbook/references/prompt-packs.md`
> Source of truth: `registry/skills/claude-design-playbook/references/prompt-packs.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Prompt Packs

These prompt packs are adapted from the upstream `awesome-claude-design` repo and rewritten for Codex skill use.

## `family-picker`

### Goal

- Choose exactly one family for the next Claude Design system.

### Sequence

1. Ask whether the product is read-heavy or scan-heavy.
2. Ask for the primary audience or operator type.
3. Ask whether the brand should feel courageous or familiar.
4. If needed, ask one tie-breaker about competitors or design-team complexity.

### Output contract

- `Recommended family`
- `Why`
- `One reference anchor`
- `Alternative family`
- `Family to avoid`
- `Next Claude Design step`

### Guardrails

- Force one recommendation.
- Avoid long style taxonomies.
- Keep the recommendation tied to product reality, not personal taste.

## `brand-to-design-md`

### Goal

- Convert a live site, screenshot set, or design artifact into a verified nine-section `DESIGN.md`.

### Sequence

1. Inspect visible tokens, spacing, typography, hero treatment, and component patterns.
2. Record only what is visible or otherwise verifiable.
3. Emit the canonical nine sections in [design-md-structure.md](design-md-structure.md).
4. Mark unknown font identities, motion details, or hidden states as `unknown`.

### Output contract

- One complete `DESIGN.md`
- Role-based color tokens
- Explicit component rules
- An `Agent Prompt Guide` with acceptance and rejection cues

### Guardrails

- No invented font names.
- No vague color names when hex can be stated.
- No generic SaaS filler like "modern and clean" without operational consequences.

## `audit-live-site-against-design-md`

### Goal

- Audit a rendered site against a target system and return an evidence-backed punch list.

### Sequence

1. Compare hierarchy, spacing, color roles, accessibility, motion, and copy against the target system.
2. Score only what can be justified from rendered evidence.
3. Produce a prioritized punch list ordered by impact and effort.

### Output contract

- Category scores
- Top issues with selectors or visible anchors
- Concrete fixes
- Ordered punch list

### Guardrails

- Audit against the target system, not against general taste.
- Do not invent screenshots or measurements that were not observed.
- Keep P0 only for problems that clearly block legibility, access, or core brand fit.

## `remix-two-brands`

### Goal

- Merge two parent systems into a third system with deliberate token arbitration.

### Sequence

1. Choose one parent for typography.
2. Choose one parent for accent strategy.
3. Keep the stricter spacing scale.
4. Keep the more restrained depth model.
5. Explain parent contribution for each major token family.

### Output contract

- One coherent `DESIGN.md`
- Parent contribution notes
- Tension notes where the systems disagree
- Approximate parent DNA split

### Guardrails

- Do not read like a stitched blend.
- Do not keep two competing accent systems.
- Resolve contradictions explicitly instead of burying them in prose.
