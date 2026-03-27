# UniText × skill-0 — Collaboration Vision

> 状态：Concept Draft
> 目的：定义 `UniText` 与 `skill-0` 的关系、合作空间、可能途径，以及目前缺少的机制。

## 1. Executive Summary

`UniText` 与 `skill-0` 不是互斥或重复的专案，而是可以形成上下游关系的两个层次：

- `UniText` 负责 shared resources 的 **registry / delivery / governance**
- `skill-0` 负责把高阶 skill 吸纳、拆解、正规化成更通用的 **atomic operation set**

因此，两者最合理的合作方式不是「谁取代谁」，而是：

**UniText 提供 canonical inputs 与可治理的承载面，skill-0 提供 decomposition / normalization / recomposition 能力。**

## 2. Each Project Solves a Different Problem

### UniText

`UniText` 解的是：

- shared resource 如何被 canonical 化
- 如何在多个 AI CLI 之间 delivery
- 如何用 `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY` 管理变更

也就是：

**distribution / governance problem**

### skill-0

`skill-0` 解的是：

- 一个高阶 skill 实际由哪些最小操作单元构成
- 哪些步骤是可重用的 primitive
- 哪些描述只是 surface wording，哪些才是核心操作
- 高阶 skill 是否可以重新组装成更小、更通用、更可移植的能力集合

也就是：

**abstraction / compiler / normalization problem**

## 3. Relationship Between the Two

如果站在 `skill-0` 的目标来看，`UniText` 最有价值的角色不是「被分发的结果」，而是：

- 一个稳定的 high-level skill source
- 一个有逻辑身份与 metadata 的 canonical corpus
- 一个可被持续分析、比较、追踪的技能资料集

从这个角度看，两者的关系可描述为：

| Project | Primary role |
|---|---|
| `UniText` | canonical source of truth for shared resources |
| `skill-0` | analyzer / decomposer / compiler over high-level skills |

一句话说：

**UniText 保存 skill，skill-0 解构 skill。**

## 4. Current Collaboration Space

目前即使不改动 `UniText` 的核心 schema，两个专案也已经有合作空间：

### 4.1 Use UniText as input corpus

`skill-0` 可以直接以这些内容作为输入：

- `registry/skills/*/SKILL.md`
- `INDEX.md` 里的 catalog metadata
- `RESOURCE_SPEC.md` 提供的 identity / canonical location 契约

这让 `skill-0` 分析的不是一堆散落副本，而是一组较干净的 canonical skill corpus。

### 4.2 Use UniText as a governed staging ground

`skill-0` 的分析输出目前可以先不进入 canonical registry，而先放在：

- `/operations`
- 例如 `ops/analysis/skill-0/`

这样做的好处是：

- 不会过早污染目前的 shared resource schema
- 可以先观察分析格式是否稳定
- 可以把 `skill-0` 视为 analysis pipeline，而不是立刻升格成 canonical source

### 4.3 Use UniText review flow to evaluate derived outputs

当 `skill-0` 产出：

- atom maps
- normalized step sets
- shared subroutine clusters
- recomposition candidates

这些输出可以先比照 `UniText` 的 review mindset 被检查：

- identity 是否稳定
- 命名是否清楚
- 与原 skill 的对映是否可追踪
- 是否需要人工决定 canonical form

## 5. Most Likely Collaboration Modes

### Mode A — skill-0 as external analyzer

`skill-0` 把 `UniText` 当资料来源，输出 analysis reports，但不反写 registry。

适合用途：

- 快速验证 decomposition 方法
- 做 skill overlap analysis
- 找 reusable primitives

优点：

- 导入成本最低
- 几乎不需要动 `UniText` schema

缺点：

- 结果停留在 sidecar artifacts
- 不容易成为 shared canonical resource

### Mode B — skill-0 as sidecar generator

`skill-0` 读取 `registry/skills`，并在相邻位置生成 machine-readable sidecar，例如：

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

优点：

- 可以建立 skill 与 atom 的明确对映
- 比纯 report 更容易做 tooling

缺点：

- 会开始碰到 `UniText` schema 边界问题
- 需要定义哪些 sidecar 属于 canonical，哪些只是 generated

### Mode C — primitives become a first-class resource type

若合作成熟，`UniText` 可以新增正式资源类型，例如：

- `/registry/primitives`
- 或 `/registry/operations`

