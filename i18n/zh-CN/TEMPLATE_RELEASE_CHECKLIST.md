# UniText — Template Release Checklist

> 用途：在输出或发布 template package 前，快速检查是否已完成最小 cleanup。

## 1. Docs

- [ ] `README.md` 没有依赖作者个人背景才能理解
- [ ] `INDEX.md` 可作为 discovery 入口
- [ ] `PROJECT_MODES.md` 清楚区分 template 与 authoring workspace
- [ ] `SECRET_HANDLING_GUIDELINES.md` 已定义 secret 边界且不含真实 credential
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` 已更新
- [ ] `MILESTONES.md` 已反映目前 phase 状态

## 2. Cleanup Boundaries

- [ ] template package 不包含 `backup/`
- [ ] template package 不包含 `recovered_*`
- [ ] template package 不包含 `.bak_*`
- [ ] template package 不包含 `ops/history/`
- [ ] template package 不包含 review-only docs
- [ ] template package 不包含 machine-specific absolute paths

## 3. Examples

- [ ] 至少 1 个 generic skill example
- [ ] 至少 1 个 generic agent example
- [ ] 至少 1 个 generic mcp example
- [ ] 至少 1 个 generic workflow example
- [ ] 至少 1 份 generic local overlay skeleton
- [ ] starter package 含跨平台 `bootstrap -> verify` 路径

## 4. Validation

- [ ] `health-check.ps1` 可通过
- [ ] `export-template-package.ps1 -DryRun` 可列出 package 内容
- [ ] `export-template-package.ps1` 可成功产出 package
- [ ] `verify-template-package.ps1` 可通过
- [ ] `bootstrap.py --dry-run` 可在干净环境预览初始化内容
- [ ] `verify-bootstrap.py` 可验证 first-run wiring
- [ ] package 内含 `manifest.json`
- [ ] package 内含 `release.json`

## 5. Release Call

若以上项目都完成，可视为：

**适合视为 template release candidate**

若仍有 local-only 边界不清、examples 不完整、或 CLI 验证不足，则仍应视为：

**template release cleanup baseline**
