# UniText — Modos del Proyecto

> Estado: Template Base
> Propósito: distinguir entre el repo de authoring y el starter/template ofrecido al exterior.

## 1. Dos Modos

### Proyecto de Desarrollo Local

Se usa para que el autor siga desarrollando, adoptando, corrigiendo y gobernando.

Puede incluir:

- inventories
- backups
- drift logs
- migration artifacts
- notas específicas de plataforma

### Project Template

Se usa para que otras personas inicialicen su propia instancia de `UniText`.

Debe incluir:

- contratos lógicos
- documentos centrales
- ejemplos mínimos
- reglas agnósticas a la plataforma

No debe incluir:

- rutas absolutas de la máquina local
- huellas de uso personal
- snapshots de backup
- historial de drift
- valores por defecto de un despliegue concreto

## 2. Regla Práctica

Si un contenido está describiendo:

- `cómo debería funcionar UniText`
  - entonces encaja mejor en `Project Template`
- `cómo está configurado el workspace del autor ahora mismo`
  - entonces encaja mejor en `Local Development Project`

## 3. Regla de Publicación

Cuando se publica un template:

1. conservar los documentos centrales y los examples seguros para template
2. eliminar los artefactos de estado local
3. eliminar valores de rutas locales, cuentas o máquinas específicas
4. reescribir la reference implementation como ejemplos abstractos
