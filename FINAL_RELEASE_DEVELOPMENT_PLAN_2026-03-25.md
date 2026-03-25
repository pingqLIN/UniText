# UniText 最終開發規劃書

> 日期：2026-03-25  
> 版本：說明書版  
> 角色：專案總指揮版本  
> 目標：以今日發布為前提，將 UniText 收斂到可辯護、可驗證、可放行的 `template release candidate`

## 0. 文件定位

這份文件不是單純的待辦清單，也不是一般的 sprint planning note。

它的角色是：

- 給專案核心維護者做最終決策用的總指揮文件
- 給協作開發者做執行對齊用的任務說明書
- 給外部審查者理解「為什麼今天能發，或為什麼今天不能發」的判斷依據

因此，這份文件會同時回答三件事：

1. `UniText` 今天要發布，真正缺的是什麼
2. 每一個缺口應該如何處理，技術上怎麼落地
3. 什麼證據足以放行，什麼情況必須直接否決發布

這份文件特別強調前後文，是因為 `UniText` 不是單一用途的小型 app，而是一個帶有：

- registry
- adapter / operations control plane
- template export
- rebuild export
- cross-platform bootstrap
- reviewer-facing package

等多重面向的共享基線專案。

在這種專案裡，真正的發布問題通常不會只出在某一支腳本或某一份 README，而是出在：

- discovery truth
- release truth
- export truth
- verification truth

沒有被收斂成同一套答案。

## 1. 專案背景與核心定位

### 1.1 UniText 是什麼

根據目前專案核心文件，`UniText` 的正式定位已相當清楚：

- 它不是單純的 skills 倉庫
- 它不是單一 CLI 的設定集合
- 它不是某位作者私人工作區的備份集合

它的正式定位是：

> 一個 text-native、registry-first、AI-first 的 shared resource hub

也就是說，`UniText` 的核心價值不在於「裡面剛好有多少 skill」，而在於它試圖提供一個統一的純文本契約，讓多個 AI CLI 與 agent 系統共享同一套 canonical resources。

這個目標本身是成熟且成立的。問題不在願景，而在今天要發布時，這個願景是否已經透過：

- 文檔
- 腳本
- package
- metadata
- 驗證

被收斂成對外一致的產品表面。

### 1.2 為什麼今天不能只看「功能有沒有」

`UniText` 現在不是從零開始，它已經有：

- `registry/`
- `local/scripts/`
- `ops/`
- review package
- template package
- rebuild package
- bootstrap / verify 路徑
- runnable MCP baseline

所以今天的問題不是「這個專案還沒做出來」，而是：

> 它是否已經到了可以對外自信宣稱為 `template release candidate` 的程度

這個判斷，不能只看功能存在與否，而要看：

- 文檔是否一致
- catalog 是否可信
- release 邊界是否清楚
- 控制面是否沒有明顯阻斷風險
- exported package 是否比 authoring workspace 更乾淨
- verify 是否真的能支撐發布說法

## 2. 指揮結論

### 2.1 今日發布的總判斷

`UniText` 今天不應以 authoring workspace 本體對外發布。

今天唯一合理的主發布物應是：

- `template package`

今天不建議主打：

- authoring repo 直接可發布
- `rebuild package` 與 `template package` 雙主發布
- 泛稱「整體治理已跨平台完成」

### 2.2 為什麼要這樣定義

這個結論不是保守，而是準確。

原因在於：

- authoring workspace 目前仍是高活躍狀態
- repo 內同時存在大量 ops 歷史產物與 review / template / rebuild 產物
- 工作樹仍有大量變更
- 文檔與實際 registry surface 仍有漂移

在這種情況下，把 authoring repo 本體當成發布物，等於把「工作現場」誤認成「產品包」。

這對一般 app 可能勉強還能辯護，但對 `UniText` 這種以規格、catalog、registry、delivery governance 為核心價值的專案而言，這是不能接受的。

### 2.3 今日發布要成立的最低條件

今日發布若要成立，必須先補齊五個任務面：

