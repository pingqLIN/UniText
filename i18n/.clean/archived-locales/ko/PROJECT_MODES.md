# UniText — Project Modes

> 상태: Template Base
> 목적: authoring repo와 외부 제공용 starter/template를 구분합니다.

## 1. Two Modes

### Local Development Project

작성자 본인이 계속 개발, 관리, 수정, 통제하는 용도입니다.

포함될 수 있는 항목:

- inventories
- backups
- drift logs
- migration artifacts
- platform-specific notes

### Project Template

다른 사람이 자신의 `UniText` 인스턴스를 시작할 수 있도록 제공하는 용도입니다.

포함해야 하는 항목:

- logical contracts
- 핵심 문서
- 최소 예시
- 플랫폼에 독립적인 규칙

포함하면 안 되는 항목:

- 로컬 절대 경로
- 개인 사용 흔적
- backup snapshot
- drift history
- 단일 배포 전용 기본값

## 2. Rule Of Thumb

어떤 내용이 다음을 설명한다면:

- `UniText가 어떻게 동작해야 하는가`
  - `Project Template`에 더 적합
- `어떤 author workspace가 지금 어떻게 설정되어 있는가`
  - `Local Development Project`에 더 적합

## 3. Publishing Rule

템플릿을 게시할 때는 다음 순서를 따릅니다.

1. 핵심 문서와 template-safe examples를 유지
2. local-only state artifacts 제거
3. 로컬 path / 계정 / 머신 특정 값 제거
4. reference implementation을 추상적 examples로 바꾸기
