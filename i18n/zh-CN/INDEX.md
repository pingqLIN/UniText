# UniText — Index

> 状态：Template Base
> 角色：所有 human / AI 的第一读取点，用于 discovery。

`UniText` 以纯文本作为共享接口，强调跨 CLI 的统一兼容与 AI-first discovery。

## 1. Core Docs

建议阅读顺序：

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
13. `docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md`
14. `docs/concepts/SKILL0_COLLABORATION_VISION.md`

## 2. Resource Catalog

目前 registry 关注以下 shared resource types：

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | 可被多个 CLI 共用的 skill 定义 |
| `mcp` | `/registry/mcp` | canonical MCP definitions |
| `agents` | `/registry/agents` | 共用 agent 指令与 persona 定义 |
| `workflow` | `/registry/workflow` | 共用流程、runbook、planning guidance |

以下内容不是 shared resource type：

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories、backups、drift logs、history records |

## 3. Starter Catalog Shape

一个最小 catalog entry 应至少包含：

- `id`
- `type`
- `canonical_location`
- `status`

建议额外补上：

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

完整字段规则见 `RESOURCE_SPEC.md`。

## 4. Current Catalog Entries

### Review Shortlist

目前外部审查主集以 [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) 的 `8 + 4` 精选 skills 为准，而不是全量候选池。

### Review Package

若要整理给外部审查者的资料，请以 [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) 为入口，并使用 `local/scripts/export-review-package.ps1` 产出可重复生成的 review package。

若要直接给审查者最短入口，请先看：

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

若要整理成干净的 starter package，请看 [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) 并使用 `local/scripts/export-template-package.ps1`。

若要验证导出的 starter package，请使用 `local/scripts/verify-template-package.ps1`。

若要先验证 authoring repo 的 tracked shared surfaces 没有混入 live workspace metadata，请使用 `local/scripts/verify-workspace-boundaries.ps1`。

若要在未来讨论 push suitability 前先做本地报告，请使用 `local/scripts/get-publishability-report.ps1`。

若要调整 shared metadata 检测规则或理解规则案例，请先看 [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md)，再使用 `local/scripts/validate-workspace-sensitive-metadata-rules.ps1`。

若要直接把当前 repo 重建成一份新的 starter project，请看 [REBUILD_AS_NEW_PROJECT.md](REBUILD_AS_NEW_PROJECT.md)，并使用：

- `local/scripts/export-rebuild-project.ps1`
- `local/scripts/verify-rebuild-project.ps1`

若要在新机器上完成第一轮 initialize → verify，优先使用：

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

若要理解 `Copilot CLI` 目前的 repo-level bootstrap baseline、限制与后续跨平台验证方向，请看 [docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md](docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md)。

若要评估 `UniText` 与 `skill-0` 的合作方式，请看 [docs/concepts/SKILL0_COLLABORATION_VISION.md](docs/concepts/SKILL0_COLLABORATION_VISION.md)。

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

以下 skills 已存在于 shared registry，但不属于目前外部审查主集的 `8 + 4` shortlist。

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
| `delivery_guidance` | Bootstrap 会写入 project `.mcp.json`、Codex native-config 条目，以及指向 bundled read-only MCP server 的 Copilot `~/.copilot/mcp-config.json` 条目。 |

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

- 这里有什么资源
- 各资源的逻辑位置在哪里
- 应该去看哪份规格或操作文件

`INDEX.md` 不直接回答：

- 某个平台的绝对路径
- 最终已解析完成的 delivery mode
- 某个作者工作区的本机配置
- local authoring plans、review notes、或 live workspace baselines 应放在哪里；这部分请看 `DOCUMENT_PLACEMENT_POLICY.md`

## 7. How To Use This Baseline

### For Humans

1. 先读 `VISION.md`
2. 用 `INDEX.md` 建立自己的 starter catalog
3. 用 `RESOURCE_SPEC.md` 定义资源字段
4. 用 `OPERATIONS.md` 定义平台与 CLI 对接方式

### For AI Agents

1. 先把 `INDEX.md` 当成 discovery 入口
2. 需要 schema 时读 `RESOURCE_SPEC.md`
3. 需要 delivery / mutation 时读 `OPERATIONS.md`
4. 不要把任何单一部署的路径当成规格真相
