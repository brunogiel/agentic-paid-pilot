---
name: operar-gates
description: >-
  Etapa 4 del playbook. Opera un piloto YA encendido: define kill
  criteria antes de prender cada gate, arma el reporte periódico "cómo venimos"
  al partner, maneja la comunicación con partners (4 baldes), valida el interés
  de un lead antes del hand-off, decide qué pasa cuando el gate agota su
  presupuesto (seguir/pivotar/matar) y opera el modo relanzamiento. Usar cuando
  el usuario diga "cómo venimos con X", "reporte del piloto", "prendé el gate
  de X", "se terminó el presupuesto del gate, qué hacemos", "hay que avisarle
  al partner", "el lead respondió, quién lo atiende", "relancemos X con otro
  ángulo", "armá el A/B de concepto de X", "revisá el prompt de la tarea
  programada de X". Consume `roles/search-query-analyst.md` y
  `roles/campaign-auditor.md` como herramientas de optimización dentro del
  ciclo de reporte, no como reemplazo. Escribe workspace/operacion-gates.md +
  entregables/reportes-{cadencia}/. NO diseña el gate (eso es
  disenar-experimento) ni escribe el cierre del piloto (eso es postmortem).
---

# Etapa 4 · operar-gates: el piloto ya está encendido, ahora hay que operarlo

Todo lo que pasa entre "encendimos las campañas" y "se acabó el presupuesto
del gate". El playbook terminaba en `s3f-pre-launch-validation`; esta etapa
cierra el hueco: la operación real de un piloto vivo (varias corridas de un
reporte periódico + varias sesiones de comunicación con el partner) suele
resolverse ad-hoc, decidiendo sobre la marcha cosas que deberían haber estado
cerradas antes de prender. Destilado de la operación de un piloto de leadgen
real ya cerrado (reemplazá esta referencia por tu propia corrida cuando
tengas una).

## Parámetros

- `NEGOCIO`, gate activo (nombre/número, ej. "Gate 4"), presupuesto del gate + fecha de baseline.
- `QUIÉN CIERRA` (partner que atiende leads), `CADENCIA` de reporte (diario / semanal), destinatario del reporte.
- Del backbone: CRM destino, canales activos (Google / Meta / ambos), CTA único.

## Prerequisitos

