# Local Scripts

這裡放的是 **本機操作腳本**，目前以 Windows PowerShell 為參考實作。

## Current Scripts

- `sync-skills.ps1`
  - 將 `registry/skills/` 同步到本機 skills targets
- `scan-skills.ps1`
  - 掃描候選 skills 並輸出 adoption 檢查結果
- `verify-delivery.ps1`
  - 驗證 source 與常見 skills targets 是否存在、是否為連結、是否可解析
- `health-check.ps1`
  - 對 registry 與 scripts 做最小健康檢查
- `batch-adopt-skills.ps1`
  - 將候選 skills 批次遷入 `registry/skills/`
- `generate-index-entries.ps1`
  - 由 `registry/skills/` 生成 INDEX 所需的 catalog 區塊
- `rollback-skills.ps1`
  - 從 `ops/history/adopt_*` 的 backup 回復指定 skill
- `export-review-package.ps1`
  - 將外部審查所需的 cover note、highlights、核心文件、精選 registry entries 與最小 scripts 匯出到 `ops/review-package/`
- `export-template-package.ps1`
  - 將 template-safe docs、generic examples 與 starter layout 匯出到 `ops/template-package/`

## Governance Note

- `sync-skills.ps1` 與 `batch-adopt-skills.ps1` 都應遵守：
  - dry-run first
  - backup before mutation
  - 產生可追溯 log

## Platform Note

- 目前腳本是 Windows-first 參考實作。
- 若要支援 POSIX 環境，可用 `rsync`、`ln -s`、`test -L` 等等效命令替代。
