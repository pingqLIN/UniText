# UniText — Security Attack Input Evaluation Report

> Source checklist: `SECURITY_ATTACK_INPUT_CHECKLIST.md`
> Date: 2026-03-25
> Scope: Evaluate which attack-input items are materially relevant to the current UniText baseline, then propose concrete mitigations only for issues that should actually be handled.

## Executive Summary

這份檢視的結論是：

- `MCP read_registry_file(path)` 這條線目前已有合理的 repo-root confinement，暫時不是主要風險。
- 真正需要優先處理的不是傳統 `SQL injection` 或 `XSS`，而是本機 automation 工具常見的兩類問題：
  - `path traversal / arbitrary write`
  - `command injection`
- 最需要優先處理的不是同一級的「一包大問題」，而是不同風險層級的具體輸入面：
  1. `webapp-testing/scripts/with_server.py` 的 `shell=True`，在 AI agent 場景下應視為 `CRITICAL`
  2. `rollback-skills.ps1` 的 `$Id` 路徑拼接搭配 `Remove-Item -Recurse -Force`，應視為 `P0-B`
  3. `batch-adopt-skills.ps1` 與兩支 export 腳本都需要 path confinement，但風險等級不應混為一談
  4. `bootstrap.py` 的 `--repo-root` 問題存在，但考慮 `--force` 與現有結構檢查後，較合理的判定是 `MEDIUM`

## Findings That Need Treatment

### SEC-001 Critical: `with_server.py` 對不可信命令字串使用 `shell=True`

Impact: 如果 `--server` 內容可被不可信輸入影響，攻擊者可透過 shell metacharacters 執行額外命令；在 AI agent 可被 prompt injection 影響的場景下，這已接近遠端 RCE。

Evidence:

- `registry/skills/webapp-testing/scripts/with_server.py:37-40`
- `registry/skills/webapp-testing/scripts/with_server.py:68-74`

Why it matters:

- checklist 中的 `;`, `&&`, `||`, `|`, `$()` 這類 payload 在這裡不是理論測項，而是真的會進 shell
- 這支工具本來就是拿來包裝自動化測試，未來很容易被 agent 或 wrapper 當成公用 helper 呼叫
- 腳本目前的 docstring 明確展示 `cd backend && python server.py` 這類多指令 shell 用法，因此修補不能只做表面替換，必須重設介面

Recommended response:

1. 預設移除 `shell=True`。
2. 把 `--server` 改成明確的 argv 結構，而不是 shell command string。
3. 若確實需要 shell 模式，改成顯式 `--allow-shell` 或 `--shell-server`，並在預設模式拒絕 metacharacters。
4. 為這個腳本新增負面測試：
   - `npm run dev && echo MARKER`
   - `python server.py; echo MARKER`
   - `$(echo MARKER)`

Suggested fix direction:

- 使用 JSON array 或重複參數來描述 server command，例如「command + args + cwd」，不要把整串 shell 指令直接交給 `Popen(...)`

### SEC-002A Critical: `rollback-skills.ps1` 的 `$Id` 可導致破壞性路徑跳脫

Impact: 若 `$Id` 未驗證，腳本可能把 `Remove-Item -Recurse -Force` 套用到 repo 外非預期目錄，而且目前刪除前沒有 backup，屬於不可逆資料損失風險。

Evidence:

- `local/scripts/rollback-skills.ps1:22-23`
- `local/scripts/rollback-skills.ps1:39-43`

Why it matters:

