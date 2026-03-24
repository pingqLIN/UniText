# UniText — Paquete de Revisión Externa

> Estado: Active Baseline  
> Uso: definir qué debe revisarse, qué no debe revisarse y cómo generar el review package de forma repetible.

## 1. Propósito

`UniText` ya entró en una fase de baseline apta para revisión externa, pero la revisión debe centrarse en:

- si la arquitectura central es razonable
- si el canonical registry ya está aterrizado
- si el modelo de seguridad de operations se puede ejecutar
- si los shared resources seleccionados representan bien la dirección del proyecto

El objetivo de este documento es condensar eso en un paquete de revisión reproducible, no entregar el workspace completo del autor tal cual.

## 2. Orden de Lectura Recomendado

Se recomienda a los revisores externos leer en este orden:

1. `EXTERNAL_REVIEW_COVER_NOTE.md`
2. `EXTERNAL_REVIEW_HIGHLIGHTS.md`
3. `README.md`
4. `INDEX.md`
5. `VISION.md`
6. `RESOURCE_SPEC.md`
7. `OPERATIONS.md`
8. `SECRET_HANDLING_GUIDELINES.md`
9. `MILESTONES.md`
10. `PROJECT_STATUS_REPORT_2026-03-23.md`
11. `ESSENTIAL_SKILLS_SHORTLIST.md`

Si se quieren ver muestras reales de recursos, mirar después:

- el conjunto curado `8 + 4` de `registry/skills/`
- `registry/agents/registry-curator/`
- `registry/mcp/claude-project-mcp-seed/`
- `registry/workflow/claude-plans/`
- los scripts mínimos de gobernanza y los scripts cross-platform de first-run en `local/scripts/`

## 3. Alcance de la Revisión

El review package debe incluir:

- Documentos centrales
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `PROJECT_MODES.md`
  - `MILESTONES.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`
  - `ESSENTIAL_SKILLS_SHORTLIST.md`
  - `EXTERNAL_REVIEW_PACKAGE.md`
- Archivos mínimos de gobernanza
  - `local/docs/ADOPTION_CHECKLIST.md`
  - `local/docs/CLI_COMPAT_MATRIX.md`
  - `local/scripts/README.md`
- Scripts mínimos de gobernanza
  - `bootstrap.py`
  - `verify-bootstrap.py`
  - `create-git-bundle.py`
  - `scan-skills.ps1`
  - `sync-skills.ps1`
  - `verify-delivery.ps1`
  - `health-check.ps1`
  - `batch-adopt-skills.ps1`
  - `generate-index-entries.ps1`
  - `rollback-skills.ps1`
  - `export-review-package.ps1`
- Shared resources seleccionados
  - el conjunto `8 + 4` de `registry/skills/`
  - `registry/agents/registry-curator/`
  - `registry/mcp/claude-project-mcp-seed/`
  - `registry/workflow/claude-plans/`

## 4. Fuera de Alcance

Los siguientes contenidos no deben formar parte del sujeto principal de la revisión:

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- mapeos de ruta locales y restos de entorno personal
- skills candidatos no incluidos en la shortlist
- contenido no rastreado o experimental

authoring notes and review archives pertenece a material de referencia del autor, no a la fuente canónica de revisión.

## 5. Comando de Exportación

En la raíz del repo, ejecutar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1
```

La salida por defecto va a:

```text
ops/review-package/review_YYYYMMDD_HHMMSS/
```

Si sólo se quiere revisar el contenido sin escribir archivos:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-review-package.ps1 -DryRun
```

## 6. Validación

Antes de exportar, conviene ejecutar al menos una vez:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Para confirmar el alineamiento del delivery canónico de skills:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-delivery.ps1
```

## 7. Interpretación Actual

Hasta 2026-03-24, `UniText` ya tiene:

- cover note y highlights para revisores
- documentos centrales aptos para revisión externa
- conjunto curado `8 + 4` de skills
- seed de agente / workflow y un baseline MCP ejecutable
- un proceso repetible para generar review package
- `bootstrap -> verify` multiplataforma
- backup portable en `git bundle`

Por tanto, la posición más adecuada es:

**external-review-ready baseline**

y no:

**fully generalized release template**

