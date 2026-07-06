# `lanzar-piloto` — playbook de adquisición pagada

Kit de skills para validar un negocio/vertical nuevo con un **piloto de adquisición pagada**: un orquestador thin (`SKILL.md`) + 13 child skills, una por sub-etapa. El proceso es siempre el mismo (**0.plan → 1.research → 2.experimento → 3.ejecución**), con un gate de budget que permite cortar antes de gastar todo.

## Por qué este kit (y no otro prompt de agencia)

El kit tiene un punto de vista sobre **dónde se gana o se pierde un piloto**. El orden de las palancas, de la que más mueve la aguja a la que menos:

1. **¿El mercado responde a la oferta?** Es lo único que el piloto realmente testea. Si no, nada de lo de abajo importa.
2. **Canal** (a dónde va el budget). La decisión más cara; se pelea antes de repartir la plata, no después.
3. **Oferta / posicionamiento** (ángulo, anchor de precio).
4. **Claridad de la landing.** Clara + con prueba le gana a "linda".
5. **Higiene de keywords / negativas.** Plata real, pero es un impuesto de eficiencia (~10-20%), no un multiplicador 2-5x.

Y una distinción que ordena el gasto: **matrícula vs impuesto evitable**. La *matrícula* es la plata en lo que no podías saber de antemano (el precio del experimento, se paga sí o sí). El *impuesto evitable* son los clics en basura que cualquier operador neguea el día cero (jobs / salary / free / course / how-to). La matrícula se paga; el impuesto se evita con la lista de negativas del día cero.

## Cómo se usa

Es un kit para tu asistente de IA (Claude Code, Cursor, ChatGPT). Copiá/pegá (o apuntá) el orquestador o la skill que necesites y arrancá:

- **End-to-end:** invocá `lanzar-piloto` ("lancemos un piloto para X"). El orquestador hace el kickoff, scaffoldea el proyecto y encadena las etapas con checkpoints (te pide OK en cada parada).
- **Suelto:** cada child skill se puede correr sola ("hacé el swipe de ads de competidores de X", "modelá el funnel CAC/LTV de Y").

## Glosario rápido

- **Orquestador thin:** el `SKILL.md` raíz. Solo coordina y gatea; no hace el trabajo, lo delegan las child skills.
- **Child skill:** cada `s*/SKILL.md`, una sub-etapa con su propia lógica (research, copy, tracking, etc.).
- **Gate de budget:** un checkpoint donde se enciende solo una parte del budget (ej. la primera tanda) y el resto queda apagado hasta que los números dan OK. Permite cortar antes de gastar todo.
- **Backbone (`templates/_backbone.md`):** el contrato de invariantes (marca, oferta, segmentos, budget) que los entregables de ejecución respetan sin re-derivar.
- **`[LATENT]` / `[DET]` / `[FANOUT]`:** etiquetas de tipo de paso — razonamiento del modelo / paso determinístico (mecánico) / fan-out a subagentes en paralelo.

## Las 4 etapas (+ operar)

```
0 · PLAN        s0-plan-piloto
1 · RESEARCH    s1a-research-mercado · s1b-kw-research-google
                s1c-swipe-ads-competidores · s1d-sizing-audiencias-meta
2 · EXPERIMENTO s2a-modelar-funnel · s2b-disenar-experimento
3 · EJECUCIÓN   s3a-copy-landings · s3b-build-landings · s3c-spec-campanias
                s3d-creativos-ads · s3e-setup-tracking · s3f-pre-launch-validation
4 · OPERAR      (punteros a roles/: search-query-analyst + campaign-auditor)
```

Cada etapa produce su doc en el proyecto: `0.plan.md`, `1.research.md`, `2.plan-piloto.md`, `3.ejecucion-piloto.md`, + `workspace/`. Hay un ejemplo ilustrativo de un `1.research.md` completo en `ejemplo/`.

## Piezas del kit

| Carpeta | Qué hay |
|---|---|
| `SKILL.md` | el orquestador (conductor thin, gateado) |
| `templates/` | skeletons reusables de los 4 docs de etapa + `_backbone.md` |
| `roles/` | los 6 roles de paid media (google ads, meta ads, creative, search query analyst, campaign auditor, tracking) que las etapas de ejecución y operación invocan |
| `ejemplo/` | una corrida ilustrativa (`1.research.md` de un vertical hipotético) |
| `s*/` | las 13 child skills (cada una con su `SKILL.md`, algunas con `scripts/`) |

## Doctrina

Thin harness / fat skills: el orquestador solo coordina, gatea y guía; el trabajo vive en las child skills. Skills como method-call (parametrizadas, sin valores hardcodeados), pasos marcados `[LATENT]/[DET]/[FANOUT]`, scripts en `scripts/` (no embebidos), success metrics por skill.

## Créditos

Los 6 roles de `roles/` son una adaptación al español/LATAM de un proyecto con licencia MIT. Ver [`NOTICE.md`](NOTICE.md).
