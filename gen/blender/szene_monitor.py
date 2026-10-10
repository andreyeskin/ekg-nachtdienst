"""Szene „Monitorzimmer" (09:15, heller Vormittag) — 3D-Grundlage für die Ebenen des Spiels.

Rückwand bei y=0, Kamera blickt entlang +y ohne Neigung: die Rückwand bleibt frontal, der große
Schirm ist im Bild ein exaktes Rechteck (darüber legt das Spiel die laufende Kurve). Tiefe kommt
aus dem versetzten Fluchtpunkt (Kamera rechts der Mitte, Objektivverschiebung), Tisch und Stuhl.
Rendern: python3 ebenen.py monitor alle
"""
import math

import bpy
from mathutils import Vector

from werkzeug import (fenster, himmel_baender, jalousie, kiste, kugel, leeren, loch, markiere, material, platzhalter,
                      raum_huelle, schirmflaeche, zylinder)

leeren()
sc = bpy.context.scene

# Materialien: Grauwerte nur für den Licht-Durchgang, die Bildfarbe steht in PALETTE
M = {n: material(n, c, r) for n, c, r in (
    ("wand", (0.62, 0.60, 0.55), 0.85), ("boden", (0.50, 0.48, 0.44), 0.4), ("decke", (0.5, 0.5, 0.5), 0.9),
    ("paneel", (0.30, 0.36, 0.36), 0.8), ("holz", (0.36, 0.26, 0.17), 0.5), ("papier", (0.90, 0.86, 0.78), 0.8),
    ("petrol", (0.22, 0.24, 0.25), 0.55), ("dunkel", (0.07, 0.08, 0.09), 0.5), ("metall", (0.45, 0.47, 0.48), 0.4),
    ("rahmen", (0.85, 0.82, 0.76), 0.6), ("flur", (0.8, 0.8, 0.8), 0.9), ("nachbarbau", (0.5, 0.55, 0.5), 0.9),
    ("rost", (0.5, 0.2, 0.1), 0.5), ("tasse", (0.22, 0.24, 0.25), 0.5), ("gehaeuse", (0.22, 0.24, 0.25), 0.5),
    ("schirm_gross", (0.02, 0.05, 0.04), 0.3), ("schirm_klein", (0.08, 0.1, 0.11), 0.3), ("schirm_aus", (0.08, 0.1, 0.11), 0.3),
    ("lamelle", (0.55, 0.68, 0.62), 0.6), ("band", (0.85, 0.82, 0.76), 0.7), ("polster", (0.22, 0.24, 0.25), 0.7),
    ("himmel_oben", (0.8, 0.85, 0.9), 0.9), ("himmel_unten", (0.85, 0.9, 0.92), 0.9), ("rasen", (0.5, 0.6, 0.45), 0.9),
    ("hecke", (0.45, 0.6, 0.52), 0.9), ("nachbar_fenster", (0.08, 0.1, 0.11), 0.3),
)}

# Lokalfarben (docs/ART_BIBLE.md §2): das Monitorzimmer ist der kühle Raum — Mint hell an den Wänden, Sand als
# Sockel (Umkehrung der Aufnahme), kühles Linoleum, Petrol für Geräte, Holz nur am Schrank und an der Zarge;
# Rost genau einmal (Falks Zirkel). Schirme: der große wie EKG-Papier (#FFF8F4, die Kurve zeichnet das Spiel),
# die Bettmonitore dunkles Glas (#1E2A30), ihre Kurven kommen ebenfalls aus dem Code (schirme.json).
PALETTE = {
    "wand": "#D6E4DD", "boden": "#B6BFB6", "decke": "#E3E6DD", "paneel": "#EFE6D3", "holz": "#C99A5B",
    "papier": "#F7F1E4", "petrol": "#2C5560", "dunkel": "#2C3E46", "metall": "#8A9598", "rahmen": "#F7F1E4",
    "flur": "#D6DED7", "nachbarbau": "#BFD9CF", "rost": "#B5552D", "tasse": "#2C5560",
    "gehaeuse": "#2C3E46", "schirm_gross": "#FFF8F4", "schirm_klein": "#1E2A30", "schirm_aus": "#2C3E46",
    "lamelle": "#BFD9CF", "band": "#F7F1E4", "polster": "#2C5560",
    "himmel_oben": "#DCE9EA", "himmel_unten": "#E6EFEE", "rasen": "#CFD9C2", "hecke": "#9FC2B3",
    "nachbar_fenster": "#1E2A30",
}
HIMMEL = "#E6EFEE"
OHNE_LINIE = {"himmel_oben", "himmel_unten"}
OHNE_SCHATTIERUNG = {"himmel_oben", "himmel_unten", "schirm_gross", "schirm_klein", "schirm_aus", "hecke", "rasen",
                     "nachbarbau", "nachbar_fenster"}   # Himmel, Draußen und Schirme bleiben flach
