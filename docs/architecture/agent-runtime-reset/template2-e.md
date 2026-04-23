# Template 2 — UniText Runtime Reset

Registry remains the canonical authoring layer; runtime becomes the only agent-facing projection.

## Diagnosis
- Codex currently has too many direct ways to consume `registry/skills`, which makes startup noisy and couples the agent runtime to authoring layout.
- `README.md` and `INDEX.md` are overloaded: they mix orientation, catalog, and operational guidance, so neither file is a clean runtime entrypoint.
- The repo already has the right canonical core, but it lacks a small, explicit, low-noise surface that an agent can read first and trust.
- Cross-CLI support exists in intent, but the current shape favors ad hoc bootstrap logic over a uniform runtime contract.

## Target State
- `registry/` remains the only canonical authoring surface for shared resources.
- `runtime/` becomes the only agent-facing surface, generated from the registry and optimized for first-read consumption.
- `README.md` and `INDEX.md` are reduced to human discovery docs only; they should not carry operational authority.
- Codex is the default runtime consumer, but the contract stays CLI-neutral so Claude, Gemini, and Copilot can project the same runtime through thin adapters.
- Local configs, bootstrap output, and ops evidence remain machine-specific, reversible, and non-canonical.

## Layer Model
| Layer | Responsibility | Canonical | Human-editable |
|---|---|---:|---:|
| `registry/` | Authoring source for skills, MCP, agents, workflow | Yes | Yes |
| `runtime/` | Generated agent-first projection and entrypoint | No | No |
| `local/` | Machine-local activation, bootstrap, verification | No | Yes |
| `ops/` | Evidence, backups, drift, audit, release artifacts | No | Yes |
| `README.md` / `INDEX.md` | Human discovery and orientation only | No | Yes |

- The generator owns `runtime/`; humans edit `registry/`.
- Runtime content must never become the source of truth for shared resource identity.
- Any CLI-specific deviation belongs in `local/`, not in `registry/`.

## Runtime Surface
- `runtime/entry.md` is the first read for agents and contains only mission, boundaries, canonical roots, and tool-order guidance.
- `runtime/manifest.json` exposes machine-readable roots, adapter names, and verify commands.
- `runtime/adapters/codex.md` defines Codex-specific loading order, MCP expectations, and failure policy.
- `runtime/adapters/<cli>.md` holds future CLI-specific deltas so cross-CLI support does not fork the common contract.
- Codex should prefer MCP-backed discovery through `unitext-registry` before any direct tree scan.
- Root `AGENTS.md` stays minimal and policy-only; it should not become the operational runtime.

## Delivery and Verify Contract
| Step | Input | Output | Stop condition |
|---|---|---|---|
| Project registry | `registry/*` | canonical tree | duplicate or conflicting IDs |
| Materialize runtime | `registry/*` + generator | `runtime/*` | stale projection or invalid manifest |
| Activate adapter | `runtime/*` + local config | Codex/CLI wiring | missing MCP or skills path |
| Verify | active wiring + runtime surface | pass/fail report | absolute-path leak or registry drift |

- Delivery must be deterministic and reversible.
- Verify must prove the runtime entrypoint is sufficient without direct registry browsing.
- If a CLI needs a special path, the path belongs in its adapter, not in the shared runtime contract.
- `bootstrap`, `sync`, `adopt`, and `repair` remain the only mutation triggers.

## Migration
- Phase 1: add the runtime projection beside the current docs and keep existing workflows working.
- Phase 2: point Codex startup and bootstrap at `runtime/entry.md` and the Codex adapter.
- Phase 3: strip operational instructions out of `README.md` and `INDEX.md`, leaving only orientation and discovery.
- Phase 4: make direct registry traversal an implementation detail behind runtime or MCP, not the default agent path.
- Phase 5: freeze the common runtime contract and add new CLI adapters only through the same projection model.

## Validation
The runtime surface is accepted only if all 20 tasks pass:

1. A clean clone exposes exactly one documented agent entrypoint.
2. The entrypoint names `registry/` as canonical and `runtime/` as derived.
3. The entrypoint does not require reading `README.md` to start work.
4. The entrypoint does not require reading `INDEX.md` to start work.
5. The runtime manifest resolves only logical paths, not machine absolute paths.
6. The runtime manifest lists the same canonical roots as the registry spec.
7. Codex can discover the registry through the runtime path without manual filesystem hunting.
8. Codex can resolve one skill, one MCP server, and one agent from the runtime surface.
9. A new skill added under `registry/skills/` appears in the projected runtime without manual edits.
10. A new agent added under `registry/agents/` appears in the projected runtime without manual edits.
11. A new workflow added under `registry/workflow/` appears in the projected runtime without manual edits.
12. The Codex adapter bootstraps cleanly on a fresh machine profile.
13. The Codex adapter verify step fails if `skills_path` or MCP wiring points outside the repo contract.
14. The Copilot adapter remains separate and does not inherit Codex-only assumptions.
15. The same registry source can be projected into a second CLI adapter without changing the common contract.
16. The runtime surface contains no local-only inventory, backups, or drift records.
17. The runtime surface contains no secret, token, or account-specific material.
18. Verification fails when the runtime projection is stale relative to `registry/`.
19. Verification succeeds after a no-op regen, proving idempotence.
20. Verification produces a short, machine-readable report that names the exact failing layer when it breaks.

## Risks
- Generator drift can reintroduce noise if runtime projection is not verified against the registry on every meaningful change.
- `README.md` and `INDEX.md` can regress into dual-purpose documents if they are allowed to carry operational steps again.
- Codex-first can become Codex-only if other adapters are deferred too long, so the common runtime contract must stay CLI-neutral.
- Cross-platform confidence remains limited until the runtime projection is tested on the target OS matrix, not just Windows.
