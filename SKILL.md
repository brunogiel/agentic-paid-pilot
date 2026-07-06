---
name: lanzar-piloto
kind: orchestrator
description: >-
  Orquestador del playbook para validar un negocio/vertical nuevo con un piloto de adquisición pagada (research → landings → campañas Google+Meta → medir con gate de budget). Usar cuando el usuario diga "lancemos un piloto para X", "armemos el paid para inmobiliarias / dentistas / lo que sea", "playbook de campañas para X", "validemos un negocio nuevo con paid", "quiero probar [vertical] con campañas", "arranquemos un piloto de adquisición", "nuevo vertical para validar", "armemos las landings + campañas para X". Es el conductor thin que encadena las child skills de las etapas 0→3; cada child skill también se puede invocar suelta. NO es para operar campañas ya prendidas (eso son los roles de paid media en `roles/`) ni para un negocio que ya está validado.
---

# Playbook: lanzar un piloto de adquisición pagada

> **Rol:** orquestador (`kind: orchestrator`). El eval de los workers es **humano-gateado**: avanza etapa por etapa (0.plan → 1.research → 2.experimento → 3.ejecución) presentando el output de cada child skill y esperando el OK del usuario en cada checkpoint gateado (eso cumple la obligación de eval de la doctrina vía gate humano, no automático).

Molde repetible para validar un vertical/negocio nuevo con un piloto pagado. El proceso es el mismo siempre: **0.plan → 1.research → 2.experimento → 3.ejecución**, con un gate de budget que permite cortar antes de gastar todo. La inteligencia de paid (estructura de campañas, creativos, tracking) la aportan los 6 roles en [`roles/`](roles/); este playbook aporta el **proceso** + la **capa operativa** (scripts, fichas, gate).

## Regla madre — cómo corre este playbook

Este orquestador es **thin, gateado y guía**, no autónomo. Su trabajo #1 es **mantener al usuario orientado** (que no pierda el hilo saltando entre etapas y subagentes):
- **Avanza etapa por etapa.** Presenta el output de cada etapa y **espera el OK del usuario** ("dale") antes de seguir. NO corre las 4 etapas de corrido ni dispara un subagente que devuelve un paquete cerrado (principio: revisar de a uno, no en swarm).
- **Guía en cada parada.** Antes de pedir el OK, emite el bloque "Guía de estado" de abajo: dónde estamos, qué cerramos, qué sigue, qué necesito de vos. Es la brújula del piloto.
- **El usuario lidera lo creativo.** El playbook ejecuta, investiga y propone; las decisiones de ángulo, oferta, segmento, copy y marca las cierra el usuario. Frasear como "armé esto, chequealo" / "¿te parece?", nunca decidir solo.
- **Único fan-out permitido:** dentro de la Etapa 1, las 3 pulls mecánicas independientes (`swipe-ads-competidores`, `sizing-audiencias-meta`, `kw-research-google`) corren en paralelo vía `Agent`, cada una con retorno JSON compacto. El resto es inline.
- **No hay lógica de negocio acá.** Todo el trabajo vive en las child skills; este archivo solo coordina, gatea, guía y loggea (doctrina thin harness / fat skills: el orquestador coordina, los workers hacen).

### Guía de estado — qué emite el orquestador en cada checkpoint

En cada parada (fin de etapa, o cuando el usuario pregunta "¿dónde estamos?"), devolver un bloque corto en criollo que lo oriente sin hacerlo releer todo:

> **📍 Dónde estamos:** Etapa {N} de 4 — {nombre}
> **✅ Qué cerramos:** {1-2 bullets de lo recién hecho + en qué archivo quedó}
> **⏭️ Qué sigue:** {próxima etapa / child skill}
> **🙋 Qué necesito de vos:** {la decisión o input puntual que destraba seguir, o "nada, decime dale y sigo"}

Mantenerlo de 4 líneas. La idea es que el usuario mire ese bloque y sepa exactamente en qué punto del piloto está parado y qué decide ahora.

