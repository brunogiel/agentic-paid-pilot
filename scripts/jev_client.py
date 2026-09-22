#!/usr/bin/env python3
"""
Cliente de jev (typesafe.ai) para el playbook lanzar-piloto.

Libreria, no CLI. El que se corre es clasificar.py.

Aca no hay nada especifico de un rubro: las preguntas entran por archivo
(scripts/preguntas/*.json) y las variables del piloto por linea de comandos.

La API key NO va en el repo ni en ningun archivo del proyecto.
    export TYPESAFE_API_KEY="tsk_..."
    # o
    mkdir -p ~/.config/typesafe && echo "tsk_..." > ~/.config/typesafe/api_key
    chmod 600 ~/.config/typesafe/api_key

jev es OPCIONAL en todo el playbook. Si falta la key, falta_key() devuelve el
motivo y el que llama sigue por el camino default de su paso (regex, o el paso
[LATENT] de siempre). Nada se rompe por no tener key.
"""

import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODELO = "jev-latest"
CONCURRENCIA = 6
REINTENTOS = 5
USD_POR_TOKEN_IN = 42 / 1e9  # USD 42 por 1.000 millones de tokens de entrada

TIPOS = ("noul", "choice", "score")


# ----------------------------------------------------------------- la key


def leer_key():
    """Devuelve la key, o None si no hay. No corta el programa."""
    k = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if k:
        return k
    f = Path.home() / ".config" / "typesafe" / "api_key"
    if f.is_file():
        k = f.read_text().strip()
        if k:
            return k
    return None


MENSAJE_SIN_KEY = (
    "sin key de typesafe: segui por el camino default de este paso.\n"
    "  jev es opcional. Para prenderlo:\n"
    "    mkdir -p ~/.config/typesafe && echo 'tsk_...' > ~/.config/typesafe/api_key\n"
    "    chmod 600 ~/.config/typesafe/api_key"
)


# ------------------------------------------------------- pack de preguntas


def cargar_pack(path, variables=None):
    """Lee un pack de scripts/preguntas/ y le mete las variables del piloto.

    Formato del pack:
        {
          "descripcion": "para que sirve",
          "variables": ["SERVICIO", "CLIENTE"],
          "preguntas": { "<id>": {"type": ..., "instructions": ..., "criteria": ...} }
        }

    En instructions y criteria, {SERVICIO} se reemplaza por su valor. Los ids de
    las preguntas son para el codigo: no se le mandan al modelo, asi que cada
    pregunta tiene que decir sola lo que quiere saber.
    """
    pack = json.loads(Path(path).read_text(encoding="utf-8"))
    preguntas = pack.get("preguntas")
    if not preguntas:
        raise ValueError(f"{path}: el pack no tiene 'preguntas'")

    variables = dict(variables or {})
    pedidas = pack.get("variables") or []
    faltan = [v for v in pedidas if v not in variables]
    if faltan:
        raise ValueError(
            f"{path}: faltan variables del piloto: {', '.join(faltan)}\n"
            f"  pasalas con --var NOMBRE=valor"
        )

    preguntas = _sustituir(preguntas, variables)
    for qid, q in preguntas.items():
        if q.get("type") not in TIPOS:
            raise ValueError(f"{path}: pregunta '{qid}' con type invalido: {q.get('type')}")
        sobrantes = _placeholders(q)
        if sobrantes:
            raise ValueError(
                f"{path}: pregunta '{qid}' quedo con {{{sobrantes[0]}}} sin resolver. "
                f"Declaralo en 'variables' del pack y pasalo con --var."
            )
    return pack, preguntas


def _sustituir(obj, variables):
    if isinstance(obj, str):
        for k, v in variables.items():
            obj = obj.replace("{" + k + "}", str(v))
        return obj
    if isinstance(obj, dict):
        return {k: _sustituir(v, variables) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sustituir(v, variables) for v in obj]
    return obj


def _placeholders(obj):
    txt = json.dumps(obj, ensure_ascii=False)
    return re.findall(r"\{([A-Z_][A-Z0-9_]*)\}", txt)


# -------------------------------------------------------------------- API


