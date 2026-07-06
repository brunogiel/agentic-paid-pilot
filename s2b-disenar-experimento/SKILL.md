---
name: disenar-experimento
description: >-
  Etapa 2 del playbook lanzar-piloto. Diseña el experimento del piloto: hipótesis falsables con riesgo asociado, presupuesto y duración, success metrics con umbrales duros, criterios de kill, gate de budget por etapas y premortem. Cierra el contrato de invariantes (_backbone.md). Usar cuando el usuario diga "diseñá el experimento de X", "las hipótesis del piloto", "definí el gate de budget", "criterios de éxito/kill de X", "armá el premortem", "cerrá el plan piloto de X". Consume el modelo de modelar-funnel + tus criterios de evaluación de oportunidades. Escribe 2.plan-piloto.md + workspace/_backbone.md. NO modela números (eso es modelar-funnel) ni ejecuta (Etapa 3).
---

# Etapa 2 · disenar-experimento — hipótesis, gates y contrato

Convierte el piloto en un experimento falsable: qué creemos, cuánta plata arriesgamos para saberlo, con qué umbral decimos "funciona" y con cuál lo matamos. Marco de referencia: *Testing Business Ideas* (Bland & Osterwalder), consultar a demanda para los tipos de experimento y el fit evidencia/costo. (Reemplazá con tu propia corrida de referencia si ya diseñaste un piloto antes.)

## Parámetros
- `NEGOCIO`, `BUDGET` (total + gate inicial), `DEADLINE`, `MODELO`, `QUIÉN CIERRA` (del kickoff).
- Insumos: LTV/CAC + CPL objetivo + CAC máximo de `modelar-funnel`; los 3 movimientos y benchmarks de `1.research.md`.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/2.plan-piloto.md` | **Escribe** (hipótesis, KPIs, gates, premortem, flujos) |
| `{NEGOCIO}/workspace/_backbone.md` | **Escribe** (contrato de invariantes para la Etapa 3) |
| `workspace/research/estimaciones-funnel.md` | **Lee** (umbrales salen del modelo, no se inventan) |
| *Testing Business Ideas* (Bland & Osterwalder) | **Consulta** (tipos de experimento, fit evidencia/costo) |

## Flujo

**Paso 1 [LATENT] — Hipótesis falsables.** 3-5 hipótesis en tabla (hipótesis + riesgo si es falsa). Cada una tiene que ser medible dentro del piloto (CAC razonable, confianza del canal, diferenciador real, close rate). Si una no se puede falsar con este budget/plazo, no va.

**Paso 2 [LATENT] — Success metrics y kill criteria.** Umbrales duros ANTES de arrancar, numéricos, derivados del modelo de `modelar-funnel` (no a ojo): ≥N reuniones/semana, ≥N firmas al día 30, margen > $X, esfuerzo ~N hs/semana. Y los kill: CPL > X en semana 2, fit-rate < X%, booking rate < X%.

**Paso 3 [LATENT] — Gate de budget.** Partir el budget en Etapa 1 (validación top-of-funnel, $gate, qué campañas se prenden, ~N días a dailies bajos) y Etapa 2 (el resto, recién con señal). Definir QUÉ libera el gate (tasas + costo por lead en rango) y qué lo corta.

**Paso 4 [LATENT] — Premortem.** "El piloto falló al día 30, ¿por qué?": 4+ escenarios con señal temprana + cobertura (tabla del template).

**Paso 5 [LATENT] — Backbone.** Volcar a `workspace/_backbone.md` (desde el template) los invariantes que la Etapa 3 hereda sin re-derivar: marca/oferta, CTA único, ICP + floor, verticales IN/OUT, segmentos canónicos, split de budget, regla madre. Lo no definido va como `[ABIERTO: ...]`, nunca inventado.

**Paso 6:** devolver al orquestador hipótesis + umbrales + gate para el checkpoint de fin de Etapa 2.

## Output esperado

`2.plan-piloto.md` completo (contexto, objetivo, hipótesis, KPIs con umbrales, flujos, premortem) y `workspace/_backbone.md` poblado como contrato para `s3a`-`s3f`.

## Success metrics

- Cada hipótesis es falsable dentro del budget/plazo del piloto (0 hipótesis decorativas).
- Umbrales de éxito Y de kill numéricos, trazables al modelo de funnel.
- Gate de budget definido: monto, campañas que prende, criterio de liberación y de corte.
- Backbone sin huecos silenciosos: lo indefinido está como `[ABIERTO]`.

## Troubleshooting

- **El usuario quiere prender todo el budget de una:** el gate existe porque el top-of-funnel se valida barato; mostrar cuánto se pierde si el CPL sale 3x y no hubo gate.
- **Umbrales "razonables" sin número:** no sirven para decidir; forzar el número aunque sea estimación interna marcada.
- **El backbone contradice el research:** manda el backbone (es el contrato); si el hueco es real, flag `[ABIERTO]` y decidir con el usuario, no parchear en silencio.
