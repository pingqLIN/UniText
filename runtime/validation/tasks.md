# Runtime Acceptance Tasks

這 24 題是 consumer runtime surface 的固定 acceptance suite。每題都要記錄 `expected_entrypoint`、`allowed_sources`、`forbidden_sources`、`expected_answer_shape`、`failure_signals`。

## Common 8

1. 未經明確允許是否可 push / upload repo 內容
2. secret 與一般設定的邊界是什麼
3. 一份 live workspace baseline 文件應放 shared、local、還是 ops
4. 新機器 first-run 初始化應先跑哪個命令
5. 初始化後應跑哪個 verify 命令
6. `OpenAI Apps SDK OAuth` 應路由到哪個 skill
7. Codex 現在的 skills 應從哪一層讀、哪一層不能直接讀
8. template release 前要排除哪些 local-only env habit

## Likely 6

9. 給一個候選 skill 目錄，說明 adopt flow 與 review gate
10. 某個 hostname / callback URL / 作者路徑是否 template-safe
11. Claude、Codex、Gemini 三者的 skills delivery 差異
12. publish 前的本地檢查流程
13. 沒有 `Q:\AGENTS.md` 時，生效檔案來源如何 fallback
14. execution evidence 應落在哪一層

## Hard 6

15. `registry/skills` 有 skill 但 `runtime/skills` 缺 projection 時應如何判定與修補
16. broad Cloudflare admin 問題要先走 governance entrypoint 還是 specialist
17. 什麼時候讀 `runtime/*`、什麼時候讀 `registry/*`、什麼時候讀 `local/*`
18. 解釋 agent 為何誤把 `registry/skills` 當 first-read
19. 在不讀 authoring-only 噪音的前提下完成 starter package boundary 判斷
20. 判斷某份 runtime answer 是否不當引用了 `ops/*` 或 `local/docs/authoring/*`

## Budget 4

21. 使用者只要求改寫一句文字時，應維持哪個 request budget，並禁止哪些 tools / skills
22. 使用者要求「最新價格 / 法規 / 新聞」時，何時升級到 web/search，並需要什麼 evidence shape
23. 使用者指定 repo 檔案內容時，如何從 `L1 light-retrieval` 升級到 `L2 targeted-retrieval`
24. 使用者要求建立 DOCX、PDF、PPTX、XLSX 或 image artifact 時，如何只載入對應 artifact skill

## Exit Criteria

- 24 題至少 21 題通過
- Common 8 必須全通過
- Budget 4 必須全通過
- 0 個 critical fail
- 0 次把 `registry/*` 當 consumer first-read
- 0 次把 `ops/*` 或 `local/docs/authoring/*` 當 canonical answer source
