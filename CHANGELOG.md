# Changelog

## 1.7.1 (2026-09-25)

- **Tres trampas del scanner, medidas corriéndolo de verdad sobre dos dominios en producción.** El
  cambio de 1.7.0 se aplicó a un piloto real y las tres aparecieron en la primera vuelta:
  (1) **el CLI no re-escanea** —devuelve el reporte guardado y solo escanea cuando no existe ninguno,
  así que después de un fix se lee el número viejo y parece que no sirvió; se re-mide con el botón
  **Rescan** de la página del reporte, y la pista de que estás leyendo lo viejo es que el path
  aleatorio de la sonda del 404 se repite. (2) **`agent-instruction` busca la frase en inglés**: con
  el encabezado en castellano el check seguía en rojo con el archivo publicado; alcanzó con dejarlo
  bilingüe, sin tocar el contenido. (3) **el scanner a veces infiere una API que no existe** y activa
  checks esenciales de OpenAPI; se verificó que no es determinístico (mismo build, mismo robots.txt,
  mismo llms.txt: se los activó a un dominio y al otro no), así que se anota y no se rompe el sitio
  real para contentarlo.
- **Lo que dio, para calibrar expectativas:** los dos dominios partían de 71/100. Con los fixes del
  playbook, uno terminó en **100/100** y el otro en **78/100**, y toda la diferencia era la familia de
  checks de API que el scanner le inventó a uno solo. Los checks que el playbook sí controla
  (negociación de Markdown, 404, llms.txt, trust anchors, Organization) quedaron iguales en los dos.

## 1.7.0 (2026-09-24)

- **Nuevo: la landing del piloto se chequea contra un scanner de agent-readability antes de encender.**
  `npx -y is-agentic@latest {dominio}` escanea un dominio público en ~20-25 s y devuelve un score
  sobre 100 con los checks que no pasaron y el fix de cada uno. Es gratis y no pide cuenta.
  `s3b-build-landings` lo corre después del deploy y `s3f-pre-launch-validation` lo anota en la
  punch-list.
- **Los requisitos se construyen, no se parchean.** El cambio grande no es correr el scan: es que el
  prompt de build de `s3b` ahora pide de entrada lo que el scan mide — JSON-LD con un tipo de
  identidad, `/about` `/contact` `/privacy` con contenido real, un 404 que devuelve 404 y un cuerpo
  en Markdown, y un `llms.txt` que dice **cuándo** conviene usarte. De entrada cuesta minutos;
  después es tocar una landing que ya está comprando tráfico. Dos landings de pilotos reales, ya en
  producción, dieron 83 y 71 sobre 100: los huecos eran todos de esta lista.
- **Se anota, no bloquea.** El ítem de `s3f` registra el score y los `essential` que fallan, y
  explícitamente **no** frena el encendido: un score bajo no impide que el ad convierta. Lo que ya
  bloqueaba sigue bloqueando por su vía (si falta `/privacy`, el FAIL lo tira el bloque legal).
- **El componente `geo-y-citacion-llm` suma la sección que le faltaba y se corrige a sí mismo.**
  Separa *ser citado* (lo que ese componente ya cubría) de *ser legible por un agente* (lo que el
  scan mide), y matiza su propio veredicto sobre `llms.txt`: sigue siendo descartable como palanca
  de citación, pero el check `agent-instruction` premia un archivo que diga cuándo usarte, y suele
  ser el mismo archivo.
- **Dos trampas documentadas, las dos verificadas contra el servicio.** (1) La API
  (`GET /api/v1/report?url=...`) es de **solo lectura**: sobre un dominio que nadie escaneó devuelve
  404 `report_not_found`, y pegarle por curl a `/scan/{dominio}` devuelve la página sin disparar
  nada — el que dispara el scan es el CLI. (2) El check `brand-search-accuracy` falla por definición
  en un dominio de piloto recién registrado, porque mide que una búsqueda de tu marca devuelva tu
  dominio. No se persigue y no cuenta como abierto.

## 1.6.0 (2026-09-22)

- **Nuevo: acelerador OPCIONAL para clasificar en volumen en el research** (`scripts/` +
  [`reference/clasificar-con-jev.md`](reference/clasificar-con-jev.md)). Tres pasos de la Etapa 1
  terminan juzgando cientos de ítems de a uno (keywords del planner, avisos del Ad Library,
  negativas candidatas). Hacerlo en tanda con un modelo de texto deriva: el juicio de un ítem
  contagia al vecino. Ahora se puede hacer con un modelo de decisiones tipadas, una llamada por
  ítem. **Nada del método lo necesita:** sin configurar nada, cada paso corre por su camino de
  siempre y el playbook está completo. Es experimental y el archivo de referencia arranca diciendo
  qué está probado y qué no.
