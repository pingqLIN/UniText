# Template 2: UniText Runtime Reset (Agent-First, Registry-First)

## Diagnosis
- **Default tool surface is noisy and slow**: Codex (and other CLIs) point `skills_path` at `registry/skills`, so the agent boots with the entire authoring inventory rather than an intentional runtime set.
- **Registry is doing two jobs**: canonical authoring *and* runtime delivery. That collapses governance boundaries and makes “safe defaults” hard (everything is always “on”).
- **README/INDEX are overloaded**: they act as marketing, discovery, spec, and operational runbook; agents lack a single, low-noise “what can I do right now” entrypoint.
- **Runtime activation is implicit**: today, “run bootstrap” mutates CLI configs and symlinks, but there is no explicit “runtime surface contract” that can be validated, switched, or audited as a unit.
- **Cross-CLI extensibility is accidental**: adapters exist, but the system does not model a stable, minimal runtime interface that new CLIs can target without inheriting authoring noise.

## Target State
- **Registry stays canonical** (`registry/**` remains the only authored source of truth).
- **No CLI reads `registry/skills` directly** in steady-state. CLIs read **materialized runtime surfaces**.
- **Runtime surfaces are explicit, versioned artifacts** generated from registry + policy, stored in a dedicated generated area, and validated by a deterministic verify contract.
- **Agents have one entrypoint** that is low-noise, stable, and runtime-oriented (what’s active, how to switch profiles, how to discover more via MCP).
- **Discovery is via MCP, action is via curated skills**: the full registry remains queryable through `unitext-registry` MCP, but the default tool list stays intentionally small.
- **Cross-CLI is a first-class contract**: adding a new CLI requires implementing a thin adapter against the runtime manifest, not re-pointing to registry.

## Layer Model
1. **L0 Canonical Authoring (tracked)**: `registry/**` plus stable root docs/specs.
2. **L1 Runtime Policy (tracked)**: `registry/workflow/runtime-surfaces/**` defining profiles, inclusion rules, and stable IDs (no machine paths).
3. **L2 Local Resolution (local-only)**: `local/config/**` for machine/OS/CLI capability flags and optional local overrides (e.g., symlink support).
4. **L3 Materialized Runtime (generated, local-only)**: `local/runtime/**` containing per-profile, per-CLI skill trees and a manifest; safe to delete and rebuild.
5. **L4 CLI Wiring (local-only)**: `~/.codex/config.toml`, `~/.claude/skills`, `~/.gemini/skills`, `~/.agents/skills`, `~/.copilot/mcp-config.json` updated to point at L3.
6. **L5 Audit + Evidence (tracked outputs, append-only)**: `ops/history/runtime_<stamp>/**` summaries, diffs, and verify reports.

## Runtime Surface
**Directory contract**
- `local/runtime/manifest.json` is the single source of runtime truth for tools.
- `local/runtime/profiles/<profile_id>.json` describes the exact skill/MCP/agent surfaces.
- `local/runtime/<cli>/<profile_id>/skills/<skill_id>/SKILL.md` exists as a symlink/mirror into `registry/skills/<skill_id>`.

**Profile model (minimum)**
- `codex:minimal`: Core “8 + 4” shortlist only, plus any safety/ops primitives required for delivery/verify.
- `codex:default`: `minimal` + workspace essentials needed for day-to-day implementation (explicitly enumerated).
- `codex:full`: everything in registry, for rare deep discovery sessions (explicitly opt-in).
- The same profile IDs can exist for `claude`/`gemini`, but each CLI may map `default` differently if it cannot consume certain surfaces.

**Agent entrypoint (low-noise)**
- Add a stable, short doc generated from the manifest: `local/runtime/ENTRYPOINT.md`.
- This is the first read for agents (not README/INDEX) and contains only: active profile, available profiles, how to rebuild/apply/verify, and how to discover additional skills via MCP.

**MCP posture**
- Keep `unitext-registry` MCP as the discovery backplane (list/read registry entries and files).
- Do not use MCP to “activate” skills implicitly; activation is via profile build/apply to keep the default tool surface predictable.

## Delivery and Verify Contract
**Single command surface (proposal)**
- `python local/scripts/runtime.py build --profile codex:default --mode auto --dry-run`
- `python local/scripts/runtime.py apply --profile codex:default --mode auto --force`
- `python local/scripts/runtime.py verify --profile codex:default --json`