1. Catalog / Registry / Source-of-Truth 對齊
2. Release Surface / Template / Rebuild 邊界清理
3. Cross-Platform `bootstrap / verify / test coverage` 補齊
4. 安全與控制面 Hardening 收尾
5. 發布證據、工作樹清理、Go/No-Go Gating

這五項不是平行可選項，而是同一條發布鏈上的五個關節。

只要其中任何一項保持模糊，今天的發布就會退回：

- 敘事不一致
- package 邊界不穩
- 驗證不充分
- 安全風險未封口
- 放行依據不足

## 3. 發布目標

### 3.1 今日發布目標

- 將 `UniText` 對外定位為 `template release candidate`
- 將 exported `template package` 作為唯一放行對象
- 以可重複的 `dry-run -> export -> verify -> first-run proof` 證據鏈作為放行基礎

### 3.2 今日不追求的目標

- 不追求把所有 authoring 狀態清到零
- 不追求一次完成完整三平台矩陣
- 不追求把所有歷史安全與治理議題一次重構完畢
- 不追求同一天把 template 與 rebuild 都做成主敘事發布

### 3.3 為什麼要明確寫「今日不追求」

這一段很重要。

很多專案在發布前會陷入一種錯覺：只要再多補幾件事，就能順手把所有長期技術債一起還掉。結果往往是：

- 發布不但沒有更穩
- 還把本來已接近收口的事情重新打開

`UniText` 今天的任務不是「把專案做到完美」，而是「把今天這次發布需要的真相說準、邊界畫清、證據做足」。

## 4. 核心判斷

根據本輪重新閱讀核心文件與成對子代理審查，`UniText` 的理論架構已成熟：

- `README.md`
- `VISION.md`
- `INDEX.md`
- `TEMPLATE_RELEASE_PACKAGE.md`
- `TEMPLATE_RELEASE_CHECKLIST.md`
- `PROJECT_STATUS_REPORT_2026-03-23.md`

目前真正阻礙今日發布的，不是缺少架構，而是以下五種「已具備雛形，但尚未完全收斂」的問題：

- `discovery truth`、`release truth`、`export truth` 尚未完全一致
- `template/rebuild` 邊界仍有文件與腳本矛盾
- `cross-platform` 敘事超前於測試證據
- 控制面仍存在少數發布阻斷風險
- 發布證據尚未形成單一放行鏈
- 任務中斷後的半寫入、編碼殘缺、部分產物覆蓋風險尚未被正式納入發布控制面

換句話說，這是一個「接近可發布，但不能靠樂觀補完」的狀態。

## 5. 任務總覽

| 任務 | 優先級 | 今日門檻 | 指揮說明 |
|---|---|---|---|
| Task A: Catalog / Registry / Source-of-Truth 對齊 | P0 | 必須完成 | 先統一專案到底在說哪一套真相 |
| Task B: Release Surface / Template / Rebuild 邊界清理 | P0 | 必須完成 | 先把要發布的東西和作者工作區切開 |
| Task C: Cross-Platform `bootstrap / verify / test coverage` 補齊 | P0 | 必須完成到最小可接受線 | 先讓跨平台承諾和證據一致 |
| Task D: 安全與控制面 Hardening 收尾 | P0 | 必須完成發布阻斷項 | 先把會直接破壞發布可信度的風險封口 |
| Task E: 發布證據、工作樹清理、Go/No-Go Gating | P0 | 必須完成 | 最終要有證據，不是只有信心 |

---

## Task A：Catalog / Registry / Source-of-Truth 對齊

### 1. 目標問題

目前 `INDEX.md`、review package、status report、實際 `registry/skills` 同時承載了兩種語義，但未正式分流：

- `full registry surface`
- `curated review surface`

這件事不是單純漏寫幾行 catalog。

它真正代表的是：專案現在同時存在兩套真相來源，但沒有在制度上說清楚哪一套回答哪一個問題。這對 `UniText` 這類 registry-first 專案尤其致命，因為它的產品表面本來就包含：

