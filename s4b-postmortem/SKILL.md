---
name: postmortem
description: >-
  Etapa 4 del playbook. Cierra un piloto: escribe el postmortem
  canónico (con rigor estadístico y sin generalizar de más), lo pasa por una
  revisión con lentes distintas antes de mandarlo al partner, corre el
  checklist de cierre operativo (pausar gasto, apagar bots, rotar
  credenciales, archivar) y destila los aprendizajes a sus destinos (skill,
  Resources, memoria, próximo piloto). Usar cuando el usuario diga "cerremos
  el piloto de X", "escribí el postmortem de X", "el piloto se terminó, qué
  aprendimos", "checklist de cierre de X", "apaguemos todo lo de X", "qué le
  queda pendiente a X", "destilá los aprendizajes de X". Escribe
  postmortem.md + workspace/checklist-cierre.md. NO decide el veredicto del
  gate (eso ya lo resolvió operar-gates, Paso 5) ni sigue operando canales
  (esta etapa es el cierre, no el día a día).
---

# Etapa 4 · postmortem: cerrar el piloto sin perder lo aprendido

Un piloto que termina sin postmortem formal pierde la mitad de su valor: la
plata ya se gastó, y si el aprendizaje no queda destilado en un formato
reusable, el próximo piloto repite los mismos errores de medición y de
cierre. Este skill formaliza el cierre: qué se escribe, quién lo revisa antes
de mandarlo, qué se apaga, y a dónde va cada aprendizaje. (Reemplazá la
referencia de "un postmortem real" de abajo con tu propia corrida cuando
tengas una.)

## Parámetros

- `NEGOCIO`, veredicto final del piloto (viene de `operar-gates` Paso 5: seguir escalado / pivotar a vertical o modelo nuevo / matar).
- Fecha de kickoff y fecha de cierre (para separar días-kickoff de días-campaña-activa, ver Paso 1).
- Destinatario del postmortem (partner, y si aplica, versión resumida para el cliente final).

## Prerequisitos

- El o los gates del piloto están cerrados con veredicto explícito (`operar-gates` Paso 5 ya corrió).
- `runs/{fecha}-{NEGOCIO}.json` tiene entradas para cada etapa relevante (si falta alguna, completarla antes de escribir el postmortem: el postmortem cita esos números).
- `workspace/operacion-gates.md` con el log completo de reportes del gate.

## Archivos / cosas que toca

| Qué | Acción |
|---|---|
| `{NEGOCIO}/postmortem.md` | **Escribe** (formato canónico, Paso 1) |
| `{NEGOCIO}/workspace/checklist-cierre.md` | **Escribe** (checklist operativo, Paso 3) |
| `workspace/operacion-gates.md` | **Lee** (log de reportes, veredictos de gate) |
| `runs/{fecha}-{NEGOCIO}.json` | **Lee** (números de cada etapa citados en el postmortem) |
| Tu propia base de conocimiento (notas de proceso, memoria, docs de referencia) | **Puede escribir** en el Paso 4 (destilado), solo lo genérico reusable |

## Flujo

**Paso 1 [LATENT]: Formato canónico del postmortem.** Usar un postmortem real ya cerrado como plantilla de estructura, con estas reglas de rigor (correcciones que suelen hacer falta sobre un primer borrador más flojo):

- **Separar días desde el kickoff vs días de campaña activa.** Un piloto de "47 días" que en realidad tuvo más días desde el kickoff pero menos con campañas activas necesita las dos cifras, no una sola que mezcla setup con ejecución.
- **Bajar la certeza estadística cuando el n es chico.** Con pocas conversiones (o cero), la redacción correcta es "señal incipiente" o "no hay evidencia suficiente", nunca "clara y consistente". El postmortem no es el lugar para sonar más seguro de lo que los números permiten.
- **No generalizar el canal desde una sola ejecución.** "No convirtió en esta ejecución" ≠ "el canal no funciona para este vertical". Si solo se probó un ángulo, una oferta o un budget en ese canal, decirlo explícito como límite del hallazgo.
- **Sacar del veredicto cualquier hipótesis de presupuesto si el presupuesto alcanzó para concluir.** Si el gate llegó al 90%+ del budget planeado y el resultado fue claro (0 conversiones sobre volumen suficiente), no diluir la conclusión con "capaz con más plata hubiera funcionado" salvo que haya evidencia real de eso.
- **Sección "Qué NO se probó."** Explícita, no implícita: ángulos, ofertas, canales o segmentos que quedaron afuera del piloto y por qué. Evita que alguien lea el postmortem y asuma que se agotó todo el espacio de hipótesis.
- **Sección "Colas abiertas con dueño."** Todo pendiente que quedó sin cerrar al momento del postmortem (llamada de validación pendiente, credencial sin rotar, decisión pateada) con quién la tiene que resolver y cuándo, no solo "pendiente".
- **Inventario de assets reutilizables.** Landing, copy, creativos, audiencias resueltas, tracking armado: qué de todo eso sirve para el próximo piloto sin reescribir de cero (ver también Paso 4).

