"""Szene „Lehrsaal" (Einschulungstag, 08:10, Vormittag) — 3D-Grundlage für die Ebenen des Spiels.

Nach docs/raeume/lehrsaal.md: Seminarraum mit Untersuchungsliege, Projektionsleinwand an der Rückwand,
Whiteboard an der rechten Seitenwand, hohe Fenster rechts, Tür links in den Flur. Rückwand bei y=0, Raum
nach −y (die Raumbeschreibung misst y von der Rückwand in den Raum; hier negiert). Kamera blickt entlang +y
ohne Neigung (Objektivverschiebung wie im Monitorzimmer): die Rückwand bleibt frontal, die Leinwand ist im
Bild ein exaktes Rechteck, auf das das Spiel zeichnet (`schirmflaeche("projektion")`).

Kamera: 28 mm, (0,9 / −9,0 / 2,0). Die vorgeschlagenen −7,6 m reichen nicht: mit der Tür ganz links
(x −4,9) und dem Whiteboard an der rechten Seitenwand (x 4,4, y −0,9 … −2,9) braucht das Bild 63° Sichtwinkel,
bei 7,6 m Abstand fiele eines von beiden aus dem Bild. Die Hülle ist entsprechend 8,4 m tief.
Rendern: python3 gen/blender/ebenen.py lehrsaal alle
"""
import math

import bpy
from mathutils import Vector

from werkzeug import (fenster, himmel_baender, jalousie, kegel, kiste, kugel, leeren, loch, markiere, material,
                      platte, platzhalter, raum_huelle, schirmflaeche, zylinder)

leeren()
sc = bpy.context.scene

# Materialien: Grauwerte nur für den Licht-Durchgang, die Bildfarbe steht in PALETTE
M = {n: material(n, c, r) for n, c, r in (
    ("wand", (0.62, 0.60, 0.55), 0.85), ("boden", (0.50, 0.48, 0.44), 0.4), ("decke", (0.5, 0.5, 0.5), 0.9),
    ("paneel", (0.30, 0.36, 0.36), 0.8), ("holz", (0.36, 0.26, 0.17), 0.5), ("papier", (0.90, 0.86, 0.78), 0.8),
    ("petrol", (0.22, 0.24, 0.25), 0.55), ("dunkel", (0.07, 0.08, 0.09), 0.5), ("metall", (0.45, 0.47, 0.48), 0.4),
    ("rahmen", (0.85, 0.82, 0.76), 0.6), ("flur", (0.8, 0.8, 0.8), 0.9), ("mint", (0.55, 0.68, 0.62), 0.7),
    ("leinwand", (0.95, 0.93, 0.9), 0.8), ("projektion", (0.98, 0.97, 0.95), 0.8), ("tafel", (0.95, 0.93, 0.9), 0.5),
    ("glas", (0.08, 0.1, 0.11), 0.3), ("kobalt", (0.1, 0.2, 0.5), 0.5), ("lamelle", (0.55, 0.68, 0.62), 0.6),
    ("band", (0.85, 0.82, 0.76), 0.7), ("himmel_oben", (0.85, 0.9, 0.9), 0.9), ("himmel_unten", (0.8, 0.86, 0.87), 0.9),
    ("hof", (0.7, 0.72, 0.7), 0.9), ("baum", (0.3, 0.45, 0.4), 0.9), ("nachbarbau", (0.85, 0.82, 0.76), 0.9),
    ("leuchte", (0.9, 0.9, 0.88), 0.8), ("kabel", (0.07, 0.08, 0.09), 0.5), ("pulli", (0.3, 0.36, 0.4), 0.8),
)}

# Lokalfarben (docs/ART_BIBLE.md §2, Zeile Lehrsaal): Wand Papier, Sockel Mint mit Holzleiste, Linoleum warm,
# Holz-Seminartisch, Petrol-Stühle und -Wagen, Liege mit Mint-Bezug, Gestelle Tinte (hier „dunkel"). Rost kommt
# im Raumrender NICHT vor: das eine Rost-Objekt ist die rote Klemme am rechten Arm des Freiwilligen (Figur Jonas).
# Kobaltblau nur in der Linealschachtel (und an Dr. Wieser). Leinwand und Whiteboard wie EKG-Papier #FFF8F4:
# die Kurven und Zeichnungen darauf kommen aus dem Code (schirme.json).
PALETTE = {
    "wand": "#F7F1E4", "boden": "#C9BDA2", "decke": "#EAE2D0", "paneel": "#BFD9CF", "holz": "#C99A5B",
    "papier": "#F7F1E4", "petrol": "#2C5560", "dunkel": "#2C3E46", "metall": "#8A9598", "rahmen": "#F7F1E4",
    "flur": "#E4DED2", "mint": "#BFD9CF", "leinwand": "#F7F1E4", "projektion": "#FFF8F4", "tafel": "#FFF8F4",
    "glas": "#1E2A30", "kobalt": "#2F5DA8", "lamelle": "#BFD9CF", "band": "#F7F1E4",
    "himmel_oben": "#EAF1F0", "himmel_unten": "#DCE9EA", "hof": "#D6DED7", "baum": "#2C5560", "nachbarbau": "#F7F1E4",
    "leuchte": "#F7F1E4", "kabel": "#2C3E46", "pulli": "#52636A",
}
HIMMEL = "#EAF1F0"
OHNE_LINIE = {"himmel_oben", "himmel_unten"}
OHNE_SCHATTIERUNG = {"himmel_oben", "himmel_unten", "hof", "baum", "nachbarbau", "projektion", "tafel", "glas",
                     "leinwand"}   # Himmel, Draußen und Schirmflächen bleiben flach
