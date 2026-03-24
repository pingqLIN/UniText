# UniText — Secret Handling Guidelines

> 狀態：Active
> 用途：定義 password、API key、token、credential 與其他敏感資料的處理邊界。

## 1. Core Principle

任何 secret 都不應出現在會被當成模板、樣板、review package 或對外分享內容的一般性文件中。

## 2. What Counts as Secret

以下內容一律視為 secret 或敏感 material：

- password
- API key
- token
- session cookie
- private key
- bearer token
- 任何可直接用來驗證身分或授權存取的值

## 3. Storage Rules

- 真實 secret 應只保留在使用者本機或受控密鑰系統中
- 文件中若需要示意，只能使用 placeholder
- placeholder 應明確標示為 mock / example / redacted
- 不得在 repository 中留下可直接使用的真實 credential

## 4. Documentation Rules

說明文件可以描述：

- secret 應存放在哪類位置
- 哪些工具負責讀取 secret
- 如何在 local 環境中載入 secret
- 如何進行 redaction 與輪替

說明文件不應包含：

- 真實值
- 可直接重放的 token
- 個人帳號密碼
- 對外可用的 API key

## 5. Template Boundary

若 `UniText` 輸出 starter template，則：

- `SECRET_HANDLING_GUIDELINES.md` 可以保留
- 所有真實 secret 必須移除
- 範例必須使用 placeholder
- 所有 path 與 account 資訊必須去識別化

## 6. Review Boundary

若內容被納入 external review package：

- 只能展示治理邏輯與邊界
- 不可包含實際 secret 值
- 不可因為「只是 review」就保留敏感資料

## 7. Operational Checklist

在提交、push、export 或分享前，請先確認：

1. 是否含有真實 credential
2. 是否有 placeholder 未標明
3. 是否有機密片段殘留在 log、snapshot 或 example
4. 是否需要 redaction
5. 是否需要從 package 中排除該檔案
