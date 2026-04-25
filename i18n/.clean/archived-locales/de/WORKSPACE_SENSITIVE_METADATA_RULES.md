[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](../zh-TW/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [简体中文](../zh-CN/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [日本語](../ja/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Deutsch](WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Français](../fr/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Español](../es/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [한국어](../ko/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Italiano](../it/WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> Status: Active Baseline
> Zweck: Definiert die Erkennungsregeln, Wartungsregeln und Prüfgrenzen für workspace-sensitive metadata auf shared surfaces.

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` ist die gemeinsame Regelquelle für das authoring repo und das exported starter package. Sie soll folgende Drift-Arten reduzieren:

- shared docs enthalten lokale absolute Pfade
- shared scripts enthalten live workspace hostnames
- shared governance files enthalten live redirect URIs oder Cloudflare IDs
- boundary verify und template verify verwenden unterschiedliche Regelsätze

Dieses Dokument beantwortet:

- was die einzelnen Bereiche der Regeldatei bedeuten
- wann neue Regeln ergänzt werden sollen
- wie verhindert wird, dass sanitized placeholders als live metadata fehlklassifiziert werden
- welche Prüfungen nach Regeländerungen ausgeführt werden müssen

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` enthält derzeit vier Top-Level-Bereiche:

- `shared_surface_scope`
  - definiert die tracked shared surfaces, die repo-side boundary verify standardmäßig prüft
- `path_rules`
  - definiert, welche tracked paths selbst nicht in shared surfaces auftauchen dürfen
- `content_patterns`
  - definiert, welche Textinhalte als workspace-sensitive metadata gelten
- `self_test_cases`
  - definiert eingebaute positive und negative Fälle, damit Regex-Änderungen keine stillen Regressionen einführen

## 3. Maintenance Rules

- Wenn ein neues shared governance doc oder shared control script hinzugefügt wird und es zur repo-side boundary review gehört, muss es auch in `shared_surface_scope` aufgenommen werden
- Wenn ein neuer live metadata Typ hinzukommt, zuerst `content_patterns`, dann passende `self_test_cases` ergänzen
- Wenn ein Placeholder als sicheres Beispiel gelten soll, muss ein self-test case mit `expected_labels = []` ergänzt werden
- Wenn eine Regex nur innerhalb eines Scripts als Regelzeichenkette erscheint, muss `skip_script_pattern_lines` explizit gesetzt werden
- authoring-only oder operations-only paths dürfen nicht in `shared_surface_scope` gepackt werden, nur um Fehlalarme zu unterdrücken; zuerst die Platzierung des Dokuments prüfen

## 4. Required Validation

Nach jeder Änderung an `WORKSPACE_SENSITIVE_METADATA_RULES.json` sollten mindestens folgende Prüfungen erneut ausgeführt werden:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Wenn die Änderung die starter baseline beeinflusst, zusätzlich:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

Das Ziel dieser Regeln ist:

- stabile, wartbare und prüfbare heuristic controls auf shared surfaces bereitzustellen

Sie sind nicht:

- ein vollständiger Schema-Validator für alle Secret-Typen
- ein generisches DLP-System für alle Infrastructure Provider
- ein Tool für Vollscans in local-only / ops-only Bereichen

Wenn die Zahl der metadata Typen weiter wächst, ist der nächste Schritt die Erweiterung der Regelquelle und der Testfälle, nicht das Zurücklegen von live references in die shared registry.