SONNE_AUS = set()


def rohr(punkte, r, m, ebene, zone=None, name="kabel"):
    """Kabel als runder Strich entlang einer glatten Kurve (Bezier -> Netz), wie figuren.Figur.rohr."""
    cu = bpy.data.curves.new("rohr", 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = r; cu.bevel_resolution = 3; cu.fill_mode = 'FULL'; cu.use_fill_caps = True; cu.resolution_u = 12
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(punkte) - 1)
    for bp, p in zip(sp.bezier_points, punkte):
        bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = 'AUTO'
    tmp = bpy.data.objects.new("rohr_tmp", cu); sc.collection.objects.link(tmp)
    bpy.context.view_layer.update()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(bpy.context.evaluated_depsgraph_get()))
    bpy.data.objects.remove(tmp, do_unlink=True); bpy.data.curves.remove(cu)
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    for p in me.polygons: p.use_smooth = True
    o.data.materials.append(m)
    return markiere(o, ebene, zone)


def torus(R, r, ort, m, ebene, zone=None, dreh=(0, 0, 0), name="torus"):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=ort, rotation=dreh, major_segments=32, minor_segments=10)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    return markiere(o, ebene, zone)


# ---------------- Raum ----------------
X0, X1, HOEHE, TIEFE = -5.4, 4.4, 3.4, 8.4
raum = raum_huelle(X0, X1, HOEHE, M["wand"], M["boden"], M["decke"], TIEFE, name="raum")
TX0, TX1, THOEHE = -4.9, -3.95, 2.1                 # Tür links, offen in den Flur
FX0, FX1, FZ0, FZ1 = 1.6, 4.0, 1.0, 2.9              # zwei hohe Seminarfenster rechts
loch(raum, (TX1 - TX0, 0.8, THOEHE), ((TX0 + TX1) / 2, 0.15, THOEHE / 2))
loch(raum, (FX1 - FX0, 0.8, FZ1 - FZ0), ((FX0 + FX1) / 2, 0.15, (FZ0 + FZ1) / 2))

# Sockel (Mint) bis 0,95 m mit Holzleiste: Rückwand links und rechts der Tür, rechte Seitenwand
PZ = 0.95
for (xa, xb, name) in ((X0, TX0 - 0.1, "links"), (TX1 + 0.1, X1, "rechts")):
    kiste((xb - xa, 0.03, PZ), ((xa + xb) / 2, -0.015, PZ / 2), M["paneel"], "hinten", fase=0, name="paneel_" + name)
    kiste((xb - xa, 0.05, 0.05), ((xa + xb) / 2, -0.025, PZ + 0.025), M["holz"], "hinten", fase=0.005, name="leiste_" + name)
kiste((0.03, 4.2, PZ), (X1 - 0.015, -2.1, PZ / 2), M["paneel"], "hinten", fase=0, name="paneel_seite")
kiste((0.05, 4.2, 0.05), (X1 - 0.025, -2.1, PZ + 0.025), M["holz"], "hinten", fase=0.005, name="leiste_seite")

# Tür: Holzzarge, Flügel steht offen im Flur, dahinter der Flur im Tageslicht (innen, keine Sonne von dort)
for x in (TX0 - 0.04, TX1 + 0.04):
    kiste((0.08, 0.06, THOEHE + 0.04), (x, -0.03, (THOEHE + 0.04) / 2), M["holz"], "hinten", "ausgang", fase=0.005, name="zarge")
