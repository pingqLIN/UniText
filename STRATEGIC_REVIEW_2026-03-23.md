# UniText 專案策略性深度審查報告

> **審查日期**：2026-03-23  
> **審查範圍**：`C:\Dev\UniText` 全目錄結構、核心文件、操作歷史、備份資料  
> **審查性質**：獨立第三方視角之策略性專案評估  
> **審查方法論**：多維度評估 × 逆向思維風險分析 × 具體應急規劃

---

## 一、優勢與正確決策

在進入批判性分析前，必須先肯定 UniText 在以下面向展現出的**設計成熟度明顯超越同類個人專案**：

### 1.1 架構願景的清晰度（★★★★★）

「Registry-first, adapter-enabled, operations-governed」不只是口號——VISION.md 將此三層架構的責任邊界、交互方式、為什麼需要每一層都講清楚了。這表現出對問題空間的深度理解：

- **Registry** 解決「canonical source of truth」問題
- **Adapter** 解決「跨 CLI 異質性」問題
- **Operations** 解決「誰動了我的設定」的治理問題

大多數同類嘗試（dotfiles manager、tool config syncer）只處理第一層或第二層，UniText 同時處理三層且有明確邊界，這是正確的架構決策。

### 1.2 治理哲學的嚴謹度（★★★★★）

「No Silent Changes」政策是本專案最具差異化的設計決策：

- **Explicit triggers only**（bootstrap, sync, adopt, repair）——拒絕背景自動同步
- **Dry-run before mutation**——每次寫入前先預覽
- **Backup before any mutation**——14 組 ops/history 紀錄證明這不只是紙上談兵
- **Audit trail**——每個操作都有時間戳記錄

在 AI 工具快速演進的時代，「不要偷偷幫我改東西」是一個極具防禦價值的治理立場。

### 1.3 文件品質與結構化程度（★★★★☆）

6 份核心文件（README / INDEX / VISION / RESOURCE_SPEC / OPERATIONS / PROJECT_MODES）形成了一套完整的「專案契約」：

- 人類讀者可以從 README → INDEX 進入
- AI agent 可以從 INDEX 的 catalog 結構開始 discovery
- 技術決策有 VISION 背書，資源規格有 RESOURCE_SPEC 約束
- 操作安全有 OPERATIONS 護欄，模式切換有 PROJECT_MODES 區分

這個文件體系的完整度，已經達到可作為 template base 對外發布的水準（前提是解決下面提到的混雜問題）。

### 1.4 操作歷史的真實性（★★★★☆）

`ops/history/` 中存有 14 組帶時間戳的操作記錄，涵蓋 backup、drift、inventory、unify、set_setting 五種操作類型。`ops/inventory.latest.json` 證實了對 15 個 CLI/runtime 的實際偵測能力。這不是概念驗證，是有實際執行痕跡的治理實踐。

### 1.5 正確的自我認知（★★★★☆）

`PROJECT_STATUS_REPORT_2026-03-23.md` 對專案的自我評估是「Phase 1.5——基礎架構已成形、核心資源納管尚未完成」。這個判斷**精確而誠實**，沒有過度美化或刻意低估。

---

## 二、目標與流程評估

### 2.1 目標合理性評估

| 目標面向 | 評估 | 說明 |
|---------|------|------|
| 問題定義 | ✅ 合理 | 跨 AI CLI 的資源碎片化確實是真實痛點，尤其隨 Claude Code / Codex / Gemini CLI 同時活躍 |
| 解決方案定位 | ✅ 正確 | Text-native + registry-first 的路線選擇合理——純文本是跨工具最大公約數 |
| 涵蓋範圍 | ⚠️ 需要注意 | skills + mcp + agents + workflow 四類資源的野心很大，但目前僅 2/4 有 registry root |
| 成功標準 | ❌ 缺失 | 沒有明確的「什麼算做完了」的量化指標 |

**關鍵缺口：缺少可量化的成功標準（Definition of Done）**

目前所有文件都在描述「UniText 應該是什麼樣子」，但沒有明確定義：
- Phase 1 完成 = 什麼？（例如：skills 100% onboarded + 至少 2 個 CLI 驗證 delivery 成功）
- Phase 2 完成 = 什麼？（例如：agents registry 上線 + template 發布）
- MVP = 什麼？（最小可向外部展示的版本包含什麼？）

