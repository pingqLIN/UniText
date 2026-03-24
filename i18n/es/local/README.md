# Local Overlay

Este directorio contiene **despliegue local, scripts, referencia de rutas y otras capas no centrales**.

Su propósito es muy simple:

- evitar que la configuración local contamine los conceptos centrales del repo
- centralizar las modificaciones locales
- permitir que todo `local/` pueda eliminarse y reconstruirse si hace falta

## Contents

- `docs/`
  - documentos de despliegue local y tablas de referencia
- `scripts/`
  - scripts para ejecutar en esta máquina

## Current Files

- [docs/authoring](/mnt/q/UniText/local/docs/authoring)
  - documentos centrales reforzados del authoring, conservados antes de la refactorización
- [docs/MCP_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/MCP_DEPLOYMENT_NOTES.md)
  - notas actuales sobre despliegue y wiring de MCP local
- [docs/PATH_MAP.md](/mnt/q/UniText/local/docs/PATH_MAP.md)
  - referencia actual de rutas desplegadas y contraste histórico
- [docs/WORKFLOW_DEPLOYMENT_NOTES.md](/mnt/q/UniText/local/docs/WORKFLOW_DEPLOYMENT_NOTES.md)
  - notas actuales sobre wiring de workflow local
- [scripts/sync-skills.ps1](/mnt/q/UniText/local/scripts/sync-skills.ps1)
  - script local de sincronización

## Rule

Si un contenido describe:

- cómo debería funcionar este sistema
  - no debería estar en `local/`
- cómo está configurada esta instancia ahora mismo
  - debería estar en `local/`
