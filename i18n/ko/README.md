[English](../../README.md) | [繁體中文](../zh-TW/README.md) | [简体中文](../zh-CN/README.md) | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [한국어](README.md) | [Italiano](../it/README.md)

# UniText

> **여러 AI CLI를 위한 text-native, registry-first 공유 리소스 허브.**
>
> Claude Code, Codex, Gemini CLI 같은 도구들이 동일한 텍스트 계약 위에서 리소스를 공유하도록 합니다.

> **동기화 नोट 2026-03-27:** 이 번역본은 current-baseline의 일부만 반영합니다. 영어 `README.md`가 authoritative version입니다. support, release boundary, review scope 같은 고위험 섹션은 맞춰 두었지만, 나머지는 이전 해석이 남아 있을 수 있습니다.

---

## Why This Exists

여러 AI CLI 도구를 함께 쓰면 리소스가 금방 흩어집니다.

- 같은 skill이 세 곳에 따로 정의되고 내용도 조금씩 다름
- MCP 서버 설정은 다른 도구가 읽지 못하는 형식으로 분산됨
- 어떤 agent 지침은 특정 CLI에서만 이해됨
- 어떤 복사본이 canonical인지 알 수 없음

UniText는 단일 shared registry와 관리된 delivery layer로 이 문제를 해결합니다. **하나의 정의, 모든 도구.**

---

## How It Works

```text
UniText/
├── registry/          ← canonical definitions (무엇이 존재하는가)
│   ├── skills/        ← shared skill definitions
│   ├── mcp/           ← MCP server definitions
│   ├── agents/        ← agent instructions & personas
│   └── workflow/      ← runbooks, plans, conventions
│
├── local/             ← deployment overlay (이 환경에서 어떻게 연결되는가)
│   ├── docs/          ← path maps, deployment notes
│   └── scripts/       ← 이 머신에서 쓰는 sync scripts
│
└── ops/               ← operations state (shared resources 아님)
    └── history/       ← timestamped audit trail
```

`registry/` 레이어는 platform-agnostic합니다. OS별 절대 경로가 아니라 논리적인 canonical path(``/registry/skills``, ``/registry/mcp``)를 사용합니다. `local/` 레이어는 이를 실제 머신 경로로 해석합니다.

---

## Architecture

**Registry-first, adapter-enabled, operations-governed.**

| Layer | Role |
|-------|------|
| **Registry** | 공유 리소스가 무엇인지와 canonical identity를 정의 |
| **Adapter** | registry 내용을 각 CLI에 전달 (mirror, symlink, native-config, pointer) |
| **Operations** | backup, dry-run, audit trail을 포함해 변경의 시점과 방식을 관리 |

### Resource Types

| Type | Logical Root | What Goes Here |
|------|-------------|----------------|
| `skills` | `/registry/skills` | AI agent가 공용으로 쓰는 skill 정의 |
| `mcp` | `/registry/mcp` | CLI 간 공유되는 MCP server 정의 |
| `agents` | `/registry/agents` | 공용 agent 지침, persona, system prompt |
| `workflow` | `/registry/workflow` | runbook, planning template, convention |

### Delivery Modes

각 리소스는 CLI 능력에 따라 다르게 전달될 수 있습니다.

- `pointer` - discovery only, 내용 복사 없음
- `mirror` - robocopy/rsync를 통한 로컬 복사
- `symlink` - canonical source로 향하는 고정 경로 링크
- `native-config` - CLI 자체 설정 형식에 등록

---

## Getting Started

### 1. 이 repository를 fork 또는 clone

```bash
git clone https://github.com/your-username/UniText.git
cd UniText
```

### 2. 첫 리소스 추가

`registry/skills/` 아래에 skill을 만듭니다.

```text
registry/skills/my-skill/
└── SKILL.md
```

최소 `SKILL.md`:

```yaml
---
name: my-skill
description: 이 skill이 하는 일을 한 줄로 설명
---

## Usage

AI agent를 위한 사용 지침...
```

### 3. catalog에 등록

`INDEX.md`에 entry를 추가합니다.

| Field | Value |
|-------|-------|
| `id` | `my-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/my-skill` |
| `status` | `active` |
| `supported_clis` | `claude, codex, gemini` |

### 4. 로컬 CLI wiring 초기화

