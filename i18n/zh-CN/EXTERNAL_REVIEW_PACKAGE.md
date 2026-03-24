# UniText — External Review Package

> 状态：Active Baseline  
> 用途：定义外部审查要看什么、不要看什么，以及如何重复产出 review package。

## 1. Purpose

`UniText` 已经进入可供外部审查的 baseline 阶段，但审查重点应集中在：

- 核心架构是否合理
- canonical registry 是否已落地
- operations safety model 是否可执行
- 精选 shared resources 是否足以代表专案方向

本文件的目的，是把这些内容收敛成一个可重复整理的审查包，而不是把整个作者工作区原封不动交出去。

## 2. Recommended Reading Order

建议外部审查者依以下顺序阅读：

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`

若要看实际资源样本，再往下看：

- `registry/skills/` 的 `8 + 4` 精选主集
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- `local/scripts/` 中的最小治理脚本与 cross-platform first-run 脚本

## 3. Review Scope

目前 review package 应包含以下内容：

- 核心文件
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `PROJECT_MODES.md`
  - `MILESTONES.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- 最小治理文件
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- 最小治理脚本
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
- 精选 shared resources
  - `registry/skills/` 的 `8 + 4` 主集
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Out Of Scope

以下内容不应作为外部审查主体：

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- 本机特定 path mapping 与个人环境残留
- 未纳入 shortlist 的候选 skills
- 未追踪或实验中的内容

authoring notes and review archives 属于作者工作参考资料，不是 canonical review source。

## 5. Export Command

在 repo root 执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

预设输出到：

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

若只想先检查内容，不写入档案：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validation

建议在 export 前至少先跑一次：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

若要确认 canonical skills delivery 对齐：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Current Interpretation

截至 2026-03-24，`UniText` 已具备：

- reviewer-facing cover note 与 highlights summary
- 外部审查可读的核心文件
- `8 + 4` 精选 skills 主集
- agent / workflow seed 与可实跑的 MCP baseline
- 可重复产出 review package 的整理流程
- cross-platform `bootstrap -> verify`
- 可携 `git bundle` 备份流程

因此目前最适合的定位是：

**external-review-ready baseline**

而不是：

**fully generalized release template**

