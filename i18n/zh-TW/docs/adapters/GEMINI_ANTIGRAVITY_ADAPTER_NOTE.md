# UniText — Gemini / Antigravity Adapter Note

> 狀態：transition note
> Last verified: 2026-06-04
> Primary source: Google Developers Blog, "An important update: Transitioning Gemini CLI to Antigravity CLI", published 2026-05-19: <https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/>.

Google 已宣布 Antigravity CLI 是 consumer 與 free Gemini Code Assist paths 的 forward-looking CLI。同一公告也說 Gemini CLI 與 Gemini Code Assist IDE extensions 會在 2026-06-18 對 Google AI Pro、Ultra、以及 free individual paths 停止 serving requests。Enterprise 或其他 managed access 可能不同，因此 operational claims 前應重新 verify。

## Supported Surfaces

| UniText concept | Gemini / Antigravity-facing surface | Delivery mode |
|---|---|---|
| Project instructions | `GEMINI.md` or host-supported instruction surface | `pointer` or `native-config` |
| Shared skills | `.agents/skills` or host-specific skill path when supported | `symlink` or `mirror` |
| MCP definitions | host settings or documented MCP support | `native-config` |
| Runtime catalog | `runtime/catalog.json` | `pointer` |

## Transition Guidance

- 將 `Gemini CLI` references 視為 compatibility notes，不當作 evergreen primary guidance。
- Public docs 優先使用 `Gemini / Antigravity` wording，直到 local target 明確。
- Google ecosystem adapter claims 要帶 `Last verified` dates。
- 沒有 fresh official evidence 時，不承諾 2026-06-18 後的 request-serving behavior。
- `.agents/skills` guidance 應依實際 host 條件化。

## Constraints

- 不從 shared docs 寫入 local Gemini 或 Antigravity settings。
- Docs-only change 不聲稱 migration completed。
- Transition notes 不包含 private account、subscription 或 workspace details。
