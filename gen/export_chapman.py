# -*- coding: utf-8 -*-
"""Chapman-Shaoxing/Ningbo → Spieldaten.

Diese Datenbank hat **keine** Wellen-Annotation, nur Diagnosen. Deshalb werden
ihre Aufnahmen mit `messbar: false` ausgegeben: man darf sie ansehen,
vergleichen und befunden, aber der Zirkel misst nur dort, wo ein Kardiologe die
Grenzen gesetzt hat (LUDB).

Ausgabe
-------
`data/chapman/<id>.json`  — je Aufnahme, 12 Ableitungen, 250 Hz, int16 in µV,
                            base64. Rund 80 kB je Datei.
`data/chapman_index.json` — Diagnosen, Alter, Geschlecht, Dateiname. Klein
                            genug fürs Repository.

Die Signaldateien kommen **nicht** ins Repository: sie sind abgeleitet und mit
diesem Skript jederzeit neu zu erzeugen.
"""
import base64
import json
import os
import sys

import numpy as np
import wfdb

QUELLE = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/daten/chapman"
ZIEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bau", "chapman")
ZIEL_FS = 250
ABLEITUNGEN = ["i", "ii", "iii", "avr", "avl", "avf", "v1", "v2", "v3", "v4", "v5", "v6"]

NAME = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "snomed.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "snomed.json")) else {}


def packe(sig_mv):
    """12 × N Werte in mV → base64 von int16 in µV. Verlustarm und kompakt."""
    mikrovolt = np.clip(np.nan_to_num(sig_mv) * 1000.0, -32000, 32000).astype("<i2")
    return base64.b64encode(mikrovolt.tobytes()).decode("ascii")


def eine(pfad):
    r = wfdb.rdrecord(pfad)
    leads = [s.lower().replace("avr", "avr") for s in r.sig_name]
    reihenfolge = []
    for a in ABLEITUNGEN:
        reihenfolge.append(leads.index(a) if a in leads else None)
    if any(i is None for i in reihenfolge):
        return None
    schritt = max(1, int(round(r.fs / ZIEL_FS)))
    sig = r.p_signal[::schritt, :][:, reihenfolge]            # N × 12
    kopf = {"alter": None, "sex": None, "dx": []}
    for k in (r.comments or []):
        k = k.strip()
        if k.lower().startswith("age:"):
            try: kopf["alter"] = int(k.split(":", 1)[1])
            except Exception: pass
        elif k.lower().startswith("sex:"):
            kopf["sex"] = k.split(":", 1)[1].strip()
        elif k.lower().startswith("dx:"):
            kopf["dx"] = [c.strip() for c in k.split(":", 1)[1].split(",") if c.strip()]
    return {
        "id": os.path.basename(pfad), "quelle": "chapman", "messbar": False,
        "fs": r.fs / schritt, "leads": ABLEITUNGEN, "n": int(sig.shape[0]),
        "alter": kopf["alter"], "sex": kopf["sex"], "dx": kopf["dx"],
        "dx_namen": [NAME.get(c, c) for c in kopf["dx"]],
        "sig": packe(sig.T),                                   # 12 × N, lead-weise
    }


if __name__ == "__main__":
    os.makedirs(ZIEL, exist_ok=True)
    pfade = []
    for wurzel, _, dateien in os.walk(os.path.join(QUELLE, "WFDBRecords")):
        for d in sorted(dateien):
            if d.endswith(".mat"):
                pfade.append(os.path.join(wurzel, d)[:-4])
    index, fehler = [], 0
    for i, p in enumerate(sorted(pfade)):
        try:
            r = eine(p)
        except Exception:
            fehler += 1
            continue
        if not r:
            fehler += 1
            continue
        with open(os.path.join(ZIEL, r["id"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, separators=(",", ":"))
        index.append({k: r[k] for k in ("id", "alter", "sex", "dx", "dx_namen")})
        if (i + 1) % 300 == 0:
            print(f"  {i+1}/{len(pfade)} …")
    with open(os.path.join(os.path.dirname(ZIEL), "chapman_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    groesse = sum(os.path.getsize(os.path.join(ZIEL, d)) for d in os.listdir(ZIEL))
    print(f"{len(index)} Aufnahmen geschrieben, {fehler} übersprungen, {groesse/1e6:.0f} MB")
