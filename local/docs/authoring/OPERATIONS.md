# UniText — Operations v1

> 狀態：Draft
> 角色：定義 adapter / operations control plane 的責任、delivery 規則、安全邊界與映射方式。

## 1. Purpose

`OPERATIONS.md` 說明的是：

- shared resources 如何被送進不同 CLI
- delivery mode 何時、如何被解析
- 哪些操作需要 dry-run、backup、explicit confirmation
- path mapping 應如何被記錄

它不定義資源本體；資源本體由 `RESOURCE_SPEC.md` 定義。

## 2. Scope

本文件涵蓋：

- adapter responsibilities
- delivery modes
- delivery triggers
- adoption flow
- drift detection 與 repair
- operations state artifacts
- logical-to-physical path mapping

本文件不涵蓋：

- shared resource metadata schema
- 單一平台的唯一實作方式
- 某個 CLI 的內部產品規格
- authoring repo 與 starter/template 的發佈邊界

repo 身分與發佈邊界由 `PROJECT_MODES.md` 定義。

## 3. Operations Model

### 3.1 Actors

- `registry`
  - 宣告 canonical resources 與 metadata
- `adapter`
  - 將 resource 對接到單一 CLI
- `operator`
  - 觸發 install、sync、adopt、repair 的 human 或 AI
- `cli runtime`
  - 最終消費資源的工具

### 3.2 Operations State

operations layer 可以產生以下 state artifacts：

- inventories
- baselines
- backup snapshots
- drift reports
- repair plans
- audit trails

這些 artifacts 屬於 `/operations`，不是 shared resource type。

## 4. Delivery Modes

| Mode | When to use | Typical effect |
|---|---|---|
| `pointer` | discovery 或非機器註冊型資源 | 提供入口，不複製內容 |
| `mirror` | CLI 需要本地副本、或 symlink 不穩定 | 複製 canonical content 到 CLI 可讀位置 |
| `symlink` | CLI 需要固定路徑，且環境支援穩定連結 | 保持單一 source of truth，同時滿足固定路徑需求 |
| `native-config` | CLI 有正式設定入口可註冊資源 | 寫入 CLI 支援的原生設定格式 |

`delivery mode` 不是資源的固定硬屬性，而是由 adapter 在操作時解析。

## 5. Delivery Resolution Rules

adapter 解析 delivery mode 時，應依下列優先序考慮：

1. 若 CLI 有穩定、正式、可維運的原生設定入口，優先 `native-config`
2. 若 CLI 需要固定路徑且平台支援穩定連結，可用 `symlink`
3. 若 symlink 不穩定、不可用，或 CLI 只接受實體副本，使用 `mirror`
4. 若資源主要目的是 discovery 或文件入口，使用 `pointer`

解析時必須考慮：

- CLI 能力
- 作業系統
- 權限模型
- 使用者的安全偏好
- 是否存在既有本地資源需納管

## 6. Delivery Triggers

delivery 只能由明確 trigger 啟動。

| Trigger | Purpose | Typical initiator |
|---|---|---|
| `bootstrap` | 新 CLI 第一次接入 UniText | human / AI operator |
| `sync` | 將 canonical changes 送到既有 CLI | human / AI operator |
| `adopt` | 將既有本地資源正式納入 registry | human / AI operator |
| `repair` | 根據 drift 檢查結果修復不一致 | human / AI operator |

禁止：

- 未經宣告的背景自動變更
- 在未建立 backup 的情況下做破壞性覆寫
- 在偵測到衝突時靜默決定 canonical source

## 7. Safety Rules

### 7.1 Dry-Run First

以下操作在會改動本地檔案、設定或連結時，應先產出 dry-run plan：

- `adopt`
- `repair`
- 會覆寫既有本地狀態的 `sync`

dry-run 至少應說明：

- 哪些資源會受影響
- 哪個 source of truth 將被採用
- 預計的 delivery mode
- backup 位置或策略
- 潛在衝突與風險

### 7.2 Backup Before Mutation

所有會改動現有狀態的操作，都應可回滾。

最小要求：

- 有 backup 或等價回復點
- 有可追溯的操作記錄
- 有失敗時的停止條件

### 7.3 No Silent Canonicalization

若找到同名異內容資源：

- 必須停在 review
- 必須讓 operator 明確決定 canonical source
- 必須記錄 provenance 或決策結果

## 8. Adoption Flow

正式納管流程如下：

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

### 8.1 SCAN

收集現有資源、候選來源、衝突與平台限制。

### 8.2 REVIEW

由 human 或 AI operator 檢視候選列表，確認：

- 哪個資源應進入 registry
- 哪些資源應保留原狀
- 哪些資源存在衝突

### 8.3 DRY-RUN

產出預計變更計畫，不做真正 mutation。

### 8.4 ADOPT

將選定資源正式納入 registry，並記錄 provenance。

### 8.5 DELIVER

由 adapter 將 canonical resources 送進目標 CLI。

### 8.6 VERIFY

確認：

- CLI 能讀到資源
- canonical source 未被意外破壞
- delivery mode 與預期一致

## 9. Drift and Repair

### 9.1 Drift

drift 指的是 registry、operations state 與實際 CLI 消費狀態之間出現不可忽略差異。

常見 drift 類型：

- canonical source 已更新，但 CLI 消費端仍是舊版本
- CLI 設定已變更，導致 native-config 註冊失效
- mirror 或 symlink 與 source of truth 脫鉤

### 9.2 Repair

`repair` 應優先：

- 偵測
- 回報
- 產生 dry-run 計畫

是否真正執行 mutation，取決於安全規則與 operator 確認。

## 10. Operations State Artifacts

以下內容屬於 operations state，而非 shared resources：

- inventories
- baselines
- backups
- drift reports
- repair plans
- audit trails

它們的用途是支援治理，而不是讓 CLI 直接消費。

## Appendix A. Logical-to-Physical Mapping

邏輯路徑是穩定契約；實體路徑是 deployment-specific mapping。

| Logical area | Meaning | Physical mapping examples |
|---|---|---|
| `/registry/skills` | canonical skill sources | central shared directory、repo subdir、mounted shared path |
| `/registry/mcp` | canonical MCP definitions | canonical config folder、generated manifest root |
| `/registry/agents` | canonical agent instruction roots | agent profiles directory、shared prompt library |
| `/registry/workflow` | workflow docs / runbooks | shared workflow folder、project-local docs |
| `/operations` | inventories、backups、drift logs | ops folder、state store、audit directory |

這張表描述的是 mapping 類型，不是單一平台的唯一答案。

## Appendix B. Legacy Reference Mapping

若 repo 中已存在特定平台或單一部署的路徑對照文件，可保留為 reference implementation。

例如：

- `local/docs/PATH_MAP.md`
- `local/docs/MCP_DEPLOYMENT_NOTES.md`
- `local/docs/WORKFLOW_DEPLOYMENT_NOTES.md`

但這類文件屬於：

- deployment notes
- migration aids
- historical snapshots

它們不應覆蓋本文件的邏輯契約。
