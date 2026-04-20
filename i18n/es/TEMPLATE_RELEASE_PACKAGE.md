# UniText — Paquete de Release de Template

> Estado: Active Baseline  
> Uso: definir el objetivo, el alcance y el flujo de exportación repetible del template release cleanup.

## 1. Propósito

El template release de `UniText` no debe ser un empaquetado literal del workspace del autor, sino una salida que:

- conserve la arquitectura y las specs centrales
- conserve ejemplos mínimos utilizables
- excluya el estado local-only
- excluya restos históricos de gobernanza
- sea adecuada para que otros usuarios hagan fork / clone y la amplíen por su cuenta

La posición de este package es:

**starter template**

y no:

**authoring workspace snapshot**

## 2. Incluir

Actualmente el template package debe incluir:

- Documentos centrales
  - `README.md`
  - `INDEX.md`
  - `VISION.md`
  - `RESOURCE_SPEC.md`
  - `OPERATIONS.md`
  - `PROJECT_MODES.md`
  - `SECRET_HANDLING_GUIDELINES.md`
  - `MILESTONES.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- configuración raíz segura para template
  - `.gitignore`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- skeleton starter de local overlay
  - `local/README.md`
  - `local/docs/PATH_MAP.md`
  - `local/scripts/bootstrap.py`
  - `local/scripts/verify-bootstrap.py`
  - `local/scripts/create-git-bundle.py`
  - `local/scripts/sync-skills.ps1`
- metadata de release
  - `manifest.json`
  - `release.json`

## 3. Excluir

El template package no debe incluir:

- `backup/`
- `recovered_*`
- `.bak_*`
- `ops/history/`
- `ops/review-package/`
- `ops/template-package/`
- authoring notes and review archives
- `local/docs/PATH_MAP.md`
- cuentas de usuario reales, home directory o rutas absolutas
- docs específicas de revisión
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `docs/reports/status/PROJECT_STATUS_REPORT_2026-03-23.md`

## 4. Comando de Exportación

En la raíz del repo, ejecutar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
```

La salida por defecto va a:

```text
ops/template-package/template_YYYYMMDD_HHMMSS/
```

Si sólo se quiere revisar el contenido sin escribir archivos:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1 -DryRun
```

Si se quiere verificar un package exportado:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

Después de exportar, la ruta recomendada para first-run del nuevo usuario es:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

## 5. Interpretación de la Exportación

El template package exportado representa:

- el contrato central de UniText
- un starter layout limpio
- un conjunto mínimo de generic examples

No representa:

- el estado completo actual del autor
- todos los skills ya adoptados
- todas las pruebas de review / audit
- todo el wiring local de delivery ya completado

## 6. Interpretación Actual

Hasta 2026-03-24, `UniText` ya tiene:

- review package para revisión externa
- reviewer-facing entry docs
- baseline de limpieza para template release
- un export script repetible para template package
- skeleton starter de local overlay
- un script de verificación de template package
- metadata de release
- scripts cross-platform de first-run
- un flujo de backup portable basado en bundle

Por tanto, la lectura más adecuada es:

**template release candidate**

y no:

**authoring workspace snapshot**
