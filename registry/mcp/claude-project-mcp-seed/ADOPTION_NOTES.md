# MCP Adoption Notes

在將真實 MCP server 納入 UniText 前，建議至少確認：

- server name 穩定且可辨識
- transport 類型明確
- command / args 不含個人私密資訊
- 是否屬於 shared config，而非 local-only secret
- server 是否可以在最小環境下啟動，避免只剩文件而無法實跑

若包含 token、secret 或機器專屬 path，應移到 local overlay，而不是直接進 registry。

目前 `claude-project-mcp-seed` 已提升為可執行 baseline：

- registry 內保留相對路徑版 canonical definition
- `bootstrap.py` 會在本機 delivery 時寫入絕對路徑版 `.mcp.json` 與 Codex config
