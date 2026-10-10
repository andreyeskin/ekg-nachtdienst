# -*- coding: utf-8 -*-
"""EKG-Renderer: echte Aufnahmen (LUDB/PTB-XL, WFDB) auf echtem Millimeterpapier.

Grundsätze
----------
* Es wird in **Millimetern** gezeichnet (SVG-viewBox in mm). Damit stimmen
  Papiervorschub (mm/s) und Verstärkung (mm/mV) per Konstruktion, egal wie groß
  die Grafik später dargestellt wird.
* Jede gezeichnete Kurve lässt sich nachmessen: `intervalle()` liefert aus den
  Experten-Annotationen (LUDB) P-Dauer, PQ-Zeit, QRS-Breite, QT und RR in msek.
"""
import math
import os

import numpy as np
import wfdb

PAPIER = "#FFF8F4"
LINIE_FEIN = "#F0BCA9"
LINIE_GROB = "#DD8A6E"
KURVE = "#1A1A1A"


# ----------------------------------------------------------------- Laden
def lade(pfad, annotationen=True):
    """Liest einen WFDB-Datensatz; gibt Signal (mV), fs, Ableitungsnamen, Kommentare, Annotationen."""
    r = wfdb.rdrecord(pfad)
    d = {"sig": r.p_signal, "fs": r.fs, "leads": [s.lower() for s in r.sig_name],
         "kommentare": r.comments, "name": os.path.basename(pfad), "ann": {}}
    if annotationen:
        for lead in d["leads"]:
            try:
                a = wfdb.rdann(pfad, lead)
                d["ann"][lead] = list(zip(a.sample.tolist(), a.symbol))
            except Exception:
                pass
    return d


def _wellen(ann):
    """LUDB-Annotation → Liste von (typ, start, peak, ende) in Samples. typ: p | N | t"""
    out, offen = [], None
    for i, (pos, sym) in enumerate(ann):
        if sym == "(":
            offen = pos
        elif sym in "pNt":
            peak, typ = pos, sym
            ende = None
            for pos2, sym2 in ann[i + 1:i + 3]:
                if sym2 == ")":
                    ende = pos2
                    break
            if offen is not None and ende is not None:
                out.append((typ, offen, peak, ende))
            offen = None
    return out


def intervalle(datensatz, lead="ii"):
    """Misst aus den Experten-Annotationen: P-Dauer, PQ, QRS, QT, RR (msek, Median über alle Schläge)."""
    ann = datensatz["ann"].get(lead)
    if not ann:
        return {}
    fs = datensatz["fs"]
    w = _wellen(ann)
    ps = [x for x in w if x[0] == "p"]
    qrs = [x for x in w if x[0] == "N"]
    ts = [x for x in w if x[0] == "t"]
    ms = lambda n: round(1000.0 * n / fs)

    p_dauer = [ms(e - s) for _, s, _, e in ps]
    qrs_dauer = [ms(e - s) for _, s, _, e in qrs]
    rr = [ms(b[2] - a[2]) for a, b in zip(qrs, qrs[1:])]
    pq, qt = [], []
    for _, ps_s, _, _ in [(x) for x in ps]:
        pass
    for p in ps:                                   # PQ: P-Beginn → nächster QRS-Beginn
        nach = [q for q in qrs if q[1] >= p[3]]
        if nach:
            pq.append(ms(nach[0][1] - p[1]))
    for q in qrs:                                  # QT: QRS-Beginn → T-Ende
        nach = [t for t in ts if t[1] >= q[3]]
        if nach:
            qt.append(ms(nach[0][3] - q[1]))

    med = lambda v: int(np.median(v)) if v else None
    erg = {"p_dauer": med(p_dauer), "pq": med(pq), "qrs": med(qrs_dauer), "qt": med(qt), "rr": med(rr)}
    erg["frequenz"] = round(60000 / erg["rr"]) if erg["rr"] else None
    if erg["qt"] and erg["rr"]:
        erg["qtc"] = round(erg["qt"] / math.sqrt(erg["rr"] / 1000.0))
    erg["schlaege"] = len(qrs)
    return erg


