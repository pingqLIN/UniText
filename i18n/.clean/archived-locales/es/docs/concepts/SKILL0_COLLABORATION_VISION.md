# UniText × skill-0 — Visión de Colaboración

> Estado: borrador conceptual
> Propósito: definir la relación entre `UniText` y `skill-0`, su espacio de colaboración, los posibles caminos y las piezas que todavía faltan.

## 1. Resumen Ejecutivo

`UniText` y `skill-0` no son proyectos mutuamente excluyentes ni duplicados; pueden formar una relación de upstream / downstream entre dos capas:

- `UniText` se encarga del **registry / delivery / governance** de shared resources
- `skill-0` se encarga de absorber skills de nivel superior, descomponerlos y normalizarlos en un **atomic operation set** más general

Por tanto, la colaboración más razonable no es “quién sustituye a quién”, sino:

**UniText aporta inputs canónicos y una superficie gobernable; skill-0 aporta capacidad de descomposición / normalización / recomposición.**

## 2. Cada Proyecto Resuelve un Problema Distinto

### UniText

`UniText` resuelve:

- cómo canonicalizar un shared resource
- cómo entregarlo entre varias AI CLI
- cómo gobernar cambios con `SCAN -> REVIEW -> DRY-RUN -> ADOPT -> DELIVER -> VERIFY`

En otras palabras:

**distribution / governance problem**

### skill-0

`skill-0` resuelve:

- de qué unidades mínimas está realmente compuesto un skill de nivel alto
- qué pasos son primitive reutilizables
- qué partes del texto son surface wording y cuáles son la operación central
- si un skill de alto nivel puede reensamblarse en un conjunto más pequeño, general y portable

En otras palabras:

**abstraction / compiler / normalization problem**

## 3. Relación Entre Ambos

Si se mira desde el objetivo de `skill-0`, el papel más valioso de `UniText` no es ser sólo el destino de entrega, sino:

- una fuente estable de skills de alto nivel
- un corpus canónico con identidad lógica y metadata
- un conjunto de datos de skills que se puede analizar, comparar y seguir en el tiempo

Desde ese ángulo, la relación puede describirse así:

| Project | Primary role |
|---|---|
| `UniText` | fuente canónica de verdad para shared resources |
| `skill-0` | analizador / descomponedor / compilador sobre skills de nivel alto |

En una frase:

**UniText guarda skills, skill-0 descompone skills.**

## 4. Espacio Actual de Colaboración

Incluso sin cambiar el schema central de `UniText`, ya existe espacio de colaboración:

### 4.1 Usar UniText como corpus de entrada

`skill-0` puede usar directamente:

- `registry/skills/*/SKILL.md`
- la metadata de catálogo de `INDEX.md`
- el contrato de identidad / canonical location de `RESOURCE_SPEC.md`

Así `skill-0` analiza un corpus canónico relativamente limpio, no copias dispersas.

### 4.2 Usar UniText como terreno de staging gobernado

La salida analítica de `skill-0` puede no entrar todavía en el registry canónico y quedarse primero en:

- `/operations`
- por ejemplo `ops/analysis/skill-0/`

Esto es útil porque:

- evita contaminar demasiado pronto el schema de shared resources
- permite observar si el formato de análisis se estabiliza
- permite tratar `skill-0` como pipeline analítico, no como fuente canónica inmediata

### 4.3 Usar el flujo de revisión de UniText para evaluar outputs derivados

Cuando `skill-0` produzca:

- atom maps
- conjuntos de pasos normalizados
- clusters de subrutinas compartidas
- candidatos a recomposición

esas salidas pueden revisarse con la misma mentalidad de `UniText`:

- la identidad es estable
- el naming es claro
- el mapeo con el skill original es trazable
- hace falta o no una decisión humana sobre la forma canónica

## 5. Modos de Colaboración Más Probables

### Mode A — skill-0 como analizador externo

`skill-0` toma `UniText` como fuente de datos y produce analysis reports, pero no reescribe el registry.

Adecuado para:

- validar rápidamente el método de decomposition
- analizar solapamientos entre skills
- localizar primitives reutilizables

Ventajas:

- coste de adopción bajo
- casi no requiere tocar el schema de `UniText`

Desventajas:

- los resultados se quedan como artefactos laterales
- cuesta más convertirlos en shared canonical resources

### Mode B — skill-0 como generador lateral

`skill-0` lee `registry/skills` y genera sidecars al lado, por ejemplo:

- `skill.atoms.json`
- `skill.graph.json`
- `skill.coverage.json`

Ventajas:

- establece un mapeo claro entre skill y atom
- es más fácil de convertir en tooling que un simple report

Desventajas:

- empieza a rozar los límites del schema de `UniText`
- hace falta definir qué sidecars son canónicos y cuáles son sólo generados

### Mode C — las primitivas pasan a ser un tipo de recurso de primera clase

Si la colaboración madura, `UniText` podría añadir un tipo formal de recurso, por ejemplo:

- `/registry/primitives`
- o `/registry/operations`

