# UniText — Index

> 상태: Template Base
> 역할: 모든 human / AI의 첫 읽기 지점으로, discovery에 사용합니다.

`UniText`는 순수 텍스트를 공유 인터페이스로 삼아, 다양한 CLI 간의 일관된 호환성과 AI-first discovery를 강조합니다.

## 1. Core Docs

권장 읽기 순서:

1. `INDEX.md`
2. `VISION.md`
3. `RESOURCE_SPEC.md`
4. `OPERATIONS.md`
5. `PROJECT_MODES.md`
6. `MILESTONES.md`
7. `EXTERNAL_REVIEW_PACKAGE.md`
8. `EXTERNAL_REVIEW_COVER_NOTE.md`
9. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
10. `TEMPLATE_RELEASE_PACKAGE.md`
11. `TEMPLATE_RELEASE_CHECKLIST.md`
12. `SECRET_HANDLING_GUIDELINES.md`
13. `NO_PUBLISH_POLICY.md`
14. `SKILL0_COLLABORATION_VISION.md`

## 2. Resource Catalog

현재 registry는 다음 shared resource types를 다룹니다.

| Type | Logical root | Purpose |
|---|---|---|
| `skills` | `/registry/skills` | 여러 CLI가 함께 쓸 수 있는 skill 정의 |
| `mcp` | `/registry/mcp` | canonical MCP definitions |
| `agents` | `/registry/agents` | 공용 agent 지침과 persona 정의 |
| `workflow` | `/registry/workflow` | 공용 flow, runbook, planning guidance |

다음은 shared resource type이 아닙니다.

| Area | Logical root | Role |
|---|---|---|
| `operations state` | `/operations` | inventories, backups, drift logs, history records |

## 3. Starter Catalog Shape

최소 catalog entry는 다음을 포함해야 합니다.

- `id`
- `type`
- `canonical_location`
- `status`

추가로 권장되는 항목:

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

필드 규칙 전체는 `RESOURCE_SPEC.md`를 보세요.

## 4. Current Catalog Entries

### Review Shortlist

현재 외부 리뷰 주력 집합은 [ESSENTIAL_SKILLS_SHORTLIST.md](ESSENTIAL_SKILLS_SHORTLIST.md)의 `8 + 4` 핵심 skills이며, 전체 후보군이 아닙니다.

### Review Package

외부 리뷰용 자료를 정리하려면 [EXTERNAL_REVIEW_PACKAGE.md](EXTERNAL_REVIEW_PACKAGE.md)를 시작점으로 삼고, `local/scripts/export-review-package.ps1`로 재생성 가능한 review package를 만드세요.

리뷰어에게 바로 보여줄 가장 짧은 입구는 다음입니다.

- [EXTERNAL_REVIEW_COVER_NOTE.md](EXTERNAL_REVIEW_COVER_NOTE.md)
- [EXTERNAL_REVIEW_HIGHLIGHTS.md](EXTERNAL_REVIEW_HIGHLIGHTS.md)

### Template Release

깨끗한 starter package로 정리하려면 [TEMPLATE_RELEASE_PACKAGE.md](TEMPLATE_RELEASE_PACKAGE.md)를 보고 `local/scripts/export-template-package.ps1`를 사용하세요.

내보낸 starter package를 검증하려면 `local/scripts/verify-template-package.ps1`를 사용하세요.

새 머신에서 첫 번째 initialize → verify를 완료하려면 우선 다음을 사용합니다.

- `local/scripts/bootstrap.py`
- `local/scripts/verify-bootstrap.py`

### Related Concept Notes

`UniText`와 `skill-0`의 협업 방식을 평가하려면 [SKILL0_COLLABORATION_VISION.md](SKILL0_COLLABORATION_VISION.md)를 보세요.

### Skills

