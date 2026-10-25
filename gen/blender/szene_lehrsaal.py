"""Ausbau „Lehrsaal" im Haus Föhrenhang (Einschulungstag und Kurswoche, 08:10) — docs/raeume/lehrsaal.md.

Baustein nach KRANKENHAUS „Entscheid (25.10.2026): Ein Haus, aus Bausteinen gebaut": die Hülle (Wände, Fenster,
Türen, Decke) baut `haus_blockout.py`, dieses Skript nur die Einrichtung, in Hauskoordinaten und in der Sammlung
„Ausbau Lehrsaal". `haus_blockout.bauen()` ruft `ausbau()` auf; die Farben, die Kamera und die Linienregeln stehen hier
und werden dort übernommen. Kein bpy auf Modulebene: haus_blockout importiert dieses Modul auch ohne Blender.

Raum (Entscheid des Nutzers 25.10.2026, Vorbild ein Seminarsaal mit Fensterfront und Tischreihen): Westende des EG,
x 0 … 14,4, y 0 … 7 (Achsen 1–4), dazu die 1-m-Nische des Eckrisalits West (x 0 … 7,2, y −1 … 0). Lichte Flächen: Giebel
x 0,45, Fensterwand y −0,55 (Nische) bzw. 0,45, Flurwand y 6,925, Rückwand x 14,325, Raumhöhe 3,4.
Blick der Spielkamera nach Südwesten (−x): links die Fenster (Südost, Morgensonne), vorn der Giebel mit der Leinwand
zwischen zwei Fenstern, rechts zwei Türen in den Flur. Vorn links in der Nische Liege und EKG-Wagen.

    python3 gen/blender/haus_blockout.py bauen && python3 gen/blender/haus_blockout.py render lehrsaal
"""
import math
import random

SAMMLUNG = "Ausbau Lehrsaal"

# Lichte Maße (Hauskoordinaten, Meter)
GIEBEL, FENSTER_NISCHE, FENSTER_WAND, FLUR_WAND, RUECK = 0.45, -0.55, 0.45, 6.925, 14.325
NISCHE_X1 = 7.2                     # Ende des Eckrisalits (Rücksprung x 6,75 … 7,2)
HOEHE = 3.4
BRUESTUNG, STURZ = 0.9, 3.1         # Fenster des Altbaus (FENSTER in haus_blockout)
# Öffnungen in den Außenwänden (aus haus_blockout: Achsen 1–2 gekoppelt, 3–4 einzeln, Giebel zwei Fenster)
FENSTER_SE_NISCHE = [(0.65, 1.65), (1.95, 2.95), (4.25, 5.25), (5.55, 6.55)]
FENSTER_SE = [(8.3, 9.7), (11.9, 13.3)]
GIEBELFENSTER = [(0.4, 1.8), (4.6, 6.0)]          # y-Bereiche; dazwischen die Leinwand (Mitte y 3,2)
TUEREN = [(3.4, 4.4), (9.3, 10.3)]                # Flurwand y 7, Türblatt 1,0 × 2,1 (vorn für die Lehrenden, hinten für alle)
SOCKEL_H = 0.8                                    # Mint-Sockel bis unter die Brüstung (0,9), Holzleiste darauf

# Tischreihen: je Reihe zwei Tische 1,8 × 0,5 m (drei Plätze), Mittelgang y 3,15 … 4,05, Gang an der Fensterseite
# 0,9 m, an der Flurseite 1,1 m. Fünf Reihen, 30 Plätze; Blick aller Stühle nach vorn (−x). Hinter der letzten Reihe
# bleiben gut 4 m frei: die Kamera steht dort, und am unteren Bildrand liegt heller Boden statt angeschnittener
# Stühle (ART_BIBLE §3.3; eine sechste Reihe bei x 11,0 lag mit den Lehnen im Bildrand).
REIHEN_X = (5.0, 6.2, 7.4, 8.6, 9.8)
BLOECKE = ((1.35, 3.15), (4.05, 5.85))
TISCH_T, TISCH_H = 0.5, 0.74

