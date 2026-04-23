# UniText — No-Publish Policy

> 상태: Active
> 용도: 어떤 내용이 명시적 허가 없이 push, upload, posting 되면 안 되는지 정의합니다.

## 1. Core Rule

사용자가 명시적으로 허가하지 않는 한, 다음 내용은 어떤 네트워크 서비스에도 외부 전송, 업로드, 게시, 동기화할 수 없습니다.

- GitHub push
- 소셜 플랫폼 게시물
- 클라우드 문서
- paste service
- 기타 third-party API 또는 hosting service

## 2. Default Sensitive Content

다음 내용은 기본적으로 비공개 대상으로 간주합니다.

- 소셜 게시물 초안
- 다른 프로젝트와의 비교 또는 협업 논의
- review notes
- strategy / roadmap / planning 문서
- 아직 공식 발표되지 않은 설계 방향

## 3. Permission Standard

게시가 가능하려면 다음 조건이 충족되어야 합니다.

- 사용자가 명확히 게시 가능하다고 밝혀야 함
- 일부만 허가한 경우, 허가된 부분만 게시 가능
- `private repo`는 자동 게시 허가가 아님

## 4. Agent Rule

이 repo에서 작동하는 모든 agent는 다음을 따라야 합니다.

1. 명시적 허가 없이 `git push` 금지
2. 명시적 허가 없이 내용을 소셜 채널이나 외부 서비스에 게시 금지
3. 사용자가 remote 생성이나 private repo 생성만 허가한 경우, 그것이 다른 민감 내용 업로드 허가를 의미한다고 추정하지 말 것
4. 다른 프로젝트 관계, 전략 논의, 소셜 문구가 포함되면 더 보수적으로 처리할 것

## 5. Current Explicitly Sensitive Topics

현재 특히 조심해야 할 내용은 다음과 같습니다.

- social post drafts
- `docs/concepts/SKILL0_COLLABORATION_VISION.md`
- `skill-0` 또는 외부 리뷰와 관련된 다른 전략 논의

## 6. Operational Interpretation

향후 게시가 필요하면 다음 세 단계로 진행합니다.

1. 먼저 허용 범위를 확인합니다.
2. 그다음 허용 목적지를 확인합니다.
3. 마지막에만 push / upload / posting을 실행합니다.