这会让 `skill-0` 的输出不再只是分析附属物，而是变成可被 registry 正式纳管的 shared resources。

优点：

- 形成真正的共同语汇层
- 有机会支撑跨 skill recomposition

缺点：

- 需要修改 `UniText` 的 resource model
- 需要新的 metadata spec、adoption flow 与 verification rules

## 6. What Is Missing Today

目前两者还不能自然深度整合，主要缺的是以下几类机制。

### 6.1 Missing canonical type for primitives

`UniText` 目前的一级 resource type 只有：

- `skills`
- `mcp`
- `agents`
- `workflow`

尚未有：

- `primitives`
- `operations`
- `atoms`

因此 `skill-0` 真正最关心的产物，在 `UniText` 里还没有第一级承载面。

### 6.2 Missing metadata spec for atomic units

目前 `RESOURCE_SPEC.md` 适合描述高阶 shared resources，但还没有定义：

- atom id
- operation signature
- preconditions / postconditions
- composition rules
- provenance back to source skill

### 6.3 Missing adoption flow for derived artifacts

`UniText` 目前有 skills adoption flow，但还没有一套专门处理下列情况的流程：

- 同一 skill 被分解出不同 atom sets
- 多个 skill 对应到相似但不完全相同的 primitive
- 某个 atom 是否足够稳定到值得 canonicalize

### 6.4 Missing verification model

如果要让 `skill-0` 的输出进入更正式的合作阶段，至少需要回答：

- decomposition 是否稳定
- 是否可 round-trip recomposition
- 是否真的提升跨 skill reuse
- 是否只是重新命名原本的描述

### 6.5 Missing boundary between analysis and canon

目前还缺一条清楚规则：

- 哪些 `skill-0` 产物只是 analysis
- 哪些产物已经可以视为 canonical shared resource

这个边界不清楚时，最安全的作法仍是先放在 `ops/analysis/skill-0/`。

## 7. Recommended Near-Term Direction

短期最合理的方向不是立刻修改 `UniText` 的 core schema，而是采取：

**Mode A -> Mode B 的渐进式合作**

### Phase A — Analysis Only

先做：

- 以 `registry/skills/*/SKILL.md` 作为输入
- 产出 decomposition reports
- 存在 `ops/analysis/skill-0/`

这一阶段的目标不是 canonicalize，而是验证：

- atom extraction 是否稳定
- skill overlap 是否真的可观察
- 哪些 primitive 值得保留

### Phase B — Stable Sidecars

当格式开始稳定后，再引入：

- sidecar schemas
- naming rules
- source-skill linkage
- basic verification

这时仍可先不新增 resource type，但可以开始建立：

- `skill -> atoms`
- `atom -> source skills`

### Phase C — First-Class Primitives

若 analysis 已证明有价值，再讨论是否把下列其中一种纳入 `UniText`：

- `/registry/primitives`
- `/registry/operations`

这时才需要正式修改：

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Concrete First Deliverables

如果要让两个专案开始合作，第一批最值得做的不是大改架构，而是这四件事：

1. 定义一份 `skill-0` analysis output draft schema
2. 对 `UniText` 的 `Core 8` skills 中挑 1 到 2 个做 decomposition sample
3. 把输出放到 `ops/analysis/skill-0/`
4. 比较：
   - 不同 skills 之间的共享 atom
   - skill 文本描述与 atom 层的落差
   - 是否能反向重组出可用的最小 workflow

## 9. Strategic Interpretation

若合作成功，两个专案的长期分工会很清楚：

- `UniText` 成为 shared AI resources 的 canonical hub
- `skill-0` 成为 skill normalization 与 primitive extraction engine

从系统分层来看：

| Layer | Project |
|---|---|
| Canonical resource governance | `UniText` |
| Skill decomposition / normalization | `skill-0` |
| Future primitive vocabulary layer | `UniText × skill-0` shared outcome |

## 10. Final Position

目前最准确的结论是：

**`UniText` 与 `skill-0` 高度相关，但不是重复建设。**

它们一个偏向治理与分发，一个偏向拆解与抽象。

因此，短期最合理的合作不是直接把 `skill-0` 塞进 `UniText` 的既有四类资源，而是：

**让 `skill-0` 先把 `UniText` 当 canonical input corpus，并把分析结果先落在 `ops/analysis/skill-0/`。**

等输出格式、价值与验证方法稳定后，再决定是否将 primitive / operation 层正式升格为新的 canonical resource type。
