[English](../../README.md) | [繁體中文](../zh-TW/README.md) | [简体中文](README.md) | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [한국어](../ko/README.md) | [Italiano](../it/README.md)

# UniText

> **一个以纯文本为核心、以 registry 为先的多 AI CLI 共享资源中枢。**
>
> 将 Claude Code、Codex、Gemini CLI 等工具的资源定义统一到同一套文字契约中。

> **同步注记（2026-03-27）：** 本译本仅反映 current-baseline 的一部分。英文 `README.md` 仍是 authoritative version。与 support、release boundary、review scope 相关的高风险段落已同步，其余内容可能仍保留较旧的解读。

---

## 为什么需要它

如果你同时使用多个 AI CLI 工具，资源很容易散落各处：

- 同一个 skill 被定义了三次，而且三份内容还略有差异
- MCP server 设定散在各种不同格式，其他工具根本读不到
- 只有某一个 CLI 看得懂的 agent 指令
- 根本不知道哪一份才是 canonical copy

UniText 用一个共享 registry 加上一层受治理的 delivery layer 解决这件事。**一份定义，所有工具共用。**

---

## 运作方式

```text
UniText/
├── registry/          ← canonical definitions（存在什么）
│   ├── skills/        ← shared skill definitions
│   ├── mcp/           ← MCP server definitions
│   ├── agents/        ← agent instructions & personas
│   └── workflow/      ← runbooks、plans、conventions
│
├── local/             ← deployment overlay（在这台机器上怎么接）
│   ├── docs/          ← path maps、deployment notes
│   └── scripts/       ← 这台机器要用的 sync scripts
│
└── ops/               ← operations state（不是 shared resources）
    └── history/       ← timestamped audit trail
```

`registry/` 层是 platform-agnostic 的，使用逻辑 canonical path（例如 `/registry/skills`、`/registry/mcp`），而不是作业系统专属的绝对路径。`local/` 层则负责把这些逻辑路径解析到你实际的机器上。

---

## 架构

**Registry-first、adapter-enabled、operations-governed。**

| Layer | Role |
|-------|------|
| **Registry** | 定义有哪些 shared resources，以及它们的 canonical identity |
| **Adapter** | 把 registry 内容送到各个 CLI（mirror、symlink、native-config、pointer） |
| **Operations** | 管理何时、如何做 mutation - 包含 backup、dry-run 与 audit trail |

### 资源类型

| Type | Logical Root | 放什么 |
|------|--------------|--------|
| `skills` | `/registry/skills` | 供 AI agents 共用的 skill definitions |
| `mcp` | `/registry/mcp` | 跨 CLI 的 MCP server definitions |
| `agents` | `/registry/agents` | 共用 agent instructions、persona、system prompts |
| `workflow` | `/registry/workflow` | runbooks、planning templates、conventions |

### Delivery Modes

每种资源都可以依 CLI 能力采用不同的 delivery 方式：

- `pointer` - discovery only，不复制内容
- `mirror` - 透过 robocopy / rsync 做本机复本
- `symlink` - 指向 canonical source 的固定路径连结
- `native-config` - 注册到 CLI 自己的设定格式中

---

## 开始使用

### 1. Fork 或 clone 这个 repository

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. 加入你的第一个资源

在 `registry/skills/` 底下建立一个 skill：

```text
registry/skills/my-skill/
└── SKILL.md
```

最小 `SKILL.md`：

```yaml
---
name: my-skill
description: 这个 skill 的一句话说明
---

## Usage

给 AI agent 的操作说明...
```

### 3. 把它注册到 catalog

在 `INDEX.md` 新增一笔 entry：

| Field | Value |
|-------|-------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. 初始化本机 CLI wiring

