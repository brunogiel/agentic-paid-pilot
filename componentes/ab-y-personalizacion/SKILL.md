---
name: ab-y-personalizacion
description: >-
  Componente del kit de leadgen: A/B testing de concepto + personalización de landing por vertical/segmento.
  Usar cuando el usuario diga "quiero testear dos versiones de la landing", "armame el A/B", "personalizá la
  landing por rubro", "que el headline cambie según el anuncio", "el split de control y challenger", "cómo
  reparto el tráfico", "una landing por vertical sin duplicar páginas". Cubre: split estable por cookie
  (middleware), personalización client-side por slug (?v=), y cómo la variante viaja hasta el CRM.
---

# A/B y personalización

## 1. First principles

### Qué problema resuelve

Un piloto necesita probar mensajes distintos sin multiplicar landings ni campañas. Acá viven dos mecanismos que se confunden pero son cosas distintas:

1. **A/B de concepto**: dos páginas enteras compitiendo (control vs challenger, ej. voz "agencia" vs voz "persona"). Se decide con un split de tráfico y se mide cuál convierte.
2. **Personalización por slug**: UNA página que se ajusta al segmento del anuncio (`?v=gastronomia` cambia headline, testimonio, FAQ y foto). No es un test: es coherencia anuncio→landing.

**El principio central del componente: un solo slug de vertical viaja idéntico por landing, tracking y CRM.** El anuncio manda `?v=gastronomia`, la landing personaliza con `gastronomia`, el evento de tracking lleva `variant=gastronomia`, y el lead cae al CRM con `Variant: gastronomia`. Si el slug se traduce, se renombra o se pierde en algún salto, la atribución muere y no podés responder "qué vertical convierte".

### Cuándo conviene y cuándo NO

- **Personalización por slug: casi siempre.** Es barata (diccionarios client-side) y sube la coherencia anuncio→landing sin duplicar páginas.
- **A/B de concepto: solo con tráfico suficiente.** Con presupuestos de piloto (decenas de clics/día) el A/B de micro-copy no llega nunca a significancia. Reservalo para diferencias GRANDES de concepto (posicionamiento, oferta, estructura), no para el color del botón.
- **NO** montar A/B antes de validar que el funnel captura algo. Primero un control que funcione, después el challenger.
- **NO** personalizar si todavía no sabés qué verticales vas a correr: el diccionario se escribe cuando existen los ad groups.

### Invariantes (sí o sí, sin esto no funciona)

- La asignación de variante A/B es **estable por usuario** (cookie): un visitante nunca ve las dos versiones.
- Precedencia de asignación fija: **override manual (query param) > cookie existente > sorteo nuevo**. El override fuerza Y persiste (sirve para QA y para apuntar remarketing a una rama).
- **Default seguro**: slug no reconocido = página genérica completa. Nunca una página rota o a medio personalizar.
- El slug/variante **viaja en cada evento de tracking y en el payload del lead** al CRM. Mismo string, sin traducir.
- El A/B de concepto se corre con **split externo y coherente**: la campaña que promete el concepto X aterriza en la landing X (campaña persona→landing persona). No mezclar.
- Los query params **se arrastran** al destino reescrito (UTMs, gclid, `?v=` sobreviven al rewrite).

### Success metrics

- 100% de los leads en el CRM tienen variante legible (o "default" explícito).
- El split real observado coincide con el configurado (verificable en analytics por cookie).
- La personalización no agrega flicker perceptible ni rompe la página cuando el slug no matchea.

## 2. Menú de stack sugerido

| Opción | Trade-offs | Cuándo tiene sentido |
|---|---|---|
| **Middleware edge (Next.js/Vercel) + diccionarios client-side** ⭐ probada en un piloto real de referencia | Sin flicker en el split (server-side rewrite), cookie propia, cero herramientas nuevas. Requiere código propio y deploy | Ya tenés la landing en Next/Vercel y querés control total sin sumar vendors |
| **Split por campañas espejo + Google Ads Experiments** | El split lo hace el ad platform (50/50 por Final URL con `?ab=`), medición dentro de Ads. No cubre tráfico orgánico/directo | El A/B es de concepto y todo el tráfico es pago. Complementa al middleware, no lo reemplaza |
| **Herramienta de A/B client-side (PostHog, GrowthBook, VWO)** | Setup visual, stats hechas. Flicker posible, script de terceros, otro vendor que aprender | Hay volumen real, equipo no técnico tocando variantes, o ya usás la herramienta para analytics |
| **Landings duplicadas en el builder (una página por variante)** | Cero código, pero N páginas que mantener a mano y el copy se desincroniza | La landing vive en un builder sin lógica (Unbounce, Framer, Lovable) y son 2-3 variantes máximo |

Cómo rindió en un piloto real de referencia (servicios profesionales, 2 idiomas): el middleware sirvió el control al 100% con el challenger accesible por `?ab=exp`; el A/B de voz corrió por campañas espejo en Google y una rama ganó claro en CTR y CPC (aprox. 6% vs 4%), aunque ambas quedaron sin conversiones (señal de tope de embudo, no del copy). La personalización por `?v=` corrió estable en 9 verticales sin incidentes.

**Son sugerencias, no obligaciones. Antes de elegir, vale buscar si apareció una opción nueva o mejor.**

## 3. Puntero a la receta

Si elegís la opción probada (middleware Next.js + diccionarios client-side), seguí **[reference.md](reference.md)**: tiene el middleware completo, la estructura de los diccionarios, el wiring del slug al tracking y al payload del lead, y los gotchas reales.

## Cómo se usa (flujo)

1. [DET] Definir qué corre: ¿A/B de concepto, personalización por slug, o ambos? Listar variantes y slugs (los slugs = los ad groups del spec de campañas).
2. [LATENT] Escribir los diccionarios de personalización por slug (headline, subhead, prueba social, FAQ) coherentes con el copy de cada ad group.
3. [DET] Implementar el mecanismo elegido del menú (receta en reference.md si es la probada).
4. [DET] Cablear el slug al tracking (evento de captura) y al payload del lead (campo Variant del CRM).
5. [DET] QA: probar cada slug real, un slug inventado (debe caer al default), el override `?ab=`, y verificar que la variante llega al CRM en un lead de prueba.

## Output esperado

- Mecanismo de split funcionando con asignación estable (si hay A/B).
- Diccionarios de personalización por slug con default seguro (si hay personalización).
- Un lead de prueba en el CRM mostrando la variante correcta, y el evento de tracking llevando el mismo string.

## Success metrics

Las de First principles: variante legible en el 100% de los leads, split observado = configurado, cero páginas rotas por slug desconocido.
