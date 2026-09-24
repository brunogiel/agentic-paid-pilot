---
name: pre-launch-validation
description: >-
  Etapa 3 del playbook lanzar-piloto. Checklist determinístico pre-encendido: links y landings vivos, forms envían y llegan al CRM, tracking dispara en GTM preview, billing activo en Google Ads y Meta, privacy y terms publicadas, scan de agent-readability de las landings, budgets y gates configurados en las plataformas, campañas en estado pausa con settings correctos. Casi todo [DET]. Usar cuando el usuario diga "validá el piloto antes de encender", "pre-launch", "punch-list", "chequéen que todo está ok", "estamos listos para encender", "prendamos las campañas", "falta algo antes de lanzar", "armá el checklist de validación". Output: checklist con PASS/FAIL por ítem; gate de "no encender hasta que todo esté verde". NO enciende las campañas sola: espera OK explícito del usuario.
---

# Etapa 3 · pre-launch-validation — la punch-list que cierra el piloto antes de prender

Checklist determinístico de todos los pre-requisitos técnicos, legales y operativos que tienen que estar en verde antes de encender la Etapa 1 del gate. Un ítem FAIL bloquea el encendido; no hay grises. El orquestador solo enciende las campañas después de que el usuario aprueba este checklist explícitamente.

## Parámetros
- `NEGOCIO`, URLs de landings publicadas, plataformas activas (Google Ads / Meta / ambas).
- IDs de tracking (del `workspace/setup-tracking.md`).
- Budget y gate de Etapa 1 (del `workspace/_backbone.md`).
- Campaña(s) y adset(s) a encender (del `workspace/campañas.md`).

