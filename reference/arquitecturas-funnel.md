# Menú de arquitecturas de funnel

> **Qué es esto:** el menú de las 6 formas típicas de encadenar "alguien vio el ad" → "alguien firmó". Se consulta ANTES de modelar el funnel (`s2a-modelar-funnel` Paso 1) y es el insumo principal de `s2c-spec-stack` para elegir arquitectura. No es una plantilla de copy ni de tracking: es la forma del embudo, la decisión de la que salen los componentes que hacen falta.

---

## Tabla resumen

| # | Arquitectura | Qué es | Cuándo conviene | Cuándo NO | Componentes que exige | Evidencia real disponible |
|---|---|---|---|---|---|---|
| 1 | **Form-first directo** | Landing con formulario (1 o 2 pasos) que prefiltra y manda directo al CRM, sin pasos intermedios | Decisión de compra simple, ciclo corto, tráfico ya tibio (branded, referido, retargeting) | Decisión de alta confianza o ciclo largo: el form solo no genera la confianza que hace falta para completarlo | `captura-y-crm` | En un piloto real de referencia (leadgen para servicios contables), esta fue la primera arquitectura corrida (form de 2 pasos con prefiltro). Terminó siendo el primero de 3 pivots de arquitectura del piloto |
| 2 | **Agendamiento directo** | El CTA único de la landing lleva directo a un calendario (Calendly/Cal.com), sin capturar el email antes | Servicio donde la call en sí es el próximo paso natural y de bajo riesgo percibido (diagnóstico gratis, consulta corta) | Si agendar una call todavía es un salto grande para el visitante frío, la fricción de "reservar 30 min con un desconocido" mata la conversión antes de sacarle el mail | `agendamiento` | El modelo original acordado con la cliente en ese mismo piloto (2 calls directas por Calendly, sin guía ni nurture) **nunca se corrió tal cual se diseñó**: se pasó a versiones de funnel más largas antes de agotar la más simple. Sigue siendo una pregunta abierta del caso |
| 3 | **Email-first** | La landing captura SOLO el email (ni teléfono, ni preguntas de calificación); la calificación se mueve a después, dentro del flujo de agendamiento o del nurture | Tráfico frío que necesita un paso de compromiso más chico antes de agendar; cuando "dejá tu teléfono" en el form frena más que ayuda | Si el volumen de tráfico es bajo, agregar un paso extra entre el click y la conversión real solo resta muestra en cada etapa | `captura-y-crm` + `agendamiento` (después del email) | Fue el funnel final del piloto de referencia (último gate): landing solo-email → Calendly directo, preguntas de calificación sacadas para bajar fricción. CTR y tráfico razonables, **cero agendas del ICP** igual |
| 4 | **Lead magnet + nurture** | La landing ofrece un recurso (guía, checklist) a cambio del email; una secuencia de mails automatizada (días, no horas) construye confianza antes de pedir la call o la compra | Decisión de alta confianza y ciclo largo, donde el visitante necesita varios puntos de contacto antes de comprometerse (ver advertencia abajo) | Compra impulsiva o ventana de decisión corta: el nurture agrega días al funnel justo cuando el prospect ya se enfrió o ya decidió con otro | `lead-magnet-y-nurture` + `captura-y-crm` | Un gate intermedio del piloto de referencia corrió guía descargable + secuencia de 7 mails (en dos idiomas). Capturó algunos emails pero **cero agendas** desde esta arquitectura puntual. Hubo algo de apertura/clic en los primeros mails, sin traducirse en ninguna conversión real; la muestra por mail era chica para sacar conclusión dura |
| 5 | **Tripwire** | Un compromiso chico y de bajo riesgo (auditoría gratis, diagnóstico acotado) sirve de escalón antes del pedido grande, para generar momentum/reciprocidad | Cuando el servicio real tiene un precio o compromiso alto y un primer paso gratis achica la barrera sin regalar el valor completo | Si armar y operar el tripwire cuesta más esfuerzo que la mejora de conversión que trae, o si el nombre del tripwire genera la defensiva que se supone que evita | `captura-y-crm` (el tripwire vive como parte del copy/CTA, no como componente aparte) | El piloto de referencia no lo corrió como arquitectura separada, pero usó un nombre de oferta gratuita tipo "revisión de libros gratis" como tripwire de baja fricción dentro del funnel email-first. Lección real (no de esta arquitectura en particular, pero aplica): un nombre de oferta que suena a auditoría genera defensiva antes de leer el resto |
| 6 | **WhatsApp-first** | La captura inicial pasa por un chat de WhatsApp (bot o router con guiones) en vez de un formulario web | Audiencia acostumbrada a mensajería (mercados LatAm), producto/servicio que se explica mejor conversacional que en una landing | Necesita infra de bot/router propia; un fallback mal diseñado puede rutear mal chats que no son del funnel | `canal-whatsapp` | El piloto de referencia tuvo una línea de WhatsApp dedicada, pero solo como canal secundario de uno de los segmentos, no como captura principal. Incidente real documentado: el router tenía ese funnel como default, así que un chat no reconocido cayó ahí y el bot respondió solo en una conversación ajena a ese negocio. Lección dura: el fallback de "no reconocido" va a hold silencioso, nunca a un funnel de negocio específico |

---

## Regla de combinación

Las arquitecturas no son mutuamente excluyentes: se combinan como capas de un mismo funnel, no como alternativas que se prueban una y se descartan las otras cinco.

- **Email-first + lead magnet como rescate**: el CTA principal va directo a agendamiento (email-first puro), y el que no agenda cae en un pop-up de salida o remarketing que ofrece el lead magnet como red de contención. Es la combinación que terminó corriendo el piloto de referencia en su versión final (landing solo-email con guía como exit-intent, no como oferta principal).
- **Form-first + WhatsApp-first por segmento**: mismo funnel, canal de captura distinto según el idioma o la geografía del segmento (ej. formulario para el segmento que llega por Google, WhatsApp para el que llega por un canal más conversacional).
- **Tripwire dentro de cualquiera de las otras cinco**: no es una arquitectura standalone, es un ajuste de framing del CTA que se monta sobre form-first, agendamiento directo o email-first.

La combinación se define y se deja explícita en `2c.spec-stack.md`, nunca a mitad de camino sin registrar por qué se sumó una capa.

---

## Advertencia: el lead magnet alarga el funnel

Sumar un lead magnet + nurture agrega días (no minutos) entre el primer contacto y la conversión real. Eso es una ventaja SOLO si la decisión de compra es de alta confianza o de ciclo largo: ahí el tiempo extra se usa para construir la confianza que la venta necesita de todos modos. Para una compra de decisión rápida o impulsiva, ese mismo tiempo extra es pura fricción: el prospect se enfría, decide con otro, o simplemente se olvida.

Antes de sumar `lead-magnet-y-nurture` al funnel, la pregunta que hay que poder contestar en `2c.spec-stack.md` es: **¿por qué esta decisión necesita más de un contacto para cerrarse?** Si la respuesta es "por si acaso" o "total no cuesta nada armarlo", no corresponde. En el piloto de referencia se sumó apostando a que la fricción estaba en la falta de confianza del prospect; el postmortem de ese piloto no llegó a una conclusión cerrada de si esa apuesta era correcta (cero agendas también en el funnel más corto que vino después).

---

Estas 6 son las arquitecturas típicas, no las únicas posibles. Si el negocio tiene una restricción real que las vuelve insuficientes (ej. el ICP directamente no usa email), vale buscar o inventar una variante antes de forzar una de esta lista.
