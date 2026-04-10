[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](../zh-TW/DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](DOCUMENT_PLACEMENT_POLICY.md) | [日本語](../ja/DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](../de/DOCUMENT_PLACEMENT_POLICY.md) | [Français](../fr/DOCUMENT_PLACEMENT_POLICY.md) | [Español](../es/DOCUMENT_PLACEMENT_POLICY.md) | [한국어](../ko/DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](../it/DOCUMENT_PLACEMENT_POLICY.md)

# UniText — 文档放置政策

> 状态：Active Baseline
> 用途：定义治理、reference、authoring、operations 类文档应该放在哪一层，避免 shared 与 live workspace 内容错层。

## 1. Purpose

UniText 同时是：

- authoring workspace
- shared registry baseline
- template / rebuild export source

因此，如果只看文档“主题是否相关”，很容易把它放错层。

这份规则回答的是：

- 哪一类文档应该放 `registry/`
- 哪一类文档应该放 `local/`
- 哪一类文档应该放 `ops/`
- 哪些文档可以 tracked
- 哪些文档只能留在 ignored local authoring 空间

## 2. Core Rule

判断文档放置位置时，优先看内容性质，而不是主题领域。

- 如果文档描述的是 shared canonical truth，就放 shared layer
- 如果文档描述的是单一作者工作区的当前状态，就放 local layer
- 如果文档描述的是操作历史、输出结果、audit evidence 或 generated state，就放 operations layer

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| 架构原则、治理规则、template-safe spec | root docs 或 `registry/` | Yes | Yes | 必须避免 live workspace values |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | 可以描述字段结构，但值必须 redacted 或 placeholder 化 |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | 不可绑定单一作者机器 |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | 可记录 location / state，但不可记录 plaintext secret |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | 必须 ignore |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | 必须 ignore |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | 必须 ignore |
| generated audit trail / export output / drift report | `ops/` | No | No | 属于 state，不是 canonical source |

## 4. Naming Rules

如果某个主题同时需要 shared 版与 live 版，默认使用成对命名：

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - 或 `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

如果 shared sanitized doc 与 live workspace doc 同时存在，应遵守：

1. shared 版只保留 template-safe 结构与 redacted placeholder
2. live 版只留在 `local/docs/` 或 `local/docs/authoring/`
3. shared 版应明确指出 live 版位置
4. live 版也应指出它对应的 shared sanitized reference

## 6. Publishing Rule

下列说法不能混为一谈：

- template export passes
- rebuild export passes
- branch is publish-safe

template / rebuild 导出安全，只代表导出产物的边界较干净，不代表 authoring repo 里当前所有 tracked content 都适合 push。

## 7. Quick Decisions

如果你不确定一份文档该放哪里，先问这三题：

1. 这份文档是不是在描述单一作者工作区当前是什么样
   - 是：优先放 `local/docs/`
2. 这份文档是不是一个操作结果、audit 产物、导出包，或 drift report
   - 是：优先放 `ops/`
3. 这份文档是不是希望未来 template / rebuild / shared registry 都能安全引用
   - 是：优先放 root docs、`registry/`，或 shared workflow layer

## 8. Common Misplacements

- 把 live Cloudflare baseline 放到 `registry/.../references/`
- 把 strategy / review plan 放到 root
- 把 export output 或 audit evidence 当成 canonical reference
- 把 machine-specific path 直接写进 shared governance docs

## 9. Review Gate

在新增任何 governance / reference 类文档前，至少先确认：

- 它是不是在描述 shared truth，而不是 live workspace state
- 它如果被 push，是否仍符合 `NO_PUBLISH_POLICY.md` 与 template-safe 预期
- 它是否需要一个 sanitized/live pair，而不是单档同时承载两者

## 10. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
