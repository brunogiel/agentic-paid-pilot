---
name: cold-outreach
description: Arma y opera una campaña de cold email a listas scrapeadas (Google Maps/OSM/web del negocio) cuando no hay presupuesto de paid ni base propia. Usar cuando querés "mandar cold email", "armar el outreach", "scrapear negocios de tal rubro", "el envío frío", "prender/frenar el outreach", "cuántos mails mandamos hoy", o cuando buscás un canal barato para tocar un vertical sin ads.
---

# Cold outreach

> **⚠ ADVERTENCIA DE ToS (leer antes de cualquier receta de esta página):**
> Los proveedores transaccionales de mail de uso general (Resend, Google Workspace, Microsoft 365, Amazon SES) **prohíben explícitamente el cold outreach en su Términos de Servicio**, aunque el cold email B2B sea legal bajo CAN-SPAM (remitente real, asunto honesto, dirección postal, opt-out). La cuenta puede cerrarse sin aviso previo por violar el ToS, independientemente de que el envío sea legal. Existen herramientas dedicadas de cold email (QuickMail, Smartlead, Instantly, lemlist) que sí lo permiten en su ToS y traen warm-up incluido. **Antes de mandar un solo mail, decidí conscientemente: (a) usar una herramienta dedicada, o (b) asumir el riesgo de usar infra transaccional general, documentando esa decisión.** No es una decisión técnica, es una decisión de negocio con riesgo real de perder la cuenta de mail.

## Nivel 1 · First principles

**Qué problema resuelve:** genera leads fríos por email a una lista scrapeada (mapas, directorios, la propia web del negocio) cuando no hay presupuesto de paid ni una base propia de contactos, y el ICP se puede identificar por categoría + geografía.

**Cuándo conviene:**
- El ICP es identificable por categoría de negocio + zona geográfica en fuentes scrapeables (Google Maps, OpenStreetMap, directorios).
- Hay tiempo para operar un ramp de varias semanas (esto no es un canal de resultado instantáneo).
- El costo objetivo es bajo/cero y el volumen que se busca es de a cientos, no de a miles por día.

**Cuándo NO conviene:**
- No hay definido quién atiende la respuesta o el agendamiento del que contesta: sin comprador para el lead, el canal no importa aunque funcione.
- Se necesita volumen alto desde el día uno (el ramp progresivo es innegociable, ver invariantes).
- El dominio de envío es el mismo que corre infra crítica (el funnel real, el nurture de clientes) sin un plan de contingencia si la reputación se daña.

**Invariantes (esto tiene que estar sí o sí):**
1. **Decisión consciente de ToS documentada** (ver advertencia arriba): herramienta dedicada o riesgo asumido, nunca por default sin decidir.
2. **Ramp progresivo de volumen**, nunca arrancar a full: empezar bajo (ej. 10/día), subir por escalones (ej. 20, luego 35) con un cap duro diario que no se cruza aunque haya más lista disponible.
3. **Stop-loss automático** que se dispara solo por tasa de rebote o quejas de spam por encima de un umbral, y que deja de enviar sin esperar a que alguien lo note a mano.
4. **Negarse a enviar si la sincronización de métricas no corrió** (o corrió hace demasiado). Preferir no mandar antes que mandar a ciegas sin saber si el stop-loss podría estar disparándose.
5. **Un contacto por dominio.** Cadenas y negocios multi-local se descartan o se deduplican a un solo contacto; mandarle a 5 casillas del mismo negocio quema reputación sin sumar leads reales.
6. **Texto plano, un solo link, sin tracking pixel de terceros ni HTML de newsletter.** Esto es lo que mejor cae en los filtros de spam.
7. **List-Unsubscribe + dirección postal física en cada mail** (requisito de CAN-SPAM, no opcional).
8. **Remitente y dominio separados de la infra transaccional crítica**, cuando sea posible: si el experimento sale mal, no debería salpicar al funnel real.

**Success metrics:**
- Tasa de enriquecimiento: % de contactos scrapeados que terminan con un email válido y enviable.
- Bounce rate bajo el umbral del stop-loss (mide la salud de la lista, no solo del copy).
- Tasa de respuesta positiva (interés real, no solo aperturas).
- Gate de muerte explícito: un volumen total de envíos sin señal positiva define el cierre del experimento, no un plazo de tiempo indefinido.

## Nivel 2 · Menú de stack sugerido

| Opción | Cómo funciona | Cuándo tiene sentido |
|---|---|---|
| **Transaccional general asumiendo el riesgo de ToS** (Resend, SES, etc.) | Infra que ya existe, sin costo extra, API simple | Cuando ya hay dominio + infra transaccional propia y se decide conscientemente asumir el riesgo de ToS, con ramp y stop-loss estrictos para minimizarlo |
| **Herramienta dedicada de cold email** (QuickMail, Smartlead, Instantly, lemlist) | ToS lo permite explícitamente, trae warm-up de dominio incluido, dashboards de deliverability | Cuando el presupuesto lo permite (planes de entrada rondan los US$40-50/mes) y se prefiere no arriesgar la cuenta de infra transaccional |
| **Casilla de Workspace/M365 nueva, dedicada solo a esto** | Dominio y reputación 100% aislados del resto | Cuando se puede pagar una casilla nueva (unos US$7/mes) y se quiere el aislamiento más fuerte sin sumar una herramienta de cold email completa |

En un piloto real de referencia (leadgen para un rubro de servicios profesionales) se usó **transaccional general (Resend) asumiendo el riesgo de ToS**, con un remitente y dominio de envío separados del dominio principal del funnel. Fue una decisión consciente para no pagar una herramienta dedicada en un experimento de costo casi cero; el riesgo que quedó vivo es que la reputación del dominio de envío es compartida con la infra crítica del proyecto (el nurture), mitigado con ramp lento, verificación de lista y stop-loss, pero no eliminado.

Son sugerencias, no obligaciones. Antes de elegir, vale buscar si apareció una opción nueva o mejor.

## Nivel 3 · Receta

Si elegís la opción probada (transaccional general asumiendo el riesgo, con ramp + stop-loss), seguí [reference.md](reference.md).

## Output esperado

- Lista de contactos scrapeada, filtrada por ICP (categoría + geografía) y deduplicada por dominio.
- Enriquecimiento de emails faltantes vía la web del propio negocio (no vía redes sociales, ver reference.md).
- Config de ramp + stop-loss + cap diario operativa.
- Copy en texto plano con las variantes a testear, List-Unsubscribe y dirección postal.
- Reporte diario de envíos, aperturas, rebotes y respuestas.

## Success metrics

Ver invariante final de Nivel 1: tasa de enriquecimiento, bounce rate bajo umbral, tasa de respuesta positiva, gate de muerte por volumen sin señal.
