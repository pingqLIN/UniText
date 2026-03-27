# 🔍 魔鬼代言人審查 — 獨立驗證與建議行動

> 角色：`code-state verification`
> **審查對象**: `DEVILS_ADVOCATE_REVIEW_2026-03-26.md`
> **驗證日期**: 2026-03-26
> **驗證方法**: 以獨立第三方立場，對審查中每項主張進行程式碼層級的實際驗證，再給出分類判定與行動建議

---

## 一、逐項驗證結果

### 1. 🚨 Anthropic Skills 授權違規

| 面向 | 審查主張 | 驗證結果 |
|------|---------|---------|
| Anthropic 版權 | 11 個 skills 含 `© Anthropic` | ✅ **確認** — 所有 skills 的 LICENSE.txt 均含 Anthropic 版權聲明 |
| Proprietary 標記 | pdf/docx/xlsx/pptx 標為 Proprietary | ✅ **確認** — 4 個 SKILL.md 明確寫 `license: Proprietary` |
| 再分發禁令 | LICENSE.txt 禁止再分發 | ✅ **確認** — 條款明示 "Distribute, sublicense, or transfer these materials to any third party" 為禁止行為 |
| 根目錄 LICENSE | 宣稱 MIT 但矛盾 | ⚠️ **修正** — 根目錄實際上**不存在** LICENSE 檔案（PRE_PUSH_AUDIT 已記錄為 blocker #5），比審查描述的更嚴重 |

**判定**: ✅ 確認 — 法律風險真實存在，嚴重度 **CRITICAL**

---

### 2. 🚨 820 MB 意外備份

| 面向 | 審查主張 | 驗證結果 |
|------|---------|---------|
| 檔案數 | ops/history 有 10,373 檔 | ✅ **確認** — 實測 10,373 檔 |
| 大小 | 820 MB | ✅ **確認** — 實測 819.71 MB |
| Windsurf 內容 | 含 Windsurf node_modules | ✅ **確認** — `backup_20260228_225519` 含 `C__Users_miles_AppData_Local_Programs_Windsurf/` 路徑，包括 chrome_100_percent.pak、ffmpeg.dll 等二進位檔 |
| 個人路徑曝露 | 會曝露個人電腦結構 | ✅ **確認** — 備份路徑含完整使用者目錄結構 |

**判定**: ✅ 確認 — 倉庫衛生問題真實存在，嚴重度 **CRITICAL**

**緩解因素**: `.gitignore` 已排除 `ops/history/backup_*`，因此若備份產生於 gitignore 生效後，不會進入 git。但需確認是否已有提交包含此內容。

---

### 3. 文件 vs 程式碼比例失衡

| 面向 | 審查主張 | 驗證結果 |
|------|---------|---------|
| Markdown 數量 | ~300 個 | ⚠️ **低估** — 實測 1,412 個 .md 檔案（含 i18n 多語言版本） |
| 核心代碼量 | < 2,000 行 | ✅ **合理** — bootstrap.py 436行 + server.py 209行 + 工具腳本 |
| 比例 | 72% 文件 vs 16% 程式碼 | ✅ **大致確認** — 實測 1,412 .md vs 833 .py/.ps1（1.7:1） |

**判定**: ✅ 確認 — 但這是否為「問題」取決於專案定位。若定位為「規範驅動的資源中心」而非「軟體產品」，高文件比例可以合理化。建議在 README 中明確定位。

---

### 4. 3 天歷史、1 個開發者、0 個外部使用者

| 面向 | 審查主張 | 驗證結果 |
|------|---------|---------|
| 第一個 commit | 2026-03-23 | ✅ **確認** |
| 貢獻者 | 1 人 2 身份 | ✅ **確認** — PingKuei Lin + root |
| 外部使用者 | 零 | ✅ **確認** |

**判定**: ✅ 確認 — 事實正確。作為早期專案這是正常狀態，但不應在文件中暗示更高的成熟度。

---

### 5. 無 CI/CD、無依賴管理

| 面向 | 審查主張 | 驗證結果 |
|------|---------|---------|
| GitHub Actions | 零 workflows | ✅ **確認** — `.github/workflows/` 目錄不存在 |
| 依賴檔案 | 無 requirements.txt / pyproject.toml / package.json | ⚠️ **部分確認** — 存在 1 個 `requirements.txt`（在 `registry/skills/mcp-builder/scripts/` 下），但根目錄級無任何依賴管理 |
| 版本鎖定 | 無 | ✅ **確認** — yaml, defusedxml, pypdf, playwright 僅存在於 import 語句中 |

**判定**: ✅ 確認 — 嚴重度 **HIGH**

---

### 6. ⚠️ 安全漏洞「未修復」— 部分反駁

這是本次驗證中最重要的發現：**審查引用了過時的安全文件，而非當前程式碼狀態。**

