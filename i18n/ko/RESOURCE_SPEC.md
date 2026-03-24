# UniText — Resource Spec

> 상태: Template Base
> 적용 범위: 단일 운영체제, 디렉터리 구조, 저장 형식에 묶이지 않는 shared resources의 논리 계약.

이 spec은 모든 핵심 metadata가 AI와 사람이 함께 읽고 비교하고 버전 관리할 수 있도록 순수 텍스트로 안정적으로 표현될 수 있어야 한다는 전제를 둡니다.

## 1. Scope

이 spec은 다음에 적용됩니다.

- `skills`
- `mcp`
- `agents`
- `workflow`

다음에는 적용되지 않습니다.

- operations state artifacts
- 플랫폼 특정 경로 매핑
- adapter 내부 실행 세부사항

## 2. Identity Rules

shared resource의 주 식별은 다음의 조합으로 구성됩니다.

- `type`
- `id`

`id`는 다음을 따라야 합니다.

- 소문자 영문자, 숫자, `-` 사용
- 공백 없음
- OS 특정 구분자 없음

## 3. Canonical Location

`canonical_location`은 어떤 머신의 절대 경로가 아니라 logical canonical path여야 합니다.

예:

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

허용되는 `status` 값은 다음과 같습니다.

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Defaults

- `source_of_truth`가 없으면 `canonical_location`과 동일한 것으로 간주
- `supported_clis`가 없으면 `undocumented`로 간주
- `delivery_guidance`가 없으면 adapter / operations 문서에서 유추

## 7. Delivery Guidance

`delivery_guidance`는 discovery를 위한 힌트이지 고정된 delivery mode가 아닙니다.

다음 내용을 설명할 수 있습니다.

- 어떤 adapter를 봐야 하는가
- 플랫폼 차이가 있는가
- `OPERATIONS.md`를 확인해야 하는가

다음은 적어서는 안 됩니다.

- 플랫폼 절대 경로
- 영구적으로 고정된 delivery mode

## 8. Conflict Rules

동일한 `(type, id)`에 내용이 다른 후보 리소스가 여러 개 발견되면:

- 자동으로 덮어쓰지 말 것
- 조용히 canonical source를 가정하지 말 것
- 반드시 `REVIEW / DRY-RUN`에서 멈출 것

허용되는 결과:

- canonical source를 명확히 선택
- 다른 `id`로 재명명
- `deprecated` 또는 `archived`로 표시
- 임시로 `draft` 유지

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
