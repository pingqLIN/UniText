---
description: Fresh second-round devil's advocate review of UniText, challenging the closure claims of the 2026-03-26 review chain
date: 2026-03-27
role: independent-opposition
---

# 🔴 UniText 魔鬼代言人審查 — 第二輪

> **角色：獨立反對觀點（FRESH 視角）**
> **日期：2026-03-27**
> **前情：** 本報告不受前一輪（2026-03-26）審查鏈影響，以全新視角重新出發。

---

## ⚠️ 開場聲明

前一輪魔鬼代言人審查於 2026-03-26 提出，2026-03-27 的「綜合審查」與「閉合備忘錄」宣稱大多數阻斷項已修復。**本輪審查的任務是：對「已修復」的宣稱本身提出質疑，並尋找前一輪遺漏的新問題。**

---

## 一、致命問題（CRITICAL）

### 🚨 C-1：6,761 個 Markdown 檔案——比前一輪翻了 22 倍，卻沒人提

前一輪審查批評專案有 1,224 個 `.md` 檔案（判定為嚴重失衡）。

**現況：**

```powershell
(Get-ChildItem -Recurse -Filter "*.md").Count  →  6,761
```

這不是修復，這是**爆炸性惡化**。6,761 個 Markdown 相對於：
- 13 個測試
- 36 個外部技能（自己寫 0 個）
- 核心 Python < 2,000 行

**沒有任何一份閉合文件提到這個數字。** 這代表審查鏈在自我評估時，根本沒有重新量測最基本的指標。

**懷疑：** i18n 擴張（9 語言 × ~750 文件）在解決授權問題的同時，靜靜地把文件負債翻了 22 倍，而且完全沒有被當成問題處理。

---

### 🚨 C-2：「修復」的授權問題，實際上是用 36 個授權未完整驗證的外部技能替換 12 個已知問題技能

閉合備忘錄聲稱授權問題「已修復」，依據是：
- `pdf/docx/xlsx/pptx` 已從 active registry 移除
- 新的 skills 來自 MIT / Apache-2.0 授權的 GitHub repo

**但現在 registry/skills/ 有 36 個目錄，全部來自外部 repo。** 問題：

1. `github/awesome-copilot` 是一個社群貢獻 repo——裡面的每個 skill 是否都由 repo maintainer 擁有版權並可在 MIT 下授權？還是它是「aggregation of contributions」，每個貢獻者保留自己的版權？
2. `obra/superpowers` 的多個 skill 是由不同人貢獻的（PR 歷史可查），UniText 是否確認每個被引入的 skill 的原作者同意 MIT 再分發？
3. `SOURCES.md` 記錄的是 **repo 層級**的授權，不是 **skill 層級**的授權。授權覆蓋範圍有歧義。

**結論：** 前一個授權問題是「已知問題」，現在的授權問題是「大量假設性問題」——後者可能更難追蹤。

---

### 🚨 C-3：CI 完全是 Windows-only，與跨平台宣稱根本矛盾

```yaml
# .github/workflows/ci.yml
runs-on: windows-latest
```

只有這一行。沒有 macOS job，沒有 Linux job，沒有 matrix strategy。

而 README 聲稱：
- macOS：`target` — Python bootstrap 設計為 portable
- Linux：`target` — Python bootstrap 設計為 portable

**「設計為 portable」 ≠ 「CI 驗證為 portable」。**

一個 Python 腳本在 Windows 上通過測試，在 macOS 上卻可能因為路徑分隔符、`USERPROFILE` vs `HOME`、`pwsh` 可用性而失敗。沒有 CI 就沒有保護。

**更深的問題：** 閉合備忘錄的驗收清單包括 `python -m unittest discover ... OK`，但這是在 Windows 上跑的。如果有人在 macOS 上 clone 這個 repo 並執行 bootstrap，成功率是多少？沒有人知道，因為沒有測試。

---

## 二、嚴重問題（HIGH）

### 🔴 H-1：「自我認證」閉合——所有「已修復」的結論都是用自己的腳本驗證自己的腳本

閉合備忘錄的驗證依據：

```
python -m unittest discover   → 自己寫的測試
health-check.ps1              → 自己寫的腳本
verify-workspace-hygiene.ps1  → 自己寫的腳本
export-review-package.ps1     → 自己寫的腳本
```

