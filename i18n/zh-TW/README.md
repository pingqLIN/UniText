[English](../../README.md) | [繁體中文](README.md)

# UniText

> **一個以純文本為核心、以 registry 為先的多 AI CLI 共享資源中樞。**
>
> 將 Claude Code、Codex、Gemini CLI、Copilot CLI 等工具的資源定義統一到同一套文字契約中。

目前英文 root 文件是 canonical source，`zh-TW` 是唯一主動維護的翻譯 surface。過往的 `zh-CN`、`ja`、`de`、`fr`、`es`、`ko`、`it` waves 已歸檔到 `i18n/.clean/archived-locales/`，不再作為 release 或 drift gate 的 active target。

---

## UniText 到底在做什麼

UniText 不只是收納 prompts、skills 或 MCP 範本的資料夾，而是一種受治理的協作方式：把 shared AI resources 維持在同一份 canonical definition，同時把 machine-local wiring、project-local activation 與 operations history 分開管理。它要解決的，是每個 CLI 都各自長出一份會慢慢漂移的能力副本。

也因為如此，這個 repository 才會把 `registry/`、`runtime/`、`local/`、`ops/`、template export、rebuild flow、boundary verification、bootstrap 與 publishability checks 放在同一個系統裡。UniText 真正想做的，是讓 shared AI tooling 可以跨 CLI、跨機器、跨專案生命週期地被攜帶、審查與重複建立。

---

## 為什麼需要它

如果你同時使用多個 AI CLI 工具，資源很容易散落各處：

- 同一個 skill 被定義了三次，而且三份內容還略有差異
- MCP server 設定散在各種不同格式，其他工具根本讀不到
- 只有某一個 CLI 看得懂的 agent 指令
- 根本不知道哪一份才是 canonical copy

UniText 用一個共享 registry、一個 tracked runtime read model、以及一層受治理的 delivery layer 解決這件事。**一份定義，所有工具共用。**

---

## 運作方式

```text
UniText/
├── registry/          ← canonical definitions（存在什麼）
│   ├── skills/        ← shared skill definitions
│   ├── mcp/           ← MCP server definitions
│   ├── agents/        ← agent instructions & personas
│   └── workflow/      ← runbooks、plans、conventions
│
├── runtime/           ← tracked runtime read model（consumer agents 先讀什麼）
│   ├── START.md       ← 低噪音 agent 入口
│   ├── RULES.md       ← runtime-safe rule quickref
│   ├── ROUTES.md      ← intent → entrypoint mapping
│   └── skills/        ← 指回 canonical source 的 runtime projections
│
├── local/             ← deployment overlay（在這台機器上怎麼接）
│   ├── docs/          ← path maps、deployment notes
│   └── scripts/       ← 這台機器要用的 sync scripts
│
└── ops/               ← operations state（不是 shared resources）
    └── history/       ← timestamped audit trail
```

`registry/` 層是 platform-agnostic 的，使用邏輯 canonical path（例如 `/registry/skills`、`/registry/mcp`），而不是作業系統專屬的絕對路徑。`runtime/` 層是 tracked consumer-facing read model。`local/` 層則負責把 runtime surface 解析到你實際的機器上。

---

## 架構

**Registry-first、adapter-enabled、operations-governed。**

| Layer | Role |
|-------|------|
| **Registry** | 定義有哪些 shared resources，以及它們的 canonical identity |
| **Runtime** | 提供 tracked、低噪音的 consumer read model 與 runtime projections |
| **Adapter** | 把 runtime / registry 內容送到各個 CLI（mirror、symlink、native-config、pointer） |
| **Operations** | 管理何時、如何做 mutation - 包含 backup、dry-run 與 audit trail |

### 資源類型

| Type | Logical Root | 放什麼 |
|------|--------------|--------|
| `skills` | `/registry/skills` | 供 AI agents 共用的 skill definitions |
| `mcp` | `/registry/mcp` | 跨 CLI 的 MCP server definitions |
| `agents` | `/registry/agents` | 共用 agent instructions、persona、system prompts |
| `workflow` | `/registry/workflow` | runbooks、planning templates、conventions |

### Delivery Modes

每種資源都可以依 CLI 能力採用不同的 delivery 方式：

- `pointer` - discovery only，不複製內容
- `mirror` - 透過 robocopy / rsync 做本機複本
- `symlink` - 指向 canonical source 的固定路徑連結
- `native-config` - 註冊到 CLI 自己的設定格式中

---

## 開始使用

### 1. Fork 或 clone 這個 repository

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. 加入你的第一個資源

在 `registry/skills/` 底下建立一個 skill：

```text
registry/skills/my-skill/
└── SKILL.md
```

最小 `SKILL.md`：

```yaml
---
name: my-skill
description: 這個 skill 的一句話說明
---

## Usage

給 AI agent 的操作說明...
```

### 3. 把它註冊到 catalog

在 `INDEX.md` 新增一筆 entry：

