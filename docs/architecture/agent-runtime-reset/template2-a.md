# Template 2 — UniText Runtime Reset

## Diagnosis
- UniText currently collapses authoring and consumption into the same surface. Pointing Codex `skills_path` at `registry/skills` makes every canonical draft a live runtime artifact.
- `README.md` and `INDEX.md` are carrying three jobs at once: human introduction, catalog/discovery, and agent startup. That is high-noise by design.
- The current default MCP shape is registry-centric (`unitext-registry` reads core docs and raw registry files). That is appropriate for curation, not for a default worker runtime.
- Generated output has already started leaking toward canonical space (`registry/dist`), which weakens the “registry is source only” boundary.
- Current verification mostly proves path wiring and MCP initialization. It does not prove that an agent can complete work from a minimal runtime surface without falling back to raw repo exploration.

## Target State
- Keep `registry/` as the only canonical authoring plane.
- Add `runtime/contracts/` as the tracked profile contract plane. It defines what each runtime profile is allowed to see.
- Generate `.unitext/` as the runtime plane. Codex consumes `.unitext`, never `registry/` directly.
- Move derived artifacts out of `registry/`. Use `dist/` for release/export bundles and `ops/history/` for local evidence.
- Make `README.md` human-facing only and `INDEX.md` catalog-facing only. Neither is a default agent entrypoint.
- Replace default `unitext-registry` consumption with a narrower `unitext-runtime` server. Keep `unitext-registry` only for curator/admin profiles.
- Ship Codex first, but keep the contract model CLI-neutral so Claude, Gemini, and Copilot adapters compile from the same source.

## Layer Model

| Layer | Location | Purpose | Mutation Rule |
|---|---|---|---|
| L0 Canonical Authoring | `registry/*` | Human-authored source of truth for skills, MCP, agents, workflow | Tracked, manual, no generated outputs |
| L1 Runtime Contract | `runtime/contracts/*` | Profile definitions, exposure rules, allowlists, provenance requirements, CLI capability map | Tracked, manual |
| L2 Compiled Runtime Pack | `.unitext/profiles/<profile>/*` | Self-contained, low-noise runtime surface for one CLI/profile | Generated, disposable, never hand-edited |
| L3 Delivery Adapter | `local/scripts/activate-runtime.py` and CLI configs | Wires one CLI to one compiled runtime pack | Machine-local only |
| L4 Verify and Evidence | `local/scripts/verify-runtime.py`, `ops/history/runtime/*` | Proves runtime behavior, drift detection, reversibility, and acceptance results | Generated and auditable |

## Runtime Surface

| Surface | Contents | Rule |
|---|---|---|
| `.unitext/profiles/codex-default/START.md` | Single startup page for the agent | Only entrypoint a default Codex session should need |
| `.unitext/profiles/codex-default/manifest.json` | Profile id, build id, hashes, exposed docs, exposed skills, MCP tools, provenance map | Machine-readable runtime contract snapshot |
| `.unitext/profiles/codex-default/skills/` | Only approved skills for this profile, with required references/scripts copied or linked into the pack | Self-contained; no runtime dependency on raw `registry/skills` |
| `.unitext/profiles/codex-default/docs/` | Low-noise docs such as `runtime-overview.md`, `operating-boundaries.md`, `task-catalog.md`, selected workflows | No `README.md`, no `INDEX.md`, no historical authoring notes |
| `.unitext/profiles/codex-default/mcp/` | `unitext-runtime` config and server entry | Exposes only runtime-safe tools |
| `.unitext/profiles/codex-default/activation.json` | Active repo root, build id, compiler version, profile, adapter targets | Explains what the CLI is currently wired to |

`unitext-runtime` should expose only four default tools:
- `runtime_overview`
- `list_runtime_resources`
- `read_runtime_resource`
- `get_runtime_provenance`

The default profile should not allow raw reads of `registry/`, `local/`, `README.md`, or `INDEX.md`. Those stay behind an explicit curator/admin profile.

