# UniText — 公開禁止ポリシー

> 状態：Active
> 用途：どの内容を、ユーザーの明示的な許可なしに push・upload・posting してはいけないかを定義する。

## 1. Core Rule

ユーザーが明示的に許可しない限り、次の内容をいかなるネットワークサービスにも対外的に push、upload、posting、同期してはなりません。

- GitHub push
- SNS への投稿
- クラウド文書
- paste service
- その他あらゆる第三者 API または hosting service

## 2. Default Sensitive Content

以下の内容は、デフォルトで公開不可として扱います。

- social post draft
- 他プロジェクトとの比較や協業に関する議論
- review notes
- strategy / roadmap / planning 文書
- まだ正式に対外発表していない設計方針

## 3. Permission Standard

公開できる前提は次の通りです。

- ユーザーが明示的に公開可と示している
- 一部のみ許可された場合は、許可された部分だけを公開する
- `private repo` であることは、自動的に公開可を意味しない

## 4. Agent Rule

この repo で動作するすべての agent は、次を守ってください。

1. 明示的な許可なしに `git push` しない
2. 明示的な許可なしに内容を SNS や外部サービスへ貼り付けない
3. ユーザーが remote 作成や private repo 作成だけを許可した場合でも、それが他の機微内容の upload 許可を意味すると推定しない
4. 他プロジェクトとの関係、戦略議論、SNS 投稿文が含まれる場合は、より保守的な基準で扱う

## 5. Current Explicitly Sensitive Topics

現時点では、以下の種類の内容は特に慎重に扱うべきです。

- social post drafts
- `docs/concepts/SKILL0_COLLABORATION_VISION.md`
- `skill-0` または外部審査に関するその他の戦略的議論

## 6. Operational Interpretation

将来的に公開が必要な場合は、次の 3 段階に分けることを推奨します。

1. まず公開を許可する範囲を確認する
2. 次に公開先を確認する
3. 最後に push / upload / posting を実行する
