# Reference: lead magnet + nurture (opción probada: ESP con automation visual gratis)

Basado en un piloto real de referencia (leadgen B2B, verticales de servicios). El código y la configuración de ese caso quedaron despersonalizados acá: los nombres de archivos, dominios y variables de ejemplo son genéricos.

## Arquitectura (la corrección de diseño más importante)

```
Landing captura email
   → POST /api/lead (backend propio)
   → orquestador (n8n, Make, un script propio)
        ├─ CRM (Notion, Sheets, lo que sea)  = ESTADO del lead
        └─ ESP: upsert subscriber             = MOTOR de mails
              → alta con fields (nombre, idioma, intención de captura, fuente, campaña)
              → status: active
              → groups: [grupo del idioma/marca]
              → el "join group" DISPARA la automation dentro del ESP
                    → Mail #1 = el magnet (inmediato)
                    → +1 día → Mail #2 … → +1 día → Mail #7 (cierre)
                    → post-cierre → el subscriber queda en el grupo, broadcasts manuales
```

**El orquestador NO manda ni un solo mail de la cadena.** Su único trabajo es el upsert (alta o actualización) del suscriptor y el alta en el grupo correcto. Toda la lógica de "cuándo sale cada mail" vive adentro de la automation del ESP. Esto es una corrección de diseño importante sobre un enfoque más ingenuo (mandar los mails desde el propio orquestador): separar las responsabilidades así evita reinventar el motor de secuencias y da opens/clicks nativos por mail.

Implementación de referencia del nodo de alta: un HTTP Request `POST` al endpoint de suscriptores del ESP, dentro de la rama "email capturado" del flujo del orquestador. Body: email + campos custom (nombre, idioma, intención de captura, fuente del lead, campaña) + `status: active` + `groups: [<id del grupo correspondiente>]`. Idempotente: re-unir al mismo grupo no re-dispara la automation.

## Paso a paso

1. **Generar el magnet.** Un script genera el PDF (por ejemplo con una librería tipo `reportlab`): banda de título, checklist o lista numerada, y un bloque de CTA final que espeja el botón de la landing. El contenido sustantivo se escribe una vez por idioma, no se traduce mecánicamente: cada versión tiene su propio texto nativo, no una traducción literal de la otra.
2. **Página de captura sin mostrar el magnet.** Un solo campo de email y un solo submit. El copy deja explícito "te lo mando por mail"; nunca hay un botón de descarga directa en esta página.
3. **El cliente dispara el alta, sin esperar confirmación del ESP.** Al enviar el form, el JS del lado cliente hace el POST a `/api/lead` con email, idioma, fuente y UTMs. Conviene dedupe por sesión (ej. `sessionStorage`) para no re-disparar el alta dos veces si el usuario navega ida y vuelta.
4. **La página de "gracias" tampoco descarga nada.** Solo confirma "revisá tu mail" (regla dura del invariante 2).
5. **Grupos = 1 por marca/idioma**, no una sola automation con condiciones. Con contenido nativo por idioma (no traducción), separar automations es más simple que meter lógica condicional adentro de una sola.
6. **Campos custom mínimos:** nombre, idioma, intención de captura (caliente vs tibio; solo para reporting, no bifurca la cadena al arrancar), fuente del lead, campaña. Un campo de vertical/rubro y uno de "ya agendó" quedan reservados para más adelante si hace falta.
7. **Automation:** trigger "cuando el suscriptor se une al grupo" → Mail 1 inmediato (el magnet) → esperar 1 día → Mail 2 → … → esperar 1 día → Mail final (cierre duro). El delay recomendado para arrancar es "esperar 1 día" simple; sincronizar a una hora fija del día es una mejora posterior, no bloqueante.
8. **UTMs por paso:** `utm_source=<esp>`, `utm_medium=email`, `utm_campaign=nurture7-<idioma>`, `utm_content=d1-guia`, `d2-...`, etc. Casi todos los ESP con automation visual tienen un toggle de "agregar UTMs" a nivel de campaña/automation; usarlo + sobreescribir `utm_content` a mano por paso da menos margen de error que hornear el link entero.
9. **El link del magnet en el mail 1 también lleva UTM** (`utm_content=d1-guia`), así se mide cuánta gente realmente abrió el PDF, no solo el mail.

