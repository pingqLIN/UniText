---
description: Remediation plan for issues raised by the devil's-advocate review set, with phased execution, deliverables, and exit criteria
---

# UniText 審查問題修補計畫書

> 文件目的：
> 針對 `DEVILS_ADVOCATE_REVIEW_2026-03-26.md`、`DEVILS_ADVOCATE_REVIEW_RESPONSE_2026-03-26.md`、`DEVILS_ADVOCATE_REVIEW_COMBINED_REVIEW_2026-03-27.md` 所指出的問題，整理一份可執行、可驗收、可對外說明的修補計畫。
>
> 文件日期：2026-03-27
> 文件定位：內部執行版 remediation plan / release gate plan

---

## 1. 執行摘要

本計畫的核心目標不是單純「修文件」，而是把 UniText 從目前的 authoring workspace 狀態，推進到一個可被合理驗證、可被安全打包、且可被誠實對外描述的 release candidate 狀態。

目前審查共識顯示，阻斷發布的問題主要集中在三類：

- **授權邊界不清**
- **workspace 衛生不足**
- **工程可信度不足**

因此，本計畫採三階段推進：

1. **Phase 1 — Release Blockers**
2. **Phase 2 — Engineering Credibility**
3. **Phase 3 — Documentation and Positioning Cleanup**

在 `Phase 1` 完成前，不應對外發布 starter package，也不應將目前工作區視為可直接公開的 release source。

---

## 2. 修補目標

本計畫完成後，UniText 應達成以下狀態：

- 專案自身與第三方內容的授權邊界清楚可說明
- authoring workspace 與 release package 的界線清楚
- 最小工程基線建立完成：
  - root-level 依賴管理
  - CI workflow
  - 可重跑測試
  - 安全文件與實作一致
- README、matrix、審查回應文件的說法與真實驗證範圍一致
- 可產生一份**乾淨、可驗證、無本機殘留**的 starter package

---

## 3. 範圍定義

### In Scope

- 授權與再分發邊界整理
- workspace 清理與 release hygiene
- 依賴管理與 CI 建立
- 測試補強與既有失敗修復
- 安全文件更新
- 跨平台與多 CLI 支持敘事收斂
- 根目錄與對外文件結構整理

### Out of Scope

- 重新設計 UniText 的核心產品方向
- 大規模重寫 registry 架構
- 新增大量新功能
- 全語言全面人工翻譯重做
- 新增未在目前 review 範圍內的 CLI support surface

---

## 4. 問題分組

| 問題群組 | 代表問題 | 目前影響 | 建議優先級 |
|---|---|---|---|
| `license-boundary` | Proprietary skills 再分發風險、根目錄 LICENSE 缺失 | 直接阻斷發布 | P0 |
| `workspace-hygiene` | `ops/history` 備份、本機路徑殘留、authoring/release 混線 | 直接阻斷發布 | P0 |
| `engineering-baseline` | 無 CI、無 root-level 依賴管理、測試窄 | 降低可信度 | P1 |
| `security-consistency` | 安全文件落後於實作、殘餘 legacy risk 未正確標示 | 高風險認知混亂 | P1 |
| `support-positioning` | README / matrix / evidence 對支持範圍描述過寬 | 容易過度承諾 | P1 |
| `docs-structure` | 根目錄文件過重、審查文件用途混雜 | 維護成本高 | P2 |
| `i18n-confidence` | 多語文件缺少抽查驗證 | 對外可信度有限 | P2 |

---

## 5. 執行原則

- **先阻斷風險，再優化敘事**
- **先修 release boundary，再修文件語氣**
- **程式碼、測試、文件三者必須同步更新**
- **所有「已修復」結論都必須有可重跑證據**
- **避免把 authoring workspace 現況誤寫成 release package 現況**

## 5.1 已定案的 skills 發布策略

為了優先完成交付，且避免擴大 scope，本計畫採以下策略：

### 採用方案

**方案 A：本地保留、公開版不附 proprietary skills、文件補充說明、後續補入公開授權 skills。**

### 不採用方案

**方案 B：先自行重寫一批 replacement skills。**

此方案雖然最乾淨，但會明顯拉長交付時間，因此目前不列入本輪修補計畫。

### 執行解釋

- authoring workspace 可暫時保留目前用於 dry-run 與功能驗證的本地 skills
- 公開版 repo / starter package / release artifact 不附上受限制的 proprietary skills 檔案
- 公開文件必須明確說明：
  - 某些本地驗證曾使用 local-only skills 驗證流程可運作
  - 這些材料不屬於可再分發內容，因此不納入公開 package