SONNE_AUS = set()

# ---------------- Raum ----------------
X0, X1, HOEHE = -5.6, 4.1, 3.2
raum = raum_huelle(X0, X1, HOEHE, M["wand"], M["boden"], M["decke"], 6.8, name="raum")
# Tür (Ausgang zurück in die Aufnahme) ganz links, Fenster rechts daneben
TX0, TX1, THOEHE = -5.0, -4.05, 2.1
FX0, FX1, FZ0, FZ1 = -3.7, -2.45, 1.25, 2.50   # Sturz knapp über Augenhöhe: Laibung oben nur eine Linie
loch(raum, (TX1 - TX0, 0.8, THOEHE), ((TX0 + TX1) / 2, 0.15, THOEHE / 2))
loch(raum, (FX1 - FX0, 0.8, FZ1 - FZ0), ((FX0 + FX1) / 2, 0.15, (FZ0 + FZ1) / 2))

# Sockel (Sand) unten an Rück- und rechter Wand, Holzleiste darüber — wie in der Aufnahme, Farben vertauscht
PZ = 0.95
kiste((TX0 - 0.1 - X0, 0.03, PZ), ((X0 + TX0 - 0.1) / 2, -0.015, PZ / 2), M["paneel"], "hinten", fase=0, name="paneel_links")
kiste((TX0 - 0.1 - X0, 0.05, 0.05), ((X0 + TX0 - 0.1) / 2, -0.025, PZ + 0.025), M["holz"], "hinten", fase=0.005, name="leiste_links")
kiste((X1 - TX1 - 0.1, 0.03, PZ), ((TX1 + 0.1 + X1) / 2, -0.015, PZ / 2), M["paneel"], "hinten", fase=0, name="paneel")
kiste((X1 - TX1 - 0.1, 0.05, 0.05), ((TX1 + 0.1 + X1) / 2, -0.025, PZ + 0.025), M["holz"], "hinten", fase=0.005, name="leiste")
kiste((0.03, 2.0, PZ), (X1 - 0.015, -1.0, PZ / 2), M["paneel"], "hinten", fase=0, name="paneel_rechts")
kiste((0.05, 2.0, 0.05), (X1 - 0.025, -1.0, PZ + 0.025), M["holz"], "hinten", fase=0.005, name="leiste_rechts")

# Tür: Holzzarge, dahinter der Flur im Tageslicht
for x in (TX0 - 0.04, TX1 + 0.04):
    kiste((0.08, 0.06, THOEHE + 0.04), (x, -0.03, (THOEHE + 0.04) / 2), M["holz"], "hinten", "ausgang", fase=0.005, name="zarge")
kiste((TX1 - TX0 + 0.16, 0.06, 0.08), ((TX0 + TX1) / 2, -0.03, THOEHE + 0.04), M["holz"], "hinten", "ausgang", fase=0.005, name="zarge_oben")
# Flur hinter der Tür, mit tiefer Decke: er ist innen, durch die Tür fällt keine Sonne. Die Rückwand des
# Flurs endet bei x=-4.7 (weiter rechts sähe man sie durchs Fenster), die Decke über der Tür hält das Licht ab.
kiste((5.3, 0.1, 2.8), (-7.35, 1.65, 1.4), M["flur"], "hinten", fase=0, name="flur_wand")
kiste((5.95, 3.2, 0.05), (-7.025, 1.9, 2.725), M["flur"], "hinten", fase=0, name="flur_decke")
kiste((5.3, 0.06, 0.05), (-7.35, 1.57, 0.9), M["holz"], "hinten", fase=0.008, name="handlauf")
kiste((5.95, 1.5, 0.05), (-7.025, 0.95, -0.025), M["boden"], "hinten", fase=0, name="flur_boden")

