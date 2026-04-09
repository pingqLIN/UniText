# UniText — 專案 MAP 網頁自動化開發報告

> 狀態：Prototype Implemented
> 用途：定義如何以高效率、自動化、低維護成本的方式，將預設目錄中的檔案解析為可瀏覽的專案 MAP 網頁。

## 1. 背景

目前 `UniText` 已有清楚的文字式結構與治理文件，但缺少一個可直接瀏覽的視覺化 MAP 網頁。

現況並不是沒有資訊，而是資訊分散在：

- `README.md` 的 repo 結構樹與架構摘要
- `INDEX.md` 的 discovery 與 catalog
- `OPERATIONS.md` 的 logical-to-physical mapping
- `registry/` 下各種 skill / mcp / agent / workflow 定義

因此真正的問題不是「沒有資料」，而是「沒有把既有 canonical 資料自動轉成一個可看的網頁」。

## 2. 需求判斷

目標方案必須同時滿足：

- 高效率：不依賴大量人工維護
- 自動化：能從預設目錄直接掃描與生成
- 低維護成本：新增或修改資源時，不需要同步維護另一份手寫地圖
- 無伺服器：瀏覽 MAP 時不需要 backend、API server、database
- 無長駐程序依賴：不需要 dev server、watcher、indexer daemon 常駐
- template-safe：不把 machine-local path、帳號、secret、live workspace state 混進 shared map
- 可擴充：未來能從文字版地圖擴充到互動式 dependency / topology 檢視

這裡需要先明確區分兩件事：

- **生成時的一次性程序**：允許，例如執行一次 `python local/scripts/build-project-map.py`
- **觀看時的持續性程序**：不允許，例如必須先啟一個本機 web server 才能看

也就是說，最佳目標不是「完全零程序」，而是：

**生成時可接受一次性 CLI；觀看時必須是純靜態、可直接開啟。**

## 3. 非目標

這份方案不追求：

- 一開始就做成完整 IDE 等級的 code graph
- 解析所有語言的 AST 與 symbol dependency
- 即時 server-side 查詢平台狀態
- 顯示 machine-local wiring、token、帳號、絕對路徑

第一階段應先把「可穩定生成、可讀、可維護」放在「超高 fidelity」之前。

## 4. 方案比較

### A. 手寫 Mermaid / 手工維護地圖

優點：

- 最快看到成果
- 易於控制視覺呈現

缺點：

- 每次結構變更都要人工同步
- 很容易與 `registry/` 真實狀態漂移
- 長期維護成本最高

判定：

不適合作為正式基線，只適合一次性示意圖。

### B. 全量 AST / dependency graph 自動分析

優點：

- 可產生非常細的技術關係圖
- 對大型程式專案很有吸引力

缺點：

- 對 `UniText` 這類文件 + registry 專案來說過重
- 維護成本高，且對多格式文件的解析器要求高
- 很容易把工具鏈本身做得比地圖還複雜

判定：

目前過度設計，不建議作為第一期。

### C. Canonical-doc-first 的結構化掃描 + 靜態網頁生成

優點：

- 直接吃現有 `README / INDEX / registry/` 結構
- 不需要重型後端
- 可用靜態 JSON + HTML 生成，跨平台容易
- 可做成單檔 HTML，直接用瀏覽器開啟
- 對 `UniText` 的 registry-first 設計最一致

缺點：

- 關係圖精度不如 AST 分析
- 初期需要定義一層 normalized graph schema

判定：

這是最佳選擇。

## 5. 建議方案

建議採用：

**Python-first 一次性掃描器 + normalized map JSON + 自包含靜態 MAP 網頁生成器**

也就是分成三層：

1. `scanner`
   - 掃描預設目錄與核心文件
2. `normalizer`
   - 把不同來源轉成統一的 graph JSON
3. `renderer`
   - 把 graph JSON 轉成靜態網頁

這樣的好處是：

- 掃描邏輯與前端呈現解耦
- 未來可更換前端技術，不必重寫解析器
- 可先輸出 JSON 給人看，再逐步加視覺化
- 可以同時保留 `project-map.json` 與單檔 `project-map.html`

## 5.1 無伺服器 / 無程序依賴設計原則

若把「觀看時不依賴任何額外程序」視為硬需求，則 renderer 應遵守：

