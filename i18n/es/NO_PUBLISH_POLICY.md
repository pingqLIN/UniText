# UniText — Política de No Publicación

> Estado: Active
> Propósito: definir qué contenido no debe enviarse, subirse o publicarse en ningún servicio de red sin permiso explícito.

## 1. Regla Principal

Salvo autorización explícita del usuario, el siguiente contenido no debe enviarse, subirse, publicarse ni sincronizarse a ningún servicio de red:

- `git push` a GitHub
- publicaciones en plataformas sociales
- documentos en la nube
- servicios de paste
- cualquier API o servicio de hosting de terceros

## 2. Contenido Sensible por Defecto

El siguiente contenido se considera no publicable por defecto:

- borradores de publicaciones sociales
- comparaciones o discusiones de colaboración entre proyectos
- notas de revisión
- documentos de estrategia / roadmap / planificación
- direcciones de diseño que todavía no se hayan anunciado formalmente

## 3. Estándar de Permiso

La condición mínima para publicar es:

- que el usuario indique de forma explícita que se puede publicar
- si sólo autoriza una parte, sólo se puede publicar esa parte
- `private repo` no equivale a permiso automático para publicar

## 4. Regla para Agentes

Todos los agentes en este repo deben seguir:

1. No hacer `git push` sin permiso explícito.
2. No pegar contenido en redes sociales ni en ningún servicio externo sin permiso explícito.
3. Si el usuario sólo autoriza crear un remote o crear un repositorio privado, no asumir que eso autoriza a subir otros contenidos sensibles.
4. Si el contenido toca relaciones con otros proyectos, discusiones estratégicas o textos sociales, aplicar un criterio más conservador.

## 5. Temas Marcados Como Especialmente Sensibles

Hasta ahora, los siguientes tipos de contenido deben tratarse con especial cautela:

- social post drafts
- `SKILL0_COLLABORATION_VISION.md`
- cualquier otra discusión estratégica relacionada con `skill-0` o con revisiones externas

## 6. Interpretación Operativa

Si en el futuro hace falta publicar algo, conviene dividir el proceso en tres pasos:

1. Confirmar el alcance exacto permitido
2. Confirmar el destino permitido
3. Sólo entonces ejecutar `push` / upload / posting

