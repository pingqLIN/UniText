# External Audit Orchestrator Usage Guide

[繁體中文](USAGE.zh-TW.md)

This guide walks through the practical path for using External Audit Orchestrator in a local development session.

## 1. Choose The Review Scope

| Scope Type | Use When | Required Value |
|---|---|---|
| `WorkingTree` | Review all current unstaged and staged changes | None |
| `Staged` | Review only staged changes before commit | None |
| `CommitRange` | Review a historical or branch range | `base..head` |
| `Path` | Review one folder or file surface | Relative path such as `src/auth` |
| `Manual` | Ask a design, release, or process question | Short question text |

Prefer the smallest scope that still contains the real risk. A narrow packet is easier for an external reviewer to inspect accurately.

## 2. Choose One Mode

| Mode | Choose It When | Stop Condition |
|---|---|---|
| `same-provider-subagent` | A local Codex or Claude reviewer path is available | Reviewer returns raw output |
| `external-web` | The user wants visible browser-based review | Raw web response is saved locally |
| `external-cli-mcp` | A stable reviewer CLI or MCP tool exists | stdout or transcript is captured |
| `tb2-template` | The goal is future TB2 handoff | Request JSON is exported |

Do not treat `tb2-template` as a completed audit. It creates handoff artifacts only.

## 3. Build A Packet

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

The generated packet includes:

- `Audit Goal`
- `Scope`
- `Project Context`
- `Change Evidence`
- `Checks Already Run`
- `Questions For Reviewer`
- `Reference Inputs`
- `Expected Output Format`

## 4. Run The Default Flow

Use the unified runner when you want one command to build the packet and prepare the selected review path.

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

If the reviewer output is produced later, save it to a local file and normalize it:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\run-external-audit-flow.ps1" `
  -SkillRoot $skillRoot `
  -TargetProject $targetProject `
  -Mode same-provider-subagent `
  -ScopeType WorkingTree `
  -RawReviewPath "$targetProject\.audit\raw-review.json" `
  -Disposition auto
```

## 5. Use External Web Review

Use this path when the review must remain visible and human-supervised.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\run-external-audit-flow.ps1" `
  -SkillRoot $skillRoot `
  -TargetProject $targetProject `
  -Mode external-web `
  -ScopeType Path `
  -ScopeValue "src/auth" `
  -Summary "Prepare a web reviewer packet for the auth changes."
```

Then:

1. Open the generated audit packet.
2. Paste it into the selected web reviewer.
3. Ask for read-only findings only.
4. Save the raw response under the target project, for example `.audit/raw-review.md`.
5. Normalize that saved response with `-RawReviewPath`.

## 6. Export A TB2 Request Template

Use TB2 template mode when you want traceable request artifacts for a later TB2 reviewer run.

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

By default, the request references the packet path and `packet_sha256` instead of embedding the full packet. Use embedded transport only when the operator accepts the sensitivity risk.

## 7. Normalize Reviewer Output Directly

When you already have raw reviewer output, run the normalizer directly.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$skillRoot\scripts\normalize-audit-report.ps1" `
  -RawReviewPath "$targetProject\.audit\raw-review.json" `
  -AuditMode same-provider-subagent `
  -ProjectPath $targetProject `
  -Scope "working-tree" `
  -Disposition auto `
  -NextAction "Fix warning-or-higher findings, then rerun the audit."
```

The report should include findings ordered by severity, assumptions, reference inputs, disposition, and the exact next action.

## 8. Release Validation

Before publishing or installing the package outside the repository, run the smoke test from the UniText root.

```powershell
.\validation\run-smoke.ps1
```

If the Codex mirror is unavailable:

```powershell
.\validation\run-smoke.ps1 -SkipCodexMirror
```

Also check that generated smoke artifacts are not staged and that `README.md`, `README.zh-TW.md`, and this guide still match the current scripts and references.
