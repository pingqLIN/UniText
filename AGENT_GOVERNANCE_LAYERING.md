# UniText Agent Governance Layering

> 用途：定義一個 simulation-first 的治理工具，讓 agent 可以依 `model / environment / instruction-profile` 解析出不同層級的生效配置。

## 1. 目標

這個工具解決的是：

- 不同模型需要不同的推理深度與 review 節奏
- 不同工作環境需要不同的更新、輸出與互動能力
- 不同指令模式需要不同的 checkpoint 與 handoff 密度

與其把這些差異散落在多份說明文件中，`UniText` 現在提供一個可直接執行的 resolver：

- 政策檔：`local/config/agent-governance-layers.json`
- 解析器：`local/scripts/resolve-agent-governance.py`

## 2. 層級順序

目前的覆蓋順序是：

1. `base`
2. `model`
3. `environment`
4. `instruction_profile`

也就是說，越後面的層級優先度越高；如果同一個 key 被多層設定，後者會覆蓋前者。

## 3. 解析內容

解析結果會包含：

- `matched_layers`
- `effective_config`
- `provenance`

其中 `provenance` 會明確指出每個生效 key 最後來自哪一層。

## 4. 使用方式

### A. 在網頁上解析與輸出

`project-map.html` 現在已內建治理面板，會直接使用：

- `Q:\AGENTS.md`
- `Q:\UniText\AGENTS.md`
- `local/config/agent-governance-layers.json`

頁面內可輸入：

- 治理模型
- 工作環境
- 指令配置
- 輸出位置

然後進行兩種操作：

- `解析治理`
  - 直接在頁面上顯示 matched layers、effective config、AGENTS sources 與 effective file-based instructions
- `寫出治理報告`
  - 若瀏覽器已授權 repo root 的讀寫權限，會把
    - `agent-governance-resolution.md`
    - `agent-governance-resolution.json`
    寫到指定輸出位置

預設輸出位置是：

- `Q:\UniText\ops\agent-governance`

目前的安全限制是：

- 頁面只接受位於目前 repo 之內的輸出位置
- 若尚未授權 repo root，頁面會先要求連結專案目錄
- 單純輸入文字路徑不會繞過瀏覽器的 File System Access 權限模型

### B. 在 CLI 上解析與輸出

最基本的解析：

```powershell
python local/scripts/resolve-agent-governance.py `
  --model gpt-5.4 `
  --environment codex-local-dev `
  --instruction-profile mapping
```

若要同時產生交接報告：

```powershell
python local/scripts/resolve-agent-governance.py `
  --model gpt-5.4 `
  --environment codex-local-dev `
  --instruction-profile mapping `
  --write-report
```

預設報告會寫到：

- `ops/agent-governance/agent-governance-resolution.json`
- `ops/agent-governance/agent-governance-resolution.md`

## 5. 預設範例

目前政策檔已提供幾類常見 profile：

- model
  - `gpt-5.4`
  - `gpt-5.4-mini`
  - `gpt-5.3-codex`
- environment
  - `codex-local-dev`
  - `browser-share-safe`
  - `yolo-unattended`
  - `ci-verify`
- instruction profile
  - `mapping`
  - `handoff`
  - `governance-review`
  - `yolo`

## 6. 治理定位

這個工具目前是：

- simulation-first
- report-first
- no-mutation

也就是說，它會告訴你「應該生效的配置是什麼」，但不會直接改寫任何 CLI、IDE、MCP 或 agent runtime 設定。

如果之後要接到更重的治理自動化，建議順序是：

1. 先用 resolver 穩定政策結構
2. 再把特定 key 接到可回復的 apply / rollback 流程
3. 最後才考慮 drift audit 與 guard task
