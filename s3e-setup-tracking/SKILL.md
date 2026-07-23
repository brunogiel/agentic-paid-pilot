---
name: setup-tracking
description: >-
  Etapa 3 del playbook lanzar-piloto. Produce el runbook completo de tracking para el piloto: GTM container plan (tags + triggers + variables), GA4 (measurement ID + eventos custom + conversiones), conversion actions de Google Ads (primary + secondary, todos los settings), Meta Pixel + CAPI (deduplication con event_id), UTM naming convention, y checklist de QA de disparo. Usar cuando el usuario diga "setup de tracking", "el tracking del piloto", "GTM del piloto", "conversion actions de X", "el pixel de X", "CAPI de X", "cómo mido las conversiones", "armá el tracking para X", "runbook de cuentas". Consume ../roles/tracking-specialist.md. Escribe workspace/setup-tracking.md. NO pone a encender campañas (eso es pre-launch-validation).
---

# Etapa 3 · setup-tracking — el runbook de tracking antes de prender un ad

Produce el plan de implementación de tracking del piloto: qué crear en cada plataforma, en qué orden, con qué settings exactos, y cómo verificar que dispara bien antes de encender. El stack es GTM (container único) + GA4 + Google Ads conversions + Meta Pixel + CAPI (si aplica). Basado en `../roles/tracking-specialist.md`.

## Parámetros
- `NEGOCIO`, URLs de las landings (del backbone o `campañas.md`).
- Plataformas de ads activas en el piloto (Google Ads y/o Meta, según `campañas.md`).
- CRM destino de los leads (Supabase / Notion / sheet / n8n webhook).
- ¿Hay CAPI? (sí si el form manda datos server-side via n8n o GTM server; consultar con el usuario).

