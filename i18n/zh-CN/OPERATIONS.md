# UniText — Operations

> 状态：Template Base
> 角色：定义 adapter / operations control plane 的责任、delivery 规则与安全边界。

所有 delivery 与 mutation 都应以 `UniText` 的纯文本 registry / spec 契约为 source of truth。

若操作涉及 password、API key、token、credential 等 sensitive material，请同时遵守 `SECRET_HANDLING_GUIDELINES.md`。

## 1. Scope

本文件涵盖：

- adapter responsibilities
- delivery modes
- delivery triggers
- adoption flow
- drift / repair
- logical-to-physical mapping

本文件不涵盖：

- shared resource metadata schema
- 单一平台的唯一实作方式
- 本机 authoring repo 的历史状态

## 2. Delivery Modes

| Mode | When to use |
|---|---|
| `pointer` | discovery 或非机器注册型资源 |
| `mirror` | CLI 需要本地副本、或 symlink 不稳定 |
| `symlink` | CLI 需要固定路径，且环境支援稳定连结 |
| `native-config` | CLI 有正式设定入口可注册资源 |

`delivery mode` 由 adapter 在操作时解析，不是资源的固定硬属性。

## 3. Delivery Resolution Rules

adapter 应依优先序考虑：

1. 有正式设定入口时，优先 `native-config`
2. 需要固定路径且平台支援稳定连结时，用 `symlink`
3. 无法安全使用 symlink 时，用 `mirror`
4. 主要用途是 discovery 或入口时，用 `pointer`

## 4. Delivery Triggers

delivery 只能由明确 trigger 启动：

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Safety Rules

### Dry-Run First

以下操作应先产出 dry-run plan：

- `adopt`
- `repair`
- 会覆写既有状态的 `sync`

### Backup Before Mutation

所有破坏性操作都应具备：

- backup 或等价回复点
- 可追溯的操作记录
- 失败时的停止条件

### No Silent Canonicalization

若遇到同名异内容资源：

- 必须停在 review
- 必须让 operator 明确决定 canonical source

## 6. Adoption Flow

1. `SCAN`
   - 扫描候选来源，列出可 adopt 的资源与 readiness 状态
2. `REVIEW`
   - 依 review checklist 检查 metadata、内容品质与 canonical source 合法性
3. `DRY-RUN`
   - 预览 adopt 或 delivery 将修改哪些目标、是否需要 backup
4. `ADOPT`
   - 将来源内容写入 registry canonical location，若覆写既有内容需先 backup
5. `DELIVER`
   - 由 adapter 将 registry 内容送到对应 CLI，若会覆写既有状态需保留 log 与 backup
   - 若 CLI 支援 `native-config`，可在 `bootstrap` 阶段写入 machine-local config，但 canonical definition 仍留在 `registry/`
6. `VERIFY`
   - 验证档案存在性、路径解析、delivery mode 与目标 CLI 载入条件是否成立

## 6.1 First-Run Baseline

若目标是让新的 template 使用者在 macOS / Linux / Windows 都能完成最小初始化，应至少提供：

- 一条跨平台 `bootstrap`
- 一条跨平台 `verify`
- 一条可携的 repo backup 流程
- 一个可实跑的最小 MCP baseline

## 7. Operations State

以下内容属于 operations state，而非 shared resources：

- inventories
- baselines
- backups
- drift reports
- repair plans
- audit trails

它们应位于 `/operations`，不应混入 `/registry`。

## 8. Logical-to-Physical Mapping

逻辑路径是稳定契约；实体路径是 deployment-specific mapping。

| Logical area | Meaning | Physical mapping examples |
|---|---|---|
| `/registry/skills` | canonical skill sources | shared directory、repo subdir、mounted path |
| `/registry/mcp` | canonical MCP definitions | config folder、generated manifest root |
| `/registry/agents` | canonical agent instruction roots | agent profiles directory、shared prompt library |
| `/registry/workflow` | workflow docs / runbooks | workflow folder、project-local docs |
| `/operations` | inventories、backups、drift logs | ops folder、state store、audit directory |
