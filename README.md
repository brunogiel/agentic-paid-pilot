# lanzar-piloto: probá un negocio nuevo con publicidad, sin gastar de más

¿Tenés una idea de negocio o un servicio nuevo y querés saber si la gente lo va a pagar, antes de invertir un montón en publicidad? Este kit le enseña a tu asistente de IA (ChatGPT, Claude, Cursor) un método paso a paso para armar y correr un **piloto**: una prueba chica y controlada de publicidad en Google y Meta, con un tope de plata para cortar a tiempo si no funciona.

No es una app ni un programa que instalás. Son instrucciones que tu asistente de IA lee y sigue con vos.

## Cómo funciona, en criollo

El método va en 4 etapas. En cada una tu asistente te muestra lo que hizo y te pide el OK antes de seguir (no dispara solo):

1. **Plan.** Arranca el proyecto y define lo básico: qué vendés, a quién, cuánta plata ponés.
2. **Research.** Investiga el mercado: qué busca la gente en Google, qué anuncios corren tus competidores, qué tan grande es la audiencia. Al final te dice si vale la pena seguir o no.
3. **Experimento.** Arma los números (cuánto te cuesta conseguir un cliente contra cuánto vale ese cliente) y define el tope de plata del piloto.
4. **Ejecución.** Escribe los avisos, arma las páginas, configura las campañas y el seguimiento, y deja todo listo para prender.

Después de prender hay una etapa 5 opcional, para ir mejorando las campañas con el tiempo.

## La idea de fondo (esto es lo que lo hace distinto)

La mayoría gasta mal en un piloto. El método ordena **dónde se gana o se pierde la plata**, de lo que más importa a lo que menos:

1. ¿El mercado responde a tu oferta? Es lo único que el piloto realmente prueba.
2. ¿En qué canal ponés la plata? La decisión más cara de todas.
3. Tu oferta y cómo la presentás.
4. Que la página sea clara (clara le gana a "linda").
5. La limpieza de palabras clave. Importa, pero es lo de menos peso.

Y una distinción que te ahorra plata: hay gasto que es **matrícula** (el precio de aprender algo que no podías saber de antes, se paga sí o sí) y gasto que es **impuesto evitable** (plata tirada en clics basura que se corta desde el día uno). El método te ayuda a no confundirlos.

## Cómo lo usás

Es para usar con tu asistente de IA. Le señalás el archivo que necesites y le pedís que lo siga:

- **Todo de una:** le decís "lancemos un piloto para [tu idea]" y te lleva de la mano por las 4 etapas.
- **Suelto:** también podés pedir una sola parte ("investigá los competidores de X", "armá los números de Y").

## Qué hay adentro

| Carpeta | Qué es |
|---|---|
| `SKILL.md` | el método principal, el que coordina todo |
| `s0` a `s3f` | cada paso del método, uno por archivo |
| `roles/` | 6 "expertos" de publicidad (Google, Meta, textos de aviso, medición) que el método consulta cuando los necesita |
| `templates/` | plantillas en blanco de los documentos que se van llenando |
| `ejemplo/` | una corrida de muestra (un negocio inventado), para ver cómo queda |

## Un par de términos que vas a ver

- **Piloto:** una prueba chica y controlada de publicidad, con un tope de plata.
- **Tope (o gate) de budget:** un freno. Prendés solo una parte de la plata y el resto queda apagado hasta que los números den bien. Sirve para cortar antes de gastar todo.
- **Landing:** la página a la que llega la gente cuando hace clic en un aviso.
- **CAC / LTV:** lo que te cuesta conseguir un cliente contra lo que ese cliente te deja en total. Si el segundo es bastante más grande que el primero, el negocio cierra.

---

## Para técnicos

Kit de *skills* (formato `SKILL.md`) para asistentes de IA. Un orquestador *thin* + 13 *child skills*, una por sub-etapa, con doctrina thin-harness / fat-skills: el orquestador solo coordina y gatea, el trabajo vive en las child skills. Pasos marcados `[LATENT]` (razonamiento), `[DET]` (determinístico) y `[FANOUT]` (subagentes en paralelo). Scripts en `scripts/` (no embebidos), parámetros sin hardcodear, success metrics por skill. Pensado para Claude Code / Cursor, pero cualquier asistente que lea markdown sirve.
