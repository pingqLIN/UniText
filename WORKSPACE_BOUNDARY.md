# UniText — Workspace Boundary

> 狀態：Active
> 用途：定義 authoring workspace、tracked source、exported package 三層邊界，避免把目前工作區誤當成可直接發布來源。

## 1. Boundary Summary

UniText 目前必須區分三層：

| Layer | 定義 | 可直接公開發布 |
|---|---|---|
| `authoring workspace` | 維護者目前正在使用的完整工作區，可能含本機驗證材料、歷史備份、審查草稿與導出產物 | No |
| `tracked source` | git 追蹤的 canonical repo 內容，用來生成 review package / template package | Not by default |
| `exported package` | 由 export scripts 產出的 review-safe 或 template-safe package | Yes, if verification passes |

核心原則：

- **不要直接把目前 authoring workspace 當成 release source**
- **公開交付應以 exported package 為準**
- **tracked source 是中介層，不等於可直接上傳的成品**

## 2. Authoring Workspace

authoring workspace 可以包含：

- `ops/history/` 中的 audit trail、backup、bootstrap records
- review 草稿與修補計畫
- local-only validation materials
- export scripts 產出的中間產物

這些內容可以存在於維護者工作區，但不應自動被視為公開發布內容。

## 3. Tracked Source

tracked source 的角色是：

- 保存 canonical docs
- 保存 registry 定義
- 保存 operations scripts
- 作為 export pipeline 的來源

tracked source 仍需經過 release hygiene 檢查，因為它可能同時承載：

- authoring-only docs
- review-specific docs
- local overlay 範本
- 不適合直接進公開 package 的內容

## 4. Exported Package

只有 exported package 才能視為正式的對外交付候選：

- review package：供外部審查
- template package：供 starter project / template release
- rebuild project：供 fresh-project baseline

判定原則：

- package 內容來自 export script
- package 已通過對應 verification
- package 不含 local-only、restricted-license、machine-specific residue

## 5. Current Workspace Hygiene Rules

以下內容不應影響 release source 判定：

- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- `ops/rebuild-project/`
- `ops/git-bundles/`
- `backup/`
- `recovered_*`
- `.bak_*`
- `local/docs/PATH_MAP.md`
- `local/docs/authoring/`
- `local/docs/reviews/`

## 6. Operational Rule

實務上請遵守：

1. authoring workspace 只用來編修與驗證
2. tracked source 用來產生 package
3. 真正對外的內容只取自 exported package

若三者發生衝突，以 exported package 的驗證結果為準，而不是以目前工作區的偶然狀態為準。