> **建議**：在根目錄新增 `MILESTONES.md`，定義 3-5 個階段的量化完成條件。每個 milestone 包含：可交付物清單、驗收條件、預估時間。
>
> **如何開始**：以目前 PROJECT_STATUS_REPORT 的「尚未達成里程碑」為基礎，為每一項附上具體數字（例如「27 個 skills 中至少 20 個完成 adoption」而非「skills 正式納管」）。

### 2.2 流程缺口分析

**SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY** 這個 adoption flow 設計得很好，但有三個流程缺口：

#### 缺口 A：SCAN 沒有工具支撐

- OPERATIONS.md 定義了 adoption flow，但目前唯一的自動化腳本是 `sync-skills.ps1`（對應 DELIVER 階段的 mirror 模式）
- SCAN 階段沒有對應的腳本或工具來「掃描哪些資源需要被 adopt」
- REVIEW 階段沒有對應的 checklist 或工具來「審核資源是否符合 RESOURCE_SPEC」

> **建議**：為 adoption flow 的每個階段建立最小工具（即使只是手動 checklist 的 markdown 文件）。
>
> **如何開始**：建立 `local/scripts/scan-resources.ps1`，功能為掃描 backup 中的 skills 目錄，列出每個 skill 的名稱、是否有 SKILL.md、是否符合 RESOURCE_SPEC 的必要欄位。

#### 缺口 B：VERIFY 缺乏定義

- Adoption flow 以 VERIFY 結尾，但沒有定義「verify 什麼」
- 是驗證檔案存在？驗證 symlink 有效？驗證 CLI 實際讀取成功？

> **建議**：在 OPERATIONS.md 補充 VERIFY 階段的驗證清單，至少包含：(1) 檔案存在性確認 (2) 路徑解析正確性 (3) 目標 CLI 實際載入測試。
>
> **如何開始**：先針對已有 symlink 的 skills delivery 撰寫一個 `verify-delivery.ps1`，確認 `~/.claude/skills`、`~/.gemini/skills`、`~/.agents/skills` 的 symlink target 是否指向正確位置、內容是否存在。

#### 缺口 C：從 adoption 到持續維護的生命週期

- 目前只定義了「怎麼把東西放進來」（adoption），沒有定義「放進來之後怎麼維護」
- 資源的 deprecation / archive / update 流程是空白的
- RESOURCE_SPEC 定義了 status 欄位（draft / active / deprecated / archived）但沒有狀態轉換的觸發條件

> **建議**：在 RESOURCE_SPEC.md 補充 lifecycle transition rules，定義每個狀態轉換的觸發條件和操作步驟。
>
> **如何開始**：先處理最簡單的 case——為「archived → active」定義流程（這正好是 27 個 skills 當前需要走的路徑）。

---

## 三、技術選擇評估

### 3.1 核心技術堆疊評估

| 技術選擇 | 評估 | 理由 |
|---------|------|------|
| 純文本（Markdown + JSON）作為資源格式 | ✅ 優秀 | 最大化跨工具相容性，AI agent 友好，版本控制友好 |
| PowerShell 作為自動化語言 | ⚠️ 可接受但有限制 | Windows 環境合理，但限制了跨平台潛力 |
| Robocopy /MIR 作為同步機制 | ⚠️ 簡陋但務實 | 能用，但缺乏增量同步、衝突檢測、回滾能力 |
| Symlink 作為主要 delivery 模式 | ✅ 正確 | 零冗餘，修改即時生效，符合 native-config > symlink > mirror > pointer 的優先序 |
| SHA256 baseline 作為 drift 偵測機制 | ✅ 好主意 | 輕量、可靠、可離線運作 |
| 扁平目錄結構（registry/{type}/{id}/） | ✅ 合理 | 簡單可預測，AI agent 容易 discover |

### 3.2 關鍵技術權衡

#### 權衡 1：Symlink vs. Copy（Mirror）

目前 inventory 顯示三條 symlink 已建立：
```
~/.claude/skills → C:\Dev\UniText\skills
~/.gemini/skills → C:\Dev\UniText\skills
~/.agents/skills → C:\Dev\UniText\skills
```

**問題**：這些 symlink 指向 `C:\Dev\UniText\skills`（不存在的舊路徑），而非 `C:\Dev\UniText\registry\skills`（架構定義的 canonical 路徑）。這是一個**架構宣稱與實際部署不一致**的問題。

> **建議**：在 registry/skills/ 正式建立後，更新所有 symlink target 到 `C:\Dev\UniText\registry\skills`。同時在 `sync-skills.ps1` 中修改 `$source` 路徑。
>
> **如何開始**：先不要動 symlink。先完成 registry/skills/ 的建立和 skill 遷移，確認內容正確後再一次性更新 symlink。在此之前，考慮在根目錄建立一個臨時 `skills → registry/skills` 的內部 junction 作為過渡。

