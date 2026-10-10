# -*- coding: utf-8 -*-
"""Spieldaten aus der LUDB: Signal plus Lage jeder einzelnen Welle.

Der Unterschied zur ersten Fassung: Für jeden Schlag im ausgegebenen Fenster
stehen die Grenzen der Experten-Annotation drin (P-Beginn, P-Ende, QRS-Beginn,
R-Gipfel, QRS-Ende, T-Ende, in Sekunden ab Fensteranfang). Damit kann das
Zirkel-Rätsel nicht nur prüfen, *wie breit* gemessen wurde, sondern auch *wo* —
und bei einer Fehlmessung genau sagen, wo die Welle wirklich anfängt.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

import ekg as E

WURZEL = "/home/claude/daten/ludb/lobachevsky-university-electrocardiography-database-1.0.1/data"
LEAD = "ii"
ZIEL_FS = 250
FENSTER = 10.0


def schlaege(datensatz, lead=LEAD, von_s=0.0, dauer_s=FENSTER):
    """Welle für Welle: Grenzen in Sekunden ab Fensteranfang."""
    ann = datensatz["ann"].get(lead)
    if not ann:
        return []
    fs = datensatz["fs"]
    a, b = von_s * fs, (von_s + dauer_s) * fs
    w = [x for x in E._wellen(ann) if a <= x[1] and x[3] <= b]
    qrs = [x for x in w if x[0] == "N"]
    ps = [x for x in w if x[0] == "p"]
    ts = [x for x in w if x[0] == "t"]
    sek = lambda n: round((n - a) / fs, 4)
    aus = []
    for q in qrs:
        vor = [p for p in ps if p[3] <= q[1] and q[1] - p[3] < 0.32 * fs]
        nach = [t for t in ts if t[1] >= q[3] and t[1] - q[3] < 0.5 * fs]
        s = {"q0": sek(q[1]), "r": sek(q[2]), "q1": sek(q[3])}
        if vor:
            s["p0"], s["pg"], s["p1"] = sek(vor[-1][1]), sek(vor[-1][2]), sek(vor[-1][3])
        if nach:
            s["t0"], s["t1"] = sek(nach[0][1]), sek(nach[0][3])
        aus.append(s)
    return aus


def werte(datensatz, lead=LEAD, von_s=0.0, dauer_s=FENSTER):
    fs = datensatz["fs"]
    i = datensatz["leads"].index(lead)
    a, b = int(von_s * fs), int((von_s + dauer_s) * fs)
    sig = datensatz["sig"][a:b, i]
    sig = sig - np.median(sig)
    schritt = max(1, int(round(fs / ZIEL_FS)))
    return {"fs": fs / schritt, "lead": lead,
            "werte": [round(float(x), 3) for x in sig[::schritt]]}


def eine(nr):
    pfad = os.path.join(WURZEL, str(nr))
    d = E.lade(pfad)
    if LEAD not in d["leads"]:
        return None
    m = E.intervalle(d, LEAD)
    if not m.get("rr"):
        return None
    sl = schlaege(d)
    if len(sl) < 4:
        return None
    rhythmus, diagnose = "", []
    for k in (d["kommentare"] or []):
        k = k.strip()
        if k.lower().startswith("rhythm"):
            rhythmus = k.split(":", 1)[-1].strip()
        elif k and ":" not in k:
            diagnose.append(k)
    return {"id": nr, "rhythmus": rhythmus, "diagnose": diagnose, "messbar": True, "mess": m,
            "p_mv": E.p_amplitude(d, LEAD), "sig": werte(d), "schlaege": sl}


if __name__ == "__main__":
    nummern = sorted(int(f.split(".")[0]) for f in os.listdir(WURZEL) if f.endswith(".dat"))
    aus, gesehen = [], {}
    for nr in nummern:
        try:
            r = eine(nr)
        except Exception:
            continue
        if not r:
            continue
        gruppe = r["rhythmus"] or "ohne Angabe"
        # Früher: höchstens acht je Rhythmusgruppe. Das war richtig, solange nur
        # Kapitel 1 gebaut wurde — für den ganzen Kurs verschenkt es 159 von 200
        # Aufnahmen, und zwar ausgerechnet die knappste Ware: LUDB ist die einzige
        # Quelle mit Wellen-Annotation, also die einzige, an der gemessen werden
        # darf. Das Spiel bündelt ohnehin nur, was es braucht (tools/baue.py).
        obergrenze = int(os.environ.get("JE_GRUPPE", "0")) or 10**6
        if gesehen.get(gruppe, 0) >= obergrenze:
            continue
        gesehen[gruppe] = gesehen.get(gruppe, 0) + 1
        aus.append(r)
    aus.sort(key=lambda r: (r["rhythmus"], r["id"]))
    ziel = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bau", "ekg_daten.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(aus, f, ensure_ascii=False, separators=(",", ":"))
    print(len(aus), "Aufnahmen |", round(os.path.getsize(ziel) / 1024), "kB")
    for g, n in sorted(gesehen.items()):
        print(f"  {n:2d} × {g}")
