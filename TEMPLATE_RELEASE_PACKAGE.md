# UniText — Template Release Package

> 狀態：Active Baseline  
> 用途：定義 template release cleanup 的目標、範圍與可重複匯出流程。

## 1. Purpose

`UniText` 的 template release 不應該是把作者工作區原樣打包出去，而應該是輸出一份：

- 保留核心架構與規格
- 保留最小可用範例
- 排除 local-only state
- 排除歷史治理殘留
- 適合其他使用者 fork / clone 後自行擴充
- 能讓 Claude、Codex、Gemini、Copilot 在 Windows / macOS / Linux 上朝同一套 shared baseline 對齊

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
  - `WORKSPACE_SENSITIVE_METADATA_RULES.json`
  - `WORKSPACE_SENSITIVE_METADATA_RULES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- template-safe root config
  - `.gitattributes`
  - `.gitignore`
  - `.mcp.json`
  - `.claude/settings.json`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- runnable MCP baseline
  - `registry/mcp/claude-project-mcp-seed/`
- starter local overlay skeleton
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
  - `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`
  - `local/scripts/lib/workspace-sensitive-metadata.ps1`
  - `local/scripts/verify-workspace-boundaries.ps1`
  - `local/scripts/get-publishability-report.ps1`
- release metadata
- `manifest.json`
- `release.json`

starter template 也應保留 repo-level line-ending policy，避免不同機器上的 `core.autocrlf` 在首次修改 shared docs 或 scripts 時產生不必要的 CRLF 噪音。

## 3. Exclude

template package 不應包含：

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- `local/docs/PATH_MAP.md`
- 實際使用者帳號、家目錄、絕對路徑
- workspace-specific Cloudflare baseline references with live IDs、hostnames、redirect URIs、or runtime paths
- authoring notes、review archives 與其他 local-only 補充材料
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

若要在匯出前先檢查 authoring repo 的 tracked shared surfaces：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
```

若要直接輸出成「全新的 starter project」而不是一般 template package：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-rebuild-project.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-rebuild-project.ps1 -Path .\ops\rebuild-project\<package-name>
```

匯出後，新使用者的 first-run 建議路徑：

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

若系統只提供 `python3`，請將上述命令中的 `python` 改為 `python3`。

## 5. Export Interpretation

匯出的 template package 代表：

- UniText 的核心契約
- 一份乾淨的 starter layout
- 一組最小 generic examples
- 一條可重複的 cross-platform `bootstrap -> verify` 路徑
- 一份可由 Claude 直接讀取的 `.claude/settings.json`
- 一份可由 project-local MCP 使用的 `.mcp.json` seed
- 一個可供 Copilot CLI 未來 adapter 對接的 shared baseline

它不代表：

- 作者目前的完整工作狀態
- 所有已納管 skills
- 所有 review / audit 證據
- 已完成的本機 delivery wiring
- 任意機器都已經完成的 interpreter pinning
- live workspace-specific infrastructure references；若需要保留結構，只能改成 sanitized placeholder docs
- authoring repo branch 本身已可安全推送；push suitability 仍需另做 repo-side boundary review

## 6. Current Interpretation

截至 2026-03-24，`UniText` 已具備：

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