- 這裡有什麼
- 哪些是 canonical
- 哪些是 review / release 主集

如果這三件事沒有對齊，那麼：

- AI agent 讀到的入口不準
- 人類維護者對專案範圍的理解不準
- review package 與主 repo 的敘事會持續分裂

### 2. 執行處理方式與技術

- 先做語義決策：
  - `INDEX.md` 要嘛回到 `full registry catalog`
  - 要嘛明確降格為 `review shortlist catalog`，並新增另一份 `full registry catalog`
- 今日建議採：
  - `INDEX.md` 仍作 discovery 入口
  - 但明確區分 `full registry` 與 `curated review surface`
- 將 `generate-index-entries.ps1` 提升為 full catalog 的正式生成來源，而不是保留為半正式工具
- 同步對齊：
  - `README.md`
  - `INDEX.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `export-review-package.ps1`
- 對誤植項目做明確決策：
  - 若 `microsoft-foundry` 確認為誤植，則不得納入 full catalog
  - 不得列為 review-wave 外候選來模糊處理
  - 必須明確標示為 stray / mistaken item，並自正式發布敘事中排除

### 3. 驗證

- `registry/skills` 目錄數量必須與 full catalog 條目一致
- `README.md`、`INDEX.md`、status report 對 skills 數量與 surface 定位說法一致
- `export-review-package.ps1 -DryRun` 的輸出必須能被文件正確解釋為 curated review surface
- `generate-index-entries.ps1` 的輸出必須可重建 full registry 條目
- 對誤植項目的處理結果必須在正式入口文件中被說清楚，避免工作樹內容與發布 surface 混淆

### 4. 指揮補充

Task A 的本質是「先定義真相」。

如果連 catalog 到底代表什麼都沒有說清楚，那後面的 release、verify、package、MCP、安全收口，全部都會建立在不穩定的敘事上。

### 今日放行判定

若 Task A 未完成，今日發布只能視為「敘事不一致的候選發布」，不應放行。

---

## Task B：Release Surface / Template / Rebuild 邊界清理

### 1. 目標問題

`UniText` 已在文件上區分：

- `authoring workspace`
- `template package`
- `rebuild project`

但目前發布邊界仍未完全收口。最明顯矛盾是：

- `TEMPLATE_RELEASE_PACKAGE.md` 的 include 區塊要求包含 `local/docs/PATH_MAP.md`
- 同一文件的 exclude 區塊又將 `local/docs/PATH_MAP.md` 列為不應包含

這種矛盾不是小錯字，而是發布邊界本身的自我衝突。

對一個主打 template export 的專案來說，這種矛盾一旦存在，就代表：

- 文件說可帶出去
- 文件又說不該帶出去
- 腳本卻已經真的把它打包出去

這會讓任何 verifier 都失去權威性。

除此之外，發布邊界還有一個常被低估但實際上非常危險的問題：

- 操作者或 AI 代理在 export / verify / metadata 寫入途中被打斷
- 導致檔案只寫入一半
- 或留下錯誤編碼、截斷內容、部分覆蓋的 package state

這類風險一旦發生，表面上可能仍然「有檔案存在」，但實際上 package 已不可信。對 `UniText` 這種依賴文檔、manifest、設定檔與 package metadata 的專案來說，這應被視為 release integrity 風險，而不是普通使用體驗問題。

### 2. 執行處理方式與技術

- 把 `export-template-package.ps1` 的 `$items` 視為唯一 template release 白名單
- 反向讓下列文件與此白名單完全對齊：
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
  - `PROJECT_MODES.md`
  - `README.md`
- 先決定 `local/docs/PATH_MAP.md` 的真實角色：
  - starter skeleton
  - 或 local-only artifact
- 強化 verifier，不只驗存在/不存在，還要驗：
  - `.mcp.json` 是否為 template-safe seed
  - `manifest.json` / `release.json` 是否與發布類型一致
  - forbidden artifacts 是否以 pattern 而不是硬編碼單例判斷
- 將 export / metadata 寫入流程提升為 interruption-safe：
  - 所有關鍵文字檔採用明確 UTF-8 寫入
  - 先寫入暫存檔，再以 rename / move 原子替換正式檔
  - package 生成完成前，不應讓半成品目錄看起來像正式輸出
  - 為 `manifest.json` / `release.json` 補上完整性欄位或至少生成狀態標記，避免中斷後誤判為有效產物
- 補 rebuild flow 的邊界一致性：
  - `export-rebuild-project.ps1` 應有同等級 path safety
  - rebuild metadata 不可沿用 template 路徑與 channel
  - rebuild verifier 指向要與文件一致
- 今日發布只鎖定單一主發布物：
  - 主發布物 = `template package`

### 3. 驗證

- `export-template-package.ps1 -DryRun` 的清單必須與文件 include/exclude 一致
- `export-template-package.ps1` 實際輸出後，`verify-template-package.ps1` 必須通過
- 在模擬中斷或不完整輸出時，verifier 必須能辨識：
  - 缺失的 `manifest.json`
  - 截斷或非法編碼的 metadata 檔
  - 只生成部分內容的 package 目錄
- package 內不得包含：
  - `backup/`
  - `recovered_*`
  - `.bak_*`
  - `ops/history/`
  - review-only docs
  - machine-specific absolute paths
- `export-rebuild-project.ps1` 與 `verify-rebuild-project.ps1` 要能自洽，但不作為今日主發布物

### 4. 指揮補充

Task B 的核心不是把 package 匯出成功，而是把「什麼能被帶出去」這件事變成單一答案。

沒有單一 release surface，就沒有可信的 template release。

### 今日放行判定

若 template 邊界、metadata、verifier 三者仍互相矛盾，今日不可發布。

---

## Task C：Cross-Platform `bootstrap / verify / test coverage` 補齊

### 1. 目標問題

目前真正跨平台成立的是 Python first-run path，但測試與文案尚未與此現實對齊。

現況：

- `bootstrap.py` 是跨平台控制面主入口
- `verify-bootstrap.py` 偏向作者基線對齊檢查
- `tests/security/test_hardening.py` 在無 `pwsh` 環境下會直接報錯

因此，今天的問題不是 `UniText` 沒有跨平台能力，而是它目前的對外說法過於完整，超過了實際可重複證明的範圍。

### 2. 執行處理方式與技術

- 將跨平台承諾明確限定為：
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`
- 把驗證拆成兩層：
  - `portable bootstrap correctness`
  - `Windows-first governance script validation`
