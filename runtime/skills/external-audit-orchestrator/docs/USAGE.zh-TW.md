---
runtime_projection: true
source_of_truth: registry/skills/external-audit-orchestrator/docs/USAGE.zh-TW.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/external-audit-orchestrator/docs/USAGE.zh-TW.md`
> Source of truth: `registry/skills/external-audit-orchestrator/docs/USAGE.zh-TW.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# External Audit Orchestrator 使用教學

[English](USAGE.md)

這份教學說明如何在本機開發 session 中使用 External Audit Orchestrator。

## 1. 選擇 Review Scope

| Scope Type | 使用時機 | 必要值 |
|---|---|---|
| `WorkingTree` | 審查目前所有 unstaged 與 staged changes | 無 |
| `Staged` | commit 前只審查 staged changes | 無 |
| `CommitRange` | 審查歷史範圍或 branch range | `base..head` |
| `Path` | 只審查特定 folder 或 file surface | 相對路徑，例如 `src/auth` |
| `Manual` | 詢問設計、release 或 process 問題 | 簡短問題文字 |

優先選擇仍能涵蓋真實風險的最小 scope。packet 越窄，外部 reviewer 越容易準確檢查。

## 2. 選擇一種 Mode

| Mode | 適用情境 | 停止條件 |
|---|---|---|
| `same-provider-subagent` | 可使用本機 Codex 或 Claude reviewer path | reviewer 回傳 raw output |
| `external-web` | 使用者想要可見的 browser-based review | raw web response 已保存到本機 |
| `external-cli-mcp` | 已有穩定 reviewer CLI 或 MCP tool | stdout 或 transcript 已保存 |
| `tb2-template` | 目標是未來 TB2 handoff | request JSON 已輸出 |

不要把 `tb2-template` 視為完成 audit。它只建立 handoff artifacts。

## 3. 建立 Packet

```powershell
$skillRoot = "Q:\UniText\runtime\skills\external-audit-orchestrator"
$targetProject = "Q:\Projects\your-project"

powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\build-audit-packet.ps1" `
  -ProjectPath $targetProject `
  -ScopeType WorkingTree `
  -Summary "Review the current working tree before acceptance." `
  -Question "Are there blocking bugs or regressions?" `
  -Question "Are tests or rollback notes missing?" `
  -Check "npm test passed locally." `
  -Reference "local: Q:\Projects\reference-project - consulted for reviewer packet shape"
```

產出的 packet 會包含：

- `Audit Goal`
- `Scope`
- `Project Context`
- `Change Evidence`
- `Checks Already Run`
- `Questions For Reviewer`
- `Reference Inputs`
- `Expected Output Format`

## 4. 執行預設 Flow

如果你希望一個指令完成 packet build 與 review path 準備，使用 unified runner。

```powershell
$skillRoot = "Q:\UniText\runtime\skills\external-audit-orchestrator"
$targetProject = "Q:\Projects\your-project"

powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\run-external-audit-flow.ps1" `
  -SkillRoot $skillRoot `
  -TargetProject $targetProject `
  -Mode same-provider-subagent `
  -ScopeType WorkingTree `
  -Summary "Review the current implementation batch." `
  -Question "Are there any P0/P1 bugs?" `
  -Question "Is the validation evidence sufficient?"
```

如果 reviewer output 稍後才產生，先保存成 local file，再正規化：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\run-external-audit-flow.ps1" `
  -SkillRoot $skillRoot `
  -TargetProject $targetProject `
  -Mode same-provider-subagent `
  -ScopeType WorkingTree `
  -RawReviewPath "$targetProject\.audit\raw-review.json" `
  -Disposition auto
```

## 5. 使用 External Web Review

當 review 必須可見且由人監督時，使用這條路徑。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\run-external-audit-flow.ps1" `
  -SkillRoot $skillRoot `
  -TargetProject $targetProject `
  -Mode external-web `
  -ScopeType Path `
  -ScopeValue "src/auth" `
  -Summary "Prepare a web reviewer packet for the auth changes."
```

接著：

1. 開啟產出的 audit packet。
2. 貼到指定 web reviewer。
3. 明確要求 read-only findings。
4. 將 raw response 存在 target project，例如 `.audit/raw-review.md`。
5. 用 `-RawReviewPath` 正規化保存下來的 response。

## 6. 匯出 TB2 Request Template

當你需要可追蹤、供未來 TB2 reviewer 執行的 request artifacts 時，使用 TB2 template mode。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\run-external-audit-flow.ps1" `
  -SkillRoot $skillRoot `
  -TargetProject $targetProject `
  -Mode tb2-template `
  -ScopeType CommitRange `
  -ScopeValue "main..HEAD" `
  -Summary "Export TB2 request artifacts for branch review." `
  -Apply
```

預設 request 只引用 packet path 與 `packet_sha256`，不會嵌入完整 packet。只有在 operator 接受敏感內容風險時，才使用 embedded transport。

## 7. 直接正規化 Reviewer Output

如果你已經有 raw reviewer output，可以直接執行 normalizer。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\normalize-audit-report.ps1" `
  -RawReviewPath "$targetProject\.audit\raw-review.json" `
  -AuditMode same-provider-subagent `
  -ProjectPath $targetProject `
  -Scope "working-tree" `
  -Disposition auto `
  -NextAction "Fix warning-or-higher findings, then rerun the audit."
```

report 應包含依 severity 排序的 findings、assumptions、reference inputs、disposition，以及明確 next action。

## 8. Release Validation

在將 package 發布或安裝到 repo 外之前，從 UniText root 執行 smoke test。

```powershell
.\validation\run-smoke.ps1
```

如果 Codex mirror 不可用：

```powershell
.\validation\run-smoke.ps1 -SkipCodexMirror
```

同時確認 generated smoke artifacts 沒有被 staged，且 `README.md`、`README.zh-TW.md` 與這份教學仍符合目前 scripts 與 references。
