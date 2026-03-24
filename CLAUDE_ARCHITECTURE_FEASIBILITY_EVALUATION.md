# UniText 在 Claude 預設架構下的可行性評估報告

> 評估日期：2026-03-24
> 評估範圍：UniText 作為 Claude Code CLI 與其他 AI CLI 的 shared resource hub 的架構相容性

---

## 執行摘要

**結論：高度可行 ✅**

UniText 的設計理念與 Claude 的預設架構高度契合。其 text-native、registry-first 的方法不僅相容，而且可以說是為 Claude 這類 AI 代理量身打造的。以下是詳細分析。

---

## 1. 架構相容性分析

### 1.1 與 Claude 技術能力的匹配

| UniText 特性 | Claude 能力 | 相容程度 |
|-------------|-------------|---------|
| **純文本格式（Markdown/JSON）** | Claude 擅長處理純文本、Markdown、JSON | ✅ 完美匹配 |
| **Registry-first 設計** | Claude 可讀取、解析、導覽目錄結構 | ✅ 完美匹配 |
| **Discovery via INDEX.md** | Claude 擅長閱讀文檔作為入口點 | ✅ 完美匹配 |
| **RESOURCE_SPEC.md 作為契約** | Claude 可理解並執行結構化規格 | ✅ 完美匹配 |
| **OPERATIONS.md 定義操作** | Claude 可按規則執行工作流程 | ✅ 完美匹配 |
| **邏輯路徑（vs 絕對路徑）** | Claude 可處理抽象路徑映射 | ✅ 完美匹配 |

### 1.2 Claude 作為 Consumer 的角色

UniText 在 VISION.md 中明確定義：

> *"AI 是重要的 consumer 與協作者，但不是唯一可靠的整合機制"*

這與 Claude 的能力和限制完美契合：

- **Claude 可做到**：讀取 registry、理解規格、執行工作流程、產生報告
- **Claude 不適合**：持久化保證、跨 session 狀態管理、自動部署（需要外部工具）

UniText 的 adapter/operations control plane 正好補足了 Claude 不擅長的部分。

---

## 2. 關鍵優勢

### 2.1 AI-First Discovery 設計

```
INDEX.md → VISION.md → RESOURCE_SPEC.md → OPERATIONS.md
```

這個閱讀順序為 AI 代理提供了清晰的學習路徑，Claude 可以：

1. 從 `INDEX.md` 快速了解有哪些資源
2. 用 `RESOURCE_SPEC.md` 理解 metadata 規範
3. 按 `OPERATIONS.md` 執行標準操作

### 2.2 明確的安全邊界

UniText 的治理規則與 Claude 的安全操作需求一致：

| UniText 規則 | Claude 操作考量 | 結果 |
|-------------|----------------|------|
| **Dry-run first** | Claude 可在執行前預覽變更 | ✅ 降低風險 |
| **Backup before mutation** | Claude 操作有回復點 | ✅ 可逆操作 |
| **Explicit triggers only** | Claude 不會意外觸發操作 | ✅ 避免副作用 |
| **No silent canonicalization** | 衝突時停止讓人類決策 | ✅ 人類在迴圈中 |

### 2.3 跨 CLI 標準化

UniText 支援多個 AI CLI：

| CLI | 支援狀態 | 對 Claude 的意義 |
|-----|---------|-----------------|
| Claude Code | ✅ 支援 | 主要目標 |
| Codex | ✅ 支援 | 可共享 skills |
| Gemini CLI | ✅ 支援 | 可共享 skills |
| GitHub CLI | ✅ 支援 | 可整合工作流程 |

這意味著 Claude 使用者可以透過 UniText 與其他工具共享資源。

---

## 3. 潛在挑戰與緩解方案

### 3.1 Session 狀態限制

**挑戰**：Claude 沒有跨 session 的持久記憶

**緩解方案**：
- UniText 的所有狀態都存在於檔案系統（`ops/`）
- Claude 每次執行都可以重新讀取 `ops/inventory.latest.json`
- Audit trail 在 `ops/history/` 提供操作歷史

**評估**：✅ 已解決 — 狀態外部化到檔案系統

### 3.2 複雜操作的執行

**挑戰**：某些操作需要多步驟、跨工具的協調

**緩解方案**：
- `bootstrap.py` 和其他腳本已提供自動化
- Claude 可調用這些腳本而非手動執行每個步驟
- 支援 `--dry-run` 模式讓 Claude 可安全預覽

**評估**：✅ 已解決 — 腳本封裝了複雜操作

### 3.3 平台差異處理