우선 크로스 플랫폼 bootstrap 경로를 사용합니다.

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
```

`bootstrap.py`는 공유 skills target을 맞추고, Codex의 `skills_path`를 갱신하며, 번들된 MCP baseline을 위한 project-local `.mcp.json`을 작성합니다. `sync-skills.ps1`는 Windows PowerShell 참고 구현으로 남아 있습니다.

---

## Supported CLIs

| CLI | Delivery Mode | Notes |
|-----|--------------|-------|
| **Claude Code** | mirror / symlink | `~/.claude/skills` |
| **Gemini CLI** | mirror / symlink | `~/.gemini/skills` |
| **Codex** | native-config + project-local MCP | `skills_path`와 `~/.codex/config.toml`의 `[mcp_servers.*]` |
| **GitHub CLI** | native-config | `config.yml` |

전체 CLI 경로 표는 [template/examples/local/docs/PATH_MAP.template.md](template/examples/local/docs/PATH_MAP.template.md)를 보세요.

---

## Governance Rules

UniText는 **no silent changes** 정책을 사용합니다.

1. **명시적 trigger만 허용** - `bootstrap`, `sync`, `adopt`, `repair`
2. **변경 전에 항상 backup** - 파괴적 작업은 모두 `ops/`에 timestamped snapshot을 생성
3. **delivery 전 dry-run** - 실제 변경 전에 미리 확인
4. **충돌 시 중단** - 같은 리소스의 두 버전이 다르면 사람이 검토할 때까지 멈춤
5. **완전한 audit trail** - 모든 작업은 `ops/history/`에 기록

Formal adoption flow: `SCAN → REVIEW → DRY-RUN → ADOPT → DELIVER → VERIFY`

---

## Documentation

| File | Purpose |
|------|---------|
| [INDEX.md](INDEX.md) | Discovery entry point - 어떤 리소스가 있고 어디 있는지 |
| [VISION.md](VISION.md) | Architecture principles and design rationale |
| [RESOURCE_SPEC.md](RESOURCE_SPEC.md) | 모든 shared resources의 metadata contract |
| [OPERATIONS.md](OPERATIONS.md) | Delivery modes, triggers, safety rules |
| [PROJECT_MODES.md](PROJECT_MODES.md) | Authoring repo와 project template 구분 |
| [SECRET_HANDLING_GUIDELINES.md](SECRET_HANDLING_GUIDELINES.md) | Secret 저장, redaction, password/API key 경계 |
| [MILESTONES.md](MILESTONES.md) | 정량화된 phase 목표와 외부 리뷰 준비 체크포인트 |
| [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md) | 현재 review wave의 `8 + 4` 핵심 skills 집합 |
| [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md) | 리뷰어용 범위, 읽기 순서, 반복 가능한 package export 흐름 |
| [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md) | 외부 리뷰 제출용 note |
| [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md) | 빠른 이해를 위한 요약 |
| [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md) | template release cleanup의 범위, 제외 항목, export 흐름 |
| [TEMPLATE_RELEASE_CHECKLIST.md](TEMPLATE_RELEASE_CHECKLIST.md) | starter package 출시 전 정리 체크리스트 |
| [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md) | UniText와 skill-0가 어떻게 협업할 수 있는지에 대한 개념 노트 |
| [NO_PUBLISH_POLICY.md](NO_PUBLISH_POLICY.md) | agent와 협력자를 위한 local-first 게시 경계 |

읽기 순서: `EXTERNAL_REVIEW_COVER_NOTE.md` → `EXTERNAL_REVIEW_HIGHLIGHTS.md` → `INDEX.md` → `VISION.md` → `RESOURCE_SPEC.md` → `OPERATIONS.md` → `SECRET_HANDLING_GUIDELINES.md` → `NO_PUBLISH_POLICY.md` → `MILESTONES.md` → `EXTERNAL_REVIEW_PACKAGE.md` → `TEMPLATE_RELEASE_PACKAGE.md` → `SKILL0_COLLABORATION_VISION.md`

---

## Two Ways to Use This

### 스타터 템플릿으로 사용

이 repo를 fork합니다. 이 머신 전용 `ops/history/`, `backup/`, `local/` 경로를 제거합니다. `registry/`에 자신만의 skills와 MCP definitions를 넣습니다. `local/scripts/`를 환경에 맞게 조정합니다.

### 참고 구현체로 사용

핵심 문서를 읽어 아키텍처를 이해합니다. 그런 다음 registry 구조, resource spec, delivery modes, operations audit trail 패턴을 자신의 환경에 맞게 적용합니다.

---

## Design Principles

- **Registry first** - 먼저 정의하고, 그다음 delivery
- **Discovery before automation** - 동기화 전에 무엇이 있는지 먼저 파악
- **Platform-agnostic contracts** - spec은 논리 경로를 쓰고, local overlay만 절대 경로를 사용
- **Minimum viable metadata** - `id`, `type`, `canonical_location`, `status`로 시작 가능
- **Safe mutation** - dry-run + backup + explicit trigger를 항상 적용
- **AI as consumer** - 모델은 registry를 읽고 사용하지만, delivery 보증을 책임지지 않음

---

## Status

| Component | Status |
|-----------|--------|
| Core documentation | Stable |
| Registry structure | Active - `skills/`, `mcp/`, `workflow/`, `agents/` roots present |
| Skills registry | Active baseline - first canonical batch adopted, broader adoption still in progress |
| Agents registry | Active seed - `registry-curator` entry created |
| MCP registry | Active baseline - canonical definition plus runnable read-only server present |
| Workflow registry | Draft seed - workflow doc plus plan template present |
| Operations audit trail | Active |
| Sync, bootstrap, and review scripts | Active baseline in `local/scripts/` |
| External review package | Active baseline - reviewer guide and export script present |
| Template release cleanup | Release candidate - template package guide, checklist, export + verify scripts, generic examples, and local overlay skeleton present |

---

## License

MIT

---

*여러 AI 도구를 사용하면서 단일 진실 소스를 원한다면.*

