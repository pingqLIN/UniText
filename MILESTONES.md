# UniText — Milestones

> 狀態：Active
> 目的：定義對外審查與內部執行都可共用的量化完成條件。

## Phase 1 — Skills Registry Online

- `registry/skills/` 已建立
- 至少 5 個 skills 完成 canonical adoption
- `INDEX.md` 有對應 catalog entries
- `local/scripts/build-runtime-layer.py` 可由 `registry/` 重建 `runtime/`
- `local/scripts/sync-skills.ps1` 指向 `runtime/skills`
- `local/scripts/verify-delivery.ps1` 可驗證 skills source 與 target 狀態
- `local/scripts/health-check.ps1` 可通過基本檢查

## Phase 2 — Full Registry Baseline

- `registry/agents/` 已建立
- `registry/mcp/` 至少 1 個非空示例維持可讀
- `registry/workflow/` 至少 1 個 catalog entry 被正式列出
- `scan` / `verify` / `sync` 三類操作都有最小工具支撐
- `CLI_COMPAT_MATRIX.md` 記錄目前依賴的 CLI 行為與最後驗證日期

## Phase 3 — External Review Ready

- Git repository 已初始化
- `.gitignore` 已排除 local-only 與大型歷史產物
- `README.md`、`INDEX.md`、`RUNTIME.md` 與 current runtime contract 狀態一致
- `README.md`、`INDEX.md`、`docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md` 三者狀態一致
- `docs/reviews/EXTERNAL_REVIEW_PACKAGE.md` 已定義審查範圍、閱讀順序與排除項目
- `docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md` 與 `docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md` 已可作為 reviewer-facing entry docs
- `SECRET_HANDLING_GUIDELINES.md` 已建立治理邊界，並納入核心閱讀順序
- `local/scripts/export-review-package.ps1` 可重複產出 review package
- 已提供跨平台 `bootstrap -> verify` first-run 路徑
- consumer agents 有明確的 runtime-first startup path
- 外部審查可直接看到：
  - 核心架構文件
  - 已 adoption 的 canonical skills
  - 最小 operations scripts
  - 清楚的下一階段里程碑

## Phase 4 — Template Release Ready

- local-only artifacts 不進入發佈包
- template export 流程已文件化
- `TEMPLATE_RELEASE_PACKAGE.md` 與 `TEMPLATE_RELEASE_CHECKLIST.md` 已存在
- `local/scripts/export-template-package.ps1` 可重複產出 starter package
- `local/scripts/verify-template-package.ps1` 可驗證 starter package 結構
- `SECRET_HANDLING_GUIDELINES.md` 已納入 starter package
- `local/scripts/create-git-bundle.py` 可產出可攜 backup artifact
- 已有 template-safe generic examples 可覆蓋 `skills`、`mcp`、`agents`、`workflow`
- 已有 template-safe `local/` skeleton
- `mcp` 至少有一個真正可執行的 baseline
- canonical resource coverage 持續擴張到 `skills`、`mcp`、`agents`、`workflow`
- 至少 2 個 CLI 實際通過 delivery 驗證
