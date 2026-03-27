---
description: Consolidated review of DEVILS_ADVOCATE_REVIEW_2026-03-26.md and its response, with current-state corrections and action plan
---

# DEVILS_ADVOCATE_REVIEW 綜合審查

> 角色：`current decision basis`
> 審查對象：
> - `DEVILS_ADVOCATE_REVIEW_2026-03-26.md`
> - `DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md`
> - 相關佐證文件與目前程式碼狀態
>
> 綜合日期：2026-03-27
> 目的：整合原始反對意見、獨立驗證回應、以及當前 repo 狀態檢查，形成一份可直接採用的決策文件。

---

## 一、綜合結論

這兩份審查的**核心方向一致**：

- 在目前狀態下，**不應直接發布 authoring workspace**
- 發布阻斷問題主要集中在：
  - 授權邊界不清
  - 工作區衛生與本機備份殘留
  - 工程可信度不足

但兩份文件也都有需要修正之處：

- 原始反對意見書的部分敘述**已落後於目前程式碼狀態**
- 回應文件雖補上了許多程式碼層級事實，但部分結論仍需要再區分：
  - `authoring workspace`
  - `tracked repository surface`
  - `clean release/template package`

**最終裁定**：

1. **原始反對意見書的發布結論可以保留**
2. **但證據鏈、時間切面、與嚴重度標示必須更新**
3. **回應文件應作為新的基礎版本**
4. **對外使用時，應以「截至 2026-03-27 的綜合判定」取代單獨引用任一份文件**

---

## 二、確認成立的主張

以下主張在綜合審查後仍然成立，且應保留為正式風險項：

### 1. 授權風險為真實阻斷項

- `pdf`、`docx`、`pptx`、`xlsx` 等 skills 的授權文字確實包含 Anthropic 專有條款與禁止再分發限制
- 這不是文件觀感問題，而是**發布邊界問題**
- 根目錄目前缺少正式 `LICENSE` 檔，讓授權敘事更混亂

**結論**：在釐清「哪些內容可再分發、哪些只能本地使用」之前，不應發布 starter package。

### 2. 工作區衛生問題為真實阻斷項

- `ops/history` 內確實存在大量本機備份與個人路徑痕跡
- 這代表目前的 authoring workspace **不能直接視為可發布來源**
- 即使 `.gitignore` 已排除 `ops/history/`，仍需清楚區分：
  - 「目前 git tracked 內容」
  - 「目前工作區殘留內容」
  - 「最終 export package 實際包含內容」

**結論**：這是 release hygiene 問題，不只是視覺上的凌亂。

### 3. 工程可信度仍不足

- 沒有正式 CI workflow
- 沒有 root-level 的統一依賴管理
- 測試覆蓋仍偏窄，且歷史 audit 顯示曾有 4 項失敗
- 跨平台與多 CLI 的宣稱仍以文件敘述多於可重複驗證證據

**結論**：即使安全腳本已有部分修復，整體工程成熟度仍不足以支撐強烈的 release-ready 敘事。

---

## 三、需要修正的原始審查內容

以下是原始反對意見書中，最需要修正的地方。

### 1. 授權段落的證據鏈有誤

原文寫「根目錄 LICENSE 是 MIT」，但目前實際狀況是：

- `README.md` 聲明 `MIT`
- 根目錄卻**沒有** `LICENSE` 檔
- `PRE_PUSH_AUDIT_2026-03-26.md` 也把缺少 `LICENSE` 列為 blocker

**建議改寫**：

> 目前 repo 文件層宣稱 MIT，但正式 LICENSE 檔缺失，且部分 skills 受第三方專有限制，導致授權邊界不清，故不應發布。

### 2. 安全段落需要改成「歷史發現 + 目前殘餘風險」

原始反對意見書把多項安全問題寫成「未修復」，但目前程式碼狀態顯示：

- `rollback-skills.ps1` 已加入 safe path 驗證
- `batch-adopt-skills.ps1` 已加入 boundary check 與 reparse point 檢查
- `bootstrap.py` 已預設拒絕 external repo root
- `with_server.py` 已改為預設 JSON-only，僅在 `--allow-shell` 下保留 legacy shell mode

**因此更準確的表述應是**：

- `SEC-002`、`SEC-003` 已有顯著修復
- `SEC-001` 不應再寫成「預設 shell=True」，而應寫成「仍保留顯式 opt-in shell mode」
- 真正的問題變成：
  - 文件未更新
  - 風險仍存在於 legacy 或 opt-in 路徑
  - 尚未形成完整的 regression test 與 CI gate

### 3. 測試段落要分清「歷史 audit」與「目前 tree」

