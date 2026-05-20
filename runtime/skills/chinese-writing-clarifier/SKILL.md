---
name: chinese-writing-clarifier
description: 幫助 AI 將「中文主體文本」中的中英混用進行統一中文潤稿：保留必要專有名詞、代碼與品牌名稱，將可對映的英文術語轉為中文並補齊工程語義註記。Use this skill when polishing Chinese responses that accidentally keep mixed English phrases, especially in Docker/Docker workflow, CI parity, deployment readiness, logs, ports, and architecture reviews.
runtime_projection: true
source_of_truth: registry/skills/chinese-writing-clarifier/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/chinese-writing-clarifier/SKILL.md`
> Source of truth: `registry/skills/chinese-writing-clarifier/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# JING JING framework


## 啟動前主動詢問（必要）
每次啟用本 skill 前，必須先詢問使用者下列兩項，並明確等待回覆：
- 是否先切到「新對話階段」（是/否）。
- 是否使用 `5.3-codex-spark` 進行文本修訂（是/否）。

預設流程：
- 使用者回覆「是」-> 開新對話後，用選定模型執行本 skill 的中文化改寫流程。
- 使用者回覆「否」-> 保持目前對話階段，但仍可執行同樣流程。
- 若未明確回覆模型選項，先詢問並保留現有預設（不自動推測）。
## 目標
- 針對中文輸出中的英中混寫進行統一修正。
- 只要不是明確專有名詞（產品名稱、版本號、API 名稱、代碼語法、命令/路徑/檔名/識別碼），就應優先使用中文。
- 不改寫句意與事實，只改寫語言表達與術語映射。

## 啟用情境
- 使用者要求「中文潤稿」「把英文清掉」「修中文混英」「文案轉中文」等任務。
- 需要檢查任務性文本（如 deployment、CI、release、測試流程、問題回報、設計說明）中英混合程度時。

## 作業流程（固定順序）
1. 先做「術語切分」。
   - 標示出英文專有詞、術語短語、單個英文字連接詞。
2. 套用連接詞規則：任意單個英語連接詞（如 `and`, `or`, `with`, `for`, `on`, `in`, `of`, `to`, `from`, `is`, `are`）優先轉為中文。
3. 套用術語映射規則：有常見中文對應的英文技術詞改為中文並附註對應詞，格式為「英文詞[中文]」或「中文（若上下文更順可省略英文）」。
4. 將結果重組為自然中文句，保留原始專有名詞原樣，例如：
   - 服務名稱、專案名稱
   - CLI 指令、參數、檔案/資料夾名稱
   - 代碼片段、標識符、版本字串
5. 回傳完整修正版，不只列出對照表；若有歧義以最保守做法註明假設。

## 專有名詞映射示例（可直接複用）
- deployment readiness [部屬準備程度]
- CI parity [持續集成一致性]
- Docker workflow [Docker 工作流程]
- ports [連接埠]
- logs [日誌]
- health [健康檢查]
- read-only [只讀]
- no-secret [無機密]
- non-destructive guardrail [非破壞性圍籬]
- prompt [提示詞]

## 對照測試清單（每次啟動必做）
- 逐句掃描英文單詞。凡是能中文化且不破壞專有名詞的，都應轉成中文或「英文[中文]」標註。
- 檢查是否存在未轉換的英語連接詞（and/or/with/for/on/in/of/to/from/is/are/was/will/be/if/then/only/only if）。若有，優先轉換。
- 檢查否定/條件語句是否自然中文化（如 if, unless, unless already, fallback 等）但不改變邏輯條件。
- 例行比對：原文中每個英文 token 是否落在「保留例外」清單；若是，必須原樣保留或只加中文註記。
- 確認修訂後段落可直接閱讀，不殘留「中英交錯」雜訊。

## 常見混寫邊界檢核（判斷準則）
- 專有名詞、品牌、縮寫與產品名：保留原文，不做意義改寫。例：`Gordon`, `Docker`, `CI`, `GitHub`, `Kubernetes`, `Terraform`。
- 命令與路徑：保留原文。例：`docker build`, `docker-compose.yml`, `--no-cache`, `/var/log`。
- 程式碼片段與識別符：保留原文。例：`REQ-123`, `REP_B02`, `if (healthcheck)`。
- 句中可對映技術概念：盡量中文化並加註中文。例：`deployment readiness`、`reproducible environment`。
- 品牌/協議/規範縮寫：可保留縮寫，但建議加中文解釋。例：`SLA[服務等級協定]`、`RBAC[基於角色存取控制]`。
- 附屬英文連結詞與介系詞：除非屬指令片段，務必中文化。

## CI/DevOps 套件詞彙庫（優先採用）
- branch [分支]
- commit [提交]
- commit message [提交訊息]
- build [建置]
- deployment readiness [部屬準備程度]
- CI/CD [持續整合/持續交付]
- build failure [建置失敗]
- reproducible environment [可重現環境]
- smoke test [冒煙測試]
- regression test [回歸測試]
- integration test [整合測試]
- health check [健康檢查]
- readiness [就緒檢查]
- liveness check [存活檢查]
- artifact [建置產物]
- pipeline [流水線]
- rollout [推展]
- rollback [回滾]
- namespace [命名空間]
- image [映像檔]
- tag [標籤]
- volume [磁碟卷]
- port [連接埠]

### 內建驗收清單（輸出前）
- 是否將可對映的關鍵術語都轉為中文且保持專有名詞保留。
- 是否保留 `REP_B02`、`REP_B05`、測試代碼、參數、路徑、檔名、數值與格式字串。
- 是否將所有英語連接詞都進行修正（若仍有，需說明例外）。
- 是否加入「詞彙對照」時能映射到高風險英文片語。
- 是否明確記錄存在歧義的詞彙與假設。

## 寫作禁忌
- 不要把整段改成英文。
- 不要把正常技術術語硬套成生硬直譯，若是專有名詞不可拆解則保留原文並加註中文。
- 不要改到 `REP_B02`、`REP_B05`、數值、欄位名、指令旗標等精準字串，除非明確要求改寫。

## 輸出格式（可選）
- 建議回覆「修訂版」：直接給出完整中文化文本。
- 必要時附「詞彙對照」欄位，列出高風險英文片語與對應中文，方便追蹤與後續審閱。
