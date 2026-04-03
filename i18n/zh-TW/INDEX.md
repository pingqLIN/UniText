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
6. `DOCUMENT_PLACEMENT_POLICY.md`
7. `WORKSPACE_SENSITIVE_METADATA_RULES.md`
8. `TEMPLATE_RELEASE_PACKAGE.md`
9. `TEMPLATE_RELEASE_CHECKLIST.md`
10. `REBUILD_AS_NEW_PROJECT.md`
11. `SECRET_HANDLING_GUIDELINES.md`
12. `NO_PUBLISH_POLICY.md`
13. `COPILOT_CLI_ADAPTER_NOTE.md`
14. `SKILL0_COLLABORATION_VISION.md`

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

### Review Package

若要整理給外部審查者的資料，請以 [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) 為入口，並使用 `local/scripts/export-review-package.ps1` 產出可重複生成的 review package。

若要直接給審查者最短入口，請先看：

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

若要整理成乾淨的 starter package，請看 [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) 並使用 `local/scripts/export-template-package.ps1`。

若要驗證匯出的 starter package，請使用 `local/scripts/verify-template-package.ps1`。

若要先驗證 authoring repo 的 tracked shared surfaces 沒有混入 live workspace metadata，請使用 `local/scripts/verify-workspace-boundaries.ps1`。

若要在未來討論 push suitability 前先做本地報告，請使用 `local/scripts/get-publishability-report.ps1`。

若要調整 shared metadata 偵測規則或理解規則案例，請先看 [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md)，再使用 `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`。

若要直接把目前 repo 重建成一份新的 starter project，請看 [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md)，並使用：

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

若要在新機器上完成第一輪 initialize → verify，優先使用：

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

若要理解 `Copilot CLI` 目前的 repo-level bootstrap baseline、限制與後續跨平台驗證方向，請看 [COPILOT_CLI_ADAPTER_NOTE.md](COPILOT_CLI_ADAPTER_NOTE.md)。

若要評估 `UniText` 與 `skill-0` 的合作方式，請看 [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md)。

### Skills

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

### Workspace-Specific Skills

以下 skills 已存在於 shared registry，但不屬於目前外部審查主集的 `8 + 4` shortlist。

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `cloudflare` | Workspace | `/registry/skills/cloudflare` | `active` |
| `wrangler` | Workspace | `/registry/skills/wrangler` | `active` |
| `building-mcp-server-on-cloudflare` | Workspace | `/registry/skills/building-mcp-server-on-cloudflare` | `active` |
| `cloudflare-governance` | Workspace | `/registry/skills/cloudflare-governance` | `active` |
| `cloudflare-access-mcp` | Workspace | `/registry/skills/cloudflare-access-mcp` | `active` |
| `cloudflare-edge-security` | Workspace | `/registry/skills/cloudflare-edge-security` | `active` |
| `cloudflare-runtime-sync` | Workspace | `/registry/skills/cloudflare-runtime-sync` | `active` |
| `cloudflare-tunnel-dns` | Workspace | `/registry/skills/cloudflare-tunnel-dns` | `active` |

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
| `supported_clis` | `claude, codex, copilot` |
| `delivery_guidance` | Bootstrap writes a project `.mcp.json`, a Codex native-config entry, and a Copilot `~/.copilot/mcp-config.json` entry pointing to the bundled read-only MCP server. |

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
- local authoring plans、review notes、或 live workspace baselines 應放哪裡；這部分請看 `DOCUMENT_PLACEMENT_POLICY.md`

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
