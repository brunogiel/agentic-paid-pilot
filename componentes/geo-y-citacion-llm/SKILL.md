---
name: geo-y-citacion-llm
description: >-
  Componente del kit de leadgen: aparecer citado en las respuestas de los motores generativos (ChatGPT,
  Copilot, Perplexity, AI Overviews) y poder medirlo. Usar cuando el usuario diga "quiero que ChatGPT
  me recomiende", "GEO", "LLMSEO", "aparecer en las respuestas de IA", "me llegó un lead por ChatGPT",
  "cómo mido si me citan", "hay que dar de alta el sitio en Bing", "los bots de IA me están bloqueados",
  "meter contenido para que nos encuentren". Cubre: qué motor se sirve de qué índice, los fixes técnicos
  que habilitan la citación, el formato de contenido que se cita, y el método de medición semanal.
  NO cubre SEO tradicional de Google ni compra de medios.
---

# GEO y citación en LLM

## 1. First principles

### Qué problema resuelve

Una parte creciente de la gente ya no busca en Google: le pregunta a un modelo. El lead que entra por ahí llega **habiendo leído una recomendación, no un anuncio**, y eso se nota en la calidad: entra convencido y el ciclo se acorta.

El componente cubre dos cosas que se confunden:

1. **Habilitar la citación.** Fixes técnicos que definen si el motor puede siquiera leerte. Son baratos, son casi todos de una vez, y su ausencia te deja afuera sin aviso.
2. **Ganarte la cita.** Contenido en formato de pregunta, cubriendo **sub-preguntas distintas** alrededor del mismo problema.

**El principio central: la palanca es la cobertura de intención, no la repetición.** Repetir literalmente la misma frase clave **baja** la tasa de citación alrededor de un 10%. Cubrir las sub-preguntas del tema con variantes reales la sube 49%, y 161% junto con la pregunta principal. Quien viene del SEO viejo trae el instinto contrario y lo aplica en piloto automático.

### Cuándo conviene y cuándo NO

- **Los fixes técnicos: siempre, y desde el día uno.** Cuestan una hora y hay uno que es puro downside: si el WAF o una regla genérica de Cloudflare bloquea los bots de búsqueda en vivo, estás afuera de las respuestas y no te enterás nunca.
- **El contenido: cuando la landing definitiva ya existe.** En un piloto con landing provisoria, escribir guías es trabajo que se tira en el cambio. Los fixes valen igual; el contenido espera.
- **NO** si el vertical se busca por marca y no por problema. GEO paga cuando la gente le describe su problema a un modelo, no cuando ya sabe a quién quiere.
- **NO** como reemplazo de paid en la ventana del piloto. Es un canal de acumulación: el caso más rápido medido tardó cuatro días, pero eso fue con un dominio que ya existía y ya estaba indexado.
- **NO** confundirlo con las respuestas de IA de Google, que corren sobre índice propio. Para eso manda el SEO de siempre, no esto.

### Qué motor se sirve de qué

| Motor | ¿Bing es la palanca? | Qué usa |
|---|---|---|
| Microsoft Copilot | Sí, directo | Bing |
| ChatGPT | Piso necesario, ya no único | Bing + crawler propio (`OAI-SearchBot`) |
| Perplexity | Complemento decreciente | Índice propio desde ~Q1 2026 |
| Google AI Overviews / AI Mode | **No** | Índice propio de Google |
| Claude | **No aplica** | Brave Search (indicios fuertes, sin confirmación oficial) |

### Invariantes (sí o sí, sin esto no funciona)

- **Los bots de búsqueda en vivo pasan.** `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Claude-SearchBot` nunca bloqueados. Son distintos de los de entrenamiento (`GPTBot`, `ClaudeBot`, `Google-Extended`), que se pueden bloquear sin perder citas. **Confundirlos es el error que más caro sale y el que menos se nota.**
- **Un solo dominio canónico, y coherente.** El `canonical`, el `sitemap` y el destino de los redirects dicen lo mismo. Un canonical que apunta a una URL que redirige a otra es peor que no tener canonical.
- **Cada pregunta, su URL.** Un acordeón de FAQ en la home es una sola oportunidad de cita. Diez páginas son diez.
- **La respuesta directa va primero y se sostiene sola**, fuera del contexto de la página. Es lo que el motor levanta como cita.
- **Se mide antes de tocar nada.** Sin la foto del antes no se puede atribuir ninguna mejora después, y el canal queda como anécdota en vez de como número.
- **El contenido de un rubro regulado lo aprueba alguien del rubro.** En legales, salud o finanzas, un dato mal puesto no es un error de posicionamiento.

### Success metrics

