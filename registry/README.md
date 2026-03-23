# Registry

這個目錄承載的是 **canonical shared resources**。

原則：

- 進入 `registry/` 的內容，應被視為 shared/canonical
- 本機部署差異、路徑映射與執行腳本，不應放在這裡
- 若某份內容屬於 local overlay，應移入 `local/`

目前已存在的 canonical roots：

- `registry/skills/`
- `registry/mcp/`
- `registry/workflow/`

後續若 `agents` 正式納管，也應收斂到這個目錄之下。
