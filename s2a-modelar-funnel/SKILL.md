---
name: modelar-funnel
description: >-
  Etapa 2 del playbook lanzar-piloto. Modela el funnel económico del piloto: tasas de conversión etapa por etapa con fuente, CAC por escenario (pesimista/benchmark/realista/optimista), CPL objetivo, CAC máximo tolerable y breakeven, en un Excel con fórmulas vivas. Usar cuando el usuario diga "modelá el funnel de X", "cuánto sale una venta en X", "CAC/LTV del piloto", "estimá el embudo", "a qué CPL cierra el modelo", "armá el CAC tracker de X". Consume el research de la Etapa 1 (CPC del kw research, benchmarks). Escribe workspace/research/estimaciones-funnel.md + CAC-Tracker xlsx. NO define hipótesis ni gates (eso es disenar-experimento).
---

# Etapa 2 · modelar-funnel — cuánto sale una firma

Convierte el research en números: dado el spend, cuántos clientes entran y a qué costo. Es el insumo duro del gate de la Etapa 2 (LTV/CAC ≥ 1 en realista o no hay piloto). (Reemplazá con tu propia corrida de referencia si ya modelaste un piloto antes.)

## Parámetros
- `NEGOCIO`, `BUDGET`, `MODELO` (cómo cobramos), `DEADLINE` (del kickoff).
- Insumos de Etapa 1: CPC realista del kw research, benchmarks de paid de `1.research.md`, ticket/retention del research de mercado (para el LTV).

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/workspace/research/estimaciones-funnel.md` | **Escribe** (embudo + tasas + escenarios + lectura) |
| `{NEGOCIO}/workspace/research/CAC-Tracker-{NEGOCIO}.xlsx` | **Escribe** (fórmulas vivas, no valores pegados) |
| `{NEGOCIO}/2.plan-piloto.md § KPIs` | **Actualiza** (umbrales que salen del modelo) |
| `1.research.md § Benchmarks` + `workspace/research/kw-research-google-ads.md` | **Lee** (tasas + CPC con fuente) |

## Flujo

**Paso 1 [LATENT] — Dibujar el embudo.** Definir las etapas concatenadas del funnel real del piloto (ej. impresión → click → landing → CTA → form completo → pasa prefiltro → show-up V1 → V2 → cierre). Cada negocio tiene su cadena; no copiar una plantilla ajena a ciegas (¿hay 1 call o 2 visitas? ¿form o Calendly?).

**Paso 2 [LATENT] — Tasas por escenario.** Para cada etapa, 4 columnas: pesimista / benchmark de mercado / realista / optimista. **Cada tasa con fuente citada** (Unbounce, WordStream, Calendly, etc.) o marcada "estimación interna — validar en el piloto". El CPC sale del kw research (planner real), no del benchmark genérico.

**Paso 3 [DET] — Excel con fórmulas vivas.** Generar el xlsx (openpyxl): inputs arriba (spend, CPC, tasas por escenario), cadena multiplicativa con **fórmulas** (cambiar un supuesto recalcula todo), y abajo CAC, LTV, LTV/CAC y margen por escenario.

**Paso 4 [LATENT] — Lectura.** Derivar del modelo: **CPL objetivo** (qué CPL hace cerrar el realista), **CAC máximo** tolerable (donde LTV/CAC = 1), **breakeven** (cuántas firmas pagan el piloto), y cuál tasa es la más sensible (dónde mirar primero si el piloto viene flojo).

**Paso 5:** devolver al orquestador LTV/CAC por escenario + CPL objetivo + CAC máximo, para el checkpoint y para que `disenar-experimento` fije umbrales.

## Output esperado

`estimaciones-funnel.md` (embudo + tabla de tasas con fuente + escenarios + lectura accionable) y `CAC-Tracker-{NEGOCIO}.xlsx` con fórmulas vivas. `2.plan-piloto.md § KPIs` con los umbrales numéricos del modelo.

## Success metrics

- 4 escenarios completos, cada tasa con fuente o "estimación interna" explícita (0 números inventados como dato duro).
- LTV/CAC calculado por escenario + veredicto claro (¿cierra en realista?).
- CPL objetivo + CAC máximo + breakeven nombrados con número.
- El xlsx recalcula al cambiar un supuesto (fórmulas, no valores).

## Troubleshooting

- **No hay benchmark del rubro:** usar el rango del rubro más cercano y marcarlo; la tasa se valida en el piloto, no se presenta como dato.
- **LTV/CAC < 1 en realista:** parar y avisar antes de seguir a `disenar-experimento`; o se cambia el modelo (ticket, geo, canal) o se descarta.
- **Cadena demasiado optimista:** el subtotal compuesto delata tasas infladas; sanity-checkear el click→firma compuesto contra benchmarks de punta a punta, no solo etapa por etapa.
