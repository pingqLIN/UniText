# Canonical DESIGN.md Structure

Every generated or remixed `DESIGN.md` should use these nine sections in order.

## 1. Visual Theme & Atmosphere

- State the overall character in implementation-relevant language.
- Include mood words only when they change layout, typography, color, or motion.

## 2. Color Palette & Roles

- Use role-based token names.
- Prefer hex values when known.
- Note usage rules such as "accent only on primary action" or "never use gradients on body backgrounds."

## 3. Typography Rules

- State stacks, scale, weights, and notable tracking or line-height rules.
- Mark uncertain type identities as `unknown`.

## 4. Component Stylings

- Cover at minimum: buttons, cards, inputs, and navigation.
- Add other components only when they are central to the brand.

## 5. Layout Principles

- Define grid, width, spacing scale, and density expectations.
- Explain when asymmetry, overlap, or reading measure matters.

## 6. Depth & Elevation

- Explain how depth is created: shadows, borders, surface shifts, blur, or flatness.
- Call out exceptions such as modals or popovers.

## 7. Do's and Don'ts

- Keep this operational.
- Include rejection cues for patterns the system must avoid.

## 8. Responsive Behavior

- State what changes at mobile or narrow breakpoints.
- Cover navigation, headline scale, tables, or density changes when relevant.

## 9. Agent Prompt Guide

- Summarize generation bias for coding agents.
- End with a rejection clause that states what the generator should restart rather than preserve.

## Output rules

- Prefer direct, implementation-relevant language.
- Keep each section compact.
- Do not pad the file with product marketing or origin story.

