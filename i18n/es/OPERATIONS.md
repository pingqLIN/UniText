# UniText — Operaciones

> Estado: Template Base
> Rol: definir responsabilidades del adapter / operations control plane, reglas de delivery y límites de seguridad.

Todo delivery y toda mutation deben tomar como fuente de verdad el contrato textual de registry / spec de UniText.

Si la operación involucra password, API key, token, credential u otro sensitive material, también debe cumplirse `SECRET_HANDLING_GUIDELINES.md`.

## 1. Alcance

Este documento cubre:

- responsabilidades del adapter
- modos de delivery
- triggers de delivery
- flujo de adopción
- drift / repair
- mapeo lógico a físico

Este documento no cubre:

- el schema de metadata de shared resources
- una única forma de implementación para una plataforma concreta
- el estado histórico de un authoring repo local

## 2. Modos de Delivery

| Mode | When to use |
|---|---|
| `pointer` | descubrimiento o recursos que no requieren registro en la máquina |
| `mirror` | cuando la CLI necesita una copia local o el symlink no es estable |
| `symlink` | cuando la CLI necesita una ruta fija y el entorno soporta enlaces estables |
| `native-config` | cuando la CLI tiene una entrada de configuración formal para registrar recursos |

El `delivery mode` lo resuelve el adapter en el momento de la operación; no es una propiedad fija del recurso.

## 3. Reglas de Resolución de Delivery

El adapter debe considerar la siguiente prioridad:

1. Si existe una entrada de configuración formal, priorizar `native-config`
2. Si se necesita una ruta fija y la plataforma soporta enlaces estables, usar `symlink`
3. Si no es seguro usar symlink, usar `mirror`
4. Si el uso principal es discovery o entrada, usar `pointer`

## 4. Triggers de Delivery

delivery sólo puede iniciarse con triggers explícitos:

- `bootstrap`
- `sync`
- `adopt`
- `repair`

## 5. Reglas de Seguridad

### Dry-Run First

Las siguientes operaciones deben generar primero un plan de dry-run:

- `adopt`
- `repair`
- `sync` cuando sobrescribe estado existente

### Backup Before Mutation

Toda operación destructiva debe incluir:

- backup o un punto de reversión equivalente
- un registro trazable de la operación
- condiciones de parada en caso de fallo

### No Silent Canonicalization

Si se encuentran recursos con el mismo nombre pero contenido distinto:

- el flujo debe detenerse en review
- el operador debe decidir explícitamente la fuente canónica

## 6. Flujo de Adopción

1. `SCAN`
   - escanear fuentes candidatas y listar recursos adoptables con su estado de readiness
2. `REVIEW`
   - comprobar metadata, calidad del contenido y legalidad de la fuente canónica según la review checklist
3. `DRY-RUN`
   - previsualizar qué objetivos cambiarán y si hace falta backup
4. `ADOPT`
   - escribir el contenido fuente en la ubicación canónica del registry; si se sobrescribe algo existente, hacer backup antes
5. `DELIVER`
   - el adapter entrega el contenido del registry a la CLI correspondiente; si sobrescribe estado existente, conservar log y backup
   - si la CLI soporta `native-config`, se puede escribir la config local de la máquina en la fase `bootstrap`, pero la definición canónica sigue viviendo en `registry/`
6. `VERIFY`
   - verificar existencia de archivos, resolución de rutas, modo de delivery y condiciones de carga de la CLI objetivo

## 6.1 Base para First-Run

Si el objetivo es que un nuevo usuario de template complete la inicialización mínima en macOS / Linux / Windows, al menos hay que ofrecer:

- un `bootstrap` multiplataforma
- un `verify` multiplataforma
- un flujo portable de backup del repo
- un baseline MCP mínimo y ejecutable

## 7. Estado de Operaciones

Lo siguiente pertenece al operations state, no a los shared resources:

- inventories
- baselines
- backups
- drift reports
- repair plans
- audit trails

Deben ubicarse en `/operations` y no mezclarse con `/registry`.

## 8. Mapeo Lógico a Físico

La ruta lógica es un contrato estable; la ruta física depende del despliegue.

| Logical area | Meaning | Physical mapping examples |
|---|---|---|
| `/registry/skills` | fuentes canónicas de skills | directorio compartido, subdirectorio del repo, ruta montada |
| `/registry/mcp` | definiciones canónicas de MCP | carpeta de config, raíz generada de manifest |
| `/registry/agents` | raíces canónicas de instrucciones de agentes | directorio de perfiles de agentes, biblioteca compartida de prompts |
| `/registry/workflow` | docs de workflow / runbooks | carpeta de workflow, docs locales del proyecto |
| `/operations` | inventories, backups, drift logs | carpeta ops, almacén de estado, directorio de auditoría |
