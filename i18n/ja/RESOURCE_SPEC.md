# UniText — Resource Spec

> 状態：Template Base
> 適用範囲：shared resources の論理契約。単一 OS、ディレクトリ構造、保存形式には依存しない。

この spec では、すべての核心 metadata が純文本で安定して保持できることを前提とします。これにより、AI と人間が共同で読み、比較し、バージョン管理しやすくなります。

## 1. Scope

この spec が適用されるのは次の通りです。

- `skills`
- `mcp`
- `agents`
- `workflow`

適用されないのは次の通りです。

- operations state artifacts
- platform-specific path mapping
- adapter の内部実行詳細

## 2. Identity Rules

shared resource の主識別は次の組み合わせで構成されます。

- `type`
- `id`

`id` は次を満たすべきです。

- 小文字の英字、数字、`-` を使う
- 空白を含まない
- OS 特有の区切り文字を含まない

## 3. Canonical Location

`canonical_location` は、機械ごとの絶対パスではなく、論理 canonical path でなければなりません。

例：

- `/registry/skills/example-skill`
- `/registry/mcp/example-mcp`
- `/registry/agents/example-agent`

## 4. Metadata Tiers

### Required

- `id`
- `type`
- `canonical_location`
- `status`

### Recommended

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

### Optional

- `owner`
- `provenance`
- `notes`
- `last_verified`

## 5. Lifecycle

許可される `status` は次の通りです。

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Defaults

- `source_of_truth` が省略された場合は、`canonical_location` と同一と見なす
- `supported_clis` が省略された場合は、`undocumented` と見なす
- `delivery_guidance` が省略された場合は、adapter / operations 文書から推論する

## 7. Delivery Guidance

`delivery_guidance` は discovery 用のヒントであり、固定の delivery mode ではありません。

次のようなことを説明できます。

- どの adapter を確認すべきか
- platform 差が存在するか
- `OPERATIONS.md` を確認すべきか

次のようなことは書き込むべきではありません。

- platform absolute path
- 永久固定の delivery mode

## 8. Conflict Rules

同じ `(type, id)` に対して内容の異なる複数候補が見つかった場合。

- 自動上書きしてはいけない
- canonical source を静かに推定してはいけない
- `REVIEW / DRY-RUN` で止めなければならない

許される結果は次の通りです。

- canonical source を明示的に選ぶ
- 別の `id` に再命名する
- `deprecated` または `archived` にする
- 一時的に `draft` のまま維持する

## 9. Example

```yaml
id: example-skill
type: skills
canonical_location: /registry/skills/example-skill
status: draft
source_of_truth: /registry/skills/example-skill/SKILL.md
supported_clis: undocumented
delivery_guidance: Use the skills adapter; resolved mode depends on CLI capabilities and local environment.
```