kiste((TX1 - TX0 + 0.16, 0.06, 0.08), ((TX0 + TX1) / 2, -0.03, THOEHE + 0.04), M["holz"], "hinten", "ausgang", fase=0.005, name="zarge_oben")
_tw = math.radians(108)                               # Türblatt, am linken Band, 108° in den Flur geschwenkt
kiste((0.9, 0.045, THOEHE - 0.05), (TX0 + 0.45 * math.cos(_tw), 0.3 + 0.45 * math.sin(_tw), (THOEHE - 0.05) / 2),
      M["holz"], "hinten", fase=0.004, dreh=(0, 0, _tw), name="tuerblatt")
kiste((5.5, 0.1, 2.8), (-7.0, 1.7, 1.4), M["flur"], "hinten", fase=0, name="flur_wand")
kiste((6.0, 3.0, 0.05), (-6.9, 1.9, 2.725), M["flur"], "hinten", fase=0, name="flur_decke")
kiste((5.5, 0.06, 0.05), (-7.0, 1.62, 0.9), M["holz"], "hinten", fase=0.008, name="handlauf")
kiste((6.0, 1.6, 0.05), (-6.9, 0.95, -0.025), M["boden"], "hinten", fase=0, name="flur_boden")

# Kleiderhaken rechts neben der Tür mit dem Kapuzenpulli der Spielfigur (sie trägt heute den Kittel)
HX, HZ = -3.68, 1.82
kiste((0.05, 0.03, 0.08), (HX, -0.015, HZ), M["dunkel"], "hinten", fase=0.004, name="haken")
kiste((0.02, 0.05, 0.02), (HX, -0.05, HZ + 0.03), M["dunkel"], "hinten", fase=0.004, name="haken_nase")
_pk = kugel(1.0, (HX, -0.07, HZ - 0.02), M["pulli"], "hinten", name="pulli_kapuze"); _pk.scale = (0.14, 0.07, 0.11)
_pb = kiste((0.34, 0.1, 0.58), (HX + 0.02, -0.07, HZ - 0.4), M["pulli"], "hinten", fase=0.05, dreh=(0, math.radians(-4), 0), name="pulli")
_pa = kiste((0.1, 0.09, 0.42), (HX + 0.2, -0.065, HZ - 0.36), M["pulli"], "hinten", fase=0.04, dreh=(0, math.radians(-10), 0), name="pulli_aermel")

# Wanduhr rechts über der Tür (Hintergrund): Rand, Zifferblatt, Stift — die Zeiger setzt das Spiel als SVG
# aus der Klickzone "uhr" (docs/ART_BIBLE.md §7.3). Ø 0,42 m statt 0,32 m, damit die Klickzone ≥ 44 CSS-px bleibt.
UX, UZ = -3.6, 2.65
zylinder(0.21, 0.02, (UX, -0.01, UZ), M["dunkel"], "hinten", "uhr", dreh=(math.radians(90), 0, 0), name="uhr_rand")
zylinder(0.19, 0.03, (UX, -0.02, UZ), M["rahmen"], "hinten", "uhr", dreh=(math.radians(90), 0, 0), name="uhr_blatt", fase=0.004)
zylinder(0.009, 0.015, (UX, -0.04, UZ), M["dunkel"], "hinten", "uhr", dreh=(math.radians(90), 0, 0), v=12, name="uhr_stift")

# Projektionsleinwand an der Rückwand: Kasten oben (Rolle), Tuch 2,4 × 1,5 m (Unterkante 1,10 m), Gewichtsleiste
# unten; die Bildfläche (leicht eingerückt, heller: der Beamer läuft) ist die Schirmfläche "projektion".
LX, LB, LH, LZ0 = -1.2, 2.4, 1.5, 1.10
kiste((LB + 0.1, 0.09, 0.09), (LX, -0.045, LZ0 + LH + 0.045), M["dunkel"], "hinten", "projektion", fase=0.008, name="leinwand_kasten")
kiste((LB, 0.012, LH), (LX, -0.04, LZ0 + LH / 2), M["leinwand"], "hinten", "projektion", fase=0, name="leinwand_tuch")
kiste((LB + 0.02, 0.03, 0.03), (LX, -0.045, LZ0 - 0.015), M["dunkel"], "hinten", "projektion", fase=0.004, name="leinwand_leiste")
proj = kiste((LB - 0.16, 0.004, LH - 0.12), (LX, -0.048, LZ0 + LH / 2), M["projektion"], "hinten", "projektion", fase=0, name="projektion_bild")
schirmflaeche("projektion", proj, "hintergrund")