## Principios — qué palanca mueve la aguja

Antes de obsesionarse con optimizar una etapa, recordar el **orden de impacto real** de las palancas de un piloto. De mayor a menor:

1. **¿El mercado responde a la oferta?** Es lo que el piloto realmente testea. Si no, nada de lo de abajo importa.
2. **Canal (a dónde va el budget).** La decisión más cara del piloto. Ej: LinkedIn ($17-43 CPC) vs Google search ($3-8, intención caliente) vs Meta para un servicio a PyMEs: esa sola asignación mueve más plata que toda la higiene de keywords junta. Se pelea **antes** de repartir budget, no después.
3. **Oferta / posicionamiento** (ángulo, anchor de precio).
4. **Claridad de la landing.** "Linda" importa menos que clara + con prueba. La estética es la palanca más **sobrevalorada** del stack.
5. **Higiene de keywords / negativas.** Plata real, pero es un impuesto de eficiencia (~10-20%), no un multiplicador 2-5x. Segundo orden.

Dos trampas que cuestan caro:

- **Visible ≠ importante.** La plata quemada en keywords malas es contable (la ves en el reporte de términos), entonces se siente como *la* lección del piloto. Pero las decisiones invisibles (canal, oferta, definición de ICP) movieron mucha más guita sin dejar rastro tan obvio. No confundir lo medible con lo que pesa.
- **Matrícula vs impuesto evitable.** Quemar para aprender está bien, pero separar dos tipos de plata quemada: la **matrícula** es plata en lo que no podías saber de antemano (el precio del experimento, inevitable, se paga sí o sí); el **impuesto evitable** son clics en basura que cualquier operador neguea el día cero (jobs/salary/free/course/how-to). La matrícula se paga; el impuesto se evita con la lista tier-1 del día cero (`s1b-kw-research-google`).

## Parámetros (kickoff)

Antes de scaffoldear, cerrar con el usuario:

> La columna "Ej." es ilustrativa (un vertical hipotético: leadgen para un estudio contable local). Reemplazá con los datos de tu piloto.

| Param | Qué es | Ej. (ilustrativo) |
|---|---|---|
| `NEGOCIO` | qué se vende y a quién | leadgen para un estudio contable local |
| `MERCADO/GEO` | dónde, radio | ciudad + 25mi / país entero |
| `IDIOMA(S)` | del copy y las landings | idioma primario + secundario |
| `BUDGET` | total del piloto + quién lo pone + gate inicial | $2.000 (50/50) · gate $200 |
| `QUIÉN CIERRA` | quién atiende/cierra los leads | el partner que presta el servicio |
| `MODELO` | cómo cobramos nosotros | finder's fee 1x retainer / % del cleanup |
| `DEADLINE` | ventana del piloto | 30 días desde el encendido |

### Modo entrevista pre-kickoff (opcional)

Activar cuando el usuario llega con una **idea vaga** o sin vertical definido (no tiene NEGOCIO claro, el ángulo de oferta no está cerrado, o dice "quiero validar algo pero no sé bien qué"). En vez de pedir los params de la tabla de corrido, correr primero una entrevista:

- Preguntar de a **1 por vez**, máx 10 preguntas.
- Empujar cuando la respuesta sea vaga ("¿qué significa 'algo de SaaS'?", "¿quién paga, el que tiene el problema o el dueño del negocio?").
- Objetivo: cerrar NEGOCIO + MODELO antes de tocar los params operativos.
- Solo después de la entrevista, proponer los params de la tabla ya completados para que el usuario confirme.

Triggea con frases como: "tengo una idea para X", "quiero validar algo", "no sé si el ángulo es A o B", "no tenemos NEGOCIO definido todavía".

## Las etapas