# Fenster: dasselbe Bauteil wie in der Aufnahme (Blendrahmen in der Laibung, zwei Flügel, Griff, Fensterbank),
# die Jalousie am Vormittag ganz hochgezogen (Kasten mit gestapelten Lamellen). Draußen: Rasen, der Nachbarflügel
# der Klinik (Mint, mit Fensterreihe) und Bäume unter einem kühlen Himmel in zwei Bändern.
fenster(FX0, FX1, FZ0, FZ1, M["rahmen"], M["dunkel"], griff_z=1.75)
jalousie(FX0 + 0.03, FX1 - 0.03, FZ1 - 0.01, FZ1 - 0.01 - 0.08 - 0.11, M["lamelle"], M["band"], M["rahmen"], y=0.0, pitch=0.032, breite=0.075, neigung=0, schnur=0.6)
AUSSEN = himmel_baender(40.0, [(-20.0, 9.0, M["himmel_unten"]), (9.0, 30.0, M["himmel_oben"])])
# Kamera 0,8/-7,4/2,45 blickt leicht nach unten: durchs Fenster sieht man den Hof — Rasen, eine Hecke, dahinter
# die Fassade des Nachbarflügels (Mint) mit dunkler Fensterreihe; Bäume wären hier nur abgeschnittene Kronen.
# Nichts davon steht im Weg der Sonne.
AUSSEN.append(kiste((60, 40, 0.1), (0, 20.5, -0.05), M["rasen"], "hinten", fase=0, name="rasen"))
AUSSEN.append(kiste((30, 0.6, 1.0), (-8.0, 14.0, 0.5), M["hecke"], "hinten", fase=0.08, name="hecke"))
AUSSEN.append(kiste((16.0, 3.0, 3.0), (-11.0, 21.5, 1.5), M["nachbarbau"], "hinten", fase=0, name="nachbarbau"))
AUSSEN.append(kiste((16.3, 3.3, 0.16), (-11.0, 21.5, 3.08), M["dunkel"], "hinten", fase=0, name="nachbar_dach"))
for i in range(10):
    AUSSEN.append(kiste((0.9, 0.05, 1.0), (-18.0 + i * 1.6, 19.97, 1.7), M["nachbar_fenster"], "hinten", fase=0, name=f"nachbar_fenster_{i}"))
SONNE_AUS = {o.name for o in AUSSEN}

# ---------------- Bildschirmwand: der große Schirm (Papierstreifen der Engine) und drei gleiche Bettmonitore
# in einer Reihe darüber (Bett 1–3, Kurven aus dem Code), rechts ein vierter Monitor ohne Bett: aus ----------------
RAND = 0.07


def monitor(sx, sz, sb, sh, farbe, zone, name, abstand=0.14, tief=0.06):
    d = (0, 0, 0)   # flach an der Wand: so bleibt die Bildfläche im Bild ein exaktes Rechteck
    kiste((0.12, abstand, 0.12), (sx, -abstand / 2, sz), M["dunkel"], "hinten", fase=0, name="halter")
    kiste((sb + 2 * RAND, tief, sh + 2 * RAND), (sx, -abstand - tief / 2, sz), M["gehaeuse"], "hinten", zone, fase=0.012, dreh=d, name="gehaeuse")
    return kiste((sb, 0.006, sh), (sx, -abstand - tief - 0.003, sz), M[farbe], "hinten", zone, fase=0, dreh=d, name=name)


gross = monitor(0.0, 1.50, 1.70, 0.96, "schirm_gross", "schirm", "schirm_bild", abstand=0.10, tief=0.07)
markiere(gross, None, "schirm_bild")   # Bildfläche: dort liegt im Spiel die laufende Kurve (Papierstil)
schirmflaeche("gross", gross, "hintergrund")
for i, sx in enumerate((-1.05, 0.0, 1.05)):
    schirmflaeche(f"bett_{i + 1}", monitor(sx, 2.36, 0.82, 0.5, "schirm_klein", "schirme_klein", f"schirm_bett_{i + 1}"), "hintergrund")
monitor(2.45, 2.2, 0.62, 0.38, "schirm_aus", None, "schirm_aus")

