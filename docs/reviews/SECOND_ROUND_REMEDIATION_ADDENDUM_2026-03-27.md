---
description: Addendum remediation plan responding to the fresh 2026-03-27 independent devil's-advocate review, separating adopted actions from watchlist risks
---

# 第二輪審查修補增補計畫

> 來源文件：`DEVILS_ADVOCATE_REVIEW_2026-03-27.md`
> 日期：2026-03-27
> 目的：針對第二輪外部審查中「前一輪尚未確認」或「閉合後才顯現」的問題，篩選出應納入正式修補計畫的項目，並將純觀察性風險與可執行工作區分開。

## 一、採納原則

本增補計畫只納入以下類型的問題：

- 有可量測證據支持
- 可轉成明確交付物
- 可定義驗收標準
- 不會把本輪修補計畫擴大成產品重設或策略重寫

不直接納入本輪執行的觀察，將保留為：

- watchlist risk
- positioning note
- governance concern

## 二、第二輪審查項目分流

| 第二輪主張 | 判定 | 處理方式 |
|---|---|---|
| Markdown 規模從 1,224 升到 6,762 | 採納 | 納入 `ACT-12` 文件規模治理 |
| 36 個外部 skills 僅有 repo-level license 記錄 | 採納 | 納入 `ACT-13` provenance 強化 |
| CI 仍為 Windows-only | 採納 | 納入 `ACT-14` cross-platform confidence expansion |
| 自我腳本驗證缺少獨立驗證 | 採納 | 納入 `ACT-16` independent operator validation |
| 沒有技能真正被 CLI 端對端使用的證據 | 採納 | 納入 `ACT-15` CLI functional proof tests |
| `ops/` 11,557 檔案仍存在 | 部分採納 | 納入 `ACT-12` 指標治理，不重開 `ACT-02` blocker |
| 審查鏈自己加重文件膨脹 | 部分採納 | 納入 `ACT-12` 文件分類與成長預算 |
| UniText 幾乎全是外部 skill aggregation | 記錄但不納入 | positioning note，不在本輪重寫產品定義 |
| 市場需求 / product-market fit 未證明 | 記錄但不納入 | strategy watchlist，維持 out-of-scope |
| 驗證日期集中於同一天 | 部分採納 | 透過 `ACT-14` / `ACT-16` 拉開驗證來源與時間面 |
| 4 天、1-2 人快速完成造成信任疑慮 | 記錄但不納入 | governance observation，不作工程工作項 |

## 三、正式新增工作項

### ACT-12 文件規模治理

**目標**

- 將文件數量與分類從「被動膨脹」轉成「可說明、可追蹤、可收斂」

**執行內容**

- 建立文件盤點報表，至少區分：
  - root canonical docs
  - review archive
  - i18n translations
  - local / script docs
- 為 `README.md` 與 `docs/reviews/README.md` 補上 authoritative-document 說明
- 定義譯本 stale 規則：
  - 英文主文件為 authoritative version
  - 譯本若未同步 release-boundary 或 support-baseline 更新，需標示 stale
- 建立文件成長監測基線，至少追蹤：
  - `.md` file count
  - `ops/` file count
  - i18n / review archive 佔比

**交付物**

- 文件盤點報告
- 文件分類 / authoritative-language 規則
- 文件規模基線記錄

**驗收標準**

- 能清楚說明為何 `.md` 數量高於前一輪
- 能區分 canonical docs 與 i18n / review archive 膨脹來源
- 非英文譯本的 stale 狀態可被外部讀者辨識

### ACT-13 Skills provenance 強化

**目標**

- 將目前偏向 repo-level 的授權與來源敘事，補強為可追溯到 import 單位的 provenance 鏈

**執行內容**

- 擴充 `SOURCE.yaml` 所需欄位，至少包含：
  - upstream repo
  - upstream path
  - imported revision / commit
  - import date
  - license scope note
  - provenance confidence
