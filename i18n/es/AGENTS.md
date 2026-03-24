# AGENTS.md

## Regla de No Publicación

Este repositorio contiene materiales que pueden permanecer privados salvo que el usuario otorgue permiso explícito.

Los agentes que operen en este repositorio DEBEN seguir estas reglas:

1. No enviar commits a ningún remoto salvo que el usuario solicite explícitamente ese `push`.
2. No subir contenido del repositorio a GitHub, plataformas sociales, documentos en la nube, sitios de pegado ni ningún otro servicio de red salvo que el usuario lo pida explícitamente.
3. Tratar como especialmente sensibles por defecto los siguientes contenidos:
   - borradores de publicaciones sociales
   - notas de comparación entre proyectos
   - discusiones de colaboración entre proyectos
   - notas de revisión
   - documentos de estrategia y planificación
4. Si el usuario pide publicar, hacer `push`, subir o publicar, sólo se debe publicar el contenido específico que el usuario haya aprobado.
5. En caso de duda, mantener el contenido local y preguntar antes de publicar.

## Nota de Alcance

Esta política aplica incluso cuando:

- ya existe un remoto
- el repositorio es privado
- el contenido parece listo para publicarse

Que el repositorio sea privado no equivale a permiso automático para publicar.

## JavaScript REPL (Node)
- Usa `js_repl` para JavaScript con Node y `top-level await` en un kernel persistente.
- `js_repl` es una herramienta libre/personalizada. Las llamadas directas a `js_repl` deben enviar JavaScript sin formato bruto (opcionalmente con la primera línea `// codex-js-repl: timeout_ms=15000`). No envíes JSON (por ejemplo `{"code":"..."}`), comillas ni fences de Markdown.
- Helpers: `codex.cwd`, `codex.homeDir`, `codex.tmpDir`, `codex.tool(name, args?)` y `codex.emitImage(imageLike)`.
- `codex.tool` ejecuta una llamada normal a herramientas y resuelve al objeto bruto de salida. Úsalo para herramientas con o sin shell. Las salidas anidadas se mantienen dentro de JavaScript salvo que las emitas explícitamente.
- `codex.emitImage(...)` agrega una imagen al output externo de `js_repl` cada vez que la llamas, así que puedes llamarla varias veces para emitir varias imágenes. Acepta un data URL, un solo ítem `input_image`, un objeto como `{ bytes, mimeType }` o una salida de herramienta cruda con exactamente una imagen y sin texto. Rechaza contenido mixto de texto e imagen.
- `codex.tool(...)` y `codex.emitImage(...)` conservan identidades estables entre celdas. Las referencias guardadas y objetos persistidos pueden reutilizarse en celdas posteriores, pero los callbacks asíncronos que se ejecuten después de que una celda termine seguirán fallando porque no hay una ejecución activa.
- Solicita procesamiento de imagen en máxima resolución con `detail: "original"` sólo cuando el esquema de `view_image` incluya el argumento `detail`. La misma disponibilidad aplica a `codex.emitImage(...)`: si `view_image.detail` está presente, también puedes pasar `detail: "original"` allí. Úsalo cuando necesites percepción visual de alta fidelidad o localización precisa, especialmente para agentes CUA.
- Ejemplo de compartir una captura de Playwright en memoria: `await codex.emitImage({ bytes: await page.screenshot({ type: "jpeg", quality: 85 }), mimeType: "image/jpeg", detail: "original" })`.
- Ejemplo de compartir el resultado de una herramienta de imagen local: `await codex.emitImage(codex.tool("view_image", { path: "/absolute/path", detail: "original" }))`.
- Al codificar una imagen para enviar con `codex.emitImage(...)` o `view_image`, prioriza JPEG con calidad aproximada de 85 cuando la compresión con pérdida sea aceptable; usa PNG cuando la transparencia o el detalle sin pérdida importen. Los uploads más pequeños son más rápidos y tienen menos probabilidades de alcanzar límites de tamaño.
- Las variables de nivel superior persisten entre celdas. Si una celda falla, las bindings previas suelen seguir disponibles y las bindings que terminaron de inicializar antes del fallo a menudo siguen siendo utilizables en celdas posteriores. Para el código que quieras reutilizar entre celdas, prefiere declararlo o asignarlo en sentencias de nivel superior directas antes de operaciones que puedan fallar. Si te encuentras con `SyntaxError: Identifier 'x' has already been declared`, reutiliza primero la binding existente, reasigna una `let` ya declarada o elige un nuevo nombre descriptivo. Usa `{ ... }` sólo como bloque temporal corto cuando necesites nombres de prueba locales; no envuelvas una celda completa en un bloque si quieres que esos nombres sigan siendo reutilizables después. Reinicia el kernel con `js_repl_reset` sólo cuando necesites un estado limpio.
- Las declaraciones `import` estáticas de nivel superior (por ejemplo `import x from "./file.js"`) no están soportadas actualmente en `js_repl`; usa imports dinámicos con `await import("pkg")`, `await import("./file.js")` o `await import("/abs/path/file.mjs")`. Los módulos locales importados deben ser `.js`/`.mjs` ESM y ejecutarse en el mismo contexto de VM del REPL. Los imports de paquetes sin prefijo siempre se resuelven desde los roots globales del REPL (`CODEX_JS_REPL_NODE_MODULE_DIRS`, luego cwd), no relativos a la ubicación del archivo importado. Los archivos locales sólo pueden importar estáticamente otros archivos locales relativos/absolutos/`file://` `.js`/`.mjs`; los imports de paquetes y builtins desde archivos locales deben seguir siendo dinámicos. `import.meta.resolve()` devuelve cadenas importables como `file://...`, nombres de paquetes sin prefijo y especificadores `node:...`. Los módulos de archivos locales se recargan entre ejecuciones, mientras que las bindings de nivel superior persisten hasta `js_repl_reset`.
- Evita el acceso directo a `process.stdout` / `process.stderr` / `process.stdin`; puede corromper el protocolo JSON por líneas. Usa `console.log`, `codex.tool(...)` y `codex.emitImage(...)`.