- 調整 `verify-bootstrap.py` 的角色說明：
  - 保留 portable 必要條件檢查
  - 將 authoring-specific `.claude/settings.json` 權限檢查降為附加檢查或分層檢查
- 補 happy-path 測試，而不只保留 negative-path hardening：
  - `bootstrap.py --dry-run`
  - `bootstrap.py --force`
  - `verify-bootstrap.py`
  - symlink 失敗退回 mirror
- 在無 `pwsh` 的環境中：
  - PowerShell 測試必須 `skip`
  - 不可再以 `FileNotFoundError` 破壞整體測試結論
- 對外文案降到證據支撐的真實水位：
  - `cross-platform Python bootstrap baseline verified`
  - 不宣稱整體治理已跨平台完成

### 3. 驗證

- `python3 -m unittest` 不得因缺少 `pwsh` 直接報錯
- 至少新增一組 Python happy-path 測試證據
- `bootstrap.py --dry-run` 與 `verify-bootstrap.py` 在當前 Linux/WSL 環境可形成可重複證據
- README、checklist、status report 對 cross-platform 的說法一致

### 4. 指揮補充

Task C 的重點不是「把跨平台做得很大」，而是把它說準。

對今天發布而言，精確比全面更重要。

### 今日放行判定

若今日仍使用「整體已跨平台完成」的敘事，且測試仍在 Linux/WSL 環境硬錯，則不可放行為 `template release candidate`。

---

## Task D：安全與控制面 Hardening 收尾