#### 權衡 2：集中式 registry vs. 分散式 delivery

UniText 選擇了「一個 canonical source + 多個 adapter delivery」的架構，這是正確的。但需要注意：

- 如果 canonical source 壞了（磁碟損壞、誤刪），所有 CLI 同時失去資源
- 目前沒有 Git 作為安全網，唯一的恢復手段是 `ops/history/` 中的 backup

> **建議**：這強化了「必須盡快建立 Git 版本控制」的緊迫性（詳見風險分析）。

#### 權衡 3：PowerShell 的跨平台限制

目前所有自動化都是 PowerShell（.ps1），這在 Windows 環境下完全合理。但如果 UniText 未來要作為 template 發布給其他使用者：

- macOS / Linux 使用者無法直接使用這些腳本
- 即使 PowerShell Core 跨平台，robocopy 是 Windows 專屬

> **建議**：短期不需要改變（先解決更緊迫的問題），但在 VISION.md 的 adapter 層設計中，應預留「adapter 腳本可以有多個平台實現」的位置。
>
> **如何開始**：在 `local/scripts/` 中建立一個 `README.md`，說明目前的腳本是 Windows-only 參考實現，並記錄 POSIX 環境的等效命令（例如 rsync 替代 robocopy）。

---

## 四、實施方案評估

### 4.1 架構設計健全度

| 架構層次 | 設計健全度 | 實際落地度 | 差距 |
|---------|----------|----------|------|
| 核心概念模型 | ★★★★★ | ★★★★★ | 無——文件已完整表達 |
| Registry 結構 | ★★★★☆ | ★★☆☆☆ | 大——2/4 root 存在，0/27+ 資源 onboarded |
| Adapter 層 | ★★★★☆ | ★☆☆☆☆ | 極大——只有 1 個 sync-skills.ps1 |
| Operations 治理 | ★★★★★ | ★★★☆☆ | 中——有歷史紀錄但工具不完整 |
| 自動化管線 | ★★★☆☆ | ★☆☆☆☆ | 極大——6 步 adoption flow 只有 1 步有腳本 |

**核心發現：設計與實施之間存在「完成度倒掛」**

文件完成度約 90%，但實際內容落地度約 15-20%。這是典型的「架構過度設計、實施不足」模式——不是說架構設計錯了，而是投入在設計文件上的精力與投入在實際執行上的精力嚴重不成比例。

> **建議**：暫停所有文件增修，進入「執行衝刺」模式。接下來的 2-4 週，目標應該是「把已設計好的東西做出來」而非「設計更多東西」。
>
> **如何開始**：設定一個 2 週的 time box，唯一目標是：建立 `registry/skills/`，遷入 10 個最常用的 skills，更新 INDEX.md 的 catalog entries，確認至少 1 個 CLI 的 delivery 可正常運作。

### 4.2 資源配置評估

基於以下證據推斷此為**單人維護專案**：
- inventory 全部指向同一使用者 `miles`
- ops history 中只見單一操作者的軌跡
- 沒有 CONTRIBUTING.md 或任何協作相關文件
- 沒有 Git / PR / issue 的協作流程

**單人專案的資源配置風險**：

- 所有知識集中在一個人腦中
- 設計決策沒有第二人挑戰
- 「做完沒人知道」的動力衰減風險
- Bus factor = 1

> **建議**：如果短期內不會有第二位維護者，至少做到「如果兩週後的自己忘了現在在做什麼，能快速 ramp up」。具體做法是：在每次操作後更新一個簡單的 `CHANGELOG.md` 或 `local/docs/JOURNAL.md`。
>
> **如何開始**：在 `local/docs/` 下建立 `JOURNAL.md`，格式為 `## YYYY-MM-DD` + 「今天做了什麼」。不需要完美，只需要持續。

### 4.3 品質保證評估

**目前的品質保證機制**：
- ✅ SHA256 baseline drift 偵測
- ✅ Backup before mutation 政策
- ✅ 14 組操作歷史紀錄
- ❌ 沒有自動化測試
- ❌ 沒有 CI/CD
- ❌ 沒有 linting 或 schema validation
- ❌ 沒有 RESOURCE_SPEC 的 metadata validator

> **建議**：建立一個最小的「健康檢查腳本」，定期驗證 registry 的完整性。
>
> **如何開始**：建立 `local/scripts/health-check.ps1`，功能包含：(1) 檢查 registry 下每個資源是否有必要的 metadata 欄位 (2) 檢查 symlink 是否有效 (3) 檢查 ops/baseline.json 的 hash 是否與當前檔案一致。