# ---------------- Mittelgrund: Arbeitsplatz ----------------
TI0, TI1, TT, TH = -2.75, 1.75, 0.85, 0.75     # Tisch von x..x, Tiefe, Höhe
kiste((TI1 - TI0, TT, 0.04), ((TI0 + TI1) / 2, -TT / 2, TH - 0.02), M["papier"], "mitte", "tisch", fase=0.012, name="tischplatte")
for x in (TI0 + 0.25, TI1 - 0.25):   # zwei Schubladenblöcke
    kiste((0.46, TT - 0.08, TH - 0.06), (x, -TT / 2 + 0.02, (TH - 0.06) / 2 + 0.01), M["petrol"], "mitte", "tisch", fase=0.01, name="block")
    for k in range(3):
        kiste((0.40, 0.01, 0.005), (x, -TT + 0.055, 0.17 + k * 0.21), M["dunkel"], "mitte", "tisch", fase=0, name="griff")
kiste((TI1 - TI0 - 1.0, 0.03, 0.42), ((TI0 + TI1) / 2, -0.12, TH - 0.27), M["holz"], "mitte", "tisch", fase=0.005, name="sichtblende")
# Tastatur und Maus vor dem großen Schirm
kiste((0.46, 0.16, 0.025), (-0.05, -0.42, TH + 0.013), M["dunkel"], "mitte", "tisch", fase=0.006, dreh=(0, 0, math.radians(-2)), name="tastatur")
kiste((0.06, 0.10, 0.03), (0.33, -0.43, TH + 0.015), M["dunkel"], "mitte", "tisch", fase=0.012, name="maus")
# Falks Platz am rechten Tischende: kalter Kaffee (Petrol), Zirkel (Rost) auf einem leeren Blatt
kiste((0.30, 0.21, 0.004), (1.02, -0.52, TH + 0.002), M["papier"], "mitte", "tisch", fase=0, dreh=(0, 0, math.radians(8)), name="blatt")
zylinder(0.045, 0.10, (1.45, -0.46, TH + 0.05), M["tasse"], "mitte", "tisch", name="tasse")
zylinder(0.022, 0.01, (1.42, -0.46, TH + 0.10), M["dunkel"], "mitte", "tisch", name="kaffee")
# Zirkel steht auf seinen Spitzen, leicht gespreizt — so liest er sich auch klein als Zirkel
GX, GY, GL, GW = 0.98, -0.55, 0.18, math.radians(16)
GZ = TH + GL * math.cos(GW)                                # Gelenk oben, Spitzen auf dem Blatt
for w in (GW, -GW):
    kiste((0.016, 0.012, GL), (GX + GL / 2 * math.sin(w), GY, TH + GL / 2 * math.cos(w)), M["rost"], "mitte", "tisch",
          fase=0, dreh=(0, -w, 0), name="zirkel")
zylinder(0.02, 0.016, (GX, GY, GZ), M["rost"], "mitte", "tisch", dreh=(math.radians(90), 0, 0), name="zirkel_gelenk")
zylinder(0.007, 0.035, (GX, GY, GZ + 0.03), M["rost"], "mitte", "tisch", v=12, name="zirkel_griff")

# Drehstuhl vor dem Tisch, Lehne zur Kamera (Polster Petrol, Gestell dunkel)
SX, SY, SD = -0.62, -1.45, math.radians(12)
for k in range(5):
    a = SD + k * 2 * math.pi / 5
    kiste((0.30, 0.05, 0.035), (SX + 0.15 * math.cos(a), SY + 0.15 * math.sin(a), 0.07), M["dunkel"], "mitte", fase=0.008,
          dreh=(0, 0, a), name="stuhlfuss")
    kugel(0.03, (SX + 0.29 * math.cos(a), SY + 0.29 * math.sin(a), 0.03), M["dunkel"], "mitte", name="rolle")
zylinder(0.03, 0.36, (SX, SY, 0.27), M["metall"], "mitte", name="stuhlsaeule", v=16)
kiste((0.50, 0.48, 0.08), (SX, SY, 0.49), M["polster"], "mitte", fase=0.03, dreh=(0, 0, SD), name="sitz")
def hinter_sitz(abstand):   # Punkt hinter der Sitzmitte (zur Kamera hin), mit dem Stuhl gedreht
    return SX + abstand * math.sin(SD), SY - abstand * math.cos(SD)