- 後續補充一批**公開授權**的 skills，作為公開版本的正式示例與驗證材料

### 這個策略的邊界

此策略的目標是**快速合法交付**，不是證明 proprietary skills 可以被安全再分發。

也就是說：

- 這是 release-boundary workaround
- 不是 license reinterpretation
- 不應在任何文件中暗示 proprietary skills 屬於公開版的一部分

---

## 6. Phase 1 — Release Blockers

## 6.1 目標

解除所有目前會阻斷對外發布的問題，建立明確的發布邊界。

## 6.2 工作項目

### ACT-01 授權邊界整理

**目標**

- 釐清 UniText 自有內容與第三方內容的授權範圍

**執行內容**

- 盤點 `registry/skills/` 中各 skill 的 license status
- 將 Proprietary skills 自可分發模板排除，並改為 pointer / install guide / excluded-from-release 說明模式
- 明確定義：
  - 哪些內容可進 starter package
  - 哪些內容只能作本地引用
  - 哪些內容只能保留在 authoring workspace
- 補一段正式說明：
  - local dry-run 可使用 local-only materials
  - public release 不包含這些 materials
  - 後續將補入公開授權的對應 skills 類型

**交付物**

- 根目錄 `LICENSE`
- 第三方內容授權說明文件
- template export exclusion 規則更新

**驗收標準**

- 能清楚回答「此 package 是否包含 Anthropic Proprietary materials」
- 公開版答案必須是：**不包含**
- export package 中不再含有不可再分發內容

### ACT-02 Workspace 清理與邊界隔離

**目標**

- 讓 authoring workspace 不再與可發布來源混淆

**執行內容**

- 清除或搬移 `ops/history` 中不應保留於 repo 工作區的備份內容
- 確認 `.gitignore` 與 export scripts 不會把這些內容帶入 package
- 補一份 workspace vs tracked vs exported 三層邊界說明

**交付物**

- 清理後的工作區
- hygiene 檢查結果
- export package inclusion / exclusion 說明

**驗收標準**

- export 結果不包含本機絕對路徑、編輯器安裝內容、個人目錄痕跡
- release hygiene 檢查可重跑

### ACT-03 建立正式 LICENSE 與 release policy

**目標**

- 補齊正式 release 基本文檔

**執行內容**

- 新增根目錄 `LICENSE`
- 在 `README.md`、`TEMPLATE_RELEASE_PACKAGE.md`、`NO_PUBLISH_POLICY.md` 中對齊授權與發布邊界
- 加入「公開版 skills 收錄原則」：
  - 只收可公開再分發內容
  - proprietary materials 僅作本地驗證，不作公開發佈

**交付物**

- 正式 `LICENSE`
- 對齊後的 release policy 文件

**驗收標準**

- README 與 LICENSE 不再互相矛盾
- 能明確說明 UniText 自身內容與第三方內容的授權範圍

## 6.3 Phase 1 Exit Criteria

- Proprietary skills 已從可分發包排除，或已明確改成不可再分發模式
- 根目錄 `LICENSE` 已建立
- `ops/history` 類本機殘留不再影響 release source 判定
- 可以產生一份初步乾淨的 export package

---

## 7. Phase 2 — Engineering Credibility

## 7.1 目標

建立最小但可信的工程基線，讓 release readiness 不再只靠文字敘述。

## 7.2 工作項目

### ACT-04 建立 root-level 依賴管理

**目標**

- 讓 repo 的 Python 依賴可被一致安裝與驗證

**執行內容**

- 建立 `pyproject.toml` 或根目錄 `requirements.txt`
- 將目前實際使用的依賴整理為可安裝清單
- 區分：
  - core runtime 依賴
  - optional tooling 依賴
  - skill-local 依賴

**交付物**

- root-level dependency manifest
- 安裝說明更新

**驗收標準**

- 新環境可依單一入口完成核心依賴安裝

### ACT-05 建立最小 CI workflow

**目標**

- 將最基本的品質門從人工執行提升到自動檢查

**執行內容**

- 建立 `.github/workflows/ci.yml`
- 至少包含：
  - Python setup
  - dependency install
  - 安全 hardening tests
  - export / verify 類 smoke checks

**交付物**

- 可執行的 GitHub Actions workflow

**驗收標準**

