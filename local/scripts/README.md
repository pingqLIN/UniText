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

## Platform Note

- 目前腳本是 Windows-first 參考實作。
- 若要支援 POSIX 環境，可用 `rsync`、`ln -s`、`test -L` 等等效命令替代。