這是**循環驗證**。如果腳本本身有缺陷，測試不會發現它，因為測試是用同一套假設寫的。

「External Review Ready」的核心意義是：有人**不在這個 repo 裡的人**驗證了它能用。截至目前：
- 外部使用者：**0**
- 外部驗證：**0**
- 對外提交的 PR/Issue/Review：**0**

---

### 🔴 H-2：11,557 個 ops/ 檔案——前一輪找到 10,373 個，「修復」後反而增加了

```powershell
(Get-ChildItem .\ops -Recurse -File).Count  →  11,557
```

原始批評：820 MB 備份、10,373 個檔案、包含 Windsurf node_modules。

閉合備忘錄的回應：`.gitignore` 已排除、export scripts 不含這些內容。

**但這些檔案仍然存在，且數量增加了。** `.gitignore` 只防止進入 git，不代表 workspace 乾淨。`verify-workspace-hygiene.ps1` 可能只檢查 git-tracked 內容，而非 working directory 全部內容。

任何人 clone 這個 repo 後執行 bootstrap，不會遇到這些問題——**但這是在作者自己的機器上，不是別人的機器。** 混淆「workspace hygiene」與「release hygiene」依然存在。

---

### 🔴 H-3：13 個測試，36 個技能，沒有一個技能被端對端驗證「能用」

前一輪批評「測試只覆蓋安全邊界，不覆蓋核心功能」。

**這個問題完全沒有被解決。** 目前的 13 個測試測的是：
- bootstrap 能寫出 json 嗎？✅ 測試
- export 腳本能跑嗎？✅ 測試
- hygiene 腳本通過嗎？✅ 測試
- 任何一個 skill 能被 Claude Code 實際載入並使用嗎？❌ 沒有測試
- 任何一個 skill 能被 Codex 讀取嗎？❌ 沒有測試
- MCP server 在 Claude 對話中實際有響應嗎？❌ 沒有測試

UniText 的核心價值主張是「One definition. Every tool.」，但沒有任何一個測試驗證了這個主張的基礎。

---

### 🔴 H-4：審查鏈本身成為了文件膨脹的最佳例子，卻對「文件膨脹」問題毫無反思

前一輪批評文件比例失衡。解決方案？新增了這些文件：

1. `DEVILS_ADVOCATE_REVIEW_2026-03-26.md`
2. `DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md`
3. `DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md`
4. `DEVILS_ADVOCATE_REVIEW_CLOSURE_NOTE_2026-03-27.md`
5. `REVIEW_FINDINGS_REMEDIATION_PLAN_2026-03-27.md`
6. `ACT_06_REGRESSION_DISPOSITION_2026-03-27.md`
7. `PHASE_1_2_AUDIT_SUMMARY_2026-03-27.md`

**7 份新文件，用來處理「文件太多」的問題。** 這不是諷刺，這是工程文化的症狀：問題的回應是製造更多文件，而不是精簡行動。

---

## 三、質疑（MEDIUM）

### 🟡 M-1：36 個技能全部來自外部——UniText 自己有沒有「canonical content」？

UniText 的定位是「shared resource hub」。但檢查 `registry/skills/`，**所有 36 個技能目錄都是從外部 GitHub repo 引入的**：

- `superpowers-*`（~19 個）← obra/superpowers
- `affaan-*`（~3 個）← affaan-m/everything-claude-code
- `copilot-*`（~6 個）← github/awesome-copilot
- `nlb-*`（~3 個）← nextlevelbuilder/ui-ux-pro-max-skill
- `antigravity-*`（~2 個）← sickn33/antigravity-awesome-skills

UniText 本身**不創作任何 canonical resource**。它是一個 re-aggregation layer，套在其他人的作品上面。這不是不行，但「registry-first canonical hub」的定位 vs「aggregator」之間，有一個根本的概念矛盾需要誠實面對。

---

### 🟡 M-2：ACT-11（i18n 抽查）明確未完成，閉合備忘錄卻說「整體修補計畫接近完成」

閉合備忘錄原文：

> Phase 3 已完成 review chain 與文件收斂主體，但 i18n spot-check follow-up 尚未關閉。

但 i18n 製造了 6,761 個 Markdown 檔案中的絕大多數，是文件負債的最大來源。「i18n 抽查」不只是一個 nice-to-have follow-up，它是對於佔用絕大比例文件資源的品質把關。把它標為「open follow-up」，然後宣稱 Phase 3「已完成主體」，是在刻意縮小問題的嚴重性。