---

## 五、風險與應急分析

### 5.1 外部環境假設

本風險分析基於以下明確假設：

| 假設 | 依據 | 影響如果假設錯誤 |
|-----|------|----------------|
| 單人維護，無團隊協作 | inventory 中只見單一使用者 | 如果有團隊，某些風險降級 |
| 主要在 Windows 環境運作 | 所有路徑為 Windows 格式 | 如果跨平台，PowerShell 風險升級 |
| AI CLI 生態持續快速迭代 | 實際市場趨勢 | 如果穩定，維護壓力降低 |
| 專案最終目標是可供他人使用的 template | PROJECT_MODES.md 定義了 template 模式 | 如果純個人使用，某些清理需求降級 |
| 目前不在任何版本控制系統下 | 驗證確認非 Git repo | 這是事實，非假設 |
| 無外部依賴（不依賴 SaaS / API / 雲端服務） | 純本地文本架構 | 降低了外部依賴風險 |

### 5.2 風險清單（按優先序排列）

---

#### 🔴 CRITICAL-1：非 Git 環境的不可逆損失風險

**風險描述**：目前 `C:\Dev\UniText` 不在任何版本控制下。所有的「復原能力」僅依賴 `ops/history/` 中的手動備份和 SHA256 baseline。一旦發生以下任何情境，可能導致不可逆的資源遺失或無法追溯的狀態損壞。

**觸發條件**：
- 誤操作刪除/覆寫 registry 內容（rm -rf、robocopy /MIR 到錯誤方向）
- 磁碟損壞或 OS 重裝
- AI agent 操作失誤（Claude Code / Codex 在專案內執行破壞性操作）
- 兩次操作之間沒有觸發 backup，而中間發生了錯誤

**影響評估**：
- **最壞情況**：全部 canonical resource 遺失，無 commit history 可恢復
- **可能情況**：某次操作的中間狀態無法回溯，only know "before" and "after" but not "what changed"
- **連帶影響**：沒有 diff 能力 → 無法進行有效的 code review → 品質保證缺口

**應急策略**：

```
立即行動（今天就做）：
1. cd C:\Dev\UniText
2. git init
3. 建立合理的 .gitignore（排除 ops/history/ 中的大型備份、.bak_* 目錄）
4. git add -A && git commit -m "Initial commit: UniText Phase 1.5 baseline"
5. 設定 remote（GitHub private repo 或其他）並 push

.gitignore 建議內容：
- ops/history/backup_*/    # 大型歷史備份
- .bak_*/                   # 暫存備份
- recovered_*/              # 恢復暫存
- backup/                   # 舊備份
```

**為什麼現在就做**：
- 不需要先「清理乾淨再 commit」——Git 允許後續重組
- 每天的延遲都是在增加不可逆損失的暴露視窗
- 初始 commit 即使包含了「不完美的狀態」也比「沒有任何快照」好無限倍

---

#### 🔴 CRITICAL-2：架構宣稱與實際內容的信任差距持續擴大

**風險描述**：核心文件描述了一個完整的 registry-first 架構，但實際 registry 內容嚴重不足。時間越長，這個差距越大，最終可能導致整個架構設計失去可信度——包括對作者自己和對未來使用者。

**量化差距**：

| 資源類型 | 文件宣稱 | 實際狀態 | 差距 |
|---------|---------|---------|------|
| skills | 26-27 已歸檔待 adoption | 0 in registry（目錄不存在） | 100% |
| mcp | claude-project-mcp-seed 已建立 | `{"mcpServers": {}}` 空物件 | 名存實亡 |
| agents | Planned | 目錄不存在 | N/A |
| workflow | claude-plans 已建立 | 目錄存在但為 Claude-specific | 部分 |

**觸發條件**：
- 超過 1 個月沒有 canonical content 被正式 adopt
- 新讀者（人或 AI）閱讀 README 後期望在 registry/ 找到 skills，卻發現空目錄
- 作者本人開始質疑「花這麼多時間設計架構到底有沒有用」

**應急策略**：

