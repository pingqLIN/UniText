# UniText — 邊界事件審查模板

> 狀態：Active Baseline
> 用途：將 shared / local / ops / publish 邊界漂移事件整理成可重複 review 的紀錄格式。

## 1. Incident Summary

- Date:
- Title:
- Reported by:
- Scope:

## 2. What Crossed The Boundary

- Artifact:
- From:
- To:
- Why this was a boundary violation:

## 3. Why It Was Plausible

- Which part looked structurally reasonable:
- Which rule was missing, implicit, or easy to misread:
- Was this a content mistake, placement mistake, or both:

## 4. Impact

- Shared surface affected:
- Local workspace sensitivity affected:
- Export / rebuild / publish implications:
- Was a secret involved:

## 5. Existing Detection Layers

| Layer | Should it have caught this | Did it catch this | Notes |
|---|---|---|---|
| authoring judgment |  |  |  |
| document placement rule |  |  |  |
| `.gitignore` / path policy |  |  |  |
| tracked-file boundary verify |  |  |  |
| export verify |  |  |  |
| publishability review |  |  |  |

## 6. Root Cause

- Primary cause:
- Secondary cause:
- Why the current controls were insufficient:

## 7. Permanent Prevention

- Doc change:
- Ignore rule change:
- Verify script change:
- Export rule change:
- Review checklist change:

## 8. Validation

- What to rerun:
- What should now fail if the incident is reintroduced:
- What should remain unaffected:

## 9. Follow-Up

- Owner:
- Priority:
- Next review date:
