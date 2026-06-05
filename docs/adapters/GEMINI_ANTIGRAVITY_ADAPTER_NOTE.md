# UniText — Gemini / Antigravity Adapter Note

> Status: transition note
> Last verified: 2026-06-04
> Primary source: Google Developers Blog, "An important update: Transitioning Gemini CLI to Antigravity CLI", published 2026-05-19: <https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/>.

Google announced that Antigravity CLI is the forward-looking CLI for consumer and free Gemini Code Assist paths. The same announcement says Gemini CLI and Gemini Code Assist IDE extensions stop serving requests for Google AI Pro, Ultra, and free individual paths on 2026-06-18. Enterprise or other managed access may differ, so this note should be reverified before making operational claims.

## Supported Surfaces

| UniText concept | Gemini / Antigravity-facing surface | Delivery mode |
|---|---|---|
| Project instructions | `GEMINI.md` or host-supported instruction surface | `pointer` or `native-config` |
| Shared skills | `.agents/skills` or host-specific skill path when supported | `symlink` or `mirror` |
| MCP definitions | host settings or documented MCP support | `native-config` |
| Runtime catalog | `runtime/catalog.json` | `pointer` |

## Transition Guidance

- Treat `Gemini CLI` references as compatibility notes, not evergreen primary guidance.
- Prefer `Gemini / Antigravity` wording in public docs until the local target is explicitly known.
- Add `Last verified` dates to Google ecosystem adapter claims.
- Do not promise request-serving behavior after 2026-06-18 without fresh official evidence.
- Keep `.agents/skills` guidance conditional on the host that is actually used.

## Recommended Flow

1. Start from [RUNTIME.md](../../RUNTIME.md).
2. Rebuild runtime projections with `python local/scripts/build-runtime-layer.py`.
3. Choose pointer, symlink, mirror, or native-config based on the verified local host.
4. Verify host-specific behavior before documenting support status.

## Constraints

- Do not write local Gemini or Antigravity settings from shared docs.
- Do not claim full migration completion from a docs-only change.
- Keep transition notes free of private account, subscription, or workspace details.

## Verification

Before changing this note, re-check official Google documentation or announcements and update `Last verified`.
