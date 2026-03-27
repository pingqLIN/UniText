# UniText — Template Release Package

> 状态：Active Baseline  
> 用途：定义 template release cleanup 的目标、范围与可重复汇出流程。

> **同步注记（2026-03-27）：** 本译本仅反映 current-baseline 的一部分。英文 `TEMPLATE_RELEASE_PACKAGE.md` 仍是 authoritative version。与 release boundary、排除项、skills 规则相关的高风险段落已同步，其余内容可能仍保留旧版解读。

## 1. Purpose

`UniText` 的 template release 不应该是把作者工作区原样打包出去，而应该是输出一份：

- 保留核心架构与规格
- 保留最小可用范例
- 排除 local-only state
- 排除历史治理残留
- 适合其他使用者 fork / clone 后自行扩充

这份 package 的定位是：

**starter template**

而不是：

**authoring workspace snapshot**

## 2. Include

目前 template package 应包含：

- 核心文件
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- template-safe root config
  - `.gitignore`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- starter local overlay skeleton
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
- release metadata
  - `manifest.json`
  - `release.json`

## 3. Exclude

template package 不应包含：

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- 实际使用者帐号、家目录、绝对路径
- review-specific docs
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Export Command

在 repo root 执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

预设输出到：

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

若只想先检查内容，不写入档案：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

若要验证输出的 package：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

汇出后，新使用者的 first-run 建议路径：

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Export Interpretation

汇出的 template package 代表：

- UniText 的核心契约
- 一份干净的 starter layout
- 一组最小 generic examples

它不代表：

- 作者目前的完整工作状态
- 所有已纳管 skills
- 所有 review / audit 证据
- 已完成的本机 delivery wiring

## 6. Current Interpretation

截至 2026-03-27，`UniText` 已具备：

- 外部审查 package
- reviewer-facing entry docs
- template release cleanup baseline
- 可重复产出 template package 的 export script
- starter local overlay skeleton
- template package verification script
- release metadata
- cross-platform first-run scripts
- portable bundle backup flow

因此目前最适合的判读是：

**template release candidate**

而不是：

**authoring workspace snapshot**

