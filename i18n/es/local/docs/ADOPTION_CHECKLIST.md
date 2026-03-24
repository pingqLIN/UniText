# Checklist de Revisión de Adopción

> Estado: Active
> Uso: define el estándar mínimo de comprobación para el paso `REVIEW` del flujo de adopción.

## Required

- [ ] el nombre del directorio cumple la regla de `id`
- [ ] existe `SKILL.md`
- [ ] `SKILL.md` empieza con frontmatter
- [ ] el frontmatter incluye al menos `name` y `description`
- [ ] `canonical_location` puede corresponder razonablemente a `/registry/{type}/{id}`
- [ ] no hay contenido claramente dañado, vacío o truncado

## Recommended

- [ ] existe `LICENSE.txt` o una nota de licencia equivalente
- [ ] existe una sección clara de Usage, Workflow o Process
- [ ] no hay cuentas personales hardcodeadas ni rutas absolutas locales
- [ ] si hay scripts / referencias, la relación de rutas es clara y un agent puede descubrirla

## Review Outcome

- `approve`
  - puede pasar directamente a `DRY-RUN`
- `needs-fix`
  - hace falta completar metadata o limpiar contenido
- `hold`
  - existe conflicto de canonical source o un problema de calidad de contenido; no puede entrar en `ADOPT`
