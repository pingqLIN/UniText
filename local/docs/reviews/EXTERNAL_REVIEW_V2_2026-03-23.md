# UniText 專案第二輪外部審查報告

> **狀態**：Archived Review Reference  
> **說明**：此文件保留作為 2026-03-23 第二輪外部審查的歷史快照。其多項建議與風險已在後續 commits 中被吸收或修正，不應視為當前專案狀態的唯一依據；現行狀態請優先參考 `README.md`、`MILESTONES.md`、`PROJECT_STATUS_REPORT_2026-03-23.md`、`EXTERNAL_REVIEW_PACKAGE.md` 與 `TEMPLATE_RELEASE_PACKAGE.md`。

> **審查日期**：2026-03-23（第二輪）  
> **審查範圍**：`Q:\UniText` 全目錄結構、核心文件、registry 內容、腳本實作、操作歷史  
> **審查性質**：獨立外部審查者視角之全面深度評估  
> **前次審查**：2026-03-23 第一輪（STRATEGIC_REVIEW_2026-03-23.md）  
> **方法論**：逐檔案實際讀取 × 腳本執行驗證 × 逆向思維風險分析 × 量化評估

---

## 1. 審查概要

**UniText 在第一輪審查後展現出顯著且方向正確的改善執行力。** 當時被標記為 CRITICAL 的三項問題（無 Git、無 registry 內容、無批次工具）已全部回應，Phase 1「Skills Registry Online」的六項完成條件已全數達標，專案確實從「設計遠超實作」的失衡狀態推進到了「骨架完備、首批內容落地」的 Phase 1 完成狀態。

然而，第二輪審查揭示了一組**新的結構性問題**：(a) 核心治理腳本 `sync-skills.ps1` 存在與 OPERATIONS.md 安全規範直接矛盾的行為（`/MIR` 無備份、無確認）；(b) 21 個 adoption-ready skills 仍在 backup 中等待——掃描工具顯示全部 26 個候選 skills 均通過 readiness 檢查，瓶頸已非工具缺失而是**執行決策**；(c) `Q:` drive 與 `C:\Dev` 雙路徑問題、`addra` 使用者殘留等環境層面的債務尚未清理；(d) agents、mcp、workflow 三類資源仍僅有 placeholder，架構宣稱與實際內容之間仍有落差。

**整體判定**：Phase 1 ✅ 完成、Phase 2 ⚠️ 門檻可觸及但需執行衝刺、Phase 3 ⚠️ 形式達標但細節仍需硬化、Phase 4 ❌ 尚遠。專案現在最需要的是一輪「治理合規修復 + 大規模 adoption 執行」的集中衝刺，而不是更多設計。

---

## 2. 架構評估（審查重點 1）

### 2.1 三層架構的合理性判定

| 層級 | 職責 | 評價 |
|------|------|------|
| **Registry** | 定義 canonical source of truth | ✅ 正確且必要 |
| **Adapter** | 將 registry 內容對接到各 CLI | ✅ 正確，但目前僅有 `sync-skills.ps1` 這一條 delivery 路徑 |
| **Operations** | 治理 mutation 的安全邊界 | ✅ 設計優秀，但實作層存在違規（詳見 §4） |

**架構合理性：★★★★★**

這三層的責任切分是本專案最具價值的智識資產：

- **Registry-first** 解決了「誰是正本」的問題——在多 CLI 並存的世界中，這是最基礎的需求
- **Adapter-enabled** 正確地將「異質 CLI 如何接收」的問題從 registry 解耦——不要求所有 CLI 都支援同一種格式
- **Operations-governed** 在 AI 工具快速演進的環境中提供了「防止靜默破壞」的安全網

### 2.2 過度設計檢測

**結論：目前沒有明顯的過度設計。**

六份核心文件（README / INDEX / VISION / RESOURCE_SPEC / OPERATIONS / PROJECT_MODES）各自有清楚的職責分工，沒有冗餘重疊。Metadata schema 採三層設計（required / recommended / optional），minimum viable metadata 只要求 4 個欄位（`id`, `type`, `canonical_location`, `status`），門檻極低。

唯一的「設計超前實作」殘留是：四種 delivery mode（pointer / mirror / symlink / native-config）都已定義，但目前只有 mirror（robocopy）和 symlink 兩種被實際使用。這不構成過度設計，因為四種 mode 的定義本身只佔 OPERATIONS.md 幾行文字，且隨著 Codex 的 `native-config` 需求（config.toml 的 skills_path），第三種 mode 已有明確的落地場景。

### 2.3 設計不足檢測

存在兩處設計不足：

1. **Adapter 的責任人不明確**：OPERATIONS.md 說「adapter 應依優先序考慮...」但從未定義誰是 adapter——是 `sync-skills.ps1`？是人工操作？是未來的 CLI plugin？這個模糊性在目前規模下可容忍，但會在 Phase 4 template release 時成為障礙。