**Contract rules**
- `build` is pure with respect to external state: it only writes under `local/runtime/**` and `ops/history/**` (unless `--dry-run`).
- `apply` is the only step allowed to mutate CLI home configs and skill targets; it must always back up to `ops/history/runtime_<stamp>/**`.
- `verify` must be deterministic and offline: it reads manifest + actual CLI configs and returns `ok` plus a machine-readable diff of mismatches.

**Codex-specific wiring (decision)**
- Set Codex `skills_path` to `local/runtime/codex/<active_profile>/skills`, never to `registry/skills`.
- Keep Codex MCP server registration for `unitext-registry`, but treat it as discovery, not as the default action surface.

## Migration
1. **Introduce runtime policy**: define `codex:minimal`, `codex:default`, `codex:full` in tracked `registry/workflow/runtime-surfaces/`.
2. **Implement runtime materialization**: generate `local/runtime/**` with symlink-first and mirror fallback (reuse the existing “auto/symlink/mirror” semantics).
3. **Cut over Codex**: change bootstrap/apply so `skills_path` points to `local/runtime/.../skills`; keep the registry MCP server unchanged.
4. **Cut over other CLIs**: repoint `~/.claude/skills`, `~/.gemini/skills`, `~/.agents/skills` to runtime surfaces (not registry).
5. **Demote README/INDEX for agents**: keep them for humans/discovery, but establish `local/runtime/ENTRYPOINT.md` as the agent-first entry.
6. **Deprecate direct-registry runtime**: add verify failures (not warnings) when any CLI is configured to read `registry/skills` as its active skills surface.

## Validation
**20 acceptance tasks to validate the runtime surface**
1. `build codex:minimal` produces `local/runtime/manifest.json` and `local/runtime/profiles/codex_minimal.json` with stable schema version and profile ID.
2. `build codex:minimal` produces a `skills/` directory where each skill entry resolves to a real `SKILL.md` (symlink or mirrored file).
3. `build` is idempotent: running it twice with no inputs changed produces byte-identical manifests for the same profile.
4. `build --dry-run` writes no files outside stdout and returns a complete planned-write list including target paths.
5. `apply codex:minimal` updates Codex `skills_path` to the runtime path and does not reference `registry/skills` anywhere in the active config.
6. After `apply`, launching Codex shows only the skills present in `codex:minimal` (tool list size matches manifest).
7. `verify codex:minimal` returns `ok=true` on a clean machine state and emits a JSON report with explicit checks and pass/fail per check.
8. `verify` fails with a specific mismatch reason if Codex points to `registry/skills`.
9. Switching profiles (`apply codex:default`) updates `skills_path` and results in the expected delta in tool list (superset of `minimal`).
10. `codex:full` is only reachable by explicit profile selection and is never the default in any script or doc.
11. `unitext-registry` MCP server remains registered after migration and can list/read registry entries without requiring the full skill tree to be active.
12. Agent entrypoint exists: `local/runtime/ENTRYPOINT.md` is generated and includes active profile, available profiles, and the three commands `build/apply/verify`.
13. Runtime manifest includes the exact list of skill IDs, and those IDs match actual folder names under `registry/skills/`.
14. If a skill is removed from policy, `apply` removes it from runtime surface without deleting canonical registry content.
15. If symlink creation is unavailable, `build --mode auto` falls back to mirror and `verify` still passes with a recorded “delivery mode”.
16. Claude/Gemini skills targets can be repointed to runtime surfaces and `verify` reports each target alignment status.
17. Copilot remains unaffected by skills surfaces and still registers `unitext-registry` MCP with the expected command/args.
18. A runtime audit artifact is created on every non-dry-run `apply` under `ops/history/runtime_<stamp>/summary.json` including inputs, outputs, and diffs.
19. Runtime surfaces do not contain absolute user-specific paths in tracked files; only local-only artifacts may contain absolutes.
20. A regression test ensures README/INDEX changes are not required for runtime correctness; runtime entrypoint and manifest are sufficient.

## Risks
- **Policy drift vs registry drift**: if runtime policy isn’t reviewed like code, the “minimal” surface can silently bloat; mitigate with verify thresholds and explicit profile diffs.
- **Symlink portability**: Windows symlink constraints can force mirroring; mitigate with explicit mode reporting and size/time budgets in verify.
- **Over-constraining defaults**: too-small `minimal` can block common work; mitigate by making `default` the normal steady-state and keeping `minimal` for constrained runs.
- **Two discovery paths**: skills surface plus MCP discovery can confuse users; mitigate by making the entrypoint state the rule: “discover via MCP, activate via profiles”.
- **Backwards compatibility**: existing scripts assume `registry/skills`; mitigate with a transitional verify that explains the remediation path and provides one command to fix.