- 補一份 provenance audit，說明：
  - 哪些 skills 僅依賴 repo-level license
  - 哪些 skills 有更細的檔案 / 路徑級來源證據
- 對 public subset skills 增加 provenance confidence 標示

**交付物**

- 更新後的 `SOURCE.yaml` schema
- provenance audit 文件
- public subset provenance confidence matrix

**驗收標準**

- 每個 public skill 都有可重建的 upstream path 與 revision
- 可以區分「repo-license-relied-upon」與「path-level provenance stronger evidence」

### ACT-14 Cross-platform confidence expansion

**目標**

- 讓目前的 portable / target 敘事不只依賴 Windows 驗證

**執行內容**

- 將 CI 擴充為：
  - `windows-latest` 維持完整 baseline
  - `ubuntu-latest` 至少執行 Python smoke / bootstrap dry-run / tests
  - `macos-latest` 至少執行 Python smoke / bootstrap dry-run / tests
- 若某些 PowerShell-only 步驟無法跨平台，需在 workflow 與文件明確切分 smoke scope
- 更新 README / matrix 的 wording，使其對應實際 CI 驗證面

**交付物**

- 更新後的 `.github/workflows/ci.yml`
- cross-platform smoke 說明

**驗收標準**

- macOS 與 Linux 至少有 machine-readable smoke evidence
- 不再只有 Windows job 承擔全部 portable 敘事

### ACT-15 CLI functional proof tests

**目標**

- 補足目前只有 delivery / export / safety 測試、但缺少「資源真的可被消費」證據的缺口

**執行內容**

- 為每個目前聲稱的 support class 補至少一種 proof artifact：
  - shared skill delivered to expected location
  - skill metadata readable by target path / config
  - MCP baseline can start and answer a minimal request
- 若完整 CLI conversation automation 不可行，至少建立：
  - contract-level smoke harness
  - path + config + parser + process-start proof
- 將 README 中的 `verified / partial` 與對應 proof artifact 連起來

**交付物**

- proof-oriented test cases or harnesses
- support claim ↔ proof artifact 對照表

**驗收標準**

- 每一個 `verified` 或 `partial` 支持敘事，都能指向至少一個功能性 proof，而不只是 delivery wiring

### ACT-16 Independent operator validation

**目標**

- 降低「自己寫腳本驗證自己腳本」造成的自我閉合風險

**執行內容**

- 準備一份非作者驗證 runbook
- 要求至少一位非 author 的 operator 執行：
  - bootstrap
  - verify
  - review package export
  - template package export / verify
- 將結果記錄為：
  - 成功 / 失敗
  - 使用平台
  - 是否需人工補救

**交付物**

- independent validation checklist
- independent validation report

**驗收標準**

- 至少有一份非作者驗證紀錄
- 對外敘事可區分 self-validation 與 independent validation

## 四、目前不納入本輪修補計畫的觀察

以下問題成立為風險或討論點，但不納入本輪工程修補清單：

### 1. 市場需求 / product-market fit

這是有效質疑，但屬於策略驗證，不屬於本輪 release remediation 的 in-scope。

### 2. UniText 是否應自稱 canonical content hub

這是定位與敘事問題。現階段較適合透過 README / positioning note 收斂，不宜在本輪重寫產品定義。

### 3. 開發速度與日期集中造成的信任感問題

這是治理觀感問題，真正能改善的途徑仍是：

- 拉開驗證來源
- 增加 cross-platform evidence
- 增加 independent validation

## 五、建議採納方式

建議不要把第二輪審查當成「重開所有 blocker」，而是採以下說法：

> 第一輪 blocker 多數已修補；第二輪審查則指出 closure 後仍存在 confidence gaps。這些缺口主要集中在文件規模治理、skill provenance 深度、cross-platform smoke evidence、CLI functional proof、以及獨立驗證來源。

因此，建議將本文件視為：

- Phase 1 / 2 / 3 之後的 confidence-hardening addendum
- 而不是重新宣告前述修補全部無效
