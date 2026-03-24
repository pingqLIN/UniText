# CLI Compatibility Matrix

> 状態：Working Draft
> 最終更新：2026-03-23

| CLI | バージョン基準 | UniText 依存行為 | 現在状態 | 最終検証 |
|---|---|---|---|---|
| Claude Code | 2.1.63 | `~/.claude/skills` を読み、project `.mcp.json` をサポートする | delivery path verified | 2026-03-24 |
| Codex CLI | 0.106.0 | `config.toml` の `skills_path` から skills を読み、`[mcp_servers.unitext_registry]` を登録できる | bootstrap verified | 2026-03-24 |
| Gemini CLI | 0.31.0 | `~/.gemini/skills` と `~/.agents/skills` を読み込む | delivery path verified | 2026-03-24 |
| GitHub CLI | 2.87.3 | workflow は参照用途のみで、native skills はサポートしない | 知られている制約 | 2026-03-02 |
| VS Code | 1.109.5 | 直接の resource consumer ではなく、主に authoring environment として使う | 知られている制約 | 2026-03-02 |
| Windsurf | 1.108.2 | 直接の resource consumer ではなく、主に authoring environment として使う | 知られている制約 | 2026-03-02 |

## Notes

- この matrix は UniText が現在依存している CLI の挙動を記録するもので、各 CLI の完全な能力を列挙するものではありません。
- major version が変わるたびに、skills と mcp delivery を少なくとも 1 回は再検証するべきです。
- `delivery path verified` は、`verify-delivery.ps1` により canonical skills path の整合が確認済みであることを意味し、end-to-end の相互操作検証完了を意味するわけではありません。
