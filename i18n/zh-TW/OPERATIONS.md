# UniText — Operations

> 狀態：active baseline
> 角色：delivery modes、mutation gates、rollback expectations、adapter responsibilities。

`registry/` 是 canonical authoring source。`runtime/` 是 agents 的 tracked read model。`local/` 是 machine-specific wiring layer。Operational reports、backups、review packets、generated evidence 預設留本機，除非使用者明確批准 publication。

若操作碰到 passwords、API keys、tokens、credentials 或 live account state，先遵守 [SECRET_HANDLING_GUIDELINES.md](../../SECRET_HANDLING_GUIDELINES.md)。

## 1. Scope

本文件涵蓋：

- adapter responsibilities
- delivery modes
- delivery triggers
- adoption flow
- conflict handling
- backup and rollback
- verification
- troubleshooting

Resource metadata schema 請看 [RESOURCE_SPEC.md](../../RESOURCE_SPEC.md)。

## 2. Delivery Modes

| Mode | Meaning | Use when |
|---|---|---|
| `pointer` | Expose a reference without copying content | Host 只需要 discovery、documentation、path reference |
| `mirror` | Copy reviewed content into a host-owned surface | Symlink 不穩、不支援或不適合 |
| `symlink` | Link a host surface to a runtime projection | 環境支援穩定 links 且需要降低 drift |
| `native-config` | Write to an official host config or instruction surface | Host 支援 documented configuration entrypoint |

Delivery mode 由 adapter logic 與 local constraints resolve，不是固定 resource identity。

## 3. Standard Flow

```text
SCAN -> PLAN -> DRY-RUN -> REVIEW -> DELIVER -> VERIFY
```

| Step | Required outcome |
|---|---|
| `SCAN` | Identify candidate resources、current targets、conflicts、sensitive boundaries |
| `PLAN` | Decide scope、delivery mode、backup path、verification、rollback |
| `DRY-RUN` | Show intended writes before mutation |
| `REVIEW` | Confirm canonical source、conflicts、no-publish impact |
| `DELIVER` | Apply the smallest reviewed mutation |
| `VERIFY` | Prove runtime、host、boundary expectations still hold |

## 4. Adapter Guidance

| Host | Instruction surface | Skill surface | Config/MCP surface | Preferred mode |
|---|---|---|---|---|
| Claude Code | `CLAUDE.md`、`.claude/settings.json` | `.claude/skills/` | `.mcp.json` or managed settings | `mirror` or `symlink` plus `native-config` |
| Codex | `AGENTS.md`、project docs | `.agents/skills/` or configured `skills_path` | `.codex/config.toml`、`codex mcp` | `symlink` plus `native-config` |
| Gemini / Antigravity | `GEMINI.md` or documented host instructions | `.agents/skills/` or host-specific skill path | host settings | compatibility-note driven |
| GitHub Copilot | `.github/copilot-instructions.md`、`.github/instructions/`、`AGENTS.md` | instruction-oriented | repository-native files and supported MCP settings | `native-config` or `pointer` |

Adapter notes 位於 [docs/adapters](../../docs/adapters)。它們記錄 current host-specific support 與 limitations；不是 host config mutation 的授權。

## 5. Safety Rules

### Dry-Run First

```powershell
python local/scripts/build-runtime-layer.py
python local/scripts/bootstrap.py --dry-run
powershell -File .\local\scripts\sync-skills.ps1 -DryRun
```

### Backup Before Mutation

Overwrite host surface 前，保留 backup file、old/new hashes、recoverable `.del` / `.clean` move，或可 review 的 git diff。

### No Silent Canonicalization

若兩個 resources 有同一 ID 但內容不同，停在 review，不自動選 winner，直到 canonical source 明確。

### No Silent Publication

本 repo 沒有任何 command 會授權 push、upload、paste 或 publish。即使 remote 存在或 repo 是 private，no-publish policy 仍然適用。

## 6. Adoption Lanes

| Lane | Meaning | Expected surface |
|---|---|---|
| `local-only overlay` | Machine-specific、user-specific、sensitive、unreviewed resource | local host wiring、ignored local notes |
| `project-local companion` | Resource belongs to one repo or one delivery context | target project docs、`.mcp.json`、repo companion docs |
| `governed registry promotion` | Reusable、share-safe、reviewed shared asset | `registry/` -> `runtime/` -> adapter delivery |

預設使用能滿足任務的最小 lane。只有 reusable 與 publishability boundaries 清楚時，才 promote 到 `registry/`。

## 7. Verification

Docs 與 governance changes：

```powershell
git diff --check
python local/scripts/build-runtime-layer.py
python local/scripts/verify-workspace-boundaries.py --format json
python local/scripts/audit-i18n-drift.py --format json --sample-size 0 --exit-zero
python -m unittest tests.test_registry_inventory tests.security.test_i18n_drift tests.security.test_workspace_sensitive_metadata tests.security.test_release_hygiene
```

Runtime、template 或 delivery changes 可再擴充：

```powershell
python local/scripts/verify-bootstrap.py
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 8. Rollback And Recovery

- Tracked documentation changes 用 git diff review。
- Recoverable cleanup 使用 `.del` 或 `.clean`；永久刪除需要明確 wording。
- Host config changes 從 backup restore 後再 retry。
- Runtime projection drift 先跑 `python local/scripts/build-runtime-layer.py`；只有 registry/runtime source change 是 intentional 時才用 `--write`。

## 9. Troubleshooting

| Symptom | Likely cause | Response |
|---|---|---|
| Agent 讀太多 context | 從 `INDEX.md` 或 `registry/` 開始 | 改從 `RUNTIME.md` 與 `runtime/` 開始 |
| Docs work 造成 runtime catalog 變動 | Manual edit 或 unintended generation | Revert 或說明對應 source change |
| i18n audit reports stale docs | Companion files 落後 source docs in git history | Companion 與 source docs 一起更新與 commit |
| GitHub templates mention public workflow | No-publish boundary 未反映 | 加入 local/private wording，避免敏感 disclosure prompts |
