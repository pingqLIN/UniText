# Local Overlay Starter

> 狀態：Template Example

這個 `local/` skeleton 的目的，是幫新使用者快速建立自己的 deployment overlay，而不是直接沿用作者工作區設定。

它預設面向：

- `Claude Code`
- `Codex`
- `Gemini CLI`
- `Copilot CLI`
- `Windows`
- `macOS`
- `Linux`

## Included Files

- `local/docs/PATH_MAP.md`
- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`
- `local/scripts/create-git-bundle.py`
- `local/scripts/sync-skills.ps1`

## Expected Customization

- 將 path mapping 換成自己的實際環境
- 先用 `bootstrap.py --dry-run` 看初始化會改哪些地方
- `bootstrap.py` 會同時處理 `Codex` 與 `Copilot CLI` 的本機 baseline，避免手動維護多套 config
- 若系統只提供 `python3`，將命令中的 `python` 改為 `python3`
- 依使用的 CLI 增刪 delivery targets
- 視需要保留 PowerShell 版本或改寫其他平台腳本
