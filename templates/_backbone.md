# Backbone compartido: {{NEGOCIO}} piloto

> **Qué es esto:** el contrato de invariantes que los 3 entregables de ejecución (`campañas`, `creativos`, `landings`) respetan **sin re-derivar**. Destilado de `3.ejecucion-piloto.md` (la constitución). Si algo en `research/` lo contradice, **manda esto**. Si encontrás un hueco real, flagealo como `[ABIERTO: ...]`, no lo inventes en silencio.

---

## Marca y oferta
- **Brand:** `{{BRAND}}` = {{nombre}} ({{dominio}}). Nuestra (quien sirve aparece como caso, no como la marca).
- **Dominios:** {{uno por idioma, mismo deploy}}. Cada campaña apunta su Final URL al dominio del idioma correcto.
- **Qué es / qué NO es el servicio:** {{precisión que define el copy; ej. distinguir el servicio de otro rubro con el que se confunde}}.
- **Escritura:** sin em-dash (—) en español; en inglés OK.
- **CTA único en todo el funnel:** "{{ej. Revisión gratuita 15 min}}" → {{form / Calendly}}.
- **ICP del cliente final:** {{tamaño/floor, perfil, vertical IN}}. El floor va como **pregunta dura del formulario**.
- **Verticales IN:** {{ }}.  **OUT:** {{ }} (se manejan por copy + prefiltro, no por exclusión de interés).
- **Regla madre:** longtail. Barato y específico. Piloto cold de {{N}} días.

## Segmentos (nombres canónicos, NO renombrar)
| # | Segmento | Ubicación / Idioma | Canal | Wedge primario |
|---|---|---|---|---|
| 1 | {{ }} | | | |

> Aclarar las mecánicas de geo por canal (ej. Google = búsqueda activa nacional; Meta = audiencia local).

## Landings (NO son traducciones una de otra)
| Landing | Segmento | Canales que alimenta | Idioma | Foco / hero |
|---|---|---|---|---|
| {{ }} | | | | |

- **Verticales = dynamic text replacement del hero** (`?v=`), NO una landing por vertical.
- Base de diseño compartida. **Stack:** diseño → agente de código → deploy (ej. Vercel).

## Google Ads: {{%}} del budget = {{$}}
| Campaña | Geo | CPC bid | Budget total | Budget diario |
|---|---|---|---|---|
| G1 · {{ }} | | | | |

- **Negativas en TODAS:** {{lista}}.
- **PMax: NO en el piloto.** Keywords completas en `research/`.

## Meta Ads: {{%}} del budget = {{$}}
| Adset | Base | Intención | Afinador | Tamaño | Budget | Prioridad |
|---|---|---|---|---|---|---|
| M1 · {{ }} | | | | | | 1 |

- **3 capas apiladas.** Edad floor 25. Retargeting + Lookalike = Fase 2 (necesitan pixel/volumen).
- **IDs Meta resueltos:** {{intereses + geo + idioma}}.

## Budget: nota de reconciliación
**Total piloto: {{$}}**. La tabla §Budget de `3.ejecucion-piloto.md` es la autoritativa. Cualquier "Budget ref" menor en otras tablas: ignorar y usar §Budget ÷ días = budget diario. Gate inicial: {{$gate}}.

## Funnel y medición
```
Ad → Landing (pain hero + CTA único, Pixel + GA4 desde el 1er click)
 → Form que califica solo (gate {{OUT / floor}})
    [no califica] → "no es el fit" · [califica] → submit = conversión → CRM + aviso (n8n) → quien cierra llama
 → V1 → V2 → Firma
```
**Métrica madre = cost-per-qualified-lead.** Fit-rate por campaña. Todo a un Sheet con UTMs.

## Dueño del proyecto
{{Quién opera los canales}} operan paid/infra/contenido; {{quién cierra}} cierra y sirve. Modelo: {{ }}. Piloto = {{N}} días desde el encendido.
