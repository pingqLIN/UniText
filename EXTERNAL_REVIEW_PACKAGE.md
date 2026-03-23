# UniText — External Review Package

> 狀態：Active Baseline  
> 用途：定義外部審查要看什麼、不要看什麼，以及如何重複產出 review package。

## 1. Purpose

`UniText` 已經進入可供外部審查的 baseline 階段，但審查重點應集中在：

- 核心架構是否合理
- canonical registry 是否已落地
- operations safety model 是否可執行
- 精選 shared resources 是否足以代表專案方向

本文件的目的是把這些內容收斂成一個可重複整理的審查包，而不是把整個作者工作區原封不動交出去。

## 2. Recommended Reading Order

建議外部審查者依以下順序閱讀：

1. `README.md`
2. `INDEX.md`
3. `VISION.md`
4. `RESOURCE_SPEC.md`
5. `OPERATIONS.md`
6. `MILESTONES.md`
7. `PROJECT_STATUS_REPORT_2026-03-23.md`
8. `ESSENTIAL_SKILLS_SHORTLIST.md`

若要看實際資源樣本，再往下看：

- `registry/skills/` 的 `8 + 4` 精選主集
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- `local/scripts/` 中的最小治理腳本

## 3. Review Scope

目前 review package 應包含以下內容：

- 核心文件
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `MILESTONES.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- 最小治理文件
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- 最小治理腳本
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
- 精選 shared resources
  - `registry/skills/` 的 `8 + 4` 主集
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Out Of Scope

以下內容不應作為外部審查主體：

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- 本機特定 path mapping 與個人環境殘留
- 未納入 shortlist 的候選 skills
- 未追蹤或實驗中的內容

`local/docs/authoring/` 屬於作者工作參考資料，不是 canonical review source。

## 5. Export Command

在 repo root 執行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

預設輸出到：

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

若只想先檢查內容，不寫入檔案：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validation

建議在 export 前至少先跑一次：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

若要確認 canonical skills delivery 對齊：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Current Interpretation

截至 2026-03-24，`UniText` 已具備：

- 外部審查可讀的核心文件
- `8 + 4` 精選 skills 主集
- agent / mcp / workflow 的最小可審查 seed
- 可重複產出 review package 的整理流程

因此目前最適合的定位是：

**external-review-ready baseline**

而不是：

**template release ready**
