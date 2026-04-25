# UniText — Secret Handling Guidelines

> 상태: Active
> 용도: password, API key, token, credential 및 기타 민감 정보의 처리 경계를 정의합니다.

## 1. Core Principle

어떤 secret도 템플릿, 샘플, review package, 외부 공유 문서로 취급될 수 있는 일반 문서 안에 들어가서는 안 됩니다.

## 2. What Counts as Secret

다음은 모두 secret 또는 민감 정보로 간주합니다.

- password
- API key
- token
- session cookie
- private key
- bearer token
- 신원을 확인하거나 접근 권한을 부여하는 데 직접 사용할 수 있는 모든 값

## 3. Storage Rules

- 실제 secret은 사용자 로컬 또는 통제된 key system에만 보관
- 문서에는 시연용 placeholder만 사용
- placeholder는 mock / example / redacted라고 명확히 표시
- repository에 직접 사용할 수 있는 실제 credential을 남기지 말 것

## 4. Documentation Rules

문서는 다음을 설명할 수 있습니다.

- secret이 어떤 종류의 위치에 저장되어야 하는가
- 어떤 도구가 secret을 읽는가
- 로컬 환경에서 secret을 어떻게 불러오는가
- redaction과 rotation을 어떻게 수행하는가

문서는 다음을 포함하면 안 됩니다.

- 실제 값
- 직접 재사용 가능한 token
- 개인 계정 비밀번호
- 외부에서 쓸 수 있는 API key

## 5. Template Boundary

`UniText`가 starter template을 내보낼 때는:

- `SECRET_HANDLING_GUIDELINES.md`는 유지 가능
- 실제 secret은 모두 제거
- 예시는 placeholder만 사용
- 모든 path와 account 정보는 비식별화

## 6. Review Boundary

내용이 external review package에 들어가면:

- governance logic과 boundary만 보여줄 것
- 실제 secret 값은 포함하지 말 것
- 단지 review용이라는 이유로도 민감 정보를 남기지 말 것

## 7. Operational Checklist

제출, push, export, 공유 전에 다음을 확인합니다.

1. 실제 credential이 포함되어 있는가
2. placeholder가 placeholder임을 충분히 표시했는가
3. log, snapshot, example에 비밀 조각이 남아 있지 않은가
4. redaction이 필요한가
5. package에서 제외해야 하는가