## Prerequisitos
- `workspace/setup-tracking.md` cerrado (IDs documentados, QA de tracking hecho).
- `workspace/campañas.md` cerrado (campañas y adsets cargados en pausa en las plataformas).
- `workspace/creativos.md` cerrado (ads cargados, sin abiertos bloqueantes de Etapa 1).
- Landings publicadas en producción (no en staging).
- Privacy policy y terms publicados en el dominio del negocio.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/workspace/pre-launch-checklist.md` | **Escribe** (checklist con estado PASS/FAIL por ítem) |
| `workspace/setup-tracking.md` | **Lee** (IDs, estado del QA de tracking) |
| `workspace/campañas.md` | **Lee** (budget, gate, naming de campañas y adsets) |
| `workspace/creativos.md` | **Lee** (abiertos bloqueantes de Etapa 1) |
| `workspace/_backbone.md` | **Lee** (gate de budget, URLs, segmentos bloqueantes) |

## Flujo

**Paso 1 [DET] — Landings y forms.** Para cada URL de landing activa en la Etapa 1:
- La URL carga en menos de 4 segundos (LCP < 3s).
- No hay errores de consola del navegador (F12 > Console, 0 errores rojos).
- El form llena y envía correctamente (test con datos falsos).
- La thank-you page aparece post-submit (o el mensaje de éxito en la misma página).
- El lead de test llega al CRM destino (Supabase / Notion / sheet / mail).
- Los UTMs pasan del ad a la landing y de la landing al CRM (`?utm_source=test` → verificar en el CRM que el campo llegó).
- El GCLID se captura en el form si aplica (pass `?gclid=test123`, verificar en el submit).
- **Agent-readability:** `npx -y is-agentic@latest {dominio}` sobre cada dominio live (~20-25 s). Se anota el `score` y los checks `essential` que no pasaron. **No bloquea el encendido**: un score bajo no impide que el ad convierta, y este ítem existe para que el número quede registrado antes de tener tráfico encima, no para frenar el piloto. Lo que sí bloquea lo tira el Paso 4 por su propia vía — si el check de trust anchors falla porque `/privacy` no existe, el FAIL es legal, no de agent-readability.

**Paso 2 [DET] — Tracking.** Por plataforma activa:
- **Google Ads:** conversion action primaria configurada (category Lead, count One per click, include in Conversions = YES); tag disparando en GTM preview en la thank-you URL.
- **Meta Pixel:** PageView disparando en todas las URLs de landing; Lead event disparando en la thank-you URL (o post-submit event); visible en Meta Test Events.
- **GA4:** page_view en todas las landings; lead_submit (o equivalente) marcado como conversión; eventos visible en DebugView.
- **CAPI (si aplica):** evento Lead llegando como "deduplicated" en Meta Test Events (Pixel + CAPI con mismo event_id).

**Paso 3 [DET] — Billing y cuentas.** Por plataforma activa:
- Google Ads: la cuenta tiene método de pago activo; no hay alertas de suspensión; la campaña no está detenida por billing.
- Meta: la cuenta tiene método de pago activo (tarjeta aceptada, no rechazada); el ad account está en estado normal (no `account_status=3` ni ningún otro código de error); no hay restricciones de política pendientes.

**Paso 4 [DET] — Legal y privacidad.** Para cada dominio del negocio:
- Privacy policy publicada (URL accesible sin login, enlazada desde el footer de la landing).
- Terms of service publicados (ídem).
- Meta Business: el dominio está verificado en el BM.
- Si hay tráfico EU potencial: Consent Mode v2 configurado o documentado como fuera de scope del piloto.

**Paso 5 [DET] — Campañas y adsets en plataformas.** Por cada campaña y adset de la Etapa 1:
- La campaña está en **pausa** (no activa todavía) con los settings correctos: geo, idioma, budget diario, bid strategy, Final URLs.

🔴 **Los 4 defaults de Google Ads que se cargan solos y nadie mira.** "Verificá los settings" no verifica nada: hay que **nombrar el valor esperado y leerlo de la cuenta**, campaña por campaña. Los cuatro se ponen solos al crear una campaña o al importar por CSV/Editor, y ninguno da error ni se nota en el reporte diario: se notan meses después, en la factura o en un lead que no podía convertir nunca.

| Setting | Campo en la API | Default que muerde | Lo que casi siempre querés |
|---|---|---|---|
| Tipo de segmentación geográfica | `campaign.geo_target_type_setting.positive_geo_target_type` | `PRESENCE_OR_INTEREST` | `PRESENCE`, si vendés un servicio local. Con el default le mostrás el anuncio a cualquiera del mundo que "muestre interés" en tu ciudad |
| Idiomas | `campaign_criterion` tipo `LANGUAGE` | El idioma de la interfaz de quien creó la campaña, que puede no ser el del mercado | El idioma real de la landing. Si la landing está en español y la campaña targetea solo inglés, estás comprando una fracción del mercado sin saberlo |
| Search partners | `campaign.network_settings.target_search_network` | `true` | `false` en un piloto: es inventario de terceros que no se puede diagnosticar por separado |
| Display | `campaign.network_settings.target_content_network` | `true` en campañas Search creadas con el asistente | `false`. Es la fuga de plata clásica de una Search armada con el wizard |

**Y la regla que hace que este bloque sirva: leerlo de la cuenta, nunca del CSV ni del spec.** Un import puede agregar defaults que el archivo no tenía y descartar columnas en silencio; los dos casos vistos en la misma cuenta fueron una ubicación "Estados Unidos" que no salía de ningún CSV y unos ajustes de puja que nunca cargaron. Si el checklist se completó mirando un borrador del asistente y después la campaña definitiva se cargó por otra vía, **lo verificado no es lo que está corriendo**.
- El adset de Meta está en **pausa** con el targeting correcto: geo, edad mínima, capa de audiencia (sin IDs fantasma), presupuesto diario.
- Los ads están aprobados por la plataforma (sin rechazos pendientes de políticas).
- **QA visual en la UI del ads manager de lo cargado por API/CSV:** abrir el preview real de cada ad y confirmar imagen correcta, copy completo, Final URL y placement. La carga programática puede diferir de lo que se cree que subió (imagen equivocada, texto truncado, duplicados silenciosos); el JSON de respuesta de la API no reemplaza mirar el ad renderizado.
- El naming de campañas y adsets coincide con `campañas.md` (0 objetos sin nombre).
- El budget total del piloto suma exacto al del backbone; el gate de Etapa 1 está seteado como límite de campaña o en el doc de control del usuario.

**Paso 6 [DET] — Abiertos de Etapa 1 en creativos.** Revisar `workspace/creativos.md` sección "Abiertos": confirmar que ningún abierto marcado como bloqueante de Etapa 1 sigue sin resolver.

**Paso 7 [LATENT] — Emitir resultado.** Tabla de todos los ítems con estado (PASS / FAIL / N/A). Si hay ≥ 1 FAIL: listar los FAIL con la acción exacta para resolverlo y quién la destraba. No proponer encender hasta que todos los ítems de Etapa 1 sean PASS o N/A. Si todo está en verde: emitir "VALIDACIÓN EN VERDE — listo para encender Etapa 1" y esperar el OK explícito del usuario.

**Paso 8 [DET] — Runbook de encendido (recién con el OK).** El encendido no es "activar todo y ver": es un mini-runbook escrito ANTES de tocar el primer switch:
- **Orden de encendido explícito**, objeto por objeto (qué campaña/adset se activa primero y cuál queda apagado hasta pasar el gate), con el cap de gasto del primer día calculado como suma de los budgets diarios que se prenden (≤ el cap acordado).
- **Verificación post-switch inmediata**: cada campaña encendida queda en estado "Apto"/activo de verdad (no "pendiente de revisión" ni pausada a nivel superior; gotcha real: un ad ACTIVE dentro de una campaña PAUSED no sirve nada).
- **Chequeo a las 2-24 h**: impresiones > 0 en cada campaña, gasto acorde al budget (ni cero ni disparado), sin rechazos tardíos de ads (las plataformas re-revisan al activar).
- **Re-leer los 4 defaults del Paso 5 con la campaña ya sirviendo**, no solo antes de prender. Es el mismo chequeo, corrido contra el objeto que está en el aire. Un piloto real perdió 8 días de gasto con la geo en `PRESENCE_OR_INTEREST` **después** de haber marcado ese ítem como PASS: se había verificado sobre el borrador del asistente, y la campaña que terminó corriendo se cargó por CSV, que reintrodujo el default. Cuesta una query y es el único momento en que el dato es el verdadero.
- **Rollback simple**: si algo está mal, pausar a nivel campaña y volver al checklist; nunca corregir settings con la campaña sirviendo.

**Post-launch (una vez encendido):** la optimización continua del piloto vive en `../roles/search-query-analyst.md` (search terms, negativos, n-grams semana a semana); si el piloto arranca sobre una cuenta de ads ya existente, pasarla antes por `../roles/campaign-auditor.md` para no heredar deuda de configuración.

## Output esperado

`workspace/pre-launch-checklist.md`: checklist con estado PASS / FAIL / N/A por ítem, agrupado por bloque (landings+forms, tracking, billing, legal, campañas, creativos), con el score de `is-agentic` por dominio en el bloque de landings, + tabla de FAIL pendientes con acción y owner + veredicto final ("EN VERDE, esperando tu OK" o "BLOQUEADO hasta resolver N ítems").

## Success metrics

- 0 ítems FAIL al momento de encender las campañas de Etapa 1.
- Cada FAIL tiene una acción de resolución concreta (no "revisar" sino "hacer X en Y").
- El veredicto final es binario: verde o bloqueado (sin grises ni "casi listo").
- El ok de encendido lo da el usuario explícitamente despues de ver el veredicto verde.

## Troubleshooting

- **El lead de test no llega al CRM:** primero verificar que el webhook URL en la landing apunta al entorno de producción (no staging); luego revisar el log del nodo n8n; finalmente verificar el destino (Notion / Supabase / sheet según el proyecto).
- **Ad rechazado por política de Meta:** leer el mensaje de rechazo, corregir el copy o la imagen infractora, reenviar para revisión. No encender el resto hasta que todos los ads de Etapa 1 estén aprobados.
- **Billing bloqueado en Meta (account_status=3 o similar):** no se resuelve cambiando tarjeta; hay que apelar el estado desde el BM. Si el fix requiere varios días, considerar si la Etapa 1 puede arrancar solo con Google Ads.
- **GCLID no llega al CRM:** el hidden input no existe o el JS que lo llena no corre antes del submit. Es un FAIL de tracking, bloquea la mejora de bidding a futuro (puede arrancar igual si el usuario lo acepta como deuda técnica explícita).
- **Privacy page sin enlace desde la landing:** el ad de Meta no pasa la revisión si la landing no tiene Privacy Policy accesible. Siempre FAIL bloqueante.
