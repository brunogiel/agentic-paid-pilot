---
name: lanzar-piloto
kind: orchestrator
description: >-
  Orquestador del playbook para validar un negocio/vertical nuevo con un piloto de adquisición pagada (research → landings → campañas Google+Meta → medir con gate de budget → operar → cerrar). Usar cuando el usuario diga "lancemos un piloto para X", "armemos el paid para inmobiliarias / dentistas / lo que sea", "playbook de campañas para X", "validemos un negocio nuevo con paid", "quiero probar [vertical] con campañas", "arranquemos un piloto de adquisición", "nuevo vertical para validar", "armemos las landings + campañas para X", "cómo venimos con el piloto de X", "cerremos el piloto de X". Es el conductor thin que encadena las child skills de las etapas 0→4; cada child skill también se puede invocar suelta. La Etapa 4 (operar gates + postmortem) es parte del playbook, no un anexo opcional: un piloto encendido sin gates operados y sin cierre formal no está terminado. NO es para operar campañas de un negocio ya validado y estable (eso es el kit de `roles/` suelto, que la Etapa 4 igual consume como herramienta).
---

# Playbook: lanzar un piloto de adquisición pagada

> **Rol:** orquestador (`kind: orchestrator`). El eval de los workers es **humano-gateado**: avanza etapa por etapa (0.plan → 1.research → 2.experimento → 3.ejecución → 4.operación) presentando el output de cada child skill y esperando el OK del usuario en cada checkpoint gateado (eso cumple la obligación de eval de la doctrina vía gate humano, no automático).

Molde repetible para validar un vertical/negocio nuevo con un piloto pagado. El proceso es el mismo siempre: **0.plan → 1.research → 2.experimento → 3.ejecución → 4.operación**, con un gate de budget que permite cortar antes de gastar todo y una etapa de operación/cierre que evita que el aprendizaje se pierda cuando el piloto termina. La inteligencia de paid (estructura de campañas, creativos, tracking) la aportan los 6 roles en [`roles/`](roles/); este playbook aporta el **proceso** + la **capa operativa** (scripts, fichas, gate, operación post-encendido).

## Regla madre — cómo corre este playbook

Este orquestador es **thin, gateado y guía**, no autónomo. Su trabajo #1 es **mantener al usuario orientado** (que no pierda el hilo saltando entre etapas y subagentes):
- **Avanza etapa por etapa.** Presenta el output de cada etapa y **espera el OK del usuario** ("dale") antes de seguir. NO corre las 4 etapas de corrido ni dispara un subagente que devuelve un paquete cerrado (principio: revisar de a uno, no en swarm).
- **Guía en cada parada.** Antes de pedir el OK, emite el bloque "Guía de estado" de abajo: dónde estamos, qué cerramos, qué sigue, qué necesito de vos. Es la brújula del piloto.
- **El usuario lidera lo creativo.** El playbook ejecuta, investiga y propone; las decisiones de ángulo, oferta, segmento, copy y marca las cierra el usuario. Frasear como "armé esto, chequealo" / "¿te parece?", nunca decidir solo.
- **Único fan-out permitido:** dentro de la Etapa 1, las 3 pulls mecánicas independientes (`swipe-ads-competidores`, `sizing-audiencias-meta`, `kw-research-google`) corren en paralelo vía `Agent`, cada una con retorno JSON compacto. El resto es inline.
- **No hay lógica de negocio acá.** Todo el trabajo vive en las child skills; este archivo solo coordina, gatea, guía y loggea (doctrina thin harness / fat skills: el orquestador coordina, los workers hacen).

### Guía de estado — qué emite el orquestador en cada checkpoint

En cada parada (fin de etapa, o cuando el usuario pregunta "¿dónde estamos?"), devolver un bloque corto en criollo que lo oriente sin hacerlo releer todo:

> **📍 Dónde estamos:** Etapa {N} de 5 (0-4) — {nombre}
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
6. **Kill criteria acordados ANTES de prender, no al cerrar.** Un piloto real improvisó el veredicto de cierre de un gate al final porque el kill criteria original era solo un techo de presupuesto. Definir con el partner qué número mata/pausa/escala un gate es parte del diseño del experimento (`s2b-disenar-experimento`), no algo que se resuelve en caliente cuando la plata se acaba (`s4a-operar-gates`).

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
| **4 · Operación y cierre** | `s4a-operar-gates`, `s4b-postmortem` | `workspace/operacion-gates.md` + `entregables/reportes-{cadencia}/` + `postmortem.md` | veredicto de gate (seguir/pivotar/matar) → si mata o valida del todo, cierre con checklist operativo en verde |

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

