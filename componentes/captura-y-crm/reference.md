# Receta probada: endpoint Next.js + Notion CRM

> Destilada de un piloto real de leadgen que corrió en producción con este patrón. Los snippets son equivalentes genéricos del código real; ejemplo hipotético: un estudio contable que captura leads por rubro y facturación. El patrón (upsert por email + stage que solo avanza) es portable a cualquier CRM; acá está la implementación con Notion.

## Arquitectura

```
form (browser) ──POST /api/lead──▶ route handler ──▶ Notion (upsert por email)
                                       │
                                       └──▶ webhook de notificación al equipo (fire-and-forget)
```

El browser manda JSON plano (nunca IDs del CRM). El route handler hace TODO: validación, matching, stage, notificación, resiliencia. Env vars: `NOTION_TOKEN`, `NOTION_DATABASE_ID`, `NOTIFY_WEBHOOK_URL`.

## 1. El tipo Lead y el flujo de 2 pasos

El funnel captura en 2 pasos: paso 1 = alta (email + opcionales desde la landing), paso 2 = calificación (rubro + facturación desde la thank-you). El payload del paso 2 lleva una copia del paso 1:

```ts
type Lead = {
  step?: number;
  name?: string; email?: string; phone?: string;
  industry?: string; revenue?: string; message?: string;
  variant?: string; language?: string;
  utm_campaign?: string; utm_content?: string;
  qualified?: string; source?: string;
  step1?: Lead;    // copia del payload del paso 1 (sessionStorage) como fallback
  dry?: boolean;   // smoke test: corta antes de tocar nada
};
```

**Por qué `step1` viaja en el paso 2**: si el POST del paso 1 nunca llegó (red, adblock), el paso 2 recrea la fila completa con ese fallback. La landing lo guarda en `sessionStorage` al capturar el email.

## 2. Listas cerradas server-side

Las opciones de los selects se validan contra las opciones EXACTAS de la DB de Notion. Cualquier otro valor crearía opciones nuevas en la DB compartida (gotcha real de Notion: el create no valida contra el schema):

```ts
const INDUSTRIES = ["Gastronomía", "E-commerce", "Servicios profesionales", "Construcción", "Otro"];
const REVENUES = ["Menos de $50M", "$50M–$200M", "$200M–$1.000M", "Más de $1.000M"];
const OUT_INDUSTRIES = ["Construcción"];  // verticales fuera del ICP: descalifican siempre
```

En el paso 2: `INDUSTRIES.includes(valor) ? valor : ""` y si queda vacío, 400 con `missing-or-invalid-fields`. La calificación también es server-side: `qualified = OUT_INDUSTRIES.includes(industry) || revenue === "Menos de $50M" ? "No" : "Yes"` (el bucket "Otro" NO descalifica: lo revisa un humano).

## 3. Asignación de stage al entrar

```ts
const NURTURE_SOURCES = ["guia-remarketing", "landing-guia", "hero-email-first"];
const isNurture = NURTURE_SOURCES.includes(String(lead.source || ""));
const stage = lead.qualified === "No" ? "Discarded" : isNurture ? "Nurture" : "New";
```

Reglas, en orden:
1. Descalificado → `Discarded`.
2. Fuente en la lista de nurture (lead magnet, email-first) → `Nurture`.
3. Fuente desconocida → `New` **conservador**: que un humano lo revise, no enterrarlo en Nurture.

⚠ Gotcha real: cada vez que se agrega una fuente nueva en el frontend hay que sumarla a `NURTURE_SOURCES`, o esos leads entran como `New`. Pasó en el piloto de referencia con las sources de un popup nuevo.

**El stage solo se pisa para descartar.** En el paso 2, si el lead califica, NO se toca `Stage`: quien cierra pudo haberlo movido a `Scheduled` o `Call Done` a mano, y el POST tardío no debe degradarlo:

```ts
const props = { Industry: {...}, "Annual revenue": {...}, Qualified: {...} };
if (qualified === "No") props.Stage = { select: { name: "Discarded" } };  // única pisada permitida
```

## 4. Upsert por email (el cliente nunca manda IDs)

