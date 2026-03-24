# UniText — Directrices para el Manejo de Secretos

> Estado: Draft  
> Rol: definir los límites de almacenamiento, los principios operativos y la forma de documentar password, API key, token, credential y otro sensitive material dentro de UniText.

## 1. Propósito

Este documento responde a:

- qué datos cuentan como secret
- dónde no deben almacenarse los secrets
- cómo registrar en UniText la “ubicación” y el “estado”
- cuándo puede ir algo en la config de una CLI y cuándo debe pasar a OS secret store o a un native helper

Este documento no ofrece una implementación final para un producto concreto; define el límite de gobernanza que UniText debe respetar.

## 2. Definición de Secret

Los siguientes contenidos se consideran siempre `secret` o `sensitive material`:

- password
- passphrase
- API key
- access token
- refresh token
- session token
- private key
- OAuth client secret
- cookie / session credential
- cualquier bearer credential que pueda representar la identidad del usuario o del sistema

Los siguientes elementos normalmente no son secret, pero aún pueden ser sensitive metadata:

- endpoint URL
- model name
- provider name
- account email
- feature toggle state
- estado de `key exists / missing`
- fecha de última actualización de la key

## 3. Principio Central

El principio básico de UniText es:

1. `registry/` no almacena secrets
2. `ops/` no registra secrets reproducibles
3. `local/` sólo permite registrar path / adapter / deployment notes, pero no secrets en texto plano
4. El secret real debe ir primero a un OS-level secret store
5. Si a corto plazo no se puede usar un OS secret store, al menos hay que separar el secret de la configuración general

En resumen:

- `registry` es shared truth, no un secret vault
- `ops` es audit trail, no un credential archive
- `local` es una capa de wiring, no un stash de texto plano

## 4. Política de Almacenamiento por Capa

| Layer | Can store secret? | Guidance |
|---|---|---|
| `registry/` | No | Sólo puede guardar definiciones canónicas, schema, hints de adapter y metadata de recursos |
| `ops/` | No | Sólo puede guardar logs redactados, metadata de backup, drift report e inventory state |
| docs de `local/` | No | Puede registrar el tipo de ubicación del secret, pero no el secret en sí |
| CLI config | Conditional | Sólo si esa CLI sólo admite secretos basados en config y el riesgo es aceptable |
| OS secret store | Yes | Opción preferida; por ejemplo Windows DPAPI / Credential Manager, macOS Keychain, Linux Secret Service |
| in-memory session | Yes | Aceptable como material de runtime desencriptado a corto plazo, pero no como única fuente persistente |

## 5. Patrones Aprobados

### 5.1 Mejor Patrón

Adecuado para extensiones comerciales, herramientas de escritorio y adapters cross-CLI:

- la configuración no sensible vive en una config / storage normal
- el secret vive en un OS secret store
- al iniciar el runtime, el secret se inyecta a la memoria del proceso
- la UI sólo muestra `stored / missing / last updated`, sin rellenar texto plano

### 5.2 Fallback Aceptable

Si todavía no existe integración con OS secret store:

- cada provider / account debe almacenar su secret por separado
- el secret debe estar separado de la configuración general
- content script / renderer / untrusted context no debe leerlo directamente
- audit y export sólo deben mostrar estado redactado
- la documentación debe marcarlo como `interim storage model`

### 5.3 No Aceptable

Los siguientes patrones no deben considerarse válidos para UniText:

- escribir la API key dentro de `registry/`
- escribir el token dentro de `ops/history/`
- pegar ejemplos de keys completas en notas de despliegue
- mezclar secrets con configuración general sin redaction
- empaquetar secrets reales en review package o template package

## 6. Reglas para Registrar Ubicaciones

La documentación puede registrar “en qué capa vive el secret”, pero no su valor.

Se permite registrar ejemplos como:

- `Windows Credential Manager`
- `DPAPI-protected local secret file`
- `%USERPROFILE%\\.codex\\config.toml` para ajustes no secretos
- `chrome.storage.local` sólo para settings no secretos del provider
- `chrome.storage.session` para material de runtime de corta vida

No se permite registrar:

- un token completo
- una API key completa
- un header Authorization completo
- un cookie reutilizable de forma directa

## 7. Reglas de Documentación

Cuando un documento necesite mencionar secret handling, debe seguir:

1. registrar sólo la clase de storage, no el valor real
2. registrar sólo ejemplos redactados
3. si el ejemplo es inevitable, usar falsos valores claros, por ejemplo:

```text
OPENAI_API_KEY=sk-example-redacted
Authorization: Bearer token-example-redacted
```

4. si un sistema sólo puede usar un modo débil por ahora, el documento debe indicar:
   - que es una solución temporal
   - cuál es el riesgo conocido
   - cuál es la ruta de mejora prevista

## 8. Reglas de Auditoría y Exportación

Cualquier review package, template package, export de inventario o snapshot de ops debe:

- eliminar el valor del secret
- eliminar credential reutilizable
- conservar sólo el estado necesario y redactado

Se puede conservar:

- nombre del provider
- endpoint
- `key exists / missing`
- scope o label de la key
- fecha de última rotación
- tipo de backend de almacenamiento

## 9. Escalera de Recomendación

El orden de preferencia de UniText para almacenar secrets es:

1. `OS secret store`
   - Windows: DPAPI / Credential Manager
   - macOS: Keychain
   - Linux: Secret Service / keyring
2. `native helper / native messaging host`
   - cuando la CLI o la extensión no pueden persistir el secret de forma segura directamente
3. `separated local secret store`
   - separado de la config general y no legible por untrusted contexts
4. `runtime session only`
   - como apoyo, no como única estrategia de persistencia a largo plazo

## 10. Checklist Mínimo

Antes de añadir cualquier recurso o adapter que vaya a manejar secretos, confirma al menos:

- si el secret está excluido de `registry/`
- si el secret está excluido de `ops/`
- si la documentación sólo registra location / state y no el valor
- si el export / review package incluye redaction
- si ya se documentó el backend de almacenamiento usado
- si ya se documentó la ruta de mejora

## 11. Guía Práctica para Browser Extensions

En escenarios tipo browser extension:

- la configuración del provider puede vivir en la storage local de la extensión
- la API key no debería mezclarse con la configuración general del provider en un solo valor compartido
- cada provider debe tener su propio secret
- la UI debe soportar borradores por etapas; no debe perder la key por cambiar de provider o por hover/collapse
- si se quiere un nivel de seguridad más alto, conviene usar native host + OS secret store en lugar de depender sólo de extension storage

## 12. Posición Actual de UniText

Hasta ahora, la postura formal de UniText sobre secret handling es:

- el canonical registry no almacena secrets
- el local overlay puede registrar el backend del secret y el tipo de ruta
- los artefactos de operations deben ir redactados
- si una integración todavía no usa OS secret store, debe marcarse explícitamente como `interim model`

Este documento debe entenderse como:

- guía de authoring
- referencia para review checklist
- baseline para futuras integraciones de adapter / secret-store
