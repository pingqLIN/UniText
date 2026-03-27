# UniText — Template Release Package

> 狀態：Active Baseline  
> 用途：定義 template release cleanup 的目標、範圍與可重複匯出流程。

> **同步註記（2026-03-27）：** 本譯本僅反映 current-baseline 的一部分。英文 `TEMPLATE_RELEASE_PACKAGE.md` 仍是 authoritative version。與 release boundary、排除項、skills 規則相關的高風險段落已同步，其餘內容可能仍保留舊版解讀。

## 1. Purpose

`UniText` 的 template release 不應該是把作者工作區原樣打包出去，而應該是輸出一份：

- 保留核心架構與規格
- 保留最小可用範例
- 排除 local-only state
- 排除歷史治理殘留
- 適合其他使用者 fork / clone 後自行擴充

這份 package 的定位是：

**starter template**

而不是：

**authoring workspace snapshot**

## 2. Include

目前 template package 應包含：

- 核心文件
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- template-safe root config
  - `.gitignore`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- starter local overlay skeleton
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
- release metadata
  - `manifest.json`
  - `release.json`

## 3. Exclude

template package 不應包含：

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- 實際使用者帳號、家目錄、絕對路徑
- review-specific docs
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Export Command

在 repo root 執行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

預設輸出到：

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

若只想先檢查內容，不寫入檔案：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

若要驗證輸出的 package：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

匯出後，新使用者的 first-run 建議路徑：

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Export Interpretation

匯出的 template package 代表：

- UniText 的核心契約
- 一份乾淨的 starter layout
- 一組最小 generic examples

它不代表：

- 作者目前的完整工作狀態
- 所有已納管 skills
- 所有 review / audit 證據
- 已完成的本機 delivery wiring

## 6. Current Interpretation

截至 2026-03-27，`UniText` 已具備：

- 外部審查 package
- reviewer-facing entry docs
- template release cleanup baseline
- 可重複產出 template package 的 export script
- starter local overlay skeleton
- template package verification script
- release metadata
- cross-platform first-run scripts
- portable bundle backup flow

因此目前最適合的判讀是：

**template release candidate**

而不是：

**authoring workspace snapshot**

