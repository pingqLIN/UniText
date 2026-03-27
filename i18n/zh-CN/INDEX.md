# UniText — Index

> 状态：Template Base
> 角色：所有 human / AI 的第一读取点，用于 discovery。

`UniText` 以纯文本作为共享介面，强调跨 CLI 的统一相容与 AI-first discovery。

## 1. 核心文件

建议阅读顺序：

1. `INDEX.md`
2. `VISION.md`
3. `RESOURCE_SPEC.md`
4. `OPERATIONS.md`
5. `PROJECT_MODES.md`
6. `MILESTONES.md`
7. `EXTERNAL_REVIEW_PACKAGE.md`
8. `EXTERNAL_REVIEW_COVER_NOTE.md`
9. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
10. `TEMPLATE_RELEASE_PACKAGE.md`
11. `TEMPLATE_RELEASE_CHECKLIST.md`
12. `SECRET_HANDLING_GUIDELINES.md`
13. `NO_PUBLISH_POLICY.md`
14. `SKILL0_COLLABORATION_VISION.md`

## 2. 资源目录

目前 registry 关心以下 shared resource types：

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

一个最小 catalog entry 至少要包含：

- `id`
- `type`
- `canonical_location`
- `status`

建议额外补上：

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

完整栏位规则请见 `RESOURCE_SPEC.md`。

## 4. 目前 Catalog Entries

### Review Shortlist

目前外部审查主集以 [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) 的 `8 + 4` 精选 skills 为准，而不是全量候选池。

### Review Package

若要整理给外部审查者的资料，请以 [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) 为入口，并使用 `local/scripts/export-review-package.ps1` 产出可重复生成的 review package。

若要直接给审查者最短入口，请先看：

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

若要整理成干净的 starter package，请看 [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) 并使用 `local/scripts/export-template-package.ps1`。

若要验证汇出的 starter package，请使用 `local/scripts/verify-template-package.ps1`。

若要在新机器上完成第一轮 initialize → verify，优先使用：

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### 相关概念笔记

若要评估 `UniText` 与 `skill-0` 的合作方式，请看 [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md)。

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

### Workflow

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | 依 CLI 能力使用 workflow adapter 或 project-local plan mapping。 |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | Bootstrap 会写入 project `.mcp.json` 与 Codex native-config，指向 bundled read-only MCP server。 |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | 可作为 review 与 adoption 任务共用的 agent persona；实际 wiring 仍依 CLI 能力而定。 |

## 5. 范例 Catalog Entries

### 范例：Skill

| Field | Value |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | 使用 skills adapter；实际解析模式依 CLI 能力与本机环境而定。 |

### 范例：MCP Definition

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | 透过 MCP adapter 注册；最终 delivery mode 依 CLI 能力与本机环境而定。 |

## 6. Discovery Rules

`INDEX.md` 回答的是：

- 这里有什么资源
- 各资源的逻辑位置在哪里
- 应该先看哪份规格或操作文件

`INDEX.md` 不直接回答：

- 某个平台的绝对路径
- 最终已解析完成的 delivery mode
- 某个作者工作区的本机配置

## 7. How To Use This Baseline

### For Humans

1. 先读 `VISION.md`
2. 用 `INDEX.md` 建立自己的 starter catalog
3. 用 `RESOURCE_SPEC.md` 定义资源栏位
4. 用 `OPERATIONS.md` 定义平台与 CLI 对接方式

### For AI Agents

1. 先把 `INDEX.md` 当成 discovery 入口
2. 需要 schema 时读 `RESOURCE_SPEC.md`
3. 需要 delivery / mutation 时读 `OPERATIONS.md`
4. 不要把任何单一部署的路径当成规格真相
