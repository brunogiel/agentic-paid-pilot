---
name: plan-piloto
description: >-
  Etapa 0 del playbook lanzar-piloto. Scaffoldea un proyecto de piloto nuevo desde los templates y arranca el plan/status. Usar cuando el usuario diga "scaffoldeá el piloto de X", "armá la estructura del proyecto para X", "arrancá el plan del piloto de inmobiliarias", o cuando el orquestador lanzar-piloto entra a la Etapa 0. Crea los 4 docs de etapa + workspace/ y registra el proyecto en el índice de tu sistema (si tenés uno). NO hace research ni campañas (eso son las etapas 1-3).
---

# Etapa 0 · plan-piloto — scaffold + plan

Primer paso de un piloto nuevo: dejar el proyecto armado y el plan/status arrancado, para que las etapas 1-3 escriban sobre una estructura que ya existe. Es el `0.plan.md` + estructura de carpetas del proyecto (reemplazá con tu propia corrida de referencia).

## Parámetros

Vienen del kickoff del orquestador (si falta alguno, preguntar, no inventar):
- `NEGOCIO` — nombre del proyecto/vertical (define la carpeta).
- `MERCADO/GEO`, `IDIOMA(S)`, `BUDGET` (total + quién + gate inicial), `QUIÉN CIERRA`, `MODELO`, `DEADLINE`.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/` | **Crea** la carpeta + `workspace/` + `workspace/research/` |
| `{NEGOCIO}/{0.plan,1.research,2.plan-piloto,3.ejecucion-piloto}.md` | **Crea** copiando de `lanzar-piloto/templates/` y rellenando params obvios |
| `{NEGOCIO}/workspace/_backbone.md` | **Crea** desde `templates/_backbone.md` (queda casi vacío hasta la Etapa 3) |
| Índice de proyectos (si tu sistema lo tiene) | **Edita** (registra el nuevo proyecto para que no quede huérfano) |
| `templates/*` | **Lee** |

## Flujo

**Paso 1 [DET]:** crear `{NEGOCIO}/` con `workspace/research/` adentro. Copiar los 5 templates (`0/1/2/3` + `_backbone`) a su lugar.

**Paso 2 [LATENT]:** rellenar en cada doc lo que ya se sabe del kickoff: en `0.plan.md` el YAML de etapas (status `todo`/`partial`), la tabla de dependencias críticas, decisiones cerradas del kickoff y la primera fila del Log; en `2.plan-piloto.md` el Contexto + Objetivo + Agreement. El resto queda con `{{placeholders}}` para las etapas siguientes. NO inventar research ni números.

**Paso 3 [DET+LATENT]:** si tu sistema lleva un índice de proyectos, registrar el nuevo ahí para que no quede huérfano:
1. Confirmar que existe `{NEGOCIO}/` (+ `skills/` si va a tener skills propias del proyecto).
2. Agregarlo al índice / mapa de proyectos de tu sistema.
3. Si tu índice tiene una lista de "proyectos activos" o de atajos/frases-gatillo, sumar el nuevo ahí.

**Paso 4:** devolver el bloque "Guía de estado" del orquestador (📍/✅/⏭️/🙋) y el link a `0.plan.md` para que el usuario lo revise.

## Output esperado

`{NEGOCIO}/` con los 4 docs de etapa + `workspace/` poblados de scaffold, el proyecto registrado en tu índice de proyectos (si tenés uno), y `0.plan.md` con objetivo + budget + quién cierra ya cargados.

## Success metrics

- Existen los 4 docs de etapa + `workspace/_backbone.md` (5 archivos creados desde template).
- El proyecto quedó registrado en tu índice de proyectos, si tu sistema lleva uno (no queda huérfano).
- `0.plan.md` tiene objetivo, budget (+ gate) y quién cierra cargados; el resto en `{{placeholder}}` sin inventar.

## Troubleshooting

- **Carpeta con espacios:** si la ruta del proyecto tiene espacios, usar rutas absolutas entre comillas.
- **Ya existe la carpeta:** no pisar; preguntar al usuario si reusa o renombra.
- **No cerrar la tarea** hasta el paso 3 completo: si el proyecto no entra a tu índice, se pierde del mapa.
