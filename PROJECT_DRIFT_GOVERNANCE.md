# UniText — Project Drift Governance

> 狀態：Draft Baseline
> 用途：定義跨專案對話中，如何偵測 project drift、如何提醒、如何隔離、以及如何安全回到原始專案。

## 1. Purpose

這份規格處理的不是一般文件或程式碼 drift，而是 agent 在多專案工作區內，因為錯誤輸入、相似症狀、截圖誤導、或對話上下文混淆，導致工作焦點從原始專案飄移到另一個專案的治理問題。

本規格的目標是：

- 在 drift 發生時先提醒，而不是直接切換工作目標
- 在未確認前凍結跨專案寫入
- 在確認後提供明確的任務隔離模式
- 在支線任務結束後提醒回到原始專案
- 為後續 `Q:\AGENTS.md` 落地與 resolver 擴充提供一致依據

## 2. Scope

本規格適用於：

- 同一工作區內有多個 repo 或 worktree 的對話式工作
- agent 需要根據目前 `cwd`、repo root、畫面內容、錯誤訊息、與使用者指令判斷是否發生 drift
- 需要區分「只是討論另一個專案」與「正式切換到另一個專案執行工作」

本規格不直接定義：

- UI 視覺高亮的實作細節
- CLI / IDE / MCP 實際注入方式
- 專案內部 feature branch 或 commit policy 的細節

## 3. Definitions

| Term | Meaning |
|---|---|
| `origin_project` | 對話起始時或最近一次正式切換後，被確認為主工作目標的專案 |
| `active_project` | 當前正在執行讀寫操作的專案 |
| `drift_candidate` | 從使用者新訊號判斷出來、可能被誤切入的另一個專案 |
| `project drift` | `active_project` 與使用者實際意圖的主專案不一致，或 agent 在未確認下準備跨專案執行 |
| `isolation_mode` | drift 被確認後，用來隔離支線任務的工作模式 |
| `return_anchor` | 在離開 `origin_project` 後，用來提醒回原專案的固定參考點 |

## 4. Core Principles

- `project drift` 應先提醒，再切換，不可默默切換
- 在未明確確認前，跨專案操作預設只允許讀取，不允許寫入
- 工作區切換與對話主題切換不是同一件事
- 若只是分析另一個專案，但未正式切換，應使用隔離段而不是直接改變 `active_project`
- 若要正式切換專案，應保留 `origin_project` 作為回返錨點

## 5. Drift Detection Signals

下列訊號可用來判定 drift 風險上升：

- 使用者明確提到另一個絕對路徑或 repo 名稱
- 使用者貼出的截圖、UI 標題、錯誤訊息、檔名、技術棧與目前 `cwd` 顯著不一致
- 使用者要求的操作若執行下去，實際會落在另一個 repo
- agent 自身回覆中的 repo 路徑、commit、狀態摘要，與目前工作目錄不一致
- 使用者對目前專案邊界提出質疑，例如「這個專案不是做 X 嗎」

下列情況不應單獨視為 drift：

- 單純討論另一個專案的想法、結構、或規格
- 引用外部 repo 作為比較對象，但未要求切換工作區
- 使用者問的是 workspace-level 規則，而不是要求對另一個 repo 直接寫入

## 6. Warning Banner Format

偵測到 drift 風險時，應輸出固定格式警示，而不是自由發揮：

```text
[Project Drift Warning]
Current project: <active_project>
Detected target: <drift_candidate>
Cross-project write is locked until isolation is confirmed.
```

固定格式的目的：

- 降低長對話中提示語變形
- 讓後續 UI 或 parser 有穩定可辨識的段落
- 讓使用者快速確認目前與候選專案是否正確

## 7. Write-Lock Policy

在 drift 已偵測但尚未確認時：

- 可讀取 `drift_candidate` 的檔案、狀態、與文件以協助判斷
- 不可直接修改 `drift_candidate`
- 不可在 `drift_candidate` commit
- 不可在 `drift_candidate` 啟動高風險或不可逆操作
- 不可把 `active_project` 默默改成 `drift_candidate`

解除 write lock 的條件：

- 使用者明確確認要切換或隔離
- 或使用者明確表示只是討論，不需進入另一個專案

## 8. Isolation Modes

### A. `project-transfer`

用途：

- 問題其實完全屬於另一個 repo
- 接下來的主要讀寫應正式移到 `drift_candidate`

要求：

- 明確宣告 `origin_project`
- 明確宣告 `active_project` 已切到新 repo
- 設定 `return_anchor`

