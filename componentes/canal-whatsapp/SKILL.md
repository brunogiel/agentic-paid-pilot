---
name: canal-whatsapp
description: >
  Componente del kit de leadgen: montar un canal de WhatsApp atendido por un LLM para
  un piloto (responder consultas, calificar y cargar leads al CRM). Usar cuando el
  pedido suene a "configurame el WhatsApp del piloto", "quiero un bot de WhatsApp que
  atienda leads", "armá el chatbot de WhatsApp", "conectá WhatsApp al funnel", "que el
  WhatsApp responda solo" o variantes. Cubre first principles (línea dedicada, guiones,
  escalamiento, anti-loop), menú de stacks (plataforma gestionada tipo Kapso / stack
  propio bridge+router / API oficial WABA) y la receta del stack probado en reference.md.
---

# Canal WhatsApp para pilotos de leadgen

## Nivel 1: First principles (agnóstico de herramienta)

### Qué problema resuelve
En muchos verticales (sobre todo LATAM y servicios) el lead no llena un form: escribe por WhatsApp. Este componente pone un agente LLM a atender esa línea 24/7: responde consultas con un guion, califica al lead con las preguntas del funnel y lo carga al CRM sin intervención humana. El humano entra recién cuando hay un lead calificado o una conversación que el bot no debe manejar.

### Cuándo conviene
- El tráfico del piloto llega por click-to-WhatsApp (ads de Meta) o el vertical chatea más de lo que llena forms.
- Las consultas son repetitivas y calificables con 3-6 preguntas.
- Querés respuesta inmediata fuera de horario sin pagar un humano de guardia.

### Cuándo NO
- Venta consultiva donde cada respuesta compromete legalmente al negocio (el bot no puede prometer).
- Volumen tan bajo (menos de 2-3 chats/día) que un humano con quick replies lo resuelve mejor y sin riesgo.
- Si todavía no hay guion claro de qué se responde: primero atendé a mano 10-20 chats y destilá el guion de ahí.

### Invariantes (sin esto no sale a producción)
- **Línea dedicada**: el bot corre en un número propio del piloto. NUNCA en la línea personal del dueño ni en la comercial principal del cliente.
- **Un guion por caso de uso**, versionado en un archivo: rol, qué puede prometer, qué no, tono, preguntas de calificación.
- **Escalamiento a humano definido**: el guion dice explícitamente cuándo se corta el bot y quién sigue (y el bot lo comunica: "te contacta una persona real hoy mismo").
- **Anti-loop**: detección de despedidas (no contestar "gracias" con otro "de nada" infinito), spam/phishing muteado, y estado sticky por chat para no reprocesar.
- **Los errores del LLM nunca llegan al chat como respuesta**: un 401, "credit balance too low" o timeout se suprime, el chat queda en hold y se alerta al dueño por otro canal. Un lead real no puede recibir un error de auth como "respuesta".
- **Un solo dueño por chat**: un único proceso responde cada mensaje. Dos bots o bot+humano simultáneos sin coordinación = respuestas duplicadas.
- **Regla dura para routers multi-caso**: si el número atiende varios casos de uso, el fallback de "no reconocido" va a **hold silencioso**, nunca a un funnel de negocio como default. Anécdota real: un bot cuyo default era el funnel de un piloto ya cerrado le respondió 3 veces, con el pitch del negocio, en un chat ajeno que nada tenía que ver. Si el número atiende UN solo caso, el riesgo es menor (todo lo que entra es de ese caso), pero el hold para lo raro sigue siendo más sano que forzar una respuesta.
- **Registro de leads validado server-side**: lo que el bot extrae (industria, facturación, etc.) se valida contra listas cerradas antes de tocar el CRM; el LLM propone, el endpoint valida.

### Success metrics
- Primera respuesta en < 1 minuto, 24/7.
- 100% de los leads calificados cargados al CRM sin intervención manual.
- 0 mensajes de error del LLM/CLI enviados a un chat.
- 0 respuestas del bot en chats ajenos al caso de uso.
- El humano solo entra en chats escalados o leads ya calificados.

## Nivel 2: Menú de stack sugerido

| Opción | Qué es | Trade-offs | Cuándo tiene sentido |
|---|---|---|---|
| **(a) Plataforma gestionada (ej. Kapso)** | SaaS sobre la API oficial de WhatsApp: agentes AI, workflows, webhooks, logs, panel y hosting resueltos. Kapso (jul-2026): Free US$0 (2.000 msgs/mes, 1 número + sandbox), Pro US$25/mes (100K msgs, 3 números), Platform US$299/mes; los cargos de conversación/template de Meta van aparte, directo a tu cuenta de Meta. **Verificar pricing vigente antes de decidir.** | + velocidad de setup, sin infra propia, compliance API oficial. − lock-in, menos control del loop del LLM, costo Meta por conversación. | Querés el canal andando en días, nadie del equipo quiere mantener infra, o el cliente necesita panel/equipo. |
| **(b) Stack propio: bridge Go (whatsmeow) + daemon router Python + CLI del LLM** ← **usado en un piloto real de referencia** (leadgen de servicios contables) | Bridge no oficial que vincula un WhatsApp común (QR, como WhatsApp Web) y guarda mensajes en SQLite; un daemon los pollea, rutea por funnel y responde invocando la CLI del LLM (un modelo barato tipo Haiku alcanza). En ese piloto atendió leads en dos idiomas, calificó y cargó al CRM solo; costo de infra ~0. | + control total del prompt/modelo, costo ~0, sin aprobación de templates. − requiere una máquina siempre prendida, permisos del sistema (TCC en macOS), mantenimiento propio, API no oficial (riesgo teórico de baneo del número: por eso línea dedicada). | Piloto barato y rápido, ya tenés una máquina always-on, querés iterar el guion sin fricción y tolerás perder el número en el peor caso. |
| **(c) API oficial WhatsApp Business (WABA) + n8n o backend propio** | Número verificado de empresa sobre la Cloud API de Meta: webhooks a n8n/tu backend, templates aprobados para iniciar conversaciones, costo por conversación de Meta. | + compliance total, podés INICIAR conversaciones (templates), cero riesgo de ban por automatización. − setup más largo (Business Manager verificado, aprobación de templates), pagás por conversación, más piezas que mantener que (a). | El canal es estratégico y de largo plazo, necesitás outbound (recordatorios, reactivación) o el volumen/riesgo hacen inaceptable la vía no oficial. |

Son sugerencias, no obligaciones. Antes de elegir, vale buscar si apareció una opción nueva o mejor (el espacio de plataformas de agentes sobre WhatsApp se mueve rápido).

## Nivel 3: Puntero a la receta

Si elegís la opción probada (b), seguí **[reference.md](reference.md)**: checklist punta a punta desde conseguir el chip hasta el smoke test, con los gotchas reales de operar ese stack.

## Output esperado
- Línea de WhatsApp dedicada respondiendo con el guion del caso de uso, 24/7.
- Leads calificados cargados al CRM del piloto (endpoint `/api/lead` o equivalente) con campos validados.
- Log operativo donde se ve cada respuesta enviada y cada lead cargado.
- Alerta al dueño ante errores de LLM/CLI (nunca al chat).

## Success metrics
Las del Nivel 1: primera respuesta < 1 min, 100% leads al CRM sin mano, 0 errores al chat, 0 respuestas en chats ajenos.