| Etapa | Child skills | Output (archivo del proyecto) | Gate |
|---|---|---|---|
| **0 · Plan** | `s0-plan-piloto` | `0.plan.md` + scaffold `1/2/3` | objetivo + budget + quién cierra cerrados |
| **1 · Research** | `s1a-research-mercado`, `s1b-kw-research-google`, `s1c-swipe-ads-competidores`, `s1d-sizing-audiencias-meta` | `1.research.md` + `workspace/research/` | checklist de mercado da AVANZAR |
| **2 · Experimento** | `s2a-modelar-funnel`, `s2b-disenar-experimento` | `2.plan-piloto.md` + `workspace/_backbone.md` | LTV/CAC ≥ 1 en realista + gate de budget definido |
| **3 · Ejecución** | `s3a-copy-landings`, `s3b-build-landings`, `s3c-spec-campanias`, `s3d-creativos-ads`, `s3e-setup-tracking`, `s3f-pre-launch-validation` | `3.ejecucion-piloto.md` + `workspace/` | pre-launch validation en verde → encender Etapa 1 |
| **4 · Operar** (opcional) | punteros a `roles/search-query-analyst` + `roles/campaign-auditor` | — | — |

## Flujo paso a paso

**Paso 0 — Kickoff + scaffold** `[LATENT]`
1. Reunir los parámetros de arriba con el usuario (preguntar lo que falte, no inventar).
2. Invocar `s0-plan-piloto` → crea `{NEGOCIO}/` con `0.plan.md` + `1.research.md` + `2.plan-piloto.md` + `3.ejecucion-piloto.md` + `workspace/` desde `templates/`.
3. Si tu sistema lleva un índice de proyectos, registrar ahí el nuevo `{NEGOCIO}/` para que no quede huérfano.
4. Checkpoint: "armé el scaffold, revisá `0.plan.md`".

**Etapa 1 — Research** `[FANOUT]`
1. Lanzar en paralelo (un `Agent` por skill, retorno JSON): `s1b-kw-research-google`, `s1c-swipe-ads-competidores`, `s1d-sizing-audiencias-meta`.
2. Con esos insumos, correr `s1a-research-mercado` inline (checklist de viabilidad + competitive + síntesis "3 movimientos"). Escribe `1.research.md`.
3. Checkpoint: presentar el veredicto del checklist (AVANZAR / no) + los 3 movimientos. Esperar OK.

**Etapa 2 — Experimento** `[LATENT]`
1. `s2a-modelar-funnel` → modelo CAC/LTV con 4 escenarios (xlsx con fórmulas vivas).
2. `s2b-disenar-experimento` → hipótesis, KPIs/success metrics, **gate de budget**, premortem, y el `_backbone.md` (contrato de invariantes). Escribe `2.plan-piloto.md`.
3. Checkpoint: presentar LTV/CAC + el gate + las hipótesis. Esperar OK.

**Etapa 3 — Ejecución** (secuencial, con checkpoints)
1. `s3a-copy-landings` → copy por landing/idioma → si hay más de un ángulo posible, invocar `copy-battle` para decidir el ganador antes de construir → checkpoint.
2. `s3b-build-landings` → build Stitch→Next/Vercel + motor `?v=` + form + webhook lead.
3. `s3c-spec-campanias` + `s3d-creativos-ads` → spec Google+Meta + RSAs/ads (apoyan en `roles/`).
4. `s3e-setup-tracking` → runbook de cuentas (lo que hace el usuario) + objetos de tracking.
5. `s3f-pre-launch-validation` → punch-list determinística. Solo cuando está en verde: **encender Etapa 1** (gate de budget). Resto del budget = Etapa 2 post-gate.

**Etapa 4 — Operar** (post-encendido, opcional): apuntar a `roles/search-query-analyst.md` (negativos/n-grams c/2-4 sem) y `roles/campaign-auditor.md` (auditoría c/4 sem). No hay skills nuevas.

## Child skills (mapa con paths)

