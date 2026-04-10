# UniText — Test Baseline

> 狀態：Active Baseline
> 更新日期：2026-04-10
> 用途：記錄目前 `main` 分支可直接執行的最低測試基線，以及下一波重建優先順序。

## 1. Current Baseline

本輪 mainline consolidation 後，tracked automated tests 以高訊號 smoke coverage 為主。

目前保留並可直接執行的基線如下：

- `tests/security/test_hardening.py`
  - 驗證安全 hardening guardrails 沒有退化
- `tests/test_registry_inventory.py`
  - 驗證目前 review shortlist 與主要擴張 skill families 仍存在於 registry
- `tests/test_project_map_baseline.py`
  - 驗證 project map 與 governance baseline 所需的核心資產仍存在

## 2. Recommended Command

優先執行：

```bash
python -m unittest tests.security.test_hardening tests.test_registry_inventory tests.test_project_map_baseline
```

若環境使用 `py` 啟動 Python：

```powershell
py -3 -m unittest tests.security.test_hardening tests.test_registry_inventory tests.test_project_map_baseline
```

## 3. What This Baseline Covers

- hardening guardrails for sensitive scripts
- minimum registry inventory integrity
- current project map / governance entry surfaces

## 4. What This Baseline Does Not Yet Cover

目前這個 baseline 還沒有完整覆蓋：

- bootstrap end-to-end 行為
- template export / rebuild export success path
- release hygiene 與 publishability flow
- i18n drift tooling
- project map generated output correctness
- cross-platform script parity

## 5. Rebuild Priorities

下一波應優先補回的測試：

1. `bootstrap.py` / `verify-bootstrap.py` 的正向 smoke path
2. `build-project-map.py` 的生成結果檢查
3. template / rebuild export scripts 的最小成功案例
4. boundary / metadata rule validation 的正向與反向案例

## 6. Policy Note

這份文件描述的是目前 `main` 的可執行最低基線，不代表歷史上所有測試仍完整保留。若後續重新導回更完整的測試集，應更新本文件，而不是默默擴張或縮減範圍。
