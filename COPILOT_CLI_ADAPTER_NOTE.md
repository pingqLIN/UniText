# UniText — Copilot CLI Adapter Note

> Status: Bootstrap Baseline Verified
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

At the same time, this note intentionally does **not** claim that `Copilot CLI` is already feature-complete or end-to-end verified across every interactive workflow inside this repository.

## 2. Current Position

The current repo baseline is:

- `registry/` is the canonical source of truth for shared resources
- `.mcp.json` is shipped as a template-safe, relative-path seed
- `.github/copilot-instructions.md` is the repo-level Copilot instructions surface
- `.claude/settings.json` is tracked as part of the shared starter baseline
- `bootstrap.py -> verify-bootstrap.py` is the preferred first-run path for the current cross-platform baseline
- `bootstrap.py` now aligns `~/.copilot/skills` and writes `~/.copilot/mcp-config.json` with the local `unitext-registry` MCP server entry
- `verify-bootstrap.py` now checks the Copilot skills target and MCP config contract alongside the existing Claude / Codex / Gemini targets

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

The main question used to be whether `Copilot CLI` exposed a stable enough config surface for the starter template. That question is now answered conservatively:

- project guidance can live in `.github/copilot-instructions.md`
- personal shared skills can live in `~/.copilot/skills`
- local MCP wiring can live in `~/.copilot/mcp-config.json`
- those two personal surfaces can be managed through `bootstrap.py -> verify-bootstrap.py`

This note exists so the template can honestly say:

- `Copilot CLI` is in scope
- the direction is defined
- the bootstrap baseline exists and is locally verifiable
- broader runtime evidence is still pending

## 4. Adapter Goals

The `Copilot CLI` adapter baseline should satisfy these goals:

1. Read from the same canonical registry rather than introducing another source of truth.
2. Work on `Windows`, `macOS`, and `Linux` without author-specific absolute paths.
3. Keep initialization steps explicit and automatable.
4. Be compatible with the template release boundary, meaning no local-only deployment assumptions should leak into the shared repo.
5. Provide a verification path comparable to `bootstrap -> verify`.

## 5. Current Adapter Contract

The current conservative contract is:

1. Keep `registry/` as the single source of truth.
2. Track repository guidance in `.github/copilot-instructions.md`.
3. Deliver shared skills to `~/.copilot/skills` during bootstrap.
4. Register the read-only `unitext-registry` server in `~/.copilot/mcp-config.json` during bootstrap.
5. Verify those outputs through `verify-bootstrap.py`.

This contract is intentionally narrow. It does not depend on interactive `/mcp add`, plugins, or one-off operator steps. It only depends on documented file surfaces that can be written atomically and checked offline.

In practice, the current implementation answers:

- How does `Copilot CLI` discover or consume shared skills?
  Through `~/.copilot/skills`, which bootstrap aligns to `registry/skills`.
- How does `Copilot CLI` discover the shared UniText MCP surface?
  Through `~/.copilot/mcp-config.json`, which bootstrap updates with the local `unitext-registry` entry.
- Which parts belong in tracked shared files?
  `.github/copilot-instructions.md` and the canonical registry.
- Which parts belong in local bootstrap output?
  `~/.copilot/skills` and `~/.copilot/mcp-config.json`.

## 6. Known Gaps

The current repo still lacks these pieces for `Copilot CLI`:

- broader interactive-session evidence that Copilot actually invokes the seeded skills and MCP server as expected in day-to-day use
- a richer verification path beyond first-run config checks
- a documented policy for repository-level custom agents if UniText later wants to expose shared agent personas through Copilot-native locations

Because of these gaps, the current compatibility status remains:

`bootstrap baseline verified; broader runtime validation pending`

The repository now includes `local/scripts/verify-copilot-session.py` to collect repeatable non-interactive prompt evidence, and the current observed boundary is documented in `COPILOT_SESSION_EVIDENCE_2026-03-26.md`. That script is an evidence collector, not a status promotion by itself.

## 7. Non-Goals

This note does not:

- claim that every Copilot workflow is already end-to-end verified
- require duplicated `skills` content just to satisfy one CLI
- move canonical truth away from `registry/`

## 8. Recommended Next Step

The next practical milestone is:

**collect end-to-end Copilot session evidence on top of the verified bootstrap baseline, then decide whether the status should be promoted beyond bootstrap verification**

Only after that should the compatibility matrix or template release checklist be upgraded beyond bootstrap verification language.
