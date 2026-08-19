---
name: sizing-audiencias-meta
description: >-
  Etapa 1 del playbook lanzar-piloto. Mide tamaños reales de audiencia en Meta (Graph API delivery_estimate) por núcleo, vertical, idioma y geo, y diseña la estructura de adsets en 3 capas (base ∩ intención ∩ afinador). Usar cuando el usuario diga "sizing de audiencias Meta de X", "cuánta gente hay en [geo]", "tamaño de audiencia en español", "volumen Meta de X", "armá las 3 capas / los adsets de X", "targeting Meta de X". Resuelve los IDs de interés/geo y corre harvest_audiences.py (config-driven). Consume ../roles/meta-ads-strategist.md. Escribe workspace/research/meta-audiences.md + audiences.json. NO crea campañas (eso es spec-campanias).
---

# Etapa 1 · sizing-audiencias-meta — cuánta gente hay y cómo apilarla

Mide el volumen real antes de prometer alcance, y arma la estructura de adsets en 3 capas para llegar a lo más angosto sin quedarse sin gente. `delivery_estimate` es un cálculo read-only (no crea nada ni gasta). Escribe `workspace/research/meta-audiences.md` + `audiences.json`.

## Parámetros
- `MERCADO/GEO` (ciudad + radio, o DMA/county), `IDIOMA(S)`, `VERTICALES`/segmentos del piloto.
- `META_ACCT` — ad account con token (cualquiera sirve para estimar; idealmente USD).

## Prerequisitos
- Token en tu `.env` de Meta (`ACCESS_TOKEN`), leído en `~/.config/meta/.env`.
- `../roles/meta-ads-strategist.md` como framework de estructura full-funnel.
- Script `scripts/harvest_audiences.py` + `scripts/audiences.example.json`.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| Graph API `delivery_estimate` + `search` | **Lee** (tamaños + resolución de IDs), read-only |
| `scripts/audiences.json` | **Escribe** (config: cuenta, geo, rows por núcleo/vertical) |
| `workspace/research/meta-audiences.md` | **Escribe** (tabla de tamaños + estructura de adsets) |
| `1.research.md § Audiencias` + `workspace/_backbone.md § Meta` | **Actualiza** (IDs resueltos) |
| `../roles/meta-ads-strategist.md` | **Lee** |

## Flujo

**Paso 1 [DET] — Resolver IDs.** Para el geo y los intereses/comportamientos del rubro, resolver los keys vía Graph API search. **Cada `type` se comporta distinto:**
- Geo: `GET /search?type=adgeolocation&q={ciudad}` → `key` de la ciudad/DMA.
- Intereses: `GET /search?type=adinterest&q={término}` → `id` + `audience_size_lower/upper_bound`. Este respeta el `q` y trae el tamaño; es el que hay que usar para intereses.
- Comportamientos: `GET /search?type=adTargetingCategory&class=behaviors` → devuelve el taxonomy entero de comportamientos (~285 items, NO respeta el `q`); filtrar por nombre.
- **NO uses `type=adTargetingCategory&class=interests`** para intereses: ignora el `q` y devuelve un volcado genérico cuyo primer item es una categoría de belleza/cuidado personal sin relación con lo buscado. Ese es el gotcha que puede hacer creer (falsamente) que un software o rubro puntual "no es targeteable". En realidad la mayoría de los softwares e industrias sí son intereses targeteables; verificá cada término con `type=adinterest` antes de descartarlo.

Guardar los IDs (van a `_backbone.md` y al config).

**Paso 2 [LATENT] — Diseñar las 3 capas.** Por segmento, definir: **capa 1 (base)** = dueños de negocio / comportamiento ancla; **capa 2 (intención)** = interés que señala el problema (ej. un interés/software propio del rubro); **capa 3 (afinador)** = idioma o interés del vertical. En verticales la capa 2 suele ser opcional (si apilás las 3 cae <10K y a daily bajo quema frecuencia). Edad floor 25. Escribir cada combinación como un `row` en `audiences.json` (ver `audiences.example.json` como modelo).

**Paso 3 [DET] — Correr el harvester.** `python3 scripts/harvest_audiences.py audiences.json`. Devuelve, por row, el tamaño total + el slice del idioma (si `locale_slice` está seteado) + el %. Correr también la **sensibilidad geo** (mismo núcleo a +15mi / +25mi / DMA) como rows extra para ver cuánto mueve el radio.

**Paso 4 [LATENT] — Lectura.** ¿El volumen es la restricción o no? ¿Qué % es del idioma objetivo? Recomendar la estructura de adsets (cuáles van, con qué prioridad, qué budget diario aguantan sin quemar frecuencia). Eso alimenta `spec-campanias` y el `_backbone`.

## Output esperado

`workspace/research/meta-audiences.md` con la tabla de tamaños (núcleos + verticales + sensibilidad geo + slice idioma), `audiences.json` reproducible, y los IDs resueltos volcados a `_backbone.md`.

## Success metrics

- Tamaños del Graph API real (no estimaciones), para el geo + edades correctas.
- Slice del idioma objetivo calculado (si el piloto es bilingüe).
- Estructura de adsets en 3 capas definida por segmento, con prioridad y feasibility de budget.
- IDs de interés/geo resueltos y guardados (reproducible).

## Troubleshooting

- **"Invalid parameter" en un interés:** algunos no son targeteables en ciertas cuentas. Sacarlo de la lista, no abortar. OJO: no confundir un interés que no existe con el gotcha del search (ver abajo): antes de descartar un término, resolvelo con `type=adinterest`, no con `type=adTargetingCategory&class=interests`.
- **El search "resuelve todo a una categoría genérica" / "el software del rubro no es targeteable":** es el gotcha del `type=adTargetingCategory&class=interests`, que ignora el `q` y devuelve un volcado genérico. Usar `type=adinterest&q={término}` para intereses. La mayoría de los softwares/rubros específicos SÍ existen y son targeteables; no borrarlos como si fueran placeholders rotos.
- **Audiencia <10K a daily bajo:** quema frecuencia rápido; bajar una capa (sacar la intención en verticales) o ampliar geo, nunca mezclar rubros (los ads y el targeting van hiper-específicos por vertical; si la audiencia queda chica, agrandá por geo, no mezclando rubros).
- **Pool de retargeting <1.000 no entrega.** Una audiencia de RT que resulta por debajo de ~1.000 personas (ventana de días configurada) suele devolver "audience too small" (Graph API `code 300`) o directamente no entregar impresiones aunque la plataforma la marque activa. **No armar un BOFU separado sobre un pool así de chico**: la solución que suele funcionar es sumar el ad de cierre/reserva directamente al adset MOFU (pool más grande, sin fragmentar) en vez de sostener una capa de embudo que nunca va a tener volumen. Antes de asumir "recién arranca, todavía no hay gente" como motivo, chequear la ventana real de la audiencia (ej. 180 días no arranca de cero): el problema casi siempre es tamaño de pool, no antigüedad.
- **El token es read-only para esto:** `delivery_estimate` no crea ni gasta; correrlo sin miedo, es solo cálculo.
- **No confundir tamaño con calidad:** un núcleo grande no garantiza fit; el creativo + el prefiltro del form son los que califican (el targeting de interés es grueso).