# Beamer unter der Decke, Linse zur Leinwand (die Leinwand ist seine sichtbare Lichtquelle, §3.2)
BX, BY, BZ = LX, -3.9, 3.08
zylinder(0.025, 0.26, (BX, BY, HOEHE - 0.13), M["dunkel"], "hinten", v=12, name="beamer_stange")
kiste((0.34, 0.26, 0.1), (BX, BY, BZ), M["dunkel"], "hinten", fase=0.012, name="beamer")
zylinder(0.03, 0.03, (BX + 0.08, BY + 0.14, BZ), M["glas"], "hinten", dreh=(math.radians(90), 0, 0), v=16, name="beamer_linse")
# Deckenleuchten (aus — es ist hell genug): zwei flache Paneele
for x in (-2.6, 1.4):
    kiste((1.2, 0.3, 0.012), (x, -3.2, HOEHE - 0.008), M["leuchte"], "hinten", fase=0, name="deckenleuchte")

# Fenster: dasselbe Bauteil wie in den anderen Räumen, zwei hohe Flügel; Jalousie halb oben (Lamellen schräg offen)
fenster(FX0, FX1, FZ0, FZ1, M["rahmen"], M["dunkel"], griff_z=1.9)
jalousie(FX0 + 0.03, FX1 - 0.03, FZ1 - 0.01, 1.95, M["lamelle"], M["band"], M["rahmen"], y=0.0, pitch=0.085, breite=0.075, neigung=22, schnur=0.55)
# Draußen: Hofseite am Vormittag — flache Himmelsbänder, Hofpflaster, ein Baum in Petrol, ein Nachbarflügel in
# Papier. Alles niedrig und nie im Weg der Sonne (SONNE_AUS).
AUSSEN = himmel_baender(40.0, [(-20.0, 1.2, M["hof"]), (1.2, 11.0, M["himmel_unten"]), (11.0, 40.0, M["himmel_oben"])])
AUSSEN.append(kiste((60, 40, 0.1), (0, 20.5, -0.05), M["hof"], "hinten", fase=0, name="hofboden"))
AUSSEN.append(zylinder(0.14, 1.8, (7.4, 15.0, 0.9), M["baum"], "hinten", v=12, name="baumstamm"))
for i, (bx, by, bz, br) in enumerate(((7.4, 15.0, 2.6, 1.4), (6.5, 15.3, 2.1, 1.0), (8.4, 15.2, 2.2, 1.0))):
    AUSSEN.append(kugel(br, (bx, by, bz), M["baum"], "hinten", name=f"baumkrone_{i}"))
AUSSEN.append(kiste((14.0, 3.0, 3.0), (16.0, 24.0, 1.5), M["nachbarbau"], "hinten", fase=0, name="nachbarbau"))
AUSSEN.append(kiste((14.3, 3.3, 0.14), (16.0, 24.0, 3.07), M["dunkel"], "hinten", fase=0, name="nachbar_dach"))
SONNE_AUS = {o.name for o in AUSSEN}

# Whiteboard an der rechten Seitenwand (y −0,9 … −2,9, Unterkante 0,9 m): Tafel (im Render leer, der Code zeichnet
# das Einthoven-Dreieck als SVG), Metallrahmen, Ablage mit zwei Markern und einem Schwamm. Vorderseite = lokale
# −y-Seite, um −90° gedreht, damit sie in den Raum (−x) zeigt und ebenen.py ihre vier Ecken exportiert.
WY, WZ0, WB, WH = -1.85, 0.9, 2.0, 1.2
_wd = (0, 0, math.radians(-90))
kiste((WB + 0.06, 0.03, WH + 0.06), (X1 - 0.015, WY, WZ0 + WH / 2), M["metall"], "hinten", "whiteboard", fase=0, dreh=_wd, name="tafel_rahmen")
tafel = kiste((WB, 0.004, WH), (X1 - 0.032, WY, WZ0 + WH / 2), M["tafel"], "hinten", "whiteboard", fase=0, dreh=_wd, name="tafel")
schirmflaeche("whiteboard", tafel, "hintergrund")
kiste((WB * 0.6, 0.07, 0.03), (X1 - 0.05, WY, WZ0 - 0.015), M["metall"], "hinten", "whiteboard", fase=0.004, dreh=_wd, name="tafel_ablage")
for k, (dy, m) in enumerate(((-0.35, "dunkel"), (-0.2, "petrol"))):
    zylinder(0.009, 0.13, (X1 - 0.055, WY + dy, WZ0 + 0.012), M[m], "hinten", "whiteboard", dreh=(math.radians(90), 0, math.radians(6 * k)), v=12, name="marker")
kiste((0.08, 0.05, 0.03), (X1 - 0.06, WY + 0.35, WZ0 + 0.015), M["papier"], "hinten", "whiteboard", fase=0.006, dreh=_wd, name="schwamm")

