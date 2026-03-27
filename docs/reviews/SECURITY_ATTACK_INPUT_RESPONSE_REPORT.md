# UniText 安全攻擊輸入回應報告

> 更新日期：2026-03-27  
> 目的：把既有 attack-input findings 轉成「目前狀態 / 殘餘風險 / 驗證證據」格式，供 Phase 2 驗收使用。

## Executive Summary

相較於 2026-03-25 的版本，這份報告現在有三個核心結論：

1. 幾個當時最重要的 security findings 已不適合再寫成 `unfixed`
2. 真正還存在的，多半是 **explicit opt-in residual risk**
3. 目前已經有 CI 與 regression tests，可把 hardening 從口頭描述提升成可重跑證據

## Treatment Matrix

| Finding | 現況 | 處置結果 | 目前分類 |
|---|---|---|---|
| `SEC-001` `with_server.py` | 預設拒絕 raw shell string | `fixed` | `default-safe / opt-in shell risk remains` |
| `SEC-002A` `rollback-skills.ps1` | safe id + boundary check + backup-before-delete + reparse-point stop | `fixed` | `destructive but guarded` |
| `SEC-002B` `batch-adopt-skills.ps1` | safe id + destination confinement + reparse-point stop | `fixed` | `destructive but guarded` |
| `SEC-002C` `export-template-package.ps1` | output root allowlist + safe package name | `fixed` | `smoke-tested export path` |
| `SEC-002D` `export-review-package.ps1` | output root allowlist + safe package name | `fixed` | `smoke-tested export path` |
| `SEC-003` `bootstrap.py --repo-root` | external root disabled by default, explicit opt-in only | `reclassified` | `mitigated / residual config injection risk` |
| `SEC-004` frontmatter validation | `quick_validate.py` 與 `scan-skills.ps1` now share the same frontmatter inspection path | `fixed` | `validation and metadata extraction share one parser` |

## Current Response by Finding

### SEC-001

**Current status**

- `with_server.py` 現在預設要求 JSON argv list
- raw shell command string 只有在 `--allow-shell` 下才允許

**Validation evidence**

- [with_server.py](/C:/dev/UniText/registry/skills/webapp-testing/scripts/with_server.py)
- [test_hardening.py](/C:/dev/UniText/tests/security/test_hardening.py)

**Residual risk**

- shell mode 仍保留作為顯式 opt-in escape hatch

### SEC-002A / SEC-002B

**Current status**

- PowerShell 路徑腳本目前已共用 [path-safety.ps1](/C:/dev/UniText/local/scripts/lib/path-safety.ps1)
- `rollback-skills.ps1` 與 `batch-adopt-skills.ps1` 都已具備：
  - safe-name validation
  - normalized path boundary checks
  - reparse-point detection
- `rollback-skills.ps1` 也已補上 backup-before-delete

**Validation evidence**

- [rollback-skills.ps1](/C:/dev/UniText/local/scripts/rollback-skills.ps1)
- [batch-adopt-skills.ps1](/C:/dev/UniText/local/scripts/batch-adopt-skills.ps1)
- [test_hardening.py](/C:/dev/UniText/tests/security/test_hardening.py)

**Residual risk**

- 這兩支仍屬 destructive operator tools，流程上仍應優先使用 dry-run

### SEC-002C / SEC-002D

**Current status**

- template / review export scripts 現在都限制在各自 `ops/*` 輸出根之下
- package name 受 safe-name 規則約束

**Validation evidence**

- [export-template-package.ps1](/C:/dev/UniText/local/scripts/export-template-package.ps1)
- [export-review-package.ps1](/C:/dev/UniText/local/scripts/export-review-package.ps1)
- [test_hardening.py](/C:/dev/UniText/tests/security/test_hardening.py)
- [test_release_flows.py](/C:/dev/UniText/tests/test_release_flows.py)

**Residual risk**

- 主要剩 operational misuse risk，不再是原本那種 unrestricted output path 問題

### SEC-003

**Current status**

- `bootstrap.py` 預設拒絕外部 repo root
- 需顯式 `--allow-external-repo-root`
- 非 dry-run 仍需 `--force`

**Why this is now MEDIUM**

- 目前更準確的威脅模型是 configuration injection，不是任意 path traversal
- 風險仍存在，但需要 operator 顯式 opt-in

**Validation evidence**

- [bootstrap.py](/C:/dev/UniText/local/scripts/bootstrap.py)
- [test_hardening.py](/C:/dev/UniText/tests/security/test_hardening.py)

### SEC-004

**Current status**

- `quick_validate.py` 已補上 duplicate-key rejection
- JSON output 已恢復，便於腳本共用與測試
- `scan-skills.ps1` 現在直接呼叫 `quick_validate.py --metadata-json`，validation 與 metadata extraction 走同一套 frontmatter inspection helper
- `scan-skills.ps1` 的 `name` / `description` 摘要已改為從 parser 結果取得，而不是 regex
**Residual risk**

- 目前沒有 material residual risk；若後續有其他 consumer 仍用舊 regex，才需要再做一致化

**Validation evidence**

- [quick_validate.py](/C:/dev/UniText/registry/skills/skill-creator/scripts/quick_validate.py)
- [scan-skills.ps1](/C:/dev/UniText/local/scripts/scan-skills.ps1)
- [test_hardening.py](/C:/dev/UniText/tests/security/test_hardening.py)

## Regression Evidence

目前安全與 release baseline 的主要可重跑證據是：

- [tests/security/test_hardening.py](/C:/dev/UniText/tests/security/test_hardening.py)
- [tests/test_release_flows.py](/C:/dev/UniText/tests/test_release_flows.py)
- [.github/workflows/ci.yml](/C:/dev/UniText/.github/workflows/ci.yml)

本地最新結果：

- `python -m unittest discover -s tests -p "test_*.py"` → `Ran 10 tests ... OK`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1` → `ok = True`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun` → success

## Explicitly Open Items

以下項目不應再與「未修復漏洞」混寫，而應視為後續 hardening / product-boundary 決策：

1. 是否要收斂 `with_server.py --allow-shell` 的使用面。
2. 是否要把 `verify-bootstrap.py` 拆成：
   - seed-state verify
   - active bootstrap verify

## Conclusion

這份 response report 的結論是：

- 2026-03-25 那批 findings 裡，幾個最重要的項目現在已經完成處置或重分類
- 目前的風險敘事應從「尚未修補」改成「哪些已 default-safe、哪些只剩 explicit opt-in residual risk」
- Phase 2 若要通過 `ACT-07`，現在最重要的是維持這份文件與 CI / tests / script behavior 的一致性
