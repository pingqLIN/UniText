# 🔴 UniText 反對意見書 — 魔鬼代言人分析

> 角色：`historical snapshot`
> 日期：2026-03-26
> 用途：保留原始反對意見的歷史切面，不應直接當成 2026-03-27 之後的 current-state 結論。

作為本專案的反對方，以下是 **不應發布、不應使用、不建議使用** 的完整論述。每一點都附有證據。

---

## 一、致命問題（CRITICAL — 單獨一項即可否決發布）

### 1. 🚨 授權違規：Skills 是 Anthropic 的專有資產

**理由：** 全部 12 個 skills 的 LICENSE.txt 清楚寫著：

> `© 2025 Anthropic, PBC. All rights reserved.`
> `Use of these materials is governed by your agreement with Anthropic regarding use of Anthropic's services.`

其中 `pdf`、`docx`、`pptx`、`xlsx` 更標註為 **`Proprietary`**。

**然而，** UniText 根目錄的 LICENSE 卻是 **MIT License (Copyright 2026 UniText contributors)**，並且計劃將這些 skills 作為 template package 重新分發。

**懷疑：** 這構成將第三方專有內容重新包裝為開源發布的行為。Anthropic 的 skills 是隨 Claude Code 提供的，不是可以自由再分發的開源素材。

**證據：**
- `registry/skills/pdf/LICENSE.txt` → `© 2025 Anthropic, PBC. All rights reserved.`
- `registry/skills/docx/SKILL.md` → `license: Proprietary. LICENSE.txt has complete terms`
- 根目錄 `LICENSE` → `MIT License, Copyright 2026 UniText contributors`

**結論：** 在解決授權問題之前，**法律上不能發布**。

---

### 2. 🚨 908 MB 的倉庫包含 820 MB 的意外備份

**理由：** `ops/history/` 目錄有 **10,373 個檔案、820 MB**，其中絕大部分是一次意外備份下來的 **Windsurf 編輯器的完整 node_modules**：

```
ops/history/backup_20260228_225519/C__Users_miles_AppData_Local_Programs_Windsurf/
  resources/app/node_modules/  ← 4,267 個 .js 檔案
```

**懷疑：** 這個「稽核追蹤」機制在不受控的情況下，把整台電腦的應用程式目錄備份進了倉庫。這表明：
1. backup-before-mutation 策略存在嚴重的範圍失控
2. 路徑限制（path confinement）缺失——這正是安全審查中指出的 SEC-002
3. 如果推送到 GitHub，會把個人電腦的完整軟體結構曝露

**證據：**
- `(Get-ChildItem -Recurse -File -Path ops\history).Count` → 10,373
- 4,267 個 `.js` 檔案全部位於 Windsurf 的 node_modules
- 倉庫總大小 908 MB，其中 .git 只有 1.6 MB

---

## 二、嚴重問題（HIGH — 構成不建議使用的充分理由）

### 3. 文件對程式碼比例嚴重失衡：72% 文件 vs 16% 程式碼

**理由：** 專案包含 **~300 個 Markdown 文件**，但實際可執行程式碼只有：
- 47 個 Python 檔案（其中 31 個屬於 skills 的附屬腳本）
- 16 個 PowerShell 腳本
- 1 個 JavaScript 檔案

扣除 skills 的腳本後，UniText **自身的核心代碼不到 2,000 行**（bootstrap.py 436行 + server.py 209行 + verify 腳本 + 幾個 report 腳本）。

**懷疑：** 這不是一個軟體產品，這是一份**帶有少量腳本的規範文件集**。38 個根目錄 Markdown 檔案（包括 VISION、RESOURCE_SPEC、OPERATIONS、MILESTONES、多份 RELEASE_EVIDENCE、EXTERNAL_REVIEW 等）的治理文件量，遠遠超過了它所治理的內容。

**證據：** 1,224 個 .md 檔案 vs 47 個 .py 檔案。核心 infra 代碼 < 2,000 行。