# ---------------- Mittelgrund ----------------
# Untersuchungsliege, Mitte (0,6 / −2,4), 20° gedreht, Kopfende zur Rückwand (nach links hinten: so liegt die
# linke Seite mit Tritt und Dr. Wieser zur Kamera, die rechte zum Wagen). Lokale Koordinaten: u entlang der
# Liege zum Kopfende, v quer nach links (zur Kamera-linken Seite), z Höhe. Liegefläche 0,75 m.
LC = Vector((0.6, -2.4, 0.0)); LA = math.radians(-20)
D = Vector((math.sin(LA), math.cos(LA), 0.0)); N = Vector((-math.cos(LA), math.sin(LA), 0.0))
LROT = (0, 0, -LA)


def L(u, v, z):
    p = LC + u * D + v * N
    return (p.x, p.y, z)


LIEGE_OBEN = 0.75
kiste((0.55, 1.3, 0.06), L(0, 0, 0.03), M["petrol"], "mitte", fase=0.01, dreh=LROT, name="liege_fuss")
kiste((0.32, 0.5, 0.52), L(0, 0, 0.31), M["dunkel"], "mitte", fase=0.01, dreh=LROT, name="liege_saeule")
kiste((0.62, 1.9, 0.05), L(0, 0, 0.595), M["dunkel"], "mitte", fase=0.006, dreh=LROT, name="liege_rahmen")
kiste((0.65, 1.95, 0.13), L(0, 0, LIEGE_OBEN - 0.065), M["mint"], "mitte", fase=0.03, dreh=LROT, name="liege_polster")
platte(0.52, 1.86, L(-0.02, 0, LIEGE_OBEN + 0.002), M["papier"], "mitte", dreh=LROT, name="liege_papier")
kiste((0.4, 0.3, 0.07), L(0.78, 0, LIEGE_OBEN + 0.035), M["papier"], "mitte", fase=0.03, dreh=LROT, name="kissen")
# Papierrolle am Kopfende auf zwei Haltern
zylinder(0.065, 0.56, L(1.03, 0, LIEGE_OBEN + 0.09), M["papier"], "mitte", dreh=(0, math.radians(90), -LA), name="papierrolle")
for v in (-0.3, 0.3):
    kiste((0.03, 0.03, 0.17), L(1.03, v, LIEGE_OBEN + 0.02), M["dunkel"], "mitte", fase=0.004, dreh=LROT, name="rollenhalter")
# Tritt links an der Liege, beim Kopfende (Dr. Wiesers Fuß steht darauf)
kiste((0.42, 0.45, 0.25), L(0.5, 0.325 + 0.21, 0.125), M["dunkel"], "mitte", fase=0.01, dreh=LROT, name="tritt")
kiste((0.42, 0.45, 0.012), L(0.5, 0.325 + 0.21, 0.256), M["petrol"], "mitte", fase=0, dreh=LROT, name="tritt_flaeche")
# Jonas' Schuhe stehen unter der Liege (seine Socken sind senfgelb, die Figur)
for v in (0.32, 0.19):
    kiste((0.11, 0.3, 0.09), L(-0.55, v, 0.045), M["dunkel"], "mitte", fase=0.025, dreh=LROT, name="schuh")
# Klickzonen: `liege` (ohne Figur) am Fußende, `jonas` am Kopfende — figuren_zeichnen.py vereinigt die
# Figur mit ihrer Zone und hält beide getrennt (getrennt in ebenen_figuren.aufbau)
platzhalter("liege", (0.4, 0.4, 0.25), L(-0.75, 0, LIEGE_OBEN + 0.12))
platzhalter("jonas", (0.6, 1.0, 0.3), L(0.4, 0, LIEGE_OBEN + 0.15))

# EKG-Wagen am Kopfende rechts neben der Liege, Schirm zur Kamera (gleiches Bauteil wie in der Aufnahme):
# zwei Böden auf vier Pfosten mit Rollen, Gerät mit geneigtem Schirm (dunkles Glas, Kurve aus dem Code über
# "wagen_schirm"), Papierfach vorn, Haken mit den sechs Saugelektroden (noch nicht geklebt — das ist die Aufgabe).
# Klickzone "wagen" nur Gerät, Schirm und obere Ablage: das Gestell darunter überlappte sonst das Fußende der Liege (§7.6)
WC = Vector((1.25, -1.4, 0.0)); WA = math.radians(-8)


def W(dx, dy, z):
    p = WC + Vector((dx * math.cos(WA) - dy * math.sin(WA), dx * math.sin(WA) + dy * math.cos(WA), 0.0))
    return (p.x, p.y, z)


