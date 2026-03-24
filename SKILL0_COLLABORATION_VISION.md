# UniText × skill-0 — Collaboration Vision

> 狀態：Concept Draft
> 目的：定義 `UniText` 與 `skill-0` 的關係、合作空間、可能途徑，以及目前缺少的機制。

## 1. Executive Summary

`UniText` 與 `skill-0` 不是互斥或重複的專案，而是可以形成上下游關係的兩個層次：

- `UniText` 負責 shared resources 的 **registry / delivery / governance**
- `skill-0` 負責把高階 skill 吸納、拆解、正規化成更通用的 **atomic operation set**

因此，兩者最合理的合作方式不是「誰取代誰」，而是：

**UniText 提供 canonical inputs 與可治理的承載面，skill-0 提供 decomposition / normalization / recomposition 能力。**

## 2. Each Project Solves a Different Problem

### UniText

`UniText` 解的是：

- shared resource 如何被 canonical 化
- 如何在多個 AI CLI 之間 delivery
- 如何用 `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY` 管理變更

也就是：

**distribution / governance problem**

### skill-0

`skill-0` 解的是：

- 一個高階 skill 實際由哪些最小操作單元構成
- 哪些步驟是可重用的 primitive
- 哪些描述只是 surface wording，哪些才是核心操作
- 高階 skill 是否可以重新組裝成更小、更通用、更可移植的能力集合

也就是：

**abstraction / compiler / normalization problem**

## 3. Relationship Between the Two

如果站在 `skill-0` 的目標來看，`UniText` 最有價值的角色不是「被分發的結果」，而是：

- 一個穩定的 high-level skill source
- 一個有邏輯身份與 metadata 的 canonical corpus
- 一個可被持續分析、比較、追蹤的技能資料集

從這個角度看，兩者的關係可描述為：

| Project | Primary role |
|---|---|
| `UniText` | canonical source of truth for shared resources |
| `skill-0` | analyzer / decomposer / compiler over high-level skills |

一句話說：

**UniText 保存 skill，skill-0 解構 skill。**

## 4. Current Collaboration Space

目前即使不改動 `UniText` 的核心 schema，兩個專案也已經有合作空間：

### 4.1 Use UniText as input corpus

`skill-0` 可以直接以這些內容作為輸入：

- `registry/skills/*/SKILL.md`
- `INDEX.md` 裡的 catalog metadata
- `RESOURCE_SPEC.md` 提供的 identity / canonical location 契約

這讓 `skill-0` 分析的不是一堆散落副本，而是一組較乾淨的 canonical skill corpus。

### 4.2 Use UniText as a governed staging ground

`skill-0` 的分析輸出目前可以先不進入 canonical registry，而先放在：

- `/operations`
- 例如 `ops/analysis/skill-0/`

這樣做的好處是：

- 不會過早污染目前的 shared resource schema
- 可以先觀察分析格式是否穩定
- 可以把 `skill-0` 視為 analysis pipeline，而不是立刻升格成 canonical source

### 4.3 Use UniText review flow to evaluate derived outputs

當 `skill-0` 產出：

- atom maps
- normalized step sets
- shared subroutine clusters
- recomposition candidates

這些輸出可以先比照 `UniText` 的 review mindset 被檢查：

- identity 是否穩定
- 命名是否清楚
- 與原 skill 的對映是否可追蹤
- 是否需要人工決定 canonical form

## 5. Most Likely Collaboration Modes

### Mode A — skill-0 as external analyzer

`skill-0` 把 `UniText` 當資料來源，輸出 analysis reports，但不反寫 registry。

適合用途：

- 快速驗證 decomposition 方法
- 做 skill overlap analysis
- 找 reusable primitives

優點：

- 導入成本最低
- 幾乎不需要動 `UniText` schema

缺點：

- 結果停留在 sidecar artifacts
- 不容易成為 shared canonical resource

### Mode B — skill-0 as sidecar generator

`skill-0` 讀取 `registry/skills`，並在相鄰位置生成 machine-readable sidecar，例如：

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

優點：

- 可以建立 skill 與 atom 的明確對映
- 比純 report 更容易做 tooling

缺點：

- 會開始碰到 `UniText` schema 邊界問題
- 需要定義哪些 sidecar 屬於 canonical，哪些只是 generated

### Mode C — primitives become a first-class resource type

若合作成熟，`UniText` 可以新增正式資源類型，例如：

- `/registry/primitives`
- 或 `/registry/operations`