---

### 4. 3 天歷史、1 個開發者、0 個外部使用者

**理由：**
- 第一個 commit：`2026-03-23`（距今 3 天）
- 貢獻者：`PingKuei Lin: 28 commits, root: 11 commits`（同一人的兩個身份）
- 外部使用者：**零**
- Forks / Stars / Issues / PRs：**零**

**懷疑：** 專案的「Phase 1 ✅ COMPLETE → Phase 2 ✅ COMPLETE → Phase 3 ✅ COMPLETE」里程碑、完整的外部審查套件、多語言翻譯（8 種語言）、詳盡的發布證據鏈——這一切在 3 天內由一個人完成，極度不符比例。這暗示大量內容是 AI 生成的，未經人類深度審查。

**證據：** `git log --reverse` 第一個 commit 是 2026-03-23。`git shortlog -sn --all` 只有兩個身份。

---

### 5. 沒有 CI/CD、沒有依賴管理、沒有自動化品質門

**理由：**
- **零** GitHub Actions workflows
- **零** `requirements.txt`、`pyproject.toml`、`package.json`
- 所有測試都是手動本地執行
- 依賴（yaml, defusedxml, pypdf, playwright）只存在於 import 語句中，無版本鎖定

**懷疑：** 對於一個聲稱有完整治理流程（SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY）的專案，卻沒有最基本的自動化測試管線，這是一個根本性的矛盾。治理是寫在紙上的，不是執行在程式碼中的。

**證據：** `.github/` 目錄只有 `copilot-instructions.md`，沒有 `workflows/` 目錄。

---

### 6. 安全漏洞已知但未修復

**理由：** 專案自己的安全審查清楚記錄了：

| 編號 | 等級 | 問題 | 狀態 |
|------|------|------|------|
| SEC-001 | CRITICAL | `with_server.py` 使用 `shell=True` | ⚠️ 緩解但未消除 |
| SEC-002 | HIGH | `rollback-skills.ps1` 可刪除倉庫外的檔案 | ❌ 未修復 |
| SEC-002 | HIGH | `batch-adopt-skills.ps1` 可覆寫倉庫外的檔案 | ❌ 未修復 |
| SEC-003 | MEDIUM | `bootstrap.py --repo-root` 接受任意路徑 | ⚠️ 部分緩解 |

更嚴重的是，`FINAL_RELEASE_DEVELOPMENT_PLAN` 自己把 `with_server.py --allow-shell` 列為 **one-vote-kill**（一票否決），但目前仍在程式碼中。

**證據：** `SECURITY_REVIEW_ADVISORY.md`、`SECURITY_ATTACK_INPUT_CHECKLIST.md`、`PRE_PUSH_AUDIT_2026-03-26.md`

---

### 7. 跨平台宣稱遠超實際驗證

**理由：** README 和文件聲稱支援：
- 4 個 CLI（Claude Code、Codex、Gemini CLI、Copilot CLI）
- 3 個作業系統（Windows、macOS、Linux）

**實際驗證：**
- ✅ Python bootstrap 在 Windows 上通過
- ⚠️ Copilot MCP 連接超時
- ❌ macOS：**零測試證據**
- ❌ Linux：僅 WSL 部分驗證
- ❌ Gemini CLI：僅驗證「delivery path」，無端到端測試
- ❌ Codex CLI：僅驗證 config 寫入，無實際載入測試

**懷疑：** 宣稱 `4 CLI × 3 OS = 12` 個組合的支援，但實際只驗證了 ~2 個。這是文件聲明（documentation claim）而非工程事實（engineering fact）。

**證據：** `COPILOT_SESSION_EVIDENCE` 記錄 MCP 超時。`CLI_COMPAT_MATRIX` 的 `Last Verified` 日期可疑地集中在 3 天內。

---

## 三、質疑（MEDIUM — 使用價值存疑）

### 8. 解決的問題可能不存在

