# UniText — Especificación de Recursos

> Estado: Template Base
> Alcance: contrato lógico para shared resources, sin vincularlo a un único sistema operativo, estructura de directorios o formato de almacenamiento.

Esta spec asume que toda metadata central debe poder sostenerse de forma estable en texto plano, para que AI y humanos puedan leerla, compararla y versionarla juntos.

## 1. Alcance

Esta spec aplica a:

- `skills`
- `mcp`
- `agents`
- `workflow`

No aplica a:

- operations state artifacts
- mapeos de rutas específicos de plataforma
- detalles internos de ejecución del adapter

## 2. Reglas de Identidad

La identidad principal de un shared resource está formada por:

- `type`
- `id`

`id` debe:

- usar letras minúsculas, números y `-`
- no contener espacios
- no contener separadores específicos del sistema operativo

## 3. Ubicación Canónica

`canonical_location` debe ser una ruta canónica lógica, no una ruta absoluta de una máquina concreta.

Ejemplos:

- `/registry/skills/example-skill`
- `/registry/mcp/example-mcp`
- `/registry/agents/example-agent`

## 4. Niveles de Metadata

### Required

- `id`
- `type`
- `canonical_location`
- `status`

### Recommended

- `source_of_truth`
- `supported_clis`
- `delivery_guidance`

### Optional

- `owner`
- `provenance`
- `notes`
- `last_verified`

## 5. Ciclo de Vida

Valores permitidos para `status`:

- `draft`
- `active`
- `deprecated`
- `archived`

## 6. Valores por Defecto

- si `source_of_truth` no se especifica, se asume que es igual a `canonical_location`
- si `supported_clis` no se especifica, se asume `undocumented`
- si `delivery_guidance` no se especifica, se deduce desde la documentación de adapter / operations

## 7. Guía de Delivery

`delivery_guidance` es una pista de discovery, no un modo de delivery fijo.

Puede indicar:

- qué tipo de adapter consultar
- si existen diferencias de plataforma
- si hay que revisar `OPERATIONS.md`

No debe fijar:

- rutas absolutas de plataforma
- un modo de delivery permanente y rígido

## 8. Reglas de Conflicto

Si se detecta que un mismo par `(type, id)` corresponde a varios candidatos con contenido distinto:

- no sobrescribir automáticamente
- no inferir en silencio la fuente canónica
- detenerse en `REVIEW / DRY-RUN`

Resultados permitidos:

- seleccionar explícitamente una fuente canónica
- renombrar a otro `id`
- marcar como `deprecated` o `archived`
- mantener temporalmente `draft`

## 9. Ejemplo

```yaml
id: example-skill
type: skills
canonical_location: /registry/skills/example-skill
status: draft
source_of_truth: /registry/skills/example-skill/SKILL.md
supported_clis: undocumented
delivery_guidance: Use the skills adapter; resolved mode depends on CLI capabilities and local environment.
```