---

### 🟡 M-3：「市場需求」問題被明確列為 out-of-scope，而這恰恰是最根本的問題

原始反對意見第 8 點：「解決的問題可能不存在」。

修補計畫的範圍說明：

> **Out of Scope：重新設計 UniText 的核心產品方向**

這個決定本身可能是正確的（scope discipline 是好事），但它意味著：**「有多少人同時使用 4 個 AI CLI？」這個問題至今沒有答案，且計劃中不會有答案。**

在零外部使用者的情況下，所有「product-market fit」的問題都以「out of scope」略過，是一個需要誠實承認的風險，而非迴避的話題。

---

## 四、結構性觀察

### 🔵 S-1：「修復日期集中性」問題仍未解決

原始審查批評：「CLI_COMPAT_MATRIX.md 的 Last Verified 日期可疑地集中在 3 天內。」

現在的 CLI_COMPAT_MATRIX.md：

```
| Claude Code | ... | 2026-03-27 |
| Codex CLI   | ... | 2026-03-27 |
| Gemini CLI  | ... | 2026-03-27 |
```

三個 CLI 全部在同一天「驗證」。這不可能是獨立的深度驗證——最多是在同一台 Windows 機器上快速跑過一遍 delivery path 腳本。

---

### 🔵 S-2：39 個 commits，~4 天，1-2 位開發者——基本信任問題未解決

```
28  PingKuei Lin
11  root
```

整個專案在不到一週內從 0 到「Phase 1/2/3 完成」、「外部審查就緒」、「Template Release Candidate」。這個速度在沒有外部驗證的情況下，依然構成信任問題。

---

## 五、總結裁定

| 維度 | 前一輪判定 | 本輪判定 | 說明 |
|------|-----------|---------|------|
| 文件膨脹 | HIGH | 🔴 **WORSE** | 1,224 → 6,761 個 .md，22 倍增長 |
| 授權合規 | CRITICAL → 聲稱 fixed | 🟡 **PARTIALLY FIXED** | 問題轉移到 36 個外部 skills 的 skill-level 授權 |
| 跨平台 CI | HIGH | 🟡 **PARTIALLY FIXED** | CI 已不再是 windows-only；但 hosted evidence 目前主要落在 branch / PR scope，仍未完全等同於 default-branch baseline closure |
| 外部驗證 | HIGH | 🔴 **UNRESOLVED** | 依然 0 個外部使用者 |
| 功能測試覆蓋 | HIGH | 🔴 **UNRESOLVED** | 仍然沒有任何技能端對端測試 |
| ops/ 清理 | CRITICAL → 聲稱 fixed | 🟡 **PARTIALLY** | 11,557 檔案仍存在，只是 export 邊界隔離 |
| i18n 品質 | MEDIUM | 🔴 **WORSE** | 未完成且規模從未驗證 |
| 市場需求 | MEDIUM | 🔴 **OPEN / OUT OF SCOPE** | 明確不處理 |
| 工程可信度 | HIGH | 🟡 **PARTIALLY** | CI + 依賴管理存在，但功能覆蓋幾乎為零 |

---

## 六、本輪最終建議

> **不應將本次審查鏈的「閉合」視為真正的外部發布許可。**

前一輪審查鏈發現了真實問題並推動了真實改善（LICENSE、CI、dependency manifests、export boundary）。這是值得肯定的。

但「閉合」本身仍然是**自我宣告的**，且有三個根本未解決的問題：

1. **沒有一個外部使用者驗證過核心流程**
2. **branch / PR hosted CI 雖已補上跨平台證據，但 default-branch baseline 與長期穩定性仍需分開處理**
3. **沒有任何功能測試驗證「技能真的能被 CLI 使用」這個核心主張**

在這三個問題解決之前，「external review ready」應該被理解為：

> **「這份材料已經準備好讓外部人士閱讀和評估，但尚未被外部人士實際使用或驗證。」**

這是一個誠實且重要的區分。

---

*分析日期：2026-03-27*  
*分析立場：獨立反對方*  
*分析方法：全新探索 repo 結構、測量實際指標（6,761 .md / 11,557 ops files / 13 tests / 36 skills）、對照前一輪審查鏈聲明，以反對方立場撰寫*
