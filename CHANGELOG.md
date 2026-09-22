# Changelog

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
