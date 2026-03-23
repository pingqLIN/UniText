# UniText — Template Release Checklist

> 用途：在輸出或發布 template package 前，快速檢查是否已完成最小 cleanup。

## 1. Docs

- [ ] `README.md` 沒有依賴作者個人背景才能理解
- [ ] `INDEX.md` 可作為 discovery 入口
- [ ] `PROJECT_MODES.md` 清楚區分 template 與 authoring workspace
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` 已更新
- [ ] `MILESTONES.md` 已反映目前 phase 狀態

## 2. Cleanup Boundaries

- [ ] template package 不包含 `backup/`
- [ ] template package 不包含 `recovered_*`
- [ ] template package 不包含 `.bak_*`
- [ ] template package 不包含 `ops/history/`
- [ ] template package 不包含 review-only docs
- [ ] template package 不包含 machine-specific absolute paths

## 3. Examples

- [ ] 至少 1 個 generic skill example
- [ ] 至少 1 個 generic agent example
- [ ] 至少 1 個 generic mcp example
- [ ] 至少 1 個 generic workflow example

## 4. Validation

- [ ] `health-check.ps1` 可通過
- [ ] `export-template-package.ps1 -DryRun` 可列出 package 內容
- [ ] `export-template-package.ps1` 可成功產出 package
- [ ] package 內含 `manifest.json`

## 5. Release Call

若以上項目都完成，可視為：

**適合進入 template release 候選階段**

若仍有 local-only 邊界不清、examples 不完整、或 CLI 驗證不足，則仍應視為：

**template release cleanup baseline**