- **Lo que lo motivó, medido, no supuesto.** Sobre 32 avisos crudos del Ad Library de un piloto
  real, la expresión regular del swipe dejó pasar 16 y **10 de esos 16 no eran competencia**: una
  masterclass para futuros contadores (era el primer aviso del archivo), tres avisos que venden
  formación a colegas del rubro, dos de software y uno de un producto, un proveedor de otro país, y
  dos avisos con el título `{{product.name}}` sin reemplazar. El swipe del que salían los ángulos
  tenía mayoría de avisos que no eran competencia. Una regex no puede separar «curso de
  contabilidad» de «servicio de contabilidad»: usan las mismas palabras.
- **Dos correcciones de método que valen sin usar el acelerador.** (1) El **hueco de mensaje se
  cuenta**, no se opina: se listan los ángulos posibles y se tilda cuáles aparecen, porque un
  ángulo con 0 avisos no está en el texto que el asistente lee y ahí no lo puede encontrar. (2) El
  **guardián anti-over-block se parte en dos**: el match literal negativa×término es código (y así
  reproduce que las negativas de frase no agarran plurales ni variantes), y solo lo semántico va a
  un modelo.
- **`s1a` Paso 2 deja de repartir el `threat` entre subagentes.** Si cada subagente puntúa la
  amenaza de su competidor sin ver a los otros, cada uno calibra su propia escala y el ranking no se
  sostiene. El camino default ahora es que los subagentes devuelvan el perfil sin el número, y que
  el padre puntúe a todos de una sola vez con los perfiles a la vista.
- `s1c-swipe-ads-competidores/scripts/build_swipe.py` suma tres variables de entorno **opcionales**
  (`SWIPE_EMITIR_ITEMS`, `SWIPE_CLASIFICACION`, `SWIPE_UMBRAL`). Sin ellas produce el mismo swipe
  que antes, byte a byte (verificado por diff contra la versión anterior del script).
## 1.5.0 (2026-09-22)

- **El README cambia de objeto: lo que el piloto valida es el canal, no el negocio.** El encuadre
  anterior ("validá un negocio con publicidad paga") dejaba afuera al que ya tiene el negocio
  facturando y solo quiere saber si Google o Meta le sirven, que es la mitad de los casos. El
  título ahora es "validá un canal de adquisición digital con un tope de inversión", y la apertura
  cubre los dos casos en la misma frase en vez de abrir con el caso nuevo y corregirse en el
  párrafo siguiente. El párrafo de qué te deja un piloto también cambió: antes prometía "una
  respuesta sobre si esto se puede vender", ahora dice lo que realmente queda, que es el canal
  armado con su costo de adquisición real, las palancas sin tocar y el aprendizaje de mercado que
  sobrevive aunque el canal no haya funcionado.
- **"La idea de fondo" pasó a "Dónde se gana o se pierde el dinero".** Su primer punto decía que la
  respuesta del mercado a la oferta era "lo único que el piloto realmente prueba", que contradecía
  de frente el encuadre nuevo. Ahora dice que si el mercado no responde, ningún canal lo arregla.
- **"Para qué se puede usar" bajó de siete filas a cinco.** Las dos que salieron (idea nueva,
  negocio ya andando) repetían lo que la apertura ya resuelve. Las cinco que quedan son entradas
  que de verdad son otra cosa: research solo, el modelo de CAC/LTV solo, los roles de optimización,
  un componente de funnel suelto y el postmortem.
- **Del commit `ajustes textos readme`, hecho en paralelo:** la lista de asistentes suma Hermes y
  Openclaw ("etc." al final, porque cualquiera que lea markdown sirve), y la **matrícula** pasó a
  llamarse **derecho de piso**. Los otros tres cambios de ese commit (sacar "en criollo", sacar
  "esto es lo que lo hace distinto" y sacar "La mayoría gasta mal en un piloto") coincidían con lo
  que ya había hecho la pasada de anti-slop.
- Tocados: `README.md`, `VERSION`, `CHANGELOG.md`.

## 1.4.0 (2026-09-22)

