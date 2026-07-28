# Reference: cold outreach (opción probada: transaccional general asumiendo el riesgo de ToS)

> Repetimos la advertencia porque importa: esta receta asume que ya se leyó y decidió conscientemente la advertencia de ToS del SKILL.md. Si todavía no se decidió, no seguir de acá para abajo.

Basado en un piloto real de referencia (leadgen B2B a negocios locales por vertical). El pipeline queda descrito acá de forma genérica: mismo diseño, sin nombres de archivos ni datos del caso original.

## Piezas del pipeline

| Rol | Qué hace |
|---|---|
| Armador de lista | Scrape crudo → contactos limpios. Filtra ICP, cadenas y duplicados |
| Enriquecedor | Busca el email en la web del negocio cuando el scraper no lo trajo. Costo 0 |
| Enviador | Tanda diaria por el proveedor elegido, con ramp, espaciado aleatorio y stop-loss |
| Sincronizador de estado | Trae aperturas, clicks y bounces desde el proveedor de envío |
| Reportador | Arma y manda el reporte diario a quien opera la campaña |
| Orquestador del día | Corre los tres anteriores en orden (sync → enviar → reportar). Es lo que dispara el cron |
| Config | Ramp, caps, umbrales del stop-loss, remitente, dirección postal |
| Archivo centinela de pausa | Si existe, el enviador no manda nada. Crearlo frena, borrarlo prende |

## Paso a paso

### 1. Armar la lista

Convierte el scrape crudo (de un actor de scraping de mapas u otra fuente) en filas listas para operar. Tres reglas de filtrado, verificadas en el piloto real:

- **Allowlist de categoría → vertical.** Todo lo que no mapea a una categoría conocida se descarta; sin esto, un término de búsqueda amplio trae de vuelta categorías fuera de ICP (más de la mitad de los descartes reales fueron por esto).
- **Deduplicación por dominio con lista de cadenas conocidas.** Un tope de sedes por dominio (ej. 2): si un dominio aparece en más filas que eso (multi-local), se descarta entero, más una lista explícita de cadenas conocidas del rubro. En el piloto real, un solo dominio de cadena metió más de un tercio de todas las filas scrapeadas.
- **Prioridad de email cuando hay varios por negocio:** email personal (ej. gmail del dueño) > email con nombre de persona en el dominio propio > email genérico (`info@`, `contact@`). El gmail personal en un negocio chico suele ser quien decide, y no un buzón que nadie lee.

Snippet ilustrativo de la lógica de prioridad:
```python
def prioridad_email(fila):
    """Menor es mejor. Preferimos que parezca una persona, no un buzon generico."""
    if es_personal(fila):
        return 0          # gmail del dueño: suele ser quien decide
    if not es_rol_generico(fila):
        return 1          # nombre@sudominio.com
    return 2              # info@ / contact@
```

### 2. Enriquecer emails faltantes

Para las filas sin email pero con sitio web, entra a la home + hasta 3 rutas de contacto tipo `/contact`, `/about` y busca emails por regex + `mailto:`. Sin dependencia de ninguna API paga. Puntúa el email encontrado (email en el dominio propio > webmail público > el resto) y descarta ruido conocido (proveedores de web en el footer, direcciones tipo `noreply@`, extensiones de archivo).

**Gotcha medido y verificado:** el enriquecimiento vía Instagram/LinkedIn/Facebook sin sesión logueada **no rinde: 0 de 15 casos probados**. Facebook bloquea el 100% sin sesión, Instagram sirve un shell vacío, LinkedIn devuelve HTML real pero sin el email. El único enriquecimiento que rinde es la web del propio negocio, con una tasa medida de **~22%** sobre los casos sin email directo del scraper.

### 3. Enviar

Lee el estado de la campaña, calcula el cupo del día según el ramp configurado, manda con espaciado aleatorio, y se niega a enviar en varios escenarios:

- Existe el archivo centinela de pausa.
- La config tiene el estado en "pausado".
- La sincronización de métricas no corrió o corrió hace demasiado (umbral configurable, ej. 48h), salvo que se fuerce explícitamente sabiendo lo que se hace.
- El stop-loss se disparó (ver abajo): en ese caso el propio script **escribe el archivo de pausa** con el motivo, no espera a que alguien lo note.

Snippet ilustrativo del cálculo de cupo diario según el ramp:
```python
def cupo_de_hoy(cfg, filas):
    dia = dias_habiles_transcurridos(filas) + 1
    for tramo in cfg["ramp"]:
        if tramo["desde_dia_habil"] <= dia <= tramo["hasta_dia_habil"]:
            return min(tramo["por_dia"], cfg["cap_duro_diario"]), dia
    return 0, dia
```

Snippet ilustrativo del stop-loss:
```python
def chequear_stop_loss(cfg, filas):
    sl = cfg["stop_loss"]
    enviados = [f for f in filas if f["estado"] in ("sent", "bounced", "replied")]
    if len(enviados) < sl["minimo_enviados_para_evaluar"]:
        return None
    bounces = sum(1 for f in filas if f.get("bounce") == "1")
    complaints = sum(1 for f in filas if f.get("complaint") == "1")
    tasa = bounces / len(enviados) if enviados else 0
    if tasa > sl["bounce_rate_max"]:
        return f"bounce rate {tasa:.1%} supera el maximo {sl['bounce_rate_max']:.0%}"
    if complaints >= sl["complaints_max"]:
        return f"{complaints} spam complaints (maximo {sl['complaints_max']})"
    return None
```