## Prerequisitos
- `../roles/tracking-specialist.md` (framework completo de tracking: GTM + GA4 + Meta CAPI + conversion actions + deduplicación).
- `workspace/campañas.md` cerrado: Final URLs, nombres de campañas, conversiones objetivo.
- Las landings publicadas o en staging (necesitamos el dominio verificado en Meta BM).
- Cuentas creadas: Google Ads activa, Meta Business Manager con el dominio añadido.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/workspace/setup-tracking.md` | **Escribe** (runbook completo + IDs + checklist QA) |
| `../roles/tracking-specialist.md` | **Lee** (framework de GTM/GA4/Ads/Pixel/CAPI/UTM) |
| `workspace/campañas.md` | **Lee** (Final URLs, objetivos de conversión, cuentas) |
| `workspace/_backbone.md` | **Lee** (CTA único, funnel form-first vs call, CRM destino) |

## Flujo

**Paso 1 [DET] — Inventario de cuentas y objetos existentes.** Listar: IDs ya disponibles (Google Ads account ID, Meta BM + pixel ID, GA4 measurement ID, GTM container ID) vs los que hay que crear. Si el piloto es completamente nuevo, todos se crean en el paso siguiente. Formato de entrega: una sección "Tracking IDs e infra operativa" en el brief del proyecto, todos los IDs juntos.

**Paso 2 [DET] — Plan de objetos de tracking a crear.** Tabla: plataforma / objeto / settings requeridos / ya existe (sí/no). Cubrir:
- **GTM:** container nuevo o existente; workspace de trabajo; tags a crear (GA4 config, GA4 event lead_submit, Google Ads conversion linker, Google Ads conversion, Meta Pixel base, Meta Pixel lead event).
- **GA4:** measurement ID; enhanced measurement (page_view, scroll, outbound click ON); eventos custom a marcar como conversión (lead_submit mínimo; WhatsApp click si aplica); linked accounts (Google Ads).
- **Google Ads:** conversion action primaria (category Lead, count One per click, window 30d, include in Conversions = YES, attribution Last click hasta tener 300+ conv/mes para Data-driven); conversion action secundaria (form started o WhatsApp click, NOT include in Conversions); conversion linker tag.
- **Meta Pixel:** pixel ID; PageView en todas las páginas; Lead event en thank-you; domain verification en BM.
- **Meta CAPI:** ¿sí o no? Si el form manda datos via n8n: event_id generado en el form + mismo event_id en el payload n8n → Meta CAPI endpoint. Checklist de dedup en Test Events tab.
- **UTM naming convention:** `utm_source` (google/meta/linkedin), `utm_medium` (cpc), `utm_campaign` (nombre de la campaña, slug), `utm_content` (nombre del ad group / adset), `utm_term` (keyword para Google). Tabla de ejemplos concretos para este piloto.

**Paso 3 [DET] — Orden de implementación.** Secuencia con dependencias explícitas:
1. Verificar dominio en Meta BM (bloquea todo lo de Meta).
2. Crear GTM container + instalar snippet en las landings.
3. Crear conversion actions en Google Ads → traer el conversion ID y label a GTM.
4. Crear Pixel en Meta → traer pixel ID a GTM.
5. Crear GA4 property → traer measurement ID a GTM.
6. Configurar tags en GTM (primero base, luego events).
7. Publicar GTM container.
8. Si hay CAPI: configurar el payload n8n con el event_id.
9. QA en preview mode y Test Events.

**Paso 4 [DET] — Checklist QA post-implementación.** Por ítem: qué verificar, dónde verificarlo, qué es un PASS. Cubrir:
- GTM preview: todos los tags disparan en la URL de la landing (PageView).
- GTM preview: tag Lead dispara en thank-you page (o post-submit).
- GA4 DebugView: llegan page_view + lead_submit.
- Google Ads conversion preview: la conversión aparece en modo preview (Tag Assistant).
- Meta Test Events: llegan PageView + Lead; si hay CAPI, aparecen como "deduplicated".
- UTMs: llenar el form con `?utm_source=test` y verificar que el parámetro llega al CRM destino.
- GCLID: verificar que el hidden field captura el GCLID (pasar `?gclid=test123` y verificar en el form submit o en el CRM).

**Paso 5 [LATENT] — Abiertos que bloquean el tracking.** Listar explícito: accesos que el usuario tiene que gestionar (cuenta Meta BM con dominio añadido, acceso al GTM container, API key si hay CAPI manual). Marcar cuál bloquea el encendido.

## Aprendizajes de terreno

- **Un evento canónico por acción; toda la lógica de tags vive en GTM.** Cero `fbq`/`gtag` sueltos disparando directo desde el código del sitio. Si el mismo botón/acción dispara 2 eventos por error (ej. un hero que disparaba 2 conversiones por 1 sola captura real), el bug casi siempre es que la lógica de cuándo disparar quedó embebida en el código en vez de vivir toda en GTM con un solo trigger/tag por acción real.
- **event_id de deduplicación Pixel/CAPI = el UUID nativo del evento de la herramienta de booking**, cuando la hay (ej. Calendly). Si el evento de reserva ya trae un UUID propio disponible tanto en el postMessage del lado cliente como en el webhook del lado servidor, usar ESE id como `event_id` de dedup: no hace falta generar ni sincronizar nada aparte entre pixel y CAPI, el mismo UUID llega solo a los dos lados.
- **La API de stats del pixel de Meta tiene retención dura de ~28 días** (`/{pixel_id}/stats` devuelve vacío para rangos más viejos). Para reconstrucciones históricas más allá de esa ventana, no hay atajo de API: hay que ir a Events Manager a mano o reconstruir desde reportes escritos previos.
- **Los fallbacks de UI de Google Ads pueden mentir cuando la grilla principal está bloqueada** (ad blocker, canvas no legible). Las estimaciones derivadas de vistas agregadas (Overview, Billing, último dato conocido) pueden diferir bastante de la grilla real, incluyendo casos donde la diferencia decide si un gate ya se había cruzado o no. Google además corrige datos hacia arriba con lag de reporting (el dato de ayer no es final el mismo día). **Regla: la grilla real manda; un fallback agregado es una estimación de emergencia, no un reemplazo, y hay que decirlo así en cualquier reporte que la use.** Si hay forma de que un humano confirme con captura de la grilla real, esa captura pesa más que cualquier fallback.

## Output esperado

`workspace/setup-tracking.md`: inventario de IDs (en blanco si hay que crearlos, con el ID real cuando existan) + tabla de objetos a crear por plataforma + orden de implementación con dependencias + checklist QA (PASS/FAIL por ítem) + UTM naming convention + abiertos bloqueantes. El doc es el runbook que el usuario ejecuta en su sesión de configuración de cuentas.

## Success metrics

- Cada plataforma tiene su IDs documentados en el runbook (0 IDs en blanco al momento de encender).
- El checklist QA tiene ≥ 1 ítem de verificación por plataforma activa.
- Hay un conversion action primario definido con todos sus settings (0 campos "a definir").
- Si hay CAPI, el event_id de dedup está descrito y verificable en Test Events.
- La UTM naming convention tiene ejemplos concretos de este piloto (no genéricos).

## Troubleshooting

- **Domain verification Meta bloqueado:** es el primero que hay que destrabar; sin él, CAPI no funciona y los eventos de conversión no se optimizan bien.
- **GCLID no llega al CRM:** el form necesita un hidden input `name="gclid"` llenado desde el query param via JS. Sin GCLID no hay offline import para enseñar al algoritmo quién califica.
- **Doble conteo CAPI:** si Pixel y CAPI mandan el mismo evento sin el mismo event_id, Meta los suma. El event_id tiene que ser idéntico en ambas llamadas (generarlo en el form + pasarlo en el payload n8n).
- **Primary conversion = PageView:** el error más costoso; envenena el bidding. Primary siempre al CTA real del piloto (lead_submit o equivalent).
- **GTM container ya existente en el dominio de otro proyecto:** nunca compartir containers entre proyectos con plataformas de ads distintas; crear uno nuevo.
