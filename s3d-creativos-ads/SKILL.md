---
name: creativos-ads
description: >-
  Etapa 3 del playbook lanzar-piloto. Escribe el copy de ejecución de todos los ads del piloto: Google RSAs (15 headlines / 4 descriptions por ad group, pin strategy, paths, sitelinks y callouts) y Meta (primary text corto+largo, headline, description, CTA, brief visual de imagen para cada ad, dirección de imagen por adset). Usar cuando el usuario diga "los creativos", "copy de los ads", "armá los RSAs", "headlines del piloto", "ads Meta del piloto", "los creativos de X", "copy de las campañas de X". Consume ../roles/ad-creative-strategist.md y hereda wedges y segmentos del _backbone. Escribe workspace/creativos.md. NO escribe la spec de estructura de cuenta (spec-campanias) ni el setup de tracking (setup-tracking).
---

# Etapa 3 · creativos-ads — el copy que va cargado en las plataformas

Traduce los wedges y segmentos del backbone a copy ejecutable por ad group y por adset: cada pieza tiene el copy completo, el conteo de caracteres, la pin strategy (Google) o el brief visual (Meta), y los abiertos que bloquean la carga. (Reemplazá con tu propia corrida de referencia si ya escribiste creativos de un piloto antes.)

## Parámetros
- `NEGOCIO`, `IDIOMA(S)`, segmentos (del kickoff + backbone).
- Wedges definidos en `workspace/_backbone.md`.
- Ad groups + Final URLs (de `workspace/campañas.md`).
- Swipe de competidores (de `workspace/research/swipe-ads-competidores.md` o similar) para extraer ángulos libres.

