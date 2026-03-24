# UniText — Visión

> Estado: Template Base
> Principio: usar contratos lógicos como referencia, no asumir ningún sistema operativo, estructura de directorios o método de despliegue como premisa de la especificación.

## 1. Qué es UniText

`UniText` es un shared resource hub nativo de texto, registry-first y AI-first, para que varios sistemas AI CLI / agentes compartan definiciones de recursos y sus formas de adopción usando el mismo contrato en texto plano.

Tiene dos capas:

1. `Registry`
   - define los shared resources, su identidad canónica y el contrato mínimo
2. `Adapter / Operations Control Plane`
   - conecta el contenido del registry con distintos CLIs y maneja install, sync, adopt y repair

## 2. Qué problema resuelve

`UniText` resuelve la fragmentación habitual al compartir recursos entre herramientas:

- skills dispersos en distintos lugares
- definiciones MCP repartidas entre distintos formatos de configuración
- instrucciones de agentes que no se pueden compartir
- convenciones de workflow difíciles de mantener entre herramientas
- falta de una interfaz textual compartida, fácil de leer para AI y amigable con versionado

## 3. Posicionamiento de la Arquitectura

Posicionamiento formal:

**Registry-first, adapter-enabled, operations-governed**

Principios clave:

- sin registry no hay fuente compartida ni semántica común
- sin adapter no se puede entregar el registry a cada CLI
- la AI es un consumer y colaborador importante, pero no el único mecanismo fiable de integración

## 4. Tipos de Recurso

Tipos compartidos por defecto:

- `skills`
- `mcp`
- `agents`
- `workflow`

`operations state` no es un shared resource type y debe vivir por separado en `/operations`.

## 5. Discovery y Delivery

`INDEX.md` se encarga de discovery y responde:

- qué recursos existen
- cuál es la ubicación lógica de cada recurso
- qué CLIs están soportadas

`OPERATIONS.md` se encarga de delivery y responde:

- cómo obtiene recursos una CLI determinada
- cuándo ejecutar install, sync, adopt o repair
- cómo se resuelve el delivery mode

Delivery modes disponibles:

- `pointer`
- `mirror`
- `symlink`
- `native-config`

## 6. Triggers de Delivery

delivery sólo puede activarse con triggers explícitos:

- `bootstrap`
- `sync`
- `adopt`
- `repair`

Todas las operaciones destructivas deben cumplir:

- primero dry-run
- primero backup
- nunca decidir en silencio cuál es la fuente canónica

## 7. Modelo de Adopción

### Soft Adoption

- primero se introduce discovery
- no se obliga a migrar recursos existentes de inmediato

### Formal Adoption

Flujo formal de adopción:

1. `SCAN`
2. `REVIEW`
3. `DRY-RUN`
4. `ADOPT`
5. `DELIVER`
6. `VERIFY`

Si aparecen recursos con el mismo nombre pero contenido distinto, el flujo debe detenerse en `REVIEW / DRY-RUN`.

## 8. Conjunto de Documentación

Documentos centrales:

- `VISION.md`
- `INDEX.md`
- `RESOURCE_SPEC.md`
- `OPERATIONS.md`
- `PROJECT_MODES.md`

## 9. Estrategia de Rutas

El texto principal usa rutas lógicas canónicas, por ejemplo:

- `/registry/skills`
- `/registry/mcp`
- `/registry/agents`
- `/registry/workflow`
- `/operations`

Las rutas absolutas y la configuración específica de plataforma sólo pertenecen al mapeo de despliegue, no a la capa de visión.

## 10. Principios de Diseño

- `Registry first`
- `Discovery before automation`
- `Explicit triggers`
- `Minimum viable metadata`
- `Canonical source of truth`
- `CLI-specific delivery`
- `Platform-agnostic contract`
- `Safe mutation`

## 11. Posicionamiento en una Frase

> UniText es un shared resource hub nativo de texto, registry-first y AI-first, que mediante adapters claros y un operations control plane permite que varias AI CLI descubran, adopten y compartan de forma segura los mismos canonical resources.
