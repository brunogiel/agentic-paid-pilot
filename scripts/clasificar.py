#!/usr/bin/env python3
"""
Clasifica una lista de items con jev: una llamada por item, respuesta tipada.

Es el acelerador OPCIONAL de los pasos de volumen del research (Etapa 1). Sin
key de typesafe sale con codigo 2 y el paso sigue por su camino default.

Uso:
    python3 clasificar.py --items ads.jsonl --pack preguntas/ads.json \\
        --var SERVICIO="servicios de contabilidad para negocios" \\
        --salida clasificacion-ads.csv --dry-run

    # sin --dry-run, corre de verdad. El cache hace que repetir sea gratis.

Formato de --items (jsonl, una linea por item):
    {"id": "ad-12", "state": "texto del ad"}
    {"id": "kw-3",  "state": {"keyword": "bookkeeper near me", "volumen": 320}}

El 'state' puede ser texto o un objeto con campos nombrados (mejor cuando el
contexto tiene varias partes). El 'id' tiene que ser unico y estable: es la
clave del cache y la que usa el paso siguiente para cruzar.

Codigos de salida:
    0  ok
    2  no hay key de typesafe → el paso sigue por su camino default
    1  error de verdad (items ilegibles, pack roto)
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev_client as jev  # noqa: E402


def leer_items(path, limite=None):
    items = []
    vistos = set()
    for n, linea in enumerate(Path(path).open(encoding="utf-8"), 1):
        linea = linea.strip()
        if not linea:
            continue
        try:
            it = json.loads(linea)
        except json.JSONDecodeError as e:
            sys.exit(f"{path}:{n}: no es JSON valido ({e})")
        if "id" not in it or "state" not in it:
            sys.exit(f"{path}:{n}: falta 'id' o 'state'")
        it["id"] = str(it["id"])
        if it["id"] in vistos:
            sys.exit(f"{path}:{n}: id repetido '{it['id']}'. Los ids tienen que ser unicos.")
        vistos.add(it["id"])
        items.append(it)
        if limite and len(items) >= limite:
            break
    if not items:
        sys.exit(f"{path}: no hay items")
    return items


def parse_vars(pares):
    out = {}
    for p in pares or []:
        if "=" not in p:
            sys.exit(f"--var mal formada: '{p}'. Va NOMBRE=valor")
        k, v = p.split("=", 1)
        out[k.strip()] = v
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Clasifica items con jev (opcional; sin key sale con codigo 2)."
    )
    ap.add_argument("--items", required=True, help="jsonl con {id, state} por linea")
    ap.add_argument("--pack", required=True, help="pack de preguntas (scripts/preguntas/*.json)")
    ap.add_argument("--salida", required=True, help="CSV de salida")
    ap.add_argument("--var", action="append", metavar="NOMBRE=valor",
                    help="variable del piloto que el pack pide (repetible)")
    ap.add_argument("--cache", help="jsonl de respuestas (default: al lado del CSV)")
    ap.add_argument("--limit", type=int, help="procesar solo los primeros N")
    ap.add_argument("--dry-run", action="store_true", help="no llama a la API")
    ap.add_argument("--rehacer", action="store_true", help="ignora el cache")
    args = ap.parse_args()

    items = leer_items(args.items, args.limit)
    try:
        pack, preguntas = jev.cargar_pack(args.pack, parse_vars(args.var))
    except (ValueError, json.JSONDecodeError) as e:
        sys.exit(str(e))

    salida = Path(args.salida)
    cache_path = Path(args.cache) if args.cache else salida.with_suffix(".respuestas.jsonl")

    print(f"Items: {len(items)} · pack: {Path(args.pack).name} "
          f"({len(preguntas)} preguntas) · modelo: {jev.MODELO}")

    tokens, usd = jev.costo_estimado(items, preguntas)
    if args.dry_run:
        print("\n--- request de ejemplo (truncado) ---")
        print(json.dumps(
            {"model": jev.MODELO, "state": items[0]["state"], "questions": preguntas},
            ensure_ascii=False, indent=2,
        )[:2600])
        print(f"\n~{tokens:,.0f} tokens de entrada · USD {usd:.4f} a precio de lista")
        print("(estimado: el precio de salida no esta publicado. Sin --dry-run se mide el real.)")
        return 0

    key = jev.leer_key()
    if not key:
        print(f"⚠ {jev.MENSAJE_SIN_KEY}", file=sys.stderr)
        return 2

    print(f"Estimado: ~{tokens:,.0f} tokens in · USD {usd:.4f}")
    respuestas, fallos = jev.correr(items, preguntas, key, cache_path, args.rehacer)

    cols = ["id"] + jev.columnas_de(preguntas)
    filas, tin, tout = [], 0, 0
    for it in items:
        a = respuestas.get(it["id"])
        if not a:
            continue
        tin += a.get("_in", 0)
        tout += a.get("_out", 0)
        filas.append({c: a.get(c, "") if c != "id" else it["id"] for c in cols})

    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(filas)

    print(f"\nSalida: {salida}  ({len(filas)} de {len(items)} items)")
    print(f"Gasto real: {tin:,} tokens in / {tout:,} out · "
          f"USD {tin * jev.USD_POR_TOKEN_IN:.4f} de entrada")
    if fallos:
        print(f"\n⚠ {len(fallos)} sin respuesta (quedaron afuera del CSV):", file=sys.stderr)
        for i, e in fallos[:10]:
            print(f"  {i}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