```
2 週內執行的「最小可信度修復」：

Week 1：Skills 首批遷入
1. mkdir registry\skills
2. 從 .bak_20260315_00\skills.bak.20260228_215107\ 選擇 5 個最常用的 skills
   （建議優先順序：frontend-design, pdf, docx, xlsx, mcp-builder）
3. 為每個建立 registry\skills\{id}\SKILL.md 符合 RESOURCE_SPEC
4. 更新 INDEX.md 新增 5 個 catalog entries
5. git commit

Week 2：Symlink 修正 + Delivery 驗證
1. 更新 symlink targets：C:\Dev\UniText\skills → C:\Dev\UniText\registry\skills
2. 修改 sync-skills.ps1 的 $source 路徑
3. 手動驗證 Claude Code 是否能讀取 skill
4. git commit
```

---

#### 🔴 CRITICAL-3：27 個 Skills 停滯瓶頸——adoption 成本過高

**風險描述**：27 個 skills 自 2026-02-28 歸檔以來已停滯近一個月。問題不是「不知道要做什麼」（adoption flow 已設計好），而是**每個 skill 的 adoption 成本太高**——需要手動建立目錄、編寫 metadata、驗證格式、更新 catalog。27 個 skills × 手動操作 = 巨大的行動門檻。

**瓶頸分析**：

```
目前每個 skill 的 adoption 需要：
1. 建立 registry/skills/{id}/ 目錄
2. 複製 skill 內容
3. 撰寫/更新 SKILL.md（符合 RESOURCE_SPEC）
4. 補充 metadata（id, type, canonical_location, status）
5. 更新 INDEX.md catalog entry
6. （可選）驗證 delivery

以每個 skill 20-30 分鐘計算，27 個 = 9-13.5 小時的純手動作業。
這就是為什麼一個月過去了還是 0/27。
```

**應急策略：用自動化打破瓶頸**

```powershell
# 建議建立：local/scripts/batch-adopt-skills.ps1
# 核心邏輯：
# 1. 掃描 backup 中的 skills 目錄
# 2. 為每個 skill 自動建立 registry/skills/{id}/ 目錄
# 3. 複製內容
# 4. 從現有 SKILL.md 提取 metadata，自動生成符合 RESOURCE_SPEC 的 header
# 5. 輸出需要人工審核的項目清單

# 第一步：先手動做 2-3 個，建立 pattern
# 第二步：將重複步驟腳本化
# 第三步：批次處理剩餘的 24-25 個
```

**為什麼這是 critical**：如果 adoption 瓶頸不解決，無論架構設計多完美，registry 永遠是空的——專案的核心價值主張「共享 canonical resources」就永遠停留在概念層。

---

#### 🟡 HIGH-1：更名遺留債務（AI_UNIFIED → UniText）的持續污染

**風險描述**：專案從 `AI_UNIFIED` 更名為 `UniText`，但舊名稱的殘留遍布整個專案：

**量化影響**：
- `ops/inventory.latest.json` 中至少 1 處
- `codex.config.toml` 備份中有指向 `C:\Dev\AI_UNIFIED\` 的路徑
- `.bak_20260315_00/template_base/` 中的 6 份核心文件都有殘留
- Symlink 指向 `C:\Dev\UniText\skills`（舊架構路徑，非 registry 路徑）

**觸發條件**：
- AI agent 讀取到 `AI_UNIFIED` 路徑並嘗試存取 → 路徑不存在 → 操作失敗
- 新使用者（或未來的自己）困惑於兩個名稱的關係
- 對外發布 template 時殘留的舊路徑暴露個人開發歷史

**應急策略**：

```
分三層清理（不要一次全做）：

Layer 1 - 活躍文件（立即）：
- 掃描根目錄 6 份核心文件，確認已無 AI_UNIFIED 引用 ✅（已確認主文件已清理）
- 清理 ops/inventory.latest.json 中的殘留
- 更新 local/docs/PATH_MAP.md

Layer 2 - 備份文件（低優先）：
- .bak_20260315_00/template_base/ 中的舊文件
- recovered_20260318_165117/ 中的副本
- 這些可以在 Git 初始化後透過 .gitignore 排除

