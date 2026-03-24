# UniText — Checklist de Release de Template

> Uso: revisar rápidamente si ya se completó el cleanup mínimo antes de exportar o publicar el template package.

## 1. Docs

- [ ] `README.md` no depende del contexto personal del autor para entenderse
- [ ] `INDEX.md` puede servir como entrada de discovery
- [ ] `PROJECT_MODES.md` distingue claramente entre template y authoring workspace
- [ ] `SECRET_HANDLING_GUIDELINES.md` define el límite de secretos y no contiene credenciales reales
- [ ] `TEMPLATE_RELEASE_PACKAGE.md` está actualizado
- [ ] `MILESTONES.md` refleja el estado actual de las fases

## 2. Límites de Cleanup

- [ ] el template package no incluye `backup/`
- [ ] el template package no incluye `recovered_*`
- [ ] el template package no incluye `.bak_*`
- [ ] el template package no incluye `ops/history/`
- [ ] el template package no incluye docs sólo para revisión
- [ ] el template package no incluye rutas absolutas específicas de la máquina

## 3. Ejemplos

- [ ] al menos 1 ejemplo de generic skill
- [ ] al menos 1 ejemplo de generic agent
- [ ] al menos 1 ejemplo de generic mcp
- [ ] al menos 1 ejemplo de generic workflow
- [ ] al menos 1 skeleton de local overlay genérico
- [ ] el starter package incluye una ruta cross-platform `bootstrap -> verify`

## 4. Validación

- [ ] `health-check.ps1` pasa correctamente
- [ ] `export-template-package.ps1 -DryRun` lista el contenido del package
- [ ] `export-template-package.ps1` produce el package con éxito
- [ ] `verify-template-package.ps1` pasa correctamente
- [ ] `bootstrap.py --dry-run` puede previsualizar la inicialización en un entorno limpio
- [ ] `verify-bootstrap.py` puede verificar el wiring de first-run
- [ ] el package contiene `manifest.json`
- [ ] el package contiene `release.json`

## 5. Decisión de Release

Si todos los puntos anteriores están completos, se puede considerar:

**adecuado para template release candidate**

Si todavía hay límites local-only poco claros, examples incompletos o validación de CLI insuficiente, entonces sigue siendo:

**template release cleanup baseline**
