[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](../zh-TW/DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](../zh-CN/DOCUMENT_PLACEMENT_POLICY.md) | [日本語](DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](../de/DOCUMENT_PLACEMENT_POLICY.md) | [Français](../fr/DOCUMENT_PLACEMENT_POLICY.md) | [Español](../es/DOCUMENT_PLACEMENT_POLICY.md) | [한국어](../ko/DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](../it/DOCUMENT_PLACEMENT_POLICY.md)

# UniText — ドキュメント配置ポリシー

> 状態：Active Baseline
> 用途：governance、reference、authoring、operations に属する文書をどの層に置くべきかを定義し、shared と live workspace の内容が混ざるのを防ぐ。

## 1. Purpose

UniText は同時に次の三つです。

- authoring workspace
- shared registry baseline
- template / rebuild export source

そのため、文書を「テーマが近いかどうか」だけで判断すると、簡単に誤った層へ置いてしまいます。

このルールが答えるのは次の点です。

- どの種類の文書を `registry/` に置くべきか
- どの種類の文書を `local/` に置くべきか
- どの種類の文書を `ops/` に置くべきか
- どの文書を tracked にできるか
- どの文書を ignored local authoring 空間にだけ残すべきか

## 2. Core Rule

文書の配置を判断するときは、テーマ分野よりも内容の性質を優先します。

- 文書が shared canonical truth を記述しているなら shared layer に置く
- 文書が単一の作者 workspace の現在状態を記述しているなら local layer に置く
- 文書が操作履歴、出力結果、audit evidence、generated state を記述しているなら operations layer に置く

どの「作業ウィンドウ」やどの authoring マシンでその文書を書いたかは、主判定ではありません。

- UniText authoring workspace 内で書かれたからといって、自動的に `local/docs/authoring/` になるわけではない
- tracked であることも、自動的に「公開可能」や「push 可能」を意味しない
- まずその文書が誰のためのもので、どの真実レイヤーを記述しているかを確認し、その後で配置先を決める

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| アーキテクチャ原則、governance ルール、template-safe spec | root docs または `registry/` | Yes | Yes | live workspace values を避ける必要がある |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | フィールド構造は書けるが、値は redacted または placeholder にする |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | 単一の作者マシンに結び付けてはいけない |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | location / state は記録できるが、plaintext secret は不可 |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | ignore 必須 |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | ignore 必須 |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | ignore 必須 |
| generated audit trail / export output / drift report | `ops/` | No | No | state であり canonical source ではない |

## 4. Naming Rules

あるトピックに shared 版と live 版の両方が必要な場合、既定では対になる命名を使います。

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - または `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

shared sanitized doc と live workspace doc が同時に存在する場合、次を守ります。

1. shared 版は template-safe な構造と redacted placeholder だけを残す
2. live 版は `local/docs/` または `local/docs/authoring/` にだけ置く
3. shared 版は live 版の位置を明示する
4. live 版も対応する shared sanitized reference を示す

## 6. Publishing Rule

次の表現は同じ意味ではありません。

- template export passes
- rebuild export passes
- branch is publish-safe

template / rebuild の export が安全でも、それは export 産物の境界が比較的きれいだという意味であり、authoring repo 内の tracked content がすべて push に適していることを意味しません。

## 7. Quick Decisions

文書をどこに置くべきか迷ったら、まず次の三つを確認します。

1. この文書は単一の作者 workspace が今どうなっているかを説明しているか
   - はい：まず `local/docs/` を検討する
2. この文書は操作結果、audit 産物、export package、または drift report か
   - はい：まず `ops/` を検討する
3. この文書は将来 template / rebuild / shared registry から安全に参照されることを期待しているか
   - はい：まず root docs、`registry/`、または shared workflow layer を検討する

## 8. Decision Ladder

より安定して判断したい場合は、次の順序で確認します。

1. これは generated state、audit evidence、drift report、または export output か
   - はい：`ops/` に置く
2. これは単一の authoring workspace、単一のマシン、または現在の live wiring を記述しているか
   - はい：`local/docs/` に置く
3. 単一 workspace を記述している場合、それは draft、review note、または authoring workboard か
   - はい：`local/docs/authoring/` に置く
4. 将来の shared readers が繰り返し参照するための canonical truth であり、template-safe であるべきか
   - はい：tracked shared layer に置く
5. tracked shared layer に置くなら、どの種類に近いか
   - repo-wide policy / spec：root docs に置く
   - sanitized reference：`registry/.../references/` に置く
   - shared workflow / runbook：`registry/workflow/` に置く
6. shared 版と live 版の両方が必要な場合
   - sanitized/live の pair を作り、2 つの境界を 1 つのファイルに混ぜない

まだ迷う場合は、次を使います。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\get-document-placement-recommendation.ps1 -Topic "cloudflare workflow" -CanonicalSharedTruth -SharedForm registry-reference
```

## 9. Common Misplacements

- live Cloudflare baseline を `registry/.../references/` に置く
- strategy / review plan を root に置く
- export output や audit evidence を canonical reference として扱う
- machine-specific path を shared governance docs に直接書く

## 10. Review Gate

新しい governance / reference 文書を追加する前に、少なくとも次を確認します。

- それは live workspace state ではなく shared truth を説明しているか
- push されたとしても `NO_PUBLISH_POLICY.md` と template-safe の期待に合うか
- 単一ファイルに両方を詰め込むのではなく sanitized/live の pair が必要ではないか

## 11. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
