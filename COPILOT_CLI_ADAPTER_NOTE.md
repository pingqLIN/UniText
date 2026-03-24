# UniText — Copilot CLI Adapter Note

> Status: Target Baseline
> Scope: Define how `Copilot CLI` fits into the UniText starter template without overstating current support.

## 1. Purpose

This note records the current collaboration model between `UniText` and `Copilot CLI`.

`Copilot CLI` is part of the starter template target baseline because the project goal is to make shared resources usable by multiple LLM AI tools across:

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`
- `Copilot CLI`
- `Windows`
- `macOS`
- `Linux`

At the same time, this note intentionally does **not** claim that `Copilot CLI` is already fully wired, verified, or feature-complete inside this repository.

## 2. Current Position

The current repo baseline is:

- `registry/` is the canonical source of truth for shared resources
- `.mcp.json` is shipped as a template-safe, relative-path seed
- `.claude/settings.json` is tracked as part of the shared starter baseline
- `bootstrap.py -> verify-bootstrap.py` is the preferred first-run path for the current cross-platform baseline

For `Copilot CLI`, the intended direction is:

- consume the same shared `skills / mcp / agents / workflow` baseline
- avoid duplicating per-tool resource copies unless the CLI requires it
- keep machine-specific wiring in the adapter/bootstrap layer rather than in canonical files

## 3. Why An Adapter Note Exists

`Copilot CLI` is currently in a different state from `Claude Code`, `Codex CLI`, and `Gemini CLI`.

The project already has a clearer first-run path for:

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`

But for `Copilot CLI`, this repository does not yet define a stable, repo-level adapter contract that is both:

- cross-platform
- template-safe
- verified by local bootstrap and validation flow

This note exists so the template can honestly say:

- `Copilot CLI` is in scope
- the direction is defined
- the implementation is still pending

## 4. Adapter Goals

The future `Copilot CLI` adapter should satisfy these goals:

1. Read from the same canonical registry rather than introducing another source of truth.
2. Work on `Windows`, `macOS`, and `Linux` without author-specific absolute paths.
3. Keep initialization steps explicit and automatable.
4. Be compatible with the template release boundary, meaning no local-only deployment assumptions should leak into the shared repo.
5. Provide a verification path comparable to `bootstrap -> verify`.

## 5. Proposed Integration Path

The most conservative integration path is:

1. Keep `registry/` as the single source of truth.
2. Discover the stable `Copilot CLI` config surface that can point at shared resources or project-local MCP configuration.
3. Add adapter-specific bootstrap logic only after the config surface is stable enough to support a GitHub-hosted starter template.
4. Add an explicit verification step before changing the compatibility matrix from `adapter pending` to `verified`.

In practice, this means the first implementation should answer:

- How does `Copilot CLI` discover project-local MCP definitions?
- How does `Copilot CLI` discover or consume shared skills?
- Which parts belong in tracked shared files, and which parts belong in local bootstrap output?

## 6. Known Gaps

The current repo still lacks these pieces for `Copilot CLI`:

- a fixed adapter contract in the shared repo
- a verified first-run initialization path
- a repo-level verification command with evidence
- a documented rule for how `Copilot CLI` should consume shared skills, MCP definitions, or agent resources

Because of these gaps, the current compatibility status remains:

`target baseline, adapter pending`

## 7. Non-Goals

This note does not:

- claim verified `Copilot CLI` support
- freeze a tool-specific config format before it is stable
- require duplicated `skills` content just to satisfy one CLI
- move canonical truth away from `registry/`

## 8. Recommended Next Step

The next practical milestone is:

**define the first repo-level `Copilot CLI` adapter baseline, then add bootstrap + verification evidence**

Only after that should the compatibility matrix or template release checklist be upgraded from target language to verified support.