建議提示：

```text
[Isolation Mode: project-transfer]
Origin project: <origin_project>
New active project: <active_project>
Return reminder: enabled
```

### B. `new-worktree`

用途：

- 同一個 git repo 中要切一個獨立工作樹處理支線任務
- 不適用於跨 repo 飄移

要求：

- 僅限同一 repo
- 明確標示新 worktree 路徑與 branch
- 完成後提醒回主 worktree

建議提示：

```text
[Isolation Mode: new-worktree]
Repo: <repo_root>
Worktree: <worktree_path>
Branch: <branch_name>
Return reminder: enabled
```

### C. `in-project-isolated-thread`

用途：

- 不正式切 repo
- 只是要在當前對話中插入一段支線分析、比對、或規格討論

要求：

- `active_project` 不變
- 對話中必須明確標示隔離段開始與結束
- 隔離段預設不得導致跨 repo 寫入

建議段落格式：

```text
[ORIGIN CONTEXT]

[DRIFT-ISOLATED TASK]

[RETURN TO ORIGIN]
```

### D. `workspace-governance-escalation`

用途：

- 主題已經不是單一 repo 內問題
- 而是應提升到 workspace-level 治理、SOP、或平台規則設計

要求：

- 明確指出「此議題不應繼續掛在目前 repo 下展開」
- 轉入治理專案或 workspace 規則層
- 若尚未真正切換 repo，保持讀取式分析

## 9. Return Rules

只要曾離開 `origin_project`，就必須保留回返提醒。

最小要求：

- 隔離任務完成後，明確輸出目前要不要回原始專案
- 若使用者未明示延續在新專案，預設應提醒 `origin_project` 仍是主線

建議提示：

```text
[Return To Origin Reminder]
Origin project: <origin_project>
Current active project: <active_project>
Return now or keep working here?
```

若使用者在隔離狀態中再次引入第三個專案，應先處理：

- 結束目前隔離段
- 或明確升級成新的正式轉移

不應在未收束前形成多層漂移鏈。

## 10. Conversation Structure Requirements

若隔離模式不是 `project-transfer`，對話本身應保留結構標記。

最低要求：

- 可機器識別的段落標頭
- 可讓人快速辨識目前是否在主線或支線
- 支線結束後有回返段落

視覺高亮、背景色、或特殊 UI 標記屬於產品層增強，不屬於本規格的強制部分。若客戶端支援，應優先以固定 banner 與顏色區分 `drift-isolated` 區段。

## 11. Enforcement Layers

這套機制應分兩層落地：

### 11.1 `Q:\AGENTS.md`

放最小可生效版本：

- drift detection rule
- warning banner
- write-lock before confirmation
- allowed isolation modes
- return reminder rule

### 11.2 `Q:\UniText`

放設計、SOP、演進與治理說明：

- 本規格文件
- incident review 樣板引用方式
- resolver 未來擴充欄位
- review gate 與驗證要求

## 12. Incident Review Integration

若真的發生 project drift，應可用 `BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md` 留下事件紀錄。

建議新增或對應的 incident 類型：

- wrong-repo execution
- cross-project status misreport
- screenshot-driven repo inference
- unconfirmed transfer write

這些事件可作為後續規則調整與 guard 強化的依據。

## 13. Future Resolver Integration

`resolve-agent-governance.py` 之後可擴充：

- `drift_guard_mode`
- `cross_project_write_policy`
- `warning_banner_style`
- `return_anchor_policy`
- `isolation_mode_default`

也可以在 report 中增加：

- `drift_governance`
- `workspace_guard_notes`
- `recommended_isolation_mode`

但在實作前，應先讓 `Q:\AGENTS.md` 的最小可生效版本穩定。

## 14. Implementation Order

建議順序如下：

1. 在 `Q:\UniText` 建立本規格，固定語彙與流程
2. 在 `Q:\AGENTS.md` 落地最小 guard 規則
3. 驗證常見 drift 情境的提醒與 write lock 行為
4. 再把 drift-related profile / report 欄位接到 resolver
5. 若客戶端支援，再加入視覺高亮與互動式回返提醒

## 15. Non-Goals

本規格不保證：

- 自動判斷所有 repo 轉移都正確
- 取代人類對工作主線的判斷
- 以 UI 裝飾取代治理規則
- 在沒有 workspace overlay 的情況下，單靠 repo-local 文件保護整個工作區

## 16. Related Docs

- `AGENT_GOVERNANCE_LAYERING.md`
- `DOCUMENT_PLACEMENT_POLICY.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md`
