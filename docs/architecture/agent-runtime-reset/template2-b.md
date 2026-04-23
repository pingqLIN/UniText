# Template 2 — UniText Runtime Reset (Agent-First, Registry-Canonical)

## Diagnosis

- Codex is currently wired to `registry/skills` (`skills_path`), so it passively “sees” the full authoring tree (large references, stray items, mixed audiences) instead of a deliberate runtime surface.
- `README.md` and `INDEX.md` are serving too many roles (human onboarding, governance, operations, discovery, runtime), so agents pay an unnecessary orientation tax and drift toward noisy, non-operational docs.
- There is no explicit “agent runtime entrypoint” that is low-noise, stable, and designed for fast execution; agents infer entrypoints from overloaded docs or directory structure.
- Delivery is “path-based” rather than “contract-based”: tools validate that paths point to canonical sources, but not that a curated, profile-specific runtime surface exists and is correct.
- Canonical authoring and runtime consumption are not cleanly separated; this increases token waste, increases accidental scope, and makes “what is actually active” hard to answer quickly.

## Target State

- Registry-first authoring remains the only canonical source of truth: `registry/{skills,mcp,agents,workflow}`.
- Every CLI consumes a **runtime surface** that is intentionally small, profile-driven, and validated, not the authoring tree.
- Codex-first design: Codex loads a **thin, curated** skill set by default and relies on the existing read-only `unitext-registry` MCP surface for on-demand discovery and retrieval.
- A single low-noise agent entrypoint exists and is stable: `RUNTIME.md` at repo root is the “start here for agents”; `README.md`/`INDEX.md` become human discovery only.
- Delivery is driven by a manifest and profiles, with deterministic build outputs and a strict verify contract.
- Cross-CLI extensibility is built-in: adding a new CLI is “add adapter + profile mapping,” not “teach the CLI to read the registry.”

## Layer Model

| Layer | Purpose | Source of Truth | Must Not |
|---|---|---|---|
| 1. Registry | Canonical resources | `registry/**` | Be used as a default runtime ingestion root by any CLI |
| 2. Catalog & Policy | What is included/excluded, by profile | `registry/workflow/runtime/**` plus `registry/catalog-exclusions.json` | Depend on local paths or machine state |
| 3. Runtime Build | Deterministic compilation into a minimal surface | Generated | Contain authoring-only docs or unbounded reference trees by default |
| 4. Local Adapter | Machine wiring into each CLI | `local/scripts/**` and user home | Mutate without backups and rollback records |
| 5. CLI Runtime | What the agent actually runs with | CLI configs + runtime surface | Point skills discovery at the registry authoring tree |
| 6. Ops/Audit | Evidence, rollback, drift tracking | `ops/**` | Be required for normal execution |

## Runtime Surface

**Core decisions**

- Define `UNITEXT_RUNTIME_ROOT` (default `$HOME/.unitext/runtime`).
- Build outputs land in `UNITEXT_RUNTIME_ROOT/builds/<build_id>/`.
- `UNITEXT_RUNTIME_ROOT/current` is the only stable pointer CLIs use (directory junction/symlink or a fully mirrored directory).
- Codex `skills_path` points to `UNITEXT_RUNTIME_ROOT/current/skills` and must never reference `registry/skills` directly or indirectly.

**Profiles**

- `core` (default): essential shortlist + lightweight meta-skill(s); excludes heavy families and excluded/stray items.
- `full`: everything allowed by policy, including large families if explicitly permitted.
- `review`: minimal set for external review and share-safe work.
- `legacy` (temporary): matches today’s behavior for migration rollback only.

**Surface shape**

```text
$UNITEXT_RUNTIME_ROOT/
  builds/
    <build_id>/
      manifest.json
      skills/
        <skill-id>/
          SKILL.md
          assets/ (optional)
          refs/ (optional, curated)
      agents/ (optional, curated)
      mcp/
        unitext-registry.json (adapter-friendly descriptor)
  current -> builds/<build_id>/
```

**Packaging rules (Codex-first)**

- Default `thin` packaging for Codex: `SKILL.md` plus explicit small whitelisted folders (`assets/`, curated `refs/`).
- Heavy `references/` trees are excluded from `core` unless explicitly declared as required for runtime correctness.
- The read-only MCP server remains the authoritative “deep read” path for registry content; agents fetch what they need when they need it.

## Delivery and Verify Contract

**Build contract**

- `runtime build --profile <p>` produces a new build under `builds/<build_id>` and writes `manifest.json`.
- Build must be deterministic given `(git_sha, profile, packaging_policy)`; manifest includes `git_sha`, profile id, tool version, and file hashes.
- Build must be offline: no network, no external fetch.