**Paso 2 [LATENT]: Revisión con lentes distintas antes de mandarlo.** Antes de compartir el postmortem con el partner, pasarlo por una revisión de 2-4 lentes: Rigor/Riesgo, Destinatario/partner, Pragmático/qué falta, y una lente de continuidad operativa. En un cierre real, esta revisión detectó un hueco genuino (faltaba llamar al cliente final antes de cerrar la narrativa del piloto) que no había salido en el primer borrador. Tratar ese tipo de hallazgo como bloqueante antes de mandar, no como nice-to-have.

**Paso 3 [DET]: Checklist de cierre operativo.** Ningún piloto queda "cerrado" sin este checklist en verde:
- **Pausar TODO el gasto residual**, incluso lo que parece marginal (un retargeting de bajo monto diario, automations de un ESP que siguen corriendo). Un piloto "cerrado" que sigue gastando algunos dólares por día indefinidamente no está cerrado.
- **Apagar bots/daemons del funnel** (chatbots, routers, automatizaciones que responden en nombre del negocio). Si el bot tenía un fallback a "funnel por default", confirmar que apagarlo no rompe otros funnels que comparten el mismo router.
- **Desactivar las tareas programadas** del piloto (reporte periódico, triage de respuestas). No dejarlas corriendo "por si acaso": una tarea programada de un piloto cerrado reporta sobre nada y confunde.
- **Rotar credenciales compartidas** que circularon durante el piloto (API keys, tokens, accesos que vio el partner o terceros). Si alguna quedó pendiente de rotar durante la operación, este es el punto de no-retorno para hacerlo.
- **Archivar el workspace viejo** (versiones descartadas, workspace v1 si hubo un v2, backups de reportes) a una subcarpeta `archive/` interna del proyecto, no a un archivo global si el proyecto entero sigue vivo por otras razones.
- **Completar `runs/` del skill con los veredictos finales.** Si alguna etapa quedó con `gate_superado` sin resolver o notas incompletas, cerrarla acá.

**Paso 4 [LATENT]: Destilado a destinos.** Cada aprendizaje del postmortem va a UN destino, no a todos por las dudas:
- **Al propio playbook**: si el aprendizaje es de proceso (cómo operar un gate, cómo comunicarse con un partner, un gotcha de una plataforma que se va a repetir), va como patch a la child skill correspondiente o, si es nuevo, a un child skill nuevo. No lo dejes solo en el postmortem: un aprendizaje que vive solo en un postmortem de un proyecto cerrado no le sirve al próximo piloto.
- **A tus docs de referencia estables**: si el aprendizaje es genérico y estable (un framework, un gotcha de una API que cualquier piloto futuro va a pisar), va a los `roles/` de paid media o a un doc de referencia propio.
- **A tu memoria de proceso**: si es un dato operativo puntual con vida útil media (un gotcha de una herramienta externa, un patrón de comportamiento de una plataforma) que no amerita reescribir un skill entero.
- **Al próximo piloto directamente**: el inventario de assets reutilizables (Paso 1) no es un aprendizaje abstracto, es un asset concreto (landing, copy, tracking armado). Documentarlo donde el próximo piloto lo vaya a buscar (ej. este mismo playbook cita el piloto anterior como prior art).

## Output esperado

`postmortem.md` completo (formato Paso 1, ya pasado por la revisión del Paso 2) + `workspace/checklist-cierre.md` con el checklist del Paso 3 marcado ítem por ítem + el mapa de destilado del Paso 4 (qué aprendizaje fue a dónde, para que quede trazable).

## Success metrics

- El postmortem no tiene ninguna afirmación de certeza ("claro", "consistente") sin un n que la sostenga.
- Las secciones "Qué NO se probó" y "Colas abiertas con dueño" existen y tienen contenido real, no están vacías por omisión.
- El checklist de cierre operativo está 100% marcado (o cada ítem pendiente tiene un dueño y fecha).
- Cada aprendizaje del postmortem tiene un destino único asignado (0 aprendizajes que quedan solo en el postmortem sin destilar).
- La revisión con lentes distintas corrió antes de mandar el postmortem al partner (no después).

## Troubleshooting

- **El postmortem suena a fracaso total cuando en realidad el piloto validó algo parcial**: separar el veredicto de negocio (paid funcionó / no funcionó para este caso) del aprendizaje de proceso (qué del sistema quedó reusable). Un piloto puede "fallar" comercialmente y aun así dejar un playbook mejor.
- **El usuario quiere mandar el postmortem ya, sin revisión**: la revisión toma minutos y en un cierre real encontró un hueco genuino (falta de llamada de cierre al cliente). Ofrecer la versión corta (1-2 lentes) si el tiempo apremia, pero no saltarla del todo.
- **El checklist de cierre tiene un ítem que no se puede resolver ahora** (ej. el partner tiene que confirmar algo): dejarlo como "cola abierta con dueño" en el postmortem (Paso 1), no como ítem tildado a medias en el checklist.
- **No queda claro si un aprendizaje es de negocio o de proceso**: si el próximo piloto (de cualquier vertical) lo necesitaría igual, es de proceso → playbook/docs de referencia/memoria. Si es específico de este negocio/partner, se queda en el proyecto cerrado.
