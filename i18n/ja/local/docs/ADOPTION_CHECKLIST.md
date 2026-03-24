# Adoption Review Checklist

> 状態：Active
> 用途：adoption flow の `REVIEW` step における最小検査基準を定義する。

## Required

- [ ] ディレクトリ名が `id` の規則に合っている
- [ ] `SKILL.md` が存在する
- [ ] `SKILL.md` が frontmatter から始まっている
- [ ] frontmatter に少なくとも `name` と `description` が含まれている
- [ ] `canonical_location` が `/registry/{type}/{id}` に合理的に対応している
- [ ] 明らかな破損、空白、途中で切れた内容がない

## Recommended

- [ ] `LICENSE.txt` または同等の license 説明がある
- [ ] 明確な Usage、Workflow、Process の段落がある
- [ ] 個人アカウントや本機 absolute path が hard-code されていない
- [ ] scripts / references を含む場合、その path 関係が明確で agent が発見できる

## Review Outcome

- `approve`
  - `DRY-RUN` にそのまま進める
- `needs-fix`
  - metadata の補完または内容整理が必要
- `hold`
  - canonical source に争いがある、または内容品質に問題があるため `ADOPT` に進めない
