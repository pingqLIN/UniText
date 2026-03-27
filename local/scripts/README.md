# Local Scripts

這裡放的是 **本機操作腳本**。

- `*.ps1` 保留 Windows-first 參考實作
- `*.py` 提供跨平台 bootstrap / verify / backup 路徑

## Current Scripts

- `bootstrap.py`
  - 跨平台初始化 skills delivery、Codex native-config 與 project `.mcp.json`
- `verify-bootstrap.py`
  - 跨平台檢查 first-run 結果是否與目前 repo 對齊
- `create-git-bundle.py`
  - 建立可攜的 `git bundle` 備份，降低僅靠本地工作樹的單點風險
- `sync-skills.ps1`
  - 將 `registry/skills/` 同步到本機 skills targets
- `scan-skills.ps1`
  - 掃描候選 skills 並輸出 adoption 檢查結果
- `verify-delivery.ps1`
  - 驗證 source 與常見 skills targets 是否存在、是否為連結、是否可解析
- `health-check.ps1`
  - 對 registry 與 scripts 做最小健康檢查
- `verify-workspace-hygiene.ps1`
  - 檢查 `.gitignore`、tracked source 與 seed config 是否符合 release hygiene 邊界
- `batch-adopt-skills.ps1`
  - 將候選 skills 批次遷入 `registry/skills/`
- `generate-index-entries.ps1`
  - 由 `registry/skills/` 生成 INDEX 所需的 catalog 區塊
- `report-docs-scale.ps1`
  - 依 canonical docs / review archive / i18n / workspace residue 口徑輸出 markdown 規模報表
- `rollback-skills.ps1`
  - 從 `ops/history/adopt_*` 的 backup 回復指定 skill
- `export-review-package.ps1`
  - 將外部審查所需的 cover note、highlights、核心文件、精選 registry entries 與最小 scripts 匯出到 `ops/review-package/`
- `export-template-package.ps1`
  - 將 template-safe docs、generic examples 與 starter layout 匯出到 `ops/template-package/`
- `verify-template-package.ps1`
  - 驗證輸出的 template package 是否包含必要 starter 結構，且不含 review-only / local-only 內容
- `export-rebuild-project.ps1`
  - 將目前 repo 重建成可重新命名、可重新初始化的 fresh-project baseline，輸出到 `ops/rebuild-project/`
- `verify-rebuild-project.ps1`
  - 在 template package 驗證之上，再確認 rebuild guide 與 fresh-project 入口存在

## Governance Note

- `sync-skills.ps1` 與 `batch-adopt-skills.ps1` 都應遵守：
  - dry-run first
  - backup before mutation
  - 產生可追溯 log

## Platform Note

- 新的 first-run 路徑優先使用 `bootstrap.py` 與 `verify-bootstrap.py`。
- `sync-skills.ps1` 仍保留作 Windows PowerShell 參考實作與治理樣板。
