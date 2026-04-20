# UniText — Hitos

> Estado: Active
> Propósito: definir condiciones cuantificables de finalización que sirvan tanto para revisión externa como para ejecución interna.

## Fase 1 — Skills Registry Online

- `registry/skills/` ya existe
- al menos 5 skills han completado su canonical adoption
- `INDEX.md` tiene entradas de catálogo correspondientes
- `local/scripts/sync-skills.ps1` apunta a `registry/skills`
- `local/scripts/verify-delivery.ps1` puede verificar el estado source/target de skills
- `local/scripts/health-check.ps1` puede pasar las comprobaciones básicas

## Fase 2 — Full Registry Baseline

- `registry/agents/` ya existe
- `registry/mcp/` tiene al menos 1 ejemplo no vacío y legible
- `registry/workflow/` tiene al menos 1 entrada de catálogo listada formalmente
- las operaciones `scan` / `verify` / `sync` tienen soporte mínimo de herramientas
- `CLI_COMPAT_MATRIX.md` registra el comportamiento de las CLIs y la última fecha de verificación

## Fase 3 — External Review Ready

- el Git repository ya está inicializado
- `.gitignore` excluye artefactos históricos grandes y material local-only
- `README.md`, `INDEX.md` y `docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md` están alineados
- `EXTERNAL_REVIEW_PACKAGE.md` define el alcance de revisión, el orden de lectura y los elementos excluidos
- `EXTERNAL_REVIEW_COVER_NOTE.md` y `EXTERNAL_REVIEW_HIGHLIGHTS.md` pueden usarse como entry docs para revisores
- `SECRET_HANDLING_GUIDELINES.md` ya define el límite de gobernanza y está en el orden de lectura central
- `local/scripts/export-review-package.ps1` puede generar el review package de forma repetible
- ya existe una ruta cross-platform `bootstrap -> verify` para first-run
- la revisión externa puede ver directamente:
  - documentos centrales de arquitectura
  - skills canónicos ya adoptados
  - scripts de operations mínimos
  - una señal clara de los hitos siguientes

## Fase 4 — Template Release Ready

- los artefactos local-only no entran en el paquete de publicación
- el flujo de exportación del template está documentado
- `TEMPLATE_RELEASE_PACKAGE.md` y `TEMPLATE_RELEASE_CHECKLIST.md` existen
- `local/scripts/export-template-package.ps1` puede generar un starter package de forma repetible
- `local/scripts/verify-template-package.ps1` puede verificar la estructura del starter package
- `SECRET_HANDLING_GUIDELINES.md` está incluido en el starter package
- `local/scripts/create-git-bundle.py` puede producir un backup portable
- ya existen generic examples seguros para template que cubren `skills`, `mcp`, `agents` y `workflow`
- ya existe un skeleton `local/` seguro para template
- `mcp` tiene al menos un baseline realmente ejecutable
- la cobertura de canonical resources sigue expandiéndose a `skills`, `mcp`, `agents` y `workflow`
- al menos 2 CLIs han pasado realmente la verificación de delivery
