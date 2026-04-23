# Template 2 — UniText Runtime Reset Architecture Proposal

## Diagnosis
- UniText is registry-first in principle, but agent runtime entry is document-first and noisy in practice (`README.md`, `INDEX.md`, and multiple governance docs are all used as de facto entrypoints).
- Codex can reach `registry/skills` directly, so runtime behavior depends on how much the agent crawls, not on a bounded contract.
- Runtime concerns are fragmented across scripts (`bootstrap.py`, `verify-bootstrap.py`, `resolve-agent-governance.py`) and prose, with no single low-noise “start here for agents” surface.
- Delivery and verification are partially defined, but not expressed as one explicit runtime API (plan/apply/verify) with stable outputs.
- Current tests protect hardening/inventory/map baselines, but do not fully enforce a runtime-surface contract for cold-start agent behavior.

## Target State
- Keep **registry-first canonical authoring** unchanged: `registry/*` remains the only source of truth.
- Add an **agent-first runtime facade**: a compact, deterministic, Codex-first surface that agents must consume before any deep reads.
- Introduce a single runtime control plane (`runtimectl`) with stable verbs: `build`, `plan`, `apply`, `verify`.
- Make runtime outputs **machine-readable first** (JSON contracts), with concise human mirrors (short markdown).
- Keep cross-CLI extensibility through per-CLI runtime profiles and adapter plugins; Codex is first implementation, not hardcoded architecture.

## Layer Model
| Layer | Purpose | Source of Truth | Mutability |
|---|---|---|---|
| L0 Canonical Authoring | Resource definitions and metadata | `registry/*`, `RESOURCE_SPEC.md` | Author-managed |
| L1 Runtime Build | Compile canonical data into low-noise runtime bundle | `runtime/build/*` generated from L0 | Generated only |
| L2 Runtime Surface | Agent-facing entrypoint and contract | `runtime/ENTRYPOINT.md`, `runtime/surface.v1.json`, `runtime/catalog.min.json` | Generated + reviewed |
| L3 Adapter Execution | CLI-specific plan/apply wiring | `runtime/profiles/*.json`, adapter modules | Tool-managed |
| L4 Verify & Evidence | Runtime conformance and drift detection | tests + `ops/runtime-evidence/*` | Generated on run |

## Runtime Surface
- **Primary entrypoint**: `runtime/ENTRYPOINT.md` (strictly short, no policy essay, no release narrative).
- **Machine contract**: `runtime/surface.v1.json` with:
  - `version`, `read_order`, `allowed_next_reads`, `commands`, `profiles`, `error_codes`.
- **Minimal catalog**: `runtime/catalog.min.json` with only high-signal fields (`id`, `type`, `status`, `canonical_location`, `supported_clis`, `summary`).
- **Policy digest**: `runtime/rules.min.md` distilled from AGENTS/policy sources into runtime-safe operational rules only.
- **Codex-first read path**:
  1. Read `runtime/ENTRYPOINT.md`
  2. Read `runtime/surface.v1.json`
  3. Read `runtime/catalog.min.json`
  4. Read deep files only through declared `allowed_next_reads`
- **Cross-CLI extension**:
  - `runtime/profiles/codex.json` first.
  - Additional `claude.json`, `gemini.json`, `copilot.json`, plus future `custom/*.json` plugin profiles, all sharing one contract schema.

## Delivery and Verify Contract
- **Contracted commands (single front door)**:
  - `runtimectl build` → regenerate runtime bundle from registry.
  - `runtimectl plan --cli <name>` → emit non-mutating delivery plan JSON.
  - `runtimectl apply --cli <name>` → execute plan with backup + audit.
  - `runtimectl verify --suite runtime-surface` → run acceptance tasks and emit conformance report.
- **Command guarantees**:
  - deterministic JSON output
  - explicit exit codes
  - dry-run support for all mutating flows
  - backup-before-mutation and traceable operation IDs

### Acceptance Tasks (20) for Runtime Surface Validation
| ID | Validation Target | Pass Condition |
|---|---|---|
| A01 | Entrypoint noise budget | `runtime/ENTRYPOINT.md` within defined size/section limits |
| A02 | Deterministic read order | `read_order` exists and is acyclic |
| A03 | Codex cold start | Codex profile can route from entrypoint to task execution without direct registry crawl |
| A04 | Minimal catalog schema | `catalog.min.json` validates against schema |
| A05 | Catalog completeness | All `active` registry entries appear in catalog |
| A06 | No hidden deep-read requirement | Default task flow succeeds using declared runtime surface only |
| A07 | Allowed-next-read enforcement | Reads outside declared allowlist are flagged |
| A08 | Build reproducibility | Two consecutive builds produce identical bundle hashes |
| A09 | Plan/apply separation | `plan` performs zero mutation |
| A10 | Backup guarantee | `apply` creates restorable backup before mutation |
| A11 | Audit traceability | Every `apply` has operation ID + evidence artifact |
| A12 | Verify catches drift | Modified runtime artifact without rebuild fails verify |
| A13 | Codex profile conformance | `runtime/profiles/codex.json` passes schema + smoke |
| A14 | Claude profile conformance | Same for Claude profile |
| A15 | Gemini profile conformance | Same for Gemini profile |
| A16 | Copilot profile conformance | Same for Copilot profile |
| A17 | Unknown CLI extensibility | New profile loads without core code change |
| A18 | Failure clarity | Missing/invalid runtime artifact returns defined error code/message |
| A19 | Documentation de-overload | README/INDEX no longer required runtime entry dependencies |
| A20 | End-to-end surface smoke | `build -> plan -> apply(dry-run) -> verify` passes on supported host |

## Migration
1. **Phase 0: Contract freeze**
   - Define `surface.v1` schema and runtime profile schema.
2. **Phase 1: Additive runtime facade**
   - Introduce `runtime/` artifacts without removing current docs/scripts.
3. **Phase 2: Unified control plane**
   - Implement `runtimectl` as wrapper over existing bootstrap/verify logic.
4. **Phase 3: Codex-first cutover**
   - Set Codex documentation and automation to use runtime surface first.
5. **Phase 4: Cross-CLI profile rollout**
   - Add/validate Claude, Gemini, Copilot profiles under same contract.
6. **Phase 5: De-overload docs**
   - Keep README/INDEX for human discovery; remove runtime-critical instructions from them.
7. **Phase 6: Governance enforcement**
   - CI gate on A01–A20 verify suite.

## Validation
- **Static validation**: schema checks for `surface`, `catalog`, and profiles.
- **Behavioral validation**: command-level tests for `build/plan/apply/verify` guarantees.
- **Conformance validation**: A01–A20 as release gate for runtime reset.
- **Evidence model**: each verify run emits machine-readable report + concise markdown summary in `ops/runtime-evidence/`.
- **Backward compatibility check**: existing scripts remain callable during migration; parity assertions ensure no capability loss before deprecation.

## Risks
- **Dual-surface drift**: registry and runtime facade diverge.
  - Mitigation: build reproducibility + drift checks (A08, A12).
- **Overfitting to Codex**: runtime becomes Codex-specific.
  - Mitigation: profile schema and mandatory cross-CLI conformance tasks (A14–A17).
- **Facade bloat over time**: low-noise surface regresses.
  - Mitigation: strict budget and entrypoint constraints (A01, A19).
- **Migration fatigue**: old scripts and new control plane conflict.
  - Mitigation: wrapper-first migration, explicit parity gates.
- **False confidence from docs-only checks**: behavior not validated.
  - Mitigation: end-to-end contract test (A20) required for acceptance.