| 編號 | 審查主張 | 程式碼實際狀態 |
|------|---------|--------------|
| SEC-001 | `with_server.py` 使用 `shell=True` | ⚠️ **已緩解** — `shell=True` 僅在明確傳入 `--allow-shell` 旗標時啟用（第 38 行），預設為 JSON-only 解析 |
| SEC-002 | `rollback-skills.ps1` 可刪除倉庫外檔案 | ✅ **已修復** — 使用 `Resolve-SafeRepoPath` 函式限制路徑範圍（第 23 行），且強制 `adopt_*` 目錄模式（第 24 行） |
| SEC-002 | `batch-adopt-skills.ps1` 可覆寫倉庫外檔案 | ✅ **已修復** — 使用 `Test-IsUnderPath` 雙重驗證來源與目標路徑（第 14-16、37-43 行），加入 reparse point 檢查防止符號連結穿越（第 50-52 行） |
| SEC-003 | `bootstrap.py --repo-root` 接受任意路徑 | ✅ **已修復** — 外部路徑預設禁用，需 `--allow-external-repo-root` 旗標；驗證函式要求 4 個必要標記檔案存在（第 134-148 行） |

**判定**: ⚠️ **部分反駁** — 程式碼已修復，但 `SECURITY_REVIEW_ADVISORY.md` 文件未更新以反映修復狀態。審查引用了文件而非程式碼，導致結論過時。

**具體程式碼證據**:

```powershell
# rollback-skills.ps1 — 路徑限制已加入
$safeRunDir = Resolve-SafeRepoPath -RepoRoot $repo -BaseRelativePath "ops\history" `
    -UserPath $RunDir -AllowBasePath -RequireExisting
if ((Split-Path $safeRunDir -Leaf) -notlike "adopt_*") {
    throw "RunDir must point to an adopt_* backup directory under ops/history."
}
```

```powershell
# batch-adopt-skills.ps1 — 雙重路徑驗證
if (-not (Test-IsUnderPath -RootPath $skillsRoot -CandidatePath $dstRoot)) {
    throw "Destination must remain under registry/skills: $dstRoot"
}
if (-not (Test-IsUnderPath -RootPath $srcRoot -CandidatePath $src)) {
    throw "Resolved source escapes source root: $src"
}
```

```python
# bootstrap.py — 外部路徑預設禁止
def validate_repo_root(candidate, script_root, allow_external):
    if candidate == script_root:
        validate_repo_surface(candidate)
        return
    if not allow_external:
        raise SystemExit("external --repo-root is disabled by default; ...")
    validate_repo_surface(candidate)
