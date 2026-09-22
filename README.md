# lanzar-piloto: validá un negocio nuevo con publicidad, con un tope de inversión

> **Sigue la metodología Lean Startup.** Construir, medir, aprender, con dinero real y un tope que corta cuando los números no dan. Cada etapa cierra con una decisión de matar o perseverar, tomada con un número adelante y no con una corazonada.

¿Tenés una idea de negocio o un servicio nuevo y querés saber si la gente lo va a pagar, antes de invertir una suma importante en publicidad? Este kit le enseña a tu asistente de IA (ChatGPT, Claude, Cursor) un método paso a paso para armar y correr un **piloto**: una prueba chica y controlada de publicidad en Google y Meta, con un tope de inversión para cortar a tiempo si no funciona.

No es una app ni un programa que instalás. Son instrucciones que tu asistente de IA lee y sigue con vos.

Lo que un piloto te deja no son clientes: es una respuesta con números atrás a la pregunta de si esto se puede vender. Cuando la respuesta es que no, el tope de inversión te lo dice temprano y barato. Para eso está.

## Cómo funciona

El método va en 5 etapas. En cada una tu asistente te muestra lo que hizo y te pide el OK antes de seguir (no dispara solo):

1. **Plan.** Arranca el proyecto y define lo básico: qué vendés, a quién, cuánto dinero ponés.
2. **Research.** Investiga el mercado: qué busca la gente en Google, qué anuncios corren tus competidores, qué tan grande es la audiencia. Al final te dice si vale la pena seguir o no.
3. **Experimento.** Arma los números (cuánto te cuesta conseguir un cliente contra cuánto vale ese cliente) y define el tope de inversión del piloto, incluido qué número lo mata, lo pausa o lo escala.
4. **Ejecución.** Escribe los avisos, arma las páginas, configura las campañas y el seguimiento, y deja todo listo para prender.
5. **Operación y cierre.** Ya con las campañas prendidas: te arma el reporte periódico de "cómo venimos", te ayuda a decidir si seguís, pivotás o matás el gate cuando se acaba el presupuesto, y cuando el piloto termina te deja el postmortem + un checklist para apagar todo lo que quedó corriendo.

## La idea de fondo (esto es lo que lo hace distinto)

La mayoría gasta mal en un piloto. El método ordena **dónde se gana o se pierde el dinero**, de lo que más importa a lo que menos:

1. ¿El mercado responde a tu oferta? Es lo único que el piloto realmente prueba.
2. ¿En qué canal ponés el presupuesto? La decisión más cara de todas.
3. Tu oferta y cómo la presentás.
4. Que la página sea clara: la claridad pesa más que la estética.
5. La limpieza de palabras clave. Importa, pero es lo de menos peso.

Y una distinción que te ahorra dinero: hay gasto que es **matrícula** (el precio de aprender algo que no podías saber de antes, se paga sí o sí) y gasto que es **impuesto evitable** (inversión desperdiciada en clics irrelevantes que se corta desde el día uno). El método te ayuda a no confundirlos.

## Cómo lo usás

Es para usar con tu asistente de IA. Le señalás el archivo que necesites y le pedís que lo siga:

- **De punta a punta:** le decís "lancemos un piloto para [tu idea]" y te guía paso a paso por las 5 etapas.
- **Suelto:** también podés pedir una sola parte ("investigá los competidores de X", "armá los números de Y").

## Componentes implementables

Antes de armar el gate de budget (etapa 2), el método arma un **spec de stack**: un documento corto que dice qué piezas del funnel se van a construir y con qué herramienta, antes de tocar código. Las piezas disponibles hoy, cada una con su propio menú de opciones:

