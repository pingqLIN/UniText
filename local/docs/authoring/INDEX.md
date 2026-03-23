# UniText — Index

> 狀態：Active
> 角色：所有 human / AI 的第一讀取點，用於 discovery，不承擔完整治理細節。

## 1. What Exists Here

`UniText` 是一個 text-native、registry-first、AI-first 的 shared resource hub。

這裡的核心不是某台機器的目錄長相，而是：

- 有哪些 shared resources
- 它們的 canonical identity 是什麼
- 哪些文件定義規則
- 應該去哪裡看 adoption、delivery、repair

## 2. Core Docs

請依下列順序閱讀：

1. `INDEX.md`
   - 快速知道這裡有什麼
2. `VISION.md`
   - 理解架構定位、邊界與 adoption model
3. `RESOURCE_SPEC.md`
   - 理解 shared resource 的最小契約
4. `OPERATIONS.md`
   - 理解 delivery、triggers、backup、repair、mapping
5. `PROJECT_MODES.md`
   - 區分本機 authoring repo 與對外 starter/template

補充文件：

- `local/docs/PATH_MAP.md`
  - local deployment reference，不是規格真相
- `local/docs/MCP_DEPLOYMENT_NOTES.md`
  - local MCP deployment note
- `local/docs/WORKFLOW_DEPLOYMENT_NOTES.md`
  - local workflow deployment note

## 3. Resource Catalog

目前 registry 關心以下 shared resource types：

| Type | Logical root | Purpose | Current registry state |
|---|---|---|---|
| `skills` | `/registry/skills` | 可被多個 CLI 共用的 skill 定義 | 尚無正式 catalog entry；有 pending adoption inventory |
| `mcp` | `/registry/mcp` | canonical MCP definitions | 已有首批正式 catalog entry |
| `agents` | `/registry/agents` | 共用 agent 指令與 persona 定義 | 尚無正式 catalog entry |
| `workflow` | `/registry/workflow` | 共用流程、runbook、planning guidance | 已有首批正式 catalog entry |

以下內容不是 shared resource type：

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories、backups、drift logs、history records |

### 3.1 Formal Catalog Entries

以下條目是目前 repo 內已可正式登錄的 shared resources。它們描述的是目前 registry 已確認的 entry，不代表所有候選資源都已完成納管。

#### Entry: `claude-project-mcp-seed`

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition` |
| `supported_clis` | `claude-code` |
| `delivery_guidance` | Use the MCP adapter; CLIs with native MCP registration typically resolve to `native-config`, but the final mode depends on platform and local environment. |
| `provenance` | Derived from the current canonical MCP seed file in this repository. |
| `notes` | Current seed exists as a formal anchor for MCP adoption, but the underlying server list is presently empty. |

#### Entry: `claude-plans`

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude-code` |
| `delivery_guidance` | Use the workflow adapter or the target CLI's planning-directory setting when available; the final mapping is deployment-specific. |
| `provenance` | Derived from the existing workflow directory and current workflow reference notes. |
| `notes` | This is a CLI-specific workflow resource already present in the repo; cross-CLI workflow formalization remains pending. |

### 3.2 Pending Adoption Inventory

以下內容已被辨識為 adoption 候選，但尚未成為正式 catalog entries：

| Area | Current observation | Registry meaning |
|---|---|---|
| `skills` | 在 `skills.bak.20260228_215107/` 下發現 27 個 `SKILL.md` 候選 | 目前屬於 inventory / backup 狀態，不視為 canonical `/registry/skills` |
| `agents` | 尚未發現正式 agent root 或 catalog manifest | 待後續建立 canonical `/registry/agents` 後再納管 |
| `workflow deployment notes` | 有 `local/docs/WORKFLOW_DEPLOYMENT_NOTES.md` 作為本機說明文件 | 屬於 local overlay supporting docs，不單獨視為 shared resource entry |

候選 skill inventory 中可辨識的項目包括：

- `frontend-design`
- `mcp-builder`
- `skill-creator`
- `webapp-testing`
- `pptx`

完整清單應在後續 adoption / catalog backfill 中逐步正式化，而不是直接把 backup 當成 canonical source。

## 4. Discovery Rules

`INDEX.md` 回答的是：

- 這裡有什麼資源
- 各資源的邏輯位置在哪裡
- 應該去看哪份規格或操作文件

`INDEX.md` 不直接回答：

- 某個平台的絕對路徑
- 某個 CLI 最後會用哪一種已解析完成的 delivery mode
- 某台機器目前的本機配置是否為標準答案

若需要知道：

- 資源欄位與 metadata
  - 看 `RESOURCE_SPEC.md`
- delivery mode 的實際決策、觸發與安全規則
  - 看 `OPERATIONS.md`

## 5. How To Consume

### For Humans

1. 先讀 `VISION.md` 確認這個系統的定位
2. 用 `INDEX.md` 找到資源類型與邏輯位置
3. 用 `RESOURCE_SPEC.md` 理解 entry 應長什麼樣子
4. 用 `OPERATIONS.md` 執行 install、sync、adopt、repair

### For AI Agents

1. 先把 `INDEX.md` 當成 discovery 入口
2. 看到 resource 時，先讀其 type 與 `canonical_location`
3. 需要 schema 時讀 `RESOURCE_SPEC.md`
4. 需要 delivery / mutation 時讀 `OPERATIONS.md`
5. 不要把 platform-specific path 或本機資料夾當成規格真相

## 6. How To Add A Resource

新增 shared resource 時，至少要完成以下步驟：

1. 選擇 `type`
2. 指定穩定的 `id`
3. 指定 `canonical_location`
4. 指定 `status`
5. 若已知支援哪些 CLI，補上 `supported_clis`
6. 若需要採用提示，補上 `delivery_guidance`

必填、推薦、選填欄位的完整規則，見 `RESOURCE_SPEC.md`。

## 7. Delivery Guidance Policy

`delivery_guidance` 是給 discovery 使用的提示，不是固定 delivery mode。

例如：

- 可以告訴你「去看哪類 adapter」
- 可以告訴你「此資源常見於哪些 CLI」
- 可以提醒你「存在平台差異」

但它不應被視為：

- 永久固定的 `mirror` / `symlink` / `native-config`
- 對所有平台都一樣的絕對規則

真正的 delivery mode 由 adapter 與 `OPERATIONS.md` 的規則解析。

## 8. Current Repository State

目前這個 repo 已具備：

- 正式願景文件 `VISION.md`
- shared resource 契約 `RESOURCE_SPEC.md`
- 已登錄的正式 catalog entries
  - `claude-project-mcp-seed`
  - `claude-plans`
- 既有的 operations state artifacts 與部分 delivery 實作

目前這個 repo 應被視為：

- `Local Development Project`
  - 也就是作者正在演化中的 authoring / governance workspace

若要提供給其他人當樣板，應另外依 `PROJECT_MODES.md` 做 template-safe 篩選，而不是直接把本 repo 全量視為 starter project。

目前仍待補齊：

- `skills` 的正式 catalog backfill
- `agents` 的 canonical root 與首批 catalog entries
- 更完整的 `mcp` shared definitions
- `OPERATIONS.md` appendix 中更完整的 deployment mapping

## 9. Stability Notes

以下內容是穩定契約：

- logical canonical paths
- resource identity (`type` + `id`)
- lifecycle 語義
- conflict / adoption 的高層規則

以下內容可能因平台或部署方式而不同：

- 絕對路徑
- 實際腳本名稱
- CLI 設定檔位置
- delivery mode 的最終解析結果
