---
name: copy-landings
description: >-
  Etapa 3 del playbook lanzar-piloto. Escribe el copy completo de las landings del piloto, por segmento/vertical e idioma: hero de dolor, social proof, pricing, FAQ de objeciones, CTA único, microcopy de confianza y privacy. Usar cuando el usuario diga "el copy de las landings de X", "escribí la landing de X", "hero para el segmento Y", "FAQ de la landing", "copy por vertical", "message match de los ads con la landing". Hereda el _backbone.md sin re-derivar. Los ángulos y el copy salen del rol ../roles/ad-creative-strategist.md. Escribe workspace/landing/landing-prompt.md (Parte B). NO buildea ni deploya (eso es build-landings) ni escribe ads (creativos-ads).
---

# Etapa 3 · copy-landings — el texto que convierte

Produce el copy customer-facing de cada variante de landing, listo para pegar en el build. El hero vende un dolor, no el servicio; el español es nativo, no traducción. (Reemplazá con tu propia corrida de referencia si ya escribiste landings de un piloto antes.)

## Parámetros
- `NEGOCIO`, `IDIOMA(S)` (del kickoff).
- Del backbone: segmentos canónicos, landings (cuáles y qué foco), CTA único, ICP + floor, verticales IN/OUT, marca por idioma.
- Del research: posiciones gastadas a evitar + posiciones sin ocupar (competitive), wedges.

## Prerequisitos
- `../roles/ad-creative-strategist.md` (framework de ángulos y copy: los mismos ejes de mensaje que alimentan los ads alimentan el hero y las secciones de la landing).

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/workspace/landing/landing-prompt.md` | **Escribe** (copy completo por landing, sección por sección) |
| `../roles/ad-creative-strategist.md` | **Lee** (ángulos, wedges, framework de copy) |
| `workspace/_backbone.md` | **Lee** (contrato: landings, CTA, segmentos, marca) |
| `workspace/research/competitive-brief.md` + `competitor-ads-swipe.md` | **Lee** (clichés a evitar, gaps a ocupar) |

## Flujo

**Paso 1 [LATENT] — Reglas de copy por piloto.** Fijar arriba del doc las reglas duras: sin em-dash en el copy en español (en inglés OK); marca por idioma si hay 2 dominios; español nativo, no traducción; nada de testimonios/números inventados (van como `[ABIERTO: ...]`); posiciones gastadas del competitive prohibidas como eje central.

**Paso 2 [LATENT] — Copy por landing.** Para cada landing del backbone, escribir sección por sección: hero (pain point + subhead + CTA + microcopy de confianza), "persona real / diferencial", sección educativa mid-page para tráfico frío, pricing/tiers visibles, social proof (con `[ABIERTO]` si no hay casos reales), timeline de onboarding, FAQ que maneja objeciones reales, CTA final + footer con disclaimer de alcance del servicio.

**Paso 3 [LATENT] — Verticales como slots.** Los verticales NO son landings nuevas: definir el texto intercambiable del hero por vertical (`?v=`) sobre la landing que corresponda, con el dolor específico del rubro.

**Paso 4 [LATENT] — Message match.** Cruzar contra los ad groups/adsets planificados: cada campaña tiene que aterrizar en un hero que cumple lo que el ad promete. Anotar el mapa campaña → landing → hero.

**Paso 5 [DET] — Privacy/Terms.** Generar el draft de Privacy Policy + Terms por idioma (requisito de Google/Meta para encender). Queda como entregable para que `build-landings` lo publique.

**Paso 6:** checkpoint con el usuario (lidera lo creativo): presentar el copy de a una landing, no el paquete cerrado.

## Aprendizajes de terreno

- **Claims defendibles en la primera call.** Todo claim de equipo, capacidad o seguridad se evalúa contra "¿esto se sostiene cuando el lead llama?", no solo contra si suena bien en el ad/landing. Un claim de "equipo" que en realidad es una sola persona operando se rompe en el primer contacto humano. Resolución tipo: en vez de bajar el claim del todo o mentir headcount, usar un frame intermedio defendible (ej. "tu especialista asignada del equipo") que sostiene el beneficio (backup, respaldo) sin prometer algo que no existe todavía.
- **El nombre de la oferta puede matar el click aunque el mensaje esté bien.** Testear el naming de la oferta en sí (no solo el copy alrededor): un nombre que suena a auditoría o a compromiso (ej. "Revisión Gratis" leído como "van a encontrar mis errores") genera defensiva antes de que el lead lea el resto. Si hay dudas sobre cómo suena una oferta, chequearlo con la lente del destinatario antes de escribir el resto de la landing alrededor.
- **BOFU sin asumir memoria.** No dar por hecho que el lead recuerda haber empezado el flujo ("Tu revisión sigue abierta", "ya casi estabas"): si el tracking del pool es flojo o pasó tiempo, ese supuesto puede ser falso y suena raro. Preferir una oferta autoexplicativa que se entiende sola, sin depender de que el lead recuerde una interacción previa.

## Output esperado

`workspace/landing/landing-prompt.md` con el copy completo de cada landing (todas las secciones), los slots por vertical, el mapa de message match y el draft de privacy/terms por idioma.

## Success metrics

- Hero de cada landing nombra un dolor, no describe el servicio.
- 0 em-dashes en el copy en español; 0 datos inventados sin `[ABIERTO]`.
- Cada landing del backbone tiene copy completo (ninguna sección en TODO).
- Ninguna posición gastada del competitive usada como eje central.

## Troubleshooting

- **Tentación de traducir:** si el segundo idioma suena a traducción, reescribir desde el dolor del segmento en ese idioma (a veces el segundo idioma tiene wedges propios: canal preferido, contexto cultural).
- **Sin social proof real:** no inventar; usar `[ABIERTO: testimonio real]` y compensar con credenciales verificables (badge, años, precio público).
- **Demasiadas landings:** si un segmento solo cambia el sustantivo del hero, es un `?v=`, no una landing nueva (multiplica mantenimiento al pedo).