def p_amplitude(datensatz, lead="ii"):
    """Höhe der P-Welle in mV (Median), gemessen gegen die Grundlinie vor dem P-Beginn."""
    ann = datensatz["ann"].get(lead)
    if not ann:
        return None
    i = datensatz["leads"].index(lead)
    sig = datensatz["sig"][:, i]
    werte = []
    for typ, s, peak, e in _wellen(ann):
        if typ != "p":
            continue
        basis = np.median(sig[max(0, s - 40):s]) if s > 5 else 0.0
        werte.append(float(sig[peak] - basis))
    return round(float(np.median(werte)), 3) if werte else None


# ----------------------------------------------------------------- Zeichnen
def _raster(breite_mm, hoehe_mm):
    s = [f'<rect x="0" y="0" width="{breite_mm}" height="{hoehe_mm}" fill="{PAPIER}"/>']
    for i in range(int(breite_mm) + 1):
        grob = i % 5 == 0
        s.append(f'<line x1="{i}" y1="0" x2="{i}" y2="{hoehe_mm}" stroke="{LINIE_GROB if grob else LINIE_FEIN}" '
                 f'stroke-width="{0.25 if grob else 0.1}"/>')
    for j in range(int(hoehe_mm) + 1):
        grob = j % 5 == 0
        s.append(f'<line x1="0" y1="{j}" x2="{breite_mm}" y2="{j}" stroke="{LINIE_GROB if grob else LINIE_FEIN}" '
                 f'stroke-width="{0.25 if grob else 0.1}"/>')
    return "".join(s)


def _pfad(y_werte, x0_mm, y0_mm, mm_pro_s, mm_pro_mv, fs, schritt=1):
    """Polyline-Punkte in mm. y0 = Grundlinie."""
    pts = []
    dt_mm = mm_pro_s / fs * schritt
    for k in range(0, len(y_werte), schritt):
        x = x0_mm + k / schritt * dt_mm
        y = y0_mm - y_werte[k] * mm_pro_mv
        pts.append(f"{x:.2f},{y:.2f}")
    return " ".join(pts)


def streifen_svg(datensatz, lead="ii", von_s=0.0, dauer_s=10.0, mm_pro_s=25, mm_pro_mv=10,
                 hoehe_mm=40, kalibrierung=True, beschriftung=True, klasse="ekg"):
    """Ein Rhythmusstreifen auf Millimeterpapier, Maße in mm (1 SVG-Einheit = 1 mm)."""
    fs = datensatz["fs"]
    i = datensatz["leads"].index(lead)
    a, b = int(von_s * fs), int((von_s + dauer_s) * fs)
    sig = datensatz["sig"][a:b, i]
    sig = sig - np.median(sig)                       # Grundlinie auf 0
    vorlauf = 12 if kalibrierung else 2              # Platz für Eichzacke
    breite_mm = vorlauf + dauer_s * mm_pro_s + 2
    y0 = hoehe_mm / 2
    s = [_raster(breite_mm, hoehe_mm)]
    if kalibrierung:                                  # 1-mV-Eichzacke: 5 mm breit, 10 mm hoch
        s.append(f'<path d="M2,{y0} H4 V{y0-mm_pro_mv} H9 V{y0} H{vorlauf}" fill="none" stroke="{KURVE}" '
                 f'stroke-width="0.3" stroke-linejoin="round"/>')
    s.append(f'<polyline points="{_pfad(sig, vorlauf, y0, mm_pro_s, mm_pro_mv, fs)}" fill="none" '
             f'stroke="{KURVE}" stroke-width="0.3" stroke-linejoin="round" stroke-linecap="round"/>')
    if beschriftung:
        s.append(f'<text x="2" y="{hoehe_mm-1.5}" font-size="2.6" fill="#444" font-family="Helvetica,Arial">'
                 f'{lead.upper()} · {mm_pro_s} mm/s · {mm_pro_mv} mm/mV</text>')
    return (f'<svg class="{klasse}" viewBox="0 0 {breite_mm:.0f} {hoehe_mm:.0f}" '
            f'style="width:100%;height:auto;display:block" role="img" aria-label="EKG {lead}">{"".join(s)}</svg>')


