# UniText — Integration Surface Profiles

> 狀態：Active Baseline  
> 用途：把新工具接入、runtime delivery、native config wiring、與 verify probe 先做成宣告式 profile，而不是散落在個別腳本內硬編碼。

## 1. Why This Exists

UniText 既有的 `registry / runtime / local / ops` 四層分工已足夠承接多工具共享資源。

真正容易漂移的是：

- 新 CLI 或 integration surface 要接進來時，target path 與 verify probe 常直接寫死在腳本裡
- `runtime/catalog.json` 知道有哪些 runtime entry，但不夠知道「哪些 surface 可消費它」
- 新產物常先落檔，之後才補治理分類

這份規則的目的，是先把「接入面」做成可被腳本與 reviewer 共用的宣告式契約。

## 2. Source Of Truth

目前的 baseline manifest 是：

- `local/config/integration-surfaces.json`

它描述的是：

- 這個 repo 已宣告哪些 integration surface
- 每個 surface 能處理哪些 resource type
- 它偏好的 delivery resolution
- 它的 verify probe 是什麼

它不是：

- 某台機器的 live state dump
- 直接可套用到所有 repo 的全域規格
- canonical shared resource type 本身

## 3. Profile Shape

每個 profile 至少應定義：

- `id`
- `kind`
- `cli_id`
- `resource_types`
- `path_scope`
- `path_template`
- `delivery_modes`
- `preferred_delivery_resolution`
- `verify_probe`
- `capabilities`

可選但建議補上：

- `instruction_surface`
- `discovery_surface`
- `runtime_projection_rules`
- `preserve_local_extras`

## 4. Current Scope

這一批先涵蓋現有已經在 bootstrap / verify 中存在的 surface：

- `runtime-read-model`
- `claude-skills`
- `gemini-skills`
- `agents-skills`
- `codex-skills`
- `codex-native-config`
- `copilot-global-mcp`
- `project-mcp-seed`

也就是說，這次不是新增新的 resource type，而是先把既有接入面宣告化。

## 5. Runtime Catalog Relationship

`runtime/catalog.json` 現在應視為：

- runtime-first consumer inventory
- 加上 integration-aware metadata 的 read model

它可以安全帶出：

- `canonical_location`
- `supported_clis`
- `delivery_guidance`
- `available_surfaces`

但如果 canonical source 沒有明確宣告某欄位，例如 `status`，runtime catalog 可以暫時保留 `null`，不要假裝已被 canonicalize。

## 6. New Artifact Intake Gate

未來新增工具、設計 sidecar、compat matrix、routing manifest、或其他衍生產物時，先走這個 gate：

1. 它是不是 shared canonical truth  
   如果是，才考慮 `registry/` 或 root shared docs。

2. 它是不是 machine-local wiring 或 local authoring state  
   如果是，放 `local/`，而不是 shared layer。

3. 它是不是 generated evidence / analysis / report  
   如果是，放 `ops/`。

若三題都還答不清楚，先不要落到 `registry/`。

## 7. Analysis vs Canonical Boundary

短期規則：

- analysis output
- sidecar draft schema
- compatibility matrix
- extension routing draft

預設先留在 `ops/` 或 runtime validation/read-model 層。

只有在下列條件成立時，才考慮升格：

- identity 穩定
- provenance 可追蹤
- verify path 清楚
- rollback 或 bounded removal path 存在
- review 後仍值得 canonicalize

## 8. What This Does Not Do Yet

這份 baseline 還沒有做到：

- manifest-driven bootstrap executor for every future resource type
- MCP runtime projection 與 adapter-aware routing 全覆蓋
- new first-class canonical resource type such as `primitives`

這是刻意保守的第一批：先把接入契約做出來，再決定是否擴大 resource model。
