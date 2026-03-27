# ACT-06 Regression Disposition

> 日期：2026-03-27  
> 目的：將 `docs/reviews/PRE_PUSH_AUDIT_2026-03-26.md` 中列出的 4 個歷史失敗項，整理成可驗收的處置結果。

## 結論

ACT-06 的歷史 4 個失敗項目前已全部有明確處置：

- `2` 項屬於 `fixed`
- `1` 項屬於 `replaced by updated test`
- `1` 項屬於 `explicitly deprecated with rationale`

## Disposition Table

| 歷史失敗項 | 目前處置 | 說明 | 主要證據 |
|---|---|---|---|
| `test_bootstrap_force_writes_complete_state_in_isolated_repo` | `fixed` | 新增隔離環境 force bootstrap regression test，驗證可在 temp repo + temp home 下寫出完整 baseline | `tests/test_release_flows.py` |
| `test_bootstrap_force_merges_existing_copilot_mcp_config` | `deprecated with rationale` | Copilot CLI 現在是 `target / adapter pending`，repo 已不再宣稱 bootstrap 會合併 Copilot MCP config，因此舊測試不再屬於 current baseline | `README.md`, `local/docs/CLI_COMPAT_MATRIX.md`, `COPILOT_CLI_ADAPTER_NOTE.md` |
| `test_verify_template_rejects_interrupted_residual` | `replaced by updated test` | 新測試改為直接驗證 template package 若混入 forbidden residual，`verify-template-package.ps1` 會回報 `ok = false` | `tests/test_release_flows.py` |
| `test_generate_index_entries_uses_explicit_root` | `fixed` | `generate-index-entries.ps1` 已補 `-Root`，可對顯式 root 產生 index entries | `local/scripts/generate-index-entries.ps1`, `tests/test_release_flows.py` |

## Notes

### 1. Bootstrap isolated repo

目前 ACT-06 採用的 current-state test，不再依賴原先的歷史環境，而是直接建立：

- temporary repo root
- temporary home directory
- `--allow-external-repo-root`
- `--force`
- `--mode mirror`

這樣能更穩定地驗證 bootstrap 的真實行為，且不污染 maintainer 機器的主設定。

### 2. Copilot merge test

這個舊失敗項之所以不再保留，不是因為「先不測」，而是因為：

- current repo baseline 已把 `Copilot CLI` 定位成 `target`
- 尚未定義穩定 repo-level adapter
- 因此不應再把「合併 Copilot MCP config」當成 ACT-06 的 required regression gate

### 3. Template residual rejection

舊失敗項的關鍵不是某個 PowerShell 屬性名，而是：

- template verify 是否能拒絕不該出現在 starter package 中的殘留內容

因此 current-state test 直接驗證 forbidden residual 的結果，比綁定單一內部屬性更穩。

## Acceptance Statement

依據 `docs/reviews/REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md` 的 ACT-06 驗收標準：

> 歷史 4 個失敗測試均有處置結果：
> - fixed
> - replaced by updated test
> - explicitly deprecated with rationale

目前已符合上述條件。
