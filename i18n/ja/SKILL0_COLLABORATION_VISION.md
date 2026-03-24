# UniText × skill-0 — Collaboration Vision

> 状態：Concept Draft
> 目的：`UniText` と `skill-0` の関係、協業空間、取り得る経路、そして現在欠けている機構を定義する。

## 1. Executive Summary

`UniText` と `skill-0` は互いに排他的でも重複でもなく、上下流関係を作れる 2 つの層です。

- `UniText` は shared resources の **registry / delivery / governance** を担当する
- `skill-0` は高階 skill を吸収し、分解し、正規化して、より通用性の高い **atomic operation set** にする

したがって、最も合理的な協業の形は「どちらがどちらを置き換えるか」ではありません。

**UniText は canonical inputs と治理可能な受け皿を提供し、skill-0 は decomposition / normalization / recomposition 能力を提供する。**

## 2. Each Project Solves a Different Problem

### UniText

`UniText` が解くのは次の問題です。

- shared resource をどう canonical 化するか
- 複数の AI CLI 間でどう delivery するか
- `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY` で変更をどう管理するか

つまり、

**distribution / governance problem**

### skill-0

`skill-0` が解くのは次の問題です。

- ある高階 skill が実際にはどの最小操作単位で構成されるか
- どの step が再利用可能な primitive か
- どの説明が surface wording で、どれが core operation か
- 高階 skill を、より小さく、より一般的で、より移植しやすい能力集合に再構成できるか

つまり、

**abstraction / compiler / normalization problem**

## 3. Relationship Between the Two

`skill-0` の目標から見ると、`UniText` の最も価値ある役割は「配布される結果」ではなく、次のようなものです。

- 安定した high-level skill source
- 論理 identity と metadata を備えた canonical corpus
- 継続的に分析、比較、追跡できる skills data set

この観点では、両者の関係は次のように表せます。

| Project | Primary role |
|---|---|
| `UniText` | shared resources の canonical source of truth |
| `skill-0` | high-level skills に対する analyzer / decomposer / compiler |

一言で言えば、

**UniText は skill を保存し、skill-0 は skill を解体する。**

## 4. Current Collaboration Space

`UniText` の core schema をまだ変更しなくても、すでに協業空間はあります。

### 4.1 Use UniText as input corpus

`skill-0` は次を入力として直接使えます。

- `registry/skills/*/SKILL.md`
- `INDEX.md` の catalog metadata
- `RESOURCE_SPEC.md` が与える identity / canonical location 契約

これにより、`skill-0` が分析するのは散らばった副本ではなく、より整理された canonical skill corpus になります。

### 4.2 Use UniText as a governed staging ground

`skill-0` の分析出力は、今のところ canonical registry に戻さず、次のような場所に置けます。

- `/operations`
- 例えば `ops/analysis/skill-0/`

こうすると次の利点があります。

- shared resource schema を早まって汚さない
- 分析形式が安定しているか先に観察できる
- `skill-0` を analysis pipeline として扱い、いきなり canonical source に昇格させずに済む

### 4.3 Use UniText review flow to evaluate derived outputs

`skill-0` が次のような出力を作ったとき。

- atom maps
- normalized step sets
- shared subroutine clusters
- recomposition candidates

それらは `UniText` の review mindset に従って検査できます。

- identity は安定しているか
- naming は明確か
- 元の skill への対映は追跡できるか
- canonical form は人間が決める必要があるか

## 5. Most Likely Collaboration Modes

### Mode A — skill-0 as external analyzer

`skill-0` は `UniText` を data source とし、analysis report を出力するが、registry には書き戻さない。

適した用途：

- decomposition method の高速検証
- skill overlap analysis
- reusable primitives の発見

利点：

- 導入コストが最小
- `UniText` schema をほとんど変えなくてよい

欠点：

- 結果が sidecar artifacts にとどまる
- shared canonical resource になりにくい

### Mode B — skill-0 as sidecar generator

`skill-0` が `registry/skills` を読み、機械可読な sidecar を隣接生成する。

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

利点：

- skill と atom の明確な対映を作れる
- 純粋な report より tooling に乗せやすい

欠点：

- `UniText` schema の境界問題に触れ始める
- どれが canonical で、どれが generated かを定義する必要がある

### Mode C — primitives become a first-class resource type

協業が成熟したら、`UniText` に正式な資源型を追加できます。

- `/registry/primitives`
- または `/registry/operations`

こうすれば `skill-0` の出力は分析の付属物ではなく、registry に正式に管理される shared resources になります。

利点：