```
s0-plan-piloto/            scaffold + plan/gate/decisiones
s1a-research-mercado/      checklist viabilidad + competitive + síntesis 3 movimientos
s1b-kw-research-google/    Keyword Planner → volúmenes, KW, CPC, negativas
s1c-swipe-ads-competidores/ Meta Ad Library (Apify) → swipe + creatividades   [+scripts]
s1d-sizing-audiencias-meta/ Graph API delivery_estimate → tamaños por capa     [+scripts]
s2a-modelar-funnel/        CAC/LTV, 4 escenarios, Excel fórmulas vivas          [+scripts]
s2b-disenar-experimento/   hipótesis + KPIs + gate de budget + premortem + _backbone
s3a-copy-landings/         copy por vertical/idioma + message-match
s3b-build-landings/        Stitch→Next/Vercel + motor ?v= + form + webhook lead
s3c-spec-campanias/        estructura Google+Meta + fichas MCP/Chrome
s3d-creativos-ads/         RSAs + ads Meta desde el swipe + wedges
s3e-setup-tracking/        runbook cuentas + GA4 + Pixel + conversiones + UTMs
s3f-pre-launch-validation/ punch-list / pre-validador + encendido por gate
```

## Log de corrida

Al final de cada etapa completada, el orquestador appendea una entrada a `runs/{fecha}-{NEGOCIO}.json` dentro de esta carpeta. Formato mínimo:

```json
{
  "run": "YYYY-MM-DD",
  "negocio": "{NEGOCIO}",
  "etapa": 0,
  "child_skills_corridas": ["s0-plan-piloto"],
  "output_paths": ["{NEGOCIO}/0.plan.md"],
  "gate_superado": true,
  "notas": "resumen de 1 línea de lo que cerró la etapa"
}
```

Si la etapa tiene más de una child skill, `child_skills_corridas` lista todas. Si el gate no se superó (el usuario dijo que no), `gate_superado: false` y `notas` explica el motivo.

## Referencias externas

- **Corrida de referencia:** (reemplazá con tu propia corrida de referencia cuando tengas una) — un piloto ya completado end-to-end sirve como el "cómo se hace en la práctica". Leerlo antes de arrancar uno nuevo.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/` | Crea el scaffold (vía `s0-plan-piloto` + `templates/`) |
| Índice de proyectos (si tu sistema lo tiene) | Edita: registra el nuevo proyecto para que no quede huérfano |
| `roles/*` | **Lee** (frameworks de paid media), no escribe |
| `runs/{fecha}-{NEGOCIO}.json` | **Appendea** log de corrida por etapa |

## Output esperado

Un proyecto nuevo en `{NEGOCIO}/` con los 4 docs de etapa poblados, el `workspace/` con los entregables de ejecución (landings + campañas + creativos + tracking), y las campañas de la Etapa 1 armadas en pausa, listas para encender tras el QA.

## Success metrics

- Cada etapa se cerró con OK explícito del usuario antes de pasar a la siguiente (0 etapas saltadas).
- El proyecto quedó registrado en el índice de proyectos (no huérfano).
- Al encender, existe el gate de budget definido y la pre-launch validation está en verde (tracking funcionando E2E).
- Reuso real: ≥1 script o template del playbook se usó tal cual (parametrizado), sin reescribir desde cero.

## Troubleshooting

- **El usuario pide "hacelo todo de una":** igual presentar checkpoints por etapa; ofrecer correr seguido pero sin saltarse la revisión del research ni del gate (ahí es donde se pierde plata).
- **Falta un dato del kickoff:** no inventar (geo, budget, quién cierra). Preguntar; bloquea el scaffold.
- **El vertical no pasa el checklist de mercado (Etapa 1):** parar y decidir con el usuario si se pivotea el ángulo o se descarta, antes de gastar en Etapa 2+.
- **Nesting:** las child skills viven anidadas; si no auto-disparan por frase, invocarlas leyendo su `SKILL.md` por path (este orquestador las cablea).