- 輸出必須是純靜態檔案
- 預設支援 `file://` 直接開啟
- 不依賴 CDN
- 不依賴 client-side fetch 讀外部 JSON
- 不要求 Node、npm、Parcel、Vite、Python HTTP server

因此最穩定的交付形態應是：

**單一自包含 HTML 檔，內嵌資料與腳本。**

例如：

- `ops/project-map/site/project-map.html`

這個檔案應包含：

- inline CSS
- inline JavaScript
- inline serialized `project-map` JSON

這樣使用者只要雙擊檔案，或拖進瀏覽器，就能直接看。

## 6. 建議資料來源

第一期只吃以下 canonical sources：

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `registry/skills/*/SKILL.md`
- `registry/mcp/*/definition.json`
- `registry/agents/*/AGENT.md`
- `registry/workflow/*/*.md`

不應預設掃描：

- `local/docs/`
- `ops/`
- `.clean/`
- `__pycache__/`
- 未追蹤暫存輸出

原因是這些屬於 local state 或 operations state，不是 shared canonical truth。

## 7. Normalized MAP Schema

建議先輸出一份 `project-map.json`，最小結構如下：

```json
{
  "meta": {
    "generated_at": "2026-04-08T00:00:00Z",
    "source_root": "/",
    "version": 1
  },
  "nodes": [
    {
      "id": "skills:doc-coauthoring",
      "type": "skill",
      "label": "doc-coauthoring",
      "path": "/registry/skills/doc-coauthoring",
      "status": "active"
    }
  ],
  "edges": [
    {
      "from": "index",
      "to": "skills:doc-coauthoring",
      "kind": "catalog_entry"
    }
  ]
}
```

第一期 node types 建議只有：

- `doc`
- `skill`
- `mcp`
- `agent`
- `workflow`
- `directory`

第一期 edge kinds 建議只有：

- `contains`
- `references`
- `catalog_entry`
- `maps_to`

這樣夠用，而且低維護。

## 8. 解析策略

### Layer 1: 結構掃描

直接從目錄結構建立骨架：

- root docs
- `registry/skills`
- `registry/mcp`
- `registry/agents`
- `registry/workflow`

這一層不做語意推論，只建立基本節點與包含關係。

### Layer 2: Metadata 提取

針對不同檔案做輕量解析：

- `SKILL.md`：讀 frontmatter 的 `name`、`description`
- `definition.json`：讀 MCP id、entrypoint、support metadata
- `AGENT.md` / `WORKFLOW.md`：抓標題與簡述
- `INDEX.md`：把 catalog entries 轉成邏輯資源連結

這一層是核心價值所在，因為它會把「檔案」提升為「資源」。

### Layer 3: 關係提取

只做低成本、高訊號的關係：

- `INDEX.md` 指向哪些 canonical locations
- `README.md` 提到哪些核心文件
- `OPERATIONS.md` 定義哪些 mapping areas
- skill 內文中的相對連結指向哪些 references

不要一開始就做全文語意 dependency inference。

## 9. 網頁呈現建議

前端不需要一開始就引入大型框架，而且要優先避免任何需要 build server 或 dev server 的方案。

建議分兩期：

### Phase 1: 靜態單頁 HTML

- 左側：資源樹
- 中央：關係圖或卡片式節點視圖
- 右側：節點 metadata 與原始路徑
- 上方：type / status 篩選器

建議直接用：

- `vanilla HTML + CSS + JS`
- 原生 DOM + SVG 繪圖

不建議第一期依賴外部圖形庫，原因是：

- 會引入額外 bundle / vendor 維護問題
- 若走 CDN，會破壞離線與 template-safe 預期
- 若走 npm / bundler，會增加程序依賴

第一期比較適合：

- 樹狀導覽用原生 DOM
- 關係視圖用簡單 SVG 線段與節點
- 詳細 metadata 用卡片視圖

若第二期真的需要更強互動，再考慮把 vendor library 以 checked-in 靜態資產方式引入，而不是改成 server-dependent 架構。

### Phase 2: 進階互動

- 搜尋節點
- 只看某一類資源
- 高亮 references chain
- 顯示 broken references / orphan nodes

## 9.1 目前原型落地狀態

截至目前，原型已不只停留在靜態結構圖，而是具備下列可直接使用的能力：