| Field | Value |
|-------|-------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. 初始化本機 CLI wiring

優先使用跨平台的 bootstrap 路徑：

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

如果你的系統以 `python3` 作為 Python 入口，請把上述指令中的 `python` 換成 `python3`。

`bootstrap.py` 會重建 tracked `runtime/` layer、將 machine-local skills targets 對齊到 `runtime/skills`、更新 Codex 的 `skills_path`、保持 tracked project `.mcp.json` 為 template-safe seed，並在偵測到 Copilot CLI 時註冊同一個 `unitext-registry` MCP server 到 `~/.copilot/mcp-config.json`。`sync-skills.ps1` 仍保留作為 Windows PowerShell 的參考實作。

---

## 支援的 CLIs

| CLI | Delivery Mode | Notes |
|-----|---------------|-------|
| **Claude Code** | mirror / symlink + project-local settings | `.claude/settings.json`、repo `.mcp.json`、`~/.claude/skills` |
| **Gemini CLI** | mirror / symlink | `~/.gemini/skills` |
| **Codex** | native-config + project-local MCP | `skills_path` 指向 `~/.codex/skills` 下的本機 runtime target；canonical MCP 留在 repo-local `.mcp.json` |
| **Copilot CLI** | global MCP config + repo instructions | `~/.copilot/mcp-config.json` 用於 MCP wiring；repo instructions 來自 `AGENTS.md` / related files |

完整的 starter local overlay 與 exported path-map stub 請見 [template/examples/local/README.md](../../template/examples/local/README.md) 與 [template/examples/local/docs/PATH_MAP.template.md](../../template/examples/local/docs/PATH_MAP.template.md)。

如果你想把此 repository 轉成乾淨的新 starter project，而不是直接使用 authoring workspace，請依 [REBUILD_AS_NEW_PROJECT.md](../../REBUILD_AS_NEW_PROJECT.md) 操作。

### Cross-Platform Baseline

GitHub-hosted starter template 的目標是支援 `Claude Code`、`Codex`、`Gemini CLI`、`Copilot CLI`，以及 `Windows`、`macOS`、`Linux`。

目前驗證狀態比目標 baseline 窄：`Windows / PC` 是目前唯一具備完整 end-to-end authoring-host 證據的平台；`macOS` 與 `Linux` 仍是設計目標，但尚未在完整 bootstrap、delivery、governance flow 上完成同等強度 revalidation。

tracked `.mcp.json` 是給 fresh clone 的 relative-path seed。支援的 first-run path 仍是：

```bash
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

這條路徑是 authoritative setup path，因為它會重建 `runtime/`、對齊 machine-local delivery targets，並保持 tracked project MCP seed 為 relative-path、template-safe 狀態。

---

## 治理規則

UniText 採用 **no silent changes** 政策：

1. **只接受明確 trigger** - `bootstrap`、`sync`、`adopt`、`repair`
2. **先備份再 mutation** - 任何破壞性操作都會先在 `ops/` 建立 timestamped snapshot
3. **先 dry-run 再 delivery** - 在實際變更前先預覽
4. **有衝突就停止** - 若同一資源有兩個版本不一致，系統會停下來交由人工審查
5. **完整 audit trail** - 每一次操作都會寫入 `ops/history/`

正式 adoption flow：`SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## 文件

