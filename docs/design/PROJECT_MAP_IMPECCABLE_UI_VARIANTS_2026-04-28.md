# Project Map Impeccable UI Variants

Date: 2026-04-28

## Source Basis

Route used: `brand-to-design-md` plus implementation handoff.

Live reference: `https://impeccable.style`

Verified cues from the rendered site:

- Product UI is treated differently from brand UI: dashboard surfaces should serve the operator task rather than perform like a landing page.
- Strong anti-references: purple gradients, Inter everywhere, nested cards, generic copy, low-contrast labels, template SaaS composition.
- Preferred product direction: token-aware polish, clearer hierarchy, fewer duplicated controls, explicit design vocabulary, and browser-visible iteration.
- Typography identity from page text is not fully verifiable from static extraction; font identities remain `unknown` unless already present in the local UI.

## DESIGN.md Compact System

### 1. Visual Theme & Atmosphere

Operator-grade product console. Quiet, exact, and slightly editorial. The UI should feel like a maintained instrument panel, not a generic SaaS dashboard.

### 2. Color Palette & Roles

- `surface.base`: warm off-white or graphite depending on variant.
- `surface.panel`: low-contrast paper or slate panel.
- `ink.primary`: high contrast text, never washed-out gray.
- `ink.secondary`: secondary labels only, still readable.
- `accent.primary`: teal, amber, or red-orange depending on variant; one main accent per version.
- Avoid purple gradients and gradient text.

### 3. Typography Rules

- Keep expressive display typography already used by the project where possible.
- Use a narrow readable body measure for explanatory text.
- Use tabular/mono numerals only for counts, paths, and governance evidence.
- Unknown external font identities: `unknown`.

### 4. Component Stylings

- Buttons: clear active/inactive states, no pill soup.
- Cards: reduce card nesting; prefer sections separated by borders, rails, or typographic rhythm.
- Inputs: functional, compact, with labels close to controls.
- Navigation: one primary tab surface only.

### 5. Layout Principles

- Main visual area gets priority.
- Governance explanation must be inspectable, not hidden behind long prose.
- Repeated controls should be removed or promoted to one intentional location.
- Variant C may break the three-column frame if the interaction model becomes clearer.

### 6. Depth & Elevation

- Use borders, surface shifts, and sparse shadows.
- Avoid glassmorphism and stacked translucent cards.
- Elevation is reserved for active controls, floating inspectors, or selected nodes.

### 7. Do's and Don'ts

- Do: name the operator task in the UI.
- Do: expose source, status, and applicability for governance files.
- Do: make map navigation tactile.
- Don't: add purple, gradient headings, or centered marketing hero language.
- Don't: duplicate the same navigation or filter controls in two areas.

### 8. Responsive Behavior

- Mobile should collapse to a single-column cockpit: controls, then map, then detail.
- Viewport controls remain reachable near the map.
- Governance funnel becomes a vertical stack.

### 9. Agent Prompt Guide

Generate product UI for an operator console. Preserve clarity and inspectability. Favor deliberate typography, one accent family, sparse depth, and direct labels. Reject any result that looks like generic modern SaaS, uses purple gradients, duplicates controls, or hides governance evidence inside decorative cards.

## Three Versions

### Version A: Original Polish

Goal: retain the current project-map structure, adjust only hierarchy, contrast, and duplication pressure.

Use when: the priority is safe adoption with minimal regression risk.

Artifact: `ops/project-map/design-variants/variant-a-original-polish.html`

### Version B: Impeccable Product Console

Goal: similar information architecture, but stronger product-console discipline: tighter density, sharper controls, more explicit governance source status.

Use when: the project-map is becoming a daily operator surface.

Artifact: `ops/project-map/design-variants/variant-b-product-console.html`

### Version C: Governance Operations Room

Goal: new concept. The UI centers the governance funnel and map as an operations board, with rule sources, path applicability, and viewport controls as the primary mental model.

Use when: the governance explanation becomes the core product, not just a side panel.

Artifact: `ops/project-map/design-variants/variant-c-governance-room.html`

## Recommendation

Implement Version B first. It keeps enough of the current structure to land safely, while borrowing the strongest Impeccable product lesson: design serves the operator task, not the page decoration.