- `workspace/_backbone.md` cerrado y `2.plan-piloto.md` con la sección **Kill criteria y condiciones de relanzamiento** completa (viene de `s2b-disenar-experimento`, ver su patch). Sin kill criteria explícitos ANTES de prender, no arrancar esta etapa: volver a `s2b` primero.
- `s3f-pre-launch-validation` en verde (tracking funcionando, campañas cargadas).
- Acceso a las fuentes de datos del gate (Meta Graph API / Google Ads / GA4 / CRM del negocio).

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/workspace/operacion-gates.md` | **Escribe** (desde `templates/4.operacion-gates.md`: tabla de gates, baseline, kill criteria, veredicto, log de reportes) |
| `entregables/reportes-{cadencia}/{fecha}-como-venimos.md` | **Escribe** (un archivo por corrida, ANTES de tocar el draft) |
| Draft de mail al partner | **Escribe** (nunca envía, deja el draft) |
| `workspace/_backbone.md` | **Lee** (CTA, CRM destino, canales activos) |
| `2.plan-piloto.md § Kill criteria` | **Lee** (qué mata/pausa/escala este gate) |
| `roles/search-query-analyst.md` + `roles/campaign-auditor.md` | **Lee/invoca** como herramienta de optimización dentro del ciclo (negativos, auditoría de cuenta) |

## Flujo

**Paso 1 [LATENT]: Setup del ciclo al prender un gate.** Antes de encender, cerrar con el partner (no después, no a mitad de camino):
- **Kill criteria explícitos**: qué número mata el gate (ej. "$X gastados con 0 agendas ICP"), qué lo pausa parcialmente, qué lo escala. Viene ya definido de `2.plan-piloto.md § Kill criteria`; acá se confirma que el partner lo vio y lo acepta ANTES de que la plata empiece a salir. Si `2.plan-piloto.md` no tiene esta sección poblada, no seguir: volver a `s2b`.
- **Baseline del gate**: fecha de encendido = fecha 0 de medición. Todo gasto/lead anterior a esa fecha queda comprimido en un bloque histórico, nunca mezclado con la lectura del gate vigente (ver regla 5 del Paso 2).
- **Cadencia de reporte** acordada con el partner (diario si el gate es corto y caliente, semanal si es largo o de bajo volumen).
- Volcar los tres a `workspace/operacion-gates.md` (usar `templates/4.operacion-gates.md`).

**Paso 2 [DET]: El reporte periódico "cómo venimos".** Este es el corazón operativo de la etapa; en un piloto real este reporte corrió muchas veces sin romperse siguiendo estas 12 reglas. Aplicarlas todas, no un subset:

1. **`.md` antes que draft.** Guardar el reporte completo como archivo en `entregables/reportes-{cadencia}/` ANTES de tocar cualquier draft de mail. Es la fuente de revisión; el mail es el segundo paso.
2. **Chequeo de continuidad.** Abrir el reporte de la corrida anterior antes de escribir el propio: copiar formato/tono, cruzar que los números no cambiaron si no debían, usar el "último dato conocido" de un canal que degradó ese día.
3. **Degradación elegante, nunca abortar.** Si una fuente (navegador, API) falla, entregar igual con lo que sí está firme + una línea de aviso. El reporte sale en cada corrida, pase lo que pase con una sola fuente.
4. **El CRM propio desempata SIEMPRE.** Pixel/GA4/analytics de plataforma son orientativos (subregistran por bloqueo de IAB, ad blockers, atribución IAB→Direct); el conteo oficial de leads/agendas es el CRM del negocio. Nombrar las tres fuentes en la redacción cuando discrepan, no solo la que gana.
5. **Denominador = solo desde la baseline del gate vigente.** Todo lo anterior (gates cerrados, relanzamientos previos) va comprimido en un bloque Histórico/Referencia al final, con un TOTAL entero del piloto como contexto. Nunca mezclar gates en la tabla principal.
6. **Ritmo forward, no promedio acumulado÷días.** Usar el gasto diario vigente para proyectar cuándo se toca el techo del gate. El promedio arrastra el ramp-up lento del arranque y subestima cuánto falta (en un piloto real esto cambió la proyección de cierre de "fin de mes" a "la semana que viene").
7. **Nurture por personas, no por envíos.** Si hay un canal de email nurture, contar personas únicas en la cadena + cuántas abrieron/hicieron clic al menos una vez. Los agregados de la mayoría de los ESPs cuentan eventos, no gente; excluir siempre los mails de prueba internos del conteo.
8. **CTR/CPC sobre link clicks, comparable entre canales.** El CTR "de anuncio" de Meta (que suma reacciones, expandir texto, clicks a perfil) infla 3-4x contra el CTR real de tráfico al sitio. Usar link clicks como base de comparación entre Google y Meta; el CTR inflado va de footnote nomás.
9. **Filtro anti-tests en el CRM.** Excluir del conteo cualquier lead sin UTM/Source real (tests internos, flujos de QA, direcciones tipo `+test`) antes de reportar.
10. **Chequear el dominio antes de llamar "caliente" a un lead** con engagement raro en el nurture. Puede ser un competidor haciendo research (dominio de una firma del mismo rubro), no un prospecto real.
11. **El primer email de un gate nuevo lleva un bloque "Estado" especial**, distinto del gestalt de números de los días siguientes: qué se prendió, por qué, y si hay creativos nuevos, una foto de cada uno. A partir del segundo reporte, el Estado vuelve al gestalt normal.
12. **Leads (captura) vs Agendas (cierre) van separados.** CPL = gasto ÷ leads capturados (señal de tope de embudo). CPA = gasto ÷ agendas (la métrica que decide el gate). Reportar los dos, pero el veredicto del gate lo da el CPA, no el CPL.

**Paso 3 [LATENT]: Comunicación con partners.** Formato que sostuvo múltiples intercambios sin fricción en un piloto real:
- **4 baldes fijos**: tareas / decisiones tomadas / decisiones pendientes / preguntas para terceros, con IDs estables por ítem (T#, D#, P#, E#) y una tabla de ruteo (item → tipo → destino). El partner responde en bloque ("T1 a T17 ok, ajusto que...") en vez de tener que releer todo.
- **Cruzar reunión + mails posteriores explícitamente.** Si hubo una reunión y después un mail sobre el mismo tema, señalar el choque entre ambos en vez de resolverlo solo ("la reu decía X, el mail dice Y, ¿cuál priorizamos?"). No decidir en silencio cuál manda.
- **Demo real, no descripción.** Para validar cómo se ve algo antes de mandarlo (un mail de reachout, un ad nuevo), mandar la pieza real al partner en vez de solo describirla.
- **Update al cliente final sin detalle interno.** Si hay un tercer actor (el cliente del partner, ej. quien atiende los leads en el día a día), la cadencia de update a esa persona explica el resultado sin exponer mecanismos internos del sistema de nurture/tracking.
- **Explicitar qué se resolvió y qué se dejó afuera a propósito** en cada cierre de intercambio, incluso cuando el fix ya está hecho, para que la decisión de scope quede trazable.

**Paso 4 [LATENT]: Manejo de leads.** Antes del hand-off al partner que cierra:
- **Validar interés primero** (SMS/llamada/mensaje corto) en vez de tirarle contactos fríos al que cierra. Un lead que nunca responde al que cierra (ni llamada ni SMS) es una señal de que el hand-off fue prematuro.
- **Lead tibio declarado ("quiero aprender, no contratar todavía") va a nurture, no a call.** No forzar el hand-off con alguien que ya dijo que no está listo.
- Si un lead sale del funnel normal (agendó, se dio de baja), sacarlo del retargeting de inmediato para no seguir gastando en alguien que ya no es el target del gasto.

**Paso 5 [LATENT]: Decisión de gate al agotarse el presupuesto.** Con el gate en o cerca del techo, decidir con evidencia (no a ojo):
- **Seguir**: hay señal real (agendas, close rate) que justifica ampliar el gate.
- **Pivotar**: hay captura (leads/clics) pero no cierre; el ángulo, la oferta o el canal necesitan cambiar antes de seguir quemando presupuesto en lo mismo. Esto dispara el modo relanzamiento (Paso 6).
- **Matar**: se cumplió el kill criteria del Paso 1 (ej. presupuesto agotado con 0 agendas ICP). Cerrar el gate, documentar el % real ejecutado (no redondear "gastamos todo" si quedó un remanente) y pasar a `s4b-postmortem`.
- El veredicto se redacta con el CPA real, el n de agendas (si es chico, decir "señal incipiente", no "clara"), y sin generalizar el canal completo a partir de una sola ejecución ("no convirtió en esta campaña" ≠ "el canal no funciona").
- Cierre escalonado: no apagar todos los canales el mismo día. El canal más caro/menos señal se corta primero; un canal barato (ej. retargeting de bajo gasto diario) puede seguir unos días más como última red antes de apagar del todo, si el costo marginal es bajo.

**Paso 6 [LATENT]: Modo relanzamiento.** Cuando el Paso 5 decide pivotar:
- **A/B de concepto = externo y coherente, nunca split interno con los mismos ads.** Si se testean dos posicionamientos (ej. "agencia" vs "persona"), cada uno necesita su propio anuncio Y su propia landing coherente entre sí (campaña persona → landing persona; campaña agencia → landing agencia). Un split interno por cookie que sortea la landing pero corre los MISMOS anuncios genera incoherencia mensaje↔landing (el ad promete una cosa, la landing muestra otra) y contamina el resultado.
- En Google, coordinar el split con **Google Experiments** (parte el budget 50/50 sin canibalizar las mismas keywords entre las dos ramas).
- Aceptar la limitación: un A/B externo mueve 2 variables a la vez (anuncio + landing), así que decide QUÉ concepto ganó, no POR QUÉ ganó. Si hace falta aislar la causa, es un segundo experimento, no este mismo.
- **Meta con pool de retargeting chico no se fragmenta.** Si la audiencia de RT es angosta, correr un solo concepto genérico en Meta (sin A/B de voz) y reservar el A/B de posicionamiento para el canal con volumen (típicamente Google).

**Paso 7 [DET]: Advertencia sobre tareas programadas.** Si el reporte periódico corre como tarea programada (cron / scheduled task): el prompt de esa tarea es una **copia congelada** al momento de crearla. NUNCA debe duplicar parámetros operativos que cambian más rápido que la propia tarea (montos de gate, nombres de campaña, destinatario del mail). El prompt correcto dice **"leé el SKILL.md de {skill} y seguilo al pie"** y nada más. Si el prompt resume valores concretos ("gate = $200", "manda a fulano@"), se desincroniza apenas esos valores cambien en la fuente real, y nadie se acuerda de actualizarlo. La corrección no es "actualizarlo cada vez"; es no cargarlo con datos que van a mutar.

## Herramientas de optimización (invocadas desde acá, no etapas propias)

Dentro del Paso 2/5, cuando el gate necesita optimización fina de cuenta (no operación de reporte):
- **`roles/search-query-analyst.md`**: negativos y n-grams, cada 2-4 semanas de gasto activo.
- **`roles/campaign-auditor.md`**: auditoría de cuenta completa, cada 4 semanas o al detectar una anomalía persistente.

Estos roles son herramientas que `operar-gates` usa cuando hace falta, no sub-etapas del playbook. No se invocan por default en cada corrida del reporte.

## Log de corrida

Al cerrar un gate (Paso 5 con veredicto seguir/pivotar/matar), appendear una entrada a `runs/{fecha}-{NEGOCIO}.json` del orquestador con `"etapa": 4`, `"gate"`, `"presupuesto_ejecutado_pct"` y `"veredicto_gate"` (ver el schema extendido documentado en el `SKILL.md` del orquestador).

## Output esperado

`workspace/operacion-gates.md` (tabla de gates con baseline/kill criteria/veredicto + log de reportes) + un archivo por corrida en `entregables/reportes-{cadencia}/` + drafts de mail al partner (nunca enviados) +, al cerrar un gate, la entrada correspondiente en `runs/`.

## Success metrics

- 0 gates encendidos sin kill criteria explícitos acordados con el partner de antemano.
- El reporte periódico sale en cada corrida programada, aun degradado (0 corridas abortadas por una fuente caída).
- El veredicto de cierre de gate cita el CPA real y el n de agendas, sin generalizar el canal a partir de una sola ejecución.
- Si hay una tarea programada, su prompt no contiene ni un solo valor operativo que pueda desincronizarse (monto, nombre de campaña, destinatario).

## Troubleshooting

- **El partner quiere prender sin kill criteria ("ya vemos sobre la marcha")**: mostrar el costo de decidirlo en caliente (en un piloto real se improvisó el veredicto de cierre de un gate al final, sin criterio previo) y ofrecer un kill criteria mínimo de una línea si no hay tiempo para más.
- **El reporte automatizado detecta que su propio prompt quedó desactualizado**: seguir el SKILL.md vigente, no el resumen del prompt (y avisarlo en la corrida), pero flaggear que el prompt necesita rediseñarse para no volver a pudrirse (Paso 7).
- **Un lead con mucho engagement en el nurture no responde al hand-off**: antes de descartarlo, chequear el dominio del email (puede ser un competidor investigando) y si es genuino, ofrecerle nurture en vez de forzar la call.
- **El gate está al borde del techo y no hay señal clara**: no estirar el gate "para ver un poco más" sin nueva evidencia; eso es la trampa de matrícula vs impuesto evitable (ver principios del orquestador). Si el kill criteria se cumplió, cerrar.
- **El usuario corrige un número del reporte con un dato real (screenshot de la grilla) horas después**: el sistema de degradación evita bloquear la entrega, pero el número final confiable en canales con navegador bloqueado (ej. Google Ads con anti-adblock) puede seguir dependiendo de que alguien mire la fuente real. No presentar la estimación degradada como definitiva si hay forma de verificarla a mano.