這會讓 `skill-0` 的輸出不再只是分析附屬物，而是變成可被 registry 正式納管的 shared resources。

優點：

- 形成真正的共同語彙層
- 有機會支撐跨 skill recomposition

缺點：

- 需要修改 `UniText` 的 resource model
- 需要新的 metadata spec、adoption flow 與 verification rules

## 6. What Is Missing Today

目前兩者還不能自然深度整合，主要缺的是以下幾類機制。

### 6.1 Missing canonical type for primitives

`UniText` 目前的一級 resource type 只有：

- `skills`
- `mcp`
- `agents`
- `workflow`

尚未有：

- `primitives`
- `operations`
- `atoms`

因此 `skill-0` 真正最關心的產物，在 `UniText` 裡還沒有第一級承載面。

### 6.2 Missing metadata spec for atomic units

目前 `RESOURCE_SPEC.md` 適合描述高階 shared resources，但還沒有定義：

- atom id
- operation signature
- preconditions / postconditions
- composition rules
- provenance back to source skill

### 6.3 Missing adoption flow for derived artifacts

`UniText` 目前有 skills adoption flow，但還沒有一套專門處理下列情況的流程：

- 同一 skill 被分解出不同 atom sets
- 多個 skill 對應到相似但不完全相同的 primitive
- 某個 atom 是否足夠穩定到值得 canonicalize

### 6.4 Missing verification model

如果要讓 `skill-0` 的輸出進入更正式的合作階段，至少需要回答：

- decomposition 是否穩定
- 是否可 round-trip recomposition
- 是否真的提升跨 skill reuse
- 是否只是重新命名原本的描述

### 6.5 Missing boundary between analysis and canon

目前還缺一條清楚規則：

- 哪些 `skill-0` 產物只是 analysis
- 哪些產物已經可以視為 canonical shared resource

這個邊界不清楚時，最安全的作法仍是先放在 `ops/analysis/skill-0/`。

## 7. Recommended Near-Term Direction

短期最合理的方向不是立刻修改 `UniText` 的 core schema，而是採取：

**Mode A -> Mode B 的漸進式合作**

### Phase A — Analysis Only

先做：

- 以 `registry/skills/*/SKILL.md` 作為輸入
- 產出 decomposition reports
- 存在 `ops/analysis/skill-0/`

這一階段的目標不是 canonicalize，而是驗證：

- atom extraction 是否穩定
- skill overlap 是否真的可觀察
- 哪些 primitive 值得保留

### Phase B — Stable Sidecars

當格式開始穩定後，再引入：

- sidecar schemas
- naming rules
- source-skill linkage
- basic verification

這時仍可先不新增 resource type，但可以開始建立：

- `skill -> atoms`
- `atom -> source skills`

### Phase C — First-Class Primitives

若 analysis 已證明有價值，再討論是否把下列其中一種納入 `UniText`：

- `/registry/primitives`
- `/registry/operations`

這時才需要正式修改：

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Concrete First Deliverables

如果要讓兩個專案開始合作，第一批最值得做的不是大改架構，而是這四件事：

1. 定義一份 `skill-0` analysis output draft schema
2. 對 `UniText` 的 `Core 8` skills 中挑 1 到 2 個做 decomposition sample
3. 把輸出放到 `ops/analysis/skill-0/`
4. 比較：
   - 不同 skills 之間的共享 atom
   - skill 文本描述與 atom 層的落差
   - 是否能反向重組出可用的最小 workflow

## 9. Strategic Interpretation

若合作成功，兩個專案的長期分工會很清楚：

- `UniText` 成為 shared AI resources 的 canonical hub
- `skill-0` 成為 skill normalization 與 primitive extraction engine

從系統分層來看：

| Layer | Project |
|---|---|
| Canonical resource governance | `UniText` |
| Skill decomposition / normalization | `skill-0` |
| Future primitive vocabulary layer | `UniText × skill-0` shared outcome |

## 10. Final Position

目前最準確的結論是：

**`UniText` 與 `skill-0` 高度相關，但不是重複建設。**

它們一個偏向治理與分發，一個偏向拆解與抽象。

因此，短期最合理的合作不是直接把 `skill-0` 塞進 `UniText` 的既有四類資源，而是：

**讓 `skill-0` 先把 `UniText` 當 canonical input corpus，並把分析結果先落在 `ops/analysis/skill-0/`。**

等輸出格式、價值與驗證方法穩定後，再決定是否將 primitive / operation 層正式升格為新的 canonical resource type。