**Etapa 4 — Operación y cierre** (post-encendido, parte del playbook, no anexo)
1. Antes de encender: verificar que `2.plan-piloto.md § Kill criteria y condiciones de relanzamiento` esté cerrado (viene de `s2b`, ver su patch). Sin esto, `s4a-operar-gates` no arranca.
2. `s4a-operar-gates` → setup del ciclo del gate, reporte periódico "cómo venimos" (12 reglas destiladas de la operación de un piloto real), comunicación con partners, manejo de leads, y la decisión de gate al agotar presupuesto (seguir/pivotar/matar). Dentro de este paso, invoca `roles/search-query-analyst.md` (negativos/n-grams c/2-4 sem) y `roles/campaign-auditor.md` (auditoría c/4 sem) como herramientas de optimización, no como sub-etapas propias.
3. Si el veredicto es **pivotar**: `s4a-operar-gates` Paso 6 opera el relanzamiento (A/B externo coherente, nunca split interno con los mismos ads) y el playbook vuelve a un gate nuevo (Paso 1 de esta etapa otra vez).
4. Si el veredicto es **matar** o el piloto llegó a su fin natural (deadline, decisión de negocio): `s4b-postmortem` → postmortem canónico + revisión con lentes distintas + checklist de cierre operativo (pausar gasto, apagar bots, rotar credenciales, archivar) + destilado de aprendizajes a sus destinos (playbook / docs propios / memoria / próximo piloto).
5. Checkpoint: presentar el veredicto del gate y, si corresponde, el postmortem. Esperar OK del usuario antes de dar el piloto por cerrado.

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
s4a-operar-gates/          kill criteria + reporte periódico + comunicación partners + relanzamiento
s4b-postmortem/            postmortem canónico + revisión con lentes distintas + checklist de cierre + destilado
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

**Extensión para Etapa 4 (gates operados/cerrados):** al cerrar un gate (`s4a-operar-gates` Paso 5) o el piloto entero (`s4b-postmortem`), la entrada suma campos propios de esa etapa, sin romper el schema base:

```json
{
  "run": "YYYY-MM-DD",
  "negocio": "{NEGOCIO}",
  "etapa": 4,
  "child_skills_corridas": ["s4a-operar-gates"],
  "output_paths": ["{NEGOCIO}/workspace/operacion-gates.md"],
  "gate_superado": false,
  "gate": "Gate N",
  "presupuesto_ejecutado_pct": 92,
  "veredicto_gate": "1 línea con el veredicto (seguir/pivotar/matar) + el número que lo sostiene",
  "notas": "resumen de 1 línea de lo que pasó al cerrar este gate"
}
```

## Referencias externas

- **Corrida de referencia:** (reemplazá con tu propia corrida de referencia cuando tengas una) — un piloto ya completado end-to-end (incluidas las Etapas 0-4: research, ejecución, operación y cierre) sirve como el "cómo se hace en la práctica". Leerlo antes de arrancar uno nuevo.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/` | Crea el scaffold (vía `s0-plan-piloto` + `templates/`) |
| Índice de proyectos (si tu sistema lo tiene) | Edita: registra el nuevo proyecto para que no quede huérfano |
| `roles/*` | **Lee** (frameworks de paid media), no escribe |
| `runs/{fecha}-{NEGOCIO}.json` | **Appendea** log de corrida por etapa (incluida Etapa 4) |

## Output esperado

Un proyecto nuevo en `{NEGOCIO}/` con los docs de las etapas 0-3 poblados, el `workspace/` con los entregables de ejecución (landings + campañas + creativos + tracking), las campañas de la Etapa 1 armadas en pausa listas para encender tras el QA, y, una vez encendido, el ciclo de operación de gates corriendo (`workspace/operacion-gates.md` + reportes periódicos) hasta el cierre formal (`postmortem.md` + checklist de cierre operativo en verde).

## Success metrics

- Cada etapa se cerró con OK explícito del usuario antes de pasar a la siguiente (0 etapas saltadas).
- El proyecto quedó registrado en el índice de proyectos (no huérfano).
- Al encender, existe el gate de budget definido (con kill criteria explícitos, no solo un techo de presupuesto) y la pre-launch validation está en verde (tracking funcionando E2E).
- Reuso real: ≥1 script o template del playbook se usó tal cual (parametrizado), sin reescribir desde cero.
- Ningún gate se cerró sin veredicto explícito en `runs/`, y ningún piloto terminado quedó sin postmortem + checklist de cierre operativo.

## Troubleshooting

- **El usuario pide "hacelo todo de una":** igual presentar checkpoints por etapa; ofrecer correr seguido pero sin saltarse la revisión del research ni del gate (ahí es donde se pierde plata).
- **Falta un dato del kickoff:** no inventar (geo, budget, quién cierra). Preguntar; bloquea el scaffold.
- **El vertical no pasa el checklist de mercado (Etapa 1):** parar y decidir con el usuario si se pivotea el ángulo o se descarta, antes de gastar en Etapa 2+.
- **El usuario quiere prender el gate ya, sin cerrar kill criteria:** no saltar `s2b § Kill criteria`; mostrarle el costo de decidir en caliente (así se improvisó el cierre de un gate en un piloto real) y, si el tiempo apremia, ofrecer un kill criteria mínimo de una línea antes de encender.
- **Un piloto quedó "cerrado" de palabra pero sigue gastando o corriendo bots:** no dar la etapa por completa hasta que `s4b-postmortem § Checklist de cierre operativo` esté en verde. Un gasto residual indefinido, aunque sea de pocos dólares por día, no es un detalle menor, es un piloto que no cerró.
- **Nesting:** las child skills viven anidadas; si no auto-disparan por frase, invocarlas leyendo su `SKILL.md` por path (este orquestador las cablea).
