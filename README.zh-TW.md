# UniText

[總覽](#總覽) · [快速開始](#快速開始) · [讀者路由](#讀者路由) · [檔案模型](#檔案模型) · [安全與發布](#安全與發布) · [核心文件](#核心文件) · [English](README.md)

> 以 Registry 優先（registry-first）的治理模式，管理 Claude Code、Codex、Gemini / Antigravity、GitHub Copilot 與相鄰 runtime 之間可重複使用的 AI agent 資源。

![Status](https://img.shields.io/badge/status-active_baseline-brightgreen)
![Runtime](https://img.shields.io/badge/runtime-Python_3%20%7C%20PowerShell_5%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

UniText 將可重複使用的 skills、MCP 定義、agent 指令、workflow 與 runtime 規則集中維護在單一 canonical registry（標準來源），再輸出較低噪音的 runtime 讀取面，最後以本機可審查流程交付到 host。

## 總覽

UniText 具備四個特性：

- **registry-first**：共用資源先有標準來源，再談交付
- **runtime-first**：agent 先讀簡化過的 runtime 入口，不直接進入全庫深度閱讀
- **local-first**：交付、驗證、備份與證據預設留在本機
- **adapter-aware**：可對接多種 AI runtime，而不是綁定單一工具

## 快速開始

### Windows

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\git-startup.ps1
python .\local\scripts\bootstrap.py --dry-run
python .\local\scripts\bootstrap.py --force
python .\local\scripts\verify-bootstrap.py
```

### macOS / Linux

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

## 讀者路由

| 你目前的角色 | 先讀 | 接著讀 |
|---|---|---|
| 第一次進來的人類讀者 | `README.md` | `INDEX.md` |
| Agent 或自動化流程 | `RUNTIME.md` | `runtime/START.md`、`runtime/catalog.json` |
| 維護者 | `VISION.md` | `OPERATIONS.md` |
| 貢獻者 | `CONTRIBUTING.md` | `OPERATIONS.md` |

## 檔案模型

| 層級 | 目的 | 典型內容 |
|---|---|---|
| `registry/` | Canonical source（標準來源） | skills、MCP 定義、agents、workflows |
| `runtime/` | Agent 讀取面 | 啟動檔與 projection |
| `local/` | 本機交付與接線層 | bootstrap、verify、sync、作業筆記 |
| `ops/` | 操作證據 | 報告、備份、review 套件 |
| `template/` | 可安全匯出的 starter |
| - | - | 範例、bootstrap 輸入 |

## 安全與發布

UniText 採用 **local-first**。clean 的 publishability report、private remote，或 GitHub template 都不代表可對外發布。

在準備任何外部 package 或發布前，請先閱讀：

- `NO_PUBLISH_POLICY.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `WORKSPACE_SENSITIVE_METADATA_RULES.md`

## 核心文件

| 檔案 | 用途 |
|---|---|---|
| `INDEX.md` | 人員導航與任務路由 |
| `RUNTIME.md` | Agent-first 啟動入口 |
| `VISION.md` | 架構意圖與非目標 |
| `OPERATIONS.md` | 交付模式、關卡、回復與驗證 |
| `DOCUMENT_PLACEMENT_POLICY.md` | 文件放置原則 |
| `RESOURCE_SPEC.md` | 共用資源 metadata 合約 |
| `docs/README.md` | `docs/` 目錄的入口頁 |

## 授權

[MIT License](LICENSE)
