# Notas de Entorno

> Estado: Active
> Uso: registrar las rutas del authoring workspace actual y sus relaciones históricas de despliegue.

## Current Working Root

- directorio principal de trabajo actual: `Q:\UniText`

## Historical Paths

- aún pueden verse snapshots antiguos de ops, inventarios y notas de rutas en `C:\Dev\UniText`
- esas rutas deben considerarse huellas históricas de despliegue y no volver a usarse como fuente de verdad para scripts nuevos

## Current Rule

- los scripts nuevos o modificados deben usar preferentemente rutas relativas al repo
- la fuente canónica de skills es `registry/skills/`
- si un documento contradice una ruta real, prevalecen los scripts actuales del repo y la estructura del registry
