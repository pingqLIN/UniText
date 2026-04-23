# Claude Project MCP Seed

這個目錄提供 **canonical MCP baseline**，用來示範 UniText 如何收納並交付可實跑的 MCP 資源。

這個 MCP 的定位是：

- 輕量
- 唯讀
- project-local
- 按需啟用

它不是一般 skill 搜尋或日常工作流程的必要依賴。大多數情況下，agent 可以直接依靠已載入的 skill 清單或本機檔案系統完成工作；只有在你想用標準 MCP 介面讀取 UniText registry 時，才需要把它掛上。

## Contents

- `definition.json`
  - canonical MCP definition，可供 adapter 或 bootstrap 腳本轉成實際 CLI 設定
- `server.py`
  - read-only MCP server，提供 registry summary、entry listing、core doc / registry file read

## Why It Exists

- 給 registry 一個非空的 MCP entry
- 作為第一個真實可用的 MCP baseline
- 幫助審查者理解：MCP 類資源在 UniText 中如何落地

## What It Is Good For

- 用標準 MCP tool 介面列出 registry 項目
- 在受限環境中提供一個明確、收斂的唯讀入口
- 示範如何把 repo 內的 registry 能力包成一個小型 MCP server

## What It Is Not For

- 不是一般 skill discovery 的必要前提
- 不是高頻工具
- 不是需要預設常駐掛載的 server
- 不提供寫入、同步、索引或大型初始化流程

## Operational Notes

- 啟動成本低，握手通常是次秒級
- `tools/list` 幾乎可視為即時
- 主要成本只在第一次讀 registry 內容時做少量本地檔案存取
- 如果本機已有直接檔案權限，很多盤點工作也可不經 MCP 完成

## Current Status

- `status`: `active-baseline`
- 用途：lightweight project-local read-only registry server
- delivery guidance：
  - Claude project 使用 tracked repo root `.mcp.json` template-safe seed
  - Codex 可由 bootstrap 腳本寫入 `~/.codex/config.toml` 的 `[mcp_servers.unitext_registry]`
  - Copilot CLI 可由 bootstrap 腳本寫入 `~/.copilot/mcp-config.json`
- default guidance：
  - 不建議為一般日常 session 預設掛載
  - 建議保留 canonical definition，並在需要 registry tool surface 時再做 machine-local wiring
- 下一步：視 CLI 能力再補更完整的 adapter wiring
