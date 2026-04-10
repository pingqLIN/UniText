[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](../zh-TW/DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](../zh-CN/DOCUMENT_PLACEMENT_POLICY.md) | [日本語](../ja/DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](DOCUMENT_PLACEMENT_POLICY.md) | [Français](../fr/DOCUMENT_PLACEMENT_POLICY.md) | [Español](../es/DOCUMENT_PLACEMENT_POLICY.md) | [한국어](../ko/DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](../it/DOCUMENT_PLACEMENT_POLICY.md)

# UniText — Richtlinie zur Dokumentplatzierung

> Status: Active Baseline
> Zweck: Definiert, in welcher Schicht Governance-, Referenz-, Authoring- und Operations-Dokumente liegen sollen, damit Shared Content und Live-Workspace-Inhalte nicht vermischt werden.

## 1. Purpose

UniText ist gleichzeitig:

- ein Authoring-Workspace
- eine Shared Registry Baseline
- eine Quelle für Template- und Rebuild-Exporte

Darum ist es leicht, Dokumente in die falsche Schicht zu legen, wenn man nur nach dem Thema urteilt.

Diese Richtlinie beantwortet:

- welche Dokumentarten in `registry/` gehören
- welche Dokumentarten in `local/` gehören
- welche Dokumentarten in `ops/` gehören
- welche Dokumente tracked sein dürfen
- welche Dokumente nur im ignorierten lokalen Authoring-Bereich bleiben dürfen

## 2. Core Rule

Für die Platzierung zählt zuerst die Natur des Inhalts, nicht das Themengebiet.

- Beschreibt ein Dokument shared canonical truth, gehört es in die shared layer
- Beschreibt ein Dokument den aktuellen Zustand eines einzelnen Authoring-Workspace, gehört es in die local layer
- Beschreibt ein Dokument Operations-Historie, Exportergebnisse, Audit-Evidence oder generated state, gehört es in die operations layer

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| Architekturprinzipien, Governance-Regeln, template-safe Specs | Root-Dokumente oder `registry/` | Yes | Yes | darf keine live workspace values enthalten |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | Feldstruktur ist erlaubt, Werte müssen redacted oder placeholder sein |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | darf nicht an einen einzelnen Rechner gebunden sein |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | location / state ist okay, plaintext secrets nicht |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | muss ignoriert werden |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | muss ignoriert werden |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | muss ignoriert werden |
| generated audit trail / export output / drift report | `ops/` | No | No | ist State, keine canonical source |

## 4. Naming Rules

Wenn ein Thema sowohl eine shared als auch eine live Variante braucht, verwende standardmäßig ein Paar:

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - oder `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

Wenn shared sanitized doc und live workspace doc gleichzeitig existieren, gilt:

1. Die shared Variante enthält nur template-safe Struktur und redacted placeholder
2. Die live Variante bleibt nur unter `local/docs/` oder `local/docs/authoring/`
3. Die shared Variante soll auf den Ort der live Variante verweisen
4. Die live Variante soll ebenfalls auf die zugehörige shared sanitized reference verweisen

## 6. Publishing Rule

Diese Aussagen sind nicht dasselbe:

- template export passes
- rebuild export passes
- branch is publish-safe

Ein sauberer Template- oder Rebuild-Export bedeutet nur, dass das Export-Artefakt saubere Grenzen hat. Es bedeutet nicht, dass sämtlicher tracked content im Authoring-Repo push-sicher ist.

## 7. Quick Decisions

Wenn du unsicher bist, wohin ein Dokument gehört, stelle zuerst diese drei Fragen:

1. Beschreibt das Dokument, wie ein einzelner Authoring-Workspace aktuell aussieht?
   - Ja: zuerst `local/docs/` prüfen
2. Ist das Dokument ein Operationsergebnis, ein Audit-Artefakt, ein Exportpaket oder ein Drift-Report?
   - Ja: zuerst `ops/` prüfen
3. Soll das Dokument künftig sicher aus template / rebuild / shared registry referenziert werden können?
   - Ja: zuerst Root-Dokumente, `registry/` oder die shared workflow layer prüfen

## 8. Common Misplacements

- eine live Cloudflare baseline in `registry/.../references/` ablegen
- strategy / review plan im Root ablegen
- export output oder audit evidence als canonical reference behandeln
- machine-specific paths direkt in shared governance docs schreiben

## 9. Review Gate

Bevor ein neues Governance- oder Referenzdokument hinzugefügt wird, prüfe mindestens:

- beschreibt es shared truth statt live workspace state
- bleibt es auch nach einem Push im Rahmen von `NO_PUBLISH_POLICY.md` und template-safe Erwartungen
- braucht es ein sanitized/live pair statt beide Rollen in einer Datei zu mischen

## 10. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