**挑戰**：Windows/macOS/Linux 有不同的路徑和權限模型

**緩解方案**：
- UniText 使用邏輯路徑作為契約
- `local/` overlay 處理平台特定映射
- `bootstrap.py` 是跨平台實作

**評估**：✅ 已解決 — 架構已考慮跨平台需求

### 3.4 MCP 整合

**挑戰**：MCP server 需要正確設定才能運作

**緩解方案**：
- `registry/mcp/claude-project-mcp-seed/` 提供參考實作
- `bootstrap.py` 自動寫入 `.mcp.json`
- 有明確的 `definition.json` 作為規格

**評估**：✅ 已解決 — 提供了可運行的 baseline

---

## 4. Claude 工作流程建議

### 4.1 初始化流程

當 Claude 第一次接觸 UniText 專案時，建議的操作順序：

```bash
# 1. 讀取 discovery 入口
view INDEX.md

# 2. 了解架構原則
view VISION.md

# 3. 驗證現有狀態
python local/scripts/verify-bootstrap.py

# 4. 如需初始化，先 dry-run
python local/scripts/bootstrap.py --dry-run

# 5. 確認後執行
python local/scripts/bootstrap.py --force
```

### 4.2 日常操作流程

| 任務 | Claude 操作 |
|------|------------|
| 新增 skill | 在 `registry/skills/` 建立目錄和 `SKILL.md` |
| 更新 catalog | 編輯 `INDEX.md` 新增 entry |
| 驗證 delivery | 執行 `verify-bootstrap.py` |
| 檢查庫存 | 讀取 `ops/inventory.latest.json` |
| 查看歷史 | 讀取 `ops/history/` 目錄 |

### 4.3 衝突處理流程

依照 OPERATIONS.md 的規範：

1. **SCAN** — 掃描候選資源
2. **REVIEW** — 檢查 metadata 和內容
3. **DRY-RUN** — 預覽變更（Claude 在此停止報告）
4. **ADOPT** — 等待人類確認後執行
5. **DELIVER** — 執行 delivery
6. **VERIFY** — 驗證結果

---

## 5. 評估結論

### 5.1 整體評分

| 評估面向 | 分數 (1-5) | 說明 |
|---------|-----------|------|
| **架構相容性** | 5/5 | 完美適配 Claude 的能力模型 |
| **文檔品質** | 5/5 | 清晰、完整、AI-friendly |
| **安全性設計** | 5/5 | Dry-run、backup、explicit triggers |
| **實用性** | 4/5 | 已有可運行的 baseline |
| **擴展性** | 5/5 | 明確的 resource types 和 spec |

**總評：4.8/5 — 高度推薦**

### 5.2 最終建議

1. **可直接採用**：UniText 在 Claude 預設架構下完全可行
2. **最佳實踐**：使用 `INDEX.md` 作為 AI discovery 入口
3. **持續改進**：可考慮增加更多 Claude 專用的 workflow 模板

### 5.3 適用場景

| 場景 | 適用性 |
|------|-------|
| 個人 AI 工具整合 | ✅ 非常適合 |
| 團隊共享 skill 定義 | ✅ 非常適合 |
| 跨 CLI 資源標準化 | ✅ 最佳選擇 |
| 企業級部署 | ⚠️ 需評估擴展性 |

---

## 6. 附錄：技術細節

### 6.1 UniText 目前資源統計

| 類別 | 數量 | 狀態 |
|------|------|------|
| Skills | 12 | Active (8 Core + 4 Expansion) |
| MCP Servers | 1 | Active baseline |
| Agents | 1 | Active |
| Workflows | 1 | Draft |

### 6.2 支援的 Delivery Modes

- `pointer` — 僅 discovery
- `mirror` — 本地副本
- `symlink` — 符號連結
- `native-config` — CLI 原生配置

### 6.3 檔案結構概覽

```
UniText/
├── registry/          ← 共享資源定義（Claude 主要讀取區）
│   ├── skills/        ← 12 個 skill 定義
│   ├── mcp/           ← MCP server 定義
│   ├── agents/        ← Agent persona 定義
│   └── workflow/      ← 工作流程模板
├── local/             ← 部署配置（平台特定）
│   ├── docs/          ← 路徑映射文檔
│   └── scripts/       ← 自動化腳本
├── ops/               ← 操作狀態（審計追蹤）
│   ├── baseline.json
│   ├── inventory.latest.json
│   └── history/
└── i18n/              ← 國際化翻譯（8 種語言）
```

---

*本評估報告由 Claude 生成，基於對 UniText 專案文檔和結構的完整分析。*