2. **Rollback 機制未定義**：OPERATIONS.md 要求「backup before mutation」並有 14 組歷史記錄，但沒有定義**如何從 backup 回復**。目前只有 `recovered_20260318_165117` 這個手動回復的痕跡，沒有 `rollback.ps1` 或等價工具。

### 2.4 2026 年 AI CLI 環境的韌性

**韌性評估：★★★★☆**

Text-native + registry-first 的路線選擇在 AI CLI 快速演進的環境中是**最具防禦性的策略**：

- **純文本是最大公約數**：無論 Claude Code、Codex、Gemini CLI 如何變化，它們都需要讀取文字檔案
- **Logical path 抽象層**：`/registry/skills` 不綁定任何特定 OS 路徑，當 CLI 改變路徑慣例時只需更新 adapter
- **四種 delivery mode 涵蓋了主要可能性**：即使新 CLI 出現，其接收方式大概率落入這四種之一

**韌性風險**：如果某個 CLI（例如 Claude Code）推出原生 registry 功能且成為事實標準，UniText 的獨立 registry 可能變得冗餘。但 VISION.md 的「AI 是重要的 consumer 與協作者，但不是唯一可靠的整合機制」定位已經預見了這個情境——UniText 的價值不是取代原生功能，而是在多工具並存時提供統一介面。

---

## 3. Resource Contract 評估（審查重點 2）

### 3.1 RESOURCE_SPEC.md 清晰度

**清晰度評估：★★★★☆**

RESOURCE_SPEC.md 在 124 行內定義了一套精簡但完整的 metadata contract：

| 面向 | 評價 |
|------|------|
| Identity model | ✅ `(type, id)` 組合清楚 |
| Canonical location | ✅ 邏輯路徑，不綁 OS |
| Metadata tiers | ✅ Required / Recommended / Optional 三層 |
| Lifecycle states | ✅ draft → active → deprecated → archived |
| Conflict rules | ✅ 明確禁止靜默覆蓋 |
| Defaults | ✅ 有合理的 fallback 設計 |

**一個待修正的矛盾**：RESOURCE_SPEC.md 第 79 行說「`source_of_truth` 缺省時，視為等於 `canonical_location`」，但 INDEX.md 中所有 5 個 active skills 都同時列出了 `canonical_location`（目錄層級）和 `source_of_truth`（檔案層級，指向 SKILL.md）。這不是矛盾，而是一個**未被明確記載的慣例**：`canonical_location` = 資源目錄，`source_of_truth` = 資源的入口檔案。建議在 RESOURCE_SPEC.md 中明確此區別。

### 3.2 延伸性評估

**新增資源類型的融入難度：低**

以 `prompts` 類型為例，融入路徑非常自然：

```yaml
id: code-review-prompt
type: prompts
canonical_location: /registry/prompts/code-review-prompt
status: active
source_of_truth: /registry/prompts/code-review-prompt/PROMPT.md
```

只需要：
1. 在 `registry/` 下建立 `prompts/` 目錄
2. 在 INDEX.md 的 Resource Catalog 表格新增一行
3. RESOURCE_SPEC.md 的 Scope 加入 `prompts`

不需要修改 identity model、metadata schema 或 adoption flow。**這是這套 contract 設計最成功的地方——它足夠抽象，不與特定資源類型耦合。**

同理，`datasets`、`templates`、`evaluations` 等類型都能以相同方式融入。

### 3.3 Identity Model Edge Cases

`(type, id)` 的 identity model 存在以下 edge cases：

| 情境 | 風險等級 | 說明 |
|------|---------|------|
| 同名跨類型 | 🟢 低 | 例如 `(skills, pdf)` 和 `(agents, pdf)` 是不同 identity，型別已區分 |
| 層級關係 | 🟡 中 | `hugging-face-cli` 和 `hugging-face-datasets` 是否應有父子關係？目前 id 是 flat 的，無法表達 `hugging-face/*` 的歸屬 |
| 改名遷移 | 🟡 中 | 如果 `huggingface-gradio` 需要改名為 `hf-gradio`，目前沒有 alias 或 redirect 機制 |
| 版本化 | 🟡 中 | 同一個 `(skills, pdf)` 只有一個 canonical 版本，無法同時維護 v1 和 v2 |

**建議**：在 RESOURCE_SPEC.md 的 Identity Rules 節新增一個「Namespacing」段落，說明：(a) id 是 flat 的，不支援階層；(b) 相關 skills 可透過命名前綴（如 `hugging-face-*`）表達關聯，但不構成正式的 hierarchy；(c) 版本化暫不在 scope 內，同一 id 永遠指向當前 canonical version。

---

## 4. 資源分類評估（審查重點 3）

### 4.1 四類覆蓋度

| 資源類型 | 需求真實性 | 目前狀態 | 評價 |
|---------|-----------|---------|------|
| `skills` | ✅ 高：所有主流 AI CLI 都支援某種形式的 skill 載入 | 5 active, 21 待 adopt | 核心主力，狀態最成熟 |
| `mcp` | ✅ 高：MCP 是 2025-2026 年 AI CLI 整合的關鍵標準 | 1 seed template（draft） | 重要但嚴重落後 |
| `agents` | ✅ 中高：多 agent 協作場景日增 | 空目錄 + README placeholder | 定義清楚，但完全無內容 |
| `workflow` | ⚠️ 中：跨 CLI 的 workflow 共享需求尚不明確 | 1 placeholder（draft） | 最模糊的類別 |

