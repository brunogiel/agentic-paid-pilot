---
name: research-mercado
description: >-
  Etapa 1 del playbook lanzar-piloto. Evalúa si un vertical/negocio merece un piloto: checklist de mercado de 9 criterios + scoring, análisis competitivo (lenses + posiciones sin ocupar + mapa de players) y síntesis "3 movimientos". Usar cuando el usuario diga "research de mercado de X", "¿vale la pena este vertical?", "scoreá el negocio X", "competitive de X", "qué slot está vacante en X", "los 3 movimientos para X". Consume tu checklist de criterios de negocio + tu caja de frameworks. Toma como insumo los outputs de las otras 3 skills de research (kw, swipe, sizing). Escribe 1.research.md. NO arma campañas ni landings.
---

# Etapa 1 · research-mercado — ¿avanza o no?

Decide si el vertical merece un piloto y deja las bases para construirlo. Es el corazón del veredicto: si el checklist no da AVANZAR, no se gasta en las etapas 2-3. Es el `1.research.md` + `competitive-brief.md` del proyecto (reemplazá con tu propia corrida de referencia).

## Parámetros
- `NEGOCIO`, `MERCADO/GEO`, `IDIOMA(S)` (del kickoff).
- Insumos de las skills hermanas (si ya corrieron): swipe de ads, sizing de audiencias, kw research. Si no, esta skill los puede pedir o correr inline.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/1.research.md` | **Escribe** (secciones checklist, competitive, síntesis, audiencias, benchmarks) |
| `{NEGOCIO}/workspace/research/competitive-brief.md` | **Escribe** (perfiles por player) |
| tu checklist de criterios de negocio | **Lee** (los 9 criterios del checklist + método 0→1) |
| tu caja de frameworks | **Lee** (framework por capa, si hace falta) |
| `workspace/research/competitor-ads-swipe.md` + `*-audiences.md` + `*-kw-*.md` | **Lee** (insumos de las skills hermanas) |

## Flujo

**Paso 1 [LATENT] — Checklist de mercado (9 criterios).** Correr los 9 criterios de tu checklist de criterios de negocio (canal digital · fragmentación · slot · unit economics · compound/asimetría · mercado estable · no-VCs · escalabilidad · AI). Para cada uno: ✅/⚠️/❌ + nota + next step. Cerrar con "**X/9 → AVANZAR / NO**". Los ⚠️/❌ no bloquean: se validan en el piloto, pero se nombran.

**Paso 2 [LATENT][FANOUT] — Competitive.** Identificar los players del mercado (web search + el swipe de ads como insumo). Si hay >5 players relevantes, spawnear un `Agent` por player (o por grupo) con prompt autocontenido y retorno JSON `{player, tipo, pricing, diferenciador, threat}`; el padre arma el mapa. Producir: lenses de análisis (2-3 ejes que importan en este mercado), **posiciones sin ocupar**, posiciones gastadas (clichés a evitar), mapa de players. Detalle a `competitive-brief.md`, resumen a `1.research.md`.

**Paso 3 [LATENT] — Síntesis "3 movimientos".** Destilar todo en los 3 movimientos que nadie está haciendo bien hoy y que el piloto va a explotar. Es el output más accionable de la etapa.

**Paso 4 [LATENT] — Audiencias + benchmarks.** Volcar a `1.research.md` el targeting pagado (Google signals + Meta targeting, alimentado por la skill de sizing) y los benchmarks de paid del rubro (CPL, CR, close rate, CAC/LTV estimados con fuente).

**Paso 5:** devolver el veredicto (AVANZAR/no + los 3 movimientos) al orquestador para el checkpoint.

## Output esperado

`1.research.md` poblado: checklist con veredicto, competitive (lenses + posiciones sin ocupar + mapa), 3 movimientos, audiencias, benchmarks. `competitive-brief.md` con perfiles por player.

## Success metrics

- Los 9 criterios evaluados con ✅/⚠️/❌ + veredicto explícito AVANZAR/NO (no "parece bien").
- ≥3 movimientos accionables + ≥1 posición sin ocupar identificada.
- Competitive con ≥5 players mapeados y el threat más alto nombrado.
- Benchmarks de paid con fuente citada (no inventados).

## Troubleshooting

- **No delegar conteo/scoring masivo al LLM:** el juicio por player es [LATENT], pero si hay que rankear N players por una métrica, que el padre lo ordene determinístico sobre los JSON de los sub-agentes (principio: nunca combinatoria al LLM).
- **Benchmarks sin fuente = no van.** Si no hay dato del rubro, marcar "estimación interna — validar en el piloto", no presentarlo como dato duro.
- **Si el checklist da NO o muy flojo:** parar y avisar al usuario antes de seguir a Etapa 2; el playbook no empuja un vertical que no pasa el filtro.