**Install contract**

- `runtime install --cli codex --profile <p>` updates `~/.codex/config.toml` to set `skills_path = "$UNITEXT_RUNTIME_ROOT/current/skills"` and ensures `unitext-registry` MCP server is present.
- Install must create backups and a rollback record under `ops/history/runtime_install_<timestamp>/` (or equivalent).
- Install must never delete; it may only add/replace runtime pointers and write audited backups.

**Verify contract**

- `runtime verify --cli codex` fails if:
  - Codex `skills_path` references `registry/skills` (string match and resolved-path check).
  - `UNITEXT_RUNTIME_ROOT/current/manifest.json` is missing or mismatched with config.
  - Included skills differ from the manifest.
- `runtime verify --strict` also enforces:
  - Exclusions policy applied (`registry/catalog-exclusions.json`).
  - Profile shape constraints (file count and size budgets).
  - No unexpected top-level docs inside runtime surface.

## Migration

1. Define profile specs and packaging policy as canonical workflow content (registry-owned).
2. Implement build + install + verify as separate operations (build is pure, install is reversible mutation, verify is strict).
3. Introduce `RUNTIME.md` as the single agent entrypoint; demote `README.md`/`INDEX.md` to human discovery and ensure they link to `RUNTIME.md`.
4. Switch Codex from `registry/skills` to runtime `current/skills` for the `core` profile; keep `legacy` as an explicit opt-in for rollback only.
5. Update existing verification scripts to validate the runtime surface instead of validating “points at registry.”
6. After a stabilization window, remove `legacy` profile and any remaining “Codex points at registry” pathways.

## Validation

### Acceptance tasks (20) for runtime surface

1. `runtime build --profile core` produces `manifest.json` with `git_sha`, `profile`, and a stable `build_id`.
2. Re-running `runtime build --profile core` at the same `git_sha` produces identical file hashes and manifest content (modulo timestamp field, if present; prefer no timestamps).
3. `runtime build --profile core` excludes any skill listed as excluded/stray by policy (starting with `registry/catalog-exclusions.json`).
4. `UNITEXT_RUNTIME_ROOT/current` resolves to a valid build directory and contains `skills/` and `manifest.json`.
5. `runtime install --cli codex --profile core` sets Codex `skills_path` to `UNITEXT_RUNTIME_ROOT/current/skills`.
6. Codex `config.toml` contains no occurrence of `registry\\skills` or `/registry/skills` after install.
7. `runtime verify --cli codex` passes on a fresh machine after install.
8. `runtime verify --cli codex` fails if `skills_path` is manually changed back to `registry/skills`.
9. `core` profile contains exactly the essential shortlist plus any required meta-skill(s); count is asserted.
10. Every included skill directory contains `SKILL.md` and no unexpected large subtrees in `core`.
11. A size budget is enforced for `core` (total bytes and per-skill bytes) and is validated by `runtime verify --strict`.
12. `runtime install` writes backups and a rollback plan artifact; presence is asserted in `ops/history/...`.
13. `runtime rollback --last` restores the prior Codex config and prior runtime pointer state.
14. The `unitext-registry` MCP server remains configured for Codex after install and responds to `registry_summary`.
15. On-demand skill retrieval via MCP (`read_registry_file` for a skill `SKILL.md`) works even when the skill is not installed in `core`.
16. `runtime build --profile full` includes all allowed skills and passes `runtime verify --strict` under a separate size budget.
17. `runtime build --profile review` produces a share-safe surface (no machine-local paths, no secret-bearing docs) and passes verify.
18. Claude/Gemini delivery can be configured to point to `UNITEXT_RUNTIME_ROOT/current/skills` and passes a CLI-specific verify check.
19. Updating the repo to a new `git_sha` and running build+install switches `current` atomically (no partial runtime visible).
20. A CI job runs `runtime build --profile core` and `runtime verify --strict` to prevent regressions in surface correctness.

## Risks

- Runtime drift (registry changes not reflected): mitigate with “build then install” workflows and `runtime verify` gating.
- Over-pruning breaks skill usefulness: mitigate with per-skill packaging declarations and a `full` profile escape hatch.
- Windows symlink/junction complexity: mitigate by supporting both “junction current pointer” and “mirror into current directory” modes.
- User confusion between registry and runtime: mitigate with the single agent entrypoint (`RUNTIME.md`), explicit profile language, and strict verify errors that explain what to change.
- Increased tooling surface area: mitigate by keeping build pure, install reversible, verify strict, and logging minimal but complete in `ops/history/`.