### 4.2 遺漏的資源類型

基於 2026 年 AI CLI 生態的觀察，以下資源類型值得考慮但目前未被覆蓋：

1. **`prompts`** — System prompts、few-shot examples、persona definitions。目前可能被隱含在 `skills` 或 `agents` 中，但隨著 prompt engineering 成為獨立實踐，分離出來可能更清晰。
2. **`evaluations`** — mcp-builder 的 reference/ 中已包含 evaluation.md，顯示評估工具已有需求。
3. **`templates`** — 專案 scaffold、starter kits。目前 `.bak_20260315_00` 中的 `template_base/` 暗示了此需求。

**建議**：暫不擴張類型——目前四類中有三類內容嚴重不足，應先填滿既有類別再考慮新增。如果確有需求，`prompts` 可以暫時作為 `skills` 的子類存在（許多 skill 本質上就是 structured prompt）。

### 4.3 邊界模糊問題

存在一個明確的邊界模糊：

- **skills vs. agents**：`frontend-design` 的 SKILL.md 本質上是一份「agent instruction」——它告訴 AI 如何做前端設計，包含 persona 和 behavioral guidelines。那它應該是 skill 還是 agent？

目前的隱含區分似乎是：
- `skills` = 特定任務的知識與工具（做什麼、怎麼做）
- `agents` = 角色定義與行為框架（以什麼身份做）

**建議**：在 RESOURCE_SPEC.md 或 VISION.md 中新增一段「Resource Type Boundaries」，明確這兩者的區分標準，避免未來 adoption 時的分類困惑。

---

## 5. Adoption Flow 評估（審查重點 4）

### 5.1 六步驟定義清晰度

| 步驟 | 定義清晰度 | 工具支撐 | 評價 |
|------|-----------|---------|------|
| **SCAN** | ⚠️ OPERATIONS.md 僅列出名稱 | ✅ `scan-skills.ps1` | 工具比文件先行——scan 的具體定義應補回 OPERATIONS.md |
| **REVIEW** | ❌ 未定義「review 什麼」 | ❌ 無工具 | **最大缺口**：應至少有一份 review checklist |
| **DRY-RUN** | ✅ 有明確的 safety rule | ✅ `batch-adopt-skills.ps1 -DryRun` | 實作到位 |
| **ADOPT** | ⚠️ 僅隱含在 batch-adopt 行為中 | ✅ `batch-adopt-skills.ps1` | 但 adopt 缺少 backup（見 §5.2） |
| **DELIVER** | ✅ 有 delivery mode 定義 | ⚠️ `sync-skills.ps1` 有嚴重問題 | 見 §5.2 |
| **VERIFY** | ⚠️ 僅定義「要驗證」 | ✅ `verify-delivery.ps1` + `health-check.ps1` | 工具存在，但驗證深度不足 |

### 5.2 治理違規：sync-skills.ps1 的嚴重問題

**這是本次審查發現的最嚴重問題。**

`sync-skills.ps1` 是專案中唯一的 delivery 執行工具，但它**直接違反了 OPERATIONS.md 定義的三條安全規則中的兩條**：

| OPERATIONS.md 規則 | sync-skills.ps1 實際行為 | 違規嚴重度 |
|-------------------|------------------------|-----------|
| **Backup Before Mutation** | ❌ 無任何 backup 機制 | 🔴 CRITICAL |
| **Dry-Run First** | ✅ 支援 `-DryRun` | ✅ 合規 |
| **No Silent Canonicalization** | ⚠️ `/MIR` 會靜默刪除目標目錄中不在 source 的檔案 | 🔴 CRITICAL |

具體問題：

```powershell
robocopy $source $t /MIR /R:1 /W:1 /NFL /NDL /NJH /NJS /NP $mode | Out-Null
```

- **`/MIR`（Mirror）**：會刪除目標目錄中不存在於 source 的所有檔案。如果使用者在 `~/.claude/skills` 中有 CLI 自行新增的檔案，`/MIR` 會**不可逆地刪除它們**
- **`| Out-Null`**：robocopy 的所有輸出（包括錯誤）都被吞掉，違反 audit trail 精神
- **無 backup**：執行前不建立任何回復點
- **無確認提示**：非 DryRun 模式下直接執行破壞性操作
- **只覆蓋 3 個 CLI**：.claude、.gemini、.agents——但 Codex 需要 native-config（config.toml 的 skills_path），完全未處理

同樣，`batch-adopt-skills.ps1` 也存在違規：

```powershell
if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
Copy-Item $src $dst -Recurse
```

在覆寫 registry/skills/ 中既有內容時，先刪後寫，無 backup。

### 5.3 Adoption Flow 可行性與可重複性

