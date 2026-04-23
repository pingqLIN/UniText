# Skills Registry

這個目錄承載的是 **canonical shared skills**。

原則：

- 每個 skill 使用 `registry/skills/{id}/` 結構
- `SKILL.md` 為主要內容入口
- 其他參考文件、腳本與資產應與 skill 一起收斂在同一目錄
- 是否採用 `symlink`、`mirror`、`native-config` 由 adapter / operations 層決定
- `INDEX.md` 負責 catalog discovery；目錄存在不代表已被 catalog 正式列出
- `docs/reviews/ESSENTIAL_SKILLS_SHORTLIST.md` 只定義對外審查主集，不等於完整 skills registry

目前此目錄已作為 UniText skills adoption 的正式落點。