- push / PR 時可自動執行最小檢查

### ACT-06 補強測試與修復歷史失敗

**目標**

- 讓關鍵流程有可重跑的回歸保護

**執行內容**

- 將 pre-push audit 中 4 個失敗項轉為現在仍可重跑的測試案例
- 補充：
  - bootstrap smoke tests
  - export / verify flow tests
  - release hygiene tests
  - safety regression tests

**交付物**

- 擴充後的 `tests/`
- 修復後的失敗案例

**驗收標準**

- 歷史 4 個失敗測試均有處置結果：
  - fixed
  - replaced by updated test
  - explicitly deprecated with rationale

### ACT-07 更新安全文件與實作對齊

**目標**

- 消除「程式碼已修，文件仍寫未修」的狀況

**執行內容**

- 更新：
  - `SECURITY_REVIEW_ADVISORY.md`
  - `SECURITY_ATTACK_INPUT_RESPONSE_REPORT.md`
- 將每個 finding 改為：
  - current status
  - residual risk
  - validation evidence

**交付物**

- 更新後的安全文件

**驗收標準**

- 安全文件與目前程式碼行為一致
- 不再出現明顯過時的「未修復」敘述

### ACT-08 收斂支持敘事

**目標**

- 讓 README、matrix、evidence 文件的說法與實際驗證範圍一致

**執行內容**

- 將支持語句統一成三類：
  - `verified`
  - `partial`
  - `target`
- 明確區分：
  - delivery path verified
  - bootstrap verified
  - end-to-end verified
- 明確區分：
  - authoring review shortlist
  - public release subset
  - local-only validation materials

**交付物**

- 更新後的 `README.md`
- 更新後的 `local/docs/CLI_COMPAT_MATRIX.md`

**驗收標準**

- 文件不再形成過度承諾
- 外部讀者可清楚理解哪些平台是目標、哪些是已驗證

## 7.3 Phase 2 Exit Criteria

- root-level 依賴管理已建立
- 最小 CI 已上線
- 歷史失敗項已有明確處置
- 安全文件與程式碼一致
- 支持矩陣與 README 敘事已收斂

---

## 8. Phase 3 — Documentation and Positioning Cleanup

## 8.1 目標

降低文件維護成本，讓對內與對外敘事一致。

## 8.2 工作項目

### ACT-09 文件結構整理

**目標**

- 讓根目錄保留高訊號文件

**執行內容**

- 將 review、analysis、advisory 類文件移入更明確的 docs / reviews 區域
- 保留根目錄核心文件：
  - README
  - INDEX
  - VISION
  - RESOURCE_SPEC
  - OPERATIONS
  - TEMPLATE_RELEASE_* 等
- 針對 skills 另補一份 release selection note，說明：
  - 為何本地驗證使用特定 skills
  - 為何公開版先排除
  - 公開授權 replacement wave 的補入方向

**交付物**

- 整理後的文件結構

### ACT-10 建立正式審查回應鏈

**目標**

- 讓原始反對意見、技術回應、綜合判定三者關係清楚

**執行內容**

- 將原始反對意見書標為 historical snapshot
- 將 response 文件標為 code-state verification
- 將 combined review 文件標為 current decision basis

**交付物**

- 文件 metadata 與用途標示更新

### ACT-11 i18n 抽查

**目標**

- 提升多語文件可信度

**執行內容**

- 挑選 2 到 3 種非中文 / 英文語言
- 抽查核心文件：
  - `README.md`
  - `OPERATIONS.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
- 記錄用語不一致、翻譯漂移、明顯 machine-translation 問題

**交付物**

- i18n 抽查報告

## 8.3 Phase 3 Exit Criteria

- 根目錄文件訊號更集中
- 審查文件用途清楚
- 多語文件至少完成抽樣信心檢查

---

## 9. 推薦執行順序

```text
Phase 1
  ACT-01 授權邊界整理
  ACT-02 Workspace 清理與邊界隔離
  ACT-03 建立正式 LICENSE 與 release policy

Phase 2
  ACT-04 建立 root-level 依賴管理
  ACT-05 建立最小 CI workflow
  ACT-06 補強測試與修復歷史失敗
  ACT-07 更新安全文件與實作對齊
  ACT-08 收斂支持敘事

Phase 3
  ACT-09 文件結構整理
  ACT-10 建立正式審查回應鏈
  ACT-11 i18n 抽查
