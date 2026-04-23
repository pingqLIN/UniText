[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> 狀態：Active Baseline
> 用途：定義 shared surfaces 上的 workspace-sensitive metadata 偵測規則、維護方式與驗證邊界。

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` 是 authoring repo 與 exported starter package 共用的規則來源，用來降低以下 drift：

- shared docs 混入本機絕對路徑
- shared scripts 混入 live workspace hostname
- shared governance files 混入 live redirect URI 或 Cloudflare IDs
- boundary verify 與 template verify 使用不同規則集

這份文件回答的是：

- 規則檔各區塊代表什麼
- 什麼時候應該新增規則
- 如何避免把 sanitized placeholder 也誤判成 live metadata
- 調整規則後要跑哪些驗證

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` 目前有四個頂層區塊：

- `shared_surface_scope`
  - 定義 repo-side boundary verify 預設要掃描的 tracked shared surfaces
- `path_rules`
  - 定義哪些 tracked 路徑本身不應出現在 shared surface
- `content_patterns`
  - 定義哪些文字內容屬於 workspace-sensitive metadata
- `self_test_cases`
  - 定義規則自帶的正反案例，避免 regex 修改後產生靜默回歸

## 3. Maintenance Rules

- 新增 shared governance doc 或 shared control script 時，若它屬於 repo-side boundary review 範圍，應同步加入 `shared_surface_scope`
- 新增 live metadata 類型時，優先補 `content_patterns`，再補對應 `self_test_cases`
- 若某個 placeholder 應視為安全範例，必須補一個 `expected_labels = []` 的 self-test case
- 若某條 regex 只是在 script 內作為規則字串出現，應明確設定 `skip_script_pattern_lines`
- 不要把 authoring-only 或 operations-only 路徑塞進 `shared_surface_scope` 來解決誤報；應先檢查文件放置是否錯層

## 4. Required Validation

每次調整 `WORKSPACE_SENSITIVE_METADATA_RULES.json` 後，至少應重跑：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

若此次變更會影響 starter baseline，還應再跑：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

這套規則的目標是：

- 在 shared surface 上提供穩定、可維護、可驗證的 heuristic controls

它不是：

- 所有 secret 類型的完整 schema 驗證器
- 對所有 infrastructure provider 的通用 DLP 系統
- 對 local-only / ops-only 區域做內容全面掃描的工具

如果未來 metadata 類型持續擴大，下一步應該是擴充規則來源與案例，不是把 live references 再放回 shared registry。
