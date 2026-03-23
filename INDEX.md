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

### Skills

| Field | Value |
|---|---|
| `id` | `frontend-design` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/frontend-design` |
| `status` | `active` |
| `source_of_truth` | `/registry/skills/frontend-design/SKILL.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

| Field | Value |
|---|---|
| `id` | `pdf` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/pdf` |
| `status` | `active` |
| `source_of_truth` | `/registry/skills/pdf/SKILL.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

| Field | Value |
|---|---|
| `id` | `docx` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/docx` |
| `status` | `active` |
| `source_of_truth` | `/registry/skills/docx/SKILL.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

| Field | Value |
|---|---|
| `id` | `xlsx` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/xlsx` |
| `status` | `active` |
| `source_of_truth` | `/registry/skills/xlsx/SKILL.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

| Field | Value |
|---|---|
| `id` | `mcp-builder` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/mcp-builder` |
| `status` | `active` |
| `source_of_truth` | `/registry/skills/mcp-builder/SKILL.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | Use the skills adapter; resolved mode depends on CLI capabilities and local environment. |

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
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude` |
| `delivery_guidance` | Register through the MCP adapter; the final delivery mode depends on CLI capabilities and local environment. |

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