**可行性：✅ 已驗證**——首批 5 個 skills 確實走通了 SCAN → ADOPT → DELIVER → VERIFY 的路徑，且 health-check 通過。

**可重複性：⚠️ 有條件的**——scan-skills.ps1 的掃描結果顯示剩餘 21 個 skills 全部通過 readiness 檢查（`adoption_ready = True`），表示批次 adopt 的技術條件已成熟。但 `batch-adopt-skills.ps1` 中 `$Ids` 參數預設只列出首批 5 個，需要手動更新才能處理其餘 21 個。

### 5.4 「No Silent Changes」政策的摩擦評估

**目前摩擦度：低**，因為操作頻率低（目前只在初始 adoption 時才觸發）。但有一個隱含的摩擦源：

- 每次新增或更新 skill 都需要手動同步到 INDEX.md 的 catalog entries
- 目前 5 個 skills 已需 5 個 table block × 7 個欄位 = 35 行 INDEX.md 內容
- 擴展到 26 個 skills 後，INDEX.md 的 catalog 部分將達 ~180 行，維護成本顯著上升

**建議**：考慮建立 `generate-index.ps1`，從 `registry/skills/*/SKILL.md` 的 frontmatter 自動生成 INDEX.md 的 catalog 區段，減少手動同步的摩擦。

---

## 6. 執行節奏評估（審查重點 5）

### 6.1 「先文件再實作」的節奏判斷

**這個節奏在 Phase 1 是正確的，但在 Phase 2 必須反轉。**

Phase 1 的成功證明了「先建立治理框架，再填入內容」的策略是有效的——有了 RESOURCE_SPEC.md 的 contract 和 OPERATIONS.md 的 safety rules，首批 5 個 skills 的 adoption 才能有章可循。

但現在框架已就位，繼續花時間在文件上會形成**設計債務的反面——實作延遲債務**。21 個 adoption-ready skills 全部通過 scan 檢查的事實，意味著**唯一的瓶頸是執行決策，不是工具或流程缺失**。

### 6.2 5/27 進度的瓶頸分析

| 假說 | 驗證結果 |
|------|---------|
| 「工具不足導致無法批次 adopt」 | ❌ 已被否定——`batch-adopt-skills.ps1` 已存在且首批驗證成功 |
| 「候選 skills 品質不足」 | ❌ 已被否定——scan 結果顯示 26/26 通過 readiness 檢查 |
| 「registry 結構未準備好」 | ❌ 已被否定——`registry/skills/` 已建立且 5 個 skills 已成功入住 |
| 「人工 review 成本過高」 | ⚠️ 可能——REVIEW 步驟缺乏 checklist，每個 skill 的 review 都需要臨時判斷 |
| 「執行時間尚未分配」 | ✅ 最可能——從 git log 看只有 2 個 commits，顯示工作集中在一天完成，之後未繼續 |

**結論**：瓶頸已從「工具缺失」轉移到「執行節奏」。建議設定明確的 batch adoption 目標（例如：下一次工作 session 完成全部 21 個 skills 的 adopt）。

### 6.3 下一步優先順序建議

**優先做：完成 skills 全覆蓋（21 → 0 待 adopt）。原因：**

1. skills 是目前唯一有完整工具鏈（scan → adopt → deliver → verify）的資源類型
2. 擴大 skills 覆蓋可以立即驗證 batch adoption 流程在大規模下的可行性
3. 26 個 skills 的 catalog 是 UniText 最具說服力的「為什麼你需要這個」論據

**暫緩做：agents/mcp 填充。原因：**

1. agents 和 mcp 的 adoption 工具尚不存在（scan-skills.ps1 只掃 skills）
2. 「先把一個類型做深做透」比「四個類型都淺嘗輒止」更能驗證架構可行性
3. agents 的 skill-vs-agent 邊界問題（§4.3）需要先釐清

---

## 7. 風險與應急分析

### 7.1 風險矩陣（已更新）

