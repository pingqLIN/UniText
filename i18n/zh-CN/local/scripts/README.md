# Local Scripts

这里放的是 **本机操作脚本**。

- `*.ps1` 保留 Windows-first 参考实作
- `*.py` 提供跨平台 bootstrap / verify / backup 路径

## Current Scripts

- `bootstrap.py`
  - 跨平台初始化 skills delivery、Codex native-config 与 project `.mcp.json`
- `verify-bootstrap.py`
  - 跨平台检查 first-run 结果是否与目前 repo 对齐
- `create-git-bundle.py`
  - 建立可携的 `git bundle` 备份，降低仅靠本地工作树的单点风险
- `sync-skills.ps1`
  - 将 `registry/skills/` 同步到本机 skills targets
- `scan-skills.ps1`
  - 扫描候选 skills 并输出 adoption 检查结果
- `verify-delivery.ps1`
  - 验证 source 与常见 skills targets 是否存在、是否为连结、是否可解析
- `health-check.ps1`
  - 对 registry 与 scripts 做最小健康检查
- `batch-adopt-skills.ps1`
  - 将候选 skills 批次迁入 `registry/skills/`
- `generate-index-entries.ps1`
  - 由 `registry/skills/` 生成 INDEX 所需的 catalog 区块
- `rollback-skills.ps1`
  - 从 `ops/history/adopt_*` 的 backup 回复指定 skill
- `export-review-package.ps1`
  - 将外部审查所需的 cover note、highlights、核心文件、精选 registry entries 与最小 scripts 汇出到 `ops/review-package/`
- `export-template-package.ps1`
  - 将 template-safe docs、generic examples 与 starter layout 汇出到 `ops/template-package/`
- `verify-template-package.ps1`
  - 验证输出的 template package 是否包含必要 starter 结构，且不含 review-only / local-only 内容

## Governance Note

- `sync-skills.ps1` 与 `batch-adopt-skills.ps1` 都应遵守：
  - dry-run first
  - backup before mutation
  - 产生可追溯 log

## Platform Note

- 新的 first-run 路径优先使用 `bootstrap.py` 与 `verify-bootstrap.py`。
- `sync-skills.ps1` 仍保留作 Windows PowerShell 参考实作与治理样板。