```

---

### 7. 跨平台宣稱超實際驗證

| 宣稱組合 | 驗證證據 | 狀態 |
|----------|---------|------|
| Windows + Claude Code | bootstrap.py 執行紀錄 | ✅ 已驗證 |
| Windows + Copilot CLI | MCP 連線超時 | ⚠️ 失敗 |
| macOS + 任何 CLI | 無任何證據 | ❌ 未測試 |
| Linux + 任何 CLI | 僅 WSL 部分驗證 | ⚠️ 薄弱 |
| Gemini CLI | 僅驗證 delivery path | ❌ 不完整 |
| Codex CLI | 僅驗證 config 寫入 | ❌ 不完整 |

**判定**: ✅ 確認 — 宣稱 12 組合，實際驗證 ~2 組合，嚴重度 **HIGH**

---

### 8–9. 市場需求與治理比例（主觀論點）

審查第 8–9 點屬於設計判斷而非事實主張，無法以程式碼驗證。

- **第 8 點**（問題是否存在）：合理的產品質疑，但無法在技術層面反駁或確認
- **第 9 點**（治理過重）：管理 15 個資源是否需要 6 步驟流程和 18 個腳本，確實值得反思

**判定**: 📝 記錄 — 作為產品策略反思，不需技術行動

---

### 10. i18n 翻譯品質存疑

| 面向 | 審查主張 | 驗證結果 |
|------|---------|---------|
| 語言數 | 8 種 | ✅ 確認 — zh-TW, zh-CN, ja, de, fr, es, ko, it |
| AI 生成 | 幾乎確定 | 合理推測但無法技術驗證 |

**判定**: 📝 記錄 — 建議進行母語使用者抽查，低優先

---

### 11. 測試覆蓋範圍極窄

| 面向 | 審查主張 | 驗證結果 |
|------|---------|---------|
| 測試總數 | 29 個 | ⚠️ **需修正** — 實測僅找到 6 個測試函式（1 個測試檔案 `tests/security/test_hardening.py`，119 行） |
| 全為安全測試 | 是 | ✅ **確認** — 6 個函式全部為安全邊界測試 |
| 零功能測試 | 是 | ✅ **確認** |
| 零整合測試 | 是 | ✅ **確認** |
| 4 個失敗測試 | PRE_PUSH_AUDIT 紀錄 | ✅ **確認** — 涉及 bootstrap 備份邏輯、verify-template 空值檢查、generate-index 路徑解析 |

**判定**: ✅ 確認 — 嚴重度 **HIGH**

---

## 二、驗證總表

| # | 主張 | 嚴重度 | 驗證結果 | 行動需求 |
|---|------|--------|---------|---------|
| 1 | Anthropic 授權違規 | 🔴 CRITICAL | ✅ 確認 | **必修** |
| 2 | 820 MB 意外備份 | 🔴 CRITICAL | ✅ 確認 | **必修** |
| 3 | 文件/程式碼比例失衡 | 🟡 HIGH | ✅ 確認 | 可接受（需明確定位） |
| 4 | 3 天 / 1 人 / 0 使用者 | 🟡 HIGH | ✅ 確認 | 可接受（不誇大成熟度） |
| 5 | 無 CI/CD | 🟡 HIGH | ✅ 確認 | **需修** |
| 6 | 安全漏洞未修 | 🟡 HIGH | ⚠️ **部分反駁** | **需更新文件** |
| 7 | 跨平台宣稱過高 | 🟡 HIGH | ✅ 確認 | **需修** |
| 8 | 問題不存在 | 🟠 MEDIUM | 📝 主觀論點 | 記錄 |
| 9 | 治理過重 | 🟠 MEDIUM | 📝 主觀論點 | 記錄 |
| 10 | i18n 品質存疑 | 🟠 MEDIUM | 📝 合理懷疑 | 低優先抽查 |
| 11 | 測試覆蓋極窄 | 🟡 HIGH | ✅ 確認 | **需修** |

---

## 三、建議行動

### 🔴 Phase 1 — 發布阻斷項（必須在任何發布前完成）

| ID | 行動 | 說明 |
|----|------|------|
| **ACT-01** | 解決 Anthropic Skills 授權 | 從 template 包中移除 Proprietary 內容，改用 pointer 引用 + 安裝指引；或將 skills 定義為「僅供本地使用、不再分發」 |
| **ACT-02** | 清除意外備份 | 刪除 ops/history 中的 Windsurf 備份；確認未進入 git history；在備份機制中加入路徑範圍限制 |
| **ACT-03** | 建立根目錄 LICENSE | 建立 MIT LICENSE，明確標註範圍僅限 UniText 自身程式碼，不涵蓋第三方 skills |

### 🟡 Phase 2 — 工程基礎（發布前強烈建議）

| ID | 行動 | 說明 |
|----|------|------|
| **ACT-04** | 建立依賴管理 | 建立 `pyproject.toml` 或根目錄 `requirements.txt`，列出所有 Python 依賴及版本範圍 |
| **ACT-05** | 建立最小 CI/CD | `.github/workflows/ci.yml`：Python lint + 測試自動執行，支援 Windows + Linux matrix |
| **ACT-06** | 擴展測試覆蓋 | 新增 bootstrap 功能測試 + registry → local 端到端測試；修復 4 個已知失敗 |
| **ACT-07** | 更新安全文件 | 將已修復的 SEC-002、SEC-003 標記為 ✅，附程式碼引用（這是審查的主要不準確之處） |
| **ACT-08** | 收斂跨平台宣稱 | README 中誠實標示各平台：✅ verified / ⚠️ expected / ❌ untested |

### 🟠 Phase 3 — 改善（非阻斷，提升可信度）

| ID | 行動 | 說明 |
|----|------|------|
| **ACT-09** | 精簡根目錄 | 將治理文件移入 `docs/`，根目錄僅保留標準檔案 |
| **ACT-10** | 正式回應審查 | 建立回應文件，逐項標註處置結果 |
| **ACT-11** | i18n 品質抽查 | 選 2-3 種語言核心文件進行母語使用者審查 |

---

## 四、執行順序

```
Phase 1 (阻斷):   ACT-01 → ACT-02 → ACT-03
Phase 2 (基礎):   ACT-04 → ACT-05 → ACT-06 → ACT-07 → ACT-08
Phase 3 (改善):   ACT-09 → ACT-10 → ACT-11
```

> Phase 1 為法律與衛生問題，必須最先處理。
> Phase 2 建立工程可信度。
> Phase 3 為可選改善。

---

## 五、對審查的整體評價

魔鬼代言人審查**整體品質高**，大多數主張有事實依據。主要問題是：

1. **SEC-002 判斷過時**：引用安全文件而非檢查實際程式碼，導致「未修復」結論不正確
2. **部分數據不精確**：Markdown 數量審查稱 ~300 但實測 1,412（含 i18n）；測試數量稱 29 但核心僅 6 個函式
3. **主觀與客觀混雜**：第 8-9 點是合理的產品質疑但不應與技術缺陷列為同等嚴重度

整體而言，審查的核心結論 —— **「不應在當前狀態下發布」**—— 在 Phase 1 三項阻斷問題未解決前是**正確的**。

---

*驗證日期：2026-03-26*
*驗證方法：獨立程式碼層級檢查，交叉比對審查主張與實際倉庫狀態*