原始文件把 `25/29` 與 `4 failed` 直接寫進結論，但這是 `PRE_PUSH_AUDIT_2026-03-26.md` 的歷史快照。

目前可直接定位到的核心測試來源為：

- `tests/security/test_hardening.py`

而且現況檢查中，該檔可執行並通過。

**建議改寫**：

> 歷史 pre-push audit 顯示 29 項測試中有 4 項失敗；目前可見的安全 hardening 測試已通過，但整體測試面仍不足。

### 4. 跨平台段落要收斂語氣

原始文件把 README 的說法解讀得比實際更強。

目前較準確的描述應是：

- README 將 `Copilot CLI` 明確標為 `adapter pending`
- `CLI_COMPAT_MATRIX.md` 也寫明 `delivery path verified` 不等於 E2E 驗證
- 問題不在於「完全虛假宣稱」，而在於「支持範圍與驗證證據仍有落差」

---

## 四、對回應文件的補充修正

`DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md` 已經比原始反對意見書更接近現況，但還有三點建議補強。

### 1. 要更明確區分 workspace 與 release surface

回應文件正確指出 `.gitignore` 已排除 `ops/history/backup_*`，但對外決策時仍應進一步區分：

- authoring workspace 現況不可直接發布
- tracked repo surface 不等於工作區全部內容
- release package 還需經過 export 與 verify 才能判定是否安全

### 2. `SEC-001` 不應被視為完全解決

回應文件正確指出 `with_server.py` 預設已不再接受 shell string，但：

- `--allow-shell` 仍保留高風險路徑
- 若此腳本未來被 agent wrapper 直接採用，仍需被視為高敏感接口

**因此應標示為**：

- 已緩解，但尚未完全退役 legacy risk

### 3. 「文件 vs 程式碼比例失衡」應改為定位問題，而非單純缺陷

若 UniText 的定位是：

- registry-first shared resource hub
- documentation-heavy operating model

那高文件比例本身不是 defect。

更好的判準應是：

- 文件是否與程式碼一致
- 文件是否過度超前於可驗證能力
- 根目錄與外部敘事是否造成誤導

---

## 五、建議採納的正式版本

若要對內或對外引用，建議採用以下表述：

> UniText 在目前狀態下，不應直接發布 authoring workspace，也不應在未釐清授權範圍前發布 starter package。主要阻斷原因是：
> 1. 第三方專有 skills 的再分發邊界不清
> 2. authoring workspace 含有不應進入發布面的本機備份與路徑痕跡
> 3. 工程可信度仍不足，包括缺少 CI、依賴管理不足、測試與跨平台驗證證據不夠完整
>
> 同時，原始反對意見書中關於部分安全項目的描述已落後於目前程式碼，應更新為「已部分修復但仍需持續驗證」。

---

## 六、整合後的建議行動

### P0 — 發布阻斷項

1. 釐清授權邊界：
   - 將 Proprietary skills 從可分發模板中移除，或改為 pointer / install guide 模式
2. 清理 authoring workspace：
   - 清除或隔離本機備份
   - 確認 export package 不包含任何本機路徑殘留
3. 新增正式根目錄 `LICENSE`：
   - 明確寫出 MIT 僅涵蓋 UniText 自身內容
   - 第三方內容採個別授權說明

### P1 — 工程可信度

4. 建立 root-level 依賴管理
5. 建立最小 CI workflow
6. 將歷史 pre-push failures 轉成可重跑的 regression tests
7. 更新 `SECURITY_REVIEW_ADVISORY.md` 與相關安全結論
8. 將 README / matrix 的支持語句收斂為 `verified / partial / target`

### P2 — 文件與產品敘事

9. 將原始反對意見書改寫為「歷史反對方快照」
10. 將回應文件改寫為「程式碼現況驗證」
11. 保留本綜合文件作為最終決策版
12. 進行 i18n 抽查與根目錄文件收斂

---

## 七、推薦文件用途

建議三份文件的定位如下：

- `DEVILS_ADVOCATE_REVIEW_2026-03-26.md`
  - 保留為原始反對觀點
  - 不建議直接作為唯一決策依據

- `DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md`
  - 保留為程式碼層級回應
  - 適合作為修正原始審查的技術附件

- `DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md`
  - 作為目前最平衡、最可引用的綜合判定

---

## 八、最終一句話結論

**「不應發布」這個方向是對的，但理由必須更新。真正準確的說法不是『整個專案不可用』，而是『在授權、工作區衛生、與工程可信度三項未完成前，不應將目前的 UniText 工作區或 starter package 對外發布』。**