Layer 3 - 歷史檔案（不處理）：
- ops/history/ 中的歷史快照應保留原樣——它們記錄的是「那個時間點的狀態」
- 改動歷史檔案會破壞 audit trail 的完整性
```

---

#### 🟡 HIGH-2：sync-skills.ps1 的單點脆弱性

**風險描述**：目前整個專案只有一個自動化腳本 `sync-skills.ps1`，它是唯一的 adapter 實現。而這個腳本有多個問題：

```powershell
$source = "C:\Dev\UniText\skills"  # ← 硬編碼路徑，且不是 registry 路徑
$targets = @(
  "$HOME\.claude\skills",     # ← 只支援 3 個 CLI
  "$HOME\.gemini\skills",
  "$HOME\.agents\skills"
)
# 使用 robocopy /MIR ← 鏡像模式會刪除目標端多出的檔案，潛在破壞性操作
```

**問題清單**：
1. 硬編碼的 source 路徑指向不存在的 `C:\Dev\UniText\skills`（而非 `registry/skills`）
2. 只覆蓋 3 個 CLI（缺少 Codex、VS Code、Windsurf）
3. 使用 `robocopy /MIR`（鏡像模式）意味著目標端如果有額外檔案會被**刪除**
4. 沒有 dry-run 選項——這違反了 OPERATIONS.md 的「Dry-Run First」原則
5. 沒有 backup 步驟——這違反了「Backup Before Mutation」原則
6. 沒有錯誤報告——只有 `Write-Output "skills synced"` 不管是否真的成功

**應急策略**：

```powershell
# 改進版 sync-skills.ps1 的核心邏輯（草稿）：
param(
    [switch]$DryRun,          # 支援 dry-run
    [switch]$SkipBackup       # 預設做 backup
)

$source = "C:\Dev\UniText\registry\skills"  # ← 修正為 registry 路徑
$targets = @(
    "$HOME\.claude\skills",
    "$HOME\.gemini\skills",
    "$HOME\.agents\skills",
    "$HOME\.codex\skills"     # ← 補上缺失的 CLI
)

# 加入 dry-run 支援
if ($DryRun) {
    robocopy $source $t /MIR /L /R:1 /W:1  # /L = list only
} else {
    # backup before mutation
    # robocopy $source $t /MIR ...
}
```

---

#### 🟡 HIGH-3：跨 CLI 生態系統快速演進的追趕壓力

**風險描述**：inventory 偵測到的 CLI 版本：
- Claude Code 2.1.63
- Codex CLI 0.106.0
- Gemini CLI 0.31.0
- VS Code 1.109.5

這些工具的更新頻率是**每週到每月**，每次更新都可能改變：
- Skills 目錄的讀取路徑
- MCP server 的設定格式
- Agent instructions 的 schema

**觸發條件**：
- 任一 CLI 的 major update 改變了 skills/MCP 的存取路徑或格式
- 例如：Claude Code 未來版本不再從 `~/.claude/skills` 讀取 skills
- 例如：Gemini CLI 改用不同的 MCP 設定格式

**應急策略**：

```
1. 建立「CLI 版本追蹤表」（在 local/docs/ 或 ops/ 中）：
   - 記錄每個 CLI 的當前版本
   - 記錄 UniText 依賴的具體行為（哪個路徑、哪個格式）
   - 記錄最後驗證日期

2. 設定季度「相容性檢查」排程（即使是 calendar reminder）：
   - 執行 inventory 掃描
   - 對比版本號是否有 major change
   - 驗證 delivery 路徑是否仍然有效

3. 在 OPERATIONS.md 中新增「Breaking Change Response Protocol」：
   - 哪些 CLI 行為改變構成 breaking change
   - 發現後的回應流程（freeze delivery → assess impact → adapt → verify）

如何開始：
先建一個 local/docs/CLI_COMPAT_MATRIX.md，列出每個 CLI 的版本、
UniText 依賴的行為、最後驗證時間。每次升級 CLI 時更新一次。
```

---

#### 🟡 HIGH-4：根目錄混雜的模式混線風險

**風險描述**：PROJECT_MODES.md 明確定義了 Template 模式不應包含的內容，但目前根目錄同時存在：

| 應屬於 Template | 應屬於 Local Dev Only | 目前狀態 |
|----------------|----------------------|---------|
| README.md | backup/ | ❌ 混在一起 |
| INDEX.md | recovered_20260318_165117/ | ❌ 混在一起 |
| VISION.md | .bak_20260315_00/ | ❌ 混在一起 |
| registry/ | ops/history/ | ❌ 混在一起 |

**應急策略**：

```
Git 初始化後，透過 .gitignore 做第一層分離：

# .gitignore
backup/
recovered_*/
.bak_*/
ops/history/backup_*/