| Componente | Qué resuelve |
|---|---|
| Lead magnet + nurture | Entregar una guía/PDF por mail y encadenar una serie automática de mails después. |
| Cold outreach | Escribirle en frío a una lista propia por email, con volumen escalonado y freno automático si algo sale mal. |
| A/B + personalización | Probar variantes de una landing y personalizar el mensaje según de dónde viene el visitante. |
| Captura + CRM | El formulario que junta el lead y lo da de alta en un CRM. |
| Agendamiento | Que el prospecto reserve una llamada solo, sin ida y vuelta de mails. |
| WhatsApp | Atender o calificar leads por WhatsApp con un bot simple. |
| GEO y citación en LLM | Aparecer citado en las respuestas de ChatGPT, Copilot y Perplexity, y medirlo. |

Cada componente sigue la misma lógica que el resto del kit: primero te explica **para qué sirve y cuándo conviene** (sin nombrar una herramienta todavía), después te muestra un menú de 2 a 4 opciones con sus trade-offs, y recién con tu OK baja a la receta paso a paso de la opción elegida.

## No se termina cuando termina el piloto

El piloto es la puerta de entrada, no el techo. Solo **4 de los 16 pasos** existen únicamente para un piloto: el plan inicial, el diseño del experimento, la operación de gates y el postmortem. Todo lo demás te sigue sirviendo con las campañas ya andando:

- **Los 6 roles de `roles/`** son de uso continuo. El auditor de cuentas y el analista de términos de búsqueda no arrancan nada: optimizan lo que ya corre. Lo mismo el rol de medición y el de textos de aviso.
- **Los 7 componentes de `componentes/`** son piezas de funnel que se implementan una vez y quedan. No caducan cuando cierra el gate.
- **El research de keywords, los creativos y el tracking** se rehacen cada vez que abrís una campaña nueva, sea o no un piloto.

El kit está escrito alrededor de un piloto porque es donde la improvisación sale más cara. Ni el método ni las piezas se apagan cuando el piloto termina.

## Qué hay adentro

| Carpeta | Qué es |
|---|---|
| `SKILL.md` | el método principal, el que coordina todo |
| `s0` a `s4b` | cada paso del método, uno por archivo (incluye `s2c`, el spec de stack) |
| `componentes/` | las 7 piezas de implementación de funnel de la tabla de arriba, una carpeta por componente |
| `roles/` | 6 "expertos" de publicidad (Google, Meta, textos de aviso, medición) que el método consulta cuando los necesita |
| `reference/` | referencia compartida (infra y credenciales, arquitecturas de funnel) |
| `templates/` | plantillas en blanco de los documentos que se van llenando (incluye `kickoff-prd-template.md`, para cuando el arranque es una corrida de muchos frentes en paralelo en vez de etapa por etapa) |
| `ejemplo/` | una corrida de muestra (un negocio inventado), para ver cómo queda |

## Un par de términos que vas a ver

- **Piloto:** una prueba chica y controlada de publicidad, con un tope de inversión.
- **Tope (o gate) de budget:** un freno. Prendés solo una parte del presupuesto y el resto queda apagado hasta que los números den bien. Sirve para cortar antes de gastar todo.
- **Landing:** la página a la que llega la gente cuando hace clic en un aviso.
- **CAC / LTV:** lo que te cuesta conseguir un cliente contra lo que ese cliente te deja en total. Si el segundo es bastante más grande que el primero, el negocio cierra.

---

## Para técnicos

Kit de *skills* (formato `SKILL.md`) para asistentes de IA. Un orquestador *thin* + 16 *child skills*, una por sub-etapa (incluye `s2c-spec-stack`, el PRD del stack adaptado de BMAD), con doctrina thin-harness / fat-skills: el orquestador solo coordina y gatea, el trabajo vive en las child skills. Además, `componentes/` suma 7 piezas reusables de implementación de funnel (workers, no etapas), cada una con 3 niveles: first principles agnósticos de herramienta, menú de stack con trade-offs, y receta (`reference.md`) de la opción probada. Pasos marcados `[LATENT]` (razonamiento), `[DET]` (determinístico) y `[FANOUT]` (subagentes en paralelo). Scripts en `scripts/` (no embebidos), parámetros sin hardcodear, success metrics por skill. Pensado para Claude Code / Cursor, pero cualquier asistente que lea markdown sirve.
