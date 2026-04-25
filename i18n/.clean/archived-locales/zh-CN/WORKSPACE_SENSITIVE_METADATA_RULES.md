[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](../zh-TW/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [简体中文](WORKSPACE_SENSITIVE_METADATA_RULES.md) | [日本語](../ja/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Deutsch](../de/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Français](../fr/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Español](../es/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [한국어](../ko/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Italiano](../it/WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> 状态：Active Baseline
> 用途：定义 shared surfaces 上的 workspace-sensitive metadata 检测规则、维护方式与验证边界。

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` 是 authoring repo 与 exported starter package 共用的规则来源，用来降低以下 drift：

- shared docs 混入本机绝对路径
- shared scripts 混入 live workspace hostname
- shared governance files 混入 live redirect URI 或 Cloudflare IDs
- boundary verify 与 template verify 使用不同规则集

这份文档回答的是：

- 规则文件各区块代表什么
- 什么时候应该新增规则
- 如何避免把 sanitized placeholder 也误判成 live metadata
- 调整规则后要跑哪些验证

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` 目前有四个顶层区块：

- `shared_surface_scope`
  - 定义 repo-side boundary verify 默认要扫描的 tracked shared surfaces
- `path_rules`
  - 定义哪些 tracked 路径本身不应出现在 shared surface
- `content_patterns`
  - 定义哪些文字内容属于 workspace-sensitive metadata
- `self_test_cases`
  - 定义规则自带的正反案例，避免 regex 修改后产生静默回归

## 3. Maintenance Rules

- 新增 shared governance doc 或 shared control script 时，如果它属于 repo-side boundary review 范围，应同步加入 `shared_surface_scope`
- 新增 live metadata 类型时，优先补 `content_patterns`，再补对应 `self_test_cases`
- 如果某个 placeholder 应视为安全范例，必须补一个 `expected_labels = []` 的 self-test case
- 如果某条 regex 只是在 script 内作为规则字串出现，应明确设置 `skip_script_pattern_lines`
- 不要把 authoring-only 或 operations-only 路径塞进 `shared_surface_scope` 来解决误报；应先检查文档放置是否错层

## 4. Required Validation

每次调整 `WORKSPACE_SENSITIVE_METADATA_RULES.json` 后，至少应重跑：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

如果这次变更会影响 starter baseline，还应再跑：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

这套规则的目标是：

- 在 shared surface 上提供稳定、可维护、可验证的 heuristic controls

它不是：

- 所有 secret 类型的完整 schema 验证器
- 面向所有 infrastructure provider 的通用 DLP 系统
- 对 local-only / ops-only 区域做全面内容扫描的工具

如果未来 metadata 类型持续扩大，下一步应该是扩充规则来源与案例，而不是把 live references 再放回 shared registry。
