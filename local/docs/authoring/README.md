# Authoring References

> 狀態：Reference Only  
> 用途：說明 `local/docs/authoring/` 的文件角色，避免被誤認成 canonical source。

## 1. Positioning

`local/docs/authoring/` 保存的是作者整理過程中的參考版本與延伸草稿。  
它們有助於理解專案如何從 authoring workspace 收斂到 template base，但不是對外審查時的正式入口。

## 2. Canonical Source Rule

對外審查、對內引用、catalog discovery，應優先閱讀 repo root 的文件：

| Canonical doc | Reference role |
|---|---|
| `README.md` | 專案總覽與對外入口 |
| `INDEX.md` | discovery 與 catalog entry point |
| `VISION.md` | 架構原則 |
| `RESOURCE_SPEC.md` | shared resource contract |
| `OPERATIONS.md` | delivery 與 mutation governance |
| `PROJECT_MODES.md` | template / authoring 模式區分 |

## 3. When To Use This Folder

以下情況才建議讀取這個資料夾：

- 需要比 root docs 更早期的 authoring 脈絡
- 需要比對 template 收斂前後的文件差異
- 需要回看某些中間版文字如何形成

若目的只是整理外部審查資料，請直接使用 repo root docs 與 `EXTERNAL_REVIEW_PACKAGE.md`。
