#!/usr/bin/env python3
"""Saca tamaños de audiencia de Meta (estimate_mau) vía delivery_estimate.
delivery_estimate es un cálculo puro: NO crea nada ni gasta nada (read-only),
así que sirve cualquier ad account con token (idealmente uno en USD para que el
costo, si aplica, vuelva en USD).

Genérico / config-driven (playbook lanzar-piloto). Toda la parte específica del
piloto (cuenta, geo, intereses, verticales, edades) vive en un JSON de config:

  {
    "account": "act_XXXXXXXXXXXX",   // o env META_ACCT
    "api_version": "v21.0",
    "locale_slice": 1002,             // opcional: locale id para calcular el % de un idioma
    "rows": [
      {"label": "N1 Owners ciudad 28-55",
       "targeting_spec": {"geo_locations": {...}, "behaviors": [{"id":"..."}], "age_min":28, "age_max":55}},
      {"label": "Vertical ejemplo",
       "targeting_spec": {"geo_locations": {...}, "flexible_spec": [{...},{...}], "age_min":25,"age_max":60}}
    ]
  }

Cada row es un targeting_spec completo (sin locales). El % del idioma se calcula
re-corriendo el mismo spec con locales=[locale_slice].

Uso: python3 harvest_audiences.py [audiences.json]
"""
import json, os, sys, time, urllib.parse, urllib.request

CFG = sys.argv[1] if len(sys.argv) > 1 else "audiences.json"
cfg = json.load(open(CFG))

API = f"https://graph.facebook.com/{cfg.get('api_version', 'v21.0')}"
ACCT = os.environ.get("META_ACCT") or cfg.get("account")
if not ACCT or "XXXX" in ACCT:
    raise SystemExit("Falta la ad account: seteá META_ACCT o 'account' en el config (act_...).")
LOCALE = cfg.get("locale_slice")

def token():
    p = os.path.expanduser("~/.config/meta/.env")
    for line in open(p):
        line = line.strip()
        if line.startswith("ACCESS_TOKEN"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no ACCESS_TOKEN in ~/.config/meta/.env")

TOKEN = token()

def estimate(spec):
    q = urllib.parse.urlencode({
        "optimization_goal": "REACH",
        "targeting_spec": json.dumps(spec),
        "access_token": TOKEN,
    })
    url = f"{API}/{ACCT}/delivery_estimate?{q}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            d = json.load(r)["data"][0]
        return d["estimate_mau_lower_bound"], d["estimate_mau_upper_bound"], d["estimate_ready"]
    except Exception as e:
        return None, None, str(e)[:60]

def row(label, spec):
    lo, hi, ok = estimate(spec)
    if lo is None:
        return f"{label:<34} ERROR {ok}"
    fmt = lambda a, b: f"{a:,}-{b:,}"
    if LOCALE:
        es_lo, es_hi, _ = estimate({**spec, "locales": [LOCALE]})
        time.sleep(0.25)
        share = (es_lo / lo * 100) if lo else 0
        return f"{label:<34} {fmt(lo,hi):>21} | slice {fmt(es_lo,es_hi):>21} | ~{share:4.0f}%"
    time.sleep(0.25)
    return f"{label:<34} {fmt(lo,hi):>21}"

print(f"# Meta audience sizes (estimate_mau) — acct {ACCT} — {cfg.get('api_version','v21.0')}\n")
hdr = "[total | slice idioma | %]" if LOCALE else "[total]"
print(f"{'audiencia':<34} {hdr}")
print("-" * 70)
for r in cfg.get("rows", []):
    print(row(r["label"], r["targeting_spec"]))
