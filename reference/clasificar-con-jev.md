# Clasificar en volumen con jev — acelerador OPCIONAL del research

> ## Esto es opcional. El playbook funciona entero sin esto.
>
> No hace falta ninguna cuenta ni ninguna key para usar `lanzar-piloto`. Cada paso que
> aparece acá tiene su camino de siempre, y ese sigue siendo el default: la regex del swipe,
> y el paso de razonamiento del asistente. Si no tenés key, `scripts/clasificar.py` sale con
> código 2 y el paso sigue como si este archivo no existiera.
>
> ## 🧪 Además es experimental. Leerlo antes de usarlo en un piloto con dinero.
>
> **Nunca corrió dentro de un piloto en vivo.** Todo lo medido acá es back-test sobre datos
> de un piloto ya cerrado. Ninguna decisión de inversión se tomó con esto.
>
> Qué está probado: que los 4 packs corren, que los números dan, que sin key nada se rompe.
> Qué NO está probado: que sirva en un rubro distinto al del back-test, y que aguante cuando
> el volumen sea de cientos y no de decenas.
>
> **La primera vez que lo uses: revisá la salida a mano, ítem por ítem, antes de que entre a
> una decisión.** Sobre todo las negativas, donde un falso descarte se paga en clientes que
> nunca llegan y no deja rastro. Los modos de falla de abajo están medidos, no son teóricos.

Tres pasos de la Etapa 1 terminan con lo mismo: **un modelo tiene que juzgar cientos de ítems
de a uno** (keywords del planificador, avisos de la biblioteca de anuncios, negativas
candidatas). Hacerlo en tanda con un modelo de texto deriva: el juicio de un ítem contagia al
vecino. Hacerlo con una expresión regular no entiende la diferencia entre «curso de
contabilidad» y «servicio de contabilidad».

