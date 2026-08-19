---
name: kw-research-google
description: >-
  Etapa 1 del playbook lanzar-piloto. Keyword research real para Google Ads de un vertical: volúmenes y CPC del Keyword Planner (geo + 12 meses), keywords prioritarias por intención, agrupación en ad groups + match types, lista de negativas y CPC realista por campaña. Usar cuando el usuario diga "kw research de X", "keywords para Google de X", "volúmenes reales de búsqueda", "CPC realista de X", "negativas de Google Ads", "estructura de campañas Google para X". Usa el MCP keyword-planner. Consume ../roles/google-ads-strategist.md. Escribe workspace/research/kw-research-google-ads.md. NO escribe los anuncios (eso es creativos-ads).
---

# Etapa 1 · kw-research-google — volúmenes, KW, CPC, negativas

Reemplaza los "rough estimates" por datos reales del Keyword Planner antes de encender Google. Evita pujar a ciegas: define qué keywords entran, en qué ad group, con qué match y a qué CPC. Escribe `workspace/research/kw-research-google-ads.md`.

## Parámetros
- `MERCADO/GEO` (para el geo del planner), `IDIOMA(S)`, `VERTICALES`/segmentos del piloto.
- Semilla de keywords (la da el usuario o se deriva del research-mercado).

## Prerequisitos
- MCP `keyword-planner` conectado (`generate_keyword_ideas`, `get_historical_metrics`, `get_keyword_forecast`).
- `../roles/google-ads-strategist.md` como framework de estructura de cuenta.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| MCP `keyword-planner` | **Lee** (volúmenes, CPC, forecast) |
| `{NEGOCIO}/workspace/research/kw-research-google-ads.md` | **Escribe** |
| `{NEGOCIO}/1.research.md § Análisis SEM` | **Actualiza** (TLDR + KW prioritarias) |
| `../roles/google-ads-strategist.md` | **Lee** |

## Flujo

**Paso 1 [DET] — Pull de volúmenes.** Con la semilla, `generate_keyword_ideas` + `get_historical_metrics` para el geo y los últimos 12 meses. Sacar búsquedas/mes + CPC low/high + competencia por keyword. Si hay >1 idioma, correr cada idioma por separado (el volumen en español suele ser otra liga que en inglés).

**Paso 2 [LATENT] — Priorización por intención.** Clasificar cada keyword por intención (transaccional alta / media / informacional) y descartar las que no son del negocio. Las longtail con CPC bajo + intención alta son oro para un piloto cold (regla madre del playbook).

**Paso 3 [LATENT] — Estructura de campañas.** Agrupar en ad groups temáticos (exact + phrase), mapear a las campañas del piloto (ej. local / idioma / probe), y asignar match types. Apoyarse en `../roles/google-ads-strategist.md` para los tiers de estructura.

**Paso 4 [LATENT] — Negativas con lente ICP + CPC.** Armar la lista de negativas clasificando la intención en tres baldes: **ICP** (quiere contratar/comprar), **no-ICP** (jobs/salary, educación/cursos/how-to/what-is, DIY/software/templates, competidores por nombre, industrias OUT) y **dudoso** (genérico/price-shopping). Las negativas tapan el no-ICP.

**Timing: dos cajones, no "más negativas".** El error típico no es *pocas* negativas, es mezclar dos cosas con timing opuesto:
- **Tier-1 (basura universal, día cero, reusable):** términos que cualquier piloto neguea sin pensar, downside cero, no ganás info dejándolos correr. Es **impuesto evitable** (ver Principios del orquestador): se cargan el minuto cero desde una lista base, no se "descubren" quemando plata. Starter reusable a adaptar por idioma/geo: `jobs`, `salary`, `careers`, `hiring`, `resume`, `free`, `cheap`, `course`, `courses`, `class`, `training`, `certification`, `certified`, `exam`, `degree`, `how to`, `how to become`, `what is`, `definition`, `meaning`, `template`, `templates`, `excel`, `spreadsheet`, `diy`, `do it yourself`, `software`, `app`, `tool` (ojo: NO negativar el software del cliente si lo querés, ej el software que usa el rubro).
- **Tier-2 (intención dudosa, reactivo, NUNCA pre-bloquear):** los guesses semánticos. Pre-bloquearlos es sobre-fittear antes de tener data y mata ICP en silencio. Solo se neguean **reactivo**, leídos contra el search-terms una vez live.

Dos reglas que suelen costar caro aprender:
- **No sobre-bloquear ICP.** Cada negativa candidata se chequea contra los términos ICP: una negativa de más mata leads en silencio (ej. términos como "for individuals", "part time" o "at home" pueden filtrar gente que quiere contratar; "pricing"/"going rate" a veces matan price-shoppers que SÍ compran). NO negativizar el software del cliente (si querés "[software] [servicio]"), ni "near me"/idioma/[industria IN], ni el plural/variante de un término ICP (`franchises` mata "[servicio] for franchises").
- **Frase no agarra variantes.** Las negativas NO tienen close-variants: `gig` no tapa `gigs`, un script no latino no matchea. Cubrir plurales/sinónimos a mano.
Para un panel robusto, barrer con varias lentes (jobs/educación/DIY, competidores/marcas, industrias OUT, short-tail/servicios adyacentes, y un **guardián anti-over-block** que audita que ninguna negativa mate ICP). CPC realista por campaña del planner, no del benchmark.

**Paso 5:** devolver al orquestador la lista de KW prioritarias + CPC por campaña + negativas para alimentar `spec-campanias`.

## Output esperado

`workspace/research/kw-research-google-ads.md`: tabla de keywords (volumen + CPC + intención), estructura de ad groups por campaña con match types, lista de negativas, CPC realista por campaña. `1.research.md § Análisis SEM` actualizado.

## Success metrics

- Volúmenes y CPC del Keyword Planner real (no estimaciones), para el geo correcto.
- Cada keyword prioritaria mapeada a un ad group + match type.
- Lista de negativas ≥15 términos, clasificada con lente ICP/no-ICP/dudoso y auditada para no sobre-bloquear ICP (sin negativar software del cliente, geo/idioma, price-shoppers, ni plurales de términos ICP).
- Si el piloto es bilingüe, hay corte por idioma (no un solo set en inglés).

## Troubleshooting

- **Planner sin volumen para un idioma en un geo local chico:** común que el search en un idioma minoritario a nivel local sea casi nulo; la lectura correcta suele ser "ese idioma se captura por Meta (audiencia), no por Google (búsqueda)". Anotarlo, no forzar la campaña.
- **PMax:** default recomendado para un piloto chico es dejarlo apagado, sin volumen de conversiones para entrenar y sin visibilidad de fit-rate por término es difícil auditarlo temprano. Con volumen de conversiones ya generado (o si el piloto escala), vale reevaluar sumarlo en paralelo a Search, no en reemplazo.
- **CPC del benchmark ≠ CPC del planner:** mandar el del planner para el geo; el benchmark genérico solo como sanity check.
- **Auditar negativas con el search-terms report una vez live, no a ciegas:** el informe de términos de búsqueda esconde ~⅔ de los clics en "Otros términos de búsqueda" (no itemizables); de lo visible, clasificar ICP/no-ICP/dudoso y cruzar contra las negativas cargadas para cazar gaps **y over-blocks** (negativas que matan ICP). Nombres de competidores sueltos de 1 impresión = whack-a-mole, no perseguir uno por uno; si hay patrón, un token estructural (`reviews`) tapa la familia.
