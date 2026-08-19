# Infra y credenciales del kit de leadgen

> Plantilla para mapear qué credencial vive dónde y qué componente la usa. Nunca valores, solo nombres de variable y paths. Antes de crear una credencial nueva para un piloto, mirar esta tabla primero (ver "Regla para pilotos nuevos" abajo). Completá las filas con tu propia infra; las de acá son ejemplos de formato.

## Tabla

| Servicio | Variable / archivo | Path | Componente(s) que la usa(n) |
|---|---|---|---|
| CRM (ej. Notion, Sheets, Supabase) | `<SERVICIO>_TOKEN`, `<SERVICIO>_DATABASE_ID` | `~/.config/<servicio>/` o env var del hosting | `componentes/captura-y-crm/` |
| Automatización (ej. n8n), webhook del piloto | `<WEBHOOK>_URL` | env var del hosting del proyecto | `componentes/captura-y-crm/`, `componentes/lead-magnet-y-nurture/`, `componentes/agendamiento/` |
| Automatización (ej. n8n), API key propia | API key | `~/.config/<automatizacion>/<tu-key>` | Transversal: cualquier componente cuyo stack elegido pase por esta automatización |
| ESP (ej. MailerLite, Brevo) | API token | `~/.config/<esp>/api-token` | `componentes/lead-magnet-y-nurture/` (si el menú elige este ESP) |
| Email transaccional/cold (sending-only) | API key | `~/.config/<proveedor>/.env` | `componentes/cold-outreach/` (envío) |
| Email transaccional/cold (full-access) | API key | `~/.config/<proveedor>/.env-full` | `componentes/cold-outreach/` (lectura de bounces/complaints para el stop-loss) |
| Meta Ads | `ACCESS_TOKEN`, `AD_ACCOUNT_ID`, `BUSINESS_ID` | `~/.config/meta/.env` | Etapas 1/3 del playbook, no un componente nuevo de este kit |
| Google Ads | credenciales del MCP/API que uses | `~/.config/google-ads/.env` | Etapas 1/3 del playbook (`s1b-kw-research-google`, `s3c-spec-campanias`), no un componente nuevo de este kit |
| Workspace de productividad (ej. Google Workspace) | credenciales del conector | `~/.config/<workspace>/` | Transversal, reusable por cualquier componente que necesite leer/escribir hojas de cálculo o mandar mail |
| Canal WhatsApp | key opcional del modelo cloud | `~/.config/<whatsapp-router>/<key>` | `componentes/canal-whatsapp/` |
| Booking (ej. Calendly, Cal.com) | PAT / API key | No guardar en texto plano; regenerar si se retoma un piloto que lo usa | `componentes/agendamiento/` (si el menú elige esta opción) |
| Hosting/deploy (ej. Vercel) | IDs del proyecto | `.vercel/project.json` (solo IDs, no secrets) | Transversal, cualquier componente con front propio |

## Gaps abiertos

> Sección viva: anotá acá lo que falta o quedó a medio resolver, para no perder el hilo entre pilotos.

- Ejemplo: si tu proveedor de email cold es sending-only, sin acceso de lectura a bounces/complaints el stop-loss automático queda ciego y depende de chequeo manual.
- Ejemplo: tokens con fecha de rotación pendiente.

## Regla para pilotos nuevos

Antes de crear una credencial nueva, mirar esta tabla:

- **Lo que es por-servicio se reusa.** Cuentas de ads, workspace, automatización, ESP: son credenciales que sirven para cualquier piloto. No crees una cuenta nueva de tu ESP por proyecto, por ejemplo.
- **Lo que es por-proyecto se crea nuevo.** La base del CRM, el webhook de la automatización del piloto, el container de tracking (ej. GTM): estos SÍ son uno por piloto. Regla dura: **nunca compartir containers de tracking entre proyectos** (mezcla datos de negocios distintos en la misma cuenta y ensucia los reportes de los dos).
