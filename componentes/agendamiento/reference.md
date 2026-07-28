# Receta probada: Calendly (plan pago) + webhook al backend

> Destilada de un piloto real de leadgen que corrió este flujo en producción, con exploración real de la API v2 de Calendly. Ejemplo hipotético: un estudio contable que ofrece una "Revisión gratis de tus números" de 30 min.

## Mapa de la receta

1. Evento configurado en la UI de Calendly (la API no alcanza para lo que importa).
2. Link con prefill cableado en la landing.
3. Webhook org-scope registrado por API hacia tu backend (n8n, endpoint propio) → CRM + mail al equipo + CAPI.
4. Redirect post-reserva a una página propia con passthrough.

## 1. Setup del evento (todo en UI)

Checklist con valores de referencia:

- **Nombre**: Revisión gratis de tus números. **Slug**: `/revision-gratis` (legible en la landing).
- **Duración**: 30 min. **Ubicación**: Google Meet (o lo que use el que atiende).
- **Descripción**: 1-2 líneas (qué es, sin compromiso). Refuerzo pre-slot.
- **Disponibilidad**: el schedule de QUIEN ATIENDE, en SU timezone real. Gotcha real: si la cuenta la crea el operador del piloto, la tz de la cuenta y el schedule default son los SUYOS. Hasta que la persona que atiende no está invitada al team con su calendario conectado y su schedule propio, el evento puede quedar creado pero apagado.
- **Buffers**: mínimo aviso 4 hs + buffer 15 min post-call (a gusto del que atiende).
- **Booking questions**: recomendado piloto: solo name / email / phone. En el piloto de referencia las preguntas calificadoras (rubro + facturación) se sacaron a mitad de campaña para bajar fricción; la calificación se recuperó en la call. Nota técnica: en Calendly las preguntas son SIEMPRE post-slot (primero el horario, después el form); si querés calificar ANTES del slot, la pieza es un Routing Form (plan pago, solo UI).
- **Confirmation page**: Redirect to external site → tu página de recursos/gracias, activando el passthrough de query params (agrega datos del booking a la URL, útil para el listener de tracking).
- **Workflows (show-rate)**: confirmación inmediata + recordatorio email 24 hs + SMS 1 h antes (SMS según plan; requiere que el invitee deje teléfono). Solo UI, no hay API de workflows.
- **Notificación interna al equipo**: NO usar los workflows de Calendly; la arma tu backend desde el webhook (llega el payload completo con las respuestas).

## 2. Qué se hace por API y qué no (destilado de exploración real de la API v2)

| Capacidad | Cómo |
|---|---|
| Crear/editar event type básico | API posible (solo 1-on-1, campos básicos) pero **conviene UI**: igual hay que entrar para el resto |
| Booking questions | **Solo UI** (la API las lee en `custom_questions`, no las crea ni edita) |
| Availability schedules | Solo UI en la práctica |
| Redirect post-booking | Solo UI |
| Workflows (email/SMS) | Solo UI |
| Routing Forms | Solo UI (`routing_forms:read` solo lee) |
| **Webhook created/canceled** | **API v2** ✅ (lo único que vale la pena automatizar) |
| Link con prefill | No necesita API (query params en la URL pública) |
| Leer reservas/invitees | API v2 (`scheduled_events:read`), útil para reportes o derivar "Call Done" |

## 3. El webhook (lo único por API)

```bash
TOKEN="<PAT de Calendly>"        # en tu gestor de credenciales, nunca en el repo
WEBHOOK_URL="https://<tu-backend>/webhook/calendly-booking"
ORG_URI="https://api.calendly.com/organizations/<uuid>"   # sale de GET /users/me

curl -s -X POST https://api.calendly.com/webhook_subscriptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "'"$WEBHOOK_URL"'",
    "events": ["invitee.created", "invitee.canceled"],
    "organization": "'"$ORG_URI"'",
    "scope": "organization",
    "signing_key": "GENERAR_UN_SECRETO_ALEATORIO_Y_GUARDARLO"
  }'
```

- **`scope: "organization"`** captura las reservas de TODOS los event types de la org (cubre el evento del que atiende cuando exista). Alternativa: `scope: "user"` + `user: <uri>`.
- **`signing_key`**: secreto propio; Calendly firma el header `Calendly-Webhook-Signature` con ese valor y tu backend lo verifica. Sin esto, cualquiera puede inyectar reservas falsas a tu CRM.
- El payload de `invitee.created` trae `payload.email`, `payload.name`, `payload.scheduled_event.start_time` y `payload.questions_and_answers[]` (ahí viene el teléfono y lo que preguntes). Eso parsea tu backend.
- Verificar: `GET /webhook_subscriptions?organization=<ORG_URI>&scope=organization`. Borrar: `DELETE /webhook_subscriptions/{uuid}`.

Qué hace el backend con el webhook (patrón del piloto de referencia): upsert en el CRM (match por email, Stage → Scheduled) + mail "Nueva call" al equipo con todo el contexto + evento server-side a la plataforma de ads usando el **UUID del invitee como `event_id`** (el mismo que manda el listener browser-side del embed, para que la plataforma dedupliqué y no cuente doble).

## 4. Link con prefill (cableado en la landing)

```
https://calendly.com/<cuenta>/revision-gratis?email={EMAIL}&name={NOMBRE}
```

- `email=` prefillea el campo Email (URL-encodear con `encodeURIComponent`; el `@` es `%40`).
- `name=` opcional; si la landing solo capturó email, omitirlo.
- Respuestas de preguntas custom: `a1=`, `a2=` (posicional). Para el funnel alcanza con email.
- **UTMs**: Calendly acepta `utm_source/medium/campaign/content/term` y los incluye en el payload del webhook. Sumarlos ayuda, pero **el fallback confiable es el match por email en el CRM**, no los UTMs arrastrados.

El wiring típico desde la landing email-first: capturar el email en el hero, postear el lead a `/api/lead`, y redirigir a la página de booking arrastrando todo el query string (ver componente `ab-y-personalizacion` §3).

## 5. Gotchas (los dos caros)

1. **Webhooks solo en plan pago.** Incidente real del piloto de referencia: al vencer el trial la cuenta cayó a Free y el webhook murió, PERO el booking siguió tomando reservas y mandando el mail nativo de confirmación. Resultado: **cero filas nuevas en el CRM ya no significaba cero reservas, significaba que dejaste de escribirlas.** Silencioso total. Mitigaciones: presupuestar el plan por toda la campaña, monitorear el webhook (un ping semanal a `GET /webhook_subscriptions`), o elegir Cal.com (webhooks en free).
2. **El setup del evento es solo UI.** No scriptees la creación del evento: preguntas, redirect, workflows y disponibilidad se configuran a mano sí o sí. Presupuestá esa sesión de clicks (el checklist de la sección 1 es el guion).

Menores: las booking questions son post-slot siempre; la tz del schedule es la del que atiende, no la de la cuenta; el passthrough de la confirmation page hay que activarlo explícito; reconciliar semanalmente reservas del scheduler vs filas del CRM (detecta el gotcha 1 a tiempo).

## Credenciales e infra a reusar

PAT del scheduler, org URI, endpoint y signing key del webhook: completá tu propio inventario en `../../reference/infra-y-credenciales.md` (plantilla del kit; nunca commitees valores reales).
