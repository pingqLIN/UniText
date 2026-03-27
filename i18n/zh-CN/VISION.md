# UniText — Vision

> 状态：Template Base
> 原则：以逻辑契约为准，不以任何单一作业系统、目录结构或部署方式作为规格前提。

## 1. What UniText Is

`UniText` 是一个 text-native、registry-first、AI-first 的 shared resource hub，让多个 AI CLI / agent 系统能用同一套纯文本契约共享资源定义与采用方式。

它包含两层：

1. `Registry`
   - 定义 shared resources、canonical identity 与最小契约
2. `Adapter / Operations Control Plane`
   - 将 registry 内容对接到不同 CLI，并处理 install、sync、adopt、repair

## 2. Problem It Solves

`UniText` 要解决的是跨工具共享资源时常见的碎片化问题：

- skills 散落在不同位置
- MCP 定义分散在不同设定格式
- agent instructions 无法共用
- workflow 惯例难以跨工具延续
- 缺少一套 AI 容易读取、版本控制友善的纯文本共同介面

## 3. Architecture Position

正式定位：

**Registry-first, adapter-enabled, operations-governed**

关键原则：

- 没有 registry，就没有共同来源与共同语义
- 没有 adapter，就无法把 registry 真正送进各 CLI
- AI 是重要的 consumer 与协作者，但不是唯一可靠的整合机制

## 4. Resource Types

预设 shared resource types：

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state` 不属于 shared resource type，应独立存在于 `/operations`。

## 5. Discovery and Delivery

`INDEX.md` 负责 discovery，回答：

- 有哪些资源
- 各资源的逻辑位置在哪里
- 哪些 CLI 被支援

`OPERATIONS.md` 负责 delivery，回答：

- 某个 CLI 如何取得资源
- 何时执行 install、sync、adopt、repair
- delivery mode 如何解析

可用的 delivery modes：

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Delivery Triggers

delivery 只能由明确 trigger 启动：

- `bootstrap`
- `sync`
- `adopt`
- `repair`

所有破坏性操作都应遵守：

- 先 dry-run
- 先 backup
- 不可静默决定 canonical source

## 7. Adoption Model

### Soft Adoption

- 先导入 discovery
- 不强迫立刻迁移既有资源

### Formal Adoption

正式纳管流程：

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

若发现同名异内容资源，流程必须停在 `REVIEW / DRY-RUN`。

## 8. Documentation Set

核心文档：

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Path Strategy

主文使用 logical canonical paths，例如：

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

绝对路径与平台专属设定只属于 deployment mapping，不属于愿景层契约。

## 10. Design Principles

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. One-Sentence Positioning

> UniText 是一个 text-native、registry-first、AI-first 的 shared resource hub，透过明确的 adapter 与 operations control plane，让多个 AI CLI 能安全地发现、采用并共享同一套 canonical resources。
