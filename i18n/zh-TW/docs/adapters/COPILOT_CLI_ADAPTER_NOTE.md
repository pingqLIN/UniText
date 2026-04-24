# UniText — Copilot CLI Adapter Note

> 狀態：Active Baseline
> 範圍：定義第一個 repo-level `Copilot CLI` adapter baseline，同時避免誇大尚未完成的缺口。

## 1. Purpose

這份 note 記錄 `UniText` 與 `Copilot CLI` 目前的協作模型。

`Copilot CLI` 屬於 starter template 的目標基線，因為本專案目標是讓 shared resources 可被多種 LLM AI tools 共用，包括：

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`
- `Copilot CLI`
- `Windows`
- `macOS`
- `Linux`

同時，這份 note 不宣稱 `Copilot CLI` 已在所有平台 feature-complete，也不宣稱它以和其他 CLI 完全相同的方式消費 UniText。

## 2. Current Position

目前 repo baseline 是：

- `registry/` 是 shared resources 的 canonical source of truth
- `.mcp.json` 以 template-safe、relative-path seed 形式提供
- `.claude/settings.json` 作為 shared starter baseline 的一部分被追蹤
- `bootstrap.py -> verify-bootstrap.py` 是目前 cross-platform baseline 的建議 first-run path

對 `Copilot CLI` 而言，目前 repo-level baseline 是：

- 從 `AGENTS.md` 與相關文件讀取 repo instructions
- 透過 `~/.copilot/mcp-config.json` 使用同一個 shared `unitext-registry` MCP server
- 將 machine-specific wiring 留在 adapter/bootstrap layer，而不是放進 canonical files

## 3. Why An Adapter Note Exists

`Copilot CLI` 目前的狀態與 `Claude Code`、`Codex CLI`、`Gemini CLI` 不完全相同。

專案對下列工具已有較清楚的 first-run path：

- `Claude Code`
- `Codex CLI`
- `Gemini CLI`

repo 現在定義的第一個 adapter contract 具有以下特性：

- template-safe
- repo-level
- 已由目前 Windows authoring host 上的 `bootstrap.py -> verify-bootstrap.py` 驗證

此階段的驗證應按字面理解：

- `Windows / PC` 已有完整 authoring-host evidence
- `macOS` 與 `Linux` 仍是規劃中的驗證目標，不是已完成的支援宣稱

仍待釐清的是更廣泛的 cross-platform validation，以及 Copilot 是否需要 repo instructions 之外的 tool-specific skill surface。

這份 note 的用途是讓 template 可以誠實表達：

- `Copilot CLI` 在 scope 內
- 方向已定義
- 實作仍在推進中

## 4. Adapter Goals

未來的 `Copilot CLI` adapter 應滿足：

1. 從同一份 canonical registry 讀取，不引入另一個 source of truth。
2. 初始化步驟明確且可自動化。
3. 符合 template release boundary，不讓 local-only deployment assumptions 洩漏到 shared repo。
4. 提供可與 `bootstrap -> verify` 對應的驗證路徑。
5. 清楚區分目前已驗證與仍屬目標的部分。

## 5. Proposed Integration Path

目前保守的整合路徑是：

1. 保持 `registry/` 作為 single source of truth。
2. 以 `AGENTS.md` / related files 作為主要 instruction surface。
3. 使用 `bootstrap.py` 將 `unitext-registry` upsert 到 `~/.copilot/mcp-config.json`。
4. 在安裝 `Copilot CLI` 時，以 `verify-bootstrap.py` 確認預期的 `unitext-registry` command、args 與 config shape。

第一版實作回答的是：

- `Copilot CLI` 如何發現 project-local MCP definitions？
  - 透過 bootstrap 寫入的 `~/.copilot/mcp-config.json`
- `Copilot CLI` 如何發現 repo instructions？
  - 透過內建載入 `AGENTS.md` / related files
- 哪些屬於 tracked shared files，哪些屬於 local bootstrap output？
  - instructions 留在 shared；machine-local MCP wiring 留在 bootstrap output

## 6. Known Gaps

目前 repo 對 `Copilot CLI` 仍缺少：

- macOS validation evidence
- Linux validation evidence
- 是否需要 repo instructions 之外的 Copilot-specific skills surface 的長期規則
- 比目前 bootstrap evidence 更強的 compatibility status

因此目前 compatibility status 應解讀為：

`repo-level MCP baseline defined; broader platform verification still pending`

## 7. Non-Goals

這份 note 不會：

- 宣稱完整 cross-platform `Copilot CLI` support
- 在 tool-specific config format 穩定前凍結格式
- 為了滿足單一 CLI 而複製 `skills` content
- 將 canonical truth 從 `registry/` 移走

## 8. Recommended Next Step

下一個實際 milestone 是：

**在 macOS 與 Linux 重新驗證同一條 `Copilot CLI` bootstrap + verify path，然後再決定 compatibility matrix 是否可以從 baseline evidence 升級為 broader verified support**

只有完成後，才應把 compatibility matrix 或 template release checklist 升級為更強的 verified language。
