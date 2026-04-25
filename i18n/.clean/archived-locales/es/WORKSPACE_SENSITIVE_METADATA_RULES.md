[English](../../WORKSPACE_SENSITIVE_METADATA_RULES.md) | [繁體中文](../zh-TW/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [简体中文](../zh-CN/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [日本語](../ja/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Deutsch](../de/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Français](../fr/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Español](WORKSPACE_SENSITIVE_METADATA_RULES.md) | [한국어](../ko/WORKSPACE_SENSITIVE_METADATA_RULES.md) | [Italiano](../it/WORKSPACE_SENSITIVE_METADATA_RULES.md)

# Workspace Sensitive Metadata Rules

> Estado: Active Baseline
> Propósito: definir las reglas de detección, las reglas de mantenimiento y los límites de validación de las workspace-sensitive metadata sobre las shared surfaces.

## 1. Purpose

`WORKSPACE_SENSITIVE_METADATA_RULES.json` es la fuente de reglas compartida entre el authoring repo y el exported starter package. Su objetivo es reducir estas derivas:

- shared docs con rutas absolutas locales
- shared scripts con live workspace hostnames
- shared governance files con live redirect URIs o Cloudflare IDs
- boundary verify y template verify usando conjuntos de reglas distintos

Este documento explica:

- qué representa cada sección del archivo de reglas
- cuándo debe añadirse una nueva regla
- cómo evitar que un sanitized placeholder se interprete como live metadata
- qué validaciones deben volver a ejecutarse tras cambiar una regla

## 2. Schema

`WORKSPACE_SENSITIVE_METADATA_RULES.json` tiene actualmente cuatro bloques de nivel superior:

- `shared_surface_scope`
  - define las tracked shared surfaces que repo-side boundary verify escanea por defecto
- `path_rules`
  - define qué tracked paths no deberían aparecer dentro de una shared surface
- `content_patterns`
  - define qué contenidos textuales se consideran workspace-sensitive metadata
- `self_test_cases`
  - define casos positivos y negativos integrados para evitar regresiones silenciosas al modificar regex

## 3. Maintenance Rules

- cuando se añade un nuevo shared governance doc o shared control script y este forma parte del repo-side boundary review, también debe añadirse a `shared_surface_scope`
- cuando aparece un nuevo tipo de live metadata, primero se amplía `content_patterns` y luego los `self_test_cases` correspondientes
- si un placeholder debe tratarse como ejemplo seguro, hay que añadir un self-test case con `expected_labels = []`
- si una regex solo aparece dentro de un script como cadena de regla, hay que marcar explícitamente `skip_script_pattern_lines`
- no se deben meter paths authoring-only u operations-only en `shared_surface_scope` para tapar falsos positivos; primero hay que revisar si el documento está mal colocado

## 4. Required Validation

Después de cada ajuste en `WORKSPACE_SENSITIVE_METADATA_RULES.json`, como mínimo hay que volver a ejecutar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\validate-workspace-sensitive-metadata-rules.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-workspace-boundaries.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\health-check.ps1
```

Si el cambio afecta a la starter baseline, también hay que ejecutar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\export-template-package.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\verify-template-package.ps1 -Path .\ops\template-package\<package-name>
```

## 5. Design Boundary

El objetivo de estas reglas es:

- ofrecer heuristic controls estables, mantenibles y verificables sobre la shared surface

No son:

- un validador de esquema completo para todos los tipos de secret
- un sistema DLP genérico para todos los infrastructure providers
- una herramienta para escanear por completo las zonas local-only / ops-only

Si los tipos de metadata siguen creciendo, el siguiente paso debe ser ampliar la fuente de reglas y los casos, no volver a meter live references en la shared registry.
