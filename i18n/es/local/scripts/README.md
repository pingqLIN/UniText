# Local Scripts

Aquí se guardan los **scripts de operación local**.

- `*.ps1` se mantiene como implementación de referencia Windows-first
- `*.py` ofrece la ruta cross-platform para `bootstrap` / `verify` / `backup`

## Current Scripts

- `bootstrap.py`
  - inicializa de forma cross-platform el skills delivery, la configuración nativa de Codex, la configuración MCP de Copilot y el archivo `.mcp.json` del proyecto
- `verify-bootstrap.py`
  - comprueba de forma cross-platform que el resultado del first-run coincide con el repo actual, y acepta tanto el seed template-safe de `.mcp.json` como un wiring local ya bootstrapped
- `create-git-bundle.py`
  - crea una copia de seguridad portable en `git bundle` y reduce el riesgo de punto único de fallo de un worktree puramente local
- `git-startup.ps1`
  - resuelve el canonical base branch para una nueva sesión, exige un worktree limpio, realiza una actualización explícita por fast-forward y crea una nueva feature branch
- `sync-skills.ps1`
  - sincroniza `registry/skills/` hacia los skills targets locales
- `scan-skills.ps1`
  - escanea skills candidatas y devuelve el resultado de la comprobación de adopción
- `verify-delivery.ps1`
  - verifica si la fuente y los skills targets habituales existen, son enlaces y pueden resolverse
- `health-check.ps1`
  - ejecuta una verificación mínima de salud sobre el registry y los scripts
- `batch-adopt-skills.ps1`
  - mueve por lotes las skills candidatas a `registry/skills/`
- `generate-index-entries.ps1`
  - genera desde `registry/skills/` el bloque de catálogo requerido por `INDEX`
- `rollback-skills.ps1`
  - restaura una skill concreta desde las copias de seguridad `ops/history/adopt_*`
- `export-review-package.ps1`
  - exporta a `ops/review-package/` la cover note, los highlights, los documentos centrales, las entradas seleccionadas del registry y los scripts mínimos necesarios para revisión externa
- `export-template-package.ps1`
  - exporta a `ops/template-package/` los docs template-safe, los generic examples y el starter layout
- `verify-template-package.ps1`
  - verifica que el template package exportado contiene la estructura starter necesaria y no incluye contenido review-only o local-only
- `verify-workspace-boundaries.ps1`
  - verifica que las tracked shared surfaces del repo de authoring actual no mezclen live workspace metadata, authoring-only docs ni operations state
- `get-publishability-report.ps1`
  - resume los cambios local-only / ops / shared-surface de la rama actual junto con el resultado del boundary verify para generar un informe local de push suitability
- `lib/workspace-sensitive-metadata.ps1`
  - carga el archivo compartido `WORKSPACE_SENSITIVE_METADATA_RULES.json` para que las validaciones de boundary, template y publishability utilicen el mismo conjunto de reglas
- `validate-workspace-sensitive-metadata-rules.ps1`
  - valida la estructura, la compilación de regex y los casos integrados del archivo compartido `WORKSPACE_SENSITIVE_METADATA_RULES.json`
- `preview-renormalize.ps1`
  - ejecuta solo un dry-run para previsualizar cuántos tracked files tocaría `git add --renormalize .`, de modo que el blast radius de la limpieza de line endings pueda revisarse antes de ejecutarse
- `run-renormalize.ps1`
  - ejecuta un renormalize controlado por scope `repo / root / registry / i18n / local / template`; por defecto sigue siendo dry-run, solo `-Apply` pone cambios en stage y existe un guard `MaxFiles` para limitar el lote
- `audit-i18n-drift.py`
  - lee `i18n/manifest.json`, enumera por locale qué documentos oficiales faltan, están desactualizados o aún no están seguidos por Git, y soporta `json / markdown`, filtros por `locale / source-doc` y salida directa a un workboard
- `export-rebuild-project.ps1`
  - reconstruye el repo actual como una fresh-project baseline que puede renombrarse y reinicializarse, y la exporta a `ops/rebuild-project/`
- `verify-rebuild-project.ps1`
  - además de la validación del template package, confirma la presencia de la guía de rebuild y del punto de entrada fresh-project

## Governance Note

- Tanto `sync-skills.ps1` como `batch-adopt-skills.ps1` deben cumplir:
  - dry-run first
  - backup before mutation
  - generar logs trazables

## Platform Note

- La nueva ruta de first-run debe priorizar `bootstrap.py` y `verify-bootstrap.py`.
- `sync-skills.ps1` se mantiene como implementación de referencia de Windows PowerShell y como plantilla de gobernanza.
