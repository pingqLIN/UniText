# UniText — Essential Skills Shortlist

> 状態：Active
> 用途：現在の外部審査主集を定義する。全量候補ではなく、`8 + 4` の精選 skills のみを残す。

## Selection Rule

この shortlist は「必須 skill」を主題にし、次の基準で選定します。

- プロジェクト横断で使える
- shared registry の実際の価値を示せる
- 外部審査者が用途を理解しやすい
- scripts、references、examples を備えた複雑または入口型 skill を優先する

## Core 8

| Skill | Why It Stays |
|---|---|
| `pdf` | 汎用性が高く、複雑度も高い。複数の scripts と reference docs を含む |
| `docx` | 汎用性が高く、複雑度も高い。OOXML tooling と schema assets を含む |
| `xlsx` | 汎用性が高く、構造化データと spreadsheet workflow を代表する |
| `pptx` | office artifact 類型を補完し、scripts と example assets を含む |
| `mcp-builder` | UniText の位置づけに最も近く、明確な入口型 / platform 型 skill |
| `skill-creator` | skill エコシステムの拡張を直接支援する入口型 skill |
| `webapp-testing` | 検証可能で対話的な QA / browser workflow を代表する |
| `doc-coauthoring` | structured writing / spec workflow の類型を補完する |

## Expansion 4

| Skill | Why It Stays |
|---|---|
| `frontend-design` | UI / frontend output 類型の代表として残す |
| `web-artifacts-builder` | heavier な artifact / app composition 類型を補完する |
| `internal-comms` | 内部協業と status reporting に実用的な skill として残す |
| `theme-factory` | styling / theming 類型を残し、artifact 出力層の補完に適している |

## Complex / Entry-Type Check

この `8 + 4` だけで十分であり、追加の新しい類型を増やす必要はありません。すでに複数の複雑または入口型 skill が含まれているからです。

- `pdf`
- `docx`
- `pptx`
- `mcp-builder`
- `skill-creator`
- `webapp-testing`

これらの skill は少なくとも 1 つ以上を備えています。

- 内部 scripts
- reference docs
- template / example assets

## Out Of Scope For This Review Wave

以下の類型は、現時点では外部審査主集に含めません。

- Hugging Face 専用技能群
- art / brand / GIF 系の縦割り技能
- そのほか高い専門性を持つが必須ではない技能

それらに価値がないわけではありません。ただし、現時点でのテーマである「必須 skill」には含めない、ということです。
