# UniText — Secret Handling Guidelines

> 狀態：Draft
> 角色：定義密碼、API key、token、credential 等 sensitive material 在 UniText 中的存放邊界、操作原則與文件記錄方式。

## 1. Purpose

這份文件回答的是：

- 哪些資料算 secret
- secret 不應該放在哪裡
- 在 UniText 中應該如何記錄「位置」與「狀態」
- 何時可以放在 CLI config、何時必須改走 OS secret store 或 native helper

這份文件不提供單一產品的最終實作；它提供的是 UniText 應遵守的治理邊界。

## 2. Secret Definition

以下內容一律視為 `secret` 或 `sensitive material`：

- password
- passphrase
- API key
- access token
- refresh token
- session token
- private key
- OAuth client secret
- cookie / session credential
- 任何足以代表使用者或系統身分的 bearer credential

以下內容通常不算 secret，但仍可能是 sensitive metadata：

- endpoint URL
- model name
- provider name
- account email
- feature toggle state
- key exists / missing 狀態
- key 最後更新時間

以下內容雖然通常不是 secret，但在 template / rebuild / review export 中仍應預設視為 `workspace-sensitive metadata`：

- Cloudflare account ID、zone ID、tunnel ID、Access app ID
- 真實 redirect URI allowlists
- 真實 hostnames 與 internal service ports
- 本機 authoring repo 路徑
- 本機 runtime / staging / production 路徑
- 任何足以重建單一作者工作區拓樸的 machine-specific baseline

## 3. Core Principle

UniText 的基本原則是：

1. `registry/` 不存放 secret
2. `ops/` 不記錄可重放的 secret
3. `local/` 只允許記錄 path / adapter / deployment notes，不允許明文 secret
4. 真正的 secret 應優先放在 OS-level secret store
5. 若短期無法使用 OS secret store，至少要把 secret 與一般設定分離

簡單說：

- `registry` 是 shared truth，不是 secret vault
- `ops` 是 audit trail，不是 credential archive
- `local` 是 wiring overlay，不是 plaintext stash

## 4. Storage Policy by Layer

| Layer | Can store secret? | Guidance |
|---|---|---|
| `registry/` | No | 只能存 canonical definition、schema、adapter hints、resource metadata |
| `ops/` | No | 只能存 redacted logs、backup metadata、drift report、inventory state |
| `local/` docs | No | 可記錄 secret location 類型，但不可記錄 secret 本身 |
| CLI config | Conditional | 只有在該 CLI 原生只支援 config-based secret 且風險可接受時才可使用 |
| OS secret store | Yes | 首選；例如 Windows DPAPI / Credential Manager、macOS Keychain、Linux Secret Service |
| in-memory session | Yes | 可接受作為短期解密後的 runtime material，但不應作為唯一持久化來源 |

## 5. Approved Patterns

### 5.1 Best Pattern

適用於商業擴充、桌面工具、跨 CLI adapter：

- 非敏感設定存在一般 config / storage
- secret 存在 OS secret store
- runtime 啟動時再注入到 process memory
- UI 只顯示 `stored / missing / last updated`，不回填明文

### 5.2 Acceptable Fallback

若暫時沒有 OS secret store integration：

- 每個 provider / account 分開存 secret
- secret 與一般設定分離
- content script / renderer / untrusted context 不可直接讀取
- audit 與 export 僅顯示 redacted state
- 需在文件中標記為 `interim storage model`

### 5.3 Not Acceptable

以下做法不應被 UniText 視為合格：

- 把 API key 寫進 `registry/`
- 把 token 寫進 `ops/history/`
- 在 deployment note 貼完整 key 範例
- 將 secret 與一般設定混存，且無 redaction
- 匯出 review package/template package 時把真實 key 一起打包

## 6. Location Recording Rules

文件可以記錄「secret 在哪一層」，但不能記錄 secret 值本身。

允許記錄的例子：

- `Windows Credential Manager`
- `DPAPI-protected local secret file`
- `%USERPROFILE%\\.codex\\config.toml` 中的 non-secret settings
- `chrome.storage.local` only for non-secret provider settings
- `chrome.storage.session` used for short-lived runtime material

不允許記錄的例子：

- 完整 token
- 完整 API key
- 完整 Authorization header
- 可直接重放的 cookie 值

## 7. Environment Baseline Boundary

除了 secret value 本身，UniText 也不應把 authoring workspace 的本地環境習慣帶進 shared baseline。

