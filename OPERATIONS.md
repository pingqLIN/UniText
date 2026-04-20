# UniText — Operations

> 狀態：Template Base
> 角色：定義 adapter / operations control plane 的責任、delivery 規則與安全邊界。

所有 delivery 與 mutation 都應以 `UniText` 的純文本 registry / spec 契約為 source of truth。

Consumer agent 的預設讀取面是 `runtime/`，不是 `registry/`。`registry/` 仍然是 canonical authoring source；`runtime/` 是 tracked runtime read model；`local/` 才是 machine-local wiring。

若操作涉及 password、API key、token、credential 等 sensitive material，請同時遵守 `SECRET_HANDLING_GUIDELINES.md`。

## 1. Scope

本文件涵蓋：

- adapter responsibilities
- delivery modes
- delivery triggers
- adoption flow
- drift / repair
- logical-to-physical mapping

本文件不涵蓋：

- shared resource metadata schema
- 單一平台的唯一實作方式
- 本機 authoring repo 的歷史狀態

若需要判斷治理文件、reference、authoring notes、與 operations artifacts 應該放在哪一層，請搭配 `DOCUMENT_PLACEMENT_POLICY.md`。

## 2. Delivery Modes

| Mode | When to use |
|---|---|
| `pointer` | discovery 或非機器註冊型資源 |
| `mirror` | CLI 需要本地副本、或 symlink 不穩定 |
| `symlink` | CLI 需要固定路徑，且環境支援穩定連結 |
| `native-config` | CLI 有正式設定入口可註冊資源 |

`delivery mode` 由 adapter 在操作時解析，不是資源的固定硬屬性。

## 3. Delivery Resolution Rules

adapter 應依優先序考慮：

1. 有正式設定入口時，優先 `native-config`
2. 需要固定路徑且平台支援穩定連結時，用 `symlink`
3. 無法安全使用 symlink 時，用 `mirror`
4. 主要用途是 discovery 或入口時，用 `pointer`

## 4. Delivery Triggers

delivery 只能由明確 trigger 啟動：

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Safety Rules

### Dry-Run First

以下操作應先產出 dry-run plan：

- `adopt`
- `repair`
- 會覆寫既有狀態的 `sync`

### Backup Before Mutation

所有破壞性操作都應具備：

- backup 或等價回復點
- 可追溯的操作記錄
- 失敗時的停止條件

### No Silent Canonicalization

若遇到同名異內容資源：

- 必須停在 review
- 必須讓 operator 明確決定 canonical source

## 6. Adoption Flow

1. `SCAN`
   - 掃描候選來源，列出可 adopt 的資源與 readiness 狀態
2. `REVIEW`
   - 依 review checklist 檢查 metadata、內容品質與 canonical source 合法性
3. `DRY-RUN`
   - 預覽 adopt 或 delivery 將修改哪些目標、是否需要 backup
4. `ADOPT`
   - 將來源內容寫入 registry canonical location，若覆寫既有內容需先 backup
5. `DELIVER`
   - 由 adapter 將 registry 內容送到對應 CLI，若會覆寫既有狀態需保留 log 與 backup
   - 若 CLI 支援 `native-config`，可在 `bootstrap` 階段寫入 machine-local config，但 canonical definition 仍留在 `registry/`
6. `VERIFY`
   - 驗證檔案存在性、路徑解析、delivery mode 與目標 CLI 載入條件是否成立

## 6.1 First-Run Baseline

若目標是讓新的 template 使用者在 macOS / Linux / Windows 都能完成最小初始化，應至少提供：

- 一條跨平台 `bootstrap`
- 一條跨平台 `verify`
- 一條可攜的 repo backup 流程
- 一個可實跑的最小 MCP baseline

## 7. Operations State

以下內容屬於 operations state，而非 shared resources：

- inventories
- baselines
- backups
- drift reports
- repair plans
- audit trails

它們應位於 `/operations`，不應混入 `/registry`。

在目前 repo 的實體目錄上，`/operations` 對應的是 `ops/`。`ops/` 屬於 state layer，不是 canonical definition layer。

## 8. Logical-to-Physical Mapping

邏輯路徑是穩定契約；實體路徑是 deployment-specific mapping。

| Logical area | Meaning | Physical mapping examples |
|---|---|---|
| `/registry/skills` | canonical skill sources | shared directory、repo subdir、mounted path |
| `/runtime` | tracked runtime read model | repo `runtime/` directory、generated projections、runtime catalog |
| `/registry/mcp` | canonical MCP definitions | config folder、generated manifest root |
| `/registry/agents` | canonical agent instruction roots | agent profiles directory、shared prompt library |
| `/registry/workflow` | workflow docs / runbooks | workflow folder、project-local docs |
| `/operations` | inventories、backups、drift logs | ops folder、state store、audit directory |
