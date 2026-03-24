# Adoption Review Checklist

> 상태: Active
> 용도: adoption flow의 `REVIEW` 단계에서 사용하는 최소 검사 기준을 정의합니다.

## Required

- [ ] 디렉터리 이름이 `id` 규칙을 따른다
- [ ] `SKILL.md`가 존재한다
- [ ] `SKILL.md`가 frontmatter로 시작한다
- [ ] frontmatter에 최소 `name`과 `description`이 포함된다
- [ ] `canonical_location`이 `/registry/{type}/{id}`에 합리적으로 대응한다
- [ ] 명백한 손상, 공백, 잘린 내용이 없다

## Recommended

- [ ] `LICENSE.txt` 또는 동등한 license 설명이 있다
- [ ] 명확한 Usage, Workflow, Process 단락이 있다
- [ ] 개인 계정과 로컬 absolute path가 hard-code되어 있지 않다
- [ ] scripts / references를 포함한다면 path 관계가 명확하고 agent가 발견할 수 있다

## Review Outcome

- `approve`
  - `DRY-RUN`으로 바로 진행할 수 있다
- `needs-fix`
  - metadata 보완 또는 내용 정리가 필요하다
- `hold`
  - canonical source에 분쟁이 있거나 내용 품질 문제가 있어 `ADOPT`로 갈 수 없다
