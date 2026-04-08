# UniText — 專案 MAP 網頁自動化開發報告

> 狀態：Draft Plan
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
4. 需要分享時，再額外 export 成 template-safe artifact

這裡刻意把 generated output 放進 `ops/`，因為它屬於 generated state，不是 canonical source。

這樣生成仍是一次性程序，但觀看完全不依賴程序。

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
- 規劃是否需要 export 專用的 share-safe map artifact

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

## 15. 建議下一步

下一步不要先做完整 UI，而是先完成一個 bounded prototype：

**做出 `build-project-map.py -> project-map.html` 的最小鏈路，內部仍保留 `project-map.json` 作為中介格式，先覆蓋 `README.md`、`INDEX.md`、`registry/skills`、`registry/mcp`。**

只要第一版能穩定生成、可看、且不需要手工同步，就已經達成這個需求的核心價值。