| File | Purpose |
|------|---------|
| [RUNTIME.md](../../RUNTIME.md) | agent-first startup entrypoint for runtime surface |
| [INDEX.md](INDEX.md) | Discovery entry point - 目前有哪些資源、在哪裡 |
| [VISION.md](VISION.md) | 架構原則與設計理由 |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | 所有 shared resources 的 metadata contract |
| [OPERATIONS.md](OPERATIONS.md) | Delivery modes、triggers 與安全規則 |
| [PROJECT_MODES.md](PROJECT_MODES.md) | 區分 authoring repo 與 project template |
| [WORKSPACE_SENSITIVE_METADATA_RULES.md](WORKSPACE_SENSITIVE_METADATA_RULES.md) | workspace-sensitive metadata detection 的 schema、維護規則與 validation flow |
| [DOCUMENT_PLACEMENT_POLICY.md](DOCUMENT_PLACEMENT_POLICY.md) | shared、local、authoring、operations 文件的 placement matrix |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | secret 儲存、redaction、password / API key 邊界 |
| [MILESTONES.md](MILESTONES.md) | 量化的 phase 目標與外部審查準備檢查點 |
| [BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md](../../BOUNDARY_INCIDENT_REVIEW_TEMPLATE.md) | boundary drift 事件的可重複 review template |
| [TEST_BASELINE.md](../../TEST_BASELINE.md) | 目前 automated test baseline、coverage scope 與 rebuild priorities |
| [docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md](docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md) | 目前審查波次使用的 `8 + 4` 精選 skills 集合 |
| [docs/reviews/EXTERNAL_REVIEW_PACKAGE.md](docs/reviews/EXTERNAL_REVIEW_PACKAGE.md) | 審查者閱讀順序、範圍與可重複匯出流程 |
| [docs/reviews/external-review-bundle.contract.json](../../docs/reviews/external-review-bundle.contract.json) | external review package 的 machine-readable membership 與 reading order contract |
| [docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md](docs/reviews/EXTERNAL_REVIEW_COVER_NOTE.md) | 給外部審查者的送審說明 |
| [docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md](docs/reviews/EXTERNAL_REVIEW_HIGHLIGHTS.md) | 供快速掌握的精簡審查摘要 |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | template release cleanup 的範圍、排除項與匯出流程 |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | starter package 發布前的清理檢查清單 |
| [REBUILD_AS_NEW_PROJECT.md](../../REBUILD_AS_NEW_PROJECT.md) | 將目前 repo 重建成乾淨 starter baseline 的 fresh-project rebuild flow |
| [docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md](../../docs/adapters/COPILOT_CLI_ADAPTER_NOTE.md) | 將 Copilot CLI 納入 cross-platform starter baseline 的 scope note |
| [docs/architecture/INTEGRATION_SURFACE_PROFILES.md](../../docs/architecture/INTEGRATION_SURFACE_PROFILES.md) | bootstrap、verify、runtime catalog enrichment 共用的 integration-surface contract |
| [docs/plans/CROSS_PLATFORM_SCRIPT_PORTABILITY_PLAN.md](../../docs/plans/CROSS_PLATFORM_SCRIPT_PORTABILITY_PLAN.md) | 將 PowerShell-first governance scripts 漸進移向跨平台 toolchain 的 migration plan |
| [docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md](../../docs/plans/EXISTING_ENVIRONMENT_ADOPTION_PLAN.md) | 將 UniText 接入既有工作環境時的 operator plan |
| [docs/concepts/SKILL0_COLLABORATION_VISION.md](docs/concepts/SKILL0_COLLABORATION_VISION.md) | 說明 UniText 與 skill-0 如何分工：一個做治理與分發，一個做拆解與原子化提煉 |
| [docs/architecture/AGENT_SELF_REPAIR_SCENARIO_SIMULATION.md](docs/architecture/AGENT_SELF_REPAIR_SCENARIO_SIMULATION.md) | 用情境模擬判斷未來執行障礙是否可由系統 agent 自我修復，以及應停在哪個治理層級 |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | 給 agents 與協作者的 local-first 發布邊界 |

human reading order：`README.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `PROJECT_MODES.md` → `WORKSPACE_SENSITIVE_METADATA_RULES.md` → `DOCUMENT_PLACEMENT_POLICY.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `REBUILD_AS_NEW_PROJECT.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md`

consumer agent reading order：`RUNTIME.md` → `runtime/START.md` → `runtime/RULES.md` → `runtime/ROUTES.md` → `runtime/catalog.json`

authoring repo 不會因為 template 或 rebuild export 驗證乾淨就自動變成 publish-safe。需要 repo-side boundary check 時，請使用 `local/scripts/verify-workspace-boundaries.ps1`。

---

## 兩種使用方式

### 作為 starter template

Fork 這個 repo。移除 `ops/history/`、`backup/` 與這台機器專屬的 `local/` 路徑。把你自己的 skills 與 MCP definitions 放進 `registry/`。再依你的環境調整 `local/scripts/`。

### 作為 reference implementation

閱讀核心文件以理解架構。然後把 registry 結構、resource spec、delivery modes、operations audit trail 這些模式，移植到你自己的環境。

---

## 設計原則

- **Registry first** - 先定義，再 delivery
- **Discovery before automation** - 先知道有什麼，再做同步
- **Platform-agnostic contracts** - 規格用邏輯路徑，本機覆蓋層才用絕對路徑
- **Minimum viable metadata** - `id`、`type`、`canonical_location`、`status` 就足夠起步
- **Safe mutation** - 一律 dry-run + backup + explicit trigger
- **AI as consumer** - AI 模型讀取並使用 registry，但不負責保證 delivery

---

## 狀態

| Component | Status |
|-----------|--------|
| Core documentation | Stable |
| Registry structure | Active - `skills/`、`mcp/`、`workflow/`、`agents/` roots 已存在 |
| Skills registry | Active baseline - 第一批 canonical skills 已納管，後續擴充仍在進行 |
| Agents registry | Active seed - 已建立 `registry-curator` entry |
| MCP registry | Active baseline - 已有 canonical definition 與可執行的 read-only server |
| Workflow registry | Draft seed - 已有 workflow doc 與 plan template |
| Operations audit trail | Active |
| Sync、bootstrap 與 review scripts | `local/scripts/` 內的 active baseline |
| External review package | Active baseline - 已有 reviewer guide 與 export script |
| Template release cleanup | Release candidate - 已有 package guide、checklist、export + verify scripts、generic examples 與 local overlay skeleton |

---

## 授權

MIT

---

*給使用超過一個 AI 工具、並希望有單一真相來源的人。*
