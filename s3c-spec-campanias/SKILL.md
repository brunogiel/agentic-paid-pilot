---
name: spec-campanias
description: >-
  Etapa 3 del playbook lanzar-piloto. Escribe la spec de ejecución de las campañas Google + Meta del piloto, campo por campo: settings comunes, campañas/ad groups con keywords y bids, adsets en 3 capas con IDs, budgets reconciliados, negativas, Final URLs por idioma y naming. Doble uso: el usuario arma a mano o un agente ejecuta vía MCP. Usar cuando el usuario diga "la spec de campañas de X", "estructura Google/Meta del piloto", "fichas de ejecución", "budget por campaña", "armá las campañas en pausa". Consume ../roles/google-ads-strategist.md + ../roles/meta-ads-strategist.md y hereda el _backbone. Escribe workspace/campañas.md. NO escribe el copy de los ads (creativos-ads) ni el tracking (setup-tracking).
---

# Etapa 3 · spec-campanias — la ficha que se ejecuta campo por campo

Traduce el backbone + research a una spec operativa que cualquiera (el usuario a mano, o un agente con MCP de Google/Meta) ejecuta sin re-decidir nada. (Reemplazá con tu propia corrida de referencia si ya especificaste campañas de un piloto antes.)

## Parámetros
- `NEGOCIO`, `BUDGET` (del kickoff); split, segmentos, gate (del backbone).
- Insumos de Etapa 1: keywords + ad groups + negativas + CPC (`kw-research-google-ads.md`), adsets 3 capas + IDs resueltos (`meta-audiences.md`).

## Prerequisitos
- `../roles/google-ads-strategist.md` + `../roles/meta-ads-strategist.md` (frameworks de estructura de cuenta, match types, split de budget: son la fuente de la estructura de campañas).
- `workspace/_backbone.md` cerrado (sin `[ABIERTO]` bloqueantes en segmentos/budget).

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/workspace/campañas.md` | **Escribe** (la spec completa) |
| `../roles/google-ads-strategist.md` + `../roles/meta-ads-strategist.md` | **Lee** (estructura de cuenta, match types, adsets, budget split) |
| `workspace/_backbone.md` + `3.ejecucion-piloto.md § Budget` | **Lee** (budget autoritativo, segmentos, Final URLs) |
| `workspace/research/kw-research-google-ads.md` + `meta-audiences.md` | **Lee** (keywords, CPC, adsets, IDs) |

## Flujo

**Paso 1 [DET] — Reconciliación de budget.** Tabla única autoritativa: campaña → total → diario (total ÷ días) → % del piloto. Marcar qué prende en Etapa 1 (gate) y qué queda apagado hasta pasar el gate. Cualquier cifra vieja en otros docs: se ignora, manda esta tabla.

**Paso 2 [LATENT] — Settings comunes Google.** Para cuenta cold con budget chico: Search only (Display/partners OFF), Manual CPC (sin Smart Bidding sin historial), bottom of page, exact + phrase (sin broad), location "Presence" (no "Presence or interest"), rotate indefinitely las primeras 2 semanas, 2 conversiones (calificado primaria + submit secundaria). PMax NO en el piloto.

**Paso 3 [LATENT] — Ficha por campaña Google.** Por campaña: geo, idioma, bid de arranque (del planner), budget, Final URL (dominio del idioma correcto), ad groups con keywords + match + volumen, negativas compartidas + propias, notas de bid por ad group.

**Paso 4 [LATENT] — Ficha por adset Meta.** Por adset: las 3 capas (base ∩ intención ∩ afinador) con los IDs resueltos del sizing, geo + radio, edades (floor 25), tamaño estimado, budget diario, prioridad, placement, Final URL por idioma. Retargeting/lookalike marcados Fase 2 (necesitan pixel con volumen).

**Paso 5 [LATENT] — Abiertos que bloquean.** Listar arriba del doc los `[ABIERTO]` que impiden ejecutar (IDs de conversión, ad account, medio de pago) y quién los destraba. No inventar IDs.

**Paso 6:** checkpoint con el usuario; la spec queda lista para cargar campañas **en pausa** (encender es de `pre-launch-validation`).

## Output esperado

`workspace/campañas.md`: reconciliación de budget + settings comunes + ficha campo por campo de cada campaña Google y cada adset Meta, con naming consistente, negativas y abiertos bloqueantes explícitos.

## Success metrics

- Un agente con MCP podría cargar las campañas sin tomar ninguna decisión nueva (0 campos en "a definir" sin `[ABIERTO]`).
- Budget de la spec suma exacto el total del kickoff; dailies = total ÷ días.
- Cada Final URL apunta al dominio del idioma del ad (0 cruces).
- Etapa 1 vs Etapa 2 del gate marcadas campaña por campaña.

## Troubleshooting

- **Smart Bidding en cuenta nueva:** sobrepaga sin historial; Manual CPC al rango bajo y bottom of page (regla longtail).
- **Mismo ad group con 2 idiomas:** Google/Meta no aceptan 2 Final URLs por idioma en el mismo objeto; partir por idioma (ad groups EN/ES, ads EN/ES).
- **Budget ref viejo en otra tabla:** ignorar y citar la reconciliación; una "nota de reconciliación" única evita que dos tablas se contradigan.