### 1. 目標問題

Task D 的本質不是重做安全工程，而是清除會直接破壞發布可信度的阻斷風險。

今日最關鍵的發布阻斷項是：

- `webapp-testing/scripts/with_server.py` 的 `--allow-shell` 路徑仍可進 `shell=True`

這不是抽象的安全焦慮，而是非常具體的控制面問題：

- 這條路徑位於正式 skill surface 內
- 它不是單純內部工具
- 它足以讓今天的安全敘事失去說服力

其餘控制面風險多數已從高危缺陷降為收尾型問題：

- `path-safety.ps1` 已成形
- adopt/rollback 已接入共享 helper
- `quick_validate.py` 已足以當 canonical frontmatter validator
- MCP server 的 read-only boundary 已相對穩健
- 但中斷導致的半寫入與殘缺狀態仍未被系統化處理，尤其是設定檔、manifest、release metadata 與 export 產物目錄

### 2. 執行處理方式與技術

- 對 `with_server.py` 做明確發布級決策：
  - 移除 `--allow-shell`
  - 或隔離為 `legacy/internal mode`
  - 或拆成另一支 clearly-unsafe script
- 不可只在文檔中加警告後繼續當正式 surface 發布
- 將 `quick_validate.py` 明確指定為唯一 canonical frontmatter validator
- 降低 `scan-skills.ps1` regex 解析地位：
  - 僅作報表展示
  - 不得形成另一套治理真相
- 將 `path-safety.ps1` 正式升格為 destructive PowerShell 腳本的唯一邊界層
- 將「中斷安全」提升為控制面 hardening 的正式要求：
  - 對 `.mcp.json`、`manifest.json`、`release.json`、catalog 類文本使用暫存檔 + 原子替換策略
  - 對長流程 export 增加明確的完成標記，而不是只靠目錄存在判定成功
  - 被打斷時應留下可辨識的失敗狀態，而不是看似成功的殘缺輸出
- 把 MCP `server.py` 的 read-only boundary 明確納入發布級安全證據
- 將控制面能力分層標示：
  - `release-grade`
  - `Windows-first reference`
  - `legacy opt-in`
  - `authoring-only`

### 3. 驗證

- `with_server.py` 的 shell mode 必須被移除、隔離、或明確排除於正式發布面之外
- destructive PowerShell 腳本必須可追蹤地使用：
  - `Assert-SafeSimpleName`
  - `Resolve-SafeRepoPath`
  - `Test-ContainsReparsePoint`
- frontmatter 真相只能有一個 canonical 結論來源
- MCP server 必須保留：
  - repo escape 拒絕
  - 非 `registry/**` / 核心文件拒絕
  - 最小 read-only tool surface
- 關鍵 control-plane 檔案在遭遇中斷後，必須滿足以下其一：
  - 完全回滾到上一個有效版本
  - 留下明確可辨識的不完整狀態
  - 不得產生會被後續流程誤判為成功的半寫入內容

### 4. 指揮補充

Task D 不要求今天把所有安全議題一次結案，但要求把「會破壞今天發布可信度」的那幾個口，確實封住。

### 今日放行判定

若 `with_server.py --allow-shell` 仍作為正式 skill surface 存在，今日不應以安全可發布狀態放行。

---

## Task E：發布證據、工作樹清理、Go/No-Go Gating

### 1. 目標問題

今天最大的發布風險，不是沒有 export，而是缺少完整證據鏈支撐 `template release candidate` 敘事。

現況：

- `ops/` 下已有多批歷史產物
- 但當前工作樹仍有 243 筆變更
- `manifest.json` / `release.json` 仍有作者絕對路徑與 rebuild metadata 不自洽問題

所以今天不能把 authoring workspace 本體當發布物，必須以新鮮 exported package 為唯一發布對象。

此外，今天還必須把「被打斷的流程產物是否會混入發布證據」這件事納入 gating。若 export、verify、metadata 寫入途中被中斷，而系統又沒有辨識機制，那麼表面上存在的 package 可能根本不是可發布產物。

