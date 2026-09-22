#!/usr/bin/env python3
"""Arma un swipe file de ads de competidores y baja las creatividades (imágenes/videos).
Lee el dump crudo del Meta Ad Library (estructura anidada con snapshot/images/videos/cards),
filtra por rubro, descarga la media a ads-creatives/ (idempotente) y escribe
competitor-ads-swipe.md con copy + CTA + links a los archivos locales.

Genérico / parametrizado (playbook lanzar-piloto). Lo específico del rubro viene por env:
  SWIPE_RELEVANT  regex de términos del rubro que SÍ importan   (requerido)
  SWIPE_NOISE     regex de ruido a descartar                    (opcional)
  SWIPE_TERMS     label de los términos buscados (para el header) (opcional)
  SWIPE_DATE      fecha de captura para el header (YYYY-MM-DD)   (opcional, default hoy)

Uso: SWIPE_RELEVANT="bookkeep|contab|tax" python3 build_swipe.py [ad-library-raw.json]

--- Camino opcional con jev (typesafe.ai) -------------------------------------
La regex no distingue "curso de contabilidad" de "servicio de contabilidad", así
que deja pasar cursos, avisos de empleo y software como si fueran competencia.
Con una key de typesafe se puede agregar un segundo corte, por ad, que sí lo
distingue. Las dos variables de abajo son OPCIONALES: sin ellas este script se
comporta exactamente como antes.

  SWIPE_EMITIR_ITEMS=items.jsonl   Pasada 1: escribe {id, state} por ad que pasó
                                   la regex y termina. No baja media ni escribe el
                                   swipe. Ese jsonl es el input de clasificar.py.
  SWIPE_CLASIFICACION=clasif.csv   Pasada 2: el CSV que devolvió clasificar.py.
                                   Descarta los ads que jev marcó como no-competencia
                                   y, si el CSV trae la columna `angulo`, agrega al
                                   swipe la tabla de gap de mensaje.
  SWIPE_UMBRAL=0.5                 Probabilidad mínima de es_competidor_p (opcional).

Las 3 pasadas:
  SWIPE_RELEVANT=... SWIPE_EMITIR_ITEMS=items.jsonl python3 build_swipe.py raw.json
  python3 ../../scripts/clasificar.py --items items.jsonl \\
      --pack ../../scripts/preguntas/ads.json --var SERVICIO="..." --var CLIENTE="..." \\
      --salida clasif.csv
  SWIPE_RELEVANT=... SWIPE_CLASIFICACION=clasif.csv python3 build_swipe.py raw.json
"""
import csv, datetime, json, os, re, sys, urllib.request

SRC = sys.argv[1] if len(sys.argv) > 1 else "ad-library-raw.json"
OUTDIR = "ads-creatives"
MD = "competitor-ads-swipe.md"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

_relevant = os.environ.get("SWIPE_RELEVANT")
if not _relevant:
    raise SystemExit("Falta SWIPE_RELEVANT (regex de términos del rubro). "
                     'Ej: SWIPE_RELEVANT="bookkeep|account|contab|tax|financ"')
RELEVANT = re.compile(_relevant, re.I)
NOISE = re.compile(os.environ.get("SWIPE_NOISE") or r"(?!x)x", re.I)  # default: matchea nada
TERMS = os.environ.get("SWIPE_TERMS", "(términos del rubro)")
DATE = os.environ.get("SWIPE_DATE") or datetime.date.today().isoformat()

# Camino opcional con jev. Sin estas env vars, todo lo de abajo es no-op.
EMITIR = os.environ.get("SWIPE_EMITIR_ITEMS")
CLASIF_PATH = os.environ.get("SWIPE_CLASIFICACION")
UMBRAL = float(os.environ.get("SWIPE_UMBRAL") or 0.5)
CLASIF = {}
if CLASIF_PATH:
    with open(CLASIF_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            CLASIF[str(row["id"])] = row
    if not CLASIF:
        raise SystemExit(f"{CLASIF_PATH}: no tiene filas. Corré clasificar.py primero.")
    print(f"Clasificación de jev: {len(CLASIF)} ads · umbral es_competidor_p ≥ {UMBRAL}",
          file=sys.stderr)


def descartado_por_jev(ad_id):
    """(descartar, motivo). Un ad sin fila en el CSV se conserva: no se pierde nada
    por una respuesta que falló. El que queda afuera es el que jev juzgó y rechazó."""
    row = CLASIF.get(str(ad_id))
    if not row:
        return False, ""
    try:
        p = float(row.get("es_competidor_p") or 0)
    except ValueError:
        return False, ""
    if p >= UMBRAL:
        return False, ""
    return True, (row.get("a_quien_le_habla") or f"es_competidor_p={p:.2f}")

# Set de palabras frecuentes en español para detectar idioma del ad (genérico, reusable).
ES_WORDS = set("que para los las con una por como tu su negocio negocios dueño gratis ayuda hoy más "
               "también nuestro nuestros servicios español conoces sabes apoyar enfocamos especializamos "
               "firma profesional clase impuestos contabilidad".split())

def clean(s):
    return re.sub(r"[ \t]+", " ", (s or "").replace("\r", "")).strip()

def celda(s):
    """Texto seguro para una celda de tabla markdown: sin saltos ni pipes crudos."""
    return re.sub(r"\s+", " ", (s or "").replace("|", "\\|")).strip()

def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:40]

