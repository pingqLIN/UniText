---
description: Closure note for the DEVILS_ADVOCATE review chain, summarizing what has been fixed, what remains open, and what should now be cited externally
---

# DEVILS_ADVOCATE_REVIEW Closure Note

> 日期：2026-03-27
> 用途：在保留原始審查鏈的前提下，補上一份 current-state closure note，說明哪些問題已修正、哪些已降級為 residual risk、哪些仍未完成。

## 結論摘要

截至 2026-03-27，`DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md` 所列的主要發布阻斷項，大部分已完成修補並已具備可重跑驗證證據。

目前較準確的狀態是：

- 原先的 P0 / P1 核心 blocker 已大致關閉
- 部分安全議題已改為 `default-safe with explicit opt-in residual risk`
- `ACT-11 i18n 抽查` 已完成 spot check，但譯本更新波次仍未執行

## 狀態表

| 項目 | 原審查判定 | 目前狀態 | 依據 |
|---|---|---|---|
| Proprietary / restricted skills 邊界 | blocker | fixed | `SKILLS_PUBLIC_RELEASE_POLICY.md`、`THIRD_PARTY_LICENSES.md`、`registry/skills/SOURCES.md` |
| 根目錄 `LICENSE` 缺失 | blocker | fixed | 根目錄 `LICENSE` 已存在 |
| 第三方授權彙整不足 | partial | fixed | `THIRD_PARTY_LICENSES.md` 已建立 |
| authoring workspace hygiene | blocker | fixed with export boundary | `verify-workspace-hygiene.ps1`、export scripts、`.gitignore` |
| root-level dependency management 缺失 | blocker | fixed | `requirements.txt`、`requirements-tooling.txt`、`requirements-skill-local.txt`、`requirements-dev.txt` |
| CI workflow 缺失 | blocker | fixed | `.github/workflows/ci.yml` |
| regression coverage 不足 | blocker | fixed to current baseline | `tests/test_release_flows.py`、`tests/security/test_hardening.py`、`ACT_06_REGRESSION_DISPOSITION_2026-03-27.md` |
| 安全文件落後於程式碼 | blocker | fixed | `SECURITY_REVIEW_ADVISORY.md`、`SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md` |
| README / matrix 支持語氣過強 | blocker | fixed | README 與 `CLI_COMPAT_MATRIX.md` 已收斂為 `verified / partial / target` |
| `SEC-001` shell 風險 | unresolved security issue | mitigated / residual risk remains | `with_server.py` 預設拒絕 raw shell string，但仍保留 `--allow-shell` |
| `ACT-11` i18n 抽查 | follow-up | completed with findings | `ACT_11_I18N_SPOT_CHECK_2026-03-27.md` |

## 已修正項

### 1. Release blocker 已不再維持原狀

以下原始 blocker 已不再成立為「未修正」狀態：

- 根目錄 `LICENSE` 缺失
- 第三方授權彙整缺失
- root-level dependency manifests 缺失
- CI workflow 缺失
- regression tests 缺失
- README / matrix 語氣過強但無驗證分級

### 2. Release boundary 已落到 package 層

目前公開 package 的邊界不是只停留在文件宣告，而是已落到：

- export scripts
- hygiene verification
- holdback 清單
- `github-backed` skill provenance

因此現在更準確的說法是：

- **authoring workspace 仍不應直接發布**
- **但 clean exported package 已有可驗證的 release-safe baseline**

### 3. 安全敘事已從「未修補」改成「已緩解 + residual risk」

`SEC-001`、`SEC-002*`、`SEC-003` 現在不應再用原始審查中的語氣描述為「尚未修復」。

較準確的 current-state 描述是：

- `SEC-001`：default-safe，保留 explicit opt-in shell risk
- `SEC-002*`：fixed
- `SEC-003`：reclassified / mitigated with explicit opt-in path

## 尚未完成項

目前仍未關閉的主要尾項是譯本更新本身，而不是 `ACT-11` spot check。

### i18n 更新波次

`ACT-11` 已透過 `ACT_11_I18N_SPOT_CHECK_2026-03-27.md` 完成抽樣檢查；目前剩餘的是依該報告補做譯本同步。

因此若要對外使用最保守且準確的說法，建議採用：

> Phase 1 已完成，Phase 2 已完成核心項並可視為完成，Phase 3 已完成 review chain 與 i18n confidence spot check；目前剩餘的是譯本同步 follow-up，而非 release blocker。

## 建議引用方式

目前對內或對外引用時，建議優先使用以下順序：

1. `DEVILS_ADVOCATE_REVIEW_2026-03-26.md`
   - historical snapshot
2. `DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md`
   - code-state verification
3. `DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md`
   - 2026-03-27 的 current decision basis
4. `DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md`
   - current-state closure note
5. `ACT_11_I18N_SPOT_CHECK_2026-03-27.md`
   - i18n confidence report

若只引用一句話，建議改用：

> 原始反對方向是對的，但截至 2026-03-27，多數發布阻斷項已完成修補；目前剩餘的是 residual risk 管理與譯本同步 follow-up，而不再是原審查所描述的全面 release blocker 狀態。

## 本次驗證依據

本 closure note 係基於以下 fresh verification：

- `python -m unittest discover -s tests -p "test_*.py"` → `Ran 13 tests ... OK`
- `powershell -File .\local\scripts\health-check.ps1` → `ok = True`
- `powershell -File .\local\scripts\verify-workspace-hygiene.ps1` → `ok = True`
- `powershell -File .\local\scripts\export-review-package.ps1 -DryRun`
  - `public_skill_source_model = github-backed`
  - `restricted_skills_holdback` 仍有生效
