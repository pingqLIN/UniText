# UniText — Rebuild As A New Project

> Status: Active Baseline
> Purpose: Turn the current UniText repository into a clean starter project instead of treating the authoring repo as the project itself.

## 1. Intent

`UniText` 應該同時扮演兩個角色：

- reference implementation
- fresh-project starter

當你要把它整理成「全新的專案」時，正確做法不是直接複製整個 authoring workspace，而是透過 rebuild export 產生一份乾淨的新專案基線。

## 2. Rebuild Output

rebuild package 應保留：

- 核心契約與規格
- template-safe root config
- starter local overlay
- generic examples
- cross-platform bootstrap / verify flow

rebuild package 不應保留：

- review-only docs
- authoring workspace snapshots
- local-only history
- backup / recovered / `.bak_*`
- 機器專屬絕對路徑
- live workspace-specific Cloudflare baseline references with real IDs、hostnames、redirect URIs、or runtime paths

## 3. Rebuild Command

在 repo root 執行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-rebuild-project.ps1
```

預設輸出到：

```text
ops/rebuild-project/rebuild_YYYYMMDD_HHMMSS/
```

若只想先看內容而不寫入：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-rebuild-project.ps1 -DryRun
```

## 4. Rebuild Verification

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-rebuild-project.ps1 -Path .\ops\rebuild-project\<package-name>
```

## 5. Next Step After Export

拿到 rebuild package 後，建議的第一輪初始化順序：

1. 進入匯出的 rebuild package
2. 以它作為新的 repo baseline
3. 執行：
   - `python local/scripts/bootstrap.py --dry-run`
   - `python local/scripts/bootstrap.py --force`
   - `python local/scripts/verify-bootstrap.py`
4. 把 examples 換成自己的 `skills / agents / mcp / workflow`
5. 視需要重新命名 repo、README 與 catalog entries

## 6. Rule Of Thumb

若你想保留 `UniText` 當參考實作，就留在目前 repo 工作。

若你想把它當成一個新的、乾淨的起始專案，請以 rebuild export 的產物為準，而不是直接把整個 authoring repo 複製出去。