| `id` | Tier | `canonical_location` | `status` |
|---|---|---|---|
| `pdf` | Core 8 | `/registry/skills/pdf` | `active` |
| `docx` | Core 8 | `/registry/skills/docx` | `active` |
| `xlsx` | Core 8 | `/registry/skills/xlsx` | `active` |
| `pptx` | Core 8 | `/registry/skills/pptx` | `active` |
| `mcp-builder` | Core 8 | `/registry/skills/mcp-builder` | `active` |
| `skill-creator` | Core 8 | `/registry/skills/skill-creator` | `active` |
| `webapp-testing` | Core 8 | `/registry/skills/webapp-testing` | `active` |
| `doc-coauthoring` | Core 8 | `/registry/skills/doc-coauthoring` | `active` |
| `frontend-design` | Expansion 4 | `/registry/skills/frontend-design` | `active` |
| `web-artifacts-builder` | Expansion 4 | `/registry/skills/web-artifacts-builder` | `active` |
| `internal-comms` | Expansion 4 | `/registry/skills/internal-comms` | `active` |
| `theme-factory` | Expansion 4 | `/registry/skills/theme-factory` | `active` |

### Workflow

| Field | Value |
|---|---|
| `id` | `claude-plans` |
| `type` | `workflow` |
| `canonical_location` | `/registry/workflow/claude-plans` |
| `status` | `draft` |
| `source_of_truth` | `/registry/workflow/claude-plans` |
| `supported_clis` | `claude` |
| `delivery_guidance` | CLI 능력에 따라 workflow adapter 또는 project-local plan mapping을 사용합니다. |

### MCP

| Field | Value |
|---|---|
| `id` | `claude-project-mcp-seed` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/claude-project-mcp-seed` |
| `status` | `active-baseline` |
| `source_of_truth` | `/registry/mcp/claude-project-mcp-seed/definition.json` |
| `supported_clis` | `claude, codex` |
| `delivery_guidance` | Bootstrap이 project `.mcp.json`과 Codex native-config를 써서 bundled read-only MCP server를 가리키도록 합니다. |

### Agents

| Field | Value |
|---|---|
| `id` | `registry-curator` |
| `type` | `agents` |
| `canonical_location` | `/registry/agents/registry-curator` |
| `status` | `active` |
| `source_of_truth` | `/registry/agents/registry-curator/AGENT.md` |
| `supported_clis` | `claude, codex, gemini` |
| `delivery_guidance` | review와 adoption 작업에 공용 persona로 사용할 수 있으며, 실제 wiring은 CLI 능력에 따라 다릅니다. |

## 5. Example Catalog Entries

### Example: Skill

| Field | Value |
|---|---|
| `id` | `example-skill` |
| `type` | `skills` |
| `canonical_location` | `/registry/skills/example-skill` |
| `status` | `draft` |
| `source_of_truth` | `/registry/skills/example-skill/SKILL.md` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | skills adapter를 사용합니다. 실제 해석 방식은 CLI 능력과 로컬 환경에 따라 달라집니다. |

### Example: MCP Definition

| Field | Value |
|---|---|
| `id` | `example-mcp` |
| `type` | `mcp` |
| `canonical_location` | `/registry/mcp/example-mcp` |
| `status` | `draft` |
| `source_of_truth` | `/registry/mcp/example-mcp/definition` |
| `supported_clis` | `undocumented` |
| `delivery_guidance` | MCP adapter로 등록하며, 최종 delivery mode는 CLI 능력과 로컬 환경에 따라 달라집니다. |

## 6. Discovery Rules

`INDEX.md`가 답하는 것은 다음입니다.

- 여기에는 어떤 리소스가 있는가
- 각 리소스의 논리적 위치는 어디인가
- 어떤 규격 또는 운영 문서를 먼저 봐야 하는가

`INDEX.md`가 직접 답하지 않는 것은 다음입니다.

- 특정 플랫폼의 절대 경로
- 최종적으로 해석된 delivery mode
- 특정 author workspace의 로컬 설정

## 7. How To Use This Baseline

### For Humans

1. 먼저 `VISION.md`를 읽습니다.
2. `INDEX.md`로 starter catalog를 만듭니다.
3. `RESOURCE_SPEC.md`로 리소스 필드를 정의합니다.
4. `OPERATIONS.md`로 플랫폼과 CLI 연결 방식을 정의합니다.

### For AI Agents

1. 먼저 `INDEX.md`를 discovery entry로 봅니다.
2. schema가 필요하면 `RESOURCE_SPEC.md`를 봅니다.
3. delivery 또는 mutation이 필요하면 `OPERATIONS.md`를 봅니다.
4. 어떤 단일 배포 경로도 규격의 진실로 취급하지 않습니다.