| ID | 風險 | 嚴重度 | 狀態 | 說明 |
|----|------|--------|------|------|
| R1 | 無 Git 版本控制 | CRITICAL | ✅ **已修復** | 2 commits on main |
| R2 | Skills registry 空置 | CRITICAL | ✅ **已修復** | 5 skills active |
| R3 | 無批次 adoption 工具 | CRITICAL | ✅ **已修復** | batch-adopt-skills.ps1 就緒 |
| R4 | 無量化里程碑 | HIGH | ✅ **已修復** | MILESTONES.md 已建立 |
| R5 | sync-skills.ps1 來源路徑錯誤 | HIGH | ✅ **已修復** | 已改指 registry/skills |
| **R6** | **sync-skills.ps1 治理違規** | **🔴 CRITICAL** | **🆕 新增** | /MIR 無 backup、無確認、吞輸出 |
| **R7** | **batch-adopt 無 backup** | **🔴 HIGH** | **🆕 新增** | Remove-Item -Recurse -Force 前無備份 |
| **R8** | **Q: vs C:\Dev 雙路徑混亂** | **🟡 MEDIUM** | **🆕 新增** | 實際工作在 Q:\UniText，但 ops/baseline.json、PATH_MAP.md、inventory.latest.json 全指 C:\Dev\UniText |
| **R9** | **addra 使用者殘留** | **🟡 MEDIUM** | **🆕 新增** | inventory.latest.json 中 codex.skills_path 引用 `C:\Users\addra\` |
| **R10** | **Gemini 設定衝突** | **🟡 MEDIUM** | **未變** | disableAutoUpdate 與 enableAutoUpdate 並存 |
| R11 | authoring 文件副本重複 | LOW | ⬇️ **降級** | 已確認 local/docs/authoring/ 是「重構前保留版」，非意外重複 |
| **R12** | **INDEX.md 手動維護擴展性** | **🟡 MEDIUM** | **🆕 新增** | 擴展到 26 skills 後 INDEX.md 將極難手動維護 |
| R13 | AI_UNIFIED 舊名殘留 | LOW | **未變** | 歷史檔案中仍有殘留 |
| **R14** | **Rollback 機制缺失** | **🟡 MEDIUM** | **🆕 新增** | 有 backup 歷史但無回復工具 |
| **R15** | **Codex delivery 路徑缺失** | **🟡 MEDIUM** | **🆕 新增** | sync-skills.ps1 只覆蓋 3 CLI，不處理 Codex 的 native-config |

### 7.2 關鍵風險應急策略

#### R6: sync-skills.ps1 治理違規（CRITICAL）

- **觸發條件**：任何非 DryRun 的 sync 執行
- **應急策略**：
  1. **立即**：在 sync-skills.ps1 中加入 backup 步驟（在 robocopy 前先 Copy-Item 目標到 timestamped backup）
  2. **立即**：將 `/MIR` 替換為 `/E`（只新增不刪除）或改用 `Copy-Item -Recurse` + 明確的差異比對
  3. **立即**：移除 `| Out-Null`，改為寫入 `ops/history/sync_<timestamp>/log.txt`
  4. **短期**：加入非 DryRun 模式的確認提示
- **影響**：修復約 1-2 小時，不影響既有 registry 內容

#### R7: batch-adopt 無 backup（HIGH）

- **觸發條件**：對已有內容的 skill 目錄執行 adopt 覆寫
- **應急策略**：在 `Remove-Item` 前加入 `Copy-Item $dst "$dst.bak.$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Recurse`
- **影響**：修復約 30 分鐘

#### R8: 雙路徑混亂（MEDIUM）

- **觸發條件**：在 C:\Dev 或 Q:\ 以外的路徑嘗試運行腳本
- **應急策略**：
  1. 在 README.md 或 PROJECT_MODES.md 中明確記載 Q: drive 的對應關係
  2. 更新 PATH_MAP.md 為 `registry/` 架構下的版本，或標記為 `archived`
  3. 長期：讓所有腳本使用 `$PSScriptRoot` 相對路徑，不依賴特定 drive letter
- **影響**：文件更新約 1 小時；腳本已使用 `Resolve-Path` 相對路徑，風險可控

---

## 8. 已 Adopt Skills 品質評估

### 8.1 逐 Skill 評估

#### frontend-design（★★★☆☆）

| 面向 | 評價 |
|------|------|
| SKILL.md | 43 行，精簡但完整的設計哲學指南 |
| 內容品質 | 優秀的 aesthetic guidelines，anti-pattern 清單實用 |
| 支援檔案 | 僅 LICENSE.txt，無範例、無腳本 |
| Production-grade? | **⚠️ 半成品**——作為「設計原則文件」足夠，但作為「可被 AI agent 執行的 skill」略薄 |

**改善建議**：增加 2-3 個具體的 before/after 設計案例，讓 AI agent 有更具體的執行參考。

#### pdf（★★★★★）

| 面向 | 評價 |
|------|------|
| SKILL.md | 226 行，含快速參考 + 工具矩陣 + workflow 決策樹 |
| 支援檔案 | forms.md (186行) + reference.md (496行) + 8 個 Python scripts |
| 總行數 | ~908 行 |
| Production-grade? | **✅ 是**——完整的工具鏈，涵蓋 fillable/non-fillable form 兩條路徑 |

#### docx（★★★★★）

| 面向 | 評價 |
|------|------|
| SKILL.md | 144 行，含 workflow 決策樹 + redlining 流程 |
| 支援檔案 | docx-js.md (320行) + ooxml.md (512行) + Python library + 48 XSD schemas |
| 總行數 | ~976 行（不含 XSD schemas） |
| Production-grade? | **✅ 是**——涵蓋 JS + Python 雙實作，含完整 OOXML 規範 |

#### xlsx（★★★★☆）

| 面向 | 評價 |
|------|------|
| SKILL.md | 222 行，含嚴格的 financial model 標準 |
| 支援檔案 | recalc.py（LibreOffice 公式重算工具） |
| Production-grade? | **✅ 是**——requirements-first 的方法特別適合 Excel 的品質控制場景 |

**小缺口**：缺少範例 financial model 模板。

#### mcp-builder（★★★★★）

