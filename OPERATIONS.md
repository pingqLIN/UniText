# UniText — Operations

> Status: active baseline
> Role: delivery modes, mutation gates, rollback expectations, and adapter responsibilities.

`registry/` is the canonical authoring source. `runtime/` is the tracked read model for agents. `local/` is the machine-specific wiring layer. Operational reports, backups, review packets, and generated evidence stay local unless the user explicitly approves publication.

If an operation touches passwords, API keys, tokens, credentials, or live account state, follow [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) first.

## 1. Scope

This document covers:

- adapter responsibilities
- delivery modes
- delivery triggers
- adoption flow
- conflict handling
- backup and rollback
- verification
- troubleshooting

It does not define the resource metadata schema. See [RESOURCE_SPEC.md](RESOURCE_SPEC.md) for that contract.

## 2. Delivery Modes

| Mode | Meaning | Use when |
|---|---|---|
| `pointer` | Expose a reference without copying content | The host only needs discovery, documentation, or a path reference |
| `mirror` | Copy reviewed content into a host-owned surface | Symlinks are unstable, unsupported, or inappropriate |
| `symlink` | Link a host surface to a runtime projection | The environment supports stable links and drift reduction matters |
| `native-config` | Write to an official host config or instruction surface | The host supports a documented configuration entrypoint |

Delivery mode is resolved by adapter logic and local constraints. It is not a fixed resource identity.

## 3. Standard Flow

```text
SCAN -> PLAN -> DRY-RUN -> REVIEW -> DELIVER -> VERIFY
```

| Step | Required outcome |
|---|---|
| `SCAN` | Identify candidate resources, current targets, conflicts, and sensitive boundaries |
| `PLAN` | Decide scope, delivery mode, backup path, verification, and rollback |
| `DRY-RUN` | Show intended writes before mutation |
| `REVIEW` | Confirm canonical source, conflicts, and no-publish impact |
| `DELIVER` | Apply the smallest reviewed mutation |
| `VERIFY` | Prove runtime, host, and boundary expectations still hold |

## 4. Delivery Triggers

Delivery may start only from explicit triggers:

- `bootstrap`
- `sync`
- `adopt`
- `repair`

Agents should not silently rewrite host configuration because a registry entry exists.

## 5. Adapter Guidance

| Host | Instruction surface | Skill surface | Config/MCP surface | Preferred mode |
|---|---|---|---|---|
| Claude Code | `CLAUDE.md`, `.claude/settings.json` | `.claude/skills/` | `.mcp.json` or managed settings | `mirror` or `symlink` plus `native-config` |
| Codex | `AGENTS.md`, project docs | `.agents/skills/` or configured `skills_path` | `.codex/config.toml`, `codex mcp` | `symlink` plus `native-config` |
| Gemini / Antigravity | `GEMINI.md` or documented host instructions | `.agents/skills/` or host-specific skill path | host settings | compatibility-note driven |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/instructions/`, `AGENTS.md` | instruction-oriented | repository-native files and supported MCP settings | `native-config` or `pointer` |

Adapter notes live under [docs/adapters](docs/adapters). They record current host-specific support and limitations; they are not permission to mutate host config.

## 6. Safety Rules

### Dry-Run First

Run dry-run or preview mode before any operation that can change tracked files, local host configuration, or mirrored runtime content.

Known dry-run surfaces include:

```powershell
python local/scripts/build-runtime-layer.py
python local/scripts/bootstrap.py --dry-run
powershell -File .\local\scripts\sync-skills.ps1 -DryRun
```

### Backup Before Mutation

When overwriting an existing host surface, keep one of:

- a backup file
- a generated report with old and new hashes
- a recoverable `.del` / `.clean` move
- a git diff that is reviewed before commit

### No Silent Canonicalization

If two resources have the same ID but different content:

- stop at review
- do not pick a winner automatically
- preserve both until the canonical source is explicit

### No Silent Publication

No command in this repository grants permission to push, upload, paste, or publish. The no-publish policy applies even when a remote exists or the repository is private.

## 7. Adoption Lanes

| Lane | Meaning | Expected surface |
|---|---|---|
| `local-only overlay` | Machine-specific, user-specific, sensitive, or unreviewed resource | local host wiring, ignored local notes |
| `project-local companion` | Resource belongs to one repo or one delivery context | target project docs, `.mcp.json`, repo companion docs |
| `governed registry promotion` | Reusable, share-safe, reviewed shared asset | `registry/` -> `runtime/` -> adapter delivery |

Default to the smallest lane that satisfies the task. Promote to `registry/` only when reuse and publishability boundaries are clear.

## 8. Verification

For documentation and governance changes:

```powershell
git diff --check
python local/scripts/build-runtime-layer.py
python local/scripts/verify-workspace-boundaries.py --format json
python local/scripts/audit-i18n-drift.py --format json --sample-size 0 --exit-zero
python -m unittest tests.test_registry_inventory tests.security.test_i18n_drift tests.security.test_workspace_sensitive_metadata tests.security.test_release_hygiene
```

For runtime, template, or delivery changes, expand to the relevant scripts:

```powershell
python local/scripts/verify-bootstrap.py
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 9. Rollback And Recovery

- Use git diff for tracked documentation changes.
- Use `.del` or `.clean` for recoverable cleanup; permanent deletion requires explicit wording.
- For host config changes, restore from backup before retrying.
- For runtime projection drift, rerun `python local/scripts/build-runtime-layer.py` first; use `--write` only when the registry/runtime source change is intentional.

## 10. Troubleshooting

| Symptom | Likely cause | Response |
|---|---|---|
| Agent reads too much context | It started from `INDEX.md` or `registry/` | Route it through `RUNTIME.md` and `runtime/` |
| Runtime catalog changed during docs work | Manual edit or unintended generation | Revert or explain the corresponding source change |
| i18n audit reports stale docs | Companion files lag source docs in git history | Update companions and commit them with source docs |
| GitHub templates mention public workflow | No-publish boundary not reflected | Add local/private wording and avoid sensitive disclosure prompts |
| Same skill appears in multiple places | Source-of-truth vs runtime projection confusion | Use runtime preambles and registry source pointers |

## 11. Related Docs

- [RUNTIME.md](RUNTIME.md)
- [RESOURCE_SPEC.md](RESOURCE_SPEC.md)
- [DOCUMENT_PLACEMENT_POLICY.md](DOCUMENT_PLACEMENT_POLICY.md)
- [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md)
- [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md)
