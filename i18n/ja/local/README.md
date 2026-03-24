# Local Overlay

このディレクトリは **本機 deployment、scripts、path 対照、その他の非核心 overlay** を収めます。

設計目的はとてもシンプルです。

- 本機設定で root のコア概念を汚染しない
- 本機の修編を集中的に管理できるようにする
- 必要なら `local/` 全体をそのまま削除して再構築できるようにする

## Contents

- `docs/`
  - 本機 deployment に関する説明と対照文書
- `scripts/`
  - 本機実行用 scripts

## Current Files

- [docs/authoring](../../../local/docs/authoring)
  - 再編前に残されている authoring 強化版のコア文書
- [docs/MCP_DEPLOYMENT_NOTES.md](docs/MCP_DEPLOYMENT_NOTES.md)
  - 現在の本機 MCP deployment と接続方法の説明
- [docs/PATH_MAP.md](docs/PATH_MAP.md)
  - 現在の deployment における path 参照と歴史的対照
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - 現在の本機 workflow 接続の説明
- [scripts/sync-skills.ps1](../../../local/scripts/sync-skills.ps1)
  - 本機同期 script

## Rule

もしある内容が次のどちらを説明しているかで判断します。

- この system がどう動くべきか
  - それは `local/` に置くべきではない
- この instance が今どう構成されているか
  - それは `local/` に置くべきである