LAYOUT_12 = [["i", "avr", "v1", "v4"], ["ii", "avl", "v2", "v5"], ["iii", "avf", "v3", "v6"]]


def zwoelf_svg(datensatz, von_s=0.0, spalten_s=2.5, mm_pro_s=25, mm_pro_mv=10, rhythmus="ii"):
    """12-Kanal-Ausdruck im üblichen 3×4-Raster plus Rhythmusstreifen — wie im Klinikausdruck."""
    fs = datensatz["fs"]
    vorlauf = 12
    spalte_mm = spalten_s * mm_pro_s
    breite_mm = vorlauf + 4 * spalte_mm + 2
    zeile_mm = 22
    hoehe_mm = 3 * zeile_mm + (zeile_mm + 4 if rhythmus else 0) + 4
    s = [_raster(breite_mm, hoehe_mm)]
    for zi, zeile in enumerate(LAYOUT_12):
        y0 = 2 + zeile_mm * zi + zeile_mm / 2
        if zi == 0:
            s.append(f'<path d="M2,{y0} H4 V{y0-mm_pro_mv} H9 V{y0} H{vorlauf}" fill="none" stroke="{KURVE}" stroke-width="0.3"/>')
        for si, lead in enumerate(zeile):
            i = datensatz["leads"].index(lead)
            t0 = von_s + si * spalten_s
            a, b = int(t0 * fs), int((t0 + spalten_s) * fs)
            sig = datensatz["sig"][a:b, i]
            sig = sig - np.median(sig)
            x0 = vorlauf + si * spalte_mm
            s.append(f'<polyline points="{_pfad(sig, x0, y0, mm_pro_s, mm_pro_mv, fs)}" fill="none" '
                     f'stroke="{KURVE}" stroke-width="0.3" stroke-linejoin="round"/>')
            s.append(f'<text x="{x0+1}" y="{y0-8}" font-size="2.8" font-weight="bold" fill="#222" '
                     f'font-family="Helvetica,Arial">{lead.upper()}</text>')
            if si:
                s.append(f'<line x1="{x0}" y1="{y0-9}" x2="{x0}" y2="{y0+9}" stroke="#B9937F" stroke-width="0.15"/>')
    if rhythmus:
        y0 = 2 + 3 * zeile_mm + zeile_mm / 2 + 2
        i = datensatz["leads"].index(rhythmus)
        a, b = int(von_s * fs), int((von_s + 4 * spalten_s) * fs)
        sig = datensatz["sig"][a:b, i] - np.median(datensatz["sig"][a:b, i])
        s.append(f'<polyline points="{_pfad(sig, vorlauf, y0, mm_pro_s, mm_pro_mv, fs)}" fill="none" '
                 f'stroke="{KURVE}" stroke-width="0.3" stroke-linejoin="round"/>')
        s.append(f'<text x="2" y="{y0+1}" font-size="2.8" font-weight="bold" fill="#222" font-family="Helvetica,Arial">{rhythmus.upper()}</text>')
    s.append(f'<text x="2" y="{hoehe_mm-1}" font-size="2.4" fill="#555" font-family="Helvetica,Arial">'
             f'{mm_pro_s} mm/s · {mm_pro_mv} mm/mV</text>')
    return (f'<svg viewBox="0 0 {breite_mm:.0f} {hoehe_mm:.0f}" style="width:100%;height:auto;display:block" '
            f'role="img" aria-label="12-Kanal-EKG">{"".join(s)}</svg>')


# ----------------------------------------------------------------- Export fürs Spiel
def export_js(datensatz, lead="ii", von_s=0.0, dauer_s=10.0, ziel_fs=200, nachkomma=3):
    """Kompakte Signaldaten für den Browser: Liste in mV, heruntergetastet."""
    fs = datensatz["fs"]
    i = datensatz["leads"].index(lead)
    a, b = int(von_s * fs), int((von_s + dauer_s) * fs)
    sig = datensatz["sig"][a:b, i]
    sig = sig - np.median(sig)
    schritt = max(1, int(round(fs / ziel_fs)))
    sig = sig[::schritt]
    return {"fs": fs / schritt, "lead": lead, "werte": [round(float(x), nachkomma) for x in sig]}
