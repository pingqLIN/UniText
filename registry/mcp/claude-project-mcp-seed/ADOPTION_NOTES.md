# MCP Adoption Notes

在將真實 MCP server 納入 UniText 前，建議至少確認：

- server name 穩定且可辨識
- transport 類型明確
- command / args 不含個人私密資訊
- 是否屬於 shared config，而非 local-only secret

若包含 token、secret 或機器專屬 path，應移到 local overlay，而不是直接進 registry。