這不需要移動任何檔案，只是讓 Git 「看不到」這些開發專用產物。
Template 發布時，直接 git archive 就會是乾淨的版本。
```

---

#### 🟠 MEDIUM-1：從 Local Development 到 Template 發布的路徑不清

**風險描述**：PROJECT_MODES.md 定義了兩種模式，但沒有具體的「如何從 Local Dev 產生 Template 發布版」的操作步驟。

**應急策略**：
- 在 Git 化之後，利用 `.gitignore` + `git archive` 或專門的 `export-template.ps1` 腳本來產生乾淨的 template 版本
- 不需要現在做，但應在 MILESTONES.md 中記錄為 Phase 3 目標

---

#### 🟠 MEDIUM-2：local/docs/authoring/ 與根目錄文件的重複維護成本

**風險描述**：`local/docs/authoring/` 中存有 INDEX.md、VISION.md、OPERATIONS.md、PROJECT_MODES.md、RESOURCE_SPEC.md 的副本，與根目錄版本存在潛在的不一致風險。

**應急策略**：
- 確認哪一份是 canonical（根據 VISION 的 registry-first 原則，根目錄版本應為 canonical）
- 將 `local/docs/authoring/` 改為 symlink 或直接刪除，只保留根目錄版本
- **如何開始**：比較兩組文件的差異，確認是否有獨特內容需要合併回根目錄版本

---

#### 🟠 MEDIUM-3：inventory.latest.json 中的不一致數據

**風險描述**：
- 三條 symlink 的 target 是 `C:\Dev\UniText\skills`（非 registry 路徑）
- WSL 版本字串包含 Unicode null bytes（`W\u0000S\u0000L\u0000`）——encoding 處理問題
- Codex skills 是普通目錄（非 symlink），其他三個 CLI 是 symlink——delivery 模式不一致

**應急策略**：
- 在 skills 正式遷入 registry/ 後，重新執行 inventory 掃描
- 修正 inventory 腳本的 encoding 處理（WSL 版本輸出為 UTF-16，需轉換）

---

### 5.3 風險矩陣總覽

| 優先級 | 風險 ID | 風險名稱 | 發生機率 | 影響程度 | 建議回應時間 |
|-------|---------|---------|---------|---------|------------|
| 🔴 | CRITICAL-1 | 非 Git 不可逆損失 | 中 | 災難性 | **今天** |
| 🔴 | CRITICAL-2 | 架構-內容信任差距 | 已發生 | 高 | **本週** |
| 🔴 | CRITICAL-3 | Skills adoption 瓶頸 | 已發生 | 高 | **2 週內** |
| 🟡 | HIGH-1 | 更名遺留債務 | 已發生 | 中高 | 2-4 週 |
| 🟡 | HIGH-2 | 腳本單點脆弱性 | 高 | 中 | 2-4 週 |
| 🟡 | HIGH-3 | CLI 生態追趕壓力 | 高 | 中高 | 持續 |
| 🟡 | HIGH-4 | 目錄模式混線 | 已發生 | 中 | Git 化後處理 |
| 🟠 | MEDIUM-1 | Template 發布路徑不清 | 中 | 低 | Phase 3 |
| 🟠 | MEDIUM-2 | 文件重複維護 | 中 | 低 | 隨 adoption 一起處理 |
| 🟠 | MEDIUM-3 | Inventory 數據不一致 | 已發生 | 低 | 重新掃描時修正 |

---

## 六、整體建議

### 6.1 Top 5 強化行動項

#### 行動 1：立即 Git 初始化（今天）

**做什麼**：`git init` + 首次 commit + push 到 remote

**為什麼**：這是所有後續改善的基礎。沒有版本控制，任何操作都有不可逆風險。備份機制（ops/history）是有用的，但無法取代 Git 的原子化 commit、差異比對、和分支管理能力。

**如何開始**：
```bash
cd C:\Dev\UniText
git init
# 建立 .gitignore（見上文）
git add -A
git commit -m "Initial commit: UniText Phase 1.5 - architecture complete, resource adoption pending"
# 建議推到 GitHub private repo 作為 off-site backup
```

#### 行動 2：執行首批 Skills 遷入（本週）

**做什麼**：建立 `registry/skills/`，遷入 5 個最常用的 skills 並更新 catalog

**為什麼**：打破「27 skills 停滯一個月」的僵局。5 個 skills 的成功遷入會建立 pattern 和信心，讓後續的 22 個更容易處理。

**如何開始**：
```
1. mkdir registry\skills
2. 選擇 5 個：frontend-design, pdf, docx, xlsx, mcp-builder
3. 從 .bak_20260315_00\skills.bak.20260228_215107\ 複製
4. 為每個建立符合 RESOURCE_SPEC 的 metadata header
5. 更新 INDEX.md
6. git commit -m "feat: adopt first 5 skills into canonical registry"
```

#### 行動 3：修正 sync-skills.ps1（與行動 2 一起）

**做什麼**：更新 source 路徑、加入 dry-run、加入 backup、加入基本錯誤處理

**為什麼**：目前唯一的自動化腳本指向錯誤路徑且違反自己的治理原則。修正後可以作為 adapter 層的 reference implementation。

**如何開始**：見 HIGH-2 中的改進版草稿。

#### 行動 4：建立 batch-adopt-skills 腳本（2 週內）

**做什麼**：自動化 skill adoption 的重複步驟（建目錄、複製內容、生成 metadata 模板）

**為什麼**：手動做 27 個 skills 的 adoption 需要 9-13 小時。腳本化可以降到 1-2 小時（腳本開發 + 人工審核）。

**如何開始**：先手動做完行動 2 的 5 個 skills，記錄每個步驟。然後將重複步驟寫成腳本。

#### 行動 5：建立成功標準與里程碑文件（2 週內）

**做什麼**：建立 `MILESTONES.md`，定義 Phase 1 / Phase 2 / Phase 3 的量化完成條件

**為什麼**：沒有 Definition of Done，就永遠無法知道「什麼時候可以停下來」。明確的里程碑也是抵抗功能蔓延和設計過度的護欄。

**如何開始**：
```markdown
# MILESTONES.md