- interactive 版：
  - 搜尋
  - 類型篩選
  - `欄式 / 圓形` 視圖切換
  - 手動 / 開頁 / 定時更新
  - browser-side repo scan
  - diagnostics 卡片與 broken/orphan 篩選
  - broken source drill-down
  - share-safe artifact + handoff bundle 的 export 入口
- share-safe 版：
  - 保留瀏覽、搜尋、類型篩選與 diagnostics
  - 移除頁內重掃與 repo 授權入口
  - 適合作為唯讀交付頁面

目前 generator 也已經同步產出 diagnostics data：

- `broken_reference_count`
- `orphan_node_count`
- `broken_references`
- `broken_source_ids`
- `orphan_node_ids`

這讓 MAP 已經從單純導覽頁，進一步變成「結構導覽 + 輕量診斷」的靜態 artifact。

同時，generator 也已開始產出 handoff artifact：

- `project-map-handoff.md`
- `project-map-handoff.json`

這表示 export 已不再只是「開一個分享頁」，而是能直接交接給下一位使用者或 agent 的 bundle。

## 10. 自動化流程

建議標準流程如下：

1. 執行 `build-project-map.py`
2. 內部完成：
   - `scanner`
   - `normalizer`
   - `renderer`
3. 一次產出：
   - `ops/project-map/project-map.json`
   - `ops/project-map/site/project-map.html`
   - `ops/project-map/site/project-map-share.html`
4. 需要分享時，優先使用 `project-map-share.html` 作為 share-safe artifact

這裡刻意把 generated output 放進 `ops/`，因為它屬於 generated state，不是 canonical source。

這樣生成仍是一次性程序，但觀看完全不依賴程序。

## 10.1 頁內更新機制

目前原型已進一步支援「靜態頁面 + 瀏覽器頁內重新掃描」雙軌模式。

也就是說，除了原本的：

- `python local/scripts/build-project-map.py`

之外，若瀏覽器支援 `File System Access API`，且使用者授權 repo root，`project-map.html` 本身也可以直接重新讀取 canonical source，更新目前頁面內容，而不需要啟動 backend 或長駐 daemon。

現階段支援三種更新模式：

### A. 開啟網頁時自動更新

- 行為：
  - 每次開啟頁面時，若已保存目錄授權，頁面會自動重新掃描 repo
- 優點：
  - 使用者幾乎不需要額外操作
  - 能降低看到 stale map 的機率
- 缺點：
  - 會增加 initial page load 時間
  - 若使用者只是想快速看前次快照，這個成本可能是多餘的
- 執行開銷：
  - 每次開頁執行一次完整掃描與重新繪圖
  - 開銷大致等同一次手動更新

### B. 手動更新

- 行為：
  - 頁面提供「立即更新」按鈕，只有在使用者點擊時才重新掃描
- 優點：
  - 最容易理解
  - 沒有背景輪詢
  - 平時執行開銷最低
- 缺點：
  - 使用者需要自己決定何時 refresh
  - 若忘記更新，可能看到舊資料
- 執行開銷：
  - 只有點擊時才發生
  - 是三種模式中平均成本最低、最穩定的預設方案

### C. 定時更新

- 行為：
  - 使用者可輸入天 / 時 / 分，預設 `1 天`
  - 頁面在開啟期間按照設定頻率自動重掃
- 優點：
  - 適合長時間開著 MAP 做導覽或監看
  - 不需要反覆手按更新
- 缺點：
  - 頁面持續開啟時會反覆產生 file I/O 與重新繪圖
  - 頁面關閉後不會在背景執行，所以它不是 daemon-based scheduler
- 執行開銷：
  - 成本與掃描頻率成正比
  - 若設成很短的分鐘級頻率，會明顯高於手動更新與開頁更新

## 10.2 更新策略總結

若以「低維護 + 低執行成本」為優先，建議預設：

- `手動更新`

若以「降低 stale 資料機率」為優先，建議：

- `開啟網頁時自動更新`

若 MAP 會長時間固定開著當作工作台，才建議：

- `定時更新`

因此從綜合平衡來看：

- **預設最佳模式是 `手動更新`**
- **最實用的次佳模式是 `開啟網頁時自動更新`**
- **`定時更新` 應保留給明確需要長時間監看的情境**

## 11. 維護成本控制原則