WROT = (0, 0, WA)
kiste((0.56, 0.46, 0.05), W(0, 0, 0.92), M["petrol"], "mitte", "wagen", fase=0.012, dreh=WROT, name="wagen_boden_oben")
kiste((0.56, 0.46, 0.04), W(0, 0, 0.24), M["petrol"], "mitte", None, fase=0.012, dreh=WROT, name="wagen_boden_unten")
for dx in (-0.23, 0.23):
    for dy in (-0.18, 0.18):
        zylinder(0.012, 0.9, W(dx, dy, 0.5), M["metall"], "mitte", None, v=10, name="wagen_pfosten")
        kugel(0.035, W(dx, dy, 0.035), M["dunkel"], "mitte", None, name="wagen_rolle")
kiste((0.5, 0.36, 0.11), W(0, 0, 1.0), M["dunkel"], "mitte", "wagen", fase=0.014, dreh=WROT, name="wagen_geraet")
kiste((0.34, 0.03, 0.25), W(0, -0.12, 1.185), M["dunkel"], "mitte", "wagen", fase=0.008, dreh=(math.radians(-14), 0, WA), name="wagen_schirm_rahmen")
wschirm = kiste((0.30, 0.004, 0.19), W(0, -0.137, 1.19), M["glas"], "mitte", "wagen", fase=0, dreh=(math.radians(-14), 0, WA), name="wagen_schirm")
schirmflaeche("wagen_schirm", wschirm, "mittelgrund")
kiste((0.22, 0.02, 0.01), W(0.02, -0.19, 0.985), M["petrol"], "mitte", "wagen", fase=0, dreh=WROT, name="papierfach")
kiste((0.12, 0.08, 0.003), W(0.02, -0.22, 0.99), M["papier"], "mitte", "wagen", fase=0, dreh=(math.radians(10), 0, WA), name="streifen")
kiste((0.12, 0.003, 0.22), W(0.02, -0.262, 0.88), M["papier"], "mitte", None, fase=0, dreh=(math.radians(4), 0, WA), name="streifen_hang")
# Haken an der rechten Seite mit den Brustwand-Saugelektroden (sechs Bälle an kurzen Leitungen)
kiste((0.03, 0.06, 0.03), W(0.28, -0.02, 0.9), M["dunkel"], "mitte", None, fase=0.004, name="haken_wagen")
for k in range(6):
    dz = 0.1 + 0.035 * (k % 3); dy = -0.06 + 0.04 * (k // 3) + 0.01 * (k % 3)
    rohr([W(0.29, -0.02, 0.9), W(0.31, dy, 0.9 - dz * 0.5), W(0.3, dy, 0.9 - dz)], 0.003, M["kabel"], "mitte", None, name="saug_leitung")
    kugel(0.018, W(0.3, dy, 0.9 - dz - 0.02), M["petrol"], "mitte", None, name="saugelektrode")
# Patientenkabel: vom Gerät (linke Seite) zur Liege, dort am Kopfende die Verteilung in vier Leitungen entlang
# der Polsterkanten — zu den Extremitätenklemmen des Freiwilligen (die Klemmen gehören zur Figur Jonas; die
# Leitungsenden liegen unter seinen Armen und Beinen, damit die Figurenebene sie deckt). Ampel-Regel
# (docs/FACHREGELN.md): rot = rechter Arm und schwarz = rechtes Bein (seine rechte Seite liegt zur Kamera, lokal +v),
# gelb = linker Arm und grün = linkes Bein (zum Wagen, −v). Er liegt flach, Arme neben dem Körper, Beine gestreckt.
STAMM = [W(-0.25, 0.0, 0.96), W(-0.33, 0.0, 0.93), L(1.1, -0.4, 0.85), L(1.08, -0.3, LIEGE_OBEN + 0.015)]
rohr(STAMM, 0.007, M["kabel"], "mitte", None, name="patientenkabel")
kugel(0.02, L(1.08, -0.3, LIEGE_OBEN + 0.02), M["dunkel"], "mitte", None, name="kabelverteiler")
Z = LIEGE_OBEN + 0.012
LEITUNGEN = {
    "rot": [L(1.08, -0.3, Z), L(1.1, 0.0, Z), L(1.05, 0.33, Z), L(0.6, 0.36, Z), L(0.15, 0.36, Z), L(0.03, 0.32, Z + 0.02)],
    "gelb": [L(1.08, -0.3, Z), L(0.7, -0.36, Z), L(0.15, -0.36, Z), L(0.03, -0.32, Z + 0.02)],
    "gruen": [L(1.08, -0.3, Z), L(0.4, -0.34, Z), L(-0.5, -0.35, Z), L(-0.8, -0.2, Z + 0.02)],
    "schwarz": [L(1.08, -0.3, Z), L(0.4, -0.33, Z), L(-0.6, -0.34, Z), L(-1.0, -0.25, Z), L(-1.03, 0.08, Z), L(-0.9, 0.22, Z), L(-0.8, 0.19, Z + 0.02)],
}
for name, pts in LEITUNGEN.items():
    rohr(pts, 0.004, M["kabel"], "mitte", None, name="leitung_" + name)

# Seminartisch (Holz, 1,8 × 0,8, 0,75 m), Mitte (−2,6 / −3,2), parallel zur Rückwand; darauf die offene Schachtel
# mit den blauen Linealen (Klickzone "lineale", mit unsichtbarem Rahmen auf Fingergröße), ein Zirkel und ein
# Stapel leerer EKG-Blätter
TXM, TYM, TB, TT, TH = -2.1, -2.0, 1.8, 0.8, 0.75   # Beschreibung: (−2,6 / 3,2) — näher an Rückwand und Mitte, sonst fiele der Tisch links aus dem 28-mm-Bild
kiste((TB, TT, 0.04), (TXM, TYM, TH - 0.02), M["holz"], "mitte", fase=0.008, name="tischplatte")
kiste((TB - 0.16, TT - 0.16, 0.06), (TXM, TYM, TH - 0.07), M["dunkel"], "mitte", fase=0.006, name="tischzarge")
for dx in (-0.8, 0.8):
    for dy in (-0.32, 0.32):
        kiste((0.05, 0.05, TH - 0.1), (TXM + dx, TYM + dy, (TH - 0.1) / 2), M["dunkel"], "mitte", fase=0.004, name="tischbein")
SX0, SY0 = TXM + 0.35, TYM + 0.1
kiste((0.26, 0.2, 0.003), (SX0, SY0, TH + 0.0015), M["papier"], "mitte", "lineale", fase=0, dreh=(0, 0, math.radians(-10)), name="schachtel_boden")
for (dx, dy, bx, by) in ((0, -0.095, 0.26, 0.012), (0, 0.095, 0.26, 0.012), (-0.125, 0, 0.012, 0.2), (0.125, 0, 0.012, 0.2)):
    a = math.radians(-10); rx = dx * math.cos(a) - dy * math.sin(a); ry = dx * math.sin(a) + dy * math.cos(a)
    kiste((bx, by, 0.07), (SX0 + rx, SY0 + ry, TH + 0.035), M["papier"], "mitte", "lineale", fase=0, dreh=(0, 0, a), name="schachtel_wand")
for k in range(5):     # Lineale: flache blaue Streifen, leicht gefächert
    kiste((0.19, 0.04, 0.003), (SX0 - 0.01 + 0.004 * k, SY0 - 0.06 + 0.03 * k, TH + 0.012 + 0.004 * k), M["kobalt"], "mitte", "lineale", fase=0,
          dreh=(0, 0, math.radians(-10 + 3 * k)), name="lineal")
kiste((0.19, 0.04, 0.003), (SX0 + 0.14, SY0 - 0.2, TH + 0.0015), M["kobalt"], "mitte", "lineale", fase=0, dreh=(0, 0, math.radians(25)), name="lineal_einzeln")
platzhalter("lineale", (0.42, 0.42, 0.3), (SX0, SY0 - 0.05, TH + 0.12))
kiste((0.3, 0.21, 0.02), (TXM - 0.5, TYM - 0.05, TH + 0.01), M["papier"], "mitte", fase=0, dreh=(0, 0, math.radians(6)), name="blaetter")
# Zirkel liegt auf dem Blätterstapel, leicht gespreizt
GX, GY, GL, GW = TXM - 0.5, TYM + 0.03, 0.17, math.radians(14)      # Gelenk bei (GX, GY), Schenkel nach −y
for w in (GW, -GW):
    kiste((0.012, 0.012, GL), (GX + GL / 2 * math.sin(w), GY - GL / 2 * math.cos(w), TH + 0.028), M["metall"], "mitte", fase=0,
          dreh=(math.radians(90), 0, w), name="zirkel")
zylinder(0.016, 0.012, (GX, GY, TH + 0.028), M["metall"], "mitte", name="zirkel_gelenk")


def stuhl(x, y, dreh, zone=None, lehne_tief=0.0):
    """Seminarstuhl: Sitz und Lehne Petrol-Polster, Gestell dunkel; Lehne auf der +y-Seite (zur Rückwand)."""
    a = math.radians(dreh); c, s = math.cos(a), math.sin(a)
    def P(dx, dy, z): return (x + dx * c - dy * s, y + dx * s + dy * c, z)
    kiste((0.44, 0.44, 0.05), P(0, 0, 0.455), M["petrol"], "mitte", zone, fase=0.02, dreh=(0, 0, a), name="stuhl_sitz")
    for dx in (-0.19, 0.19):
        for dy in (-0.19, 0.19):
            zylinder(0.011, 0.43, P(dx, dy, 0.215), M["dunkel"], "mitte", zone, v=10, name="stuhl_bein")
        zylinder(0.011, 0.34, P(dx, 0.2, 0.65), M["dunkel"], "mitte", zone, v=10, dreh=(math.radians(-8), 0, a), name="stuhl_holm")
    kiste((0.44, 0.035, 0.24), P(0, 0.23, 0.71), M["petrol"], "mitte", zone, fase=0.015, dreh=(math.radians(-8), 0, a), name="stuhl_lehne")
    return P


for k, dx in enumerate((-0.68, -0.23, 0.23, 0.68)):   # vier Stühle an der Tischseite zur Kamera, der dritte um 0,4 m herausgezogen (Platz der Spielerin)
    if k == 2: stuhl(TXM + dx + 0.06, TYM - 0.4 - 0.33 - 0.4, -18)
    else: stuhl(TXM + dx, TYM - 0.4 - 0.33, 0)
# Stuhl neben der Liege, unter der Leinwand: Dr. Wiesers Jacke über der Lehne, das Stethoskop darüber (sie sitzt nicht)
SA = 200
P5 = stuhl(-1.6, -0.9, SA)
_j = kiste((0.5, 0.14, 0.42), P5(0, 0.25, 0.78), M["dunkel"], "mitte", fase=0.06, dreh=(math.radians(-8), 0, math.radians(SA)), name="jacke")
_jk = kugel(1.0, P5(0, 0.24, 0.98), M["dunkel"], "mitte", name="jacke_kragen"); _jk.scale = (0.2, 0.09, 0.05); _jk.rotation_euler = (0, 0, math.radians(SA))
rohr([P5(-0.12, 0.3, 0.96), P5(-0.14, 0.33, 0.8), P5(-0.1, 0.32, 0.62)], 0.0085, M["kabel"], "mitte", name="stethoskop")
rohr([P5(0.1, 0.3, 0.96), P5(0.13, 0.33, 0.84), P5(0.12, 0.34, 0.7)], 0.0085, M["kabel"], "mitte", name="stethoskop")
zylinder(0.024, 0.012, P5(-0.1, 0.32, 0.6), M["metall"], "mitte", dreh=(math.radians(90), 0, 0), name="bruststueck")

# Dr. Wieser steht links neben dem Kopfende der Liege, ein Fuß auf dem Tritt (Figur aus eigener Ebene)
platzhalter("wieser", (0.7, 0.01, 1.75), (-0.45, -2.05, 1.75 / 2))

# ---------------- Licht: 08:10, Vormittag, neutrales Tageslicht von rechts durch die hohen Fenster ----------------
bpy.ops.object.light_add(type='SUN'); sonne = bpy.context.object
sonne.data.energy = 12.0; sonne.data.angle = math.radians(1.0); sonne.data.color = (1.0, 0.99, 0.96)
sc.world = bpy.data.worlds.new("Welt"); sc.world.use_nodes = True


def sonne_stellen(s):
    """Vormittagssonne, ~28° hoch, von rechts hinten durchs Fenster: die beiden Flügel legen zwei helle
    Parallelogramme auf Boden, Wagen und das Kopfende der Liege (Lichtinsel auf Jonas), die halb hochgezogene
    Jalousie darüber kurze Streifen davor. Keine langen Morgenschatten."""
    s.data.energy = 12.0; s.data.angle = math.radians(0.8)
    s.rotation_euler = Vector((-0.44, -0.765, -0.47)).to_track_quat('-Z', 'Y').to_euler()


sonne_stellen(sonne)

# ---------------- Kamera: frontal, rechts der Mitte, ohne Neigung, Objektivverschiebung ----------------
bpy.ops.object.camera_add(location=(0.9, -9.0, 2.0), rotation=(math.radians(90), 0, 0))
kamera = bpy.context.object; sc.camera = kamera
kamera.data.lens = 28; kamera.data.sensor_width = 36; kamera.data.sensor_fit = 'HORIZONTAL'
sc.render.resolution_x, sc.render.resolution_y = 1600, 900
# Verschiebung: Bildmitte (x) auf 0,65 an der Rückwand — so liegen die linke Zarge der Tür und die Vorderkante
# des Whiteboards gerade noch im Bild; Bodenlinie der Rückwand (y) auf ~615 px
bpy.context.view_layer.update()
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
p = world_to_camera_view(sc, kamera, Vector((0.55, 0.0, 0.0)))
kamera.data.shift_x = p.x - 0.5
kamera.data.shift_y = (p.y - (1 - 615 / 900)) * 900 / 1600
bpy.context.view_layer.update()
