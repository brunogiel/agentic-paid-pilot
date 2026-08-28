# Roles de paid media

Seis "personalidades" de agente para armar y operar campañas de publicidad paga. Cada una cubre
una pata del ciclo (estrategia de plataforma, copy, tracking, optimización, auditoría) con su
framework propio y su criterio de cuándo se usa.

**No son etapas del playbook.** Las etapas (`s0` a `s4b`) son el método del piloto, de punta a
punta. Los roles son herramientas que varias etapas consumen, y que siguen sirviendo cuando el
piloto ya cerró y las campañas quedaron corriendo.

---

## Los 6 roles

| Rol | Para qué | Cuándo arranca |
|---|---|---|
| [google-ads-strategist](google-ads-strategist.md) | Estructura de cuenta y campañas de búsqueda en Google Ads | Arrancar de cero, o reestructurar una cuenta que ya corre |
| [meta-ads-strategist](meta-ads-strategist.md) | Estructura full-funnel en Meta: prospecting y retargeting | Cuando hay presupuesto para una segunda plataforma, o el negocio es más visual que de intención |
| [ad-creative-strategist](ad-creative-strategist.md) | Copy de RSAs, creativos de Meta y ángulos de mensaje | Después de decidir keywords y audiencias, antes de subir un solo ad |
| [search-query-analyst](search-query-analyst.md) | Optimización continua: términos de búsqueda, negativos, n-grams | Cada 2-4 semanas de gasto activo |
| [campaign-auditor](campaign-auditor.md) | Auditoría de una cuenta existente, en Google o en Meta | Al tomar una cuenta que ya venía corriendo, o cuando algo huele raro |
| [tracking-specialist](tracking-specialist.md) | GTM, GA4, CAPI y acciones de conversión, con deduplicación | En el setup inicial, o cuando los números de dos plataformas no cierran |

---

## Qué etapa consume qué rol

Si estás corriendo el playbook, no hace falta elegirlos a mano: cada etapa ya dice cuál lee.

| Rol | Lo consumen |
|---|---|
| google-ads-strategist | `s1b-kw-research-google`, `s3c-spec-campanias` |
| meta-ads-strategist | `s1d-sizing-audiencias-meta`, `s3c-spec-campanias` |
| ad-creative-strategist | `s3a-copy-landings`, `s3d-creativos-ads` |
| tracking-specialist | `s3e-setup-tracking` |
| search-query-analyst | `s4a-operar-gates` (cada 2-4 semanas de gasto activo) |
| campaign-auditor | `s4a-operar-gates` (cada 4 semanas, o ante una anomalía) |

---

## Cómo se encadenan fuera del playbook

Caso típico: una cuenta nueva donde hay que armar la publicidad desde cero, sin correr un piloto
entero.

1. **google-ads-strategist** → estructura de cuenta, keywords, tipos de concordancia, reparto de presupuesto.
2. **tracking-specialist** → píxel, CAPI y acciones de conversión, **antes** de prender nada.
3. **ad-creative-strategist** → RSAs, creativos de Meta y variantes para testear.
4. **meta-ads-strategist** → audiencias y ad sets full-funnel, si hay presupuesto para dos plataformas.
5. Se enciende. Pasadas dos semanas de gasto:
6. **search-query-analyst** → primera cosecha de negativos e ideas de keywords nuevas.
7. Cada cuatro semanas: **campaign-auditor** liviano sobre lo que está corriendo.

El orden importa en un punto y solo en uno: el tracking va antes del encendido. Todo lo demás se
puede reordenar según lo que tengas a mano.

---

## Cómo se usan

**Manual.** Abrís el archivo, pegás la persona y el framework al inicio de una sesión con tu
asistente, sumás tus datos y ejecutás. Es lo más simple y no necesita nada instalado.

**Como comando propio.** Si tu asistente soporta comandos o atajos definidos por vos, envolvé cada
rol en uno (`/ads-ppc`, `/ads-meta`, `/ads-creative`, y así) apuntando a estos archivos como fuente
de verdad. El wrapper queda fino: la doctrina vive acá, no duplicada adentro del comando.

**Como skill formal.** Si un rol lo usás tres veces o más y siempre con el mismo flujo, conviene
convertirlo en un skill con sus pasos y sus scripts. Antes de eso, no: es sobre-construir.

---

## Calibración

Los roles están escritos para presupuestos chicos y medianos, una cuenta por negocio, sin
estructura de agencia multi-cliente. Si administrás decenas de cuentas con un equipo, los
frameworks siguen valiendo pero las reglas operativas (cadencia de revisión, umbrales, quién toca
qué) te van a quedar cortas.

Lo que no depende del tamaño: la clasificación de intención de búsqueda, los niveles de estructura
de cuenta, el análisis de n-grams, la deduplicación de conversiones y la jerarquía de conversiones.
Eso es la parte que vale y se sostiene sola.