# Lokalfarben (ART_BIBLE §2, Zeile Lehrsaal): Wand Papier, Sockel Mint mit Holzleiste, Linoleum warm, Holz für Tische
# und die Lattendecke, Stühle Petrol, Gestelle Tinte. Rost kommt im Raum nicht vor (das eine Objekt ist die rote Klemme
# an der Figur Jonas). Kobalt nur in der Linealschachtel. Leinwand und Whiteboard wie EKG-Papier.
PALETTE = {
    "ls_wand": "#F7F1E4", "ls_sockel": "#BFD9CF", "ls_boden": "#C9BDA2", "ls_decke": "#C99A5B", "ls_holz": "#C99A5B",
    "ls_petrol": "#2C5560", "ls_dunkel": "#2C3E46", "ls_metall": "#8A9598", "ls_papier": "#F7F1E4", "ls_mint": "#BFD9CF",
    "ls_vorhang": "#BFD9CF", "ls_leinwand": "#F7F1E4", "ls_projektion": "#FFF8F4", "ls_tafel": "#FFF8F4",
    "ls_kobalt": "#2F5DA8", "ls_leuchte": "#FBF6EA", "ls_glas": "#1E2A30", "ls_flasche": "#D6E4DD",
    "ls_pflanze": "#2C5560", "ls_topf": "#EFE6D3", "ls_jacke": "#52636A", "ls_jacke2": "#BFD9CF",
}
OHNE_LINIE = set()
OHNE_SCHATTIERUNG = {"ls_projektion", "ls_tafel", "ls_leuchte", "ls_glas"}

# Spielkamera: hinten im Mittelgang, Augenhöhe 1,55, Blick zur Leinwand. Sonne 08:10 Anfang November (47° N): Azimut 126°,
# Höhe 9° — sie steht fast senkrecht vor der Südostfront und legt lange Lichtbahnen über Tische, Boden und Flurwand.
KAMERA = dict(ort=(14.05, 3.6, 1.55), ziel=(GIEBEL, 3.3, 1.45), brennweite=24, sonne=(126.0, 9.0),
              licht="#F8E7BF", anteil=0.55, himmel=["#DCE9EA", "#E6EFEE", "#EAF1F0"], schatten=0.2,
              linien_nur=("Trakt A EG", SAMMLUNG), ausbau=(SAMMLUNG,), ohne_scheiben=True,
              sonne_staerke=80.0)   # bei 9° trifft die Sonne Tische und Boden streifend: stark genug, dass jede besonnte Fläche zählt