def lang(s):
    return "ES" if len(set(re.findall(r"[a-záéíóúñ]+", s.lower())) & ES_WORDS) >= 2 else "EN"

def listdict(v):
    return [x for x in (v if isinstance(v, list) else [v]) if isinstance(x, dict)]

def download(url, dest):
    if os.path.exists(dest):
        return "skip"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=40) as r, open(dest, "wb") as f:
            f.write(r.read())
        return "ok"
    except Exception as e:
        return f"FAIL {str(e)[:40]}"

items = json.load(open(SRC))
os.makedirs(OUTDIR, exist_ok=True)

ads, seen, counts = [], set(), {}
emitidos, descartes_jev = [], []
for it in items:
    snap = it.get("snapshot") or {}
    pn = it.get("page_name") or snap.get("page_name") or "?"
    body = clean((snap.get("body") or {}).get("text") if isinstance(snap.get("body"), dict) else snap.get("body"))
    title = clean(snap.get("title"))
    blob = f"{pn} {title} {body}"
    if NOISE.search(blob) or not RELEVANT.search(blob):
        continue
    key = (pn, body[:60])
    if key in seen:
        continue
    seen.add(key)

    ad_id = str(it.get("ad_archive_id") or it.get("ad_id") or f"{pn}-{len(seen)}")
    if EMITIR:
        emitidos.append({"id": ad_id, "state": {
            "anunciante": pn, "titulo": title, "copy": body,
            "cta": clean(snap.get("cta_text")),
            "descripcion_del_link": clean(snap.get("link_description")),
        }})
        continue
    fuera, motivo = descartado_por_jev(ad_id)
    if fuera:
        descartes_jev.append((pn, title or body[:60], motivo))
        continue

    counts[pn] = counts.get(pn, 0) + 1
    sl = slug(pn) + (f"-{counts[pn]}" if counts[pn] > 1 else "")

    img_urls, vid_urls = [], []
    for im in listdict(snap.get("images")):
        if im.get("original_image_url"): img_urls.append(im["original_image_url"])
    for c in listdict(snap.get("cards")):
        if c.get("original_image_url"): img_urls.append(c["original_image_url"])
        if c.get("video_sd_url"): vid_urls.append(c["video_sd_url"])
    for v in listdict(snap.get("videos")):
        if v.get("video_sd_url"): vid_urls.append(v["video_sd_url"])
        elif v.get("video_hd_url"): vid_urls.append(v["video_hd_url"])
    img_urls = list(dict.fromkeys(img_urls))
    vid_urls = list(dict.fromkeys(vid_urls))

    local = []
    addir = os.path.join(OUTDIR, sl)
    if img_urls or vid_urls:
        os.makedirs(addir, exist_ok=True)
    for i, u in enumerate(img_urls, 1):
        dest = os.path.join(addir, f"img-{i}.jpg")
        st = download(u, dest); print(f"[{st}] {dest}", file=sys.stderr)
        if st in ("ok", "skip"): local.append(("imagen", f"{OUTDIR}/{sl}/img-{i}.jpg"))
    for i, u in enumerate(vid_urls, 1):
        dest = os.path.join(addir, f"video-{i}.mp4")
        st = download(u, dest); print(f"[{st}] {dest}", file=sys.stderr)
        if st in ("ok", "skip"): local.append(("video", f"{OUTDIR}/{sl}/video-{i}.mp4"))

    ads.append({
        "id": ad_id,
        "page": pn, "lang": lang(blob), "title": title, "body": body,
        "cta": clean(snap.get("cta_text")), "dest": snap.get("link_url") or "",
        "lib": it.get("ad_library_url") or "", "start": (it.get("start_date_formatted") or "")[:10],
        "active": it.get("is_active"),
        "plat": ", ".join(it.get("publisher_platform")) if isinstance(it.get("publisher_platform"), list) else (it.get("publisher_platform") or ""),
        "local": local,
    })

if EMITIR:
    with open(EMITIR, "w", encoding="utf-8") as f:
        for e in emitidos:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"OK: {len(emitidos)} ads (los que pasó la regex) -> {EMITIR}\n"
          f"Ahora pasalos por clasificar.py y volvé a correr con SWIPE_CLASIFICACION.")
    raise SystemExit(0)