优先使用跨平台的 bootstrap 路径：

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py` 会对齐共用 skills target、更新 Codex 的 `skills_path`，并为 bundled MCP baseline 写入 project-local `.mcp.json`。`sync-skills.ps1` 仍保留作为 Windows PowerShell 的参考实作。

---

## 支援的 CLIs

| CLI | Delivery Mode | Notes |
|-----|---------------|-------|
| **Claude Code** | mirror / symlink | `~/.claude/skills` |
| **Gemini CLI** | mirror / symlink | `~/.gemini/skills` |
| **Codex** | native-config + project-local MCP | `~/.codex/config.toml` 中的 `skills_path` 与 `[mcp_servers.*]` |
| **GitHub CLI** | native-config | `config.yml` |

完整的每个 CLI 路径对照请见 [template/examples/local/docs/PATH_MAP.template.md](template/examples/local/docs/PATH_MAP.template.md)。

---

## 治理规则

UniText 采用 **no silent changes** 政策：

1. **只接受明确 trigger** - `bootstrap`、`sync`、`adopt`、`repair`
2. **先备份再 mutation** - 任何破坏性操作都会先在 `ops/` 建立 timestamped snapshot
3. **先 dry-run 再 delivery** - 在实际变更前先预览
4. **有冲突就停止** - 若同一资源有两个版本不一致，系统会停下来交由人工审查
5. **完整 audit trail** - 每一次操作都会写入 `ops/history/`

正式 adoption flow：`SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## 文件

| File | Purpose |
|------|---------|
| [INDEX.md](INDEX.md) | Discovery entry point - 目前有哪些资源、在哪里 |
| [VISION.md](VISION.md) | 架构原则与设计理由 |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | 所有 shared resources 的 metadata contract |
| [OPERATIONS.md](OPERATIONS.md) | Delivery modes、triggers 与安全规则 |
| [PROJECT_MODES.md](PROJECT_MODES.md) | 区分 authoring repo 与 project template |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | secret 储存、redaction、password / API key 边界 |
| [MILESTONES.md](MILESTONES.md) | 量化的 phase 目标与外部审查准备检查点 |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | 目前审查波次使用的 `8 + 4` 精选 skills 集合 |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | 审查者阅读顺序、范围与可重复汇出流程 |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | 给外部审查者的送审说明 |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | 供快速掌握的精简审查摘要 |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | template release cleanup 的范围、排除项与汇出流程 |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | starter package 发布前的清理检查清单 |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | 说明 UniText 与 skill-0 如何分工：一个做治理与分发，一个做拆解与原子化提炼 |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | 给 agents 与协作者的 local-first 发布边界 |

阅读顺序：`EXTERNAL_REVIEW_COVER_NOTE.md` → `EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `SKILL0_COLLABORATION_VISION.md`

---

## 两种使用方式

### 作为 starter template

Fork 这个 repo。移除 `ops/history/`、`backup/` 与这台机器专属的 `local/` 路径。把你自己的 skills 与 MCP definitions 放进 `registry/`。再依你的环境调整 `local/scripts/`。

### 作为 reference implementation

阅读核心文件以理解架构。然后把 registry 结构、resource spec、delivery modes、operations audit trail 这些模式，移植到你自己的环境。

---

## 设计原则

- **Registry first** - 先定义，再 delivery
- **Discovery before automation** - 先知道有什么，再做同步
- **Platform-agnostic contracts** - 规格用逻辑路径，本机覆盖层才用绝对路径
- **Minimum viable metadata** - `id`、`type`、`canonical_location`、`status` 就足够起步
- **Safe mutation** - 一律 dry-run + backup + explicit trigger
- **AI as consumer** - AI 模型读取并使用 registry，但不负责保证 delivery

---

## 状态

| Component | Status |
|-----------|--------|
| Core documentation | Stable |
| Registry structure | Active - `skills/`、`mcp/`、`workflow/`、`agents/` roots 已存在 |
| Skills registry | Active baseline - 第一批 canonical skills 已纳管，后续扩充仍在进行 |
| Agents registry | Active seed - 已建立 `registry-curator` entry |
| MCP registry | Active baseline - 已有 canonical definition 与可执行的 read-only server |
| Workflow registry | Draft seed - 已有 workflow doc 与 plan template |
| Operations audit trail | Active |
| Sync、bootstrap 与 review scripts | `local/scripts/` 内的 active baseline |
| External review package | Active baseline - 已有 reviewer guide 与 export script |
| Template release cleanup | Release candidate - 已有 package guide、checklist、export + verify scripts、generic examples 与 local overlay skeleton |

---

## 授权

MIT

---

*给使用超过一个 AI 工具、并希望有单一真相来源的人。*