def ausbau(h):
    """Baut die Einrichtung. `h`: Euler (mathutils), kiste/netz/wandnetz aus haus_blockout. Alle Körper als Netz aus
    Punktlisten, ohne bpy.ops: in der Szene mit 4000 Objekten kostete jeder Operator-Aufruf eine Depsgraph-Aktualisierung
    (erste Fassung mit werkzeug-Grundkörpern: Bau 9:44 min statt einiger Sekunden)."""
    Euler = h["Euler"]
    zr = random.Random(8)

    def netz(name, verts, faces, m):
        return h["netz"](name, verts, faces, m, SAMMLUNG)

    def box(name, x0, y0, x1, y1, z0, z1, m):                     # achsparallel
        return h["kiste"](name, x0, y0, x1, y1, z0, z1, m, SAMMLUNG)

    def gedreht(punkte, ort, dreh):
        mat = Euler(dreh).to_matrix()
        return [tuple(mat @ h["Vector"](p) + h["Vector"](ort)) for p in punkte]

    def kiste(groesse, ort, m, dreh=0.0, kipp=0.0, fase=0.0, name="kiste"):   # gedreht um z (Grad), gekippt um die lokale x-Achse
        a, b, c = (g / 2 for g in groesse)
        v = [(-a, -b, -c), (a, -b, -c), (a, b, -c), (-a, b, -c), (-a, -b, c), (a, -b, c), (a, b, c), (-a, b, c)]
        return netz(name, gedreht(v, ort, (math.radians(kipp), 0, math.radians(dreh))),
                    [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (3, 0, 4, 7), (1, 2, 6, 5)], m)

    def kegelstumpf(r0, r1, hoehe, ort, m, dreh=(0, 0, 0), v=16, name="zylinder"):   # Achse lokal z, Mitte bei ort
        ring = [(math.cos(2 * math.pi * i / v), math.sin(2 * math.pi * i / v)) for i in range(v)]
        pts = [(r0 * c, r0 * s, -hoehe / 2) for c, s in ring] + [(r1 * c, r1 * s, hoehe / 2) for c, s in ring]
        faces = [tuple(range(v - 1, -1, -1)), tuple(range(v, 2 * v))] + [(i, (i + 1) % v, v + (i + 1) % v, v + i) for i in range(v)]
        return netz(name, gedreht(pts, ort, dreh), faces, m)

    def zyl(r, hoehe, ort, m, dreh=(0, 0, 0), v=16, name="zylinder"):
        return kegelstumpf(r, r, hoehe, ort, m, dreh, v, name)

    def ring(R, r, ort, m, n=40, k=8, name="ring"):
        pts = [((R + r * math.cos(2 * math.pi * j / k)) * math.cos(2 * math.pi * i / n), (R + r * math.cos(2 * math.pi * j / k)) * math.sin(2 * math.pi * i / n),
                r * math.sin(2 * math.pi * j / k)) for i in range(n) for j in range(k)]
        faces = [(i * k + j, i * k + (j + 1) % k, ((i + 1) % n) * k + (j + 1) % k, ((i + 1) % n) * k + j) for i in range(n) for j in range(k)]
        return netz(name, gedreht(pts, ort, (0, 0, 0)), faces, m)

    def wand(name, achse, w0, w1, a0, a1, z0, z1, oeffnungen, m):
        return h["wandnetz"](name, achse, w0, w1, a0, a1, z0, z1, oeffnungen, m, SAMMLUNG)

    # ---------------- Boden, Wandflächen, Sockel ----------------
    box("LS Boden", GIEBEL, FENSTER_NISCHE, RUECK, FLUR_WAND, 0.0, 0.015, "ls_boden")
    fo = lambda liste: [(a0, a1, BRUESTUNG, STURZ) for a0, a1 in liste]
    d = 0.02                                                   # Wandfläche 2 cm vor der Rohwand (Altbau-Rustika innen)
    wand("LS Wand Giebel", "x", GIEBEL, GIEBEL + d, FENSTER_NISCHE, FLUR_WAND, 0, HOEHE, fo(GIEBELFENSTER), "ls_wand")
    wand("LS Wand Nische", "y", FENSTER_NISCHE - d, FENSTER_NISCHE, GIEBEL, 6.75, 0, HOEHE, fo(FENSTER_SE_NISCHE), "ls_wand")
    box("LS Pfeiler Nische", 6.75 - d, FENSTER_NISCHE, NISCHE_X1, FENSTER_WAND, 0, HOEHE, "ls_wand")
    wand("LS Wand Fenster", "y", FENSTER_WAND, FENSTER_WAND + d, NISCHE_X1, RUECK, 0, HOEHE, fo(FENSTER_SE), "ls_wand")
    tueren = [(a0, a1, -0.02, 2.1) for a0, a1 in TUEREN]
    wand("LS Wand Flur", "y", FLUR_WAND - d, FLUR_WAND, GIEBEL, RUECK, 0, HOEHE, tueren, "ls_wand")
    s = 0.03                                                   # Sockel Mint, Holzleiste darauf
    box("LS Sockel Giebel", GIEBEL + d, FENSTER_NISCHE + d, GIEBEL + d + s, FLUR_WAND - d, 0, SOCKEL_H, "ls_sockel")
    box("LS Leiste Giebel", GIEBEL + d, FENSTER_NISCHE + d, GIEBEL + d + s + 0.02, FLUR_WAND - d, SOCKEL_H, SOCKEL_H + 0.05, "ls_holz")
    box("LS Sockel Nische", GIEBEL + d, FENSTER_NISCHE, 6.75 - d, FENSTER_NISCHE + s, 0, SOCKEL_H, "ls_sockel")
    box("LS Leiste Nische", GIEBEL + d, FENSTER_NISCHE, 6.75 - d, FENSTER_NISCHE + s + 0.02, SOCKEL_H, SOCKEL_H + 0.05, "ls_holz")
    box("LS Sockel Fenster", NISCHE_X1, FENSTER_WAND + d, RUECK, FENSTER_WAND + d + s, 0, SOCKEL_H, "ls_sockel")
    box("LS Leiste Fenster", NISCHE_X1, FENSTER_WAND + d, RUECK, FENSTER_WAND + d + s + 0.02, SOCKEL_H, SOCKEL_H + 0.05, "ls_holz")
    tuer_sockel = [(a0 - 0.1, a1 + 0.1, -0.1, SOCKEL_H + 0.2) for a0, a1 in TUEREN]
    wand("LS Sockel Flur", "y", FLUR_WAND - d - s, FLUR_WAND - d, GIEBEL + d, RUECK, 0, SOCKEL_H, tuer_sockel, "ls_sockel")
    for i, (a0, a1) in enumerate([(GIEBEL + d, TUEREN[0][0] - 0.1), (TUEREN[0][1] + 0.1, TUEREN[1][0] - 0.1), (TUEREN[1][1] + 0.1, RUECK)]):
        box(f"LS Leiste Flur {i}", a0, FLUR_WAND - d - s - 0.02, a1, FLUR_WAND - d, SOCKEL_H, SOCKEL_H + 0.05, "ls_holz")
    for a0, a1 in TUEREN:                                      # Holzzarge zur Flurseite der Tür
        for x in (a0 - 0.08, a1):
            box("LS Zarge", x, FLUR_WAND - d - 0.05, x + 0.08, FLUR_WAND, 0, 2.18, "ls_holz")
        box("LS Zarge oben", a0 - 0.08, FLUR_WAND - d - 0.05, a1 + 0.08, FLUR_WAND, 2.1, 2.18, "ls_holz")

    # Fensterbänke innen (Papier) und Vorhänge (Mint, je Fenstergruppe links und rechts gerafft), Vorhangschiene
    def fensterbank(achse, lage, innen, a0, a1):
        w0, w1 = sorted((lage, lage + innen * 0.28))
        if achse == "y": box("LS Fensterbank", a0 - 0.05, w0, a1 + 0.05, w1, BRUESTUNG - 0.04, BRUESTUNG, "ls_papier")
        else: box("LS Fensterbank", w0, a0 - 0.05, w1, a1 + 0.05, BRUESTUNG - 0.04, BRUESTUNG, "ls_papier")

    def vorhang(achse, lage, innen, a, seite):
        """Gerafftes Paket: drei Falten (schmale Kisten), leicht versetzt, vom Boden bis zur Schiene."""
        for f in range(3):
            u = a + seite * (0.06 + 0.09 * f); w = lage + innen * (0.05 + 0.035 * (f % 2))
            if achse == "y": box("LS Vorhang", u - 0.06, w - 0.03, u + 0.06, w + 0.03, 0.06, 3.22, "ls_vorhang")
            else: box("LS Vorhang", w - 0.03, u - 0.06, w + 0.03, u + 0.06, 0.06, 3.22, "ls_vorhang")

    gruppen = [("y", FENSTER_NISCHE, +1, (0.65, 2.95)), ("y", FENSTER_NISCHE, +1, (4.25, 6.55)),
               ("y", FENSTER_WAND + d, +1, FENSTER_SE[0]), ("y", FENSTER_WAND + d, +1, FENSTER_SE[1]),
               ("x", GIEBEL + d, +1, GIEBELFENSTER[0]), ("x", GIEBEL + d, +1, GIEBELFENSTER[1])]
    for achse, lage, innen, (a0, a1) in gruppen:
        fensterbank(achse, lage, innen, a0, a1)
        vorhang(achse, lage, innen, a0, -1); vorhang(achse, lage, innen, a1, +1)
    box("LS Schiene Nische", GIEBEL + d, FENSTER_NISCHE + 0.02, 6.75 - d, FENSTER_NISCHE + 0.06, 3.22, 3.26, "ls_dunkel")
    box("LS Schiene Fenster", NISCHE_X1, FENSTER_WAND + 0.04, RUECK, FENSTER_WAND + 0.08, 3.22, 3.26, "ls_dunkel")
    box("LS Schiene Giebel", GIEBEL + 0.04, FENSTER_NISCHE + d, GIEBEL + 0.08, FLUR_WAND - d, 3.22, 3.26, "ls_dunkel")

    # Pflanzen auf den Fensterbänken (Petrol, die dunkle Form): Topf und drei bis fünf Blätter als gekippte Kisten
    def pflanze(x, y, groesse=1.0):
        zyl(0.08 * groesse, 0.14 * groesse, (x, y, BRUESTUNG + 0.07 * groesse), "ls_topf", v=14, name="LS Topf")
        for b in range(zr.randint(3, 5)):
            w = zr.uniform(0, 360); k = zr.uniform(15, 40)
            kiste((0.05 * groesse, 0.02, 0.24 * groesse), (x + 0.04 * math.cos(math.radians(w)), y + 0.04 * math.sin(math.radians(w)),
                  BRUESTUNG + 0.24 * groesse), "ls_pflanze", dreh=w, kipp=k, name="LS Blatt")

    pflanze(1.15, FENSTER_NISCHE + 0.14); pflanze(5.9, FENSTER_NISCHE + 0.13, 1.3); pflanze(12.2, FENSTER_WAND + 0.17, 0.9)
    pflanze(GIEBEL + 0.16, 5.5, 1.2)

    # ---------------- Decke: Holzlatten längs des Raums, Lichtbänder quer, zwei Ringleuchten, Beamer ----------------
    y = FENSTER_NISCHE
    while y < FLUR_WAND - 0.05:                                # Latten 0,6 m, Fuge 2,4 cm; in der Nische nur bis zum Rücksprung
        box("LS Latte", GIEBEL, y + 0.012, NISCHE_X1 if y + 0.3 < FENSTER_WAND else RUECK, min(y + 0.6, FLUR_WAND) - 0.012, 3.31, 3.36, "ls_decke")
        y += 0.6
    for (x, ya, yb) in ((1.6, 0.6, 5.2), (3.7, 1.8, 6.2), (6.4, -0.2, 3.0), (8.3, 2.4, 6.0), (10.5, 0.9, 4.6), (12.6, 3.0, 6.4)):
        box("LS Lichtband", x - 0.03, ya, x + 0.03, yb, 3.29, 3.31, "ls_leuchte")
    for (x, y) in ((7.8, 2.25), (7.8, 4.95)):                  # Ringleuchten (aus), an drei dünnen Seilen
        ring(0.55, 0.025, (x, y, 2.75), "ls_leuchte", name="LS Ringleuchte")
        for w in (90, 210, 330):
            zyl(0.004, 0.56, (x + 0.55 * math.cos(math.radians(w)), y + 0.55 * math.sin(math.radians(w)), 3.03), "ls_dunkel", v=6, name="LS Seil")
    zyl(0.02, 0.18, (6.6, 3.25, 3.22), "ls_dunkel", v=10, name="LS Beamer Stange")
    kiste((0.34, 0.3, 0.11), (6.6, 3.25, 3.08), "ls_papier", fase=0.012, name="LS Beamer")
    zyl(0.035, 0.03, (6.42, 3.25, 3.08), "ls_glas", dreh=(0, math.radians(90), 0), v=16, name="LS Beamer Linse")

    # ---------------- Giebel: Leinwand zwischen den Fenstern, Uhr; Flurwand vorn: Whiteboard ----------------
    gx = GIEBEL + d; lm, lb, lh, lz = 3.2, 2.4, 1.5, 1.0
    box("LS Leinwand Kasten", gx, lm - lb / 2 - 0.05, gx + 0.09, lm + lb / 2 + 0.05, lz + lh, lz + lh + 0.09, "ls_dunkel")
    box("LS Leinwand Tuch", gx + 0.03, lm - lb / 2, gx + 0.042, lm + lb / 2, lz, lz + lh, "ls_leinwand")
    box("LS Leinwand Leiste", gx + 0.02, lm - lb / 2 - 0.01, gx + 0.05, lm + lb / 2 + 0.01, lz - 0.03, lz, "ls_dunkel")
    box("LS Projektion", gx + 0.042, lm - lb / 2 + 0.08, gx + 0.046, lm + lb / 2 - 0.08, lz + 0.06, lz + lh - 0.06, "ls_projektion")
    for (r, t, m) in ((0.21, 0.02, "ls_dunkel"), (0.19, 0.03, "ls_papier")):   # Wanduhr über der vorderen Tür
        zyl(r, t, (sum(TUEREN[0]) / 2, FLUR_WAND - d - t / 2, 2.6), m, dreh=(math.radians(90), 0, 0), v=32, name="LS Uhr")
    wx0, wx1, wz0, wz1 = 0.9, 2.9, 0.9, 2.1
    box("LS Whiteboard Rahmen", wx0 - 0.03, FLUR_WAND - d - 0.03, wx1 + 0.03, FLUR_WAND - d, wz0 - 0.03, wz1 + 0.03, "ls_metall")
    box("LS Whiteboard", wx0, FLUR_WAND - d - 0.034, wx1, FLUR_WAND - d - 0.03, wz0, wz1, "ls_tafel")
    box("LS Whiteboard Ablage", wx0 + 0.3, FLUR_WAND - d - 0.1, wx1 - 0.3, FLUR_WAND - d, wz0 - 0.06, wz0 - 0.03, "ls_metall")

    # ---------------- Vorn: Dozententisch mit Linealschachtel, Liege und EKG-Wagen in der Nische ----------------
    def tisch(xm, ym, lx, ly, h_=TISCH_H, name="LS Tisch"):
        box(name + " Platte", xm - lx / 2, ym - ly / 2, xm + lx / 2, ym + ly / 2, h_ - 0.03, h_, "ls_holz")
        for ya in (ym - ly / 2 + 0.06, ym + ly / 2 - 0.1):     # T-Gestell an beiden Enden (wie Klapptische)
            box(name + " Bein", xm - 0.02, ya, xm + 0.02, ya + 0.04, 0.04, h_ - 0.03, "ls_dunkel")
            box(name + " Fuss", xm - lx / 2 + 0.02, ya, xm + lx / 2 - 0.02, ya + 0.04, 0.0, 0.04, "ls_dunkel")
        box(name + " Zarge", xm - 0.02, ym - ly / 2 + 0.1, xm + 0.02, ym + ly / 2 - 0.1, h_ - 0.09, h_ - 0.03, "ls_dunkel")

    tx, ty = 2.1, 4.9                                          # Dozententisch rechts vor der Leinwand, quer zum Raum
    tisch(tx, ty, 0.75, 1.6, name="LS Dozententisch")
    kiste((0.2, 0.26, 0.07), (tx + 0.05, ty - 0.45, TISCH_H + 0.035), "ls_papier", dreh=8, name="LS Linealschachtel")
    for k in range(5):
        kiste((0.04, 0.19, 0.004), (tx + 0.0 + 0.025 * k, ty - 0.45, TISCH_H + 0.075 + 0.003 * k), "ls_kobalt", dreh=8 + 3 * k, name="LS Lineal")
    kiste((0.21, 0.3, 0.02), (tx - 0.1, ty + 0.05, TISCH_H + 0.01), "ls_papier", dreh=-6, name="LS EKG-Blaetter")
    kiste((0.24, 0.33, 0.015), (tx + 0.05, ty + 0.5, TISCH_H + 0.008), "ls_dunkel", dreh=0, name="LS Laptop")
    kiste((0.24, 0.015, 0.22), (tx - 0.07, ty + 0.5, TISCH_H + 0.12), "ls_dunkel", dreh=90, kipp=-12, name="LS Laptop Deckel")
    zyl(0.035, 0.24, (tx + 0.22, ty - 0.1, TISCH_H + 0.12), "ls_flasche", v=14, name="LS Flasche")

    # Liege längs der Nische, Kopfende zum Giebel; Tritt zur Raumseite; Wagen am Kopfende, Schirm zum Raum
    lx0, lx1, ly0, ly1, lo = 2.5, 4.45, -0.42, 0.23, 0.75
    lyM = (ly0 + ly1) / 2
    box("LS Liege Fuss", lx0 + 0.3, ly0 + 0.05, lx1 - 0.3, ly1 - 0.05, 0.0, 0.06, "ls_petrol")
    box("LS Liege Saeule", (lx0 + lx1) / 2 - 0.25, lyM - 0.16, (lx0 + lx1) / 2 + 0.25, lyM + 0.16, 0.06, 0.57, "ls_dunkel")
    box("LS Liege Rahmen", lx0 + 0.03, ly0 + 0.015, lx1 - 0.03, ly1 - 0.015, 0.57, 0.62, "ls_dunkel")
    kiste((lx1 - lx0, ly1 - ly0, 0.13), ((lx0 + lx1) / 2, lyM, lo - 0.065), "ls_mint", fase=0.03, name="LS Liege Polster")
    box("LS Liege Papier", lx0 + 0.05, ly0 + 0.07, lx1 - 0.05, ly1 - 0.07, lo, lo + 0.003, "ls_papier")
    kiste((0.3, 0.4, 0.07), (lx0 + 0.2, lyM, lo + 0.035), "ls_papier", fase=0.03, name="LS Kissen")
    zyl(0.065, 0.56, (lx0 - 0.03, lyM, lo + 0.09), "ls_papier", dreh=(math.radians(90), 0, 0), v=20, name="LS Papierrolle")
    box("LS Tritt", lx0 + 0.25, ly1 + 0.02, lx0 + 0.7, ly1 + 0.44, 0.0, 0.25, "ls_dunkel")
    box("LS Tritt Flaeche", lx0 + 0.25, ly1 + 0.02, lx0 + 0.7, ly1 + 0.44, 0.25, 0.262, "ls_petrol")
    wcx, wcy = 1.85, 0.55                                      # EKG-Wagen
    box("LS Wagen Boden oben", wcx - 0.23, wcy - 0.28, wcx + 0.23, wcy + 0.28, 0.9, 0.95, "ls_petrol")
    box("LS Wagen Boden unten", wcx - 0.23, wcy - 0.28, wcx + 0.23, wcy + 0.28, 0.22, 0.26, "ls_petrol")
    for dx in (-0.18, 0.18):
        for dy in (-0.23, 0.23):
            zyl(0.012, 0.9, (wcx + dx, wcy + dy, 0.5), "ls_metall", v=8, name="LS Wagen Pfosten")
    box("LS Wagen Geraet", wcx - 0.18, wcy - 0.25, wcx + 0.18, wcy + 0.25, 0.95, 1.06, "ls_dunkel")
    kiste((0.03, 0.34, 0.25), (wcx + 0.12, wcy, 1.19), "ls_dunkel", dreh=0, name="LS Wagen Schirmrahmen")
    box("LS Wagen Schirm", wcx + 0.135, wcy - 0.15, wcx + 0.139, wcy + 0.15, 1.095, 1.285, "ls_glas")
    box("LS Wagen Streifen", wcx + 0.18, wcy - 0.06, wcx + 0.183, wcy + 0.06, 0.82, 1.0, "ls_papier")

    # Stuhl der Dozentin neben dem Tisch, Jacke über der Lehne (sie sitzt nicht)
    def stuhl(x, y, dreh=-90.0, name="LS Stuhl", jacke=None, tasche=None):
        """Seminarstuhl: Sitz und Lehne Petrol, Gestell Tinte. Lehne auf der lokalen +y-Seite; dreh −90° = Lehne nach +x."""
        a = math.radians(dreh); c, s_ = math.cos(a), math.sin(a)
        P = lambda dx, dy, z: (x + dx * c - dy * s_, y + dx * s_ + dy * c, z)
        kiste((0.44, 0.44, 0.05), P(0, 0, 0.455), "ls_petrol", dreh=dreh, fase=0.015, name=name + " Sitz")
        for dx in (-0.19, 0.19):
            for dy in (-0.19, 0.19):
                zyl(0.011, 0.43, P(dx, dy, 0.215), "ls_dunkel", v=8, name=name + " Bein")
        kiste((0.44, 0.035, 0.26), P(0, 0.23, 0.74), "ls_petrol", dreh=dreh, kipp=-8, fase=0.012, name=name + " Lehne")
        for dx in (-0.19, 0.19):
            zyl(0.011, 0.3, P(dx, 0.21, 0.62), "ls_dunkel", v=8, name=name + " Holm")
        if jacke:
            kiste((0.36, 0.07, 0.5), P(0.02, 0.28, 0.6), jacke, dreh=dreh + 4, kipp=-6, name=name + " Jacke")   # hängt hinter der Lehne
        if tasche:
            kiste((0.34, 0.14, 0.3), P(0.32, -0.05, 0.15), tasche, dreh=dreh + zr.uniform(-20, 20), fase=0.04, name=name + " Tasche")

    stuhl(tx + 0.55, ty + 0.55, dreh=180 + 20, name="LS Stuhl Dozentin", jacke="ls_dunkel")

    # ---------------- Tischreihen ----------------
    for r, xm in enumerate(REIHEN_X):
        for (ya, yb) in BLOECKE:
            tisch(xm, (ya + yb) / 2, TISCH_T, yb - ya)
            for p in range(3):
                yp = ya + 0.3 + 0.6 * p
                raus = zr.choice((0.0, 0.0, 0.05, 0.12, 0.25)); dreh = -90 + zr.choice((0, 0, 0, -8, 6, 12))
                jacke = zr.choice((None,) * 9 + ("ls_jacke", "ls_jacke2"))
                tasche = zr.choice((None,) * 8 + ("ls_dunkel", "ls_petrol"))
                if r == len(REIHEN_X) - 1: tasche = None    # keine dunklen Klötze am unteren Bildrand (ART_BIBLE §3.3)
                stuhl(xm + TISCH_T / 2 + 0.3 + raus, yp, dreh, jacke=jacke, tasche=tasche)
                if zr.random() < 0.55:                     # Block und Stift am Platz
                    kiste((0.21, 0.29, 0.006), (xm + 0.05, yp, TISCH_H + 0.003), "ls_papier", dreh=90 + zr.uniform(-8, 8), name="LS Block")
                    kiste((0.008, 0.14, 0.008), (xm + 0.06, yp + 0.17, TISCH_H + 0.01), "ls_dunkel", dreh=zr.uniform(-20, 20), name="LS Stift")
            if zr.random() < 0.6:                          # eine Wasserflasche je zweitem Tisch
                zyl(0.028, 0.2, (xm - 0.15, ya + 0.25 + zr.uniform(0, 1.2), TISCH_H + 0.1), "ls_flasche", v=14, name="LS Flasche")

    # Stehleuchten zwischen den Fenstern (aus): Fuß, Stange, Schirm
    for (x, y) in ((7.75, 0.85), (10.85, 0.85)):
        zyl(0.16, 0.02, (x, y, 0.01), "ls_dunkel", v=20, name="LS Stehleuchte Fuss")
        zyl(0.012, 1.45, (x, y, 0.74), "ls_dunkel", v=8, name="LS Stehleuchte Stange")
        kegelstumpf(0.22, 0.15, 0.3, (x, y, 1.6), "ls_petrol", v=24, name="LS Stehleuchte Schirm")