# Stütze und Lehne stehen hinter der Sitzkante (0,24 m) — ragen sie darüber, werfen sie Schatten auf den Sitz
kiste((0.04, 0.04, 0.30), (*hinter_sitz(0.26), 0.62), M["dunkel"], "mitte", fase=0.008, dreh=(0, 0, SD), name="lehnenstuetze")
kiste((0.46, 0.07, 0.46), (*hinter_sitz(0.32), 0.92), M["polster"], "mitte", fase=0.03, dreh=(math.radians(6), 0, SD), name="lehne")   # leicht nach hinten geneigt

# Aktenschrank (Holz, Ordner der Monitorbefunde) an der rechten Wand: vier Schubladen mit Griffmulden
kiste((0.45, 0.9, 1.95), (X1 - 0.24, -1.15, 0.975), M["holz"], "mitte", fase=0.01, name="schrank")
kiste((0.46, 0.9, 0.03), (X1 - 0.24, -1.15, 1.965), M["dunkel"], "mitte", fase=0.004, name="schrank_deckel")
for k in range(4):
    kiste((0.01, 0.8, 0.005), (X1 - 0.47, -1.15, 0.45 + k * 0.45), M["dunkel"], "mitte", fase=0, name="schrankfuge")
    kiste((0.012, 0.16, 0.025), (X1 - 0.47, -1.15, 0.62 + k * 0.45), M["dunkel"], "mitte", fase=0.003, name="schrankgriff")

# Wanduhr über dem Aktenschrank, neben dem rechten kleinen Schirm — Zifferblatt und Stift ohne Zeiger:
# die Zeiger setzt das Spiel als Overlay aus der Klickzone "uhr" (docs/ART_BIBLE.md §7.3)
UX, UZ = 3.68, 2.42
zylinder(0.21, 0.02, (UX, -0.01, UZ), M["dunkel"], "hinten", "uhr", dreh=(math.radians(90), 0, 0), name="uhr_rand")
zylinder(0.19, 0.03, (UX, -0.02, UZ), M["rahmen"], "hinten", "uhr", dreh=(math.radians(90), 0, 0), name="uhr_blatt", fase=0.004)
zylinder(0.009, 0.015, (UX, -0.04, UZ), M["dunkel"], "hinten", "uhr", dreh=(math.radians(90), 0, 0), v=12, name="uhr_stift")

# Dr. Falk steht rechts vom großen Schirm, frei auf dem Boden (Figur kommt aus eigener Ebene)
platzhalter("falk", (0.74, 0.01, 1.87), (2.36, -0.80, 1.87 / 2))

# ---------------- Licht: 09:15, kühles Tageslicht durchs Fenster ----------------
bpy.ops.object.light_add(type='SUN'); sonne = bpy.context.object
sonne.data.energy = 12.0; sonne.data.angle = math.radians(1.0); sonne.data.color = (0.95, 0.98, 1.0)
# Vormittagssonne, ~35° hoch, fast gerade von hinten: das Fenster wirft sein Kreuz vor das linke Tischende
sonne.rotation_euler = Vector((0.25, -0.75, -0.6)).to_track_quat('-Z', 'Y').to_euler()
sc.world = bpy.data.worlds.new("Welt"); sc.world.use_nodes = True

# ---------------- Kamera: frontal, rechts der Mitte, leicht erhöht, ohne Neigung ----------------
bpy.ops.object.camera_add(location=(0.8, -7.4, 2.45), rotation=(math.radians(90), 0, 0))
kamera = bpy.context.object; sc.camera = kamera
kamera.data.lens = 28; kamera.data.sensor_width = 36; kamera.data.sensor_fit = 'HORIZONTAL'
sc.render.resolution_x, sc.render.resolution_y = 1600, 900
# Objektivverschiebung: großer Schirm in die Bildmitte (x), Bodenlinie der Figur auf ~705 px (y)
bpy.context.view_layer.update()
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
p = world_to_camera_view(sc, kamera, Vector((0.0, 0.0, 1.50)))
kamera.data.shift_x = p.x - 0.5
kamera.data.shift_y = (p.y - (1 - 400 / 900)) * 900 / 1600
bpy.context.view_layer.update()