**jev** ([typesafe.ai](https://docs.typesafe.ai)) hace exactamente eso: una llamada por ítem,
sin lote y sin vecinos, respuesta tipada con probabilidad. No redacta. No razona. Contesta
preguntas cerradas. Endpoint `POST https://api.typesafe.ai/v1/systemone`, modelo `jev-latest`.

## La regla que no se negocia

**El corte lo hace el código sobre dato duro. jev llena campos, no ordena listas.**

Medido en otro uso del mismo motor, un filtro de 409 currículums: **la confianza calibrada no
ordenó nada.** Media 0,59 en los 30 mejores contra 0,51 en el resto, y 268 de 405 por debajo de
0,6. El que cortó la lista fue un campo duro leído con una expresión regular del PDF.

En el research, el dato duro ya existe y es mejor: volumen y costo por clic del planificador de
palabras clave, tamaño de audiencia de la API de la plataforma, cantidad de avisos por
anunciante. Usá **eso** para ordenar y cortar. La probabilidad de jev sirve para dos cosas:
filtrar por un umbral explícito (≥ 0,5 es competidor) y marcar de qué ítem puntual dudar. Nunca
para rankear.

## Las 3 primitivas

| Necesidad | Primitiva | Qué devuelve |
|---|---|---|
| ¿se cumple esta condición? | `noul` | probabilidad de sí, 0 a 1. **No lleva confianza aparte: la probabilidad ES la respuesta** |
| una de un conjunto cerrado | `choice` | la opción elegida + su confianza (qué tan concentrada está la distribución) |
| grado en una escala descripta | `score` | el nivel + confianza. Sirve para rankear porque cada ítem se puntúa contra la misma rúbrica |

Reglas para escribir un pack (`scripts/preguntas/*.json`):
- **Los identificadores de las preguntas no se le mandan al modelo.** Cada pregunta tiene que
  decir sola lo que quiere saber. `es_competidor` no significa nada del otro lado.
- Los niveles de un `score` describen situaciones concretas, no adjetivos («nos tapa: domina la
  categoría en el canal que necesitamos», no «amenaza alta»).
- En un `choice`, incluir siempre la salida de no-match (`ninguno_claro`, `no_se_entiende`).
- Todas las preguntas del pack viajan en **una** llamada: el contexto se cobra una sola vez.
  Corren en paralelo y no se ven entre ellas.
- Las preguntas se re-mandan en cada llamada. Con un contexto corto (una keyword), el pack **es**
  casi todo el costo. `--dry-run` lo calcula antes de gastar.

## Los 4 sitios

| Pack | Paso | Qué decide | El corte lo hace |
|---|---|---|---|
| `ads.json` | `s1c` Paso 2 y 3 | si el aviso es competencia de verdad + su ángulo | umbral 0,5 en código; el hueco de mensaje es un **conteo** de ángulos |
| `keywords.json` | `s1b` Paso 2 | intención de cada keyword | el orden sale del volumen y el costo por clic del planificador |
| `negativas.json` | `s1b` Paso 4 | si una negativa candidata bloquea clientes buenos | el match literal lo hace el código (ver abajo) |
| `players.json` | `s1a` Paso 2 | la amenaza de cada competidor, con rúbrica fija | el ranking sale del `score`, comparable entre competidores |

**Por qué el guardián de negativas no cruza pares.** «¿El término bueno contiene el texto de la
negativa?» es comparación de texto: eso es código, y de paso reproduce lo que hace la
plataforma (las negativas de frase no agarran plurales ni variantes, así que el match literal ES
el comportamiento real). Lo semántico es otra pregunta: *¿existe una búsqueda de alguien que
quiere contratar y que contiene ese texto?* Eso es **una llamada por negativa candidata**, no un
producto cruzado.

**Por qué la amenaza va con `score` y no repartida entre subagentes.** Un subagente por
competidor, cada uno puntuando de 1 a 5 sin ver a los otros, da un ranking que no se sostiene:
cada agente calibra su propia escala. Con una rúbrica fija en el pack, cada llamada se mide
contra el mismo texto, no contra los vecinos. El perfil en prosa lo sigue escribiendo el
subagente: jev no redacta.

## Cómo se corre

```bash
# 1. el paso emite los items (id + contexto por linea)
SWIPE_RELEVANT="..." SWIPE_EMITIR_ITEMS=items.jsonl python3 build_swipe.py raw.json

# 2. clasificar (--dry-run primero: muestra la llamada y el costo, no gasta)
python3 scripts/clasificar.py --items items.jsonl --pack scripts/preguntas/ads.json \
  --var SERVICIO="servicios de contabilidad" --var CLIENTE="dueño de un negocio chico" \
  --salida clasif.csv --dry-run

# 3. el paso consume el CSV
SWIPE_RELEVANT="..." SWIPE_CLASIFICACION=clasif.csv python3 build_swipe.py raw.json
```

El caché (`clasif.respuestas.jsonl`) hace que repetir sea gratis. `--rehacer` lo ignora.
La key va en `~/.config/typesafe/api_key` (`chmod 600`). **Nunca en el repo, nunca en un archivo
del proyecto.**

## La regla operativa: el desacuerdo entre las dos respuestas es la bandera

Cada pack pregunta dos cosas que tienen que ser coherentes entre sí. Corren en paralelo y no se
ven. **Cuando no coinciden, ese ítem va a ojo humano; cuando coinciden, va derecho.** Salió de
las corridas de abajo, y es más útil que mirar la confianza (que ya sabemos que no ordena). Los
tres casos que aparecieron:

| Ítem | Las dos respuestas | Quién tenía razón |
|---|---|---|
| negativa `part time` | balde `basura_universal` pero `mata_icp_p` 0,91 | el `noul`. Bloqueaba clientes reales |
| keyword `booking for small business` | `transaccional_alta` pero `quiere_contratar` 0,34 | el `noul`. Es otro rubro (reserva de turnos) |
| un competidor que vende formación | `tipo` software con confianza 0,56 (el resto ≥ 0,85) | ninguna: **faltaba la opción** en el pack |

El tercero es el que hay que leer con cuidado: una confianza baja en un `choice` suele querer
decir que **al pack le falta una opción**, no que el ítem sea raro. El modelo no puede elegir un
valor que no está en la lista. Ahí se arregla el pack, no el ítem.

**Ojo con qué llamás contradicción.** En el back-test de avisos el test estaba mal definido:
contar `es_competidor` bajo + destinatario `negocio_que_contrata` como choque daba 4 de 10. Al
abrir los 4 casos, los dos campos eran correctos a la vez: el aviso **sí** le habla a un dueño
de negocio, pero vende software, o un producto, o el servicio en otro país. Destinatario
correcto, oferta distinta. El choque de verdad es el otro: `es_competidor` **alto** con
destinatario `profesional_del_rubro`. Ese dio **0 de 16**.

Referencia del filtro de 409 currículums: el 48% de los descartes de un modelo de texto barato
se contradecían con sus propias respuestas de la misma llamada; en jev fue 1 de 38.

## El contexto va en el `state`, no alcanza el ítem pelado

La lección más caras de estas corridas. Sobre 7 negativas que en un piloto real habían estado
bloqueando clientes en silencio, con el **texto pelado** jev acertó 4 de 7: mandó `part time`,
`at home` y `for individuals` a «basura universal», porque sin contexto suenan a lenguaje de
alguien que busca empleo. Es la lectura razonable del texto que se le dio.

Con las **búsquedas reales que contienen el texto** en el contexto, los tres se dieron vuelta:

| Texto de la negativa | Probabilidad con el texto solo | con las búsquedas que lo contienen |
|---|---|---|
| `part time` | 0,55 | **0,91** |
| `at home` | 0,57 | **0,88** |
| `for individuals` | 0,51 | **0,83** |

Ese contexto no hay que inventarlo: **lo produce el match literal del código** sobre las
keywords del planificador o el informe de términos de búsqueda. Las dos mitades del guardián se
encadenan.

Contracara medida: con contexto el `noul` se vuelve más propenso a decir sí (`jobs` subió a 0,72
con una búsqueda de empleo en el contexto). Por eso el guardián **marca para revisar, no
decide**: 5 textos marcados sobre 30 se leen en un minuto, y una negativa que bloquea clientes
se paga en gente que nunca llega.

## Back-test medido

Las 4 corridas, todas contra material de un piloto ya cerrado (servicios de contabilidad para
negocios chicos en Estados Unidos). **Costo total: USD 0,002.**

| Pack | Set | Resultado |
|---|---|---|
| `ads.json` | 16 avisos que pasó la regex | 6 competidores reales, 10 descartados (ver abajo) |
| `negativas.json` | 16 de basura universal + 7 que habían bloqueado clientes | 20/23 con el texto pelado · 7/7 en la basura universal · los 3 fallos se arreglan con contexto |
| `keywords.json` | 12 keywords etiquetadas a mano | 9/12 exacto. En `bookkeeping prices` jev tenía razón y la etiqueta estaba mal: el propio `s1b` avisa que el que pregunta el precio compra |
| `players.json` | 5 competidores reales del rubro | el orden que daría una persona, y comparable entre ellos porque la rúbrica es fija |

### El detalle del swipe

Sobre 32 avisos crudos de la biblioteca de anuncios, la regex dejó pasar 16. De esos 16, **10 no
eran competencia**:

- **Una «masterclass de impuestos».** Le vende un curso a quien quiere *ser* contador. Entró por
  contener la palabra del rubro. Era el primer aviso del archivo.
- **Tres avisos que le venden formación, coaching y plantillas de contenido a colegas del
  rubro.** Se pelean otro cliente, no el nuestro.
- **Dos de software y uno de un producto físico** (una agenda de contabilidad): el cliente lo usa
  solo. Competencia adyacente, no por el mismo servicio.
- **Un proveedor que ofrece el servicio, pero en otro país.** El piloto era de Estados Unidos.
- **Dos avisos con el título literal `{{product.name}}`:** la variable de la plantilla quedó sin
  reemplazar, o sea que el aviso está roto. jev contestó `no_se_entiende`. Una regex no puede ver
  eso.

**Lo que esto dice del método:** el swipe del que salieron los ángulos de ese piloto tenía
mayoría de avisos que no eran competencia, y el hueco de mensaje se leyó sobre una muestra sucia.
No es higiene: es la entrada de `s3d-creativos-ads`.

Con los 6 que quedaron, el hueco dejó de ser una opinión y pasó a ser un conteo: cuatro ángulos
con 0 avisos. Eso es una tabla, no una lectura de ojo.

## Para sacarlo

Borrá este archivo, la carpeta `scripts/`, y los bloques marcados `[opcional]` de `s1a` Paso 2,
`s1b` Pasos 2 y 4, y `s1c` Paso 2b. Los caminos default quedan intactos: no hay nada que
restaurar.
