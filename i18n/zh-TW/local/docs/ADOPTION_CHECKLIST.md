# Adoption Review Checklist

> 狀態：Active
> 用途：定義 adoption flow 中 `REVIEW` 步驟的最小檢查標準。

## Required

- [ ] 目錄名稱符合 `id` 規則
- [ ] `SKILL.md` 存在
- [ ] `SKILL.md` 以 frontmatter 開頭
- [ ] frontmatter 至少包含 `name` 與 `description`
- [ ] `canonical_location` 可合理對應到 `/registry/{type}/{id}`
- [ ] 無明顯損壞、空白或截斷內容

## Recommended

- [ ] 有 `LICENSE.txt` 或等價授權說明
- [ ] 有清楚的 Usage、Workflow 或 Process 段落
- [ ] 無硬編碼的個人帳號與本機絕對路徑
- [ ] 若含 scripts / references，路徑關係清楚且可被 agent 發現

## Review Outcome

- `approve`
  - 可直接進入 `DRY-RUN`
- `needs-fix`
  - 需先補 metadata 或清理內容
- `hold`
  - 有 canonical source 爭議或內容品質問題，不可進入 `ADOPT`