- 真の共通語彙層ができる
- cross-skill recomposition を支えられる

欠点：

- `UniText` の resource model を変える必要がある
- 新しい metadata spec、adoption flow、verification rules が必要になる

## 6. What Is Missing Today

現在、両者が自然に深く統合できない最大の理由は、次の機構がまだ欠けているからです。

### 6.1 Missing canonical type for primitives

`UniText` の現在の一級 resource type は次の 4 つです。

- `skills`
- `mcp`
- `agents`
- `workflow`

まだ次はありません。

- `primitives`
- `operations`
- `atoms`

したがって、`skill-0` が最も重視する産物を受け止める第一級の器が、まだ `UniText` にありません。

### 6.2 Missing metadata spec for atomic units

今の `RESOURCE_SPEC.md` は高階 shared resources を記述するのに適していますが、次はまだ定義していません。

- atom id
- operation signature
- preconditions / postconditions
- composition rules
- provenance back to source skill

### 6.3 Missing adoption flow for derived artifacts

`UniText` には skills adoption flow はありますが、次のようなケースを扱う専用フローはまだありません。

- 同じ skill から異なる atom set が分解される
- 複数の skill が似ているが完全には同じでない primitive に対応する
- ある atom が canonicalize するほど安定しているかを判断する

### 6.4 Missing verification model

`skill-0` の出力をより正式な協業段階に進めるには、少なくとも次に答える必要があります。

- decomposition は安定しているか
- round-trip recomposition は可能か
- cross-skill reuse を本当に高めているか
- 単に既存 description を言い換えているだけではないか

### 6.5 Missing boundary between analysis and canon

まだ次の境界規則が必要です。

- どの `skill-0` 産物が analysis だけなのか
- どの産物が canonical shared resource と見なせるのか

この境界が不明瞭なうちは、最も安全なのは `ops/analysis/skill-0/` に置くことです。

## 7. Recommended Near-Term Direction

短期的に最も合理的なのは、`UniText` の core schema をすぐ変更するのではなく、次のように段階的に進めることです。

**Mode A -> Mode B の漸進的協業**

### Phase A — Analysis Only

まず次を行います。

- `registry/skills/*/SKILL.md` を入力にする
- decomposition report を出力する
- `ops/analysis/skill-0/` に保存する

この段階の目標は canonicalize ではなく、次を検証することです。

- atom extraction は安定しているか
- skill overlap は本当に観察できるか
- どの primitive を残す価値があるか

### Phase B — Stable Sidecars

形式が安定してきたら、次を導入します。

- sidecar schemas
- naming rules
- source-skill linkage
- basic verification

この時点でも、まだ resource type を増やさずに、次の関係を作れます。

- `skill -> atoms`
- `atom -> source skills`

### Phase C — First-Class Primitives

analysis が価値を示したら、次のいずれかを `UniText` に正式導入することを検討します。

- `/registry/primitives`
- `/registry/operations`

その時点で初めて、次の文書を正式に更新する必要があります。

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Concrete First Deliverables

両プロジェクトを動かし始める最初の成果物として、最も価値が高いのは次の 4 つです。

1. `skill-0` の analysis output draft schema を定義する
2. `UniText` の `Core 8` skills から 1〜2 個を選び、decomposition sample を作る
3. 出力を `ops/analysis/skill-0/` に置く
4. 次を比較する
   - 異なる skills 間で共有される atom
   - skill 文面と atom 層の間の差
   - 最小 workflow として逆再構成できるか

## 9. Strategic Interpretation

協業が成功した場合、長期的な役割分担は明快になります。

- `UniText` は shared AI resources の canonical hub になる
- `skill-0` は skill normalization と primitive extraction engine になる

system の層で見ると、次のようになります。

| Layer | Project |
|---|---|
| Canonical resource governance | `UniText` |
| Skill decomposition / normalization | `skill-0` |
| Future primitive vocabulary layer | `UniText × skill-0` の共同成果 |

## 10. Final Position

現在の最も正確な結論は次の通りです。

**`UniText` と `skill-0` は高い関連性を持つが、重複建設ではない。**

一方は治理と配布、もう一方は分解と抽象化を担当します。

したがって、短期的に最も合理的な協業は、`skill-0` を `UniText` の既存 4 類 resource に直接押し込むことではありません。

**`skill-0` にまず `UniText` を canonical input corpus として扱わせ、その analysis 結果をまず `ops/analysis/skill-0/` に置く。**

出力形式、価値、検証方法が安定したら、その時点で primitive / operation 層を新しい canonical resource type として正式に昇格させるかどうかを決めればよいのです。
