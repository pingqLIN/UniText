# UniText — Index

> 狀態：Template Base
> 角色：所有 human / AI 的第一讀取點，用於 discovery。

`UniText` 以純文本作為共享介面，強調跨 CLI 的統一相容與 AI-first discovery。

## 1. Core Docs

建議閱讀順序：

1. `INDEX.md`
2. `VISION.md`
3. `RESOURCE_SPEC.md`
4. `OPERATIONS.md`
5. `PROJECT_MODES.md`
6. `TEMPLATE_RELEASE_PACKAGE.md`
7. `TEMPLATE_RELEASE_CHECKLIST.md`
8. `REBUILD_AS_NEW_PROJECT.md`
9. `SECRET_HANDLING_GUIDELINES.md`
10. `NO_PUBLISH_POLICY.md`
11. `COPILOT_CLI_ADAPTER_NOTE.md`
12. `SKILL0_COLLABORATION_VISION.md`

## 2. Resource Catalog

目前 registry 關心以下 shared resource types：

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | 可被多個 CLI 共用的 skill 定義 |
| `mcp` | `/registry/mcp` | canonical MCP definitions |
| `agents` | `/registry/agents` | 共用 agent 指令與 persona 定義 |
| `workflow` | `/registry/workflow` | 共用流程、runbook、planning guidance |

以下內容不是 shared resource type：

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories、backups、drift logs、history records |

## 3. Starter Catalog Shape

一個最小 catalog entry 應至少包含：

- `id`
- `type`
- `canonical_location`
- `status`

建議額外補上：

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

完整欄位規則見 `RESOURCE_SPEC.md`。

## 4. Current Catalog Entries

### Review Shortlist

目前外部審查主集以 [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) 的 `8 + 4` 精選 skills 為準，而不是全量候選池。

這代表下方列出的 skills 表格是：

- curated review surface
- template / review 敘事中正式對外說明的 skills
- 不是 `registry/skills` 目錄的 full catalog

若要取得 full registry skills 的驗證後 catalog 物件，請使用：

- `local/scripts/generate-index-entries.ps1 -AsJson`

任何尚未被正式納入 catalog 的工作樹項目，即使目錄存在，也不自動等於正式發布 surface。

### Review Package

若要整理給外部審查者的資料，請以 [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) 為入口，並使用 `local/scripts/export-review-package.ps1` 產出可重複生成的 review package。

若要直接給審查者最短入口，請先看：

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

若要整理成乾淨的 starter package，請看 [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) 並使用 `local/scripts/export-template-package.ps1`。

若要驗證匯出的 starter package，請使用 `local/scripts/verify-template-package.ps1`。

若要直接把目前 repo 重建成一份新的 starter project，請看 [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md)，並使用：

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

若要在新機器上完成第一輪 initialize → verify，優先使用：

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

若要理解 `Copilot CLI` 為何已列入 starter template 目標、但目前仍屬 `adapter pending`，請看 [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md)。

若要評估 `UniText` 與 `skill-0` 的合作方式，請看 [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md)。

### Skills In Curated Review Surface

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `pdf` | Core 8 | `/registry/skills/pdf` | `active` |
| `docx` | Core 8 | `/registry/skills/docx` | `active` |
| `xlsx` | Core 8 | `/registry/skills/xlsx` | `active` |
| `pptx` | Core 8 | `/registry/skills/pptx` | `active` |
| `mcp-builder` | Core 8 | `/registry/skills/mcp-builder` | `active` |
| `skill-creator` | Core 8 | `/registry/skills/skill-creator` | `active` |
| `webapp-testing` | Core 8 | `/registry/skills/webapp-testing` | `active` |
| `doc-coauthoring` | Core 8 | `/registry/skills/doc-coauthoring` | `active` |
| `frontend-design` | Expansion 4 | `/registry/skills/frontend-design` | `active` |
| `web-artifacts-builder` | Expansion 4 | `/registry/skills/web-artifacts-builder` | `active` |
| `internal-comms` | Expansion 4 | `/registry/skills/internal-comms` | `active` |
| `theme-factory` | Expansion 4 | `/registry/skills/theme-factory` | `active` |

### Full Registry Note

`registry/skills` 的實際目錄面可能大於目前 review shortlist。

因此：

- `INDEX.md` 負責 discovery 與 curated surface 敘事
- full registry entries 應由驗證後腳本輸出取得
- 不應再把手寫 shortlist 表格誤讀為 full catalog

### Workflow

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Use workflow adapter or project-local plan mapping depending on CLI capability. |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | Bootstrap writes a project `.mcp.json` plus Codex native-config entry pointing to the bundled read-only MCP server. |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use as a shared agent persona for review and adoption tasks; actual wiring depends on CLI capability. |

## 5. Example Catalog Entries

### Example: Skill

| Field | Value |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

### Example: MCP Definition

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | Register through the MCP adapter; the final delivery mode depends on CLI capabilities and local environment. |

## 6. Discovery Rules

`INDEX.md` 回答的是：

- 這裡有什麼資源
- 各資源的邏輯位置在哪裡
- 應該去看哪份規格或操作文件

`INDEX.md` 不直接回答：

- 某個平台的絕對路徑
- 最終已解析完成的 delivery mode
- 某個作者工作區的本機配置

## 7. How To Use This Baseline

### For Humans

1. 先讀 `VISION.md`
2. 用 `INDEX.md` 建立自己的 starter catalog
3. 用 `RESOURCE_SPEC.md` 定義資源欄位
4. 用 `OPERATIONS.md` 定義平台與 CLI 對接方式

### For AI Agents

1. 先把 `INDEX.md` 當成 discovery 入口
2. 需要 schema 時讀 `RESOURCE_SPEC.md`
3. 需要 delivery / mutation 時讀 `OPERATIONS.md`
4. 不要把任何單一部署的路徑當成規格真相
