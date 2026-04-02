# UniText — Copilot CLI Adapter Note

> Status: Active Baseline
> Scope: Define the first repo-level `Copilot CLI` adapter baseline without overstating remaining gaps.

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

At the same time, this note intentionally does **not** claim that `Copilot CLI` is already feature-complete across every platform or that it consumes UniText in exactly the same way as every other CLI.

## 2. Current Position

The current repo baseline is:

- `registry/` is the canonical source of truth for shared resources
- `.mcp.json` is shipped as a template-safe, relative-path seed
- `.claude/settings.json` is tracked as part of the shared starter baseline
- `bootstrap.py -> verify-bootstrap.py` is the preferred first-run path for the current cross-platform baseline

For `Copilot CLI`, the current repo-level baseline is:

- consume repo instructions from `AGENTS.md` and related files
- consume the same shared `unitext-registry` MCP server via `~/.copilot/mcp-config.json`
- keep machine-specific wiring in the adapter/bootstrap layer rather than in canonical files

## 3. Why An Adapter Note Exists

`Copilot CLI` is currently in a different state from `Claude Code`, `Codex CLI`, and `Gemini CLI`.

The project already has a clearer first-run path for:

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`

The repo now defines a first adapter contract that is:

- template-safe
- repo-level
- validated by `bootstrap.py -> verify-bootstrap.py` on the current Windows authoring host

What still remains open is broader cross-platform validation and the exact long-term story for any Copilot-specific skill surface beyond repo instructions.

This note exists so the template can honestly say:

- `Copilot CLI` is in scope
- the direction is defined
- the implementation is still pending

## 4. Adapter Goals

The future `Copilot CLI` adapter should satisfy these goals:

1. Read from the same canonical registry rather than introducing another source of truth.
2. Keep initialization steps explicit and automatable.
3. Be compatible with the template release boundary, meaning no local-only deployment assumptions should leak into the shared repo.
4. Provide a verification path comparable to `bootstrap -> verify`.
5. Stay honest about what is verified now versus what is still only intended.

## 5. Proposed Integration Path

The current conservative integration path is:

1. Keep `registry/` as the single source of truth.
2. Use repo instructions from `AGENTS.md` / related files as the primary instruction surface.
3. Use `bootstrap.py` to upsert `unitext-registry` into `~/.copilot/mcp-config.json`.
4. Use `verify-bootstrap.py` to confirm the expected `unitext-registry` command, args, and config shape when `Copilot CLI` is installed.

In practice, the first implementation answers:

- How does `Copilot CLI` discover project-local MCP definitions?
  - through `~/.copilot/mcp-config.json`, written by bootstrap
- How does `Copilot CLI` discover repo instructions?
  - through built-in loading of `AGENTS.md` / related files
- Which parts belong in tracked shared files, and which parts belong in local bootstrap output?
  - instructions stay shared; machine-local MCP wiring stays in bootstrap output

## 6. Known Gaps

The current repo still lacks these pieces for `Copilot CLI`:

- macOS validation evidence
- Linux validation evidence
- a documented long-term rule for whether Copilot needs any separate skills surface beyond repo instructions
- a compatibility status stronger than the currently observed bootstrap evidence

Because of these gaps, the compatibility status should be interpreted as:

`repo-level MCP baseline defined; broader platform verification still pending`

## 7. Non-Goals

This note does not:

- claim full cross-platform `Copilot CLI` support
- freeze a tool-specific config format before it is stable
- require duplicated `skills` content just to satisfy one CLI
- move canonical truth away from `registry/`

## 8. Recommended Next Step

The next practical milestone is:

**revalidate the same `Copilot CLI` bootstrap + verify path on macOS and Linux, then decide whether the compatibility matrix can move from baseline evidence to broader verified support**

Only after that should the compatibility matrix or template release checklist be upgraded to stronger verified language.