## Prerequisitos
- `../roles/ad-creative-strategist.md` (framework de RSAs y Meta creative: los 10 ángulos de headline, la pin strategy, los formatos de Meta salen de acá).
- `workspace/_backbone.md` cerrado: wedges, CTA único, segmentos, URLs por idioma.
- `workspace/campañas.md` cerrado: ad groups nombrados, Final URLs por grupo.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/workspace/creativos.md` | **Escribe** (copy completo de todos los ads) |
| `../roles/ad-creative-strategist.md` | **Lee** (framework de ángulos, RSAs, Meta creative) |
| `workspace/_backbone.md` | **Lee** (wedges, CTA único, segmentos, URLs) |
| `workspace/campañas.md` | **Lee** (ad groups, Final URLs, naming) |
| `workspace/research/swipe-ads-competidores.md` | **Lee** (ángulos libres, posiciones gastadas a evitar) |

## Flujo

**Paso 1 [LATENT] — Leer el swipe + extraer mapa de ángulos libres.** Antes de escribir una sola línea: revisar qué ángulos usa la competencia, qué posiciones están saturadas ("peace of mind", "free consultation") y qué frames están libres. El backbone ya lista los wedges; acá se confirma cuáles refuerzan y cuáles evitar porque son commodity. Resultado: nota al inicio del doc con "ángulos a evitar (gastados)" y "frames libres que usamos".

**Paso 2 [LATENT] — Google RSAs por ad group.** Para cada ad group de `campañas.md`:
- 15 headlines (≤ 30 chars c/u). Cubrir los 10 ángulos del framework (keyword match, beneficio, diferencial/prueba, precio, urgencia, autoridad, CTA, geo modifier, reducción de riesgo, pregunta). Contar caracteres ad hoc, no estimar.
- 4 descriptions (≤ 90 chars c/u). Un ángulo distinto por description: resumen+CTA, prueba+diferencial, proceso, objeción+urgencia.
- 2 paths (≤ 15 chars c/u, refuerzan keyword).
- Pin strategy: pinear solo cuando hay compliance, branding forzado o message match crítico (no por default). Máximo 2 pins por RSA.
- 4 sitelink extensions + 4 callout extensions (a nivel campaña).
- Tabla con nro / headline / largo / wedge / pin.

**Paso 3 [LATENT] — Meta ads por adset.** Para cada adset de `campañas.md`:
- 3 ads con 3 ángulos distintos (no variantes del mismo ángulo). Ángulos del framework: problema→solución, antes/después, prueba social, educacional, FOMO/urgencia, comparación, autoridad/behind the scenes.
- Por ad: primary text largo (storytelling, 8-12 líneas si hay copy emocional) + primary text corto (3-4 líneas, conversión directa) + headline + description + CTA (botón). Hook en la primera línea del primary text (lo que se ve antes del "Ver más").
- Brief visual por ad: qué muestra la imagen, formato (1:1 / 4:5 / 9:16), fuente (foto real disponible / generar / stock de calidad). Si hay foto real del cliente, usar. Marcar con `[ABIERTO: ...]` cuando la imagen no existe.
- Botón CTA: funnel form-first → "Más información" / "Learn more" por default; nunca "Reservar" si no hay agenda directa.
- Nota de dedup de idioma: si el negocio tiene 2 idiomas, separar copy por idioma (nunca mezclar en el mismo ad).

**Paso 4 [LATENT] — Abiertos que bloquean la carga.** Listar al inicio del doc todos los `[ABIERTO]` que impiden cargar un ad (foto no disponible, stat no confirmada, precio no definido). Separar los que bloquean Etapa 1 de los que son Etapa 2.

**Paso 5 [DET] — Plan de rotación y fatiga.** Al final del doc: cuándo hacer el primer refresh (señal: CTR cae 30%+ o frequency Meta supera 6 en prospecting), qué hipótesis testear en ronda 2, cuántas variantes activas por adset (3-5).

**Paso 6:** checkpoint con el usuario; el doc queda listo para cargar las campañas en pausa (encender es de `pre-launch-validation`).

## Aprendizajes de terreno

- **RT: la imagen comunica oferta + CTA sola, sin depender del primary text.** Un ad de retargeting que no repite la oferta en la propia imagen desperdicia frecuencia: el copy del ad y el copy quemado en la imagen tienen que decir LO MISMO (no dos promesas distintas, ej. headline genérico + imagen con el gancho real enterrado adentro).
- **Safe zones 9:16, regla dura, no sugerencia.** Top 13% y bottom ~18% del lienzo libres de texto/CTA (contenido central entre y≈280 e y≈1590 en un lienzo 1080×1920). Diseñar en arquitectura de 3 franjas (buffer superior/inferior + contenido central) desde el origen; estirar un 4:5/1:1 a 9:16 SIEMPRE rompe el creativo (sujeto pegado al borde, vacíos donde la UI de la plataforma tapa). **Truco si la cuenta bloquea la customización de creativo por placement** (típico en adsets Dynamic Creative, error genérico de API): usar el 9:16 como imagen única del ad. La plataforma la muestra full-bleed en placements verticales (Stories) y recorta al centro en feed, que se ve bien si el contenido ya está diseñado dentro de la safe zone.
- **La frecuencia alta en retargeting no se setea, se diseña.** El control de frecuencia por API (`frequency_control_specs` en Meta) suele solo existir para el objetivo de Alcance/Awareness, no para Tráfico/conversión. Para lograr frecuencia sana en un objetivo de conversión: pool de audiencia chico + variedad de creativos rotando (3-5 impresiones/semana por variedad), nunca un cap duro que la plataforma no deja setear en ese objetivo.
- **Gotchas de edición bulk de RSAs (Google Ads Editor, Buscar y reemplazar):** aplicado sobre selección múltiple, no campo por campo. Segunda pasada de `"  "` (doble espacio) → `" "` después de cualquier reemplazo por vacío, porque deja espacios dobles o texto que arranca con espacio. Nunca vaciar un headline entero por find&replace: si el término buscado ES el headline completo, reemplazarlo por vacío deja el slot en blanco y rompe el mínimo de 3 headlines del RSA, hay que borrar el slot a mano o reescribirlo. Para decenas de ads conviene exportar a planilla, editar ahí y reimportar en vez de find&replace directo. Los conteos de caracteres `[n]` declarados en un doc no son confiables por sí solos: contar con script antes de cargar. Dejar la convención de pins explícita en la intro del doc de creativos (qué headline va pineado a qué posición) para que quien carga a mano no tenga que inferir la intención. El display path cosmético (ej. `/ciudad`) no necesita ser una ruta real del sitio si el Final URL real está documentado aparte.
- **Gate de consistencia cruzada pre-carga.** Antes de cargar los ads en las plataformas, correr una verificación cruzando spec ↔ assets ↔ landing: detecta menciones textuales desactualizadas (ej. "te respondo por WhatsApp" en un RSA cuando el funnel ya migró a agenda directa) y creativos apuntando al brazo equivocado de un A/B (ej. un UGC de persona en un ad que cae en la landing "agencia"). Este chequeo es un paso formal de pre-launch, no un nice-to-have.
- **Producción programática de los estáticos (script Python + Pillow), no edición a mano.** Cuando los creativos son imagen base + texto quemado (banda de color + headline + CTA), un script que compone cada pieza desde la imagen base genera los 4 formatos (1.91:1 / 1:1 / 4:5 / 9:16) con un layout propio por formato (nunca resize del otro) y respeta las safe zones por construcción. Dos ventajas reales: (a) un cambio de copy o color regenera la tanda entera gratis (retocar 30 PNGs a mano no escala), y (b) el mismo script arma **planchas** (contact sheets: todos los creativos de una tanda en una sola imagen grande) para revisarla de un vistazo con quien decide antes de subir nada. El script se versiona junto al workspace del piloto.

## Output esperado

`workspace/creativos.md`: mapa de wedges → ángulos libres + RSAs completos por ad group (tabla headlines + descriptions + paths + pins) + ads Meta completos por adset (primary text corto y largo + headline + description + CTA + brief visual) + abiertos bloqueantes + plan de rotación.

## Success metrics

- 0 headlines > 30 chars, 0 descriptions > 90 chars (conteo real, no estimado).
- Cada ad group tiene su propio RSA con copy que coincide con el ad group theme (message match claro).
- 3 ángulos distintos por adset Meta (no variantes del mismo).
- Todos los `[ABIERTO]` identificados y separados por etapa (Etapa 1 vs 2).
- Un agente con acceso al doc podría cargar los ads sin tomar ninguna decisión de copy nueva.

## Troubleshooting

- **Headline justo en el límite (28-30 chars):** contar letra por letra, no confiar en estimación visual. Incluir el espacio entre palabras.
- **Mismo ad group en 2 idiomas:** Google no acepta 2 Final URLs por idioma en el mismo RSA; dividir en ad groups separados por idioma.
- **Ángulos todos parecidos:** releer el swipe antes de forzar variantes. Si el backbone tiene solo 2-3 wedges fuertes, mejor 3 ads bien distintos que 6 variantes mediocres del mismo ángulo.
- **Copy con claims sin sustento:** marcar `[ABIERTO: estadística / testimonial / dato]` en lugar de inventar. No poner números que el cliente no confirmó.
