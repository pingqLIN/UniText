# Local Scripts

这里放的是 **本机操作脚本**。

- `*.ps1` 保留 Windows-first 参考实现
- `*.py` 提供跨平台 bootstrap / verify / backup 路径

## Current Scripts

- `bootstrap.py`
  - 跨平台初始化 skills delivery、Codex native-config、Copilot MCP config 与 project `.mcp.json`
- `verify-bootstrap.py`
  - 跨平台检查 first-run 结果是否与当前 repo 对齐，并接受 template-safe `.mcp.json` seed 或已 bootstrapped 的本机 wiring
- `create-git-bundle.py`
  - 建立可携带的 `git bundle` 备份，降低只依赖本地工作树的单点风险
- `git-startup.ps1`
  - 为新 session 解析 canonical base branch、要求干净工作树、显式 fast-forward 更新，并建立新的 feature branch
- `sync-skills.ps1`
  - 将 `registry/skills/` 同步到本机 skills targets
- `scan-skills.ps1`
  - 扫描候选 skills 并输出 adoption 检查结果
- `verify-delivery.ps1`
  - 验证 source 与常见 skills targets 是否存在、是否为链接、是否可解析
- `health-check.ps1`
  - 对 registry 与 scripts 做最小健康检查
- `batch-adopt-skills.ps1`
  - 将候选 skills 批量迁入 `registry/skills/`
- `generate-index-entries.ps1`
  - 由 `registry/skills/` 生成 INDEX 所需的 catalog 区块
- `rollback-skills.ps1`
  - 从 `ops/history/adopt_*` 的 backup 恢复指定 skill
- `export-review-package.ps1`
  - 将外部审查所需的 cover note、highlights、核心文件、精选 registry entries 与最小 scripts 导出到 `ops/review-package/`
- `export-template-package.ps1`
  - 将 template-safe docs、generic examples 与 starter layout 导出到 `ops/template-package/`
- `verify-template-package.ps1`
  - 验证导出的 template package 是否包含必要 starter 结构，且不含 review-only / local-only 内容
- `verify-workspace-boundaries.ps1`
  - 验证当前 authoring repo 的 tracked shared surfaces 是否混入 live workspace metadata、authoring-only docs 或 operations state
- `get-publishability-report.ps1`
  - 汇总当前 branch 的 local-only / ops / shared-surface 变更与 boundary verify 结果，作为 push suitability 的本地报告
- `lib/workspace-sensitive-metadata.ps1`
  - 载入 shared `WORKSPACE_SENSITIVE_METADATA_RULES.json`，让 boundary / template / publishability 验证共用同一套规则
- `validate-workspace-sensitive-metadata-rules.ps1`
  - 验证 shared `WORKSPACE_SENSITIVE_METADATA_RULES.json` 的结构、regex 可编译性与自带案例是否通过
- `preview-renormalize.ps1`
  - 只做 dry-run，预览 `git add --renormalize .` 会碰到多少 tracked files，让 line-ending cleanup 可以先看 blast radius 再决定是否执行
- `run-renormalize.ps1`
  - 以 `repo / root / registry / i18n / local / template` 为 scope 执行受控的 renormalize；默认仍是 dry-run，只有明确加上 `-Apply` 才会 stage 变更，并带有 `MaxFiles` guard
- `audit-i18n-drift.py`
  - 读取 `i18n/manifest.json`，列出各 locale 哪些官方文件缺翻译、翻译落后，或尚未被 Git 历史追踪到；支持 `json / markdown`、依 `locale / source-doc` 缩小范围，以及直接输出成工作报表
- `export-rebuild-project.ps1`
  - 将当前 repo 重建成可重新命名、可重新初始化的 fresh-project baseline，输出到 `ops/rebuild-project/`
- `verify-rebuild-project.ps1`
  - 在 template package 验证之上，再确认 rebuild guide 与 fresh-project 入口存在

## Governance Note

- `sync-skills.ps1` 与 `batch-adopt-skills.ps1` 都应遵守：
  - dry-run first
  - backup before mutation
  - 产生可追溯 log

## Platform Note

- 新的 first-run 路径优先使用 `bootstrap.py` 与 `verify-bootstrap.py`。
- `sync-skills.ps1` 仍保留作 Windows PowerShell 参考实现与治理样板。