Eso haría que la salida de `skill-0` ya no fuera un adjunto analítico, sino un shared resource gobernado por el registry.

Ventajas:

- se crea una capa de vocabulario compartido real
- podría soportar recomposición entre skills

Desventajas:

- exige cambiar el resource model de `UniText`
- exige nuevo metadata spec, flow de adopción y reglas de verificación

## 6. Qué Falta Hoy

Actualmente no se puede integrar `skill-0` en profundidad de forma natural porque faltan estas piezas:

### 6.1 Falta un tipo canónico para primitives

`UniText` hoy sólo tiene como tipos de recurso de primer nivel:

- `skills`
- `mcp`
- `agents`
- `workflow`

Todavía no existe:

- `primitives`
- `operations`
- `atoms`

Por eso, lo que más le importa a `skill-0` todavía no tiene una superficie de primer nivel en `UniText`.

### 6.2 Falta un spec de metadata para unidades atómicas

`RESOURCE_SPEC.md` sirve para recursos de alto nivel, pero todavía no define:

- atom id
- operation signature
- preconditions / postconditions
- reglas de composición
- provenance de vuelta al skill fuente

### 6.3 Falta un flujo de adopción para artefactos derivados

`UniText` ya tiene un flujo de adopción para skills, pero todavía no tiene uno específico para casos como:

- un mismo skill descompuesto en varios atom sets
- varios skills que producen primitives parecidas pero no idénticas
- decidir si un atom ya es suficientemente estable como para canonizarlo

### 6.4 Falta un modelo de verificación

Si la salida de `skill-0` entra en una fase más formal de colaboración, hay que responder como mínimo:

- si la descomposición es estable
- si se puede recomponer de vuelta
- si realmente mejora el reuse entre skills
- si simplemente renombra la descripción original

### 6.5 Falta el borde entre análisis y canon

Todavía hace falta una regla clara:

- qué productos de `skill-0` son sólo analysis
- cuáles ya pueden verse como canonical shared resource

Mientras ese borde no esté claro, lo más seguro sigue siendo dejar la salida en `ops/analysis/skill-0/`.

## 7. Dirección Recomendada a Corto Plazo

La dirección más razonable a corto plazo no es cambiar ya el schema central de `UniText`, sino seguir un camino gradual:

**Mode A -> Mode B**

### Fase A — sólo análisis

Primero:

- usar `registry/skills/*/SKILL.md` como input
- producir decomposition reports
- guardar la salida en `ops/analysis/skill-0/`

El objetivo no es canonicalizar, sino verificar:

- si la extracción de atoms es estable
- si el solapamiento entre skills realmente se puede observar
- qué primitives merecen conservarse

### Fase B — sidecars estables

Cuando el formato empiece a estabilizarse, introducir:

- schemas de sidecar
- reglas de naming
- enlace con el skill fuente
- verificación básica

En esta fase todavía no hace falta un nuevo resource type, pero ya se puede construir:

- `skill -> atoms`
- `atom -> source skills`

### Fase C — primitives como recurso de primera clase

Si el análisis demuestra valor real, entonces puede discutirse si incorporar a `UniText` alguna de estas opciones:

- `/registry/primitives`
- `/registry/operations`

Sólo ahí tendría sentido modificar formalmente:

- `VISION.md`
- `RESOURCE_SPEC.md`
- `INDEX.md`
- `OPERATIONS.md`

## 8. Primeros Entregables Concretos

Si se quiere que ambos proyectos empiecen a colaborar, los primeros entregables útiles no son un cambio de arquitectura grande, sino estas cuatro cosas:

1. definir un draft schema de salida de análisis para `skill-0`
2. elegir 1 o 2 skills del `Core 8` de UniText para un ejemplo de decomposition
3. guardar la salida en `ops/analysis/skill-0/`
4. comparar:
   - atoms compartidos entre distintos skills
   - la distancia entre la descripción del skill y la capa de atoms
   - si se puede reconstruir el workflow mínimo útil

## 9. Interpretación Estratégica

Si la colaboración funciona, la división a largo plazo sería clara:

- `UniText` como hub canónico de shared AI resources
- `skill-0` como motor de normalización de skills y extracción de primitives

Visto por capas del sistema:

| Layer | Project |
|---|---|
| Canonical resource governance | `UniText` |
| Skill decomposition / normalization | `skill-0` |
| Future primitive vocabulary layer | resultado compartido entre `UniText × skill-0` |

## 10. Posición Final

La conclusión más precisa es:

**`UniText` y `skill-0` están muy relacionados, pero no hacen lo mismo.**

Uno se centra en gobernar y distribuir; el otro en descomponer y abstraer.

Por eso, a corto plazo, la colaboración más razonable no es meter `skill-0` directamente en las cuatro categorías de recursos actuales de `UniText`, sino:

**dejar que `skill-0` use `UniText` como corpus canónico de entrada y que sus resultados vivan primero en `ops/analysis/skill-0/`.**

Cuando el formato de salida, su valor y su método de verificación ya estén estables, entonces se puede decidir si la capa de primitive / operation merece convertirse en un nuevo tipo canónico de recurso.