## Gotchas (verificados en un caso real)

- **"Publicar cambios" ≠ autosave.** Muchos editores visuales de mail autoguardan el borrador, pero el mail que efectivamente sale (preview o envío real) no cambia hasta apretar el botón explícito de "listo"/"publicar". Sin eso se manda el cuerpo viejo aunque el borrador se vea bien en el editor. Buscá la señal de que sí commiteó (suele ser una navegación o un timestamp que cambia).
- **Doble opt-in OFF a propósito**, alineado con el invariante 3: como el alta entra por API (no por un form nativo del ESP), el suscriptor se da de alta directo con `status: active`.
- **Ojo con los techos de los planes free.** Un free tier típico de este tipo de ESP ronda algunos cientos de suscriptores y unos miles de mails por mes (verificar el número vigente del proveedor elegido, cambia con el tiempo). Vigilar el techo si el piloto escala; una migración con exportación de la lista es la salida si se supera.
- **El nombre de un campo custom puede no coincidir con lo que esperás.** Un campo tipo "fuente" puede terminar llamándose distinto en el ESP real porque choca con un nombre reservado. Verificar el nombre real del campo antes de mapear el payload del orquestador.
- **La intención de captura no bifurca la cadena al arrancar**, solo sirve para segmentar/reportar después. Meter un branch de intención desde el día uno es sobre-construir.

## Email del dominio (prerequisito antes del primer envío)

Antes de que el ESP o cualquier pieza mande un solo mail desde `hola@tudominio.com`:

1. **Verificar el dominio en el ESP**: cargar los registros DNS que pide (SPF + DKIM) en el registrar. Sin esto los mails salen como "via <esp>.com" o directo a spam.
2. **DMARC mínimo** (`p=quarantine` alcanza para un piloto): un TXT en `_dmarc.` del dominio. Si ya existe, no tocarlo.
3. **Las respuestas necesitan a dónde caer**: la casilla `hola@` no existe sola. Forwarding gratuito (ImprovMX, Cloudflare Email Routing) hacia la casilla real del operador resuelve replies sin pagar un Workspace por dominio.
4. **Gotcha de registrar**: algunos no aceptan cargar MX + TXT del mismo host en una sola pasada; guardar de a un registro y verificar propagación antes de dar por hecho el setup.

## Piezas satélite del funnel de captura (probadas en el piloto real)

- **Popup de exit-intent como red de rescate**: dispara por intención de salida o timer (~15-30 s) y ofrece el magnet al que se va sin dejar el mail. Reusa el MISMO pipeline de captura (`/api/lead`) con un `source` propio. Gotcha real: toda fuente nueva hay que sumarla a las reglas de stage del CRM, o esos leads entran mal clasificados (ver componente `captura-y-crm`).
- **Página de recursos post-captura**: destino único del post-gracias y del post-reserva. Confirma "el material te llega por mail" (nunca descarga directa) y linkea contenido propio para que el click no muera en un callejón.
- **Blog de respaldo, generado por script**: artículos por vertical/tema escritos una vez en markdown y compilados a HTML por idioma con un build script. Su rol en un piloto NO es SEO (arrancan `noindex` por default; indexar es una decisión explícita posterior): es darle sustancia a la página de recursos, destino a los links del nurture y credibilidad al dominio. Horas de esfuerzo, no semanas; no armarlo antes de que el funnel capture algo.

## Alternativas evaluadas (no usadas en el piloto, quedan documentadas)

- **Orquestador + ESP con API de contactos ilimitados (tipo Brevo):** sin techo de suscriptores, pero con un cap de mails/día en el free tier. Riesgo real si entra un pico de leads en una cadena diaria. HTML crudo por API en vez de editor visual.
- **Transaccional puro (tipo Resend):** sirve para el mail #1 de entrega inmediata (útil como red de contingencia mientras se arma el ESP), pero no da secuencias ni opens/clicks sin instrumentar algo aparte. No reemplaza al ESP para la cadena completa.

## Credenciales e infra a reusar

Ver [reference/infra-y-credenciales.md](../../reference/infra-y-credenciales.md) para dónde viven los tokens/credenciales de este componente en tu propio proyecto (nunca valores en texto plano en este documento).