Constantes de config reales del piloto de referencia: ramp de días hábiles 1-5 → 10/día, 6-10 → 20/día, 11+ → 35/día, con un cap duro diario de 60 (nunca se cruza aunque un tramo lo permita). Stop-loss: bounce rate máximo 3%, máximo 2 quejas de spam, evaluado recién desde un mínimo de 40 enviados (con muestra chica el % engaña). Espaciado entre mails: entre 90 y 240 segundos, elegido al azar en ese rango.

**Lock contra doble envío:** una tanda grande con espaciado puede durar más de 2 horas; si una corrida programada se solapa con una corrida manual, ambas leerían los mismos pendientes y mandarían doble. La solución es un lock de archivo (`flock` o equivalente) tomado antes de arrancar a enviar.

**Guarda de testing:** un flag de "forzar cantidad" sin un flag de "forzar destino" debería rechazarse explícitamente, porque sin destino forzado terminaría mandándole a prospectos reales pese a estar pensado como flag de prueba.

### 4. Sincronizar estado

Trae del proveedor de envío el estado real (abierto, click, rebote, queja) por cada mail mandado. **Suele necesitar una API key distinta a la de envío** (con permisos de lectura, no solo de envío), porque muchas keys de solo-envío no pueden leer nada (401). Sin esta sincronización corriendo, el stop-loss del punto 3 queda ciego: ve columnas de bounce/complaint siempre vacías, así que nunca se dispara aunque el bounce real sea alto.

### 5. Reportar y orquestar

Un script orquestador corre los tres pasos en orden (sync → enviar → reportar) y es lo que dispara el cron. El reporte sale siempre, aunque no se haya enviado nada en la tanda (para que el freno se note, no quede en silencio).

## Guardas encontradas por auditoría adversarial (aplicar siempre, no son opcionales)

1. **Stop-loss ciego sin la sync:** corregido negando el envío si la sync no corrió (ver punto 3).
2. **Doble envío sin lock:** corregido con un lock de archivo (ver punto 3).
3. **Un flag de "forzar cantidad" sin "forzar destino" mandaba a prospectos reales** pese a ser pensado como flag de prueba: corregido exigiendo el destino forzado o un modo explícito de simulación.
4. **Header de unsubscribe de un click inválido cuando solo hay `mailto:`.** El estándar (RFC 8058) exige que ese header vaya solo si hay una URL https que reciba el POST; con un `mailto:` como único unsubscribe, declarar ese header es inválido y se sacó.

## Anti-spam, resumido (el detalle está en el SKILL.md como invariantes)

Remitente separado del dominio que corre el nurture real. Un contacto por dominio. Texto plano, un link. Sin "free" ni palabras gatillo en el asunto. Lista verificada por sintaxis + MX antes de enviar. Dirección postal física en el cuerpo. Header List-Unsubscribe con `mailto:`. SPF/DKIM/DMARC del dominio de envío verificados ANTES del primer mail, y las respuestas cayendo en una casilla real que alguien mira (receta de email del dominio: `../lead-magnet-y-nurture/reference.md` §Email del dominio).

## Economía del scraping

El costo depende del actor de scraping elegido, no solo de la cantidad de contactos. En el piloto real de referencia, cambiar de un actor "todo en uno" (que además intenta enriquecer contactos) a un actor barato de solo-scraping + el enriquecimiento local (costo 0) bajó el costo por 1.000 contactos en un factor de aproximadamente 12x, a costa de que el proceso tarda más porque el enriquecimiento local pide de a pocos sitios con pausa entre requests al mismo dominio.

Una fuente gratuita e ilimitada de datos de mapas (tipo OpenStreetMap/Overpass) sirve como fuente complementaria, no como reemplazo de la fuente principal (tipo Google Maps): en el piloto real dio unos cientos de negocios pero solo alrededor de un 13% con email directo, y el resto necesita el mismo enriquecimiento vía web. Útil para sumar volumen gratis mientras se espera un reset de cuota de la fuente principal, no para armar el volumen completo.

## Qué pasa con los que responden

Las respuestas caen en la casilla de correo real (por el remitente/reply-to configurado). Conviene un triage manual o semi-automático diario: quien pide baja se marca como dado de baja y no se le vuelve a escribir; quien muestra interés entra al CRM del funnel real con una fuente distinguible (para no mezclarlo con el tráfico pago/orgánico). Este componente **no responde solo**: la decisión de a quién y qué contestar la toma una persona.

## Gate de muerte

Definir de antemano un volumen total de envíos (ej. 1.000) que, si se llega sin respuestas positivas ni capturas, cierra el experimento y se documenta el aprendizaje. El stop-loss (punto 3) puede frenarlo antes por razones técnicas, independientemente del gate de resultado.

## Credenciales e infra a reusar

Ver [reference/infra-y-credenciales.md](../../reference/infra-y-credenciales.md) para dónde viven los tokens/credenciales de este componente en tu propio proyecto (nunca valores en texto plano en este documento).