**核心主張：** 「使用者同時使用多個 AI CLI 時，skills 定義會碎片化」

**反問：**
- 有多少人**同時**使用 Claude Code + Codex + Gemini CLI + Copilot CLI？
- 即使同時使用，每個 CLI 的 skill 格式略有不同，UniText 真的能統一嗎？（SKILL.md 是純 Markdown，各 CLI 的載入機制不同）
- 一個 `cp -r` 或符號連結不就解決了嗎？為什麼需要一個 6 步驟治理流程？

**懷疑：** 這是一個**過度工程化的解決方案**，針對一個**尚未被市場驗證的問題**。

---

### 9. 治理複雜度與被治理對象不成比例

**被治理的內容：**
- 12 個 skills（其中 5 個只是純 Markdown 指導文件）
- 1 個 MCP server
- 1 個 agent seed
- 1 個 workflow seed

**治理機制：**
- 6 步驟採納流程（SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY）
- 4 種交付模式（pointer、mirror、symlink、native-config）
- 11 個 PowerShell 管理腳本
- 7 個 Python 操作腳本
- 完整稽核追蹤系統（ops/history）
- 原子寫入機制
- generation_state 完整性標記
- 中斷恢復測試

管理 15 個文字資源需要這麼多基礎設施嗎？

---

### 10. i18n 翻譯品質存疑

**理由：** 在 3 天內完成 8 種語言、21 個源文件的翻譯。i18n Wave Report 顯示 63 個檔案有變更（全部是 EOL 正規化）。

**懷疑：** 這些翻譯幾乎確定是 AI 生成的，未經母語使用者審查。作為一個「AI-first」專案的文件，用 AI 翻譯本身不是問題——但如果翻譯品質低劣，反而會損害專案的可信度。

---

### 11. 測試雖通過但覆蓋範圍極窄

**理由：** 29 個測試全部通過，但：
- 全部集中在 `tests/security/`（安全/完整性）
- **零**功能測試（skills 是否真的能被 CLI 載入和使用？）
- **零**整合測試（bootstrap → 實際 CLI 使用的端到端流程？）
- **零**回歸測試
- Pre-push audit 仍有 4 個失敗測試（在不同條件下）

**懷疑：** 測試存在嚴重的倖存者偏差——只測試了安全邊界，沒測試核心功能是否真的有效。

---

## 四、總結裁定

| 維度 | 裁定 | 嚴重度 |
|------|------|--------|
| **授權合規** | Anthropic 專有 skills 不得以 MIT 再分發 | 🔴 CRITICAL |
| **倉庫衛生** | 820 MB 意外備份、個人路徑曝露 | 🔴 CRITICAL |
| **產品成熟度** | 3 天、1 人、0 使用者 | 🔴 HIGH |
| **工程基礎** | 無 CI/CD、無依賴管理 | 🟡 HIGH |
| **安全狀態** | 已知漏洞未修、一票否決項未清 | 🟡 HIGH |
| **跨平台可信度** | 宣稱 12 組合，驗證 ~2 組合 | 🟡 HIGH |
| **市場需求** | 問題未經驗證，使用者為零 | 🟠 MEDIUM |
| **治理比例** | 極重的流程管理極少的內容 | 🟠 MEDIUM |

### 最終建議：**不應在當前狀態下發布**

1. **法律風險**：先解決 Anthropic skills 的授權問題（移除專有 skills 或取得再分發許可）
2. **衛生風險**：清除 820 MB 的意外備份和個人路徑
3. **信任風險**：在至少有 1 個外部使用者驗證核心流程之前，不應宣稱「ready」
4. **工程風險**：先建立 CI/CD 和依賴管理，再談治理流程

> *「一個宣稱自己有完整治理流程的專案，卻連最基本的自動化品質門都沒有——這本身就是最大的治理漏洞。」*

---

*分析日期：2026-03-26*
*分析方法：完整探索專案結構、程式碼、文件、發布證據後，以反對方立場撰寫*
