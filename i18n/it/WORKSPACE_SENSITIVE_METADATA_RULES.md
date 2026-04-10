[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](../zh-TW/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [简体中文](../zh-CN/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [日本語](../ja/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Deutsch](../de/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Français](../fr/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Español](../es/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [한국어](../ko/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Italiano](WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> Stato: Active Baseline
> Scopo: definire le regole di rilevamento, le regole di manutenzione e i confini di validazione delle workspace-sensitive metadata sulle shared surfaces.

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` è la fonte di regole condivisa tra l'authoring repo e l'exported starter package. Serve a ridurre i seguenti drift:

- shared docs che includono percorsi assoluti locali
- shared scripts che includono live workspace hostnames
- shared governance files che includono live redirect URI o Cloudflare IDs
- boundary verify e template verify che usano set di regole diversi

Questo documento spiega:

- cosa rappresenta ciascuna sezione del file di regole
- quando va aggiunta una nuova regola
- come evitare che un sanitized placeholder venga interpretato come live metadata
- quali validazioni devono essere rilanciate dopo una modifica alle regole

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` contiene attualmente quattro sezioni di primo livello:

- `shared_surface_scope`
  - definisce le tracked shared surfaces che repo-side boundary verify controlla di default
- `path_rules`
  - definisce quali tracked path non dovrebbero apparire nella shared surface
- `content_patterns`
  - definisce quali contenuti testuali sono considerati workspace-sensitive metadata
- `self_test_cases`
  - definisce casi positivi e negativi integrati per evitare regressioni silenziose dopo modifiche alle regex

## 3. Maintenance Rules

- quando si aggiunge un nuovo shared governance doc o shared control script e questo rientra nel repo-side boundary review, va aggiunto anche a `shared_surface_scope`
- quando compare un nuovo tipo di live metadata, prima si estende `content_patterns` e poi i relativi `self_test_cases`
- se un placeholder deve essere trattato come esempio sicuro, va aggiunto un self-test case con `expected_labels = []`
- se una regex compare in uno script solo come stringa di regola, bisogna impostare esplicitamente `skip_script_pattern_lines`
- non si devono inserire path authoring-only o operations-only in `shared_surface_scope` per nascondere falsi positivi; prima va verificato se il documento è collocato nel layer sbagliato

## 4. Required Validation

Dopo ogni modifica a `WORKSPACE_SENSITIVE_METADATA_RULES.json`, bisogna almeno rieseguire:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Se la modifica tocca anche la starter baseline, bisogna eseguire inoltre:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

L'obiettivo di questo set di regole è:

- fornire heuristic controls stabili, manutenibili e verificabili sulla shared surface

Non è:

- un validatore di schema completo per tutti i tipi di secret
- un sistema DLP generico per tutti gli infrastructure provider
- uno strumento per scansionare in modo completo le aree local-only / ops-only

Se in futuro i tipi di metadata continueranno ad aumentare, il passo successivo dovrà essere ampliare la fonte di regole e i casi di test, non riportare le live references nella shared registry.
