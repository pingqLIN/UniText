# Skills Registry

這個目錄承載的是 **canonical shared skills**。

原則：

- 每個 skill 使用 `registry/skills/{id}/` 結構
- `SKILL.md` 為主要內容入口
- `SOURCE.yaml` 為來源與授權資料入口
- 其他參考文件、腳本與資產應與 skill 一起收斂在同一目錄
- 是否採用 `symlink`、`mirror`、`native-config` 由 adapter / operations 層決定

目前此目錄已作為 UniText skills adoption 的正式落點。

補充：

- 自 `2026-03-27` 起，保留於此目錄的每個 active skill 都必須附帶 `SOURCE.yaml`
- GitHub 匯入 skill 需標記來源 repo、來源路徑、授權、匯入日期
- 無法確認來源或再分發邊界的 skill 不應保留在此目錄
- 目前來源總覽見 [SOURCES.md](SOURCES.md)
