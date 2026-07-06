---
name: swipe-ads-competidores
description: >-
  Etapa 1 del playbook lanzar-piloto. Arma un swipe file de los ads que los competidores tienen corriendo en el Meta Ad Library (copy + CTA + creatividades descargadas) y detecta gaps de mensaje. Usar cuando el usuario diga "swipe de ads de X", "qué ads usan los competidores", "ad library de X", "copy de la competencia en Meta", "bajame las creatividades de competidores", "qué está corriendo la competencia". Scrapea el Ad Library vía Apify y procesa con build_swipe.py (parametrizado). Escribe workspace/research/competitor-ads-swipe.md + ads-creatives/. Es insumo de creativos-ads. NO escribe nuestros anuncios.
---

# Etapa 1 · swipe-ads-competidores — qué corre la competencia

Junta el copy + las creatividades reales que los competidores tienen al aire y los ordena para escribir mejores anuncios (etapa 3) y detectar el gap de mensaje (research). Escribe en `workspace/research/meta/` (`competitor-ads-swipe.md` + `ads-creatives/`).

## Parámetros
- `TÉRMINOS` — qué buscar en el Ad Library (el rubro del piloto, ej. "contabilidad" para un estudio contable local).
- `PAÍS` — country del Ad Library (ej. US, AR).
- `RELEVANT` / `NOISE` — regex de términos del rubro que SÍ importan / ruido a descartar (se pasan al script).

## Prerequisitos
- Apify MCP conectado (para el scrape del Ad Library).
- Python 3 con `urllib` (stdlib). Script en `scripts/build_swipe.py`.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| Apify (actor Meta/Facebook Ad Library) | **Lee** (scrape) |
| `workspace/research/meta/ad-library-raw.json` | **Escribe** (dump crudo, input estable del script) |
| `workspace/research/meta/competitor-ads-swipe.md` | **Escribe** (el swipe) |
| `workspace/research/meta/ads-creatives/` | **Escribe** (imágenes/videos descargados) |
| `scripts/build_swipe.py` | **Corre** |

## Flujo

**Paso 1 [DET] — Scrape del Ad Library.** Buscar el actor de Apify (`search-actors "meta ad library"` / "facebook ad library ads"), revisar su input schema (`fetch-actor-details`) y correrlo con `TÉRMINOS` + `PAÍS`. Guardar el output crudo en `ad-library-raw.json` (estructura anidada con `snapshot`, `page_name`, `images`, `videos`, `cards`).

**Paso 2 [DET][FANOUT-able] — Build del swipe.** Correr `python3 scripts/build_swipe.py ad-library-raw.json` con las env vars del rubro (ejemplo ilustrativo para un estudio contable local):
```
SWIPE_RELEVANT="account|contab|contad|tax|cpa|financ|libros"   # términos del rubro
SWIPE_NOISE="arthritis|assisted living|playground"             # opcional, ruido
SWIPE_TERMS="contabilidad / contadora"                         # label para el header
```
El script filtra por `RELEVANT`, descarta `NOISE`, dedupea, detecta idioma (ES/EN), baja las creatividades a `ads-creatives/` (idempotente, salta lo ya bajado) y escribe `competitor-ads-swipe.md` con copy + CTA + links a los archivos locales + link al Ad Library en vivo.

**Paso 3 [LATENT] — Lectura de patrones.** Leer el swipe y extraer para el research: anunciantes con más volumen, **gap de mensaje** (qué ángulo/idioma nadie está usando), copies más efectivos observados. Eso alimenta `1.research.md § Meta Ads` y los wedges de `creativos-ads`.

## Output esperado

`competitor-ads-swipe.md` (ads agrupados por idioma, con copy + CTA + creatividades locales + link en vivo), `ads-creatives/` con las imágenes/videos, y `ad-library-raw.json` como input reproducible.

## Success metrics

- ≥10 ads relevantes capturados (tras filtrar ruido), con creatividades descargadas.
- Split por idioma cuando el mercado es bilingüe.
- ≥1 gap de mensaje identificado (ángulo/idioma que nadie usa) para el research + los wedges.

## Troubleshooting

- **El Ad Library US no expone geo ni spend:** no se puede saber a quién targetean ni cuánto gastan; solo copy/creatividad. Anotarlo como limitación.
- **Ruido por match de palabra suelta:** ajustar `SWIPE_NOISE`; el filtro `RELEVANT`/`NOISE` es lo único específico del rubro.
- **Videos pesados:** el script baja SD (no HD) a propósito. Si falla una descarga, queda registrado `[FAIL]` y sigue (no aborta el swipe).
- **No re-scrapear de gusto:** `ad-library-raw.json` es el input estable; re-correr `build_swipe.py` sobre él es gratis e idempotente.
