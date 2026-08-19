---
name: agendamiento
description: >-
  Componente del kit de leadgen: agendamiento de calls con el lead (scheduler + webhook al CRM + atribución).
  Usar cuando el usuario diga "configurame el Calendly", "quiero que agenden una call", "el link de agenda",
  "que la reserva caiga en el CRM", "el webhook de reservas", "prefill del email en la agenda", "recordatorios
  de la call", "no me cuenta las agendas". Cubre: setup del evento con mínima fricción, prefill por query,
  webhook server-side, deduplicación pixel/CAPI con event_id, y atribución por match de email.
---

# Agendamiento

## 1. First principles

### Qué problema resuelve

Convertir el email capturado en una call agendada, y que esa reserva quede REGISTRADA en tu CRM con atribución correcta. La agenda es el momento de la verdad del funnel de servicios: todo lo anterior (ads, landing, nurture) existe para llegar acá.

Dos mitades del problema:
1. **Conversión**: que el que hizo clic llegue a un slot con la menor fricción posible.
2. **Registro**: que la reserva dispare tu maquinaria (fila en el CRM, aviso al equipo, evento de conversión a las plataformas de ads) sin depender del reporting de la herramienta de agenda.

### Cuándo conviene y cuándo NO

- Conviene cuando el cierre pasa por una call (servicios, tickets altos, venta consultiva).
- **NO** para funnels donde el lead se trabaja por chat o teléfono directo (mercados donde nadie agenda: mejor un canal conversacional, ver componente WhatsApp).
- **NO** metas calificación pesada antes del slot en un piloto: cada pregunta pre-slot baja la conversión. Primero conseguí agendas, después filtrá.

### Invariantes (sí o sí, sin esto no funciona)

- **Mínima fricción pre-slot**: el camino clic→slot no pide nada que ya tengas. Las preguntas de calificación se recuperan en la call o por nurture, no como peaje para agendar.
- **Prefill por query param** (`?email=...&name=...`): el usuario que ya dejó el email NO lo re-tipea.
- **Webhook server-side de reservas** (created + canceled) hacia tu backend, con firma verificada. La reserva escribe en TU CRM; el dashboard de la herramienta no es tu sistema de registro.
- **event_id compartido browser/CAPI**: el ID único de la reserva (UUID que da la herramienta) viaja como `event_id` tanto en el evento del pixel como en el server-side, para que la plataforma dedupliqué y no cuentes doble.
- **Atribución por match de email en el CRM**: la reserva se une al lead por email. NO confiar en que la herramienta de agenda arrastre UTMs (a veces lo hace, a veces no; el email siempre está).
- **Redirect post-reserva con passthrough**: después de reservar, el usuario cae en una página tuya con los query params arrastrados (ahí disparás el evento de conversión browser-side).
- **Monitoreo del webhook**: un chequeo de que sigue vivo. Gotcha real: si el webhook muere, las reservas SIGUEN entrando pero dejás de verlas en el CRM. Cero filas nuevas ya no significa cero reservas.

### Success metrics

- 100% de las reservas del scheduler tienen fila/actualización en el CRM (conciliar herramienta vs CRM semanalmente).
- Conversión de la página de booking (llegó al widget → reservó) medible y > 30% como referencia sana con prefill.
- 0 conversiones dobles en las plataformas de ads (dedupe por event_id verificado).
- Show-rate de las calls con recordatorios activos.

## 2. Menú de stack sugerido

| Opción | Trade-offs | Cuándo tiene sentido |
|---|---|---|
| **Calendly (plan pago)** ⭐ probada en un piloto real de referencia | Setup en minutos, prefill y redirect nativos, recordatorios email+SMS. ⚠ Webhooks SOLO en plan pago; el setup del evento es solo UI (la API no crea preguntas ni workflows) | Piloto rápido, el que atiende ya conoce Calendly, presupuesto para el plan (o trial) durante toda la campaña |
| **Cal.com** | Open source, webhooks en el plan free, self-hosteable. Menos pulido, un vendor menos conocido para el que atiende | Piloto largo o sin presupuesto para SaaS: el gotcha del webhook pago desaparece |
| **Booking nativo del CRM** (HubSpot Meetings, etc.) | Reserva y CRM en el mismo sistema: atribución gratis. Solo si el negocio ya paga ese CRM | El equipo comercial ya vive en un CRM con scheduler incluido |
| **Agenda conversacional (WhatsApp/teléfono)** | Cero fricción de herramienta en mercados donde nadie agenda solo. Todo el registro es manual o por bot propio | El ICP no usa schedulers (común en LATAM consumer/PyME). Ver componente WhatsApp |

Cómo rindió Calendly en un piloto real de referencia: el flujo email→prefill→slot funcionó bien y el webhook registró las reservas en el CRM con aviso al equipo y evento server-side a la plataforma de ads. Dos lecciones caras: (1) a mitad de piloto se SACARON las preguntas de calificación del booking para bajar fricción (la calificación se recuperó en la call); (2) al vencer el trial la cuenta cayó a Free y el webhook murió EN SILENCIO: las reservas seguían entrando pero ya no se escribían en el CRM. Presupuestar el plan pago por toda la campaña o elegir Cal.com.

**Son sugerencias, no obligaciones. Antes de elegir, vale buscar si apareció una opción nueva o mejor.**

## 3. Puntero a la receta

Si elegís la opción probada (Calendly pago + webhook a tu backend/n8n), seguí **[reference.md](reference.md)**: checklist del evento en UI, qué se puede hacer por API y qué no, el curl del webhook con signing key, el formato del link con prefill y los gotchas.

## Cómo se usa (flujo)

1. [DET] Elegir la herramienta del menú según mercado y presupuesto.
2. [DET] Crear el evento: nombre, duración, ubicación (Meet/Zoom), disponibilidad del que atiende (¡su timezone real!), recordatorios email + SMS.
3. [LATENT] Decidir qué se pregunta en el booking (recomendado piloto: solo nombre/email/teléfono) y redactar la descripción del evento.
4. [DET] Cablear el link con prefill desde la landing y el redirect post-reserva a una página propia con passthrough.
5. [DET] Registrar el webhook (created + canceled) hacia el backend con signing key, y conectar: fila CRM + aviso al equipo + evento CAPI con el UUID de la reserva como event_id.
6. [DET] Probar E2E con una reserva real: fila en el CRM, dedupe en la plataforma de ads, recordatorios recibidos, cancelación registrada.

## Output esperado

- Evento de agenda publicado con disponibilidad real del que atiende y recordatorios activos.
- Link con prefill cableado en la landing + redirect post-reserva propio.
- Webhook registrado y verificado: reserva de prueba visible en el CRM y deduplicada en ads.

## Success metrics

Las de First principles: reservas 100% registradas, conversión de booking medible, 0 dobles conteos, show-rate con recordatorios.
