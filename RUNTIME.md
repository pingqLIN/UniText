# UniText Runtime Entry

> 狀態：Active baseline
> 角色：consumer agents 的第一讀取點。

如果你是要執行任務的 agent，先讀這裡，不要先把 `README.md` 或 `INDEX.md` 當作 startup surface。

## First Read Order

1. [runtime/START.md](runtime/START.md)
2. [runtime/RULES.md](runtime/RULES.md)
3. [runtime/ROUTES.md](runtime/ROUTES.md)
4. [runtime/catalog.json](runtime/catalog.json)

## Runtime Contract

- `registry/` 是 canonical authoring source，不是預設 consumer runtime。
- `runtime/` 是 tracked runtime read model，提供低噪音入口與 runtime projection。
- `bootstrap.py` 會先重建 `runtime/`，再把各 CLI 的本機 target 指到 `runtime/skills`。
- Codex 只應讀自己的本機 `skills_path` target，不應直接指向 `registry/skills`，也不應由 bootstrap 自動寫入全域 `unitext_registry`。
- 若需要回讀 canonical source，優先走 repo/project-local MCP surface，而不是依賴 Codex 全域註冊。

## Human Docs

- [README.md](README.md) 給 human orientation。
- [INDEX.md](INDEX.md) 給 human discovery 與 catalog。
- [docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md](docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md) 給既有工作環境接入與新資源 lane 選擇。
- [docs/operations/skill-runtime-codex-duplication.SOP.md](docs/operations/skill-runtime-codex-duplication.SOP.md) 給同名 skill 在 UniText runtime 與 Codex local bundle 雙曝光時的處理程序。
- [docs/architecture/runtime-transition-inventory.md](docs/architecture/runtime-transition-inventory.md) 給 runtime reset 盤點與歷史入口。
- 如果 runtime surface 缺資料，再從 `runtime/` 指到對應 canonical doc。
