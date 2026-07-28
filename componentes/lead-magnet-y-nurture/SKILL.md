---
name: lead-magnet-y-nurture
description: Arma el imán de leads (guía/checklist descargable) y la cadena de mails que calienta a quien lo pidió hasta que agenda o se descarta. Usar cuando querés "un lead magnet", "la cadena de mails", "una guía para capturar emails", "configurar el nurture del piloto", "qué ESP usar para la secuencia", "el drip de mails", o cuando el funnel tiene gente que deja el mail pero no agenda todavía.
---

# Lead magnet + nurture

## Nivel 1 · First principles

**Qué problema resuelve:** captura el email de alguien con intención real pero que todavía no está listo para hablar, le entrega algo de valor genuino a cambio (guía, checklist, mini-curso) y lo calienta con una secuencia automática de mails hasta que agenda, compra o se descarta solo.

**Cuándo conviene:**
- El ciclo de venta no es instantáneo: la mayoría de quien llega al funnel no agenda en la primera visita.
- Hay algo de valor real para regalar (no un PDF genérico de relleno): un checklist, una guía, una calculadora.
- El volumen de leads justifica automatizar (a mano, una cadena de 7 mails a 3 personas no se nota; a 300, sí).

**Cuándo NO conviene:**
- El producto se compra en la misma visita (ecommerce de impulso, urgencia real): el nurture solo agrega fricción.
- No hay nadie para escribir contenido de valor real en los mails: una cadena vacía de "¿todavía estás ahí?" quema la lista.
- El volumen es tan bajo (2-3 leads/semana) que un mail manual personalizado rinde más que armar toda la infraestructura.

**Invariantes (esto tiene que estar sí o sí):**
1. **La cadena la manda el ESP (Mailchimp/MailerLite/Brevo/etc.), nunca el orquestador de infra (n8n, Zapier, un backend propio).** El orquestador hace UNA sola cosa: dar de alta al suscriptor en el grupo/lista correcta (upsert por email). El "se unió al grupo" es lo que dispara la automation completa dentro del ESP. Si el orquestador intenta mandar los mails él mismo, se pierde open/click tracking nativo y se reinventa un motor de mails a mano.
2. **El lead magnet no se muestra ni se descarga en la página.** Se entrega por mail. Esto fuerza la primera apertura real (primera señal de engagement) y de paso valida que el email existe: un email inválido nunca recibe nada, así que no hace falta un gate de confirmación aparte.
3. **Opt-in coherente con el punto anterior:** si el magnet solo se entrega por mail (nunca se descarga en la página), single opt-in alcanza, porque el propio flujo ya filtra los emails falsos. Si el magnet se descarga directo en la página, ahí sí conviene doble opt-in.
4. **Cadena corta con cierre duro en una fecha definida** (ej. día 7): entrega inmediata el día 1, un mail por día, y un pedido explícito de agendar/comprar al final. Después del cierre, el que no actuó queda en el grupo para envíos manuales u ocasionales, no una automation infinita de goteo.
5. **UTMs por mail** (`utm_content=d1-guia`, `d2-señal`, etc.) para saber qué mail de la cadena tracciona cada click, no solo que "el nurture" funcionó en general.
6. **Todos los que capturan el email entran a la misma cadena al arrancar** (no bifurcar por intención desde el día uno: eso es optimización de fase 2). La única excepción razonable es sacar del cierre duro final a quien ya agendó o compró, para no insistirle con algo que ya hizo.

**Success metrics:**
- % que abre el mail 1 (mide si el asunto + la entrega real funcionan).
- % que llega vivo hasta el mail de cierre (mide si la cadena retiene o la gente se da de baja).
- % que agenda/compra desde algún punto de la cadena, y en qué mail (`utm_content`) lo hizo.
- Open/click rate por mail individual, no solo agregado de la cadena.
- Lista bajo el techo del plan free del ESP elegido (si se acerca, hay que decidir upgrade o poda de inactivos antes de que rompa el envío).

## Nivel 2 · Menú de stack sugerido

| Opción | Cómo funciona | Cuándo tiene sentido |
|---|---|---|
| **ESP con automation visual gratis** (ej. MailerLite) | Grupos disparan automations multi-paso por API; opens/clicks nativos; node oficial en n8n | Lista chica-mediana, arranque rápido, sin presupuesto. Techo de suscriptores en el free tier a vigilar |
| **ESP con contactos ilimitados pero cap diario de envío** (ej. Brevo) | Igual que arriba pero sin techo de subs, con un tope de mails/día en el free tier | Lista que puede crecer mucho en subs pero con volumen diario bajo/medio; el cap diario es el riesgo si entra un pico de leads |
| **Transaccional puro** (ej. Resend, Postmark) | Manda mails 1 a 1 por API, sin automations ni secuencias propias; alguien más tiene que armar el scheduling | Solo para el mail #1 de entrega inmediata, o cuando ya existe un orquestador (n8n) dispuesto a manejar los delays a mano. No trackea opens sin trabajo extra |
| **Suite de creators** (ej. Kit/ConvertKit) | Automations orientadas a newsletters, límite alto de subs | Cuando el nurture se parece más a contenido editorial recurrente que a una cadena de venta corta |

En un piloto real de referencia se usó un **ESP con automation visual gratis** (tipo MailerLite): automations visuales completas en el free tier, node nativo en n8n para el upsert, y la UX más simple de las evaluadas. Rindió bien para una cadena diaria de 7 mails con volumen chico-mediano; el riesgo que quedó abierto fue el techo de suscriptores del free tier, que hay que vigilar si el piloto escala.

Son sugerencias, no obligaciones. Antes de elegir, vale buscar si apareció una opción nueva o mejor.

## Nivel 3 · Receta

Si elegís la opción probada (ESP con automation visual gratis, tipo MailerLite), seguí [reference.md](reference.md).

## Output esperado

- El lead magnet (PDF o equivalente) generado y alojado, con el link de descarga solo dentro del mail #1.
- La página que captura el email (sin mostrar el magnet).
- El ESP configurado: grupo(s), campos custom, automation con los N mails y sus delays, UTMs por paso.
- El nodo de alta (upsert + join-group) en el orquestador que ya exista (n8n u otro), disparando al capturar el email.

## Success metrics

Ver invariante final de Nivel 1: open rate del mail 1, retención hasta el cierre, tasa de conversión por `utm_content`, techo del plan del ESP no superado.