- `$Id` 直接串接到 `registry\skills\` 後面
- 刪除動作發生在 restore 前，且沒有保護當前目標內容
- 這是目前 repo 內最容易形成「路徑穿越 + 強制遞迴刪除」組合的腳本

Recommended response:

1. 先對 `$Id` 加最小安全修補：
   - non-empty
   - trim 後不可為空
   - 僅允許 `[a-z0-9-]`
   - 長度限制
2. 再補上 post-resolve boundary check，確認 target 仍在 `registry/skills` 之下。
3. 在刪除既有 target 前新增 backup。
4. 明確拒絕 symlink target 或先偵測再停止。

### SEC-002B High: `batch-adopt-skills.ps1` 缺少 source / target confinement

Impact: 若 `Ids` 或 `Destination` 被不可信輸入影響，可能把內容複製到 repo 外或覆寫非預期位置。

Evidence:

- `local/scripts/batch-adopt-skills.ps1:10-13`
- `local/scripts/batch-adopt-skills.ps1:20-39`

Why it matters:

- `$Ids` 直接參與 `Join-Path`
- `$Destination` 沒有限定在 `registry/skills`
- 腳本包含覆蓋與刪除現有目標的流程

Recommended response:

1. 驗證 `$Ids` 為合法 skill identifier。
2. 對最終 `$dst` 做 resolve 後 boundary check。
3. 對 `$Destination` 明確限制在 allowlist 位置。
4. 補上 symlink 偵測，避免 `Copy-Item` 跟隨外部連結。

### SEC-002C Medium: `export-template-package.ps1` 的輸出位置過於寬鬆

Impact: 目前主要風險在於輸出目錄可被導向絕對路徑，但 source 清單是硬編碼的，因此風險低於破壞性腳本。

Evidence:

- `local/scripts/export-template-package.ps1:11-13`
- `local/scripts/export-template-package.ps1:68-88`

Why it matters:

- `OutputRoot` 可直接接受絕對路徑
- `Name` 目前直接變成目錄名，未檢查 `..`、絕對路徑、UNC path、Windows reserved names、ADS `:`

Recommended response:

1. 對輸出型參數只允許：
   - repo-relative path
   - 或明確 allowlist 下的子目錄，例如 `ops/template-package`、`ops/review-package`
2. 對 `Name` 類參數強制：
   - non-empty
   - trim 後不可為空
   - 僅允許 `[a-z0-9-]`
   - 拒絕 `..`, `/`, `\`, `:`
   - 拒絕 Windows reserved names

### SEC-002D Low-Medium: `export-review-package.ps1` 也應補 path validation，但風險較低

Impact: 主要仍是輸出位置與 package name 邊界，而不是 source traversal。

Evidence:

- `local/scripts/export-review-package.ps1:11-12`
- `local/scripts/export-review-package.ps1:95-115`

Why it matters:

- package source 清單是硬編碼的
- 腳本會先 join 到 repo root，再產生 package
- 風險主要來自命名與輸出位置控制，不像 rollback / batch-adopt 那樣帶有高破壞性

Recommended response:

1. 和 template export 共用同一套 path helper。
2. 限制 package name 與 output root。
3. 順手修正 manifest 中暴露本機路徑的欄位策略。

Suggested fix direction:

- 建一個 PowerShell helper，例如 `Resolve-RepoPathSafe` / `Test-RepoRelativeName`
- 先套在 `rollback` / `batch-adopt`，再擴到 `export-*`

### SEC-003 Medium: `bootstrap.py` 可被外部 `--repo-root` 重新導向成本機配置注入點

Impact: 若 `--repo-root` 可被不可信輸入控制，腳本可把本機 Codex config 與 project `.mcp.json` 改寫成指向外部 repo 的 MCP server。

Evidence:

- `local/scripts/bootstrap.py:129`
- `local/scripts/bootstrap.py:141-145`
- `local/scripts/bootstrap.py:178-204`

Why it matters:

- 這不是單純的路徑整潔問題，而是設定注入問題
- 目前腳本接受任意 `--repo-root`，只要該目錄底下存在 `registry/skills` 與 `registry/mcp/claude-project-mcp-seed/server.py`，就會被視為合法來源
- 之後腳本會更新：
  - `~/.codex/config.toml`
  - repo `.mcp.json`
- 但同時也已有兩層緩解：
  - 非 dry-run 必須明確 `--force`
  - 目標 repo 至少需要通過基本結構檢查

Recommended response:

1. 預設只允許腳本所在 repo root。
2. 若真的要支援外部 repo，改成明確 `--allow-external-repo-root`，且只能在 `--force` 下啟用。
3. 在 summary 中記錄 repo identity，例如：
   - git root
   - current HEAD
   - expected marker files
4. 在寫入前印出更明確的 target summary，讓 operator 能看出是否被導向到錯的 repo。

Suggested fix direction:

- `repo = Path(args.repo_root).resolve()` 後，若不是 `get_repo_root()`，預設直接拒絕，除非顯式啟用 external mode

### SEC-004 Medium: frontmatter 驗證可被 duplicate keys、Unicode 混淆與 size bombs 繞過或拖慢

Impact: 目前不太像直接 RCE，但會造成 skill 驗證、索引與 adoption 判斷不一致，並為未來 automation 留下模糊輸入面。

Evidence:

- `registry/skills/skill-creator/scripts/quick_validate.py:22-39`
- `registry/skills/skill-creator/scripts/quick_validate.py:59-84`
- `local/scripts/scan-skills.ps1:9-20`

Why it matters:

- `yaml.safe_load(...)` 可避免危險 object construction，但不會自動替你處理 duplicate keys policy
- `scan-skills.ps1` 目前只是用 regex 抽 `name` / `description`，不是嚴格 parser
- 目前也沒有：
  - frontmatter size limit
  - whole file size limit
  - Unicode normalization
  - invisible character rejection
  - folder name 與 `frontmatter.name` 一致性檢查

Recommended response:

1. 對 `SKILL.md` 建立 strict validation policy：
   - frontmatter 最大大小
   - description 最大大小
   - duplicate keys reject
   - Unicode normalize to NFC
   - reject zero-width / bidi override / NBSP 類字元
2. `scan-skills.ps1` 不要再當成準權威 parser；若要做 readiness gate，應改呼叫同一份嚴格 validator。
3. 明定 folder name 與 `frontmatter.name` 必須一致，且皆符合同一套 identifier policy。

## Additional Gaps Confirmed After Advisory Review

### GAP-001 High: PowerShell 路徑腳本尚未處理 symlink 攻擊面

Impact: `Copy-Item` / `Remove-Item` 對 symlink 的處理如果未明確控制，可能把操作延伸到 repo 外目標。

Evidence:

- `local/scripts/batch-adopt-skills.ps1:35-39`
- `local/scripts/rollback-skills.ps1:39-43`

Recommended response:

1. 在破壞性腳本中先顯式偵測 symlink / junction。
2. 一旦目標或來源為 symlink，預設停止並要求人工處理。
3. 把 symlink payload 納入 regression test。

### GAP-002 Medium: `bootstrap.py -> .mcp.json -> server.py` 是一條完整設定注入鏈

Impact: 單看 `bootstrap.py` 是設定注入；連同 `.mcp.json` 與 `server.py --root` 來看，這形成可持續的錯誤信任鏈。

Evidence:

- `local/scripts/bootstrap.py:196-204`
- `.mcp.json`
- `registry/mcp/claude-project-mcp-seed/server.py:177-182`

Recommended response:

1. `bootstrap.py` 加 repo identity 驗證。
2. `.mcp.json` 在 verify 階段顯示更明確的 root。
3. `server.py` 對 `--root` 補 marker 檢查或與 bootstrap 相同的 repo identity guard。

### GAP-003 High: `rollback-skills.ps1` 目前 restore 前刪除目標但不備份

Impact: 即使沒有 traversal，這也是高風險的不可逆操作。

Evidence:

- `local/scripts/rollback-skills.ps1:39-43`

Recommended response:

1. 刪除目標前先寫 backup。
2. 把 backup 納入 rollback summary / ops history。
3. 對 `--dry-run` 顯示清楚的 delete plan。

## Items Reviewed But Not Immediate Problems

### SAFE-001 MCP `read_registry_file(path)` 目前已有合理 confinement

Evidence:

- `registry/mcp/claude-project-mcp-seed/server.py:29-38`
- `registry/mcp/claude-project-mcp-seed/server.py:135-149`

Assessment:

- 目前流程先 `resolve()`
- 再檢查是否仍在 repo root 下
- 並限制只能讀：
  - `registry/**`
  - top-level core docs allowlist

Conclusion:

- checklist 中的 `../README.md`、`registry/../../.git/config`、絕對路徑等 payload 仍值得保留為 regression tests
- 但這條線目前不是最急的修補點

### SAFE-002 以 argument list 執行的 `subprocess.run(...)` 不是這輪重點

Evidence:

- `local/scripts/create-git-bundle.py:11-19`
- `local/scripts/create-git-bundle.py:73-77`

Assessment:

- 這些呼叫使用 argv list，而不是 shell string
- 沒有看到與 checklist 中 shell metacharacter 直接相乘的高風險模式

## Priority Plan

### P0-A

- 修掉 `with_server.py` 的 `shell=True`

### P0-B

- 先為 `rollback-skills.ps1` 加 `$Id` 驗證與 backup-before-delete

### P1

- 建立統一的 path validation / confinement helper
- 先套用到 `batch-adopt-skills.ps1`
- 再套用到 `export-template-package.ps1` / `export-review-package.ps1`

### P2

- 強化 `SKILL.md` frontmatter strict validation
- 讓 `scan-skills.ps1` 和 `quick_validate.py` 使用一致判定邏輯

### P3

- 限制 `bootstrap.py --repo-root` 的外部重導能力
- 補上 repo identity 驗證

### Parallel

- 把 checklist 中已確認有效的 payload 轉成 regression test matrix，並隨每一批修補同步補測

## Proposed Deliverables

若要進入修補階段，建議拆成四批：

1. `command execution hardening`
   - `with_server.py`
2. `destructive path safety hardening`
   - `rollback-skills.ps1`
   - `batch-adopt-skills.ps1`
3. `output path safety hardening`
   - `export-template-package.ps1`
   - `export-review-package.ps1`
4. `configuration + metadata hardening`
   - `bootstrap.py`
   - `quick_validate.py`
   - `scan-skills.ps1`

## Final Assessment

真正需要處理的項目不是全部 checklist，而是那些已經對到目前實作輸入面的部分。

以目前 UniText 狀態來看，最值得先修的是：

1. `shell=True`
2. `rollback-skills.ps1` 的 destructive path risk
3. `batch-adopt` / `export-*` 的 path confinement
4. `frontmatter` validator inconsistency
5. `bootstrap -> .mcp.json -> server.py` 的設定注入鏈

這幾項修掉之後，這份 checklist 才會從「理論攻擊面列表」變成「已納入工程防線」。
