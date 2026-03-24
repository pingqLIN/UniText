# Claude Project MCP Seed

這個目錄提供 **canonical MCP baseline**，用來示範 UniText 如何收納並交付可實跑的 MCP 資源。

## Contents

- `definition.json`
  - canonical MCP definition，可供 adapter 或 bootstrap 腳本轉成實際 CLI 設定
- `server.py`
  - read-only MCP server，提供 registry summary、entry listing、core doc / registry file read

## Why It Exists

- 給 registry 一個非空的 MCP entry
- 作為第一個真實可用的 MCP baseline
- 幫助審查者理解：MCP 類資源在 UniText 中如何落地

## Current Status

- `status`: `active-baseline`
- 用途：project-local read-only registry server
- delivery guidance：
  - Claude project 可由 bootstrap 腳本寫入 repo root `.mcp.json`
  - Codex 可由 bootstrap 腳本寫入 `~/.codex/config.toml` 的 `[mcp_servers.unitext_registry]`
- 下一步：視 CLI 能力再補更完整的 adapter wiring
