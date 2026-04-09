# UniText Project Map — 5H YOLO Development Log

> 狀態：In Progress
> 模式：`project-development-loop` / `yolo-unattended`
> 範圍：靜態 `project-map.html`、browser-side refresh、generator、share-safe export 規劃與實作

## 1. 啟動判斷

### 1.1 目標

- 以連續 3 輪 `評估 > 開發 > 檢驗 > 外部審查 > 修正` 的節奏，持續推進 `UniText Project Map`
- 把過程留成可續跑、可審查、可交接的開發紀錄
- 優先做高訊號、可驗證、可在靜態頁模式下落地的改進

### 1.2 Skill / Tool 評估

- `project-development-loop`
  - 用途：作為這次 5 小時 YOLO 模式的主流程與分輪節奏
- `webapp-testing`
  - 用途：在本機瀏覽器驗證靜態頁行為、互動與版面
- `chrome_devtools`
  - 用途：做快照、互動驗證、Lighthouse 外部審查
- `build-project-map.py`
  - 用途：每輪改動後重新生成 canonical output

### 1.3 初始審核摘要

- 目前 `project-map.html` 已具備：
  - `欄式 / 圓形` 視圖
  - 搜尋與類型篩選
  - browser-side repo refresh
  - 手動 / 開頁 / 定時更新
- 目前最有價值的缺口：
- 視覺對比仍有可讀性弱點
- relation 導覽仍偏靜態，從 detail 回跳相關節點不夠快
- share-safe export 仍停留在報告規劃，沒有真正落地

## Round 4

### 評估

- 聚焦先前列出的下一步：
  - broken reference / orphan resource 顯示
  - export workflow 的 UI 入口
- 目標是把既有 MAP 從「可看」補到「可診斷、可分享導覽」

### 開發

- `build-project-map.py` 新增 diagnostics 產出：
  - `broken_reference_count`
  - `orphan_node_count`
  - `broken_references`
  - `broken_source_ids`
  - `orphan_node_ids`
- `project-map.html` 新增 diagnostics 卡片：
  - 顯示 broken / orphan 計數
  - 提供 `只看 broken sources`、`只看 orphan`、`清除診斷篩選`
- interactive 版新增 export 卡片：
  - 直接提供 `開啟分享版` 入口
- browser-side repo scan 也同步補上 diagnostics 計算，避免頁內更新後資料模型降級

### 檢驗

- 重新產出：
  - `python -m py_compile local/scripts/build-project-map.py`
  - `python local/scripts/build-project-map.py`
- 產出資料確認：
  - `broken_reference_count = 34`
  - `orphan_node_count = 1`
  - `broken_source_ids = [doc:INDEX.md, doc:README.md]`
  - `orphan_node_ids = [skill:microsoft-foundry]`
- 瀏覽器互動驗證：
  - 點 `只看 broken sources` 後，節點數從 `38 / 38` 變成 `2 / 38`
  - 點 `只看 orphan` 後，節點數變成 `1 / 38`
  - 點 `清除診斷篩選` 後，節點數回到 `38 / 38`
  - `開啟分享版` 可直接打開 `project-map-share.html`

### 外部審查

- 使用真實瀏覽器互動驗證 diagnostics filter 與 share-safe entry
- Lighthouse snapshot（share-safe）結果：
  - Accessibility: `100`
  - Best Practices: `100`
  - SEO: `60`
- 判斷：
  - diagnostics / export UI 沒有把可及性拉壞
  - `SEO 60` 仍主要受 `file://` 靜態快照情境影響，不是這輪功能的阻塞項

### 修正

- 本輪未再發現需要立即修補的互動錯誤
- broken/orphan 與 export entry 已正式從規劃項轉成已落地能力

## Round 5

### 評估

- 目標從 diagnostics summary 進一步推到：
  - broken reference 的 source-target drill-down
  - 更完整的 export / handoff 體驗
  - 補一個可重用的 agent governance resolver

### 開發

- project map diagnostics 升級：
  - `broken_sources` 進入 payload
  - diagnostics 卡片新增 source-level jump buttons
  - detail 區若選中 broken source，會顯示 unmapped target 明細
- export / handoff 升級：
  - generator 會額外產出
    - `project-map-handoff.md`
    - `project-map-handoff.json`
  - export 卡片新增：
    - `開啟 handoff.md`
    - `開啟 handoff.json`
    - `複製 handoff 摘要`
- 治理工具：
  - 新增 `local/config/agent-governance-layers.json`
  - 新增 `local/scripts/resolve-agent-governance.py`
  - 新增 `AGENT_GOVERNANCE_LAYERING.md`
  - tool 可根據 `model / environment / instruction-profile` 解析 matched layers、effective config 與 provenance

### 檢驗

- `python -m py_compile local/scripts/build-project-map.py local/scripts/resolve-agent-governance.py`
- `python local/scripts/build-project-map.py`
  - 產出包含：
    - `project-map.html`
    - `project-map-share.html`
    - `project-map-handoff.md`
    - `project-map-handoff.json`
- `python local/scripts/resolve-agent-governance.py --model gpt-5.4 --environment codex-local-dev --instruction-profile mapping --write-report`
  - 成功產出：
    - `ops/agent-governance/agent-governance-resolution.json`
    - `ops/agent-governance/agent-governance-resolution.md`

### 外部審查

- 真實瀏覽器驗證：
  - diagnostics 卡片可顯示 `UniText — Index` 與 `README` 兩個 broken sources
  - 點選 `README` source 後，detail 內可見 `BROKEN REFERENCES` 區塊與 unmapped target 清單
  - export 卡片可見：
    - `開啟分享版`
    - `開啟 handoff.md`
    - `開啟 handoff.json`
    - `複製 handoff 摘要`