### 2. 執行處理方式與技術

- 鎖定唯一放行對象：
  - `template package`
- 將工作樹清理策略改為：
  - 不要求 repo 立刻全乾淨
  - 但要求發布物必須和工作樹有效隔離
- 升級 metadata，使其可作放行依據：
  - `release_target`
  - `source_commit`
  - `workspace_dirty`
  - `evidence_bundle`
  - release-relative `package_path`
  - rebuild 自洽 metadata
  - `generation_state` 或等價完成標記，用來區分成功輸出與中斷殘留
- 建立單一 release evidence bundle，至少包含：
  - `git status`
  - `export -DryRun`
  - 實際 export
  - `verify-template-package.ps1`
  - `bootstrap.py --dry-run`
  - `verify-bootstrap.py`
- 將 Go/No-Go 寫成硬門檻：
  - `P0`: metadata 錯誤、package 邊界錯誤、verify 失敗、author-specific path 洩漏
  - `P1`: cross-platform 證據不足、surface 敘事不一致
  - `P2`: 可發布後跟進的深化工作

### 3. 驗證

- 明確保存本次發布對應的 `git status` 證據
- 新鮮 export 的 package 必須存在且 verifier 通過
- `manifest.json` / `release.json` 不得含作者絕對路徑
- rebuild metadata 不得再沿用 template 路徑或 channel
- 必須能從 `ops/` 中指出與本次發布直接對應的一組新鮮證據
- 必須形成完整 evidence chain：
  - `dry-run -> export -> verify -> first-run proof`
- 必須證明中斷殘留不會被當成有效發布證據：
  - 半成品 package 不可混入正式 evidence bundle
  - 未完成 metadata 不可被 verifier 視為有效
  - 若流程被打斷，必須能明確判斷本次發布作廢

### 4. 指揮補充

Task E 的核心不是「把 git status 清零」，而是把今天這次發布變成一個可以回頭審計的決策。

### 今日放行判定

若今日無法提供完整 evidence chain，就不應發布為 `template release candidate`，最多只能降為 `template release cleanup baseline`。

---

## 6. 今日實施順序

### Phase 1：先處理發布阻斷語義

1. 完成 Task A 的 surface / catalog 定義
2. 完成 Task B 的 template 邊界與文檔矛盾收口
3. 決定今天唯一主發布物 = `template package`

### Phase 2：補齊可發布底線

1. 完成 Task D 的 release-blocking 安全收口
2. 完成 Task C 的最小跨平台證據補齊
3. 修正文檔中所有超前承諾

### Phase 3：形成放行證據

1. 執行 `export-template-package.ps1 -DryRun`
2. 執行實際 export
3. 執行 `verify-template-package.ps1`
4. 對 exported package 執行 first-run proof
5. 生成最終 release evidence bundle

### Phase 4：Go / No-Go 決策

只有在以下全部成立時才 `Go`：

- A/B/C/D/E 五任務都達到今日最低門檻
- package 邊界正確
- cross-platform 敘事與證據一致
- 控制面無發布阻斷風險
- evidence chain 完整

否則一律 `No-Go`，並降級為：

- `template release cleanup baseline`

## 7. 一票否決條件

以下任一成立，今日直接 `No-Go`：

- `INDEX` / README / status report / export surface 仍互相矛盾
- template package 邊界仍有 include/exclude 自相矛盾
- `with_server.py --allow-shell` 仍作為正式發布 surface 存在
- 測試在 Linux/WSL 下仍因缺少 `pwsh` 直接硬錯
- package 仍含 local-only / review-only / history 類內容
- `manifest.json` / `release.json` 仍含作者絕對路徑或 rebuild metadata 錯誤
- 任務中斷後仍可能留下會被誤判為成功輸出的半成品 package / metadata
- 無法提供 `dry-run -> export -> verify -> first-run proof` 完整證據鏈

## 8. 最終指令

今天的正確目標不是「把 repo 看起來整理得差不多」，而是把 `UniText` 從一個高活躍 authoring workspace，收斂成一個有單一主發布物、有清楚邊界、有真實驗證、有放行證據的 `template release candidate`。