| 面向 | 評價 |
|------|------|
| SKILL.md | 165 行，含 4-phase 開發流程 |
| 支援檔案 | 4 份 reference 指南 (1,037行) + evaluation 框架 + scripts |
| 總行數 | ~2,202 行 |
| Production-grade? | **✅ 是**——這是五個 skills 中最完整的，含 TypeScript + Python 雙語言指南 |

### 8.2 品質總結

| 品質等級 | Skills | 佔比 |
|---------|--------|------|
| ★★★★★ Production-grade | pdf, docx, mcp-builder | 3/5 (60%) |
| ★★★★☆ Near-production | xlsx | 1/5 (20%) |
| ★★★☆☆ Needs improvement | frontend-design | 1/5 (20%) |

**整體評價**：首批 5 個 skills 的選擇是正確的——它們代表了「文件處理」和「工具開發」兩大使用場景，4/5 達到 production-grade。首批選擇展示了 UniText 的實際價值：AI agent 可以直接讀取這些 skills 並執行複雜任務（PDF 表單填寫、Word 文件 redlining、MCP server 開發）。

---

## 9. 具體改善建議

### 建議 1：修復 sync-skills.ps1 的治理違規 [CRITICAL]

**做什麼**：重寫 sync-skills.ps1，加入 backup-before-mutation、移除 `/MIR`、移除 `| Out-Null`、加入確認提示。

**為什麼**：這是專案自身治理規則（OPERATIONS.md §5）與實作之間最嚴重的矛盾。如果核心 delivery 工具都不遵守自己定義的安全規則，整套治理框架的可信度歸零。

**如何開始**：

```powershell
# 在 robocopy 前加入：
$backupDir = Join-Path $repo "ops\history\sync_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
foreach($t in $targets){
  if (Test-Path $t) {
    $backupTarget = Join-Path $backupDir (Split-Path $t -Leaf)
    Copy-Item $t $backupTarget -Recurse
  }
}

# 將 /MIR 替換為 /E（只新增、不刪除）
# 或使用更安全的 diff-then-copy 策略
robocopy $source $t /E /R:1 /W:1 *>&1 | Tee-Object -FilePath "$backupDir\sync.log"
```

---

### 建議 2：執行全量 Skills Adoption [HIGH]

**做什麼**：一次性完成剩餘 21 個 skills 的 batch adoption，從 `.bak_20260315_00\skills.bak.20260228_215107` 遷入 `registry/skills/`。

**為什麼**：scan 結果顯示全部 26 個候選 skills 均 `adoption_ready = True`。技術瓶頸已不存在，唯一需要的是執行決策。26 個 active skills 的 registry 比 5 個有數量級的說服力差異。

**如何開始**：

```powershell
$allIds = @("algorithmic-art","brand-guidelines","canvas-design","doc-coauthoring",
  "hf-mcp","hugging-face-cli","hugging-face-datasets","hugging-face-evaluation",
  "hugging-face-jobs","hugging-face-model-trainer","hugging-face-paper-publisher",
  "hugging-face-tool-builder","hugging-face-trackio","huggingface-gradio",
  "internal-comms","pptx","skill-creator","slack-gif-creator","theme-factory",
  "web-artifacts-builder","webapp-testing")

# 先 DryRun
.\local\scripts\batch-adopt-skills.ps1 -Ids $allIds -DryRun

# 確認無誤後正式執行（先修好 backup 問題！）
.\local\scripts\batch-adopt-skills.ps1 -Ids $allIds
```

然後更新 INDEX.md 的 catalog entries（或建立 generate-index.ps1 自動化此步驟）。

---

### 建議 3：建立 REVIEW Checklist [HIGH]

**做什麼**：建立 `local/docs/ADOPTION_CHECKLIST.md`，定義 REVIEW 步驟的具體檢查項目。

**為什麼**：Adoption Flow 六步驟中，REVIEW 是唯一既無定義也無工具的步驟。缺少 checklist 會導致每次 adoption 的品質標準不一致。

**如何開始**：

```markdown
# Adoption Review Checklist

## Required（必須全部通過）
- [ ] SKILL.md 存在且以 `---` frontmatter 開頭
- [ ] frontmatter 含 `name` 和 `description`
- [ ] name 與目錄名稱一致（或有合理的 alias 說明）
- [ ] 內容非空白，至少含一個 ## 段落

## Recommended（建議通過）
- [ ] LICENSE.txt 存在
- [ ] 包含 Usage 或 Workflow 章節
- [ ] 無硬編碼的使用者路徑
- [ ] 無 CLI 特定的設定（應抽象為通用指引）

## Optional
- [ ] 包含支援腳本
- [ ] 包含參考文件
```

---

### 建議 4：解決雙路徑問題 [MEDIUM]

**做什麼**：在 PROJECT_MODES.md 或新建的 `local/docs/ENVIRONMENT.md` 中記載 Q: drive 與 C:\Dev 的對應關係；將 PATH_MAP.md 的 status 從「Legacy Reference」改為「Archived」或直接更新為 `registry/` 架構版本。

