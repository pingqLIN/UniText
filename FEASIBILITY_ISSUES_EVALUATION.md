# 可行性問題評估報告

> 評估日期：2026-03-24
> 目的：評估另一個模型所發現的三個問題是否重要，以及是否需要修復

---

## 執行摘要

**結論：這些是重要且有效的問題 ✅**

另一個模型識別的三個問題都是合理且重要的：

| 問題 | 重要性 | 狀態 |
|------|--------|------|
| 1. settings.json 反斜線過度轉義 | 🔴 高 | 語法錯誤，影響功能 |
| 1b. MCP 權限參照錯誤工具 | 🔴 高 | 指向不存在的 Docker MCP |
| 2. .mcp.json seed 配置缺失 | 🟡 中 | 影響開箱即用體驗 |
| 3. .gitignore 排除 .mcp.json | 🟡 中 | 設計決策，需權衡 |

---

## 問題 1：`.claude/settings.json` 反斜線轉義問題

### 現況分析

```json
"Bash(find . -type f \\\\\\(-name *.py -o -name *.js ...)"
```

**原始檔案字節分析**：
- 原始檔案中有 6 個反斜線字元：`\\\\\\(`
- JSON 解析後變成 3 個反斜線：`\\\(`
- Bash 實際需要：`\(` （只需 1 個反斜線來轉義括號）
- 正確的 JSON 表示：`\\(` （2 個字元，解析後變成 1 個反斜線）

### 問題嚴重性：🔴 高

這是一個**語法錯誤**：
- 過多的反斜線會導致 find 指令的分組表達式無效
- 權限模式可能無法正確匹配預期的指令
- 會影響 Claude 執行程式碼搜尋的能力

### 建議修復

```json
"Bash(find . -type f \\(-name *.py -o -name *.js -o -name *.ts -o -name *.sh -o -name *.ps1 \\))"
```

---

## 問題 1b：MCP 權限參照錯誤

### 現況分析

```json
"mcp__MCP_DOCKER__read_file"
```

**問題**：
- `MCP_DOCKER` 是 Docker 相關的 MCP 服務器，不是本專案的 MCP
- 本專案的 MCP 服務器名稱是 `unitext-registry`
- 應該參照本專案 MCP 的三個工具

### MCP 服務器提供的工具

根據 `registry/mcp/claude-project-mcp-seed/server.py`：

1. `registry_summary` — 返回 registry 統計和核心文檔清單
2. `list_registry_entries` — 按類型列出 registry 項目
3. `read_registry_file` — 安全讀取 registry 檔案

### 問題嚴重性：🔴 高

這是一個**配置錯誤**：
- 指向不存在的 MCP 服務器
- Claude 無法使用本專案的 MCP 功能
- 喪失了 UniText 設計的 AI discovery 能力

### 建議修復

```json
"mcp__unitext-registry__registry_summary",
"mcp__unitext-registry__list_registry_entries", 
"mcp__unitext-registry__read_registry_file"
```

---

## 問題 2：`.mcp.json` Seed 配置缺失

### 現況分析

- `.mcp.json` 目前不存在於 repo 中（被 gitignore）
- 使用者需要先執行 `bootstrap.py` 才能使用 MCP
- 存在一個模板：`registry/mcp/claude-project-mcp-seed/definition.json`

### 模板內容（definition.json）

```json
{
  "mcpServers": {
    "unitext-registry": {
      "transport": "stdio",
      "command": "python",
      "args": ["registry/mcp/claude-project-mcp-seed/server.py", "--root", "."]
    }
  }
}
```

這個模板使用相對路徑，可以在任何機器上運作。

### 問題嚴重性：🟡 中

這是一個**使用者體驗問題**：
- 新使用者 clone 後無法立即使用 MCP 功能
- 需要額外步驟（執行 bootstrap.py）
- 但不是功能性錯誤，有明確的解決方案

### 建議方案

創建 `.mcp.json` 作為 seed 配置，使用相對路徑：
- `python3` 而非 `python`（更好的跨平台相容性）
- 相對路徑讓 fresh clone 可以立即運作
- `bootstrap.py --force` 會升級為絕對路徑版本

---

## 問題 3：`.gitignore` 排除 `.mcp.json`

### 現況分析

`.gitignore` 第 4 行：
```
.mcp.json
```

### 設計考量

**排除的理由**（目前設計）：
- `bootstrap.py` 會生成包含絕對路徑的版本
- 絕對路徑是機器特定的，不應追蹤
- 避免不同開發者的配置衝突

**追蹤的理由**（建議改進）：
- 可以追蹤一個使用相對路徑的 seed 版本
- 新 clone 可以開箱即用
- bootstrap.py 會在需要時升級它

### 問題嚴重性：🟡 中

這是一個**設計決策**，而非錯誤：
- 兩種方案都有合理性
- 追蹤 seed 版本可以改善使用者體驗
- 但需要確保 bootstrap.py 的行為一致

### 建議方案

1. 從 `.gitignore` 移除 `.mcp.json`
2. 追蹤一個使用相對路徑的 seed `.mcp.json`
3. 在 seed 配置中使用 `python3`
4. 確保 `bootstrap.py` 會正確升級它

---

## 綜合評估

### 問題有效性

| 問題 | 有效性 | 理由 |
|------|--------|------|
| 反斜線轉義 | ✅ 有效 | 技術性錯誤，經字節分析確認 |
| MCP 權限錯誤 | ✅ 有效 | 指向不存在的服務，經代碼分析確認 |
| Seed 配置缺失 | ✅ 有效 | 影響開箱即用體驗，但非功能性錯誤 |
| Gitignore 設計 | ✅ 有效 | 合理的改進建議，但現有設計也有道理 |

### 是否應該修復？

**強烈建議修復** ✅

1. **問題 1 & 1b**：必須修復
   - 這些是實際的配置錯誤
   - 會影響 Claude 與本專案的整合

2. **問題 2 & 3**：建議修復
   - 改善使用者體驗
   - 符合 UniText 「AI-first discovery」的設計原則
   - 讓新使用者可以立即體驗 MCP 功能

### 修復影響評估

| 修復項目 | 影響範圍 | 風險 |
|---------|---------|------|
| settings.json | 僅權限配置 | 低 |
| 新增 .mcp.json | 新檔案 | 低 |
| 修改 .gitignore | 一行變更 | 低 |

所有修復都是低風險的小型變更，不會影響核心功能。

---

## 結論

另一個模型的評估是**準確且有價值的**。這些問題確實會影響 UniText 在 Claude 預設架構下的可行性，應該予以修復。

修復後，UniText 將能夠：
1. ✅ 正確配置 Claude 的檔案搜尋權限
2. ✅ 啟用本專案的 MCP 工具
3. ✅ 新 clone 可以開箱即用 MCP 功能
4. ✅ 完全符合「可行性評估」報告中的預期架構

---

*本評估報告基於對原始檔案的字節級分析、JSON 解析驗證、以及 MCP 服務器代碼審查。*
