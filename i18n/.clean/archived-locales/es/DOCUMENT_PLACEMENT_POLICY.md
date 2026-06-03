[English](../../DOCUMENT_PLACEMENT_POLICY.md) | [繁體中文](../zh-TW/DOCUMENT_PLACEMENT_POLICY.md) | [简体中文](../zh-CN/DOCUMENT_PLACEMENT_POLICY.md) | [日本語](../ja/DOCUMENT_PLACEMENT_POLICY.md) | [Deutsch](../de/DOCUMENT_PLACEMENT_POLICY.md) | [Français](../fr/DOCUMENT_PLACEMENT_POLICY.md) | [Español](DOCUMENT_PLACEMENT_POLICY.md) | [한국어](../ko/DOCUMENT_PLACEMENT_POLICY.md) | [Italiano](../it/DOCUMENT_PLACEMENT_POLICY.md)

# UniText — Política de ubicación de documentos

> Estado: Active Baseline
> Propósito: definir en qué capa deben vivir los documentos de governance, reference, authoring y operations para evitar que se mezclen el shared content y el live workspace content.

## 1. Purpose

UniText es al mismo tiempo:

- un authoring workspace
- una shared registry baseline
- una fuente para export template / rebuild

Por eso, si un documento se clasifica solo por su tema, es fácil colocarlo en la capa equivocada.

Esta regla responde:

- qué tipos de documentos deben ir en `registry/`
- qué tipos de documentos deben ir en `local/`
- qué tipos de documentos deben ir en `ops/`
- qué documentos pueden quedar tracked
- qué documentos deben quedarse solo en el espacio local de authoring ignorado

## 2. Core Rule

Para decidir dónde colocar un documento, primero importa la naturaleza del contenido y no el área temática.

- si describe shared canonical truth, va a la shared layer
- si describe el estado actual de un único authoring workspace, va a la local layer
- si describe historial operativo, resultados de export, audit evidence o generated state, va a la operations layer

El hecho de que un documento se haya escrito en una “ventana de trabajo” concreta o en una máquina de authoring concreta no es el criterio principal.

- Haberlo escrito dentro del UniText authoring workspace no significa automáticamente `local/docs/authoring/`
- Estar tracked tampoco significa automáticamente “publicable” o “listo para push”
- Primero pregunta a quién sirve el documento y qué capa de verdad describe; después decide su ubicación

## 3. Placement Matrix

| Content type | Canonical location | Tracked | Share-safe | Notes |
|---|---|---|---|---|
| principios de arquitectura, reglas de governance, specs template-safe | root docs o `registry/` | Yes | Yes | deben evitar live workspace values |
| shared sanitized reference | `registry/.../references/` | Yes | Yes | puede describir la estructura, pero los valores deben estar redacted o en placeholders |
| shared workflow / runbook / template | `registry/workflow/` | Yes | Yes | no debe quedar atado a una sola máquina autora |
| machine-local path map / wiring notes | `local/docs/` | Case-by-case | Usually no | puede registrar location / state, pero no plaintext secret |
| live workspace baseline | `local/docs/*_WORKSPACE_BASELINE.md` | No | No | debe ignorarse |
| live operational checklist | `local/docs/*_LIVE.md` | No | No | debe ignorarse |
| authoring plans / drafts / review notes | `local/docs/authoring/` | No | No | debe ignorarse |
| generated audit trail / export output / drift report | `ops/` | No | No | es state, no canonical source |

## 4. Naming Rules

Si un mismo tema necesita versión shared y versión live, por defecto usa nombres en pareja:

- shared sanitized doc
  - `registry/.../references/<topic>.md`
- live workspace doc
  - `local/docs/<TOPIC>_WORKSPACE_BASELINE.md`
  - o `local/docs/<TOPIC>_LIVE.md`

## 5. Pair Rule

Si shared sanitized doc y live workspace doc existen al mismo tiempo, debe cumplirse:

1. la versión shared conserva solo estructura template-safe y redacted placeholders
2. la versión live se queda solo en `local/docs/` o `local/docs/authoring/`
3. la versión shared debe indicar dónde está la versión live
4. la versión live también debe señalar su shared sanitized reference correspondiente

## 6. Publishing Rule

Estas afirmaciones no deben confundirse:

- template export passes
- rebuild export passes
- branch is publish-safe

Que template / rebuild export sean seguros solo significa que el artefacto exportado tiene una frontera más limpia. No significa que todo el tracked content dentro del repo de authoring sea apto para push.

## 7. Quick Decisions

Si no sabes dónde va un documento, primero hazte estas tres preguntas:

1. ¿Describe cómo se ve actualmente un único authoring workspace?
   - sí: prioriza `local/docs/`
2. ¿Es un resultado operativo, un artefacto de auditoría, un paquete exportado o un drift report?
   - sí: prioriza `ops/`
3. ¿Debe poder referenciarse con seguridad desde template / rebuild / shared registry?
   - sí: prioriza root docs, `registry/` o la shared workflow layer

## 8. Decision Ladder

Si necesitas un criterio más estable, sigue este orden:

1. ¿Es generated state, audit evidence, un drift report o un export output?
   - sí: va a `ops/`
2. ¿Describe un único authoring workspace, una sola máquina o el live wiring actual?
   - sí: va a `local/docs/`
3. Si describe un único workspace, ¿es un draft, una review note o un authoring workboard?
   - sí: va a `local/docs/authoring/`
4. ¿Es canonical truth para que futuros shared readers la reutilicen y además debe ser template-safe?
   - sí: va a la tracked shared layer
5. Si va a la tracked shared layer, ¿a qué se parece más?
   - repo-wide policy / spec: va a root docs
   - sanitized reference: va a `registry/.../references/`
   - shared workflow / runbook: va a `registry/workflow/`
6. Si deben existir versiones shared y live
   - crea un sanitized/live pair; no mezcles ambas fronteras en un solo archivo

Si aún no estás seguro, usa:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\local\scripts\get-document-placement-recommendation.ps1 -Topic "cloudflare workflow" -CanonicalSharedTruth -SharedForm registry-reference
```

## 9. Common Misplacements

- poner una live Cloudflare baseline en `registry/.../references/`
- poner un strategy / review plan en la raíz
- tratar un export output o una audit evidence como canonical reference
- escribir machine-specific paths directamente en shared governance docs

## 10. Review Gate

Antes de añadir cualquier documento de governance / reference, como mínimo hay que confirmar:

- que describe shared truth y no live workspace state
- que, si se hace push, sigue cumpliendo `NO_PUBLISH_POLICY.md` y la expectativa template-safe
- que no necesita un par sanitized/live en vez de mezclar ambas cosas en un solo archivo

## 11. Related Docs

- `README.md`
- `INDEX.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`
- `SECRET_HANDLING_GUIDELINES.md`
- `NO_PUBLISH_POLICY.md`
