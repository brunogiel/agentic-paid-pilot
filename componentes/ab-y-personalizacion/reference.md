# Receta probada: middleware Next.js + diccionarios client-side

> Destilada de un piloto real de leadgen (2 dominios, 2 idiomas, 9 verticales personalizadas). Los snippets son equivalentes genéricos del código que corrió en producción; ejemplo hipotético: un estudio contable que personaliza por rubro del cliente.

## Mapa de la receta

- **Split A/B (server-side)**: un `middleware.ts` decide control vs challenger con una cookie propia y reescribe el root a la página HTML correspondiente. Puede además resolver idioma por host si corrés 2 dominios.
- **Personalización por slug (client-side)**: script inline al final del body con 3 diccionarios (hero, testimonio, FAQ) indexados por el slug de `?v=`.
- **Wiring al tracking y al CRM**: el handler del form arma la atribución una sola vez (`variant` + UTMs + cookie de A/B) y la mete en el evento de tracking y en el POST al endpoint de leads.

## 1. El split (middleware.ts)

Corre en edge, matcher solo en `/`. Lógica completa:

```ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const COOKIE_NAME = "ab_pilot";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 30; // 30 días
const SPLIT_EXP = 0; // fracción de tráfico al challenger. 0 = todos al control.

export function middleware(request: NextRequest) {
  const url = request.nextUrl;

  // Precedencia: 1) ?ab= (QA/remarketing, fuerza Y persiste)  2) cookie  3) sorteo
  const abParam = url.searchParams.get("ab");
  const cookieVariant = request.cookies.get(COOKIE_NAME)?.value;

  let variant: "exp" | "ctrl";
  if (abParam === "exp" || abParam === "ctrl") variant = abParam;
  else if (cookieVariant === "exp" || cookieVariant === "ctrl") variant = cookieVariant;
  else variant = Math.random() < SPLIT_EXP ? "exp" : "ctrl";

  const dest = variant === "exp" ? "/landing-challenger.html" : "/landing-control.html";

  // Arrastrar los query params al destino reescrito (UTMs, gclid, ?v= sobreviven).
  const response = NextResponse.rewrite(new URL(dest + url.search, request.url));

  response.cookies.set(COOKIE_NAME, variant, {
    maxAge: COOKIE_MAX_AGE, path: "/", sameSite: "lax",
    httpOnly: false, // el frontend la lee para mandarla en el tracking
  });
  return response;
}

export const config = { matcher: ["/"] };
```

Puntos que importan:

- **URL limpia**: el usuario ve el root, nunca el nombre del archivo de la variante. El rewrite es invisible (no redirect).
- **`SPLIT_EXP = 0` deja la lógica viva**: el 100% va al control, pero el challenger sigue accesible por `?ab=exp` (un adset de remarketing puede apuntar directo ahí) y encender el A/B es cambiar un número.
- **`httpOnly: false` es a propósito**: el script de la landing lee la cookie para adjuntarla al payload de tracking. Si la hacés httpOnly, perdés esa pata.
- Si corrés 2 idiomas por dominio, el mismo middleware resuelve idioma por `request.headers.get("host")` antes de elegir el archivo.
- Las landings viejas quedan accesibles por su path directo como backup.

## 2. La personalización por slug (script inline)

Tres diccionarios indexados por el valor de `?v=`. Cada uno toca una zona distinta de la página. Ejemplo con un estudio contable que corre ads por rubro:

```js
(function(){
  // Hero: headline + subhead por rubro
  var V = {
    gastronomia: { h: "Enfocate en tu restaurante, no en los papeles.", s: "Llevamos tus impuestos y sueldos al día, vos manejás el salón." },
    ecommerce:   { h: "Vendé más. De la contabilidad nos ocupamos nosotros.", s: "Facturación, IIBB y stock conciliado sin que pierdas una tarde." },
    profesionales: { h: "Tu matrícula es atender clientes, no cargar facturas.", s: "Monotributo o RI, te dejamos los números claros todos los meses." }
  };
  var p = new URLSearchParams(location.search).get('v');
  var v = p && V[p];
  if (v) {
    var h = document.getElementById('v-headline'), s = document.getElementById('v-subhead');
    if (h && v.h) h.textContent = v.h;
    if (s && v.s) s.textContent = v.s;
  }
  // Si el slug no matchea: no se toca NADA, queda el default completo.
})();
```

