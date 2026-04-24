# UniText — Test Baseline

> 狀態：Active Baseline
> 更新日期：2026-04-24
> 用途：記錄目前 `main` 分支可直接執行的最低測試基線，以及下一波重建優先順序。

## 1. Current Baseline

本輪 runtime-first consolidation 後，tracked automated tests 仍以高訊號 smoke coverage 為主，但已不再只覆蓋 4 個最小檔案。`python -m unittest` 在此 repo 不會自動 discover 測試，請使用下方 explicit suite 或 discover command。

目前保留並可直接執行的基線如下：

- `tests/security/test_hardening.py`
  - 驗證安全 hardening guardrails 沒有退化
- `tests/security/test_release_hygiene.py`
  - 驗證 release hygiene report 的 blocker / warning / clean-scope 分類
- `tests/security/test_i18n_wave.py`
  - 驗證 i18n wave report 能區分 line-ending-only、changed、untracked 與 clean
- `tests/security/test_copilot_session.py`
  - 驗證 Copilot session payload 與 project MCP wiring 檢查邏輯
- `tests/security/test_catalog_generation.py`
  - 驗證 catalog generation 對正式、excluded、stray skill entries 的分類
- `tests/test_registry_inventory.py`
  - 驗證目前 review shortlist 與主要擴張 skill families 仍存在於 registry
- `tests/test_bootstrap_verify_smoke.py`
  - 驗證 `bootstrap.py -> verify-bootstrap.py` 可在隔離的 temp home 上走通，不會依賴真實使用者設定
- `tests/test_runtime_bundle_hidden_entries.py`
  - 驗證 `runtime/skills/.system/` 這類 hidden local overlays 不會被當成 runtime baseline 同步或 verify 要求
- `tests/test_project_map_baseline.py`
  - 驗證 project map 與 governance baseline 所需的核心資產仍存在
- `tests/test_project_map_share_safe.py`
  - 驗證 interactive / share-safe project-map surface contract、handoff contract，以及頁內 refresh 後 static artifacts 的 stale 提醒

## 2. Recommended Command

完整 explicit gate：

```bash
python -m unittest tests.security.test_hardening tests.security.test_release_hygiene tests.security.test_i18n_wave tests.security.test_copilot_session tests.security.test_catalog_generation tests.test_registry_inventory tests.test_bootstrap_verify_smoke tests.test_runtime_bundle_hidden_entries tests.test_project_map_baseline tests.test_project_map_share_safe
```

快速 discover gate：

```bash
python -m unittest discover -s tests -p "test*.py"
```

若環境使用 `py` 啟動 Python：

```powershell
py -3 -m unittest tests.security.test_hardening tests.security.test_release_hygiene tests.security.test_i18n_wave tests.security.test_copilot_session tests.security.test_catalog_generation tests.test_registry_inventory tests.test_bootstrap_verify_smoke tests.test_runtime_bundle_hidden_entries tests.test_project_map_baseline tests.test_project_map_share_safe
```

## 3. What This Baseline Covers

- hardening guardrails for sensitive scripts
- release hygiene and publishability report classification
- i18n wave classification logic
- minimum registry inventory integrity
- isolated `bootstrap -> verify` smoke coverage for local runtime wiring
- hidden local runtime overlay handling for materialized Codex bundles
- current project map / governance entry surfaces
- interactive vs. share-safe project-map contract and handoff metadata

## 4. What This Baseline Does Not Yet Cover

目前這個 baseline 還沒有完整覆蓋：

- 真實使用者 home / live CLI config 上的 bootstrap end-to-end 行為
- template export / rebuild export success path
- live publishability decision with real remote / review state
- i18n drift coverage beyond the wave-classification fixture layer
- rendered project-map browser behavior with real Playwright screenshots
- cross-platform script parity

## 5. Rebuild Priorities

下一波應優先補回的測試：

1. 真實 home-dir / live config 邊界下的 `bootstrap.py` / `verify-bootstrap.py` 驗證
2. `build-project-map.py` 的生成結果與 browser rendering 檢查
3. template / rebuild export scripts 的最小成功案例
4. boundary / metadata rule validation 的正向與反向案例

## 6. Policy Note

這份文件描述的是目前 `main` 的可執行最低基線，不代表歷史上所有測試仍完整保留。若後續重新導回更完整的測試集，應更新本文件，而不是默默擴張或縮減範圍。
