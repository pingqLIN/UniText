# UniText — Essential Skills Shortlist

> 狀態：Active
> 用途：定義目前外部審查主集，只保留 `8 + 4` 的精選 skills，而不是全量候選池。
> 註：截至 `2026-04-10`，authoring tree 的 `registry/skills/` 共有 `44` 個 skill 目錄；本文件只描述 review shortlist，不描述完整 inventory。

## Selection Rule

這份 shortlist 以「必備 skill」為主題，篩選標準如下：

- 跨專案通用
- 能代表 shared registry 的實際價值
- 外部審查看得懂用途
- 優先保留具備 scripts、references、examples 的複雜或入口型 skill

## Core 8

| Skill | Why It Stays |
|---|---|
| `pdf` | 高通用、高複雜度，含多個 scripts 與 reference docs |
| `docx` | 高通用、高複雜度，含 OOXML tooling 與 schema assets |
| `xlsx` | 高通用，代表結構化資料與 spreadsheet workflow |
| `pptx` | 補齊 office artifact 類型，含 scripts 與範例資產 |
| `mcp-builder` | 與 UniText 定位最接近，屬於明確的入口型／平台型 skill |
| `skill-creator` | 直接支援 skill 生態擴張，屬於入口型 skill |
| `webapp-testing` | 代表可驗證、可互動的 QA / browser workflow |
| `doc-coauthoring` | 補齊 structured writing / spec workflow 類型 |

## Expansion 4

| Skill | Why It Stays |
|---|---|
| `frontend-design` | 保留 UI / frontend output 類型代表 |
| `web-artifacts-builder` | 補齊較重型的 artifact / app composition 類型 |
| `internal-comms` | 保留面向內部協作與 status reporting 的實用 skill |
| `theme-factory` | 保留 styling / theming 類型，適合作為 artifact 輸出層補充 |

## Complex / Entry-Type Check

這份 `8 + 4` 不需要額外再新增新的類型，因為已經包含多個複雜或入口型 skill：

- `pdf`
- `docx`
- `pptx`
- `mcp-builder`
- `skill-creator`
- `webapp-testing`

這些 skill 都具備至少一項：

- 內部 scripts
- reference docs
- template / example assets

## Out Of Scope For This Review Wave

以下類型目前不列入外部審查主集：

- Hugging Face 專用技能群
- 藝術 / 品牌 / GIF 類垂直技能
- 其他高專用性但非必備的技能

它們不是無價值，而是暫時不屬於「必備 skill」主題。

