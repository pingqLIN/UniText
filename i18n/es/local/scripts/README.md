# Local Scripts

Aquí van los **scripts de operación local**.

- `*.ps1` conserva implementaciones de referencia Windows-first
- `*.py` ofrece rutas cross-platform para bootstrap / verify / backup

## Current Scripts

- `bootstrap.py`
  - inicializa de forma cross-platform el delivery de skills, el native-config de Codex y el `.mcp.json` del proyecto
- `verify-bootstrap.py`
  - comprueba de forma cross-platform que el resultado del first-run coincide con el repo actual
- `create-git-bundle.py`
  - crea un backup portable en forma de `git bundle`, reduciendo el riesgo de depender sólo del working tree local
- `sync-skills.ps1`
  - sincroniza `registry/skills/` con los targets locales de skills
- `scan-skills.ps1`
  - escanea skills candidatos y produce el resultado de la revisión de adopción
- `verify-delivery.ps1`
  - verifica si la fuente y los targets comunes de skills existen, son enlaces y se pueden resolver
- `health-check.ps1`
  - realiza una comprobación mínima de salud del registry y de los scripts
- `batch-adopt-skills.ps1`
  - migra por lotes los skills candidatos a `registry/skills/`
- `generate-index-entries.ps1`
  - genera el bloque de catálogo que necesita `INDEX` a partir de `registry/skills/`
- `rollback-skills.ps1`
  - restaura un skill concreto desde backups de `ops/history/adopt_*`
- `export-review-package.ps1`
  - exporta a `ops/review-package/` el cover note, highlights, docs centrales, entradas seleccionadas del registry y scripts mínimos para la revisión externa
- `export-template-package.ps1`
  - exporta docs seguros para template, ejemplos genéricos y un layout starter a `ops/template-package/`
- `verify-template-package.ps1`
  - verifica que el template package exportado incluya la estructura starter necesaria y no contenga material review-only ni local-only

## Governance Note

- `sync-skills.ps1` y `batch-adopt-skills.ps1` deben cumplir:
  - dry-run first
  - backup before mutation
  - generar logs trazables

## Platform Note

- La nueva ruta de first-run debe usar preferentemente `bootstrap.py` y `verify-bootstrap.py`.
- `sync-skills.ps1` sigue existiendo como implementación de referencia para Windows PowerShell y como patrón de gobernanza.