## Delivery and Verify Contract
- `build-runtime --profile codex-default` compiles `.unitext/profiles/codex-default` from `registry/` plus `runtime/contracts/`.
- `activate-runtime --cli codex --profile codex-default` writes Codex config so `skills_path` points at `.unitext/profiles/codex-default/skills` and registers `unitext-runtime`.
- `verify-runtime --cli codex --profile codex-default` validates config wiring, MCP health, manifest integrity, negative access rules, and acceptance tasks.
- `bootstrap.py` should become a compatibility wrapper over `build-runtime -> activate-runtime -> verify-runtime`. It should stop containing primary resource-selection logic.
- Every compiled runtime item must carry canonical provenance back to `registry/*`.
- Every build must be deterministic: same inputs, same manifest hash.
- No generated runtime output may be committed under `registry/`.

## Migration
1. Declare `registry/` authoring-only and remove `registry/dist` from canonical space.
2. Introduce `runtime/contracts/codex-default.*` as the first tracked runtime contract.
3. Build `unitext-runtime` against `.unitext`, not the repo root. Keep `unitext-registry` only for curator/admin flows.
4. Split docs by role:
   - `README.md` = human intro
   - `INDEX.md` = discovery catalog
   - `.unitext/.../START.md` and runtime docs = agent startup surface
5. Change Codex activation so `skills_path` points to the compiled pack, never to `registry/skills`.
6. Rewrite verify logic around runtime behavior, not only file-path alignment.
7. Add secondary profiles after Codex:
   - `claude-default`
   - `gemini-default`
   - `copilot-default` or `copilot-instructions`
8. Keep one release of compatibility wrappers, then remove direct-registry runtime paths.

## Validation
Each acceptance task must begin from `START.md` or `runtime_overview`. If the task requires opening `README.md`, `INDEX.md`, or raw `registry/` in the default profile, the runtime surface has failed.

1. Read the active profile id, build id, and version from the runtime manifest.
2. Enumerate all allowed runtime docs from `runtime_overview`.
3. Enumerate all exposed skills from the manifest or MCP.
4. Open one exposed skill and its required references without leaving `.unitext`.
5. Resolve provenance for one skill back to its canonical `registry/*` source.
6. Locate one workflow document through runtime docs only.
7. Confirm the agent can start without reading `README.md`.
8. Confirm the agent can discover resources without reading `INDEX.md`.
9. Confirm default runtime cannot list raw `registry/skills`.
10. Confirm default runtime cannot read `local/` or machine-local config paths.
11. Confirm Codex `skills_path` points to `.unitext/profiles/codex-default/skills`.
12. Confirm Codex MCP wiring points to `unitext-runtime`, not `unitext-registry`.
13. Confirm `unitext-runtime` initializes and exposes exactly the runtime tool set.
14. Confirm manifest counts match actual shipped docs and skills in the compiled pack.
15. Confirm all relative references inside the pack resolve successfully.
16. Rebuild without source changes and confirm the manifest hash is identical.
17. Change one contract input and confirm only targeted runtime outputs change.
18. Roll back activation and confirm prior Codex config is restored.
19. Compile one non-Codex profile from the same contracts without changing `registry/`.
20. Produce a verify bundle in `ops/history/runtime/<build-id>/` containing task results, hashes, provenance, and adapter state.

## Risks
- Over-curation can make the runtime too thin. Mitigation: keep a small default surface, but provide an explicit curator/admin profile with broader access.
- The compiler adds one more moving part. Mitigation: keep contracts declarative and keep `bootstrap.py` as a thin wrapper, not a second control plane.
- Self-contained packs can drift from canonical content. Mitigation: generated-only output, manifest hashes, and per-resource provenance are mandatory.
- Cross-CLI support can degrade into lowest-common-denominator design. Mitigation: keep contracts shared, but allow per-CLI profile overlays and let Codex lead the first implementation.
- Hidden local state in `.unitext/` can confuse maintainers. Mitigation: require `activation.json`, deterministic build ids, and verify bundles in `ops/history/runtime/`.