def preguntar(state, preguntas, key):
    """Una llamada con TODAS las preguntas juntas: el state se cobra una vez.

    Las preguntas corren en paralelo y no se ven entre ellas. Por eso sirven
    para cruzar: si dos respuestas de la MISMA llamada se contradicen, el pack
    esta mal escrito (ver el test de auto-contradiccion del reference).
    """
    cuerpo = json.dumps(
        {"model": MODELO, "state": state, "questions": preguntas}, ensure_ascii=False
    ).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=cuerpo,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    ultimo = None
    for intento in range(REINTENTOS):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detalle = e.read().decode("utf-8", "replace")[:300]
            ultimo = f"HTTP {e.code}: {detalle}"
            if e.code in (429, 500, 502, 503, 529):
                time.sleep((2 ** intento) + random.random())
                continue
            raise RuntimeError(ultimo) from e
        except (urllib.error.URLError, TimeoutError) as e:
            ultimo = str(e)
            time.sleep((2 ** intento) + random.random())
    raise RuntimeError(f"sin respuesta tras {REINTENTOS} intentos: {ultimo}")


def aplanar(resp):
    """De la respuesta de la API a columnas planas.

    Por pregunta deja el valor y su confianza. Ojo con la confianza: en la
    corrida de los 409 CVs NO ordeno la lista (media 0,59 en el top 30 contra
    0,51 en el resto). Sirve para dudar de un item, no para cortar una lista.
    El corte lo hace el codigo sobre dato duro.
    """
    out = {}
    for qid, a in (resp.get("answers") or {}).items():
        tipo = a.get("type")
        if tipo == "noul":
            out[f"{qid}_p"] = a.get("noul")
        elif tipo == "choice":
            out[qid] = a.get("choice")
        elif tipo == "score":
            out[qid] = a.get("score")
        out[f"{qid}_conf"] = a.get("confidence")
    u = resp.get("usage") or {}
    out["_in"] = u.get("input_tokens", 0)
    out["_out"] = u.get("output_tokens", 0)
    return out


def columnas_de(preguntas):
    """Los nombres de columna que va a devolver aplanar(), en orden del pack.

    Un noul no lleva columna de confianza: la probabilidad ES la respuesta, no
    hay una confianza aparte (por eso la API devuelve confidence vacio ahi).
    """
    cols = []
    for qid, q in preguntas.items():
        if q["type"] == "noul":
            cols.append(f"{qid}_p")
        else:
            cols += [qid, f"{qid}_conf"]
    return cols


# ------------------------------------------------------------ la corrida


def correr(items, preguntas, key, cache_path, rehacer=False, avisar=print):
    """Pregunta por cada item, una llamada cada uno, y cachea a jsonl.

    items: lista de dicts con 'id' (unico) y 'state' (string o dict).
    Devuelve (respuestas_por_id, fallos). Los fallos se reportan, no se tragan:
    un item sin respuesta queda afuera del CSV y listado al final.
    """
    cache = {}
    cache_path = Path(cache_path)
    if cache_path.is_file() and not rehacer:
        for linea in cache_path.open(encoding="utf-8"):
            try:
                fila = json.loads(linea)
                cache[fila["id"]] = fila
            except (json.JSONDecodeError, KeyError):
                pass
        if cache:
            avisar(f"Cache: {len(cache)} ya respondidos ({cache_path.name})")

    pendientes = [i for i in items if i["id"] not in cache]
    if not pendientes:
        return cache, []

    lock = Lock()
    fallos = []
    hechos = [0]
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    def trabajar(item):
        try:
            resp = preguntar(item["state"], preguntas, key)
        except Exception as e:  # noqa: BLE001 — se reporta, no se traga
            with lock:
                fallos.append((item["id"], str(e)[:140]))
            return
        fila = {"id": item["id"], **aplanar(resp)}
        with lock:
            cache[item["id"]] = fila
            with cache_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(fila, ensure_ascii=False) + "\n")
            hechos[0] += 1
            if hechos[0] % 25 == 0 or hechos[0] == len(pendientes):
                avisar(f"  {hechos[0]}/{len(pendientes)}")

    avisar(f"Consultando {len(pendientes)} de {len(items)}…")
    with ThreadPoolExecutor(max_workers=CONCURRENCIA) as ex:
        list(ex.map(trabajar, pendientes))
    return cache, fallos


def costo_estimado(items, preguntas):
    """USD de entrada a precio de lista. El de salida no esta publicado.

    Las preguntas viajan en CADA llamada, asi que suman por item. Cuando el
    state es corto (una keyword) el pack de preguntas es casi todo el costo.
    """
    pack_chars = len(json.dumps(preguntas, ensure_ascii=False))
    chars = sum(
        len(i["state"] if isinstance(i["state"], str) else json.dumps(i["state"], ensure_ascii=False))
        + pack_chars
        for i in items
    )
    tokens = chars / 4
    return tokens, tokens * USD_POR_TOKEN_IN