**為什麼**：ops/baseline.json 指向 `C:\Dev\UniText`，ops/inventory.latest.json 指向 `C:\Dev\UniText`，但實際工作目錄是 `Q:\UniText`。symlink targets 也指向 `Q:\UniText\registry\skills`。這種混亂在多人協作或機器遷移時會造成不可預測的故障。

**如何開始**：
1. 在 `local/docs/ENVIRONMENT.md` 中記載：`Q:\ 是 C:\Dev 的映射（subst Q: C:\Dev）` 或實際的對應關係
2. 將 PATH_MAP.md 標題改為 `# AI CLI Path Map (Archived)`，加入 banner 指向 OPERATIONS.md
3. 清理 inventory.latest.json 中的 `addra` 引用——重新執行 inventory scan 或手動修正

---

### 建議 5：建立 INDEX 自動生成工具 [MEDIUM]

**做什麼**：建立 `local/scripts/generate-index-entries.ps1`，從 `registry/skills/*/SKILL.md` 的 frontmatter 自動產生 INDEX.md 格式的 catalog entries。

**為什麼**：目前 5 個 skills 的 catalog 在 INDEX.md 中佔 ~50 行。擴展到 26 個後將達 ~260 行，手動維護將成為嚴重的摩擦源，也違反「No Silent Changes」的精神（因為人工編輯大量重複結構時極易引入靜默錯誤）。

**如何開始**：

```powershell
Get-ChildItem registry\skills -Directory | ForEach-Object {
  $skillMd = Get-Content (Join-Path $_.FullName "SKILL.md") -Raw
  $name = if ($skillMd -match '(?m)^name:\s*(.+)$') { $Matches[1].Trim() } else { $_.Name }
  @"
| Field | Value |
|---|---|
| ``id`` | ``$($_.Name)`` |
| ``type`` | ``skills`` |
| ``canonical_location`` | ``/registry/skills/$($_.Name)`` |
| ``status`` | ``active`` |
| ``source_of_truth`` | ``/registry/skills/$($_.Name)/SKILL.md`` |
| ``supported_clis`` | ``claude, codex, gemini`` |
"@
}
```

---

### 建議 6：補齊 Adoption Flow 中每步驟的定義 [MEDIUM]

**做什麼**：在 OPERATIONS.md 的 §6 Adoption Flow 中，為每個步驟加入 1-3 行的操作定義。

**為什麼**：目前六個步驟只有名稱沒有定義，像一個沒有內容的目錄頁。這讓外部使用者無法獨立執行 adoption flow。

**如何開始**：

```markdown
## 6. Adoption Flow

1. **SCAN** — 掃描候選資源來源，列出所有可被 adopt 的資源及其 readiness 狀態
2. **REVIEW** — 依 ADOPTION_CHECKLIST 逐項檢查資源品質與合規性
3. **DRY-RUN** — 以 dry-run 模式執行 adopt，預覽將發生的檔案操作
4. **ADOPT** — 將資源從來源複製到 registry 的 canonical location（含 backup）
5. **DELIVER** — 透過 adapter 將 registry 內容同步到各 CLI 的預期路徑
6. **VERIFY** — 驗證 delivery 結果：檔案存在性、symlink 正確性、CLI 實際載入
```

---

### 建議 7：建立最小 Rollback 工具 [LOW-MEDIUM]

**做什麼**：建立 `local/scripts/rollback-skills.ps1`，能從 `ops/history/` 的 backup 中回復到指定時間點。

**為什麼**：OPERATIONS.md 要求 backup before mutation，且 `ops/history/` 確實有 14 組歷史記錄。但目前唯一的回復經驗是 `recovered_20260318_165117` 的手動操作。沒有 rollback 工具意味著 backup 的價值只在理論上存在。

**如何開始**：先建立一個最簡版本——列出可用的 backup、讓使用者選擇、以 dry-run 模式預覽回復內容、確認後執行。

---

## 10. Phase 推進路線圖建議

### 現況判定

| Phase | 完成度 | 判定 |
|-------|--------|------|
| Phase 1: Skills Registry Online | **100%** | ✅ 6/6 條件全部達標 |
| Phase 2: Full Registry Baseline | **30%** | agents/ 已建立但空，mcp/ 有 seed，workflow/ 有 placeholder，scan/verify/sync 工具存在但需硬化 |
| Phase 3: External Review Ready | **70%** | Git ✅，.gitignore ✅，但文件狀態一致性仍有缺口（PATH_MAP 過時、雙路徑問題） |
| Phase 4: Template Release Ready | **10%** | local-only artifacts 尚未清理，template export 流程未文件化 |

### 建議路線圖

