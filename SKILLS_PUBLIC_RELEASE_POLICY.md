# UniText — Skills Public Release Policy

> 狀態：Active
> 用途：定義 skills 在 authoring workspace、本地驗證、review package、template package 與公開發布之間的邊界。

## 1. Policy Summary

UniText 對 skills 採以下發布原則：

- **本地驗證可使用 local-only materials**
- **公開版不得包含授權邊界不明或限制再分發的 skill 檔案**
- **公開版只應包含 template-safe examples 與已確認可公開再分發的 skills**
- **active shared skills 應優先收斂為可追溯的 GitHub-backed entries，並附來源資料**

這個原則的目標是：

- 保留 authoring 階段的實作與 dry-run 能力
- 避免把不適合再分發的 skill 內容帶進公開 repo 或 package
- 讓公開版的授權敘事與實際內容一致

## 2. Current Decision

本輪修補採用以下決策：

### Public Release Surface

- 不附上 proprietary 或 restricted-license skills 檔案
- 不將這些 skills 視為公開版的一部分
- 公開版只提供：
  - `example-skill`
  - 公開授權且可再分發的 skills
  - 相關說明文件與使用指引
  - 每個 active public skill 的來源資料

### Current Registry Treatment

- active shared skills 目前已清理為 GitHub-backed imports
- 每個 active skill 目錄均附 `SOURCE.yaml`
- skills 來源總覽集中於 `registry/skills/SOURCES.md`
- local-only 驗證材料若仍存在，只能位於公開 package 之外

## 3. Skills Treatment Matrix

| 類型 | 可留在 authoring workspace | 可進 review package | 可進 template package | 可進公開發布 |
|---|---|---|---|---|
| `example-skill` | Yes | Yes | Yes | Yes |
| 公開授權、已確認可再分發的 skill | Yes | Yes | Yes | Yes |
| local-only validation skill | Yes | No | No | No |
| proprietary / restricted-license skill | Yes | No | No | No |

## 4. Current Restricted Set

在公開版中，以下目前已知 skills 不應直接納入 package 或對外上傳面：

- `pdf`
- `docx`
- `xlsx`
- `pptx`
- `doc-coauthoring`

說明：

- `pdf`、`docx`、`xlsx`、`pptx` 目前帶有 Proprietary / restricted redistribution 風險
- `doc-coauthoring` 目前缺少明確 `LICENSE.txt`，在公開版中暫列為 holdback
- 這份清單是基於目前授權資訊的保守排除清單
- 是否未來重新納入，必須以明確可公開再分發授權為前提

## 4.1 Current Public Subset

根據目前 repo 內現成的授權資訊，以下 skills 可作為公開版第一波 public subset：

- `frontend-design`
- `internal-comms`
- `mcp-builder`
- `skill-creator`
- `theme-factory`
- `web-artifacts-builder`
- `webapp-testing`

這些 skills 目前均已改為 GitHub-backed entries，並附 `SOURCE.yaml`。目前其來源為 `sickn33/antigravity-awesome-skills`，授權為 Apache 2.0，可作為公開 review / release 的第一波候選內容。

## 5. Evidence Wording Rule

若某次 dry-run、驗證或設計評估曾使用 local-only skills，公開文件可使用以下敘事：

> 本地驗證曾使用 authoring-only skills 驗證流程可運作，但相關 skill 檔案不屬於公開再分發內容，因此未納入公開 package。

公開文件不得使用以下誤導性敘事：

- 暗示公開 package 已附上這些 skills
- 暗示 UniText 擁有這些 skills 的再分發權
- 用公開 package 去證明受限 skills 已被對外提供

## 6. Public Replacement Direction

為了恢復公開版中仍被 holdback 的類型覆蓋，後續將逐步補入公開授權的 replacement skills，優先順序如下：

1. 文件類
2. 結構化資料類
3. QA / testing 類
4. builder / workflow 類

在後續 replacement wave 完成前，公開版的 skills baseline 以：

- `example-skill`
- current public subset with GitHub-backed provenance
- shortlist metadata
- release policy explanation

為主。

## 7. Release Gate

若任一公開 package 含有：

- proprietary skills
- restricted-license skills
- local-only validation materials

則該 package 應視為：

**not release-safe**