```ts
async function findByEmail(email: string): Promise<string | null> {
  const r = await fetch(`https://api.notion.com/v1/databases/${NOTION_DB}/query`, {
    method: "POST", headers: NOTION_HEADERS,
    body: JSON.stringify({
      filter: { property: "Email", email: { equals: email } },
      sorts: [{ timestamp: "created_time", direction: "descending" }],
      page_size: 1,
    }),
    signal: AbortSignal.timeout(3000),
  });
  if (!r.ok) { console.error("Notion query error", r.status, await r.text()); return null; }
  const data = await r.json();
  return data?.results?.[0]?.id || null;
}
```

- El matching vive **acá, server-side**: nadie desde el browser puede pisar filas ajenas.
- Se toma **la fila más reciente** con ese email (sort por `created_time` desc).
- Si existe → `PATCH /v1/pages/{id}` solo con los campos nuevos. Si no → `POST /v1/pages` con la fila completa.
- Si `findByEmail` falla (timeout, 500), devuelve `null` y el flujo crea fila nueva: preferimos un posible duplicado a un lead perdido.

## 5. Resiliencia: nunca romper el flujo del usuario

- **Timeout 3s en TODA llamada externa** (`AbortSignal.timeout(3000)`): query, create, update y el webhook de notificación.
- **`ok: true` aunque el CRM falle**: el catch responde `{ ok: true, stored: false }` con status 200. El form sigue a la thank-you; el lead queda en el log.
- **Log crudo SIEMPRE, antes de todo**: `console.log("LEAD", JSON.stringify(lead))`. Es la red final: si el CRM no estaba configurado o falló, el lead se recupera de los logs del hosting.
- **La notificación es fire-and-forget**: try/catch propio, nunca bloquea ni afecta la respuesta. El payload lleva `type: "new" | "update"` para que el workflow de notificación distinga alta de actualización con un Switch.

## 6. Modo dry (smoke tests)

```ts
if (lead.dry === true) {
  console.log("LEAD DRY", JSON.stringify(lead));
  return NextResponse.json({ ok: true, dry: true });
}
```

Corta ANTES del dispatch a paso 1/paso 2: no notifica a nadie ni escribe en el CRM. El frontend lo activa con `?dry=1` en la URL o un email con `+dry@`. Imprescindible para probar el funnel en prod sin ensuciar el CRM ni spamear al equipo.

## 7. Límites de Notion (truncados obligatorios)

Notion rechaza `rich_text` > 2000 chars con un 400, y perderíamos el lead. Todo campo de texto libre se trunca antes de mandar:

```ts
if (lead.message) props.Message = { rich_text: [{ text: { content: String(lead.message).slice(0, 1900) } }] };
if (lead.variant) props.Variant = { rich_text: [{ text: { content: String(lead.variant).slice(0, 200) } }] };
if (lead.utm_campaign) props["UTM campaign"] = { rich_text: [{ text: { content: String(lead.utm_campaign).slice(0, 500) } }] };
```

Ojo: `utm_*` vienen de la URL, o sea son controlables por terceros. El truncado también es una defensa.

Schema sugerido de la DB (el que corrió en el piloto de referencia): `Name` (title), `Stage` (select), `Email` (email), `Phone` (phone_number), `Industry` (select), `Annual revenue` (select), `Qualified` (select), `Source` (select), `Message`, `Variant`, `Language`, `UTM campaign`, `UTM content` (rich_text).

## 8. Portar el patrón a otro CRM

Lo que cambia es solo la capa de I/O (`findByEmail` / `create` / `update`):

- **Supabase/Postgres**: el upsert entero es un `insert ... on conflict (email) do update`, y las listas cerradas son constraints/enums. Más simple que Notion.
- **Sheets**: buscar por email con la API de valores y matchear por contenido de celda, NUNCA por número de fila (las filas corren cuando alguien inserta a mano).
- **CRM de terceros**: mapear los stages a los del pipeline existente y respetar el invariante "solo avanza" con el orden de stages de ese CRM.

Los invariantes (matching server-side, stage solo avanza, timeouts + ok:true, dry mode, log crudo) NO cambian con el destino.

## Credenciales e infra a reusar

Tokens, IDs de la DB y webhooks: completá tu propio inventario en `../../reference/infra-y-credenciales.md` (plantilla del kit; nunca commitees valores reales).
