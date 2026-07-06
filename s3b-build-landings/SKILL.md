---
name: build-landings
description: >-
  Etapa 3 del playbook lanzar-piloto. Construye y deploya las landings del piloto: dominios (registro + DNS), prompt de build para el agente de código, repo local, motor de dynamic text ?v=, form que califica, webhook de lead (n8n) y deploy en Vercel. Usar cuando el usuario diga "buildeá las landings de X", "deployá la landing", "armá el repo de las landings", "subí esto a Vercel", "conectá el dominio", "el form de la landing". Consume el copy de copy-landings + el _backbone. NO escribe copy (copy-landings) ni instala tracking (setup-tracking, aunque deja los hooks listos).
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

## Flujo

**Paso 1 [DET] — Dominios.** Verificar disponibilidad (RDAP para TLDs regionales; MCP de dominios para `.com`), registrar los elegidos del backbone y conectarlos a Vercel. Regla: un dominio por idioma, mismo deploy; cada campaña apunta su Final URL al dominio del idioma correcto.

**Paso 2 [LATENT] — Prompt de build.** Escribir el prompt en 2 partes: (a) diseño visual (estructura de secciones, mood, mobile-first, base compartida entre variantes) y (b) agente de código para convertirlo en sitio real: copy de la Parte B, rutas, form, motor `?v=` (dynamic text del hero por vertical), thank-you page, y los hooks de tracking vacíos (gtag/fbq/dataLayer) para que `setup-tracking` los llene.

**Paso 3 [DET] — Repo + build.** Crear el repo en `~/Code/` siguiendo tu playbook de repos (tipo de proyecto; gitignore, config local). Ejecutar el build con el prompt.

**Paso 4 [DET] — Form + webhook.** El form prefiltra solo (gate del backbone: vertical OUT / floor → "no es el fit"); el submit calificado pega a un webhook n8n (skill `n8n-workflow-builder` si hay que crearlo) que escribe al CRM y avisa a quien cierra.

**Paso 5 [DET] — Deploy + QA visual.** `vercel deploy --prod` desde la carpeta del repo (NO desde la home). QA: responsive mobile, `?v=` cambia el hero, form submitea, dominios sirven el idioma correcto. Comparar contra el diseño aprobado e iterar.

**Paso 6:** devolver URLs live + repo al orquestador.

## Output esperado

Landings live en los dominios del backbone, repo en `~/Code/{negocio}-landings/` registrado en tu mapa de repos, `prompt-build.md` reusable, form + webhook funcionando, hooks de tracking listos para `setup-tracking`.

## Success metrics

- Cada landing del backbone responde 200 en su dominio + idioma correcto.
- `?v=` swapea el hero por vertical sin romper el resto.
- Submit de prueba llega al CRM y dispara el aviso (webhook E2E).
- Repo creado por tu playbook (no suelto en Documents) y registrado en el mapa.

## Troubleshooting

- **Deploy de Vercel agarra el proyecto equivocado:** deployar siempre desde la carpeta del repo; desde la home linkea mal.
- **Dominio elegido tomado:** volver al backbone con 2-3 alternativas chequeadas, no decidir solo (la marca la cierra el usuario).
- **Form sin prefiltro "para simplificar":** el prefiltro ES el experimento (cost-per-qualified-lead); si se saca, el gate de budget mide cualquier cosa.
