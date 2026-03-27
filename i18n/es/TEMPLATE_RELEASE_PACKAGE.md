# UniText — Paquete de Release de Template

## Nota de sincronización 2026-03-27

Para esta traducción, las reglas de release-boundary que deben leerse como current baseline son:

- un package público sólo puede incluir skills públicamente redistributable
- si se incluyen shared skills, deben llevar `SOURCE.yaml` o metadata de provenance equivalente
- `local-only validation materials` y `proprietary / restricted-license skills` no deben entrar en el package público
- si hay diferencia entre el authoring workspace y el export, la release truth es el exported package

Si esta traducción difiere del documento principal, debe tratarse el [guide en inglés](../../TEMPLATE_RELEASE_PACKAGE.md) como authoritative version.

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
  - `SKILLS_PUBLIC_RELEASE_POLICY.md`
  - `TEMPLATE_RELEASE_PACKAGE.md`
  - `TEMPLATE_RELEASE_CHECKLIST.md`
- configuración raíz segura para template
  - `.gitignore`
  - `.mcp.json`
  - `.claude/settings.json`
- generic examples
  - `registry/skills/example-skill/`
  - `registry/agents/example-agent/`
  - `registry/mcp/example-mcp/`
  - `registry/workflow/example-workflow/`
- skills con licencia pública y redistributable
  - sólo entries cuya frontera de licencia permite entrar en el package público
  - si se incluyen shared skills, deben llevar `SOURCE.yaml` o datos equivalentes de procedencia
- runnable MCP baseline
  - `registry/mcp/claude-project-mcp-seed/`
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
- local-only validation materials
  - skills o materiales usados en dry-run / validación del authoring workspace que no forman parte del contenido públicamente redistributable
- proprietary / restricted-license skills
  - archivos o assets de skills cuya frontera de licencia no permite o no aclara su redistribución pública
- docs específicas de revisión
  - `EXTERNAL_REVIEW_PACKAGE.md`
  - `EXTERNAL_REVIEW_COVER_NOTE.md`
  - `EXTERNAL_REVIEW_HIGHLIGHTS.md`
  - `PROJECT_STATUS_REPORT_2026-03-23.md`

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

Si se quiere exportar directamente como un starter project nuevo, en vez de un template package general:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-rebuild-project.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-rebuild-project.ps1 -Path .\ops\rebuild-project\<package-name>
```

Después de exportar, la ruta recomendada para first-run del nuevo usuario es:

```bash
python local/scripts/bootstrap.py --dry-run
python local/scripts/bootstrap.py --force
python local/scripts/verify-bootstrap.py
python local/scripts/create-git-bundle.py
```

Si el sistema sólo expone `python3`, sustituye `python` por `python3`.

## 5. Interpretación de la Exportación

El template package exportado representa:

- el contrato central de UniText
- un starter layout limpio
- un conjunto mínimo de generic examples
- una ruta repetible `bootstrap -> verify` de tipo cross-platform
- una `.claude/settings.json` que Claude puede leer directamente
- un seed `.mcp.json` para project-local MCP
- un shared baseline al que un adapter futuro de Copilot CLI puede conectarse
- skills / examples template-safe y públicamente redistributable
  - si algo distinto de `example-skill` entra en el package, debe poder rastrearse a un upstream claro

No representa:

- el estado completo actual del autor
- todos los skills ya adoptados
- todos los materiales locales de validación del mantenedor
- todas las pruebas de review / audit
- todo el wiring local de delivery ya completado
- el interpreter pinning ya resuelto para cualquier máquina

## 5.1 Skills Release Rule

El template release aplica estas reglas para skills:

- un skill públicamente redistributable puede entrar en el package
- si se incluye un active shared skill, debe llevar metadata de procedencia
- un skill con licencia incierta o restringida no puede entrar en el package
- los local-only validation materials pueden existir en el authoring workspace, pero no deben salir como contenido público

Si un dry-run o una validación utilizó skills locales no exportables, la documentación puede dejar constancia de que:

- la validación sí se realizó localmente
- esos materiales no se incluyeron en la versión pública por límites de licencia o de release boundary

Pero la documentación no debe dejar entender que:

- el package público ya contiene esos skills
- UniText puede redistribuir públicamente esos skills

## 6. Interpretación Actual

Hasta 2026-03-27, `UniText` ya tiene:

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

