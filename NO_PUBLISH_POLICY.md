# UniText — No-Publish Policy

> 狀態：Active
> 用途：定義哪些內容在未經明確許可前不得推送、上傳或張貼到任何網路服務。

## 1. Core Rule

除非使用者明確授權，否則下列內容不得對外推送、上傳、張貼或同步到任何網路服務：

- GitHub push
- 社群平台貼文
- 雲端文件
- paste service
- 任何第三方 API 或 hosting service

## 2. Default Sensitive Content

以下內容預設視為不可發布：

- 社群文草稿
- 與其他專案的比較或合作討論
- review notes
- strategy / roadmap / planning 文件
- 尚未正式對外宣告的設計方向

## 3. Permission Standard

可發布的前提必須是：

- 使用者明確表示可以發布
- 若只授權部分內容，僅能發布被授權的那部分
- `private repo` 不等於自動可發布

## 4. Agent Rule

所有 agent 在此 repo 內應遵守：

1. 未經明確許可，不得 `git push`
2. 未經明確許可，不得將內容貼到社群或任何外部服務
3. 若使用者只允許建立 remote 或建立 private repo，不可自行推定等於允許上傳其他敏感內容
4. 若內容涉及其他專案關係、策略討論或社群文，應採更保守標準

## 5. Current Explicitly Sensitive Topics

截至目前，以下類型內容應特別保守處理：

- 社群文草稿與對外發佈文案
- `SKILL0_COLLABORATION_VISION.md`
- 其他與 `skill-0` 或外部審查相關的策略討論

## 6. Operational Interpretation

若未來需要發布，建議分成三步：

1. 先確認允許發布的範圍
2. 再確認允許發布的目的地
3. 最後才執行 push / upload / posting
