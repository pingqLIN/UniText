# UniText — Project Modes

> 狀態：Draft
> 目的：明確區分 `本機開發中的 authoring repo` 與 `提供給其他人採用的 starter/template`。

## 1. Why This Distinction Exists

`UniText` 同時扮演兩種可能完全不同的角色：

1. `Local Development Project`
   - 供作者本人持續開發、實驗、納管、修復與遷移
2. `Project Template`
   - 供其他人複製、初始化、再依自身環境調整的起始樣板

若不明確區分，最常見的問題是：

- 把本機路徑、備份資料、歷史狀態誤當成模板的一部分
- 把模板應保留抽象的邏輯契約，錯寫成某台機器的既有部署快照
- 把 authoring repo 的治理痕跡誤發佈給其他使用者

## 2. Mode Definitions

### 2.1 Local Development Project

這是作者本人正在使用的工作區。

特徵：

- 可以包含 inventories、backups、drift logs、history
- 可以包含過渡期 artifact、遷移腳本、實驗性 adapter
- 可以保留 platform-specific notes
- 可以反映「目前這台機器」的部署現況

目的：

- 持續開發 registry / spec / operations
- 執行 adoption、repair、sync
- 保存治理痕跡與回滾能力

### 2.2 Project Template

這是提供給其他人使用的起始樣板。

特徵：

- 只保留邏輯契約、最小文檔與可移植範例
- 不攜帶使用者本機絕對路徑
- 不攜帶私人 inventory、backup、history
- 不把某個既有部署的 state 當成模板預設值

目的：

- 讓他人快速建立自己的 UniText 實例
- 保留跨平台、跨環境可適配性
- 提供最小但完整的 doc set 與 starter structure

## 3. Inclusion Rules

### 3.1 Belongs In Local Development Project

- `ops/` 內的 inventories、baselines、history、backups
- 單一部署的 path maps
- 本機遷移腳本與 repair artifacts
- adoption 過程中的暫存與過渡資料
- 尚未正式納管的 inventory 候選

### 3.2 Belongs In Project Template

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- starter-level 的 registry layout 說明
- 範例 catalog entries
- 平台無關的 delivery / adoption 規則

### 3.3 Never Ship As Template Defaults

- 本機絕對路徑
- 個人使用痕跡
- 備份快照
- drift history
- 本機工作目錄下的暫存狀態
- 僅適用單一平台的部署值

## 4. Mapping To Current Repo

以目前這個 repo 來看：

- `VISION.md`、`INDEX.md`、`RESOURCE_SPEC.md`、`OPERATIONS.md`
  - 應被視為 template-safe core docs
- `registry/`
  - 是 canonical shared content 的正式位置
- `local/docs/PATH_MAP.md`
  - 是 local/reference deployment note，不是模板規格真相
- `local/docs/MCP_DEPLOYMENT_NOTES.md`
  - 是 local MCP deployment note
- `local/docs/WORKFLOW_DEPLOYMENT_NOTES.md`
  - 是 local workflow deployment note
- `local/scripts/sync-skills.ps1`
  - 是 local execution script，不是模板規格真相
- `ops/`
  - 是 local development state，不應直接視為模板內容
- `skills.bak.*`
  - 是 adoption inventory / backup，不是模板預設 registry
- `registry/mcp/claude-project-mcp-seed/definition.json`
  - 是 reference implementation artifact，可作為範例來源，但不應自動視為所有使用者的模板預設

## 5. Publishing Rule

當要把 `UniText` 作為「給其他人使用的專案樣板」發佈時，應執行以下過濾：

1. 保留 core docs 與 template-safe examples
2. 移除 local-only state artifacts
3. 移除本機 path / account / machine-specific values
4. 將 reference implementation 改寫為抽象 examples
5. 確認所有 default values 都不依賴單一作業系統

## 6. Operational Rule Of Thumb

可以問一個簡單問題：

> 這份內容是在描述「UniText 應該如何運作」，還是在描述「我這台機器目前怎麼配置」？

若答案偏向後者，它大多屬於 `Local Development Project`。  
若答案偏向前者，而且對其他人也成立，它才適合進入 `Project Template`。
