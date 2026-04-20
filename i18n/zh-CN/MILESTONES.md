# UniText — Milestones

> 状态：Active
> 目的：定义对外审查与内部执行都可共用的量化完成条件。

## Phase 1 — Skills Registry Online

- `registry/skills/` 已建立
- 至少 5 个 skills 完成 canonical adoption
- `INDEX.md` 有对应 catalog entries
- `local/scripts/sync-skills.ps1` 指向 `registry/skills`
- `local/scripts/verify-delivery.ps1` 可验证 skills source 与 target 状态
- `local/scripts/health-check.ps1` 可通过基本检查

## Phase 2 — Full Registry Baseline

- `registry/agents/` 已建立
- `registry/mcp/` 至少 1 个非空示例维持可读
- `registry/workflow/` 至少 1 个 catalog entry 被正式列出
- `scan` / `verify` / `sync` 三类操作都有最小工具支撑
- `CLI_COMPAT_MATRIX.md` 记录目前依赖的 CLI 行为与最后验证日期

## Phase 3 — External Review Ready

- Git repository 已初始化
- `.gitignore` 已排除 local-only 与大型历史产物
- `README.md`、`INDEX.md`、`docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md` 三者状态一致
- `docs/reviews/EXTERNAL_REVIEW_PACKAGE.md` 已定义审查范围、阅读顺序与排除项目
- `docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md` 与 `docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md` 已可作为 reviewer-facing entry docs
- `SECRET_HANDLING_GUIDELINES.md` 已建立治理边界，并纳入核心阅读顺序
- `local/scripts/export-review-package.ps1` 可重复产出 review package
- 已提供跨平台 `bootstrap -> verify` first-run 路径
- 外部审查可直接看到：
  - 核心架构文件
  - 已 adoption 的 canonical skills
  - 最小 operations scripts
  - 清楚的下一阶段里程碑

## Phase 4 — Template Release Ready

- local-only artifacts 不进入发布包
- template export 流程已文件化
- `TEMPLATE_RELEASE_PACKAGE.md` 与 `TEMPLATE_RELEASE_CHECKLIST.md` 已存在
- `local/scripts/export-template-package.ps1` 可重复产出 starter package
- `local/scripts/verify-template-package.ps1` 可验证 starter package 结构
- `SECRET_HANDLING_GUIDELINES.md` 已纳入 starter package
- `local/scripts/create-git-bundle.py` 可产出可携 backup artifact
- 已有 template-safe generic examples 可覆盖 `skills`、`mcp`、`agents`、`workflow`
- 已有 template-safe `local/` skeleton
- `mcp` 至少有一个真正可执行的 baseline
- canonical resource coverage 持续扩张到 `skills`、`mcp`、`agents`、`workflow`
- 至少 2 个 CLI 实际通过 delivery 验证