- Los tres user-agents de búsqueda en vivo devuelven 200 en todas las URLs públicas.
- El sitio está en Bing Webmaster Tools y su sitemap aceptado.
- `canonical`, `sitemap` y redirects apuntan al mismo dominio.
- Hay un set fijo de 15-20 prompts por sitio corriendo semanalmente, con su baseline tomado **antes** del primer cambio.
- El reporte periódico lleva dos números: tasa de citación y menciones de marca.

## 2. Menú de implementación

Por orden de rendimiento sobre hora de trabajo:

1. **Auditar robots.txt, WAF y CDN.** Lo más barato y lo que más daño evita.
2. **Alta en Bing Webmaster Tools**, importando desde Search Console. Gratis, cinco minutos, es el gate.
3. **Analytics**: el canal nativo de asistentes de IA, más un canal manual para los que no vengan en la lista oficial. Sin esto no hay reporte.
4. **Contenido por variantes de intención**, una URL por pregunta madre, con datos estructurados de FAQ.
5. **Datos estructurados** de la organización y del servicio.
6. **IndexNow** para acelerar la indexación. Acelera el descubrimiento, no es una palanca de citación en sí.
7. `llms.txt`: **descartable.** Ningún proveedor grande confirmó que lo lea.

## 3. Medir el lado técnico desde afuera: `is-agentic`

```bash
npx -y is-agentic@latest {dominio}          # reporte legible en la terminal
npx -y is-agentic@latest {dominio} --json   # el mismo reporte como JSON
```

Escanea un dominio público y devuelve un `score` sobre 100 con los checks que no pasaron y el fix de cada uno. Tarda ~20-25 s, es gratis y no pide cuenta. El informe web queda en `https://is-agentic.com/scan/{dominio}`. Hay además una API de solo lectura, `GET https://is-agentic.com/api/v1/report?url=https://{dominio}`, que sirve el último reporte **ya corrido**: sobre un dominio que nadie escaneó devuelve 404, porque no dispara scans. El CLI sí los dispara, y después la API ya lo tiene.

**Qué mide y qué no.** Mide si un agente que llega al sitio puede leerlo y confiar en él: identidad en JSON-LD, páginas de About / Contact / Privacy con contenido real, un 404 que se comporta, negociación de contenido en Markdown, y un archivo de instrucciones para agentes. **No mide citación.** Un score alto no dice que un motor te recomiende, y el único check que se le acerca (`brand-search-accuracy`) depende de que la marca ya esté indexada, así que en un dominio nuevo falla por definición. Sirve para lo que esta sección no tenía: convertir "los fixes técnicos están hechos" en un número reproducible, con foto del antes y del después.

**Dónde entra en el piloto.** Los requisitos se construyen en `s3b-build-landings` (van en el prompt de build) y el score se registra en `s3f-pre-launch-validation`, como ítem que se anota y no bloquea. Es también la foto del "antes" que pide el invariante de medición, para el lado técnico.

**Y la corrección que trae sobre `llms.txt`.** El menú de arriba lo da por descartable y, **para citación, lo sigue siendo**: ningún proveedor grande confirmó que lo lea. El scan lo premia por otro motivo — su check `agent-instruction` busca un archivo que diga **cuándo** conviene usarte, y ese archivo suele ser el mismo. Descartable como palanca de citación, barato como instrucción para el agente que ya llegó. Son dos objetivos distintos y conviene no mezclarlos.

## 4. Tensión conocida con `lead-magnet-y-nurture`

Ese componente define que el blog de respaldo arranca **`noindex` por default**, y dice explícitamente que su rol en un piloto no es SEO. Era la decisión correcta cuando el único beneficio de indexar era posicionar a meses vista.

Hoy tiene un costo que antes no tenía: **un blog en `noindex` tampoco puede ser citado por un motor generativo**, y esa citación no tarda meses. **La tensión queda anotada, no resuelta**: si el piloto va a apoyarse en GEO, la decisión de `noindex` deja de ser gratis y hay que tomarla a propósito, no por default.

## 5. Troubleshooting

- **"No aparecemos y hace semanas que publicamos."** Antes de tocar contenido, verificar que los bots de búsqueda en vivo no estén bloqueados y que el canonical no apunte a otro dominio. El 90% de las veces está ahí.
- **"Publicamos veinte variantes de la misma pregunta y bajó."** Es el efecto esperado. Son veinte preguntas distintas, no la misma veinte veces.
- **"El caso que vi tardó cuatro días, el nuestro no arranca."** Ese caso corrió sobre un dominio ya indexado. Un dominio nuevo no tiene ese piso.
- **"Medimos y da cero."** Antes de concluir, revisar que los prompts del set correspondan a la intención real del producto. Un set escrito para la categoría equivocada da cero para siempre y ese cero no dice nada.
- **"El scan nos da 80 y nadie nos cita."** Son dos cosas distintas. El scan mide si un agente puede leerte; la cita se gana con cobertura de intención (sección 1). El score alto es condición, no causa.