這裡的 `local-only environment habit` 包含：

- `localhost`、`127.0.0.1`、或只對單一作者機器成立的 callback URL
- 本機絕對路徑、作者帳號名稱、或 machine-specific working directory
- 只為本地開發方便而存在的 debug flag、feature override、stub endpoint
- staging / production 不應承接的測試帳號、測試 provider、或臨時 fallback 值

治理原則：

1. tracked shared docs 只能描述 env schema、layering、placeholder、或 sanitized example
2. `registry/`、root shared docs、template package 不應包含 local-only override 值
3. authoring 機器專用 env baseline 應留在 ignored local layer，而不是 shared layer
4. release/export 流程應優先從 template-safe source 產出 env baseline，不應從作者本機 `.env` 或等價檔案複製
5. 若某文件同時需要 shared guidance 與 live local baseline，應拆成 sanitized/shared 與 local/live pair

允許出現在 shared surface 的例子：

- `API_BASE_URL=https://api.example.com`
- `OPENAI_API_KEY=sk-example-redacted`
- `Set this value through CI or your platform secret manager`

不應出現在 shared surface 的例子：

- `API_BASE_URL=http://localhost:3000`
- `CALLBACK_URL=http://127.0.0.1:8787/callback`
- `MODEL_CACHE_DIR=C:\\Users\\miles\\...`
- `DEBUG_BYPASS_AUTH=true`

## 8. Documentation Rules

當文件需要提到 secret handling 時，應遵守：

1. 只記錄 storage class，不記錄實際值
2. 只記錄 redacted examples
3. 若範例不可避免，使用明確假值，例如：

```text
OPENAI_API_KEY=sk-example-redacted
Authorization: Bearer token-example-redacted
```

4. 若某系統目前只能用較弱模式，文件必須標明：
   - 這是暫時方案
   - 已知風險是什麼
   - 目標升級路線是什麼

## 9. Audit and Export Rules

任何 review package、template package、inventory export、ops snapshot 都必須：

- 移除 secret value
- 移除可重放 credential
- 保留必要的 redacted state
- 移除或改寫 workspace-sensitive metadata，使其無法還原單一作者工作區

允許保留：

- provider name
- endpoint
- key exists / missing
- key scope 或 label
- last rotated at
- storage backend type

若某份 reference 同時包含 canonical guidance 與 live workspace values，應拆成：

- 可共享的 sanitized guidance / template example
- 僅留在 authoring repo 的 live baseline reference

## 10. Recommendation Ladder

UniText 對 secret storage 的建議優先序如下：

1. `OS secret store`
   - Windows: DPAPI / Credential Manager
   - macOS: Keychain
   - Linux: Secret Service / keyring
2. `native helper / native messaging host`
   - 當 CLI 或 extension 無法直接安全持久化 secret 時
3. `separated local secret store`
   - 與一般 config 分離，且不可被 untrusted contexts 直接讀取
4. `runtime session only`
   - 作為輔助，不應是唯一長期持久化策略

## 11. Minimum Checklist

在 UniText 中新增任何會處理 secret 的資源或 adapter 前，至少確認：

- secret 是否被排除在 `registry/` 之外
- secret 是否被排除在 `ops/` 之外
- 文件是否只記錄 location / state，而沒有記錄 value
- local-only env habit 是否被排除在 shared env baseline 之外
- export / review package 是否有 redaction
- 是否已記錄目前採用的 storage backend
- 是否已記錄升級路線

## 12. Practical Guidance for Browser Extensions

以 browser extension 類場景為例：

- provider settings 可存在 extension local storage
- API key 不應與一般 provider settings 混存為單一共享值
- 每個 provider 應各自持有 secret
- UI 應支援 staged draft，不可因 provider 切換或 hover/collapse 導致 key 遺失
- 若要達到較高安全等級，應改用 native host + OS secret store，而不是只靠 extension storage

## 13. Current UniText Position

截至目前，UniText 對 secret handling 的正式立場是：

- canonical registry 不承載 secret
- local overlay 可以記錄 secret backend 與路徑類型
- operations artifacts 必須 redacted
- shared env baseline 不承載 local-only environment habit
- 若某整合尚未接上 OS secret store，必須在文件中明示為 interim model

這份文件應被視為：

- authoring guidance
- review checklist reference
- future adapter / secret-store integration 的基準線