**Testimonio y FAQ por slug**: en vez de IDs, hooks declarativos en el HTML (`data-variant-review-text`, `data-variant-review-name`, `data-variant-faq-q`, `data-variant-faq-a`) y dos diccionarios más (`R` para el testimonio con cita/iniciales/nombre/rol, `F` para la pregunta frecuente del rubro). El patrón es el mismo: buscar el hook con `querySelector('[data-variant-...]')` y pisar `textContent`. Gotcha: si el elemento tiene hijos que querés conservar (ej. un ícono dentro del `<summary>` del FAQ), reemplazá el texto y re-appendeá el hijo, no uses `innerHTML`.

**Foto de hero por vertical**: precarga con `new Image()` y recién pinta en `onload`, con un veil de gradiente encima para que el texto siga legible:

```js
if (p) {
  var hb = document.getElementById('hero-bg');
  var img = new Image(), src = '/variantes/' + p + '.png',
      veil = "linear-gradient(to bottom, rgba(255,255,255,.86) 0%, rgba(255,255,255,1) 100%)";
  img.onload = function(){ hb.style.backgroundImage = veil + ",url('" + src + "')"; hb.style.opacity = "1"; };
  img.src = src;
}
```

Si la imagen del slug no existe, `onload` nunca dispara y queda el fondo default: degradación silenciosa, nunca un 404 visible.

## 3. El slug en el tracking y el payload del lead

El handler del form arma la atribución una sola vez y la usa en los dos lados:

```js
function abCookie(){ var m = document.cookie.match(/(?:^|; )ab_pilot=([^;]*)/); return m ? decodeURIComponent(m[1]) : ''; }
var qp = new URLSearchParams(location.search);
function attr(){ return {
  variant: (qp.get('v') || 'default'),   // el slug, o 'default' explícito
  utm_campaign: qp.get('utm_campaign') || '',
  utm_content: qp.get('utm_content') || '',
  ab: abCookie()                          // la rama del A/B
};}

var payload = Object.assign({ email: em, source: 'landing-hero', language: 'es' }, attr());
dataLayer.push(Object.assign({ event: 'email_captured' }, payload));                      // tracking
fetch('/api/lead', { method: 'POST', headers: {'Content-Type':'application/json'},
                     keepalive: true, body: JSON.stringify(payload) });                   // CRM
```

Esto cierra el invariante central: el string del slug que puso la campaña en `?v=` llega intacto al evento de tracking y al campo `Variant` del CRM (el componente `captura-y-crm` lo persiste server-side, truncado a un largo sano).

## 4. Gobernanza del A/B de concepto

- El A/B serio se corre **externo y coherente**: en Google, campañas espejo (misma estructura, budget partido) o Experiments 50/50, con el brazo challenger apuntando a `…/?ab=exp` y el control al root. Así la promesa del anuncio y la landing siempre coinciden.
- El middleware es el guardián de la estabilidad: aunque el usuario vuelva después por el root sin `?ab=`, la cookie lo mantiene en su rama 30 días.
- El veredicto sale de comparar las campañas espejo (CTR/CPC/conversiones por rama), no hace falta una herramienta de A/B aparte.

## 5. Gotchas reales

- **Duplicación manual de copy entre idiomas**: si corrés 2 idiomas, los diccionarios existen por duplicado en cada HTML. Cada cambio de copy se aplica dos veces a mano y se desincronizan si no sos prolijo. Si arrancás de cero, generá ambos desde una fuente única.
- El switcher de idioma tiene que **arrastrar el query string** (`link.href = '/otra-lengua.html' + location.search`), si no el usuario que cambia de idioma pierde slug y UTMs.
- `Math.random()` corre bien en el edge runtime de Vercel; no hace falta nada exótico para el sorteo.
- Los slugs son **contrato con las campañas**: el spec de campañas define `?v=` por ad group y los diccionarios deben cubrir exactamente esos slugs. Un typo en el ad = default silencioso (no error), así que QA con las URLs finales reales.

## Credenciales e infra a reusar

Dominios, deploy y cuentas del stack: completá tu propio inventario en `../../reference/infra-y-credenciales.md` (plantilla del kit; nunca commitees valores reales).