```
Week 1: 治理修復衝刺
├── Day 1: 修復 sync-skills.ps1（R6）+ batch-adopt backup（R7）
├── Day 2: 建立 ADOPTION_CHECKLIST.md + 補齊 OPERATIONS.md §6
└── Day 3: 修正雙路徑問題（R8）+ 清理 addra 引用（R9）
         → git commit: "fix: operations compliance and env cleanup"

Week 2: 大規模 Adoption 衝刺
├── Day 1: 全量 21 skills batch adoption（DryRun → 執行）
├── Day 2: 建立 generate-index-entries.ps1 + 更新 INDEX.md
├── Day 3: sync + verify 全部 26 skills 到 3 CLI targets
         → git commit: "feat: full skills registry adoption (26 skills)"

Week 3: Phase 2 補齊
├── Day 1: 建立第一個 agents entry（從現有 skills 中辨識 agent-like 內容）
├── Day 2: 將 mcp seed 從 draft 升級為 active（或加入第二個 MCP 定義）
├── Day 3: CLI_COMPAT_MATRIX 重新驗證 + Codex native-config delivery 實作
         → git commit: "feat: Phase 2 registry baseline"

Week 4: Phase 3 硬化
├── Day 1: 歸檔 PATH_MAP.md + 清理 local/docs/authoring/ 殘留
├── Day 2: 建立 rollback-skills.ps1 最小版本
├── Day 3: 全面 health-check + 外部審查 re-verification
         → git commit: "chore: Phase 3 external review hardening"
```

### 里程碑量化條件（建議更新 MILESTONES.md）

| Phase | 建議新增的量化條件 |
|-------|-----------------|
| Phase 1 ✅ | （已達標，不需修改） |
| Phase 2 | adopted_skills ≥ 20、agents 至少 1 個 active entry、mcp 至少 1 個 active entry、sync-skills.ps1 通過治理合規檢查 |
| Phase 3 | 所有核心文件間無交叉引用錯誤、PATH_MAP.md 已歸檔或更新、無 `addra` / `AI_UNIFIED` 殘留、health-check + verify-delivery 全部通過 |
| Phase 4 | `git archive` 或等價 export 流程可產出不含 `ops/history/`、`backup/`、`recovered_*/` 的乾淨包、至少 2 個 CLI（Claude Code + Gemini CLI）完成端到端 delivery + 實際載入驗證 |

---

## 附錄 A：額外深度分析

### A.1 Q: drive vs C:\Dev 雙路徑問題

**事實**：
- `ops/baseline.json` 中所有 8 個被追蹤檔案的路徑均以 `C:\Users\miles\` 開頭
- `ops/inventory.latest.json` 中 `shared_root` 為 `C:\Dev\UniText`
- `PATH_MAP.md` 中所有路徑指向 `C:\Dev\UniText\`
- 實際 working directory 為 `Q:\UniText`
- symlink targets 指向 `Q:\UniText\registry\skills`

**推斷**：Q: 很可能是 `subst Q: C:\Dev` 或類似的 drive mapping。兩條路徑指向同一物理位置。

**風險**：如果 `subst` mapping 失效（重開機後未自動建立），symlink 會斷裂。此外，Git 記錄中的路徑與 ops/ 中的路徑不一致，影響 drift detection baseline 的有效性。

**建議**：在 `local/docs/ENVIRONMENT.md` 中明確記載映射關係，並將 `subst` 命令加入開機自動執行（或改為使用 `mklink /D` 永久映射）。

### A.2 local/docs/authoring/ 文件副本處理

**事實**：經 MD5 比對確認，`local/docs/authoring/` 中的 5 份文件（INDEX.md、OPERATIONS.md、PROJECT_MODES.md、RESOURCE_SPEC.md、VISION.md）與根目錄版本**不相同**——它們是「重構前保留的 authoring 強化版」。

**建議**：
- 短期：在 `local/docs/authoring/README.md` 中加入明確的 banner，說明這些是「歷史參考版本」，canonical version 在根目錄
- 中期：逐一比對 authoring 版本與根目錄版本的差異，將任何有價值的內容合併回根目錄
- 長期：合併完成後，將 authoring/ 目錄加入 .gitignore 或刪除

### A.3 Phase 1→4 推進路徑的現實性

**Phase 1 → Phase 2**：**✅ 現實且可在 2 週內完成。** 主要工作量是 21 個 skills 的 batch adopt（技術上只需一條命令）+ INDEX.md 更新 + agents/mcp 各一個最小 entry。

**Phase 2 → Phase 3**：**✅ 現實且可在 1 週內完成。** 主要是文件清理和一致性修復，不需要新的架構設計。

**Phase 3 → Phase 4**：**⚠️ 有條件的現實。** Template release 需要：(a) 乾淨的 export 流程；(b) 至少 2 個 CLI 的端到端驗證。其中 (b) 的風險在於 CLI 版本更新可能改變 skills 讀取行為——CLI_COMPAT_MATRIX 中所有 3 個主要 CLI 都標記為「待重新驗證」。如果驗證失敗，需要更新 adapter 邏輯，時間不可預測。

**整體判斷**：4 週完成到 Phase 3 是現實的；Phase 4 需要視 CLI 驗證結果而定，建議預留 2-4 週彈性。

---

*報告結束。以上分析基於 2026-03-23 對 `Q:\UniText` 全目錄的實際檔案讀取與腳本執行驗證。*