若五個任務全部補齊，今日可以發布。

若其中任一 P0 任務未收口，今日不應強行發布。  
應降級為 `template release cleanup baseline`，待阻斷項解除後再切 release。

## 9. 附錄：Interrupted-Run / Release Integrity 子專案

### 9.1 為什麼這要升格成正式子專案

這個風險不只是腳本健壯性問題，而是發布完整性問題。

對 `UniText` 來說，很多關鍵真相都不是存在於單一程式執行結果，而是存在於：

- `manifest.json`
- `release.json`
- `.mcp.json`
- `config.toml`
- exported package 目錄
- `ops/` 下的 evidence 與 summary

一旦操作者或 AI 代理在流程中被打斷，就可能留下：

- 半寫入的正式檔案
- 截斷或殘缺編碼的 metadata
- 看似完整但其實少檔的 package
- 語義已變更但 metadata 尚未同步的 rebuild package
- 舊狀態與新狀態卡在中間的 bootstrap wiring

這種狀態最危險的地方不在於它會失敗，而在於它可能「看起來成功」。

因此，這個子專案的目的不是只是讓流程更穩，而是確保：

- 中斷後不會留下假成功狀態
- 中斷後可辨識
- 中斷後可清理或可重跑
- verifier 能拒絕不完整產物
- evidence chain 只接納完整完成的輸出

### 9.2 子專案結論摘要

本輪成對子代理的結論高度一致。要把這個風險收斂到發布可接受水位，至少需要五個核心機制一起成立：

1. `atomic file writes`
2. `transactional package export`
3. `generation_state / completion marker`
4. `integrity-aware verifier`
5. `interrupted-run tests`

少掉其中任何一項，都仍會留下假成功空間。

### 9.3 Workstream A：Atomic Write 與 Transactional Export

#### 1. 風險與目標問題

目前多個流程會直接寫正式目標：

- `export-template-package.ps1`
- `export-rebuild-project.ps1`
- `bootstrap.py`

這種模式在正常情況下可以工作，但一旦中斷，最終會留下：

- 正式目錄已存在，但內容未完成
- metadata 尚未寫完
- package 類型已切換，但 release metadata 仍是舊值
- `.mcp.json` 或 `config.toml` 被部分覆寫

#### 2. 執行處理方式與技術

- 所有關鍵文字檔改為 `temp -> flush/fsync -> atomic replace`
- 所有 package export 改為 `staging -> validate -> commit`
- 正式 package 名稱只能代表「完整成功輸出」，不能代表「流程開始了」
- rebuild 不得先 `Move-Item` 再補 metadata，而應在 staging 完成全部修改後一次 commit
- bootstrap 的關鍵寫入點都應改成 atomic write：
  - `.mcp.json`
  - `~/.codex/config.toml`
  - `summary.json`

#### 3. 驗證

- 中斷於 metadata 寫入前、中、後，正式檔案不得留下截斷內容
- 中斷於 export copy 過程中，正式 package 路徑不得被視為完成產物
- 中斷於 rebuild metadata 改寫前後，verifier 必須拒絕該 package

### 9.4 Workstream B：Verifier / Generation State / Evidence Chain

#### 1. 風險與目標問題

現有 verifier 大多只檢查：

- 檔案是否存在
- 不該存在的檔案是否不存在

這不足以辨識：

- 截斷 JSON
- 合法 JSON 但語義錯誤的 metadata
- rebuild package 仍沿用 template path / channel / phase
- staging 殘留或 interrupted-run 殘留
- 舊批次 package 被誤當成今日證據

#### 2. 執行處理方式與技術

- 為 package 與 metadata 補 `generation_state`
  - `in_progress`
  - `complete`
  - `failed`
- 增加或重構 metadata schema，至少納入：
  - `release_target`
  - `source_commit`
  - `workspace_dirty`
  - `generated_by`
  - `generation_state`
  - `evidence_bundle`
  - release-relative `package_path`