- **El README deja de encuadrar todo como "lanzar un piloto".** El kit servía desde siempre para
  más casos que el piloto completo, pero el README solo contaba ese, así que alguien que ya tiene
  el negocio andando y quiere abrir un canal pago por primera vez no se reconocía en el texto y se
  iba. Ahora hay una sección **Para qué se puede usar** con una tabla de siete situaciones, cada
  una con su puerta de entrada al kit y lo que deja: el método completo, las etapas de research
  sueltas, el modelo de CAC/LTV solo, los roles de optimización para campañas que ya corren, los
  componentes de funnel, y el postmortem. La vieja sección "Cómo lo usás" quedó absorbida ahí
  adentro para que el mismo dato no viva en tres lugares del documento. El título y el primer
  párrafo también se abrieron: el piloto sigue siendo el caso central, ya no el único.
- **Pasada de anti-slop sobre el README.** Once correcciones, casi todas del mismo patrón: el
  reframe "no es X, es Y" ("no son clientes: es una respuesta", "no es una app", "la puerta de
  entrada, no el techo", "no arrancan nada: optimizan"). Se reemplazaron por la afirmación
  positiva sola. También se sacó el puffery del heading "La idea de fondo (esto es lo que lo hace
  distinto)", dos cierres que repetían lo ya dicho y el arranque de párrafo "La mayoría gasta mal
  en un piloto".
- Tocados: `README.md`, `VERSION`, `CHANGELOG.md`.

## 1.3.0 (2026-09-22)

- **Registro editorial: se saca el coloquialismo, se mantiene el voseo.** El kit estaba escrito en
  un registro demasiado informal para un repo público: "plata" en vez de presupuesto, un heading
  que decía "Cómo funciona, en criollo", "te lleva de la mano", "chequealo", "a ojo", "mueve la
  aguja". Nada de eso agregaba precisión y sí restaba seriedad al primer contacto de alguien que
  llega desde GitHub. El registro nuevo es profesional pero sigue siendo rioplatense: el voseo
  queda intacto (tenés, podés, armá, revisá), y los términos del dominio se escriben siempre igual
  (gate, piloto, landing, kill criteria, CAC/LTV, matrícula vs impuesto evitable). Se unificó
  además el estado "Parkeado" a "Pausado" en los cuatro estados por frente del kickoff multifrente,
  que era el último anglicismo informal con peso estructural.
- **Corrección de dato:** el README y el `SKILL.md` decían "las 4 etapas" cuando el playbook tiene
  5 (Etapa 0 a Etapa 4). Corregido en ambos.
- Tocados: `README.md`, `SKILL.md`, `templates/kickoff-prd-template.md`, `s4a-operar-gates/SKILL.md`,
  `s3d-creativos-ads/SKILL.md`, `s4b-postmortem/SKILL.md`, `VERSION`, `CHANGELOG.md`.

## 1.2.0 (2026-08-22)

- **Séptimo componente: `geo-y-citacion-llm`.** El kit optimizaba tráfico pago y SEO tradicional
  pero no cubría el canal que crece más rápido: la gente que le pregunta a un modelo generativo en
  vez de buscarlo en Google. El componente nuevo separa dos cosas que se confunden: habilitar la
  citación (fixes técnicos — los user-agents de búsqueda en vivo nunca bloqueados, alta en Bing
  Webmaster Tools, un solo dominio canónico coherente) y ganarte la cita (contenido por
  sub-pregunta, no por repetición de la misma keyword, que es el instinto que trae el SEO viejo y
  que de hecho baja la tasa de citación un 10%). Trae la tabla de qué motor se sirve de qué índice
  (Copilot y ChatGPT corren sobre Bing, Perplexity ya tiene índice propio, Google AI Overviews y
  Claude no pasan por ahí), el menú de implementación ordenado por rendimiento sobre hora de
  trabajo, y la tensión con `lead-magnet-y-nurture`: ese componente deja el blog en `noindex` por
  default, y un blog en `noindex` tampoco puede ser citado por un motor generativo.
- Tocados: `componentes/geo-y-citacion-llm/SKILL.md` (nuevo), `SKILL.md`, `README.md`, `VERSION`,
  `CHANGELOG.md`.

## 1.1.1 (2026-08-28)

- **El ejemplo de audiencias de Meta dice qué representa cada ID.** `audiences.example.json` traía
  números pelados que no le servían de nada al que lo abre: había que resolverlos igual contra la
  Graph API para saber qué eran. Ahora cada uno es un placeholder con nombre
  (`BEHAVIOR_ID_DUENIOS_DE_NEGOCIO`, `INTEREST_ID_SOFTWARE_DEL_RUBRO_1`), que es exactamente la
  lista de lo que tenés que ir a buscar para tu propio rubro. El comentario de arriba avisa además
  que sin reemplazarlos la API rebota con un error de parámetro inválido, en vez de dejarte
  descubrirlo corriendo el script.
