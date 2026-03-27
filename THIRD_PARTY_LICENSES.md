# UniText — Third-Party Licenses

> 狀態：Active
> 用途：彙整目前 `registry/skills` 中第三方來源的授權資訊，並說明哪些內容屬於 holdback / 不進公開 package。

## 1. Scope

本文件處理的是：

- 目前 active shared skills 的第三方來源與授權
- catalog-only source repositories
- 已被移除或 holdback 的 restricted materials

本文件不取代：

- [LICENSE](LICENSE)
- [registry/skills/SOURCES.md](registry/skills/SOURCES.md)
- 各 skill 目錄內的 `SOURCE.yaml`

`LICENSE` 定義的是 UniText 專案本身的授權。  
本文件處理的是 UniText 所收錄或引用的第三方 skill 來源。

## 2. Active Third-Party Skill Sources

目前 active shared skills 已清理為 GitHub-backed entries，來源如下：

| Source repository | License | Current role |
|---|---|---|
| `obra/superpowers` | MIT | active imported skills |
| `affaan-m/everything-claude-code` | MIT | active imported skills |
| `github/awesome-copilot` | MIT | active imported skills |
| `nextlevelbuilder/ui-ux-pro-max-skill` | MIT | active imported skills |
| `sickn33/antigravity-awesome-skills` | Apache-2.0 | active imported skills |
| `VoltAgent/awesome-openclaw-skills` | MIT | catalog-only source, not directly imported |

更細的每-skill 對照請見：

- [registry/skills/SOURCES.md](registry/skills/SOURCES.md)
- 各 skill 目錄內的 `SOURCE.yaml`

## 3. Current Public Redistribution Position

目前公開 package 可納入的 shared skills，限於：

- 已存在於 `registry/skills/`
- 已附 `SOURCE.yaml`
- 授權邊界已確認允許公開再分發

這代表目前 active imports 的授權基線為：

- `MIT`
- `Apache-2.0`

## 4. Holdback / Removed Materials

以下 skill 類型目前不屬於公開 package：

- `pdf`
- `docx`
- `xlsx`
- `pptx`
- `doc-coauthoring`

原因如下：

- `pdf` / `docx` / `xlsx` / `pptx`
  - 原先內容帶有 Anthropic restricted redistribution 條款
  - 現已自 active registry 移除
- `doc-coauthoring`
  - 先前缺少足夠清楚的公開再分發依據
  - 現已自 active registry 移除

這些內容目前只能視為：

- 歷史 holdback 記錄
- 不得納入公開 package 的內容

## 5. Operational Rule

若新增新的第三方 skill source，至少要同步更新：

1. `registry/skills/<skill>/SOURCE.yaml`
2. [registry/skills/SOURCES.md](registry/skills/SOURCES.md)
3. 本文件（若是新增 source repository 或改變授權判讀）

若授權無法清楚證明可公開再分發，則不應納入 active public subset。