- verifier 從 `path checker` 升級為 `integrity checker`
  - JSON 可解析
  - schema 完整
  - 關鍵欄位彼此一致
  - `generation_state == complete`
  - 不接受 staging / partial / interrupted-run 產物
- `verify-bootstrap.py` 也要提升：
  - 不只驗值匹配
  - 還要驗完整性與新鮮度

#### 3. 驗證

- `verify-template-package.ps1` 必須能拒絕：
  - 缺欄位 metadata
  - 截斷 JSON
  - `generation_state != complete`
  - package path 帶作者機器絕對路徑
- `verify-rebuild-project.ps1` 必須能拒絕：
  - rebuild package 仍指向 template 路徑
  - `release_channel` / `phase_target` 不自洽
- evidence bundle 必須能明確指出：
  - 哪一批輸出屬於本次 release
  - 哪些只是舊歷史產物

### 9.5 Workstream C：Recovery / Rollback / Interrupted-Run Tests

#### 1. 風險與目標問題

即使做到 atomic write 與 staging export，若沒有：

- 明確的 cleanup policy
- 清楚的 rerun-safe 策略
- 可重現的 interrupted-run 測試

那麼實際上仍無法保證一線操作不會留下混亂狀態。

今天最務實的目標不是做到「中途續跑」，而是先做到：

- 失敗可辨識
- 殘留可清理
- rerun 安全
- verify 可拒絕假成功

#### 2. 執行處理方式與技術

- 將 run transaction 正式化，至少記錄：
  - `run_id`
  - `generation_state`
  - `started_at`
  - `completed_at`
  - `target_path`
  - `cleanup_required`
- cleanup policy 分兩層：
  - 自動清理當次 staging
  - 對可能污染正式狀態的失敗 run 保留 failed evidence
- rerun 預設策略：
  - 先做到 rerun-safe
  - 不把 resumability 當第一優先
- 為 interrupted-run 建立三類測試：
  - 檔案級中斷
  - 目錄級中斷
  - 交易級中斷

#### 3. 驗證

- `export-template-package.ps1` 中斷於任意 copy 階段後，正式 package 不得被視為成功
- `export-rebuild-project.ps1` 中斷於 `Move-Item` / metadata 改寫任一點後，rebuild package 不得被誤判成功
- `bootstrap.py` 中斷於設定檔寫入途中後，必須滿足其一：
  - 回滾到舊版
  - 留下明確失敗狀態
  - 不得產生會被 verifier 誤判為成功的半成品
- rerun 後不需要依賴人工猜測現場狀態

### 9.6 子專案的今日最低交付線

如果今天不打算一次把所有 interrupted-run 設計都實作完，最低也要做到以下四件事：

1. 將 package export 改成 `staging -> commit`
2. 將 `manifest.json` / `release.json` / `.mcp.json` / `config.toml` 改成 atomic write
3. 為 package 補上 `generation_state` 或等價 completion marker
4. 讓 verifier 能拒絕 interrupted-run 半成品

只要這四件事沒做到，今天就不應宣稱 release integrity 已成立。

### 9.7 子專案的一票否決條件

以下任一成立，代表 interrupted-run 風險仍是發布阻斷項：

- 正式 package 目錄可能在未完成時就存在
- metadata 沒有 generation state / completion marker
- verifier 仍只驗存在性，不驗完整性
- rebuild package 仍可能留下 template/rebuild 混合語義
- `.mcp.json` / `config.toml` 仍可能被部分覆寫而無法辨識
- interrupted-run 測試仍不存在

### 9.8 指揮結論

這個子專案不是額外加分項，而是 `UniText` 從「有 export 腳本」進化到「有可信發布控制面」的必要門檻。

如果今天要對外主打：

- `template release candidate`

那麼 `atomic write + staging export + generation_state + integrity-aware verifier + interrupted-run tests`

至少要做到最小可接受線。  
否則發布敘事仍會建立在「流程看起來成功」，而不是「輸出真的可信」之上。
