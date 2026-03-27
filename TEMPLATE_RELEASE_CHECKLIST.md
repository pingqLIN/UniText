# UniText — Template Release Checklist

> 用途：在輸出或發布 template package 前，快速檢查是否已完成最小 cleanup。

## 1. Docs

- [ ] `README.md` 沒有依賴作者個人背景才能理解
- [ ] `INDEX.md` 可作為 discovery 入口
- [ ] `PROJECT_MODES.md` 清楚區分 template 與 authoring workspace
- [ ] `SECRET_HANDLING_GUIDELINES.md` 已定義 secret 邊界且不含真實 credential
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` 已更新
- [ ] `SKILLS_PUBLIC_RELEASE_POLICY.md` 已定義公開版 skills 邊界
- [ ] `MILESTONES.md` 已反映目前 phase 狀態

## 2. Cleanup Boundaries

- [ ] template package 不包含 `backup/`
- [ ] template package 不包含 `recovered_*`
- [ ] template package 不包含 `.bak_*`
- [ ] template package 不包含 `ops/history/`
- [ ] template package 不包含 review-only docs
- [ ] template package 不包含 machine-specific absolute paths
- [ ] template package 不包含 restricted-license skills
- [ ] template package 若引用 local-only validation skills，已附正式說明且未附原始檔案
- [ ] 若 template package 納入 shared skills，已附來源資料或 `SOURCE.yaml`
- [ ] tracked `.mcp.json` 為 relative-path seed，而非作者本機絕對路徑

## 3. Examples

- [ ] 至少 1 個 generic skill example
- [ ] 至少 1 個 generic agent example
- [ ] 至少 1 個 generic mcp example
- [ ] 至少 1 個 runnable project-local MCP baseline
- [ ] 至少 1 個 generic workflow example
- [ ] 至少 1 份 generic local overlay skeleton
- [ ] starter package 含跨平台 `bootstrap -> verify` 路徑
- [ ] starter package 含 `.claude/settings.json`
- [ ] starter package 含 `.mcp.json`
- [ ] starter package 對 `Claude / Codex / Gemini / Copilot` 的目標定位有明確說明

## 4. Validation

- [ ] `health-check.ps1` 可通過
- [ ] `export-template-package.ps1 -DryRun` 可列出 package 內容
- [ ] `export-template-package.ps1` 可成功產出 package
- [ ] `verify-template-package.ps1` 可通過
- [ ] `bootstrap.py --dry-run` 可在乾淨環境預覽初始化內容
- [ ] `verify-bootstrap.py` 可驗證 first-run wiring
- [ ] `.claude/settings.json` 指向 UniText MCP 工具而非錯誤服務
- [ ] 未宣稱 Copilot 已完成驗證，除非真的有 adapter 與實測證據
- [ ] package 內含 `manifest.json`
- [ ] package 內含 `release.json`

## 5. Release Call

若以上項目都完成，可視為：

**適合視為 template release candidate**

若仍有 local-only 邊界不清、examples 不完整、或 CLI 驗證不足，則仍應視為：

**template release cleanup baseline**