## Phase 1: Skills Canonical Registry Online
- [ ] registry/skills/ 目錄存在
- [ ] 至少 20/27 skills 完成 adoption
- [ ] INDEX.md 包含所有 adopted skills 的 catalog entries
- [ ] 至少 2 個 CLI 的 delivery 驗證通過
- [ ] sync-skills.ps1 指向正確路徑且支援 dry-run

## Phase 2: Full Resource Registry
- [ ] registry/agents/ 至少 1 個 entry
- [ ] registry/mcp/ 至少 1 個非空 entry
- [ ] VERIFY 流程有對應的腳本或 checklist
- [ ] 所有 AI_UNIFIED 殘留在活躍文件中清除

## Phase 3: Template Release Ready
- [ ] .gitignore 正確排除 local-only 產物
- [ ] Template export 腳本或流程 documented
- [ ] README 適合首次讀者（非作者本人）
```

### 6.2 啟動前應做的應急準備

| 準備項目 | 為什麼 | 預估時間 |
|---------|--------|---------|
| Git init + 首次 commit | 建立安全網再做任何修改 | 15 分鐘 |
| 確認 .bak 中的 skills 完整性 | 避免遷移到一半發現源檔案有問題 | 30 分鐘 |
| 記錄當前 symlink 狀態 | 方便日後比對修改前後 | 10 分鐘 |
| 備份 ops/inventory.latest.json | 修改前保留當前 baseline | 5 分鐘 |

### 6.3 執行過程中的監控點

| 監控點 | 頻率 | 方法 | 警報條件 |
|-------|------|------|---------|
| Registry 內容增長率 | 每週 | 計算 registry/ 下的目錄數 | 連續 2 週無增長 |
| Symlink 有效性 | 每次 CLI 更新後 | 手動或腳本驗證 | 任一 symlink 失效 |
| AI_UNIFIED 殘留數量 | 每次清理後 | `grep -r "AI_UNIFIED"` | 活躍文件中仍有殘留 |
| CLI 版本變動 | 每月 | 執行 inventory 掃描 | Major version 變更 |
| 設計-實施差距 | 每 2 週 | 對照 README 宣稱與 registry 實際 | 差距不收斂或擴大 |
| commit 頻率 | 每週 | `git log --oneline` | 超過 1 週沒有 commit |

---

## 結語

UniText 是一個**理念正確、設計成熟、但執行嚴重落後**的專案。它的核心價值主張——「跨 AI CLI 的 registry-first 共享資源中心」——在 2026 年的工具生態中確實是一個真實且有價值的需求。

六份核心文件構成了一套完整、嚴謹、且具有前瞻性的架構契約。這個設計品質是本專案最大的資產。

但設計不等於產品。一個空的 registry 配上一套完美的 spec，其實際價值接近零。

**當務之急不是設計更多、不是寫更多文件、不是規劃更遠的未來——而是把已經設計好的東西做出來。**

具體來說：
1. **今天**：`git init`
2. **本週**：5 個 skills 進入 registry
3. **2 週內**：批次工具 + 20 個 skills 進入 registry
4. **1 個月內**：所有 symlink 指向正確路徑、delivery 驗證通過

如果這四步完成，UniText 就會從「一個設計精美的空盒子」變成「一個能用且在用的 canonical resource hub」。

> *「The best architecture is the one that has actual content behind it.」*
