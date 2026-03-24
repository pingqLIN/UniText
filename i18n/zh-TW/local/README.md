# Local Overlay

這個目錄承載的是 **本機部署、腳本、路徑對照與其他非核心覆蓋層**。

它的設計目的很單純：

- 不讓本機配置污染根目錄的核心概念
- 讓本機修編可以集中管理
- 讓整個 `local/` 在必要時可以被直接刪除並重建

## Contents

- `docs/`
  - 本機部署相關說明與對照文件
- `scripts/`
  - 本機執行用腳本

## Current Files

- [docs/authoring](/mnt/q/UniText/local/docs/authoring)
  - 重構前保留下來的 authoring 強化版核心文檔
- [docs/MCP_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/MCP_DEPLOYMENT_NOTES.md)
  - 當前本機 MCP 部署與對接說明
- [docs/PATH_MAP.md](/mnt/q/UniText/local/docs/PATH_MAP.md)
  - 當前部署的路徑參考與歷史對照
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - 當前本機 workflow 對接說明
- [scripts/sync-skills.ps1](/mnt/q/UniText/local/scripts/sync-skills.ps1)
  - 本機同步腳本

## Rule

若某份內容描述的是：

- 這個系統應該如何運作
  - 它不應放在 `local/`
- 這個實例目前怎麼配置
  - 它應放在 `local/`
