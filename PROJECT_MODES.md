# UniText — Project Modes

> 狀態：Template Base
> 目的：區分 authoring repo 與對外提供的 starter/template。

## 1. Two Modes

### Local Development Project

用於作者本人持續開發、納管、修復與治理。

可包含：

- inventories
- backups
- drift logs
- migration artifacts
- platform-specific notes

### Project Template

用於提供其他人初始化自己的 `UniText` 實例。

應包含：

- 邏輯契約
- 核心文檔
- 最小範例
- 平台無關規則

不應包含：

- 本機絕對路徑
- 個人使用痕跡
- 備份快照
- drift history
- 單一部署預設值

## 2. Rule Of Thumb

如果某份內容是在描述：

- `UniText 應該如何運作`
  - 它更適合進入 `Project Template`
- `某個作者工作區目前怎麼配置`
  - 它更適合留在 `Local Development Project`

## 3. Publishing Rule

當要發佈模板時：

1. 保留核心文檔與 template-safe examples
2. 移除 local-only state artifacts
3. 移除本機 path / account / machine-specific values
4. 將 reference implementation 改寫為抽象 examples
