---
name: spec-stack
description: >-
  Etapa 2 del playbook lanzar-piloto (entre disenar-experimento y la Etapa 3). Produce el spec de stack del piloto ANTES de construir nada: elige la arquitectura de funnel (del menú reference/arquitecturas-funnel.md), decide qué componentes van con qué proveedor, y arma los journeys + requisitos + spec de tracking. Usar cuando el usuario diga "definamos el stack", "spec del piloto", "qué herramientas vamos a usar", "armame el PRD del funnel", "cerremos la arquitectura antes de buildear". Consume 2.plan-piloto.md + reference/arquitecturas-funnel.md. Escribe 2c.spec-stack.md. Gate duro: nada de s3a-s3f arranca sin este spec aprobado.
---

# Etapa 2 · spec-stack: el PRD del funnel antes de tocar código

Cierra QUÉ se va a construir antes de que arranque la Etapa 3 (copy, landings, campañas, tracking). Es la bisagra entre "decidimos qué apostamos" (`s2b-disenar-experimento`) y "lo construimos" (`s3a` en adelante): sin este spec, cada child skill de la Etapa 3 termina inventando su propia versión de qué componentes usar, con qué proveedor, y el tracking se reconstruye después mirando el código en vez de diseñarse antes.

## Parámetros
- `NEGOCIO` (del kickoff).
- Insumos: `2.plan-piloto.md` completo (objetivo, hipótesis, flujos) + `reference/arquitecturas-funnel.md` (el menú de 6 arquitecturas).

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/2c.spec-stack.md` | **Escribe** (desde `templates/2c.spec-stack.md`) |
| `{NEGOCIO}/2.plan-piloto.md` | **Lee** (objetivo, hipótesis, flujos, ICP) |
| `reference/arquitecturas-funnel.md` | **Lee** (menú de arquitecturas + evidencia real) |
| `reference/infra-y-credenciales.md` | **Lee** (qué credenciales/infra ya existen para reusar, nunca copia valores) |
| `componentes/*/SKILL.md` | **Lee** (menú de stack sugerido de cada componente que entra en la arquitectura elegida) |

## Flujo

**Paso 1 [LATENT]: proponer arquitectura con el porqué.** Leer `2.plan-piloto.md` (tipo de decisión de compra, largo del ciclo, temperatura del tráfico esperado) y cruzarlo contra la tabla de `reference/arquitecturas-funnel.md`. Proponer UNA arquitectura (o una combinación explícita, ver §Regla de combinación del menú) con el porqué citando la columna "Cuándo conviene / Cuándo NO" para este negocio puntual. No dejar la elección implícita ni copiar la de un piloto anterior por default.

**Paso 2 [LATENT]: entrevista corta de decisiones.** Con la arquitectura acordada, recorrer los componentes que exige (según la tabla del menú) y para cada uno cerrar 3 cosas con el usuario: (a) qué componente va, (b) con qué proveedor (usando el menú de stack sugerido de cada `componentes/{X}/SKILL.md`), (c) qué queda pendiente. Regla dura: **lo que no se define en esta entrevista se marca `pendiente` con dueño y fecha en la tabla de Preguntas Abiertas del spec, nunca se deja implícito** para que alguien lo asuma más adelante.

**Paso 3 [DET]: escribir `2c.spec-stack.md`.** Completar el template sección por sección: resumen, arquitectura + porqué, tabla de componentes (componente · decisión · proveedor · estado · notas), 2-3 journeys (happy path + al menos un edge real: no califica, abandona, reincide), requisitos por componente como FRs numerados (capacidades, no implementación, sin adjetivos subjetivos: "el sistema debe capturar el email antes de mostrar el calendario", no "un form simple y rápido"), spec de tracking (evento · cuándo dispara · destino · conversión primaria/secundaria, naming canónico un evento por acción), tabla de credenciales apuntando a `reference/infra-y-credenciales.md` (nunca valores), qué NO incluye este piloto, y preguntas abiertas con dueño y fecha.

**Paso 4 [DET]: gate.** El spec se presenta completo para aprobación explícita antes de que arranque `s3a-copy-landings` o cualquier otro child skill de la Etapa 3. Si el usuario pide arrancar a construir sin este gate, mostrar qué queda sin definir (la tabla de pendientes) y el costo de descubrirlo a mitad de un build en vez de ahora.

**Paso 5:** devolver al orquestador la arquitectura elegida + tabla de componentes + preguntas abiertas, para el checkpoint de fin de Etapa 2.

## Output esperado

`2c.spec-stack.md` completo y aprobado: arquitectura elegida con el porqué, tabla de componentes sin casillas implícitas, 2-3 journeys, FRs numerados por componente, spec de tracking con naming canónico, y tabla de preguntas abiertas con dueño y fecha para todo lo pendiente.

## Success metrics

- Arquitectura elegida explícitamente (o combinación explícita), citando el menú, no copiada de memoria de otro piloto.
- 0 componentes en estado implícito: todos son `definido`, `pendiente` (con dueño+fecha) o `fuera de alcance`.
- Cada evento de tracking tiene destino y si es conversión primaria o secundaria.
- El spec está aprobado ANTES de que cualquier child skill de la Etapa 3 escriba código o toque una cuenta de ads.

## Troubleshooting

- **El usuario quiere arrancar a buildear sin cerrar el spec:** mostrar la tabla de pendientes tal cual está: cuántas filas son `pendiente` sin dueño, y qué child skill de la Etapa 3 se traba si esa fila no se define primero.
- **La arquitectura "obvia" no tiene evidencia real que la respalde:** no es motivo para descartarla, pero sí para marcarla como hipótesis en `2.plan-piloto.md § Hipótesis` en vez de presentarla como decisión cerrada.
- **El negocio no encaja en ninguna de las 6 arquitecturas del menú:** no forzar una; documentar la combinación o variante nueva en el spec igual, citando qué restricción real la generó (ver cierre de `reference/arquitecturas-funnel.md`).