- governance resolver 報告內容已確認包含：
  - matched layers
  - effective config
  - provenance

### 修正

- 外部審查時發現 `renderMap()` 內 `getFocusBox()` 誤用未定義的 `allEdges`
- 已改為直接使用 `DATA.edges`
- 修正後 console error 清空，detail 渲染恢復正常

## 2. 回合記錄

## Round 1

### 評估

- Lighthouse 初始結果：
  - Accessibility: `92`
  - Best Practices: `100`
  - SEO: `60`
- 失敗項：
  - `color-contrast`
  - `meta-description`
  - `robots-txt`

### 外部審查判斷

- `color-contrast` 值得修
- `meta-description` 值得補
- `robots-txt` 對 `file://` 靜態頁面不是高價值項目，暫不處理

### 開發

- 拉高頁面與細節面板中的低對比文字顏色
- 補上 `<meta name="description">`

### 檢驗

- 重新執行 `python local/scripts/build-project-map.py`
- 重跑 Lighthouse snapshot
- 結果：
  - Accessibility: `100`
  - Best Practices: `100`
  - SEO: `80`

### 外部審查

- 使用 Lighthouse 作為外部審查基準
- 結論：
  - `color-contrast` 已解除
  - `meta-description` 已解除
  - 剩餘 `robots-txt` 為 `file://` 靜態頁低價值項目，暫不投入

### 修正

- 將 Round 1 結論定為完成，後續不再把 `robots.txt` 視為優先缺口

## Round 2

### 評估

- 聚焦 relation 導覽與節點跳轉效率
- 目前 detail 區的關聯資訊是可讀但不可直接操作
- 若節點被搜尋或類型篩選隱藏，回到相關節點的操作成本偏高

### 開發

- 將 detail 區的 relation item 改為可點擊跳轉按鈕
- 新增 `jumpToNode()`，在目標節點被搜尋或類型篩選隱藏時，自動解除限制並重新聚焦

### 檢驗

- 瀏覽器場景測試：
  - 搜尋 `doc-coauthoring`
  - 從 detail 區點擊 `skills`
  - 預期：自動清空搜尋、恢復節點清單、切到 `skills`
- 實測結果：
  - `目前顯示 1 / 38` 會回到 `38 / 38`
  - detail 與中央視圖都切到 `skills`

### 外部審查

- 使用真實瀏覽器互動作為外部審查
- 結論：relation 導覽已從靜態資訊升級成可操作流程

### 修正

- 將 hidden peer reveal 設為預設行為，避免使用者卡在被篩選遮蔽的關聯節點

## Round 3

### 評估

- 預計聚焦 share-safe artifact 與 generator/export workflow

### 開發

- `build-project-map.py` 會自動多產出：
  - `ops/project-map/site/project-map.html`
  - `ops/project-map/site/project-map-share.html`
- share-safe 版本改成唯讀頁：
  - 隱藏頁內重掃區塊
  - 隱藏目錄授權入口
  - 說明文改成分享快照語境
- runtime 依 `PROJECT_MAP_PAGE_MODE` 自動切換 interactive / share-safe 行為

### 檢驗

- `python -m py_compile local/scripts/build-project-map.py`
- `python local/scripts/build-project-map.py`
- 產出確認：
  - `project-map.html`
  - `project-map-share.html`
- share-safe Lighthouse：
  - Accessibility: `100`
  - Best Practices: `100`
  - SEO: `80`

### 外部審查

- 以瀏覽器直接打開 `project-map-share.html`
- 審查結果：
  - 頁面僅保留 `搜尋 / 類型篩選 / Map View`
  - 不再顯示更新模式、目錄連結、立即更新
  - 移除 relation button 的 `aria-label` 後，可及性回到 `100`

### 修正

- share-safe 模式下強制停用 browser-side repo scan，避免分享版行為與互動版混淆
- 保留 `robots.txt` 未處理，因為它對 `file://` 靜態快照仍是低價值項目

## 3. 目前判斷

- 這輪開發不需要額外 server、bundler 或外部 library
- 高訊號外部審查以 Lighthouse + 真實瀏覽器互動為主
- 5 輪已完成的主軸：
  - `Round 1`：可讀性與 metadata
  - `Round 2`：relation 導覽效率
  - `Round 3`：share-safe artifact 落地
  - `Round 4`：diagnostics 與 export UI 入口
  - `Round 5`：broken drill-down、handoff artifact、governance resolver
- 若後續繼續開發，下一個優先方向會是：
  - governance resolver 與實際 runtime / MCP config apply 流程的銜接
  - project map 對更多 canonical docs / workflow 節點的擴充

## 4. 階段結論

- 5 輪開發已完成，且每輪都有獨立驗證與外部審查訊號
- 目前最有價值的新成果：
  - interactive 版的可讀性與可及性明顯提升
  - relation 導覽已可直接跳轉並自動 reveal hidden peer
  - generator 已具備 share-safe artifact 產出能力
  - diagnostics 已可直接顯示 broken/orphan 狀態並用篩選方式切入
  - interactive 版已提供 share-safe artifact 的直接入口
  - broken reference 已可 drill-down 到 source-target 明細
  - export 已從單一分享頁升級成 share page + handoff bundle
  - agent governance 已有 simulation-first resolver 與 provenance 報告
- 目前不建議再做的大項：
  - 重型 graph library
  - AST 級 dependency parser
  - server-side map backend