- Tocados: `s1d-sizing-audiencias-meta/scripts/audiences.example.json`, `VERSION`, `CHANGELOG.md`.

## 1.1.0 (2026-08-28)

Los roles dejan de ser seis archivos sueltos y pasan a tener índice, y entran dos bloques de
oficio que hasta ahora no estaban escritos en ningún lado: cómo se producen estáticos con un
generador de imágenes, y cómo se entrega un modelo de Excel que abre bien en la máquina del otro.

- **`roles/INDEX.md`, nuevo.** Antes había que abrir los seis archivos para saber cuál servía. Ahora
  hay una tabla con qué hace cada rol y cuándo arranca, un mapa de qué etapa del playbook consume
  cuál (así no elegís a mano si estás corriendo el método), y la secuencia para usarlos fuera de un
  piloto: cuenta nueva, tracking antes de encender, negativos a las dos semanas, auditoría al mes.
- **Diez reglas para creativos generados con IA**, en `s3d-creativos-ads`. Las dos que más plata
  ahorran: la etapa de funnel la define la audiencia del ad set y no el tono del texto (un lookalike
  de tus clientes es TOFU, por más que el copy suene a cierre), y la foto se genera sin texto con el
  copy sobreimpreso por código, porque cambiar una palabra no puede costar una generación nueva.
  Además: el apaisado se resuelve con maqueta y no extendiendo con IA, no existe una regla de
  recorte que sirva para todas las fotos, y renderizar sin mirar la plancha de contacto no es
  verificar. Son independientes del generador: valen con cualquiera, o dibujando a mano.
- **Safe zones 9:16**, en `roles/ad-creative-strategist`. Los porcentajes concretos que la interfaz
  tapa arriba y abajo, el rango de píxeles donde puede vivir lo crítico, y qué hacer cuando la
  cuenta no te deja personalizar por ubicación: subir el vertical ya diseñado como imagen única.
- **El xlsx del modelo de funnel tiene que abrir sin pedir reparación**, en `s2a-modelar-funnel`.
  Un archivo escrito con openpyxl y nada más llega roto y no te enterás: la librería no guarda el
  valor cacheado de las fórmulas, así que Excel pide repararlo y las vistas previas de mail y drive
  muestran todo en blanco. LibreOffice lo tolera, con lo cual el bug no aparece si solo probás ahí.
  Va como criterio de éxito de la etapa: si la validación falla, el archivo no sale.
- Tocados: `roles/INDEX.md` (nuevo), `s3d-creativos-ads/SKILL.md`, `roles/ad-creative-strategist.md`,
  `s2a-modelar-funnel/SKILL.md`, `VERSION`, `CHANGELOG.md`.

## 1.0.0 (2026-08-27)

Primera versión numerada del kit. Lo que hay adentro, en una línea: un método de 16 pasos para
validar un negocio nuevo con un piloto de publicidad paga, más 6 componentes de funnel y 6 roles
de paid media, todo escrito para que lo lea y lo siga tu asistente de IA.

- **El README dice de entrada de qué metodología viene.** Arriba de todo, antes del hook: el kit
  sigue **Lean Startup**, construir-medir-aprender, con plata real y un tope que corta cuando los
  números no dan. Cada etapa cierra con una decisión de matar o perseverar tomada con un número
  adelante. Estaba implícito en el método desde siempre (el gate de budget *es* esa decisión) y
  ahora se dice, en vez de dejar que el lector lo deduzca.
- **Sección nueva: «No se termina cuando termina el piloto».** El título prometía menos de lo que
  el kit trae. Solo **4 de los 16 pasos** existen únicamente para un piloto (plan, diseño del
  experimento, operación de gates y postmortem); todo lo demás se reusa con las campañas ya
  andando: los 6 roles, los 6 componentes, el research de keywords, los creativos y el tracking.
  Ese dato estaba enterrado en media frase del cuarto párrafo y ahora tiene su propio bloque.
- **Qué deja un piloto, dicho sin vueltas.** No son clientes: es una respuesta con números atrás a
  la pregunta de si esto se puede vender. Cuando la respuesta es que no, el tope de plata te lo
  dice temprano y barato, que es exactamente para lo que está.
- Tocados: `README.md`, `VERSION` (nuevo), `CHANGELOG.md` (nuevo).

---

**Semver de este kit.** Mayor: cambia el método o se rompe la compatibilidad de un template.
Menor: entra una etapa, un componente o un rol. Patch: se afina algo que ya estaba.