要讓這套方案真的低維護，關鍵不是「功能少」，而是「不要讓人手同步兩份 truth」。

因此應遵守：

- 以 `registry/` 與 core docs 為唯一 source of truth
- 只寫少量 parser adapter，不寫大量客製規則
- 先支援高訊號格式，不追求全格式完美解析
- 前端只消費 normalized JSON，不直接讀 repo 檔案
- 任何額外人工標註都應是 optional overlay，而不是必填欄位

## 12. 推薦實作切分

### Batch 1

- 新增 `local/scripts/build-project-map.py`
- 定義 `ops/project-map/` 輸出形狀
- 先支援 `README.md`、`INDEX.md`、`registry/skills`、`registry/mcp`
- 產出單檔 `project-map.html`，可直接用瀏覽器開啟

### Batch 2

- 補 `agents`、`workflow`
- 加入 references edge
- 增加 broken reference / orphan resource 檢查

### Batch 3

- 補互動篩選與搜尋
- 補 export 專用的 share-safe map artifact

### Batch 3.5

- 加入頁內更新模式切換
- 補 `天 / 時 / 分` 定時頻率設定
- 補 browser-side repo scan
- 補 `Map View` 的 `欄式 / 圓形` 切換

### Batch 4

- 補 diagnostics summary
- 補 broken source / orphan resource 篩選
- 補 interactive 版 share-safe export 入口

### Batch 5

- 補 broken source → target drill-down
- 補 handoff markdown / JSON artifact
- 補 copyable handoff summary
- 補 agent governance resolver（model / environment / instruction-profile）

## 12.1 Map View 視圖策略

目前原型保留兩種 MAP 呈現：

### 欄式

- 以資源類型分欄排列
- 最適合看全域結構與數量分布
- 可讀性最高，也是最穩定的 baseline

### 圓形

- 以所選節點為圓心，向外一圈一圈展開
- 第一圈優先顯示直接關聯節點
- 適合看單點周邊 topology

## 13. 風險

- 若一開始把 parser 做太重，會讓這個功能本身變成高維護系統
- 若讓前端直接解析 repo，跨平台與可攜性會變差
- 若 renderer 依賴 `fetch("./project-map.json")`，在 `file://` 模式下可能被瀏覽器限制
- 若依賴 CDN 或 bundler，會偏離無伺服器 / 無程序依賴目標
- 若把 local / ops 狀態也混進圖，MAP 很快會失真
- 若沒有 normalized schema，後續 renderer 很容易反覆推翻重寫

## 14. 結論

最合理的方向不是手工畫圖，也不是直接做重型 code intelligence。

**最佳方案是：以 canonical docs 與 `registry/` 為 source of truth，透過一次性 Python 掃描器產出 normalized map JSON，再渲染成自包含的單檔靜態 MAP 網頁。**

這條路最符合：

- `UniText` 的 registry-first 架構
- 跨平台腳本收斂方向
- generated state 與 canonical source 分層原則
- 無伺服器、無長駐程序依賴的交付目標
- 高效率、自動化、低維護成本的要求

而在原型已經落地後，下一層治理能力也可以沿用同一個方法：

- 用一份 template-safe 的 policy JSON 表示層級
- 用一次性 resolver 腳本解析 effective config
- 用 Markdown / JSON 報告做交接與審查

這也是 `agent governance` 最低維護成本的實作方式。

## 14.1 Agent Governance Resolver

這次也補了一個配套治理工具：

- 政策檔：`local/config/agent-governance-layers.json`
- 解析器：`local/scripts/resolve-agent-governance.py`
- 說明文件：`AGENT_GOVERNANCE_LAYERING.md`

它的目的不是直接改動 runtime，而是先提供：

- matched layers
- effective config
- provenance

也就是讓 agent 可以依 `model / environment / instruction-profile` 得到不同配置層級，同時還看得出每個生效 key 是從哪一層來的。

## 15. 建議下一步

下一步不要先做完整 UI，而是先完成一個 bounded prototype：

**做出 `build-project-map.py -> project-map.html` 的最小鏈路，內部仍保留 `project-map.json` 作為中介格式，先覆蓋 `README.md`、`INDEX.md`、`registry/skills`、`registry/mcp`。**

只要第一版能穩定生成、可看、且不需要手工同步，就已經達成這個需求的核心價值。
