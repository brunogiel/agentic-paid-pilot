---
name: captura-y-crm
description: >-
  Componente del kit de leadgen: captura de leads server-side + persistencia en el CRM del piloto.
  Usar cuando el usuario diga "conectá el form al CRM", "guardame los leads", "que el lead caiga en
  Notion/Sheets/Supabase", "armame el endpoint del form", "no quiero leads duplicados", "el upsert de
  leads", "cómo califico al lead", "el stage del lead". Cubre: endpoint propio, upsert por email,
  asignación y avance de stage, validación server-side, modo dry y resiliencia (nunca romper el flujo
  del usuario). El CRM concreto es intercambiable; lo que se reusa es el patrón.
---

# Captura y CRM

## 1. First principles

### Qué problema resuelve

Llevar cada lead del form al CRM sin perderlo, sin duplicarlo y con un estado confiable, aunque el CRM esté caído, el usuario mande el form dos veces o un paso del funnel nunca llegue.

La pieza clave NO es el CRM: **es un endpoint propio server-side entre el form y el CRM.** El form nunca habla directo con la base. El endpoint valida, dedupea, asigna estado y absorbe fallas. Con ese patrón, el CRM de atrás es un detalle intercambiable.

**El CRM en Notion es UNA opción del menú, no LA respuesta.** Sheets, Supabase o el CRM que el proyecto ya tenga valen igual. Lo reusable es el patrón: upsert server-side por email + stage que solo avanza.

### Cuándo conviene y cuándo NO

- Conviene siempre que haya un form propio y un equipo que necesita ver/trabajar los leads (piloto con partner, handoff a quien cierra).
- **NO** hace falta si el funnel entero vive en una plataforma que ya persiste (ej. lead forms nativos de Meta con su CRM sync): no dupliques persistencia al pedo.
- **NO** empieces eligiendo el CRM. Definí el patrón (upsert + stages) y después elegí dónde viven las filas según quién las va a mirar.

### Invariantes (sí o sí, sin esto no funciona)

- **El cliente nunca manda IDs del CRM.** El matching es por email, server-side. Nadie desde el browser puede pisar filas ajenas.
- **Upsert por email**: si ya existe una fila con ese email, se actualiza (la más reciente); si no, se crea. Un humano = una fila.
- **Validación server-side con listas cerradas**: los selects (industria, facturación, etc.) se validan contra las opciones exactas del CRM. Un valor inventado se rechaza o se descarta, nunca se inserta crudo.
- **Stage por reglas al entrar** (calificado No→Descartado; fuente de nurture→Nurture; fuente desconocida→New conservador, que lo revise un humano).
- **El stage solo avanza, nunca retrocede**: si un humano ya movió el lead, un POST tardío del funnel no lo degrada. La única pisada permitida es descartar.
- **Nunca romper el flujo del usuario**: timeouts cortos (3s) en todo lo externo y responder `ok: true` aunque el CRM falle (con log del error). El usuario siempre llega a la thank-you.
- **Modo dry** para smoke tests (`?dry=1` o un marcador en el email) que corta ANTES de tocar CRM o notificaciones.
- **Log crudo de cada lead** (console/archivo) como red final: si todo lo demás falla, el lead se recupera del log.
- Respetar los límites del CRM destino (largos de texto, tipos): truncar antes de mandar, no perder el lead por un 400.

### Success metrics

- 0 leads perdidos: todo POST válido termina en el CRM o en el log recuperable.
- 0 duplicados por email en el CRM.
- 0 usuarios que vieron un error por una falla del CRM.
- El stage de cada fila refleja las reglas (spot-check con leads de prueba).

## 2. Menú de stack sugerido

| Opción | Trade-offs | Cuándo tiene sentido |
|---|---|---|
| **Notion database** ⭐ probada en un piloto real de referencia | UI lista para compartir con el equipo, vistas y filtros gratis. API con límites molestos (selects estrictos, rich_text 2000 chars, sin transacciones), query lenta | Piloto con partner no técnico que necesita VER y tocar los leads ya. Volumen chico (decenas/semana) |
| **Google Sheets** | Cero fricción de adopción, todos saben usarlo. Sin tipos, sin locking, fórmulas se rompen al insertar filas por API | El equipo ya vive en Sheets y el piloto es corto. Cuidado con el matcheo por posición de fila |
| **Supabase / Postgres** | Tipos, constraints, upsert nativo (`on conflict`), escala. Requiere armar una UI o un dashboard aparte para no técnicos | Ya hay código en el proyecto o el piloto va camino a producto. La opción más sólida a mediano plazo |
| **El CRM que el negocio ya usa** (HubSpot, Pipedrive, lo que sea) | El equipo comercial no cambia de herramienta; API madura. Mapear stages ajenos + otro vendor en el medio | El que cierra ya trabaja ahí. No lo saques de su herramienta para meterlo en la tuya |

Cómo rindió Notion en un piloto real de referencia: cero leads perdidos, el CRM compartido con el equipo funcionó como única fuente de verdad del funnel, y el patrón upsert absorbió sin drama forms repetidos y pasos fuera de orden. Los dolores fueron los límites de la API (opciones de select exactas o se crean opciones nuevas en la DB compartida, truncados obligatorios) y que toda consulta agregada es lenta.

**Son sugerencias, no obligaciones. Antes de elegir, vale buscar si apareció una opción nueva o mejor.**

## 3. Puntero a la receta

Si elegís la opción probada (endpoint Next.js + Notion), seguí **[reference.md](reference.md)**: tiene el route handler completo, las reglas de stage, el flujo de 2 pasos con fallback, el modo dry y los gotchas de la API de Notion.

## Cómo se usa (flujo)

1. [DET] Definir el esquema del lead: campos del form (paso 1 y paso 2 si hay), listas cerradas de opciones, reglas de calificación y stages.
2. [DET] Elegir CRM del menú según quién mira los leads.
3. [DET] Implementar el endpoint con los invariantes (receta en reference.md si es la probada; el patrón aplica igual a cualquier CRM).
4. [LATENT] Mapear fuentes (`source`) a stage de entrada: qué fuentes son nurture, cuáles son intención caliente.
5. [DET] Smoke test en dry + un lead real de punta a punta verificando fila, stage y notificación.

## Output esperado

- Endpoint `/api/lead` (o equivalente) deployado con upsert, validación, stages, dry mode y timeouts.
- CRM con el esquema de columnas/propiedades definido y compartido con el equipo.
- Un lead de prueba visible en el CRM con stage correcto + el caso duplicado verificado (mismo email dos veces = una fila).

## Success metrics

Las de First principles: 0 perdidos, 0 duplicados, 0 errores visibles al usuario, stages consistentes con las reglas.
