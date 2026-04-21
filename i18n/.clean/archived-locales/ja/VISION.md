# UniText — 構想

> 状態：Template Base
> 原則：仕様の前提は、いかなる単一の OS、ディレクトリ構造、または展開方式にも置かない。論理契約を基準とする。

## 1. What UniText Is

`UniText` は text-native、registry-first、AI-first の shared resource hub です。複数の AI CLI / agent システムが、同じ純文本契約を用いて資源定義と採用方法を共有できるようにします。

それは 2 層から成ります。

1. `Registry`
   - shared resources、canonical identity、最小契約を定義する
2. `Adapter / Operations Control Plane`
   - registry 内容を各 CLI に接続し、install、sync、adopt、repair を扱う

## 2. Problem It Solves

`UniText` が解決するのは、ツールをまたいだ資源共有でよく起きる断片化です。

- skills が別々の場所に散らばる
- MCP 定義が異なる設定形式に分かれる
- agent instructions を共用できない
- workflow の慣例をツール間で引き継ぎにくい
- AI と人間が読みやすい純文本の共通インターフェースがない

## 3. Architecture Position

正式な位置づけは次の通りです。

**Registry-first, adapter-enabled, operations-governed**

重要な原則は以下です。

- registry がなければ、共通の source も共通の意味もない
- adapter がなければ、registry を各 CLI に実際に届けられない
- AI は重要な consumer であり collaborator だが、唯一の信頼できる統合機構ではない

## 4. Resource Types

デフォルトの shared resource types は次の通りです。

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state` は shared resource type ではありません。`/operations` に独立して置くべきです。

## 5. Discovery and Delivery

`INDEX.md` は discovery を担当し、次を答えます。

- どんな資源があるか
- 各資源の論理位置はどこか
- どの CLI がサポートされているか

`OPERATIONS.md` は delivery を担当し、次を答えます。

- ある CLI はどうやって資源を取得するか
- いつ install、sync、adopt、repair を実行するか
- delivery mode をどう解釈するか

利用可能な delivery mode は次の通りです。

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Delivery Triggers

delivery は明示的な trigger でのみ開始できます。

- `bootstrap`
- `sync`
- `adopt`
- `repair`

破壊的操作はすべて次の条件に従うべきです。

- まず dry-run
- まず backup
- canonical source を静かに決めてはいけない

## 7. Adoption Model

### Soft Adoption

- まず discovery を導入する
- 既存資源を直ちに移行することを強制しない

### Formal Adoption

正式な納管フローは次の通りです。

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

同名で内容が異なる資源が見つかった場合、フローは `REVIEW / DRY-RUN` で止めなければなりません。

## 8. Documentation Set

コア文書は次の通りです。

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Path Strategy

本文では次のような logical canonical paths を使います。

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

absolute path や platform-specific 設定は deployment mapping に属し、構想レイヤーの契約ではありません。

## 10. Design Principles

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. One-Sentence Positioning

> UniText は、明示的な adapter と operations control plane を通じて複数の AI CLI が同じ canonical resources を安全に発見・採用・共有できるようにする、text-native、registry-first、AI-first の shared resource hub である。