```

### 9.1 Skills 相關的實際落地順序

為了符合「先快交付、再補公開授權 skills」的決策，本計畫對 skills 採以下順序：

1. 先把公開版 release surface 中的 proprietary skills 排除
2. 補上公開文件說明，避免外界誤解為缺漏或失誤
3. 保留 generic example skill 作為最小 template-safe 例子
4. 再逐步補入公開授權 skills，優先補：
   - 文件類
   - 結構化資料類
   - QA / testing 類
   - builder / workflow 類

這樣做的目的，是先完成合法交付，再逐步恢復示例密度與說服力

---

## 10. 風險與對策

| 風險 | 說明 | 對策 |
|---|---|---|
| scope creep | 修補過程變成重構專案 | 嚴守本計畫的 in-scope 項目 |
| license ambiguity | 第三方內容授權仍難明確界定 | 先採保守策略：從分發面排除 |
| stale documents | 程式碼修了但文件沒同步 | 將文件更新列為每個 phase 的交付物 |
| false confidence | 補少量測試後誤判已 ready | 使用 exit criteria，而非主觀感受 |
| narrative drift | README 與 evidence 再次失配 | 將支持語句統一為 `verified / partial / target` |

---

## 11. 驗收方式

本計畫不以「看起來比較整齊」為完成標準，而以以下方式驗收：

- 文件驗收：
  - README / LICENSE / security docs / review docs 是否互相一致
- 工程驗收：
  - CI 是否可執行
  - 關鍵測試是否可重跑
- hygiene 驗收：
  - export package 是否乾淨
  - 是否仍殘留本機路徑痕跡
- release 驗收：
  - 是否能清楚說明可發布範圍
  - 是否還存在 P0 阻斷項

---

## 12. 最終決策門檻

只有在以下條件全部成立時，才可重新評估對外發布：

1. `Phase 1` 全部完成
2. `Phase 2` 至少完成核心項：
   - 依賴管理
   - 最小 CI
   - 歷史失敗處置
   - README / matrix 收斂
3. export package 經過 verify
4. 對外敘事可誠實表述目前支持範圍
5. 公開版已清楚區分：
   - included public skills
   - excluded local-only proprietary materials

若上述任一項未完成，建議維持：

> **Do not publish current authoring workspace or starter package yet.**

---

## 13. 第二輪審查增補項

2026-03-27 的第二輪外部審查 `DEVILS_ADVOCATE_REVIEW_2026-03-27.md` 指出：前述 Phase 1 / 2 / 3 雖已修補原始 blocker，但仍存在數個 closure 後才變得明顯的 confidence gaps。

這些增補項不應被解讀為「前述修補全部無效」，而應被視為：

- post-remediation confidence hardening
- release narrative strengthening
- external trust building

### 13.1 已採納為正式新增工作項

以下項目已被納入正式修補清單：

- `ACT-12` 文件規模治理
  - 回應 `.md` 規模膨脹、review archive / i18n 導致的文件量失真，以及 stale translation 可見性不足
- `ACT-13` skills provenance 強化
  - 回應目前多數 skill 僅具 repo-level license / source mapping，缺少 path-level provenance 與 confidence 分級
- `ACT-14` cross-platform confidence expansion
  - 回應當時 CI 僅有 `windows-latest`、無法支撐 macOS / Linux 的 portable 敘事；目前已補上 cross-platform smoke workflow 與 branch / PR hosted evidence
- `ACT-15` CLI functional proof tests
  - 回應目前測試偏重 wiring / export / hygiene，而缺少 shared skill / MCP 真正可被消費的 proof artifact
- `ACT-16` independent operator validation
  - 回應目前驗證仍高度依賴作者本人與 repo 內自寫腳本

### 13.2 未採納為本輪工程工作項，但保留為 watchlist

以下問題保留為治理或策略風險，不納入本輪工程修補：

- 市場需求 / product-market fit
- UniText 與「pure aggregator」定位的產品敘事問題
- 快速開發節奏造成的信任觀感問題

這些問題值得誠實記錄，但不適合在目前 remediation plan 中偽裝成可短期驗收的工程項目。

### 13.3 增補文件

本節對應的正式增補說明見：

- [SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md](SECOND_ROUND_REMEDIATION_ADDENDUM_2026-03-27.md)

---

## 14. 一句話總結

**本修補計畫的目的，不是把反對意見壓掉，而是把其中成立的問題逐一轉成可驗收的工程與文件工作，直到 UniText 能被誠實且安全地對外發布。**