ads.sort(key=lambda a: (a["lang"] != "ES", a["page"]))

out = []
out.append("# Swipe file — anuncios de competidores (Meta Ad Library)\n")
out.append(f"> Capturado el {DATE} vía Apify sobre el Meta Ad Library (términos: {TERMS}).")
out.append("> Copy + creatividades reales que los competidores tienen corriendo. Las imágenes/videos están en `ads-creatives/` (videos en SD). El link \"Ver en Ad Library\" muestra el ad en vivo mientras siga activo.")
out.append("> Limitación: el Ad Library no muestra a quién targetean ni cuánto gastan.")
out.append(f"> {len(ads)} ads relevantes (filtrado el ruido que matcheaba por palabra suelta).\n")
if descartes_jev:
    out.append(f"> Segundo corte con jev: **{len(descartes_jev)} ads que la regex había dejado pasar "
               f"no son competencia** (cursos, avisos de empleo, software, otro rubro). "
               f"Están listados al final, para que se vea qué se descartó y por qué.\n")
out.append("---")
cur = None
for a in ads:
    if a["lang"] != cur:
        cur = a["lang"]
        out.append(f"\n## {'En español' if cur=='ES' else 'En inglés'}\n")
    out.append(f"### {a['page']}")
    meta = " · ".join(x for x in [a["plat"] or None, "activo" if a["active"] else None, ("desde " + a["start"]) if a["start"] else None] if x)
    if meta: out.append(f"*{meta}*  ")
    if a["title"]: out.append(f"**Título:** {a['title']}  ")
    if a["body"]: out.append("**Copy:**\n> " + a["body"].replace("\n", "\n> ") + "  ")
    if a["cta"]: out.append(f"**CTA:** {a['cta']}  ")
    if a["dest"]: out.append(f"**Destino:** {a['dest']}  ")
    if a["local"]:
        out.append("**Creatividad (archivos locales):** " + " · ".join(f"[{t}]({p})" for t, p in a["local"]) + "  ")
    if a["lib"]: out.append(f"**[Ver en Ad Library]({a['lib']})**  ")
    out.append("")

# --- Gap de mensaje: se cuenta, no se opina (solo con la clasificación de jev) ---
if CLASIF:
    angulos = {}
    for a in ads:
        ang = (CLASIF.get(a["id"], {}).get("angulo") or "").strip()
        if ang:
            angulos.setdefault(ang, []).append(a["page"])
    if angulos:
        # El universo de ángulos posibles sale del pack de preguntas, no de lo observado:
        # un ángulo con 0 ads es justamente el hallazgo, y si no está en la lista no se ve.
        pack = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "..", "scripts", "preguntas", "ads.json")
        posibles = list(angulos)
        try:
            with open(pack, encoding="utf-8") as f:
                posibles = list(json.load(f)["preguntas"]["angulo"]["criteria"])
        except Exception as e:  # noqa: BLE001 — se degrada a lo observado, no aborta
            print(f"[aviso] no pude leer los ángulos posibles de {pack}: {e}", file=sys.stderr)
        out.append("\n---\n")
        out.append("## Gap de mensaje\n")
        out.append(f"Cada ad quedó con un ángulo tipado (una llamada por ad). Esto es un **conteo "
                   f"sobre {len(ads)} ads**, no una lectura de ojo. El ángulo con 0 ads es el hueco.\n")
        out.append("| Ángulo | Ads | Quién lo usa |")
        out.append("|---|---|---|")
        for ang in sorted(posibles, key=lambda x: -len(angulos.get(x, []))):
            usan = angulos.get(ang, [])
            quien = celda(", ".join(sorted(set(usan))[:4])) if usan else "**nadie**"
            out.append(f"| {ang} | {len(usan)} | {quien} |")
        vacios = [a for a in posibles if not angulos.get(a)]
        if vacios:
            out.append(f"\n**Ángulos que nadie está usando:** {', '.join(vacios)}. "
                       f"Son los candidatos a wedge para `s3d-creativos-ads`.\n")

if descartes_jev:
    out.append("\n---\n")
    out.append("## Descartados por el segundo corte\n")
    out.append("La regex los dejó pasar por matchear una palabra del rubro. No son competencia.\n")
    out.append("| Anunciante | Ad | Le habla a |")
    out.append("|---|---|---|")
    for pn, que, motivo in descartes_jev:
        out.append(f"| {celda(pn)} | {celda(que[:60])} | {celda(motivo)} |")
    out.append("")

open(MD, "w").write("\n".join(out))
n_files = sum(len(a["local"]) for a in ads)
print(f"\nOK: {len(ads)} ads, {n_files} archivos de creatividad enlazados. Swipe -> {MD}")
if descartes_jev:
    print(f"   ({len(descartes_jev)} descartados por jev, listados al final del swipe)")
