---
name: build-landings
description: >-
  Etapa 3 del playbook lanzar-piloto. Construye y deploya las landings del piloto: dominios (registro + DNS), prompt de build para el agente de código, repo local, motor de dynamic text ?v=, form que califica, webhook de lead (n8n), deploy en Vercel y scan de agent-readability de la landing publicada (`is-agentic`). Usar cuando el usuario diga "buildeá las landings de X", "deployá la landing", "armá el repo de las landings", "subí esto a Vercel", "conectá el dominio", "el form de la landing", "¿la landing se lee bien para un agente?", "pasale el is-agentic". Consume el copy de copy-landings + el _backbone. NO escribe copy (copy-landings) ni instala tracking (setup-tracking, aunque deja los hooks listos).
---

# Etapa 3 · build-landings — del copy al sitio en prod

Convierte el copy aprobado en landings live: repo, build, dominios y deploy. El stack de referencia es **diseño → agente de código (build) → Vercel (deploy)**; para pilotos chicos un estático self-contained alcanza, Next.js si hay lógica (form multi-paso, i18n). (Reemplazá con tu propia corrida de referencia si ya buildeaste landings de un piloto antes.)

## Parámetros
- `NEGOCIO`, `IDIOMA(S)` (del kickoff); marca + dominios por idioma (del backbone).
- Copy completo de `copy-landings` (Parte B) como input del build.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `~/Code/{negocio}-landings/` | **Crea** (repo nuevo, siguiendo tu playbook de repos) |
| Dominios + Vercel | **Registra/conecta** (un dominio por idioma, mismo deploy) |
| `{NEGOCIO}/workspace/landing/prompt-build.md` | **Escribe** (prompt de build copy-pasteable) |
| `workspace/_backbone.md § Landings` | **Lee** (qué landings, qué dominio sirve cada una) |
| MCP / CLI de dominios | **Usa** (disponibilidad + registro) |
| `npx is-agentic {dominio}` | **Corre** (scan de agent-readability sobre cada dominio live, post-deploy) |

## Flujo

**Paso 1 [DET] — Dominios.** Verificar disponibilidad (RDAP para TLDs regionales; MCP de dominios para `.com`), registrar los elegidos del backbone y conectarlos a Vercel. Regla: un dominio por idioma, mismo deploy; cada campaña apunta su Final URL al dominio del idioma correcto.

**Paso 2 [LATENT] — Prompt de build.** Escribir el prompt en 2 partes: (a) diseño visual (estructura de secciones, mood, mobile-first, base compartida entre variantes) y (b) agente de código para convertirlo en sitio real: copy de la Parte B, rutas, form, motor `?v=` (dynamic text del hero por vertical), thank-you page, y los hooks de tracking vacíos (gtag/fbq/dataLayer) para que `setup-tracking` los llene.

**Lo que la landing necesita para que un agente la lea, va en el prompt de build y no se parchea después:** JSON-LD con un tipo de identidad (`Organization` o `LocalBusiness` para un negocio de servicios) con `name`, `url`, `description`, `contactPoint` y `address`; `/about`, `/contact` y `/privacy` con 500+ caracteres reales cada una (la de privacy es obligatoria igual para que Meta apruebe el ad, así que las otras dos son el único trabajo nuevo); un 404 que devuelva status 404 de verdad y un cuerpo en Markdown cuando el request trae `Accept: text/markdown`; y un `llms.txt` que diga **cuándo** conviene usarte, no qué vendés. Construirlo de entrada cuesta minutos. Agregarlo después es tocar una landing que ya está comprando tráfico.

**Paso 3 [DET] — Repo + build.** Crear el repo en `~/Code/` siguiendo tu playbook de repos (tipo de proyecto; gitignore, config local). Ejecutar el build con el prompt.

**Paso 4 [DET] — Form + webhook.** El form prefiltra solo (gate del backbone: vertical OUT / floor → "no es el fit"); el submit calificado pega a un webhook n8n (skill `n8n-workflow-builder` si hay que crearlo) que escribe al CRM y avisa a quien cierra.

**Paso 5 [DET] — Deploy + QA visual.** `vercel deploy --prod` desde la carpeta del repo (NO desde la home). QA: responsive mobile, `?v=` cambia el hero, form submitea, dominios sirven el idioma correcto. Comparar contra el diseño aprobado e iterar.

**Paso 6 [DET] — Scan de agent-readability.** Con cada dominio ya live:

```bash
npx -y is-agentic@latest {dominio} --json
```

Dispara el scan y devuelve el reporte en ~20-25 s: `score` sobre 100, `score_breakdown` (`essential` / `recommended` / `bonus`) e `issues[]` con **solo** los checks que no pasaron (`failed` o `partial`), cada uno con su fix textual. Sin `--json` sale el mismo reporte legible en la terminal; el informe web queda en `https://is-agentic.com/scan/{dominio}`. Anotar el score en `workspace/landing/` y resolver los `essential` que fallen **antes** del encendido: esta es la ventana barata, después se toca con tráfico encima. Los `recommended` van al backlog del piloto salvo que sean gratis.

**Paso 7:** devolver URLs live + repo + score del scan al orquestador.

## Output esperado

Landings live en los dominios del backbone, repo en `~/Code/{negocio}-landings/` registrado en tu mapa de repos, `prompt-build.md` reusable, form + webhook funcionando, hooks de tracking listos para `setup-tracking`.

## Success metrics

- Cada landing del backbone responde 200 en su dominio + idioma correcto.
- `?v=` swapea el hero por vertical sin romper el resto.
- Submit de prueba llega al CRM y dispara el aviso (webhook E2E).
- Repo creado por tu playbook (no suelto en Documents) y registrado en el mapa.
- El scan de `is-agentic` corrió sobre cada dominio live, su score quedó anotado, y los `essential` que fallan están resueltos o aceptados a propósito (no ignorados).

## Troubleshooting

- **Deploy de Vercel agarra el proyecto equivocado:** deployar siempre desde la carpeta del repo; desde la home linkea mal.
- **Dominio elegido tomado:** volver al backbone con 2-3 alternativas chequeadas, no decidir solo (la marca la cierra el usuario).
- **Form sin prefiltro "para simplificar":** el prefiltro ES el experimento (cost-per-qualified-lead); si se saca, el gate de budget mide cualquier cosa.
- **La API de is-agentic devuelve 404 `report_not_found`:** es de solo lectura y no dispara scans. Un dominio recién publicado no tiene reporte hasta que alguien lo escanea. Corré el CLI una vez (`npx -y is-agentic@latest {dominio}`) y recién ahí `GET https://is-agentic.com/api/v1/report?url=https://{dominio}` sirve el JSON. Pegarle a `/scan/{dominio}` con curl tampoco alcanza: devuelve la página, no el scan.
- **El check `brand-search-accuracy` falla y no hay nada que hacer:** mide si una búsqueda de tu marca devuelve tu dominio. Un dominio de piloto recién registrado no está indexado, así que falla por definición. No se persigue en la Etapa 1 y no cuenta como abierto.
