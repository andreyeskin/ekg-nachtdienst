"""Blockout „Haus Föhrenhang" (docs/KRANKENHAUS.md, Konzept §2–§5, §9) — Kubatur, Räume, Umgebung, Probe-Renders.

    python3 gen/blender/haus_blockout.py bauen            baut die Szene, speichert bau/blender/haus/haus_blockout.blend + .glb
    python3 gen/blender/haus_blockout.py render aussen    Probe-Render (a): Außenansicht 06:40  -> docs/haus/probe_aussen.jpg
    python3 gen/blender/haus_blockout.py render flur      Probe-Render (b): Flur 1. OG 09:15    -> docs/haus/probe_flur.jpg
    python3 gen/blender/haus_blockout.py grundriss eg|1og|2og|alle   Draufsicht (orthografisch) -> docs/haus/grundriss_<g>.png

Alle Maße stehen in den Tabellen oben (Meter, lokale Koordinaten nach KRANKENHAUS §2: Ursprung Südwestecke des
Altbaus am EG-Boden, +x entlang des Riegels nach Nordost, +y nach Nordwest, +z nach oben). Eine Maßänderung ist eine
Zeile in einer Tabelle. Räume sind Quader (Bodenplatte mit Raumnamen + Wände mit Tür- und Fensteröffnungen), Möbel nur
grobe Klötze im Probe-Flur, Bäume aus Stamm und Kugel-Kronen bzw. Kegel-Etagen (Wald hinten als Silhouettenbänder),
Stadt im Tal eine ferne Kulisse (Südost unsichtbar, Nordost-Talbiegung im Bild von Kamera (a)).

Render: Fläche (Lokalfarbe, Stufen nach Flächenrichtung), Sonne (nur direktes Licht, grau) und Freestyle-Linie wie in
ebenen.py, zusammengesetzt mit komposit.py — ohne die Ebenen-Trennung (kein Mittelgrund, keine Klickzonen); die
Ebenen-Pipeline bleibt unverändert. Jeder Durchgang lädt die .blend neu (die Durchgänge verändern die Materialien).
"""
import math
import os
import random
import subprocess
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(HIER))
BAU = os.path.join(WURZEL, "bau", "blender", "haus") + os.sep
DOCS = os.path.join(WURZEL, "docs", "haus") + os.sep
BLEND = BAU + "haus_blockout.blend"

# ======================================================================================================
# Tabellen (KRANKENHAUS §2–§5). Rechtecke (x0, y0, x1, y1) als Achsmaße, Wände liegen innerhalb.
# ======================================================================================================
A = dict(x0=0.0, x1=61.2, y0=0.0, y1=16.0, geschosse=3, aussen=0.45, innen=0.15)    # Trakt A, Altbau
RISALIT_SE = (25.2, -3.0, 36.0, 0.0)          # Mittelrisalit, alle Geschosse, Quergiebel
RISALIT_NW = (25.2, 16.0, 30.6, 19.0)         # Treppenhausrisalit, kleiner Walm
N = dict(x0=61.2, x1=85.2, y0=-6.0, y1=18.0, geschosse=2, aussen=0.45, innen=0.15)  # Trakt N, Neubau (Flachdach)
VORDACH = dict(x0=85.2, x1=91.2, y0=-6.0, y1=4.0, unterkante=3.6, dicke=0.4)
GESCHOSS = 4.0                                 # Geschosshöhe beider Trakte
RAUMHOEHE = {"A": 3.4, "N": 3.0}              # Raumhöhe (darüber Decke bzw. Installationsraum)
DACH = dict(neigung=30.0, traufe=12.0, first_y=8.0, ueberstand=0.6, kamine=(12.0, 30.6, 48.0))
ATTIKA_N = 1.1                                 # Dachgarten Trakt N, z 8 … 9,1
SOCKEL = 0.6                                   # sichtbar an der SE-Seite (Gelände dort z −0,6)
ACHSE, ACHSEN = 3.6, 17                        # Fensterachsen Altbau: Mitte x = 3,6·k − 1,8
FENSTER = dict(b=1.4, h=2.2, bruestung=0.9)    # Altbau-Fenster
FLUR = (7.0, 10.0)                             # Flur y 7 … 10 in allen Geschossen
TUER = dict(zimmer=1.0, patient=1.25, doppel=1.8, h=2.1)
PORTAL = dict(x0=29.1, x1=32.1, h=3.2)
RETTUNGSTOR = dict(y0=-5.0, y1=-2.0, h=2.8)
AUFNAHME_GLAS = dict(y0=2.0, y1=12.0, h=3.0)   # Fensterfront NE x 85,2

# Türen: (Wandachse "x"|"y", Lage der Wand, Mitte entlang der Wand, Breite, Art).
# Art: "zu" (Blatt Petrol), "auf" (offen, Blatt in den Raum geschwenkt), "glas" (Glasfläche), "offen" (Wand fehlt dort).
def T(achse, wand, mitte, breite=TUER["zimmer"], art="zu"):
    return (achse, wand, mitte, breite, art)


# Räume je Geschoss: (Name, x0, y0, x1, y1, Boden, Türen). Boden = Materialname (ART_BIBLE §2).
def patientenzimmer(nummern, y0, y1, k0, art="zu", breite=TUER["patient"]):
    """Zimmer an den Achsen k0, k0+1, …: Tür in der Flurwand bei x = 3,6·k − 0,7."""
    aus = []
    for i, nr in enumerate(nummern):
        k = k0 + i
        x0, x1 = ACHSE * (k - 1), ACHSE * k
        wand = y1 if y0 < FLUR[0] else y0          # Flurwand: y 7 (Südostseite) oder y 10 (Nordwestseite)
        aus.append((f"Zimmer {nr}", x0, y0, x1, y1, "lino_warm", [T("y", wand, ACHSE * k - 0.7, breite, art)]))
    return aus


RAEUME = {
    "EG": [
        ("Lehrsaal", 0, 0, 10.8, 7, "lino_warm", [T("y", 7, 9.8)]),
        ("Garderobe Lehre", 10.8, 0, 14.4, 7, "lino_warm", [T("y", 7, 12.6)]),
        ("Ambulanz Innere", 14.4, 0, 21.6, 7, "lino_warm", [T("y", 7, 16)]),
        ("Portier", 21.6, 0, 25.2, 7, "lino_warm", [T("x", 25.2, 3.5, 2.0, "glas")]),
        ("Eingangshalle", 25.2, -3, 36, 10, "lino_warm", [T("y", -3, (PORTAL["x0"] + PORTAL["x1"]) / 2, PORTAL["x1"] - PORTAL["x0"], "glas"),
                                                       T("y", 7, 30.6, 10.8, "offen")]),
        ("Rhythmusambulanz Warten", 36, 0, 39.6, 7, "lino_warm", [T("y", 7, 37.8, art="glas")]),
        ("Rhythmusambulanz Untersuchung", 39.6, 0, 46.8, 7, "lino_warm", [T("y", 7, 41), T("x", 46.8, 3.5)]),
        ("Rhythmusambulanz Arztzimmer", 46.8, 0, 50.4, 7, "lino_warm", [T("y", 7, 48)]),
        ("Holter Ergometrie", 50.4, 0, 54, 7, "lino_warm", [T("y", 7, 52.2)]),
        ("Sanitaer Besucher", 54, 0, 57.6, 7, "lino_kuehl", [T("y", 7, 55.8)]),
        ("Lager EG", 57.6, 0, 61.2, 7, "lino_kuehl", [T("y", 7, 59.4)]),
        ("Sekretariat Lehre", 0, 10, 7.2, 16, "lino_warm", [T("y", 10, 2)]),
        ("Umkleide Studierende", 7.2, 10, 10.8, 16, "lino_kuehl", [T("y", 10, 9)]),
        ("Technik Lager EG", 10.8, 10, 18, 16, "lino_kuehl", [T("y", 10, 14.4)]),
        ("Sozialraum", 18, 10, 25.2, 16, "lino_warm", [T("y", 10, 20)]),
        ("Treppenhaus S1", 25.2, 10, 30.6, 19, "lino_kuehl", [T("y", 10, 27.9, TUER["doppel"], "auf")]),
        ("Lifte L1", 30.6, 10, 36, 13.5, "lino_kuehl", [T("y", 10, 32.0, 1.4, "zu"), T("y", 10, 34.6, 1.1, "zu")]),
        ("Technik Lift", 30.6, 13.5, 36, 16, "lino_kuehl", [T("x", 30.6, 14.75)]),
        ("Cafeteria", 36, 10, 50.4, 16, "lino_warm", [T("y", 10, 40, art="glas"), T("y", 16, 45, TUER["doppel"], "glas")]),
        ("Kueche Ausgabe", 50.4, 10, 54, 16, "lino_kuehl", [T("x", 50.4, 13)]),
        ("Fluchttreppe S2", 54, 10, 57.6, 16, "lino_kuehl", [T("y", 10, 55.8)]),
        ("Bettenlift L2", 57.6, 10, 61.2, 13.5, "lino_kuehl", [T("y", 10, 59.4, 1.4)]),
        ("Flur EG", 0, 7, 61.2, 10, "lino_warm", [T("x", 61.2, 8.5, TUER["doppel"], "glas")]),
        ("Flur N EG", 61.2, 7, 66, 10, "lino_kuehl", [T("x", 66, 8.5, TUER["doppel"], "glas")]),
        ("Wartebereich Notaufnahme", 61.2, 10, 66, 14, "lino_kuehl", [T("y", 10, 63.6, 4.3, "offen")]),
        ("Fluchttreppe S3", 61.2, 14, 66, 18, "lino_kuehl", [T("y", 14, 63.6)]),
        ("Vorraum Schockraum", 61.2, 2, 66, 7, "lino_kuehl", [T("y", 7, 63.6, 4.3, "offen")]),
        ("Schockraum", 61.2, -6, 70, 2, "lino_kuehl", [T("y", 2, 67, TUER["doppel"], "glas"), T("x", 70, 0, 1.25)]),
        ("Aufnahme", 66, -2, 85.2, 14, "lino_warm", [T("y", -2, 77, 2.0, "glas")]),
        ("Triage Rettungsschleuse", 70, -6, 85.2, -2, "lino_kuehl", []),
        ("Dienstzimmer Notaufnahme", 66, 14, 72, 18, "lino_kuehl", [T("y", 14, 69)]),
        ("Medikamente Arbeitsraum", 72, 14, 79, 18, "lino_kuehl", [T("y", 14, 75.5)]),
        ("Sanitaer Umkleide N", 79, 14, 85.2, 18, "lino_kuehl", [T("y", 14, 82)]),
    ],
    "1OG": [
        *patientenzimmer((101, 102, 103, 104, 105, 106), 0, 7, 1),
        ("Zimmer 107", 21.6, 0, 25.2, 7, "lino_warm", [T("y", 7, 24.5, TUER["patient"])]),
        ("Stuetzpunkt Station 1", 25.2, -3, 30.6, 7, "lino_warm", [T("y", 7, 27.9, 5.4, "offen")]),
        ("Dienstzimmer Aerzte Station 1", 30.6, 0, 36, 7, "lino_warm", [T("y", 7, 34)]),
        *patientenzimmer((108, 109, 110, 111, 112), 0, 7, 11, art="auf"),
        ("Bad Station", 54, 0, 57.6, 7, "lino_kuehl", [T("y", 7, 55.8)]),
        ("Lager unrein", 57.6, 0, 61.2, 7, "lino_kuehl", [T("y", 7, 59.4)]),
        *patientenzimmer((113, 114, 115, 116), 10, 16, 1),
        ("Pflegearbeitsraum rein", 14.4, 10, 18, 16, "lino_kuehl", [T("y", 10, 16.2)]),
        ("Pflegearbeitsraum unrein", 18, 10, 21.6, 16, "lino_kuehl", [T("y", 10, 19.8)]),
        ("Waesche Lager", 21.6, 10, 25.2, 16, "lino_kuehl", [T("y", 10, 23.4)]),
        ("Treppenhaus S1", 25.2, 10, 30.6, 19, "lino_kuehl", [T("y", 10, 27.9, TUER["doppel"], "auf")]),
        ("Lifte L1", 30.6, 10, 36, 13.5, "lino_kuehl", [T("y", 10, 32.0, 1.4, "zu"), T("y", 10, 34.6, 1.1, "zu")]),
        ("Lager L1", 30.6, 13.5, 36, 16, "lino_kuehl", [T("x", 30.6, 14.75)]),
        ("Monitorzimmer", 36, 10, 46.8, 16, "lino_kuehl", [T("y", 10, 37.5, 2.2, "glas")]),
        *patientenzimmer((117, 118), 10, 16, 14),
        ("Fluchttreppe S2", 54, 10, 57.6, 16, "lino_kuehl", [T("y", 10, 55.8)]),
        ("Bettenlift L2", 57.6, 10, 61.2, 13.5, "lino_kuehl", [T("y", 10, 59.4, 1.4)]),
        ("Flur 1OG", 0, 7, 61.2, 10, "lino_warm", [T("x", 61.2, 8.5, TUER["doppel"], "glas")]),
        ("Flur N 1OG", 61.2, 7, 85.2, 10, "lino_kuehl", []),
        ("Technik N", 61.2, -6, 66, 7, "lino_kuehl", [T("y", 7, 63.6)]),
        ("Herzkatheterlabor", 66, -6, 74.4, 1, "lino_kuehl", [T("y", 1, 70, TUER["doppel"], "glas")]),
        ("Schaltraum HKL", 74.4, -6, 78, 1, "lino_kuehl", [T("y", 1, 76.2), T("x", 74.4, -2.5, 2.0, "glas")]),
        ("Vorbereitung Schleuse", 66, 1, 78, 7, "lino_kuehl", [T("y", 7, 72, TUER["doppel"])]),
        ("Arztzimmer Herzkatheter", 78, -6, 85.2, 0, "lino_warm", [T("y", 0, 81.6)]),
        ("Befundung Umkleide HKL", 78, 0, 85.2, 7, "lino_kuehl", [T("y", 7, 81.6)]),
        ("Warten Angehoerige", 61.2, 10, 66, 14, "lino_kuehl", [T("y", 10, 63.6, 4.3, "offen")]),
        ("Fluchttreppe S3", 61.2, 14, 66, 18, "lino_kuehl", [T("y", 14, 63.6)]),
        ("Chest Pain Unit", 66, 10, 85.2, 18, "lino_kuehl", [T("y", 10, 68, 2.2, "glas")]),
    ],
    "2OG": [
        *patientenzimmer((201, 202, 203), 0, 7, 1),
        ("Aufwachraum Innere", 10.8, 0, 21.6, 7, "lino_kuehl", [T("y", 7, 12, TUER["doppel"], "glas")]),
        ("Stuetzpunkt Innere", 21.6, 0, 25.2, 7, "lino_warm", [T("y", 7, 23.4, 3.3, "offen")]),
        ("Befundraum", 25.2, -3, 30.6, 7, "lino_warm", [T("y", 7, 29), T("x", 30.6, 3.5)]),
        ("Dienstzimmer Nachtdienst", 30.6, 0, 36, 7, "lino_warm", [T("y", 7, 34)]),
        *[(f"Intensiv Box {i + 1}", 36 + 3.6 * i, 0, 39.6 + 3.6 * i, 7, "lino_kuehl", [T("y", 7, 3.6 * (11 + i) - 1.8, 1.6, "glas")]) for i in range(5)],
        ("Sanitaer Technik Intensiv", 54, 0, 57.6, 7, "lino_kuehl", [T("y", 7, 55.8)]),
        ("Entsorgung", 57.6, 0, 61.2, 7, "lino_kuehl", [T("y", 7, 59.4)]),
        *patientenzimmer((204, 205, 206, 207), 10, 16, 1),
        ("Pflegearbeitsraum 2OG", 14.4, 10, 18, 16, "lino_kuehl", [T("y", 10, 16.2)]),
        ("Lager 2OG", 18, 10, 21.6, 16, "lino_kuehl", [T("y", 10, 19.8)]),
        ("Arztzimmer Innere", 21.6, 10, 25.2, 16, "lino_warm", [T("y", 10, 23.4)]),
        ("Treppenhaus S1", 25.2, 10, 30.6, 19, "lino_kuehl", [T("y", 10, 27.9, TUER["doppel"], "auf")]),
        ("Lifte L1", 30.6, 10, 36, 13.5, "lino_kuehl", [T("y", 10, 32.0, 1.4, "zu"), T("y", 10, 34.6, 1.1, "zu")]),
        ("Lager L1", 30.6, 13.5, 36, 16, "lino_kuehl", [T("x", 30.6, 14.75)]),
        ("Intensiv Zentrale", 36, 10, 43.2, 16, "lino_kuehl", [T("y", 10, 39.6, 7.2, "offen")]),
        ("Intensiv Box 6", 43.2, 10, 50.4, 16, "lino_kuehl", [T("y", 10, 45, 1.6, "glas")]),
        ("Angehoerigenraum", 50.4, 10, 54, 16, "lino_warm", [T("y", 10, 52.2)]),
        ("Fluchttreppe S2", 54, 10, 57.6, 16, "lino_kuehl", [T("y", 10, 55.8)]),
        ("Bettenlift L2", 57.6, 10, 61.2, 13.5, "lino_kuehl", [T("y", 10, 59.4, 1.4)]),
        ("Flur 2OG", 0, 7, 61.2, 10, "lino_warm", [T("x", 61.2, 8.5, TUER["doppel"], "glas"), T("x", 36, 8.5, TUER["doppel"], "glas")]),
    ],
}
GESCHOSSE = {"EG": 0.0, "1OG": 4.0, "2OG": 8.0}
GESCHOSSE_Z1OG = GESCHOSSE["1OG"]

# Fenster außen (zusätzlich zu den Achsfenstern des Altbaus): (Trakt, Geschoss, Wandachse, Lage, a0, a1, z0, z1, Art)
# Altbau: Achsen k auf SE (y 0 bzw. Risalit y −3) und NW (y 16), Ausnahmen unten in `achsfenster()`.
SONDERFENSTER = [
    ("A", "EG", "y", -3, 25.2 + 1.1, 25.2 + 2.5, 0.4, 3.2, "glas"),        # Risalit SE Achse 8, hoch
    ("A", "EG", "y", -3, 36 - 2.5, 36 - 1.1, 0.4, 3.2, "glas"),            # Risalit SE Achse 10, hoch
    ("A", "EG", "y", 19, 27.4, 28.6, 2.0, 6.0, "glas"),                    # Treppenhausrisalit NW, hohes Fenster
    ("A", "1OG", "y", 19, 27.4, 28.6, 6.0, 10.0, "glas"),                  # zweites hohes Fenster (z 6 … 10)
    ("A", "EG", "x", 0, 7.3, 9.7, 0.9, 3.1, "glas"), ("A", "1OG", "x", 0, 7.3, 9.7, 4.9, 7.1, "glas"),   # Stirnfenster
    ("A", "2OG", "x", 0, 7.3, 9.7, 8.9, 11.1, "glas"),
    ("N", "EG", "x", 85.2, AUFNAHME_GLAS["y0"], AUFNAHME_GLAS["y1"], 0.0, AUFNAHME_GLAS["h"], "glas"),  # Fensterfront Aufnahme
    ("N", "EG", "x", 85.2, RETTUNGSTOR["y0"], RETTUNGSTOR["y1"], 0.0, RETTUNGSTOR["h"], "tor"),         # Rettungstor
    ("N", "EG", "x", 85.2, -1.6, -0.4, 1.0, 2.6, "glas"),                                               # Triage NE Seitenlicht
    ("N", "EG", "y", -6, 62.0, 69.5, 2.2, 3.0, "warm"),                                                 # Schockraum Oberlichter (06:40 in Betrieb)
    ("N", "EG", "y", 18, 62.0, 84.6, 1.0, 2.6, "glas"),                                                 # NW Band EG
    ("N", "1OG", "y", 18, 66.0, 85.2 - 0.6, 5.0, 6.6, "glas"),                                          # CPU Fensterband NW
    ("N", "1OG", "y", 18, 61.8, 65.4, 5.0, 6.6, "glas"),                                                # Warten Angehörige
    ("N", "1OG", "x", 85.2, -5.4, 6.4, 5.0, 6.6, "glas"),                                               # NE Band HKL-Arzt/Befundung
    ("N", "1OG", "x", 85.2, 7.3, 9.7, 4.9, 7.1, "glas"),                                                # Flurende 1. OG
    ("N", "EG", "y", -6, 71.0, 84.4, 1.0, 2.6, "glas"),                                                 # Triage SE Fensterband (25.10.: Leben an der SE-Seite)
    ("N", "1OG", "y", -6, 74.8, 84.6, 4.9, 7.0, "glas"),                                                # Schaltraum HKL und Arztzimmer: Band hinter den Lamellen
    ("N", "1OG", "y", -6, 62.4, 65.4, 5.4, 6.6, "warm"),                                                # Technik N: ein warmes Fenster hinter den Lamellen
]
BLIND_NW = {9, 10}                      # Achsen ohne NW-Fenster (Lifte L1, Blindfeld); Achse 8 liegt im Risalit

# Fassade SE (Antwort 3 des Nutzers, 23.10.2026): nicht 17 gleiche Achsen, sondern Rhythmus [PP] s s P s s [Risalit] s s P s s [PP].
# Eckrisalite (Entscheid 23.10.2026, an Claude delegiert): 1,0 m vor der SE-Flucht, eigener Walm, beidseitig — West über alle
# Geschosse, Ost nur im 2. OG über dem Flachdach des Neubaus (darunter steckt das Altbau-Ende im Winkel von Trakt N).
# Die Fensterpaare der Achsen 1–2 und 16–17 liegen in den Risaliten; Raumrechtecke und Türen bleiben, nur die Außenhaut rückt vor.
ECK_VOR = 1.0
ECKRISALITE = [dict(name="West", x0=0.0, x1=7.2, geschosse=("EG", "1OG", "2OG")),
               dict(name="Ost", x0=54.0, x1=61.2, geschosse=("2OG",))]
ECK_NEIGUNG = 42.0                         # Walm der Risalite steiler als das Hauptdach (30°), Traufe gleich hoch: der First (z ≈ 15,4)
                                           # steht 1,1 m über dem Hauptwalm und liest als Eckpavillon; bei 30° lägen West- bzw. Ostfläche
                                           # deckungsgleich auf den Walmflächen des Hauptdachs (Z-Fighting, lose Freestyle-Kanten)
FENSTERPAARE = {1, 2, 5, 13, 16, 17}       # Achsen mit gekoppelten Fenstern (SE und NW): zwei Flügel PAAR.b breit, Pfosten dazwischen
PAAR = dict(b=1.0, pfosten=0.3)            # Paar deckt xm ± 1,15 — bleibt 0,65 m von den Achsgrenzen (Innenwände bei x = 3,6·k) weg
# Warm beleuchtete Fenster um 06:40 (Ende des Nachtdiensts): (Geschoss, Achse) auf der SE-Front, unregelmäßig, vor allem Station
# 1. OG; dazu in SONDERFENSTER die Schockraum-Oberlichter (Steiner, Reanimation seit 06:30) und das Portal (Foyer). Rest Tinte/Glas.
WARME_FENSTER = {("1OG", 3), ("1OG", 6), ("1OG", 9), ("1OG", 11), ("1OG", 15), ("2OG", 4), ("2OG", 14), ("EG", 7)}

# Fassade ausdetailliert (25.10.2026, Auftrag B; Vorbild nur für den Detailgrad: vorlagen/haus/fotos/, nie im Repository).
# Maßstab von Kamera (a): etwa 17 px je Meter an der Fassade — ein Detail unter 0,1 m ist nur noch Rauschen. Deshalb Fenster-
# rahmen, Sprossen, Faschen und Fugen als flache Farbflächen OHNE eigene Tuschelinie (Materialien in OHNE_LINIE); Linie nur
# an der Laibung (Wandnetz), an der Scheibe, am Rollladen und an den Gesimsen.
FENSTERDEKOR = dict(rahmen=0.13, pfosten=0.10, kaempfer=0.12, kaempfer_hoehe=0.68, fasche=0.16, sohlbank=0.20, sohlbank_vor=0.08,
                    tiefe=0.14,                        # Scheibe 0,14 m hinter der Außenflucht (statt 0,30: weniger Doppellinie)
                    rollladen=0.26, gardine=0.30, offen=0.07)   # Anteile der SE-Fenster mit Rollladen (halb/ganz), Gardine, offenem Flügel
RUSTIKA = dict(fugen=(0.5, 1.1, 1.7, 2.3, 2.9, 3.5), hoehe=0.06, vor=0.012)   # gebändertes Sockelgeschoss: horizontale Fugen (ohne Linie)
GESIMSE = [dict(z0=3.86, z1=4.10, vor=0.12), dict(z0=7.88, z1=8.08, vor=0.08), dict(z0=11.66, z1=12.0, vor=0.14)]   # Geschoss- und Traufgesims
# Fassadenkanten, an denen Gesimse laufen: (Wandachse, Lage, a0, a1, Außenseite ±1); nur was Kamera (a) sieht (SE und West)
FASSADENKANTEN = [("y", -ECK_VOR, 0.0, 7.2, -1), ("x", 7.2, -ECK_VOR, 0.0, +1), ("y", 0.0, 7.2, RISALIT_SE[0], -1),
                  ("x", RISALIT_SE[0], RISALIT_SE[1], 0.0, -1), ("y", RISALIT_SE[1], RISALIT_SE[0], RISALIT_SE[2], -1), ("x", RISALIT_SE[2], RISALIT_SE[1], 0.0, +1),
                  ("y", 0.0, RISALIT_SE[2], A["x1"], -1), ("x", 0.0, -ECK_VOR, A["y1"], -1)]
TRAUFE_OHNE = {("y", RISALIT_SE[1]), ("x", RISALIT_SE[0]), ("x", RISALIT_SE[2])}   # am Mittelrisalit steigt die Giebelwand weiter: dort kein Traufgesims
SPARREN = dict(abstand=0.9, b=0.12, h=0.16, tiefe=0.55)                            # dunkle Sparrenköpfe unter dem Dachüberstand (ohne Linie)
FALLROHRE = [("y", -ECK_VOR, 0.25), ("y", 0.0, 7.45), ("y", 0.0, 24.95), ("y", 0.0, 36.25), ("y", 0.0, 53.8), ("y", 0.0, 60.9)]   # (Achse, Lage, Stelle)
GAUBEN = [13.0, 19.2, 42.0, 48.2]              # Giebelgauben auf der SE-Dachfläche (x der Mitte), Front bei y 1,8
GAUBE = dict(b=1.6, y=1.8, tiefe=1.8, fenster=(1.0, 1.1))
PORTAL_DEKOR = dict(bogen=1.5, tuer_h=2.4, pilaster=0.6, pilaster_vor=0.22, stufen=3, stufe=0.37, stufen_b=6.4,
                    balkon=(27.4, 33.8, 1.45), bruestung=0.95, baluster=0.2)   # Balkon 1. OG = Vordach des Portals, Holzbrüstung
LOGGIA = dict(pfeiler=0.42, tiefe=0.3, z_kaempfer=6.2, ueber_bogen=0.35)   # Arkade vor dem Portalbalkon: Bogenansatz z 6,2, Platte darüber (25.10.)
GIEBEL_DEKOR = dict(streifen=0.32, balkon=(27.6, 33.6, 1.2), rundfenster=(0.42, 15.72), tuer=(0.95, 1.7))
# Umgebung: Zufahrt (Pflaster, 4,5 m, geschwungen vom Vorplatz zur Rettungsvorfahrt), Stellplätze mit Autos, Figuren als Silhouetten,
# Wegweiser an der Kehre, Haltestelle an der Klinikstraße, Raucherecke an der Ecke von Trakt N, Fahrradständer am Vorplatz
ZUFAHRT = [(41.0, -12.0), (50.0, -13.6), (62.0, -15.0), (76.0, -14.2), (88.0, -10.0), (92.0, -6.5)]
STELLPLAETZE = dict(flaeche=(43.5, -10.8, 53.5, -5.5), autos=[(45.6, -8.1, "auto_weiss"), (51.2, -8.1, "auto_blau")])   # (x, y Mitte, Material), längs y
FIGUREN = [(30.6, -4.9, 0.0), (34.6, -6.6, 2.2), (35.3, -6.3, -0.8), (64.0, -8.6, 1.0), (23.5, -18.5, 0.6), (106.4, 7.5, 3.1)]   # (x, y, Blick rad)
WEGWEISER = dict(ort=(17.0, -23.8), hoehe=2.4, schilder=((2.1, 1), (1.6, -1)))   # Schilder (z Unterkante, Pfeilrichtung ±1): Notaufnahme →, Bettenstationen ←
HALTESTELLE = dict(x=106.6, y0=3.5, y1=7.5, tiefe=1.6, hoehe=2.6, schild=(105.6, 1.5))
RAUCHERECKE = dict(bank=(66.0, -8.4), ascher=(63.6, -8.0))
FAHRRAEDER = dict(buegel=(21.2, 22.0, 22.8, 23.6), y=-5.0, raeder=((21.6, "figur"), (23.2, "tor")))
JUNGBAEUME = [(57.0, -18.6, 2.0, "laub_gelb"), (70.5, -19.0, 1.9, "laub"), (84.0, -18.2, 2.1, "laub_rost"), (10.0, -15.0, 1.8, "laub_gelb")]
KAHLE_BAEUME = [(13.0, -45.0, 2.8)]       # ein kahler Jungbaum auf der Wiese rechts des Wegs, vor Wiese und Himmel (vor der Fassade las das Astwerk als Gekritzel)
HERBST = dict(linden=("laub_gelb", "laub_rost"), kastanie="laub_rost", wald_anteil=0.35)   # Spätherbst (ART_BIBLE §4): Kronen teils gelb/rostig
LAUB = dict(weg=(18.0, 95.0, 90, 2.6), linden=6.5, je_linde=28, vorplatz=30, radius=(0.25, 0.7))   # Herbstlaub: (s0, s1, Anzahl, Streubreite) am Parkweg West

# Umgebung (§5)
LINDEN = [(15.0, -10.0, 4.5), (46.0, -10.0, 4.5)]                 # (x, y, Kronenradius); nach außen gerückt (Antwort 4): bei x 18 deckte die Krone aus
                                                                  # Kamera (a) per Parallaxe noch das Portal (Blick diagonal), ab x 15 / y −10 ist der Risalit frei
KASTANIE = (50.0, 27.0, 6.0)
VORPLATZ = (20.0, -20.0, 41.0, -3.0)
PARKWEG = [(30.0, -20.0), (14.0, -34.0), (44.0, -52.0), (60.0, -70.0)]           # zwei Kehren zur Haltestelle (§5)
PARKWEG_WEST = [(-34.0, -68.0), (-24.0, -54.0), (-12.0, -44.0), (2.0, -36.0), (16.0, -27.0), (26.0, -21.0), (30.0, -20.0)]
                                           # Ast von der Hangwiese herauf: Kamera (a) steht darauf (−30/−62); er läuft als Führungslinie
                                           # vom unteren Bildrand in einer S-Kurve zum Vorplatz und Portal, Laternen an seiner NW-Seite
LATERNEN = [("west", 45.0), ("west", 60.0), ("west", 75.0), ("halte", 15.0)]      # (Weg, Meter ab Anfang); 1,6 m links (NW) des Wegs,
                                           # damit ihr Fußschatten nicht auf den Weg fällt; die nächste steht 36 m vor der Kamera
LATERNE = dict(hoehe=3.2, kopf=0.4)
WEG = dict(breite=2.5, kante=0.25)        # Gehweg mit Kantenstein beidseits
HECKEN = [((-14.0, -40.0), (-2.0, -33.5)), ((30.0, -24.0), (40.0, -30.0))]        # (Anfang, Ende), 1,1 m hoch, beide im Bild von (a)
BAENKE_WEG = [("west", 38.0)]              # (Weg, Meter ab Anfang): Ruhebank 2,2 m links des Parkwegs West, 36 m vor der Kamera, längs zum Weg
KLINIKSTRASSE = [(103.0, -80.0), (103.0, 40.0)]
RETTUNGSZUFAHRT = [(103.0, -1.0), (91.0, -1.0)]
PLATANEN = [(98.0, y, 4.0) for y in (-70, -50, -30, 10, 30, 50)]  # Lücke y −30 … 10 an der Zufahrt: dort geht der Blick von (a) ins Tal
RTW = dict(x0=96.0, x1=98.4, y0=-6.5, y1=-1.0, h=2.1)             # Rettungswagen auf der Abstellfläche neben dem Vordach, längs y, Front nach
                                           # Südost (06:30 kam die Reanimation, REDESIGN_FALL1 §5.2) — das eine Rost-Objekt von Bild (a): Papier-Klotz
                                           # mit Rost-Streifen. Unter dem Vordach (x 85,7 … 91,2) verschwand er hinter Stütze und Trakt-N-Ecke; hier
                                           # steht er rechts der Ecke (−19,2° … −21,6°) vor der Unterstadt, Seite und Front mit Streifen zur Kamera
PARKPLATZ = (70.0, 20.0, 100.0, 40.0)
WALDTOR = (48.0, 34.0)
TERRASSE_Y = -40.0           # bis hier eben (z −0,6), dann 6 % Gefälle nach Südost
TAL_Y = -200.0               # ab hier Talboden
WALD_Y = 35.0                # dahinter steigt der Waldhang mit 10 % …
WALD_STEIL = (60.0, 0.25)    # … und ab y 60 mit 25 % (Hügelrücken): sonst verschwinden die Waldbänder aus Kamera (a) hinter dem First
WALD_AUSLAUF = (110.0, 170.0)   # östlich davon läuft der Waldhang aus (Faktor 1 → 0): der Rücken fällt in die Talbiegung
OSTHANG = dict(x0=115.0, gefaelle=0.08, tiefe=5.0)     # östlich der Klinikstraße fällt das Gelände 8 % zum Talboden (−5 m ab x 177,5)
GEGENHANG = dict(x0=440.0, steigung=0.08, hoehe=30.0)  # jenseits des Flusses steigt der Gegenhang mit der Oberstadt (bis +30 m bei x 815)
# Von Kamera (a) (z 3) ist der Osthang selbst unsichtbar (die Terrassenkante bei x 115 verdeckt alles unter −1,3°); sichtbar sind nur
# Dächer, die darüber ragen, der Fluss ab ≈ 450 m und der Gegenhang, der dem Betrachter zugewandt ist. Flacher Talboden (−5) statt −25.
FLUSS = dict(punkte=[(410.0, -160.0), (413.0, -80.0), (417.0, 0.0), (423.0, 80.0), (431.0, 160.0), (447.0, 240.0), (473.0, 320.0)], breite=110.0)
                                           # heller Streifen im Morgenlicht; 110 m breit, weil er aus 3 m Höhe nur als Linie erscheint (≈ 7 px)
HIMMEL_BAENDER = ["#F8E7BF", "#F6DCA4", "#F3CD8C"]            # oben → Horizont (§9 a)
# Wolken: flache Linsen auf der Himmelsebene (900 m), (seitlich m, Höhe z, Länge, Dicke, Material); negativ = links der Blickachse
WOLKEN = [(260.0, 150.0, 520.0, 24.0, "wolke_warm"), (-140.0, 232.0, 820.0, 30.0, "wolke_hell"), (150.0, 290.0, 440.0, 18.0, "wolke_warm")]
# Comic-Wolken (Stile tag/blau, 25.10.2026): geballte Kumulus mit Umriss statt Linsen — (seitlich m, Unterkante z, Länge, Höhe, Material);
# Umriss = flache Unterkante, oben eine Kette überlappender Kreise mit Kerben (siehe `kumulus` in himmel_setzen). Dachfirst liegt auf
# der Himmelsebene bei z ≈ 140, Bildoberkante bei ≈ 300.
WOLKEN_KUMULUS = [(-320.0, 224.0, 230.0, 62.0, "wolke_hell"), (-70.0, 250.0, 170.0, 52.0, "wolke_hell"),
                  (190.0, 165.0, 270.0, 92.0, "wolke_hell"), (375.0, 240.0, 140.0, 44.0, "wolke_warm"), (-30.0, 198.0, 80.0, 26.0, "wolke_warm")]
                                           # alle innerhalb des Bildes (± 458 m bei 900 m): eine angeschnittene Wolke zog ihre Grundlinie als Lineal bis zum Rand.
                                           # Links liegt das ferne Waldband 2 (wald_fern, 170–240 m vor der Kamera) VOR der Himmelsebene und reicht aus (a) bis
                                           # ≈ 13° (z ≈ 208 auf 890 m): Wolken links brauchen eine Unterkante ≥ 220, sonst schiebt sich das Band in die Wolke.

# Vordergrund von Render (a): Büsche (x, y, Radius) in drei Gruppen mit Bodenkontakt neben dem Parkweg, nicht in der Bildmitte,
# alle ≥ 33 m vor der Kamera (näher werden sie zu grünen Wolken); Wiesenflecken zufällig im Bildausschnitt
BUESCHE = [(-10.0, -36.0, 0.9), (-8.4, -34.6, 0.6), (-11.6, -34.8, 0.7),                 # Gruppe links des Wegs vor der Hecke
           (11.5, -24.0, 1.0), (13.2, -22.6, 0.7), (10.0, -22.4, 0.6), (12.4, -25.6, 0.5),  # Gruppe an der Kehre, NW-Seite
           (20.0, -40.0, 0.9), (22.0, -39.2, 0.6), (21.2, -41.6, 0.7),                     # Gruppe an der Gabel zur Haltestelle
           (-2.0, -52.0, 0.8), (-0.2, -50.8, 0.55), (-3.4, -50.6, 0.6)]                    # Gruppe rechts unten am Hang (Bildrand)
WIESENFLECKEN = dict(bereich=(-40.0, -70.0, 90.0, -5.0), anzahl=18, radius=(4.0, 11.0))

# Wald (§5): nahes Band als dichte Baumgruppen (zwei Reihen), Mitte und Ferne als Silhouettenbänder (ein Netz je Band).
# Tiefenstaffelung: vorn Laub (grün, besonnt), Mitte Petrol (Kamm im Schatten, die dunkle Form), hinten Papier (Dunst).
WALD_NAH = dict(x0=-10.0, x1=150.0, reihen=((38.0, 44.0), (45.0, 52.0)), abstand=6.0, hoehe=(17.0, 26.0))
UNTERHOLZ = [(-4.0, 36.5, 2.6), (2.5, 36.0, 2.9), (9.0, 36.8, 2.4), (15.5, 36.2, 2.7)]   # Büsche am Waldrand (25.10.): Stämme der Reihe 1 standen als Pfähle neben dem Haus
WALD_WEST = dict(x0=-62.0, x1=-24.0, y0=-26.0, y1=38.0, abstand=(8.0, 9.0), hoehe=(16.0, 24.0))   # y0 −26 (25.10.): bei −40 ragten zwei Föhrenstämme 23 m neben der Kamera als „Pfähle" in den linken Bildrand
WALDBAENDER = [(76.0, -150.0, 230.0, "wald_mitte", (20.0, 28.0)), (106.0, -160.0, 205.0, "wald_fern", (22.0, 30.0))]   # (y, x0, x1, Material, Höhen)
WALDBAND_AUSLAUF = 40.0      # auf den letzten Metern sinkt die Oberkante eines Bands (kein senkrechter Schnitt hinter Trakt N)

# Stadt (§5): im Tal südöstlich (y < −200, von Kamera (a) nicht sichtbar) UND in der Talbiegung nordöstlich: Kamera (a) sieht rechts
# neben Trakt N (18–26° rechts von +x) die Unterstadt gleich hinter der Klinikstraße (nur ihre Dächer ragen über die Terrassenkante),
# dahinter den Fluss und die Oberstadt am Gegenhang. `neigung`: Streifen schräg zur Blickachse (y0/y1 wandern mit x).
# Nur Bänder, keine Linie. Dächer Holz (eine Stufe dunkler als Linoleum warm): auf Papier-Hängen blieb die Stadt sonst unsichtbar.
STADT = [dict(x0=-120.0, x1=200.0, y0=-290.0, y1=-210.0, haeuser=40, tuerme=((20.0, -250.0, "helm"), (110.0, -250.0, "zwiebel"))),
         dict(x0=150.0, x1=235.0, y0=8.0, y1=24.0, neigung=0.46, haeuser=45, groesse=0.65, hoehe=(5.0, 8.0), tuerme=((178.0, 26.0, "helm"),)),
                                           # Unterstadt, linke Hälfte der Lücke; kleine Häuser, sonst deckt ein einziges 170 m vor der Kamera die Lücke
         dict(x0=445.0, x1=660.0, y0=40.0, y1=320.0, haeuser=260, tuerme=((470.0, 130.0, "zwiebel"), (560.0, 190.0, "helm")))]   # Oberstadt am Gegenhang
# Die Stadt liegt um 06:40 noch im Schatten des Tals (nur die Hangterrasse hat schon Sonne): ihre Materialien sind IMMER_SCHATTEN,
# das Komposit legt die Schattenstufe darüber; der Fluss spiegelt den Himmel und bleibt hell.
HUEGEL = [(-110.0, -260.0, 70.0, 40.0), (190.0, -270.0, 80.0, 50.0), (820.0, 150.0, 260.0, 60.0), (1000.0, -60.0, 320.0, 80.0), (700.0, 420.0, 220.0, 50.0)]
                             # (x, y, r, sichtbare Höhe); drei Kämme hinter der Oberstadt schließen das Tal (alle vor der Himmelsebene, 900 m)

# Kameras (§9): Ort, Ziel, Brennweite; Sonne (Azimut °, Höhe °); Licht- und Himmelsfarben
KAMERAS = {
    "aussen": dict(ort=(-30.0, -62.0, 3.0), ziel=(34.0, 2.0, 7.0), brennweite=35, sonne=(80.0, 7.0),
                   licht="#FFF0C6", anteil=0.45, himmel=HIMMEL_BAENDER, schatten=0.14, wolken=WOLKEN),
    "flur": dict(ort=(23.3, 8.5, GESCHOSSE_Z1OG + 1.55), ziel=(61.0, 8.5, GESCHOSSE_Z1OG + 1.55), brennweite=24, sonne=(120.0, 35.0),   # §9: Augenhöhe 1,55 über dem Boden des 1. OG; x 23,3 statt 24 (23.10.): Tür 107 ganz hinter dem Bildrand, Tresen im rechten Drittel
                 licht="#FBFDF8", anteil=0.42, himmel=["#DCE9EA", "#E6EFEE", "#EAF1F0"], schatten=0.10,
                 linien_nur=("Trakt A 1OG", "Trakt N 1OG", "Moebel Flur 1OG", "Kerne")),   # Linien-Durchgang: nur diese Sammlungen (Freestyle verliert in der 600-m-Szene die Verdeckung)
}
B, H = 1600, 900
UEBER = 2                    # Überabtastung der Linie (wie ebenen.py)
PROBEN = dict(flat=4, lines=4, sun=16)

# Lokalfarben (ART_BIBLE §2) und Grauwerte für den Sonnen-Durchgang
PALETTE = {
    "putz": "#EFE6D3", "sockel": "#B6BFB6", "ziegel": "#C9795A", "rahmen": "#2C5560", "glas": "#1E2A30",
    "tor": "#2C5560", "lamelle": "#C99A5B", "beton": "#F7F1E4", "stuetze": "#2C5560", "attika": "#F7F1E4",
    "wand": "#EFE6D3", "wand_n": "#F7F1E4", "paneel": "#BFD9CF", "paneel_n": "#2C5560", "decke": "#F7F1E4",
    "lino_warm": "#C9BDA2", "lino_kuehl": "#B6BFB6", "tuer": "#2C5560", "zarge": "#C99A5B", "holz": "#C99A5B",
    "lift": "#2C5560", "petrol": "#2C5560", "figur": "#2C5560",
    # Außengrün (ART_BIBLE §2 „Wiese"/„Laub", Entscheid des Nutzers 23.10.2026): Rasen Wiese, Kronen/Hecken/Büsche Laub
    "wiese": "#ACB98B", "wiese_hell": "#B9C59A", "weg": "#C9BDA2", "kante": "#EFE6D3", "asphalt": "#B6BFB6", "pflaster": "#F7F1E4", "hecke": "#6F8A62",
    "stamm": "#2C3E46", "laub": "#6F8A62", "wald_nah": "#6F8A62", "wald_mitte": "#2C5560", "wald_fern": "#F7F1E4",
    "stadt": "#F7F1E4", "stadt_sand": "#EFE6D3", "stadt_dach": "#C99A5B", "himmel_0": HIMMEL_BAENDER[0], "himmel_1": HIMMEL_BAENDER[1],
    "himmel_2": HIMMEL_BAENDER[2], "beet": "#C99A5B",
    # Leben und Tiefe in Bild (a): warme Fenster (Morgenlicht, eine Stufe wärmer als die Fassadensonne), Fluss, Wolken (Morgenlicht-
    # Abwandlungen), Fußschatten der Bäume (Lokalfarbe des Bodens, im Sonnen-Durchgang schwarz → Schattenstufe), Rettungswagen
    "fenster_warm": "#F3CD8C", "fluss": "#F8E7BF", "wolke_hell": "#FBF0D6", "wolke_warm": "#F8E7BF",
    "schatten_wiese": "#ACB98B", "schatten_pflaster": "#F7F1E4", "rtw": "#F7F1E4", "rost": "#B5552D",
    # Fassadendetails (25.10.2026): Faschen/Gesimse Papier, Sockelgeschoss Linoleum kühl mit Fugen, Rollläden und Giebelholz Laub,
    # Portaltür dunkles Holz, Zink für Rinne und Fallrohre, Schrift Tinte; Herbst: Kronen gelb/rostig, Laub am Boden
    "fasche": "#F7F1E4", "gesims": "#F7F1E4", "rustika": "#D8D2C0", "fuge": "#B6AE9C", "rollladen": "#6F8A62", "holz_gruen": "#6F8A62",
    "gardine": "#E6E4DC", "holz_dunkel": "#5A3A2A", "stein": "#D9D2C2", "zink": "#8A8F96", "schrift": "#1E2A30", "sparren": "#3B2A22",
    "auto_weiss": "#F7F1E4", "auto_blau": "#2C5560", "laub_gelb": "#D0A54A", "laub_rost": "#B8703A", "laub_boden": "#B07A3C", "laub_boden_hell": "#D2A354",
}
OHNE_LINIE = {"himmel_0", "himmel_1", "himmel_2", "wald_fern", "stadt", "stadt_sand", "stadt_dach", "wiese_hell",
              "fluss", "schatten_wiese", "schatten_pflaster",
              "rahmen", "fasche", "fuge", "holz_gruen", "gardine", "zink", "schrift", "sparren", "laub_boden", "laub_boden_hell", "lamelle"}
OHNE_SCHATTIERUNG = {"himmel_0", "himmel_1", "himmel_2", "glas", "wald_fern", "wald_mitte", "stadt", "stadt_sand", "stadt_dach", "wiese_hell",
                     "fluss", "wolke_hell", "wolke_warm", "fenster_warm", "rahmen", "fasche", "fuge", "gardine", "schrift", "laub_boden", "laub_boden_hell"}
IMMER_SCHATTEN = {"schatten_wiese", "schatten_pflaster", "stadt", "stadt_sand", "stadt_dach"}   # im Sonnen-Durchgang schwarz: das Komposit
                                         # legt dort die Schattenstufe hin (Fußschatten; die Stadt im Tal liegt um 06:40 noch im Schatten)
OHNE_SCHATTEN = {"Baeume", "Buesche", "Laternen", "Figuren", "Hof"}   # Sammlungen, deren Objekte keinen Schlagschatten werfen (ART_BIBLE §3.5: bei 7° Sonne
                                         # würde jeder Busch 20 m, jede Laterne 28 m Schatten werfen; Kronenschatten zerlegten die Fassade).
                                         # Sie bekommen stattdessen einen flachen Fußschatten (`fussschatten`). Gebäude und RTW werfen echte.
SONNE_AUS_MATERIAL = {"glas"}            # Glas lässt die Sonne durch (Sonnen-Durchgang ohne Scheiben)

# Stilproben (25.10.2026, Referenzen des Nutzers: Chaland/Tram-Wandbild für „tag", Dauger für „blau"). Nur Farbe, Licht und
# Linie; die Geometrie bleibt. Aufruf `render aussen --stil tag|blau` -> docs/haus/stil_<stil>.jpg; die freigegebene Probe
# bleibt unberührt. Grundpalette beider Stile ist TAG_PALETTE; „blau" legt sie im Komposit als Duoton in den Blauen Stunde.
TAG_PALETTE = {
    "putz": "#E9C46A", "sockel": "#8F8A7A", "ziegel": "#B8452F", "rahmen": "#F4F1E6", "glas": "#1B2240", "tor": "#3A5A8C",
    "lamelle": "#B9783E", "beton": "#ECE8DC", "attika": "#ECE8DC", "stuetze": "#3A5A8C",
    "wiese": "#8DB255", "wiese_hell": "#A5C46A", "weg": "#D9C9A0", "kante": "#F4F1E6", "asphalt": "#6E7480", "pflaster": "#E2D7B9",
    "hecke": "#3F7A3A", "stamm": "#3B2A22", "laub": "#5E9440", "wald_nah": "#3F7A3A", "wald_mitte": "#2F5A55", "wald_fern": "#9DB8C8",
    "stadt": "#E8DCC2", "stadt_sand": "#D9C08A", "stadt_dach": "#B8452F", "beet": "#8A5A3A",
    "fenster_warm": "#FFD25A", "fluss": "#7FB3D5", "wolke_hell": "#FFFFFF", "wolke_warm": "#F2F6FA",
    "schatten_wiese": "#8DB255", "schatten_pflaster": "#E2D7B9", "rtw": "#F4F1E6", "rost": "#C8382B",
    # Fassadendetails und Herbst (ART_BIBLE §2 „Außen", Ergänzung 25.10.2026)
    "fasche": "#F4F1E6", "gesims": "#F4F1E6", "rustika": "#D6D0BE", "fuge": "#AFA896", "rollladen": "#4F7F4A", "holz_gruen": "#4F7F4A",
    "gardine": "#E3E6EC", "holz_dunkel": "#4A2E22", "stein": "#CFC9BA", "zink": "#7E858F", "schrift": "#1A1F2E", "sparren": "#3B2A22",
    "auto_weiss": "#F4F1E6", "auto_blau": "#3A5A8C", "laub_gelb": "#D9A93C", "laub_rost": "#B9652C", "laub_boden": "#B8762F", "laub_boden_hell": "#D8A24A",
}
STILE = {
    "tag": dict(palette=TAG_PALETTE, kamera=dict(sonne=(115.0, 24.0), licht="#FFF3D6", anteil=0.22, schatten=0.45,
                                                 himmel=["#5E9AD0", "#86B6E0", "#B9D7EE"], wolken=WOLKEN_KUMULUS),
                schatten="#3B4A7A", tinte="#1A1F2E", kontur=2.6, innen=1.3, baumschatten=True),
    "blau": dict(palette=dict(TAG_PALETTE, wolke_hell="#3A3A3A", wolke_warm="#303030"),
                 kamera=dict(sonne=(80.0, 7.0), licht="#F6C98A", anteil=0.0, schatten=0.0,
                             himmel=["#0E0E0E", "#262626", "#E9A86A"], wolken=WOLKEN_KUMULUS),           # unten ein Streifen Morgenrot (Dienst endet)
                 schatten="#1A2350", tinte="#0E1226", kontur=2.6, innen=1.3, mit_sonne=False,
                 duoton=("#121A48", "#8FA4EC"), eigen=0.10, leuchten=("fenster_warm", "himmel_2")),
}


def stil():
    return STILE.get(os.environ.get("HAUS_STIL", ""))


def stil_endung():
    return "_" + os.environ["HAUS_STIL"] if stil() else ""


def hexc(s):
    return tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))


def hex_lin(s):
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in hexc(s))


def gelaende_z(x, y):
    """Höhe des Geländes (§5): Terrasse eben, Hang 6 % nach Südost ab y −40, Waldhang 10 % ab y 35 (läuft östlich x 110 … 170
    aus); östlich der Klinikstraße (x > 115) fällt alles mit 8 % auf den Talboden (−5), der Fluss liegt bei x ≈ 400, dahinter
    steigt der Gegenhang mit der Oberstadt (ab x 440, 8 %, bis +30)."""
    if y >= WALD_STEIL[0]: z = 0.1 * (WALD_STEIL[0] - WALD_Y) + WALD_STEIL[1] * (y - WALD_STEIL[0])
    elif y >= WALD_Y: z = 0.1 * (y - WALD_Y)
    elif y >= A["y1"]: z = 0.0
    elif y >= 0: z = -SOCKEL * (1 - y / A["y1"])          # Übergang unter dem Haus (unsichtbar)
    elif y >= TERRASSE_Y: z = -SOCKEL
    elif y >= TAL_Y: z = -SOCKEL - 0.06 * (TERRASSE_Y - y)
    else: z = -SOCKEL - 0.06 * (TERRASSE_Y - TAL_Y)
    if y >= WALD_Y and x > WALD_AUSLAUF[0]:                # Waldhang läuft nach Osten aus
        z *= max(0.0, (WALD_AUSLAUF[1] - x) / (WALD_AUSLAUF[1] - WALD_AUSLAUF[0]))
    if x > OSTHANG["x0"]: z -= min(OSTHANG["gefaelle"] * (x - OSTHANG["x0"]), OSTHANG["tiefe"])
    if x > GEGENHANG["x0"]: z += min(GEGENHANG["steigung"] * (x - GEGENHANG["x0"]), GEGENHANG["hoehe"])
    return z


def schattenrichtung(kamera="aussen"):
    """Richtung, in die Fußschatten versetzt werden (Lichtrichtung der Kamera-Sonne, in der Ebene normiert)."""
    dx, dy, _ = sonnenrichtung(*KAMERAS[kamera]["sonne"]); l = math.hypot(dx, dy)
    return dx / l, dy / l


# ======================================================================================================
# Bauen
# ======================================================================================================
def bauen():
    sys.path.insert(0, HIER)
    import bpy
    from mathutils import Vector
    import werkzeug as wz

    wz.leeren()
    sc = bpy.context.scene
    M = {}
    for name, farbe in PALETTE.items():
        lin = hex_lin(farbe); grau = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
        M[name] = wz.material(name, (grau, grau, grau), 0.8)       # Grau nur für den Sonnen-Durchgang
    sammlungen = {}

    def sammlung(name):
        if name not in sammlungen:
            c = bpy.data.collections.new(name); sc.collection.children.link(c); sammlungen[name] = c
        return sammlungen[name]

    def einordnen(o, name):
        for c in list(o.users_collection): c.objects.unlink(o)
        sammlung(name).objects.link(o)
        return o

    def kiste(name, x0, y0, x1, y1, z0, z1, m, samm, fase=0.0):
        """Achsparalleler Quader. Ohne Fase direkt als Netz (from_pydata, kein Operator): bei 4000 Objekten kostete jeder
        bpy.ops-Aufruf eine Depsgraph-Aktualisierung, der Bau dauerte 8 min statt 1,5."""
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
        if min(x1 - x0, y1 - y0, z1 - z0) < 1e-4: return None
        if fase:
            o = wz.kiste((x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), M[m], "hinten", fase=fase, name=name)
            return einordnen(o, samm)
        v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        return netz(name, v, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (3, 0, 4, 7), (1, 2, 6, 5)], m, samm)

    def netz(name, verts, faces, m, samm, glatt=False, normalen=False):
        me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces)
        if normalen:                                                   # geschlossene Körper (Prismen): Normalen konsequent nach außen
            import bmesh
            bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); bm.to_mesh(me); bm.free()
        me.update()
        o = bpy.data.objects.new(name, me); o.data.materials.append(M[m]); sc.collection.objects.link(o)
        wz.markiere(o, "hinten")
        return einordnen(o, samm)

    def prisma(name, punkte, achse, w0, w1, m, samm):
        """Beliebiges ebenes Vieleck (u entlang der Wand, v = z), zwischen w0 und w1 quer zur Wand ausgezogen (Bogenzwickel,
        Giebelfelder). `achse` wie bei wandnetz."""
        n = len(punkte); verts = []
        for w in (w0, w1):
            for (u, v) in punkte: verts.append((u, w, v) if achse == "y" else (w, u, v))
        faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        return netz(name, verts, faces, m, samm, normalen=True)

    def wandnetz(name, achse, w0, w1, a0, a1, z0, z1, oeffnungen, m, samm):
        """Wand mit Öffnungen als EIN sauberes Netz ohne Boolesche Operation: Vorder- und Rückseite sind ein Raster aus
        Zellen (Spalten an den Öffnungsrändern, Zeilen an Sturz und Brüstung), dazu Laibungen, Stirn-, Ober- und
        Unterseiten — alles ohne T-Stöße. Boolesch gelochte n-Ecke ließen Freestyle die Verdeckung verlieren (Kanten
        dahinter schimmerten als lose Striche durch). `achse` 'y': Wand läuft in x (a0…a1), Dicke in y (w0…w1); 'x' umgekehrt.
        Öffnungen: (a0, a1, z_unten, z_oben) in Wandkoordinaten, werden auf die Wand beschnitten."""
        oeff = [(max(a0, o[0]), min(a1, o[1]), max(z0, o[2]), min(z1, o[3])) for o in oeffnungen]
        oeff = [o for o in oeff if o[1] - o[0] > 1e-6 and o[3] - o[2] > 1e-6]
        us = sorted({a0, a1, *[c for o in oeff for c in o[:2]]}); vs = sorted({z0, z1, *[c for o in oeff for c in o[2:]]})
        ecken = {}; verts = []; faces = []

        def P(u, w, v):
            key = (round(u, 5), w, round(v, 5))
            if key not in ecken:
                ecken[key] = len(verts); ww = w0 if w == 0 else w1
                verts.append((u, ww, v) if achse == "y" else (ww, u, v))
            return ecken[key]

        def offen(u0, u1, v0, v1):
            return any(u0 >= o[0] - 1e-6 and u1 <= o[1] + 1e-6 and v0 >= o[2] - 1e-6 and v1 <= o[3] + 1e-6 for o in oeff)

        for i in range(len(us) - 1):
            u0, u1 = us[i], us[i + 1]
            for j in range(len(vs) - 1):
                v0, v1 = vs[j], vs[j + 1]
                if offen(u0, u1, v0, v1): continue
                faces.append((P(u0, 0, v0), P(u1, 0, v0), P(u1, 0, v1), P(u0, 0, v1)))
                faces.append((P(u0, 1, v0), P(u0, 1, v1), P(u1, 1, v1), P(u1, 1, v0)))
            if not offen(u0, u1, z1 - 1e-6, z1): faces.append((P(u0, 0, z1), P(u1, 0, z1), P(u1, 1, z1), P(u0, 1, z1)))   # Oberseite
            if not offen(u0, u1, z0, z0 + 1e-6): faces.append((P(u0, 0, z0), P(u0, 1, z0), P(u1, 1, z0), P(u1, 0, z0)))   # Unterseite
        for j in range(len(vs) - 1):                                                                                 # Stirnseiten
            v0, v1 = vs[j], vs[j + 1]
            if not offen(a0, a0 + 1e-6, v0, v1): faces.append((P(a0, 0, v0), P(a0, 0, v1), P(a0, 1, v1), P(a0, 1, v0)))
            if not offen(a1 - 1e-6, a1, v0, v1): faces.append((P(a1, 0, v0), P(a1, 1, v0), P(a1, 1, v1), P(a1, 0, v1)))
        for (f0, f1, zb, zt) in oeff:                                                                                # Laibungen
            spalten = [u for u in us if f0 - 1e-6 <= u <= f1 + 1e-6]; zeilen = [v for v in vs if zb - 1e-6 <= v <= zt + 1e-6]
            for k in range(len(spalten) - 1):
                u0, u1 = spalten[k], spalten[k + 1]
                if zb > z0 + 1e-6: faces.append((P(u0, 0, zb), P(u0, 1, zb), P(u1, 1, zb), P(u1, 0, zb)))               # Brüstung
                if zt < z1 - 1e-6: faces.append((P(u0, 0, zt), P(u1, 0, zt), P(u1, 1, zt), P(u0, 1, zt)))               # Sturz
            for k in range(len(zeilen) - 1):
                v0, v1 = zeilen[k], zeilen[k + 1]
                if f0 > a0 + 1e-6: faces.append((P(f0, 0, v0), P(f0, 1, v0), P(f0, 1, v1), P(f0, 0, v1)))               # Laibung links
                if f1 < a1 - 1e-6: faces.append((P(f1, 0, v0), P(f1, 0, v1), P(f1, 1, v1), P(f1, 1, v0)))               # Laibung rechts
        import bmesh
        me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces)
        bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); bm.to_mesh(me); bm.free(); me.update()
        o = bpy.data.objects.new(name, me); o.data.materials.append(M[m]); sc.collection.objects.link(o)
        wz.markiere(o, "hinten")
        return einordnen(o, samm)

    # ---------------- Gelände ----------------
    schritt, xa, xb, ya, yb = 5.0, -140.0, 1060.0, -300.0, 470.0      # bis hinter Gegenhang und Hügel (Kamera (a) blickt 900 m weit)
    nx, ny = int((xb - xa) / schritt) + 1, int((yb - ya) / schritt) + 1
    verts = [(xa + i * schritt, ya + j * schritt, gelaende_z(xa + i * schritt, ya + j * schritt)) for j in range(ny) for i in range(nx)]
    faces = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i) for j in range(ny - 1) for i in range(nx - 1)]
    netz("Gelaende", verts, faces, "wiese", "Boden")   # eigene Sammlung: Freestyle nimmt daraus keine Linien (Terrassenkante schnitt sonst als
                                                        # Silhouette quer durch die Stadt im Tal), das Netz verdeckt aber weiter (Buschfüße, Hang)

    def band(name, punkte, breite, m, samm="Gelaende", hoch=0.03, versatz=0.0):
        """Weg/Straße als Streifen, der dem Gelände folgt (Höhe aus gelaende_z + hoch). Der Streckenzug wird alle 2 m unterteilt,
        sonst taucht ein gerades Stück über einem Geländeknick (Terrassenkante y −40) unter die Wiese."""
        dicht = []
        for p0, p1 in zip(punkte, punkte[1:]):
            n = max(1, int(math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / 2.0))
            dicht += [(p0[0] + (p1[0] - p0[0]) * j / n, p0[1] + (p1[1] - p0[1]) * j / n) for j in range(n)]
        punkte = dicht + [punkte[-1]]
        v, f = [], []
        for i, (x, y) in enumerate(punkte):
            p0 = punkte[max(i - 1, 0)]; p1 = punkte[min(i + 1, len(punkte) - 1)]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]; l = math.hypot(dx, dy) or 1
            nx_, ny_ = -dy / l * breite / 2, dx / l * breite / 2
            x, y = x - dy / l * versatz, y + dx / l * versatz        # `versatz`: seitlich neben der Mittellinie (Wegkanten)
            for s in (1, -1):
                v.append((x + s * nx_, y + s * ny_, gelaende_z(x + s * nx_, y + s * ny_) + hoch))
        for i in range(len(punkte) - 1):
            f.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
        return netz(name, v, f, m, samm)

    def flaeche(name, x0, y0, x1, y1, m, samm="Gelaende", hoch=0.02):
        z = gelaende_z((x0 + x1) / 2, (y0 + y1) / 2) + hoch
        return netz(name, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [(0, 1, 2, 3)], m, samm)

    def ellipse(name, cx, cy, ra, rb, dreh, m, samm="Gelaende", hoch=0.015, n=12, nur_in=None):
        """Flache Ellipse auf dem Gelände (Wiesenfleck, Fußschatten); `nur_in` = Rechteck, auf das die Fläche beschnitten wird."""
        pts = []
        for j in range(n):
            t = 2 * math.pi * j / n; ex, ey = ra * math.cos(t), rb * math.sin(t)
            pts.append((cx + ex * math.cos(dreh) - ey * math.sin(dreh), cy + ex * math.sin(dreh) + ey * math.cos(dreh)))
        if nur_in:                                                 # Sutherland–Hodgman gegen das achsparallele Rechteck
            for seite in range(4):
                neu = []
                drin = (lambda p: p[0] >= nur_in[0], lambda p: p[1] >= nur_in[1], lambda p: p[0] <= nur_in[2], lambda p: p[1] <= nur_in[3])[seite]
                grenze = nur_in[seite]; achse = seite % 2
                for a, b in zip(pts, pts[1:] + pts[:1]):
                    if drin(b):
                        if not drin(a): neu.append(schnitt(a, b, achse, grenze))
                        neu.append(b)
                    elif drin(a): neu.append(schnitt(a, b, achse, grenze))
                pts = neu
                if len(pts) < 3: return None
        v = [(px, py, gelaende_z(px, py) + hoch) for (px, py) in pts]
        return netz(name, v, [tuple(range(len(v)))], m, samm)

    def schnitt(a, b, achse, grenze):
        t = (grenze - a[achse]) / (b[achse] - a[achse]); return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    sr = schattenrichtung()

    def fussschatten(name, x, y, r, laenge=1.5, breite=0.9, versatz=0.9):
        """Fußschatten (ART_BIBLE §3.5): flache, harte Form in Schattenfarbe knapp über dem Boden, in Sonnenrichtung versetzt, damit
        Bäume, Büsche und Laternen nicht aufgeklebt wirken. Auf der Wiese unter Wegen und Vorplatz (hoch 0,012), auf dem Vorplatz
        ein eigener Zuschnitt in Pflasterfarbe darüber (0,028, unter dem Parkweg 0,03)."""
        cx, cy = x + sr[0] * r * versatz, y + sr[1] * r * versatz; dreh = math.atan2(sr[1], sr[0])
        ellipse(name, cx, cy, r * laenge, r * breite, dreh, "schatten_wiese", hoch=0.012)
        ellipse(name + " Pflaster", cx, cy, r * laenge, r * breite, dreh, "schatten_pflaster", hoch=0.028, nur_in=VORPLATZ)

    def entlang(punkte, s):
        """Punkt und Richtung `s` Meter nach dem Anfang eines Streckenzugs."""
        for p0, p1 in zip(punkte, punkte[1:]):
            l = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            if s <= l: return (p0[0] + (p1[0] - p0[0]) * s / l, p0[1] + (p1[1] - p0[1]) * s / l), ((p1[0] - p0[0]) / l, (p1[1] - p0[1]) / l)
            s -= l
        return punkte[-1], (1.0, 0.0)

    flaeche("Vorplatz", *VORPLATZ, "pflaster")
    for name, weg in (("Parkweg", PARKWEG), ("Parkweg West", PARKWEG_WEST)):   # Kiesweg 2,5 m (Linoleum warm, eine Stufe dunkler als
        band(name, weg, WEG["breite"], "weg")                                      # Papier: er war die hellste Fläche im Bild und zog
        for s in (1, -1):                                                           # das Auge vom Haus weg), beidseitig eine Sand-Kante
            band(f"{name} Kante {'links' if s > 0 else 'rechts'}", weg, WEG["kante"], "kante", hoch=0.035, versatz=s * (WEG["breite"] + WEG["kante"]) / 2)
    band("Klinikstrasse", KLINIKSTRASSE, 6.0, "asphalt")
    band("Rettungszufahrt", RETTUNGSZUFAHRT, 5.0, "asphalt")
    band("Fluss", FLUSS["punkte"], FLUSS["breite"], "fluss", hoch=0.05)
    flaeche("Abstellflaeche Rettung", 91.2, -7.0, 100.0, 2.0, "asphalt")
    flaeche("Parkplatz Personal", *PARKPLATZ, "asphalt")
    flaeche("Terrasse Cafeteria", 36.0, 16.0, 50.4, 20.0, "pflaster")
    kiste("Hecke Parkplatz", 69.0, 19.0, 101.0, 20.0, 0.0, 1.6, "hecke", "Umgebung")

    for i, (weg, s) in enumerate(LATERNEN):                        # Laternen: Mast Petrol, Kopf mit warmem Glas (brennt noch um 06:40) und Kappe
        (x, y), (tx, ty) = entlang(PARKWEG_WEST if weg == "west" else PARKWEG[1:], s)
        x, y = x - ty * 1.6, y + tx * 1.6; z = gelaende_z(x, y); h, kopf = LATERNE["hoehe"], LATERNE["kopf"]
        einordnen(wz.zylinder(0.06, h, (x, y, z + h / 2), M["petrol"], "hinten", v=8, name=f"Laterne {i + 1} Mast"), "Laternen")
        kiste(f"Laterne {i + 1} Kopf", x - kopf / 2, y - kopf / 2, x + kopf / 2, y + kopf / 2, z + h, z + h + kopf * 0.8, "fenster_warm", "Laternen")
        kiste(f"Laterne {i + 1} Kappe", x - kopf * 0.6, y - kopf * 0.6, x + kopf * 0.6, y + kopf * 0.6, z + h + kopf * 0.8, z + h + kopf * 0.95, "petrol", "Laternen")
        fussschatten(f"Laterne {i + 1} Schatten", x, y, 0.5, laenge=1.6, breite=0.6, versatz=1.0)
    # Rettungswagen (RTW): Kasten mit Fahrerhaus (Front −y, zur Kamera), Räder, Windschutzscheibe, Rost-Streifen an Seite und Front
    r = RTW; zr_ = gelaende_z(r["x0"], r["y1"]); kab = r["y0"] + 1.6
    kiste("RTW Kasten", r["x0"], kab, r["x1"], r["y1"], zr_ + 0.5, zr_ + r["h"] + 0.5, "rtw", "Umgebung", fase=0.06)
    kiste("RTW Fahrerhaus", r["x0"] + 0.05, r["y0"], r["x1"] - 0.05, kab + 0.05, zr_ + 0.5, zr_ + 1.95, "rtw", "Umgebung", fase=0.08)
    kiste("RTW Scheibe", r["x0"] + 0.3, r["y0"] - 0.03, r["x1"] - 0.3, r["y0"] + 0.01, zr_ + 1.2, zr_ + 1.85, "glas", "Umgebung")
    kiste("RTW Streifen Seite", r["x0"] - 0.02, kab + 0.1, r["x0"] + 0.02, r["y1"] - 0.1, zr_ + 1.0, zr_ + 1.5, "rost", "Umgebung")
    kiste("RTW Streifen Front", r["x0"] + 0.2, r["y0"] - 0.02, r["x1"] - 0.2, r["y0"] + 0.02, zr_ + 0.6, zr_ + 1.1, "rost", "Umgebung")
    for j, (xr, yr) in enumerate(((r["x0"] + 0.15, r["y0"] + 1.0), (r["x0"] + 0.15, r["y1"] - 1.0), (r["x1"] - 0.15, r["y0"] + 1.0), (r["x1"] - 0.15, r["y1"] - 1.0))):
        einordnen(wz.zylinder(0.38, 0.3, (xr, yr, zr_ + 0.38), M["stamm"], "hinten", dreh=(0, math.radians(90), 0), v=12, name=f"RTW Rad {j + 1}"), "Umgebung")
    # Lamellen NE: oben und unten eine Schiene, damit das Raster von (a) aus als Schirm liest (sonst dünne Striche neben Trakt N)
    for name, z0 in (("Lamellenschiene NE unten", 0.2), ("Lamellenschiene NE oben", N["geschosse"] * GESCHOSS - 0.42)):
        kiste(name, N["x1"] + 0.18, AUFNAHME_GLAS["y0"], N["x1"] + 0.34, AUFNAHME_GLAS["y1"], z0, z0 + 0.14, "lamelle", "Trakt N EG")
    # Waldtor: zwei Putzpfeiler mit Ziegeldächlein, Lattentor
    tx, ty = WALDTOR; tz = gelaende_z(tx, ty)
    for s in (-1.4, 1.4):
        kiste(f"Torpfeiler {'links' if s < 0 else 'rechts'}", tx + s - 0.3, ty - 0.3, tx + s + 0.3, ty + 0.3, tz, tz + 2.4, "putz", "Umgebung")
        kiste("Torpfeiler Dach", tx + s - 0.45, ty - 0.45, tx + s + 0.45, ty + 0.45, tz + 2.4, tz + 2.7, "ziegel", "Umgebung")
    kiste("Lattentor", tx - 1.1, ty - 0.04, tx + 1.1, ty + 0.04, tz + 0.2, tz + 1.5, "holz", "Umgebung")
    for i in range(7):                                             # Lattenzaun beidseits des Tors
        x = 36 + i * 4
        if abs(x + 1.5 - tx) > 2.5: kiste(f"Zaun {i + 1}", x, ty - 0.03, x + 3.0, ty + 0.03, tz + 0.2, tz + 1.3, "holz", "Umgebung")

    # ---------------- Bäume: Stamm mit Astansatz, Kronen aus überlappenden Kugeln, Nadelbäume in Etagen ----------------
    def vereinen(teile, name):
        """Mehrere Netze zu einem Objekt (eine Krone = ein Objekt; Freestyle zeichnet nur die sichtbare Silhouette)."""
        bpy.ops.object.select_all(action='DESELECT')
        for o in teile: o.select_set(True)
        bpy.context.view_layer.objects.active = teile[0]; bpy.ops.object.join()
        o = bpy.context.object; o.name = name
        return o

    def krone_kugeln(name, x, y, zc, r, dz_spanne, zr, n, m, flach=(0.78, 0.95)):
        """n überlappende, verschieden große Kugeln um (x, y, zc), leicht gedrückt, plus eine Kugel als Wipfel."""
        teile = []
        for i in range(n):
            rr = r * zr.uniform(0.45, 0.72); ang = zr.uniform(0, 2 * math.pi); d = (r - rr) * zr.uniform(0.35, 1.0)
            k = wz.kugel(rr, (x + math.cos(ang) * d, y + math.sin(ang) * d, zc + zr.uniform(-dz_spanne, dz_spanne)), M[m], "hinten", name=name)
            k.scale = (1, 1, zr.uniform(*flach)); bpy.ops.object.transform_apply(scale=True); teile.append(k)
        rw = r * 0.55
        k = wz.kugel(rw, (x + zr.uniform(-0.2, 0.2) * r, y + zr.uniform(-0.2, 0.2) * r, zc + dz_spanne + rw * 0.35), M[m], "hinten", name=name)
        k.scale = (1, 1, 0.85); bpy.ops.object.transform_apply(scale=True); teile.append(k)
        return vereinen(teile, name)

    def baum(name, x, y, r, art="laub", m="laub", samm="Baeume", hoehe=None, z=None, stammanteil=None):
        """laub: Stamm sichtbar, zwei Astansätze, Krone aus 5–7 Kugeln. foehre: hoher Stamm, lichter Schirm aus drei
        flachen Kugeln. fichte: vier gestapelte Kegel mit Lücken. Zufall je Baum aus dem Namen (reproduzierbar)."""
        zr = random.Random(name)
        if z is None: z = gelaende_z(x, y); fussschatten(name + " Schatten", x, y, r)    # nur Bäume auf dem Gelände (nicht im Kübel)
        if art == "laub":
            h = hoehe or r * 2.6; hs = h * (stammanteil or 0.36); rs = max(0.12, r * 0.07)   # Waldbäume: Krone tiefer (0,2), sonst stehen 8-m-Stämme als „Pfähle" neben dem Haus
            stamm = wz.zylinder(rs, hs + 0.4, (x, y, z + (hs + 0.4) / 2), M["stamm"], "hinten", v=8, name=name + " Stamm")
            aeste = [stamm]
            for j in range(0 if stammanteil else 2):               # zwei Äste schräg in die Krone (Waldbäume: keine, die Gabel ragte unter der Krone hervor)
                ang = zr.uniform(0, 2 * math.pi); neig = math.radians(zr.uniform(28, 42)); la = r * 0.55
                dreh = (neig * math.sin(ang), -neig * math.cos(ang), 0)
                mitte = (x + math.sin(neig) * la / 2 * math.cos(ang), y + math.sin(neig) * la / 2 * math.sin(ang), z + hs + math.cos(neig) * la / 2)
                aeste.append(wz.zylinder(rs * 0.5, la, mitte, M["stamm"], "hinten", dreh=dreh, v=6, name=name + " Ast"))
            einordnen(vereinen(aeste, name + " Stamm"), samm)
            zc = z + hs + (h - hs) * 0.5
            krone = krone_kugeln(name, x, y, zc, r, (h - hs) * 0.22, zr, 5 + zr.randint(0, 2), m)
            if stammanteil:                                        # Waldbäume: eine Unterkrone direkt über dem Stammende, damit kein langer Stamm frei steht
                unten = wz.kugel(r * 0.7, (x, y, z + hs + r * 0.55), M[m], "hinten", name=name); unten.scale = (1, 1, 0.8)
                bpy.ops.object.transform_apply(scale=True); krone = vereinen([krone, unten], name)
            einordnen(krone, samm)
        elif art == "foehre":
            h = hoehe or r * 3.4; hs = h * 0.62; rs = max(0.14, r * 0.08)
            einordnen(wz.zylinder(rs, hs + 0.3, (x + zr.uniform(-0.3, 0.3), y, z + (hs + 0.3) / 2), M["stamm"], "hinten", v=8, name=name + " Stamm"), samm)
            einordnen(krone_kugeln(name, x, y, z + hs + (h - hs) * 0.45, r * 0.95, (h - hs) * 0.18, zr, 3, m, flach=(0.45, 0.6)), samm)
        elif art == "kahl":                                        # Spätherbst: junger Baum ohne Laub — Stamm und fünf kräftige Hauptäste mit Umriss,
            h = hoehe or r * 2.6; rs = max(0.14, r * 0.05)          # keine feinen Zweige (bei 17–30 px/m wurden sie zu Gekritzel); ein Objekt
            teile = [wz.zylinder(rs, h * 0.5, (x, y, z + h * 0.25), M["stamm"], "hinten", v=8, name=name + " Stamm")]
            for j in range(5):
                ang = j * 2 * math.pi / 5 + zr.uniform(-0.3, 0.3); neig = math.radians(zr.uniform(22, 42)); la = h * zr.uniform(0.45, 0.6)
                z0_ = z + h * zr.uniform(0.4, 0.5); dreh = (neig * math.sin(ang), -neig * math.cos(ang), 0)
                mitte = (x + math.sin(neig) * la / 2 * math.cos(ang), y + math.sin(neig) * la / 2 * math.sin(ang), z0_ + math.cos(neig) * la / 2)
                teile.append(wz.zylinder(rs * 0.55, la, mitte, M["stamm"], "hinten", dreh=dreh, v=6, name=name + " Ast"))
            einordnen(vereinen(teile, name), samm)
        else:                                                      # fichte: Etagen
            h = hoehe or r * 3.2; hs = h * 0.18; rs = max(0.12, r * 0.07)
            einordnen(wz.zylinder(rs, h * 0.6, (x, y, z + h * 0.3), M["stamm"], "hinten", v=8, name=name + " Stamm"), samm)
            teile = []; etagen = 4; z0 = z + hs
            for j in range(etagen):
                rj = r * (1.0 - 0.2 * j) * zr.uniform(0.9, 1.1); hj = (h - hs) / etagen * 1.45
                zj = z0 + (h - hs) / etagen * j
                teile.append(wz.kegel(rj, rj * 0.1 if j < etagen - 1 else 0.0, hj, (x, y, zj + hj / 2), M[m], "hinten", v=9, name=name))
            einordnen(vereinen(teile, name), samm)

    def busch(name, x, y, r, m="laub", samm="Buesche"):
        """Busch: Kugelhaufen, Mitte nur 0,3 r über dem Boden (Bodenkontakt, keine schwebende Wolke), dazu ein Fußschatten."""
        zr = random.Random(name); z = gelaende_z(x, y)
        einordnen(krone_kugeln(name, x, y, z + r * 0.3, r, r * 0.15, zr, 3 + zr.randint(0, 2), m, flach=(0.6, 0.8)), samm)
        fussschatten(name + " Schatten", x, y, r, laenge=1.3, breite=0.8, versatz=0.6)

    def hecke(name, p0, p1, hoehe=1.1, dicke=0.9):
        """Geschnittene Hecke: gedrehter Quader mit stark gerundeter Oberkante (Fase 0,3; ein scharfer Quader las sich als Betonmauer,
        eine Kugelkette als Raupe). Kein Schlagschatten (Sammlung Buesche), dafür ein Fußschatten-Viereck in Sonnenrichtung."""
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]; l = math.hypot(dx, dy); w = math.atan2(dy, dx)
        xm, ym = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2; z0 = min(gelaende_z(*p0), gelaende_z(*p1)) - 0.15
        o = wz.kiste((l, dicke, hoehe + 0.15), (xm, ym, z0 + (hoehe + 0.15) / 2), M["hecke"], "hinten", fase=0.3, dreh=(0, 0, w), name=name)
        einordnen(o, "Buesche")
        r = dicke / 2; nx_, ny_ = -dy / l * r * 1.1, dx / l * r * 1.1; vs = (sr[0] * 0.8, sr[1] * 0.8)
        sch = [(p0[0] + nx_ + vs[0], p0[1] + ny_ + vs[1]), (p1[0] + nx_ + vs[0], p1[1] + ny_ + vs[1]), (p1[0] - nx_ + vs[0], p1[1] - ny_ + vs[1]), (p0[0] - nx_ + vs[0], p0[1] - ny_ + vs[1])]
        netz(name + " Schatten", [(x, y, gelaende_z(x, y) + 0.012) for x, y in sch], [(0, 1, 2, 3)], "schatten_wiese", "Gelaende")

    for i, (p0, p1) in enumerate(HECKEN): hecke(f"Hecke Parkweg {i + 1}", p0, p1)

    def bank(name, x, y, w, samm="Buesche"):
        """Ruhebank: Petrol-Gestell, vier Sitz- und zwei Lehnenlatten Holz; `w` = Richtung der Sitzfläche (rad), Lehne links davon."""
        z = gelaende_z(x, y); tx, ty = math.cos(w), math.sin(w); nx_, ny_ = -ty, tx
        def teil(teilname, groesse, laengs, quer, hoch, m):
            einordnen(wz.kiste(groesse, (x + tx * laengs + nx_ * quer, y + ty * laengs + ny_ * quer, z + hoch), M[m], "hinten", dreh=(0, 0, w), name=f"{name} {teilname}"), samm)
        for a in (-0.7, 0.7):                                      # Seitenwangen: Fuß und Lehnenstütze
            teil("Wange", (0.05, 0.5, 0.42), a, 0.0, 0.21, "petrol"); teil("Stuetze", (0.05, 0.05, 0.45), a, 0.2, 0.62, "petrol")
        for q in (-0.19, -0.065, 0.065, 0.19): teil("Latte", (1.7, 0.1, 0.04), 0.0, q, 0.44, "holz")
        for h in (0.6, 0.78): teil("Lehnenlatte", (1.7, 0.04, 0.1), 0.0, 0.22, h, "holz")
        fussschatten(f"{name} Schatten", x, y, 0.9, laenge=1.2, breite=0.5, versatz=0.5)

    for i, (weg, s) in enumerate(BAENKE_WEG):                      # Ruhebank 2,2 m links des Parkwegs, längs zum Weg, Lehne zur NW-Seite (Blick ins Tal)
        (x, y), (tx, ty) = entlang(PARKWEG_WEST if weg == "west" else PARKWEG[1:], s)
        bank(f"Bank Parkweg {i + 1}", x - ty * 2.2, y + tx * 2.2, math.atan2(ty, tx))
    for i, (x, y, r) in enumerate(LINDEN): baum(f"Linde {i + 1}", x, y, r, m=HERBST["linden"][i % 2])   # Spätherbst: gelb und rostig
    baum("Kastanie", *KASTANIE, m=HERBST["kastanie"])
    for i, (x, y, r, m) in enumerate(JUNGBAEUME): baum(f"Jungbaum {i + 1}", x, y, r, m=m, hoehe=r * 3.3)   # schlanker Stamm, lockere runde Krone
    for i, (x, y, r) in enumerate(KAHLE_BAEUME): baum(f"Kahler Baum {i + 1}", x, y, r, "kahl")
    for i, (x, y, r) in enumerate(PLATANEN): baum(f"Platane {i + 1}", x, y, r)
    for i, (x, y, r) in enumerate(BUESCHE): busch(f"Busch {i + 1}", x, y, r)
    for i, (x, y, r) in enumerate(UNTERHOLZ): busch(f"Unterholz {i + 1}", x, y, r, "wald_nah")   # Waldrand hinter dem Haus: verdeckt die Stämme links des Westgiebels

    # ---------------- Hof (25.10.2026): Zufahrt, Stellplätze mit Autos, Figuren, Wegweiser, Haltestelle, Raucherecke, Herbstlaub ----------------
    band("Zufahrt", ZUFAHRT, 4.5, "pflaster", hoch=0.03)
    for s_ in (1, -1): band(f"Zufahrt Kante {'links' if s_ > 0 else 'rechts'}", ZUFAHRT, WEG["kante"], "kante", hoch=0.035, versatz=s_ * (4.5 + WEG["kante"]) / 2)
    flaeche("Stellplaetze", *STELLPLAETZE["flaeche"], "asphalt", hoch=0.025)
    for i, x in enumerate((46.9, 49.7)):                           # Markierung zwischen den Stellplätzen
        kiste(f"Stellplatz Linie {i + 1}", x - 0.05, STELLPLAETZE["flaeche"][1] + 0.3, x + 0.05, STELLPLAETZE["flaeche"][3] - 0.3, -SOCKEL + 0.03, -SOCKEL + 0.04, "kante", "Gelaende")

    def auto(name, x, y, m):
        """Pkw längs y (Front nach −y): Wanne, Kabine mit Glas, Räder; Material = Lackfarbe. Wirft echten Schatten (Fahrzeug)."""
        z = gelaende_z(x, y)
        kiste(f"{name} Wanne", x - 0.9, y - 2.2, x + 0.9, y + 2.2, z + 0.3, z + 0.95, m, "Umgebung", fase=0.08)
        kiste(f"{name} Kabine", x - 0.8, y - 1.0, x + 0.8, y + 1.3, z + 0.95, z + 1.5, "glas", "Umgebung", fase=0.06)
        kiste(f"{name} Dach", x - 0.78, y - 0.75, x + 0.78, y + 1.1, z + 1.5, z + 1.56, m, "Umgebung")
        for j, (xr, yr) in enumerate(((x - 0.85, y - 1.4), (x - 0.85, y + 1.4), (x + 0.85, y - 1.4), (x + 0.85, y + 1.4))):
            einordnen(wz.zylinder(0.32, 0.22, (xr, yr, z + 0.32), M["stamm"], "hinten", dreh=(0, math.radians(90), 0), v=12, name=f"{name} Rad {j + 1}"), "Umgebung")

    for i, (x, y, m) in enumerate(STELLPLAETZE["autos"]): auto(f"Auto {i + 1}", x, y, m)

    def figur(name, x, y, blick, m="figur"):
        """Silhouette: Kapsel 1,7 m (Rumpf, Kopf, zwei Beine als ein schmalerer Zylinder), kein Schlagschatten, kleiner Fußschatten."""
        z = gelaende_z(x, y)
        einordnen(wz.zylinder(0.15, 0.85, (x, y, z + 0.425), M[m], "hinten", v=10, name=f"{name} Beine"), "Figuren")
        einordnen(wz.kiste((0.42, 0.24, 0.62), (x, y, z + 1.16), M[m], "hinten", dreh=(0, 0, blick), fase=0.08, name=f"{name} Rumpf"), "Figuren")
        einordnen(wz.kugel(0.12, (x, y, z + 1.6), M[m], "hinten", name=f"{name} Kopf"), "Figuren")
        fussschatten(f"{name} Schatten", x, y, 0.3, laenge=1.4, breite=0.7, versatz=0.8)

    for i, (x, y, blick) in enumerate(FIGUREN): figur(f"Figur {i + 1}", x, y, blick, "rtw" if i == 1 else "figur")   # eine im weißen Kittel

    wwz = WEGWEISER; (wx, wy) = wwz["ort"]; wzz = gelaende_z(wx, wy)                 # Wegweiser an der Kehre: Pfosten, zwei weiße Schilder mit Pfeil und Textbalken
    einordnen(wz.zylinder(0.05, wwz["hoehe"], (wx, wy, wzz + wwz["hoehe"] / 2), M["zink"], "hinten", v=8, name="Wegweiser Pfosten"), "Hof")
    for i, (zs, richtung) in enumerate(wwz["schilder"]):
        kiste(f"Wegweiser Schild {i + 1}", wx - 0.7, wy - 0.03, wx + 0.7, wy + 0.03, wzz + zs, wzz + zs + 0.4, "rtw", "Hof")
        sx = wx + richtung * 0.42; sz = wzz + zs + 0.2
        kiste(f"Wegweiser Pfeil {i + 1}", sx - 0.14, wy - 0.045, sx + 0.14, wy - 0.035, sz - 0.03, sz + 0.03, "schrift", "Hof")
        netz(f"Wegweiser Pfeilspitze {i + 1}", [(sx + richtung * 0.1, wy - 0.045, sz - 0.11), (sx + richtung * 0.1, wy - 0.045, sz + 0.11), (sx + richtung * 0.26, wy - 0.045, sz)], [(0, 1, 2)], "schrift", "Hof")
        kiste(f"Wegweiser Text {i + 1}", wx - 0.55 + (0.2 if richtung > 0 else 0.0), wy - 0.045, wx + 0.2 + (0.2 if richtung > 0 else 0.0), wy - 0.035, sz - 0.03, sz + 0.03, "schrift", "Hof")

    hs_ = HALTESTELLE; hz = gelaende_z(hs_["x"], (hs_["y0"] + hs_["y1"]) / 2)         # Haltestelle an der Klinikstraße: Glashäuschen und H-Schild
    for yy in (hs_["y0"] + 0.1, hs_["y1"] - 0.1):
        kiste("Haltestelle Pfosten", hs_["x"] - 0.06, yy - 0.06, hs_["x"] + 0.06, yy + 0.06, hz, hz + hs_["hoehe"], "zink", "Hof")
    kiste("Haltestelle Dach", hs_["x"] - 0.3, hs_["y0"] - 0.2, hs_["x"] + hs_["tiefe"], hs_["y1"] + 0.2, hz + hs_["hoehe"], hz + hs_["hoehe"] + 0.15, "stein", "Hof")
    kiste("Haltestelle Rueckwand", hs_["x"] + hs_["tiefe"] - 0.06, hs_["y0"], hs_["x"] + hs_["tiefe"], hs_["y1"], hz + 0.3, hz + hs_["hoehe"] - 0.1, "glas", "Hof")
    kiste("Haltestelle Bank", hs_["x"] + hs_["tiefe"] - 0.6, hs_["y0"] + 0.4, hs_["x"] + hs_["tiefe"] - 0.2, hs_["y1"] - 0.4, hz + 0.4, hz + 0.46, "holz", "Hof")
    sx, sy = hs_["schild"]; sz = gelaende_z(sx, sy)
    einordnen(wz.zylinder(0.04, 2.6, (sx, sy, sz + 1.3), M["zink"], "hinten", v=8, name="Haltestelle Schildpfosten"), "Hof")
    einordnen(wz.zylinder(0.32, 0.04, (sx, sy, sz + 2.7), M["rtw"], "hinten", dreh=(0, math.radians(90), 0), v=16, name="Haltestelle Schild"), "Hof")
    kiste("Haltestelle H", sx - 0.04, sy - 0.12, sx + 0.04, sy + 0.12, sz + 2.6, sz + 2.8, "schrift", "Hof")

    bank("Raucherecke Bank", *RAUCHERECKE["bank"], math.radians(180))                 # Raucherecke an der SE-Ecke von Trakt N, Standascher
    ax, ay = RAUCHERECKE["ascher"]; az = gelaende_z(ax, ay)
    einordnen(wz.zylinder(0.12, 1.0, (ax, ay, az + 0.5), M["zink"], "hinten", v=10, name="Standascher"), "Hof")
    einordnen(wz.zylinder(0.14, 0.06, (ax, ay, az + 1.03), M["petrol"], "hinten", v=10, name="Standascher Deckel"), "Hof")

    lz = random.Random(11); lb = LAUB                                               # Herbstlaub: kleine Ellipsen in zwei Tönen auf Weg, Vorplatz und Wiese
    def laubfleck(name, x, y):
        ra = lz.uniform(*lb["radius"]); m = "laub_boden" if lz.random() < 0.55 else "laub_boden_hell"
        ellipse(name, x, y, ra, ra * lz.uniform(0.5, 0.75), lz.uniform(0, math.pi), m, hoch=0.045, n=8)
    s0, s1, n_, streu = lb["weg"]
    for i in range(n_):
        (px, py), (tx, ty) = entlang(PARKWEG_WEST, lz.uniform(s0, s1)); q = lz.uniform(-streu, streu) * (1.4 if lz.random() < 0.3 else 1.0)
        laubfleck(f"Laub Weg {i + 1}", px - ty * q, py + tx * q)
    for j, (x, y, r) in enumerate(LINDEN):
        for i in range(lb["je_linde"]):
            a, d = lz.uniform(0, 2 * math.pi), lb["linden"] * math.sqrt(lz.random())
            laubfleck(f"Laub Linde {j + 1} {i + 1}", x + math.cos(a) * d + sr[0] * 1.5, y + math.sin(a) * d + sr[1] * 1.5)
    for i in range(lb["vorplatz"]):
        laubfleck(f"Laub Vorplatz {i + 1}", lz.uniform(VORPLATZ[0], VORPLATZ[2]), lz.uniform(VORPLATZ[1], VORPLATZ[3]))
    for i, (x, y) in enumerate(((38, 24), (54, 20))):
        kiste(f"Holzbank Garten {i + 1}", x - 0.9, y - 0.25, x + 0.9, y + 0.25, 0.0, 0.45, "holz", "Umgebung")
    for i, x in enumerate((25.0, 36.2)): bank(f"Bank Vorplatz {i + 1}", x, -7.8, 0.0)   # Bänke am Vorplatz, Blick nach Südost
    fr = FAHRRAEDER; zf_ = gelaende_z(fr["buegel"][0], fr["y"])                            # Anlehnbügel (flache Platten, lesbar als Bügel) und zwei Räder
    for i, x in enumerate(fr["buegel"]):
        kiste(f"Fahrradbuegel {i + 1}", x - 0.3, fr["y"] - 0.025, x + 0.3, fr["y"] + 0.025, zf_, zf_ + 0.8, "stuetze", "Hof")
    for i, (x, m) in enumerate(fr["raeder"]):
        for dy in (-0.52, 0.52):
            einordnen(wz.zylinder(0.33, 0.04, (x, fr["y"] + dy, zf_ + 0.33), M[m], "hinten", dreh=(0, math.radians(90), 0), v=16, name=f"Fahrrad {i + 1} Rad"), "Hof")
        kiste(f"Fahrrad {i + 1} Rahmen", x - 0.02, fr["y"] - 0.45, x + 0.02, fr["y"] + 0.45, zf_ + 0.45, zf_ + 0.75, m, "Hof")
    zufall = random.Random(7)
    # Wiesenflecken: hellere Ellipsen auf der Wiese (ohne Linie, ohne Schattierung), folgen dem Gelände
    wf = WIESENFLECKEN; fx0, fy0, fx1, fy1 = wf["bereich"]
    for i in range(wf["anzahl"]):
        cx, cy = zufall.uniform(fx0, fx1), zufall.uniform(fy0, fy1); ra = zufall.uniform(*wf["radius"]); rb = ra * zufall.uniform(0.35, 0.7)
        ellipse(f"Wiesenfleck {i + 1}", cx, cy, ra, rb, zufall.uniform(0, math.pi), "wiese_hell", hoch=0.008)   # unter den Fußschatten (0,012)
    # Wald (§5): nahes Band als dichte Gruppe in zwei Reihen (Laub, Föhren, Fichten gemischt), dahinter Silhouettenbänder
    def herbstfarbe(art):                                          # Spätherbst: ein Teil der Laubkronen gelb oder rostig, Nadeln bleiben
        if art != "laub" or zufall.random() > HERBST["wald_anteil"]: return "wald_nah"
        return "laub_gelb" if zufall.random() < 0.6 else "laub_rost"
    wn = WALD_NAH
    for reihe, (y0, y1) in enumerate(wn["reihen"]):
        x = wn["x0"] + reihe * wn["abstand"] / 2
        while x < wn["x1"]:
            xx = x + zufall.uniform(-1.5, 1.5); yy = zufall.uniform(y0, y1); w = zufall.random()
            art = "laub" if w < 0.5 else ("foehre" if w < 0.8 else "fichte")
            baum(f"Wald {reihe + 1} {x:g}", xx, yy, zufall.uniform(3.5, 5.5), art, herbstfarbe(art), hoehe=zufall.uniform(*wn["hoehe"]), stammanteil=0.14)
            x += wn["abstand"]
    ww = WALD_WEST
    for x in range(int(ww["x0"]), int(ww["x1"]), int(ww["abstand"][0])):     # Wald westlich (x < −20), rahmt Render (a) links
        for y in range(int(ww["y0"]), int(ww["y1"]), int(ww["abstand"][1])):
            w = zufall.random(); art = "laub" if w < 0.5 else ("foehre" if w < 0.8 else "fichte")
            baum(f"Wald W {x} {y}", x + zufall.uniform(-2, 2), y + zufall.uniform(-2, 2), zufall.uniform(3.5, 5.5), art, herbstfarbe(art), hoehe=zufall.uniform(*ww["hoehe"]), stammanteil=0.14)

    def waldband(name, y, x0, x1, m, hoehen):
        """Silhouettenband: ein senkrechtes Netz bei y, Oberkante = Umriss überlappender Kronen und Wipfel."""
        baeume = []; x = x0
        while x < x1:
            r = zufall.uniform(4.0, 7.0); baeume.append((x + zufall.uniform(-1, 1), r, zufall.uniform(*hoehen), zufall.random() < 0.4)); x += zufall.uniform(4.0, 7.0)
        v, f = [], []; xs = [x0 + i for i in range(int(x1 - x0) + 1)]
        for i, x in enumerate(xs):
            basis = gelaende_z(x, y); top = 12.0
            for (bx, r, h, nadel) in baeume:
                d = abs(x - bx)
                if nadel: top = max(top, h - d * (h * 0.5 / r)) if d < 2 * r else top
                elif d < r: top = max(top, h - r * 0.9 + math.sqrt(r * r - d * d) * 0.9)
            top *= min(1.0, (x1 - x) / WALDBAND_AUSLAUF, 1.0) if x > x1 - WALDBAND_AUSLAUF else 1.0   # Band läuft nach Osten aus
            v.append((x, y, basis - 3.0)); v.append((x, y, basis + max(top, 0.5)))
            if i: f.append((2 * i - 2, 2 * i, 2 * i + 1, 2 * i - 1))
        return netz(name, v, f, m, "Baeume")

    for i, (y, x0, x1, m, hoehen) in enumerate(WALDBAENDER): waldband(f"Waldband {i + 1}", y, x0, x1, m, hoehen)

    # ---------------- Stadt im Tal: ferne Kulisse (Papier/Sand, ohne Linie), Hügel ----------------
    def stadt(nr, st):
        zr = random.Random(100 + nr)
        for i in range(st["haeuser"]):
            x = zr.uniform(st["x0"], st["x1"]); schraeg = st.get("neigung", 0.0) * (x - st["x0"])
            gr = st.get("groesse", 1.0)
            y = zr.uniform(st["y0"], st["y1"]) + schraeg; b = zr.uniform(8, 22) * gr; t = zr.uniform(7, 14) * gr
            if zr.random() < 0.5: b, t = t, b
            zg = gelaende_z(x + b / 2, y + t / 2); h = zr.uniform(*st.get("hoehe", (6.0, 11.0))); m = "stadt" if i % 3 else "stadt_sand"
            kiste(f"Stadt {nr} Haus {i + 1}", x, y, x + b, y + t, zg - 1.0, zg + h, m, "Stadt")
            md = "stadt_dach"
            if b >= t:                                             # Satteldach längs x
                netz(f"Stadt {nr} Dach {i + 1}", [(x, y, zg + h), (x + b, y, zg + h), (x + b, y + t, zg + h), (x, y + t, zg + h), (x, y + t / 2, zg + h + t * 0.45), (x + b, y + t / 2, zg + h + t * 0.45)],
                     [(0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)], md, "Stadt")
            else:
                netz(f"Stadt {nr} Dach {i + 1}", [(x, y, zg + h), (x + b, y, zg + h), (x + b, y + t, zg + h), (x, y + t, zg + h), (x + b / 2, y, zg + h + b * 0.45), (x + b / 2, y + t, zg + h + b * 0.45)],
                     [(3, 2, 5, 4), (1, 0, 4, 5), (0, 3, 4), (2, 1, 5)], md, "Stadt")
        for j, (x, y, art) in enumerate(st["tuerme"]):            # Kirchtürme: einer mit Helm, einer mit Zwiebelhaube
            zg = gelaende_z(x + 3, y + 3)
            kiste(f"Stadt {nr} Kirchturm {j + 1}", x, y, x + 5, y + 5, zg - 1.0, zg + 24, "stadt_sand", "Stadt")
            if art == "helm": einordnen(wz.kegel(3.8, 0.0, 11, (x + 2.5, y + 2.5, zg + 29.5), M["stadt_dach"], "hinten", v=8, name=f"Stadt {nr} Helm"), "Stadt")
            else:
                einordnen(wz.kugel(3.4, (x + 2.5, y + 2.5, zg + 26.5), M["stadt_dach"], "hinten", name=f"Stadt {nr} Zwiebel"), "Stadt")
                einordnen(wz.kegel(1.3, 0.0, 5, (x + 2.5, y + 2.5, zg + 31.5), M["stadt_dach"], "hinten", v=8, name=f"Stadt {nr} Zwiebel Spitze"), "Stadt")

    for nr, st in enumerate(STADT): stadt(nr + 1, st)
    for i, (x, y, r, h) in enumerate(HUEGEL):                      # Hügel: Kugeln, nur die oberen h Meter ragen heraus
        zg = gelaende_z(x, y)
        einordnen(wz.kugel(r, (x, y, zg - r + h), M["wald_fern"], "hinten", name=f"Huegel {i + 1}"), "Stadt")

    # ---------------- Sockel und Decken ----------------
    kiste("Sockel A", A["x0"], A["y0"], A["x1"], A["y1"], -SOCKEL, 0.0, "sockel", "Trakt A EG")
    kiste("Sockel Risalit SE", *RISALIT_SE, -SOCKEL, 0.0, "sockel", "Trakt A EG")
    for e in ECKRISALITE:
        if "EG" in e["geschosse"]: kiste(f"Sockel Eckrisalit {e['name']}", e["x0"], -ECK_VOR, e["x1"], 0.0, -SOCKEL, 0.0, "sockel", "Trakt A EG")
    kiste("Sockel Risalit NW", *RISALIT_NW, -SOCKEL, 0.0, "sockel", "Trakt A EG")
    kiste("Sockel N", N["x0"], N["y0"], N["x1"], N["y1"], -SOCKEL, 0.0, "sockel", "Trakt N EG")

    def decke(name, x0, y0, x1, y1, z_unten, samm, oben=None):
        z_oben = z_unten + (GESCHOSS - RAUMHOEHE["A" if "A" in samm else "N"])
        kiste(name, x0, y0, x1, y1, z_unten, min(z_oben, oben) if oben else z_oben, "decke", samm)

    for g, z in GESCHOSSE.items():
        samm = f"Trakt A {g}"
        decke(f"Decke A {g}", A["x0"], A["y0"], A["x1"], A["y1"], z + RAUMHOEHE["A"], samm)
        decke(f"Decke Risalit SE {g}", *RISALIT_SE, z + RAUMHOEHE["A"], samm)
        for e in ECKRISALITE:
            if g in e["geschosse"]: decke(f"Decke Eckrisalit {e['name']} {g}", e["x0"], -ECK_VOR, e["x1"], 0.0, z + RAUMHOEHE["A"], samm)
        decke(f"Decke Risalit NW {g}", *RISALIT_NW, z + RAUMHOEHE["A"], samm)
        if g != "2OG":
            decke(f"Decke N {g}", N["x0"], N["y0"], N["x1"], N["y1"], z + RAUMHOEHE["N"], f"Trakt N {g}")

    # ---------------- Außenwände mit Öffnungen ----------------
    def achsfenster():
        """Altbau-Fenster nach Achsen: (Geschoss, Wandachse, Lage, a0, a1, z0, z1)."""
        aus = []
        for g, z in GESCHOSSE.items():
            for k in range(1, ACHSEN + 1):
                xm = ACHSE * k - 1.8
                z0, z1 = z + FENSTER["bruestung"], z + FENSTER["bruestung"] + FENSTER["h"]
                if k in FENSTERPAARE:                                  # gekoppeltes Fenster: zwei Flügel um einen Pfosten
                    oeffnungen = [(xm - PAAR["pfosten"] / 2 - PAAR["b"], xm - PAAR["pfosten"] / 2), (xm + PAAR["pfosten"] / 2, xm + PAAR["pfosten"] / 2 + PAAR["b"])]
                else: oeffnungen = [(xm - FENSTER["b"] / 2, xm + FENSTER["b"] / 2)]
                im_risalit = RISALIT_SE[0] <= xm <= RISALIT_SE[2]
                im_eck = any(e["x0"] <= xm <= e["x1"] and g in e["geschosse"] for e in ECKRISALITE)
                lage_se = RISALIT_SE[1] if im_risalit else (-ECK_VOR if im_eck else A["y0"])
                art = "warm" if (g, k) in WARME_FENSTER else "glas"
                for (x0, x1) in oeffnungen:
                    if g == "EG" and im_risalit: pass                   # Portal und hohe Fenster (SONDERFENSTER)
                    else: aus.append((g, "y", lage_se, x0, x1, z0, z1, art))
                    if k not in BLIND_NW and not (RISALIT_NW[0] <= xm <= RISALIT_NW[2]):
                        aus.append((g, "y", A["y1"], x0, x1, z0, z1, "glas"))
        return aus

    FENSTER_ALLE = [("A", *f) for f in achsfenster()] + SONDERFENSTER + \
        [("A", "EG", "y", -3, PORTAL["x0"], PORTAL["x1"], 0.0, PORTAL["h"], "portal")]

    def aussenwand(trakt, g, achse, lage, a0, a1, innen_seite, oben=None):
        """Eine Außenwand (Wandachse 'x' oder 'y' bei `lage`, von a0 bis a1, ein Geschoss hoch), Öffnungen nach
        FENSTER_ALLE. `innen_seite` = +1, wenn der Raum auf der Plus-Seite der Wand liegt. `oben`: Oberkante statt
        Geschossdecke (Eckrisalit unter der verlängerten Dachfläche)."""
        z = GESCHOSSE[g]; d = A["aussen"] if trakt == "A" else N["aussen"]
        w0, w1 = (lage, lage + d) if innen_seite > 0 else (lage - d, lage)
        name = f"Aussenwand {trakt} {g} {achse}{lage:g} {a0:g}-{a1:g}"
        oeffnungen = []
        for (t, gg, ac, la, f0, f1, z0, z1, art) in FENSTER_ALLE:
            if t != trakt or gg != g or ac != achse or abs(la - lage) > 1e-6: continue
            if f1 <= a0 or f0 >= a1: continue
            oeffnungen.append((f0, f1, z0, z1))
            scheibe(trakt, g, achse, lage, f0, f1, z0, z1, art, innen_seite)
        m = "beton" if trakt == "N" else ("rustika" if g == "EG" else "putz")       # Neubau hell, Altbau-Sockelgeschoss gebändert
        if m == "rustika":                                                            # Fugen: flache Streifen zwischen den Fenstern (ohne Linie)
            frei = [(a0, a1)]
            for (f0, f1, z0, z1) in oeffnungen:
                neu_ = []
                for (b0, b1) in frei:
                    o0, o1 = f0 - FENSTERDEKOR["fasche"] - 0.02, f1 + FENSTERDEKOR["fasche"] + 0.02
                    if o1 <= b0 or o0 >= b1: neu_.append((b0, b1)); continue
                    if o0 > b0: neu_.append((b0, o0))
                    if o1 < b1: neu_.append((o1, b1))
                frei = neu_
            fw0, fw1 = (lage - RUSTIKA["vor"], lage) if innen_seite > 0 else (lage, lage + RUSTIKA["vor"])
            for (b0, b1) in frei:
                if b1 - b0 < 0.15: continue
                for zf in RUSTIKA["fugen"]:
                    if achse == "y": kiste("Fuge", b0, fw0, b1, fw1, z + zf, z + zf + RUSTIKA["hoehe"], "fuge", f"Trakt {trakt} {g}")
                    else: kiste("Fuge", fw0, b0, fw1, b1, z + zf, z + zf + RUSTIKA["hoehe"], "fuge", f"Trakt {trakt} {g}")
        return wandnetz(name, achse, w0, w1, a0, a1, z, oben or z + GESCHOSS, oeffnungen, m, f"Trakt {trakt} {g}")

    def scheibe(trakt, g, achse, lage, f0, f1, z0, z1, art, innen_seite):
        """Fenster in der Laibung (25.10.2026, Auftrag B). Altbau: Scheibe 0,14 m hinter der Flucht, davor weißer Rahmen mit Pfosten und
        Kämpfer (flache Streifen ohne Linie), außen Fasche und Sohlbank (Putzrahmen, ohne Linie); nach festem Zufall je Fenster ein grüner
        Rollladen in wechselnder Höhe (mit Linie an der Unterkante), eine Gardine oder ein nach außen geöffneter Flügel (Kastenfenster) —
        nur auf den Seiten, die Kamera (a) sieht. Neubau: Scheibe und dünner weißer Rahmen. Portal: Rundbogen (Zwickel), dunkle
        Holz-Doppeltür, Oberlicht warm."""
        FD = FENSTERDEKOR; tiefe = FD["tiefe"] * innen_seite; aussen = -innen_seite; d = 0.06
        m = {"glas": "glas", "portal": "fenster_warm", "tor": "tor", "warm": "fenster_warm"}[art]
        samm = f"Trakt {trakt} {g}"; sichtbar_a = (achse == "y" and lage <= 0) or (achse == "x" and lage <= 0)

        def box(name, a0, a1, zz0, zz1, w0, w1, mat, **kw):
            """Quader in Wandkoordinaten: a entlang der Wand, w quer (absolut), z."""
            return kiste(name, a0, w0, a1, w1, zz0, zz1, mat, samm, **kw) if achse == "y" else kiste(name, w0, a0, w1, a1, zz0, zz1, mat, samm, **kw)

        def quer(von, bis):                                        # Querschicht relativ zur Außenflucht, nach außen positiv (sortiert)
            return tuple(sorted((lage + aussen * von, lage + aussen * bis)))

        if art == "portal":
            R = PORTAL_DEKOR["bogen"]; um = (f0 + f1) / 2; zk = z1 - R; th = PORTAL_DEKOR["tuer_h"]
            for seite in (-1, 1):                                  # Bogenzwickel: Rechteck minus Viertelkreis, durch die ganze Wandstärke
                bogen = lambda winkel: [(um + R * math.cos(math.radians(a)), zk + R * math.sin(math.radians(a))) for a in winkel]
                if seite < 0: pts = [(um - R, zk), (um - R, z1), (um, z1)] + bogen(range(95, 180, 5))
                else: pts = [(um, z1), (um + R, z1), (um + R, zk)] + bogen(range(5, 90, 5))
                prisma(f"Portal Zwickel {'links' if seite < 0 else 'rechts'}", pts, achse, *sorted((lage, lage + innen_seite * A["aussen"])), "rustika", samm)
            box("Portal Oberlicht", f0, f1, th, z1, *quer(tiefe * aussen - d / 2, tiefe * aussen + d / 2), "fenster_warm")
            for (a0, a1) in ((f0, um - 0.02), (um + 0.02, f1)):
                box("Portal Tuerblatt", a0, a1, 0.0, th, *quer(tiefe * aussen - d / 2, tiefe * aussen + d / 2), "holz_dunkel")
            box("Portal Kaempfer", f0, f1, th - 0.05, th + 0.05, *quer(tiefe * aussen + d / 2, tiefe * aussen + d / 2 + 0.03), "sparren")
            for a in (um - 0.4, um + 0.4): box("Portal Griff", a - 0.03, a + 0.03, 1.0, 1.35, *quer(tiefe * aussen + d / 2, tiefe * aussen + d / 2 + 0.03), "zink")
            return
        box(f"Scheibe {achse}{lage:g} {f0:g} {g}", f0, f1, z0, z1, *quer(tiefe * aussen - d / 2, tiefe * aussen + d / 2), m)
        if trakt != "A" or art == "tor":                           # Neubau: dünner weißer Rahmen, sonst nichts
            r = 0.08; w = quer(tiefe * aussen + d / 2, tiefe * aussen + d / 2 + 0.03)
            for a in (f0, f1 - r): box("Rahmen", a, a + r, z0, z1, *w, "rahmen")
            for zz in (z0, z1 - r): box("Rahmen", f0, f1, zz, zz + r, *w, "rahmen")
            return
        zr = random.Random(f"{g}{achse}{lage:g}{f0:g}{z0:g}")
        r, p, k, fa, sb = FD["rahmen"], FD["pfosten"], FD["kaempfer"], FD["fasche"], FD["sohlbank"]
        h = z1 - z0; b = f1 - f0; t0 = tiefe * aussen + d / 2    # t0: Außenseite der Scheibe (relativ, nach außen positiv)
        # Fasche und Sohlbank bündig auf der Wandfläche
        wf = quer(0.0, 0.03)
        box("Fasche", f0 - fa, f0, z0, z1 + fa, *wf, "fasche"); box("Fasche", f1, f1 + fa, z0, z1 + fa, *wf, "fasche")
        box("Fasche", f0, f1, z1, z1 + fa, *wf, "fasche")
        box("Sohlbank", f0 - fa, f1 + fa, z0 - sb, z0, *quer(0.0, FD["sohlbank_vor"]), "fasche")
        # Rahmen: außen umlaufend, Pfosten in der Mitte (nur Einzelfenster), Kämpfer bei 68 % der Höhe
        wr = quer(t0 + 0.02, t0 + 0.05)
        for a in (f0, f1 - r): box("Rahmen", a, a + r, z0, z1, *wr, "rahmen")
        for zz in (z0, z1 - r): box("Rahmen", f0, f1, zz, zz + r, *wr, "rahmen")
        zk = z0 + h * FD["kaempfer_hoehe"]; box("Kaempfer", f0, f1, zk - k / 2, zk + k / 2, *wr, "rahmen")
        if b > 1.2: box("Pfosten", (f0 + f1) / 2 - p / 2, (f0 + f1) / 2 + p / 2, z0, z1, *wr, "rahmen")
        if not sichtbar_a: return
        wahl = zr.random()
        if art == "glas" and wahl < FD["rollladen"]:               # Rollladen: grün, halb oder ganz herunter, vor dem Rahmen
            anteil = zr.choice((0.3, 0.42, 0.55, 0.55, 1.0))
            box("Rollladen", f0, f1, z1 - h * anteil, z1 - 0.04, *quer(t0 + 0.06, t0 + 0.09), "rollladen")
        elif art == "glas" and wahl < FD["rollladen"] + FD["gardine"]:   # Gardine: helle Fläche hinter dem Rahmen, unteres Drittel bis zwei Drittel
            anteil = zr.choice((0.45, 0.6, 0.62))
            box("Gardine", f0 + r, f1 - r, z0 + r, z0 + h * anteil, *quer(t0, t0 + 0.02), "gardine")
        elif art == "glas" and achse == "y" and wahl < FD["rollladen"] + FD["gardine"] + FD["offen"]:   # Flügel nach außen geöffnet (Kastenfenster)
            wl = (b / 2 - p / 2 - 0.02) if b > 1.2 else b - 0.04; th = math.radians(zr.uniform(55, 75))
            hx, hy = f1 - 0.02, lage + aussen * (t0 + 0.07)
            cx, cy = hx - math.cos(th) * wl / 2, hy - math.sin(th) * wl / 2
            einordnen(wz.kiste((wl, 0.05, h), (cx, cy, (z0 + z1) / 2), M["rahmen"], "hinten", dreh=(0, 0, th), fase=0.0, name="Fluegel offen"), samm)
            einordnen(wz.kiste((wl - 2 * r, 0.056, h - 2 * r), (cx, cy, (z0 + z1) / 2), M["glas"], "hinten", dreh=(0, 0, th), fase=0.0, name="Fluegel offen Glas"), samm)

    for g in GESCHOSSE:
        # Trakt A: SE-Front mit Eckrisaliten (West alle Geschosse, Ost nur 2. OG) und Mittelrisalit, NW-Front mit Treppenhausrisalit,
        # Stirnwände x 0 und x 61,2. Die Hauptflucht y 0 läuft zwischen den Risaliten; Rücksprünge als Wandstücke y −1 … 0.
        se0, se1 = A["x0"], A["x1"]
        for e in ECKRISALITE:
            if g not in e["geschosse"]: continue
            z0, z1 = GESCHOSSE[g], GESCHOSSE[g] + GESCHOSS
            aussenwand("A", g, "y", -ECK_VOR, e["x0"], e["x1"], +1)
            if e["x0"] > A["x0"]: kiste(f"Eckrisalit {e['name']} Ruecksprung {g}", e["x0"], -ECK_VOR + A["aussen"], e["x0"] + A["aussen"], 0.0, z0, z1, "putz", f"Trakt A {g}")
            if e["x1"] < A["x1"]: kiste(f"Eckrisalit {e['name']} Ruecksprung {g}", e["x1"] - A["aussen"], -ECK_VOR + A["aussen"], e["x1"], 0.0, z0, z1, "putz", f"Trakt A {g}")
            if e["x0"] <= A["x0"]: se0 = e["x1"]; aussenwand("A", g, "x", A["x0"], -ECK_VOR, A["y0"], +1)    # Stirnwand-Stück im Risalit
            if e["x1"] >= A["x1"]: se1 = e["x0"]; aussenwand("A", g, "x", A["x1"], -ECK_VOR, A["y0"], -1)
        aussenwand("A", g, "y", A["y0"], se0, RISALIT_SE[0], +1); aussenwand("A", g, "y", A["y0"], RISALIT_SE[2], se1, +1)
        aussenwand("A", g, "y", RISALIT_SE[1], RISALIT_SE[0], RISALIT_SE[2], +1)
        aussenwand("A", g, "x", RISALIT_SE[0], RISALIT_SE[1], A["y0"], +1); aussenwand("A", g, "x", RISALIT_SE[2], RISALIT_SE[1], A["y0"], -1)
        aussenwand("A", g, "y", A["y1"], A["x0"], RISALIT_NW[0], -1); aussenwand("A", g, "y", A["y1"], RISALIT_NW[2], A["x1"], -1)
        aussenwand("A", g, "y", RISALIT_NW[3], RISALIT_NW[0], RISALIT_NW[2], -1)
        aussenwand("A", g, "x", RISALIT_NW[0], A["y1"], RISALIT_NW[3], +1); aussenwand("A", g, "x", RISALIT_NW[2], A["y1"], RISALIT_NW[3], -1)
        aussenwand("A", g, "x", A["x0"], A["y0"], A["y1"], +1)                                          # Stirnwand West (Hauptteil)
        if g == "2OG": aussenwand("A", g, "x", A["x1"], A["y0"], A["y1"], -1)       # Stirnwand über dem Neubau frei
        else:
            aussenwand("N", g, "y", N["y0"], N["x0"], N["x1"], +1); aussenwand("N", g, "y", N["y1"], N["x0"], N["x1"], -1)
            aussenwand("N", g, "x", N["x1"], N["y0"], N["y1"], -1)
            aussenwand("N", g, "x", N["x0"], N["y0"], A["y0"], +1); aussenwand("N", g, "x", N["x0"], A["y1"], N["y1"], +1)
    # Quergiebel-Wand über dem Risalit (Traufe 12 → Giebelfuß 13,5), Giebeldreieck bis 16,6
    gz0 = DACH["traufe"]; gz1 = gz0 + 1.5
    kiste("Giebelwand", RISALIT_SE[0], RISALIT_SE[1], RISALIT_SE[2], RISALIT_SE[1] + A["aussen"], gz0, gz1, "putz", "Trakt A Dach")
    xm = (RISALIT_SE[0] + RISALIT_SE[2]) / 2; first = gz1 + (RISALIT_SE[2] - RISALIT_SE[0]) / 2 * math.tan(math.radians(DACH["neigung"]))
    y0, y1 = RISALIT_SE[1], RISALIT_SE[1] + A["aussen"]
    netz("Giebeldreieck", [(RISALIT_SE[0], y0, gz1), (RISALIT_SE[2], y0, gz1), (xm, y0, first), (RISALIT_SE[0], y1, gz1), (RISALIT_SE[2], y1, gz1), (xm, y1, first)],
         [(0, 1, 2), (5, 4, 3), (0, 2, 5, 3), (1, 4, 5, 2), (0, 3, 4, 1)], "putz", "Trakt A Dach")
    for s in (RISALIT_SE[0], RISALIT_SE[2] - A["aussen"]):
        kiste("Giebel Seitenwand", s, RISALIT_SE[1], s + A["aussen"], 0.0, gz0, gz1, "putz", "Trakt A Dach")

    # ---------------- Dach Altbau: Walm mit Quergiebel, Treppenhaus-Walm, Kamine ----------------
    u = DACH["ueberstand"]; tan = math.tan(math.radians(DACH["neigung"]))
    hb = (A["y1"] - A["y0"]) / 2                         # halbe Tiefe bis zum First (y 8)
    ze = DACH["traufe"] - u * tan                        # Traufe am Überstand
    zf = DACH["traufe"] + hb * tan                       # First z 16,6
    fx0, fx1 = A["x0"] + hb, A["x1"] - hb                # Walm: First um die halbe Tiefe eingerückt
    netz("Walmdach", [(A["x0"] - u, A["y0"] - u, ze), (A["x1"] + u, A["y0"] - u, ze), (A["x1"] + u, A["y1"] + u, ze), (A["x0"] - u, A["y1"] + u, ze),
                      (fx0, DACH["first_y"], zf), (fx1, DACH["first_y"], zf)],
         [(0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4), (3, 2, 1, 0)], "ziegel", "Trakt A Dach")
    # Eckrisalite: eigener Walm (First längs y, steiler als das Hauptdach), Traufe wie das Hauptdach; läuft hinten bis zum Hauptfirst
    # und taucht dort in die Hauptdachfläche (Blockout, keine Kehle). Sichtbar von (a): vordere Walmfläche und der Rücken über dem Hauptwalm.
    tan_e = math.tan(math.radians(ECK_NEIGUNG))
    for e in ECKRISALITE:
        ex0, ex1, ey0, ey1 = e["x0"] - u, e["x1"] + u, -ECK_VOR - u, DACH["first_y"]
        hw = (ex1 - ex0) / 2; exm = (ex0 + ex1) / 2; zr = ze + hw * tan_e
        netz(f"Walm Eckrisalit {e['name']}", [(ex0, ey0, ze), (ex1, ey0, ze), (ex1, ey1, ze), (ex0, ey1, ze), (exm, ey0 + hw, zr), (exm, ey1 - hw, zr)],
             [(0, 1, 4), (1, 2, 5, 4), (2, 3, 5), (3, 0, 4, 5), (3, 2, 1, 0)], "ziegel", "Trakt A Dach")
    # Quergiebel: Sattel über dem Risalit, First z 16,6 von y −3,6 bis zum Hauptfirst
    hx = (RISALIT_SE[2] - RISALIT_SE[0]) / 2 + u; gy0 = RISALIT_SE[1] - u; gy1 = DACH["first_y"]
    netz("Quergiebel", [(xm - hx, gy0, gz1 - u * tan), (xm + hx, gy0, gz1 - u * tan), (xm, gy0, zf), (xm - hx, gy1, gz1 - u * tan), (xm + hx, gy1, gz1 - u * tan), (xm, gy1, zf)],
         [(0, 2, 5, 3), (2, 1, 4, 5), (3, 5, 4), (1, 0, 3, 4)], "ziegel", "Trakt A Dach")
    # Treppenhausrisalit: kleiner Walm (First längs x) über y 16 … 19
    rx0, rx1, ry0, ry1 = RISALIT_NW[0] - u, RISALIT_NW[2] + u, RISALIT_NW[1], RISALIT_NW[3] + u
    rh = (ry1 - ry0) / 2; rz = ze; rf = rz + rh * tan
    netz("Walm Treppenhaus", [(rx0, ry0, rz), (rx1, ry0, rz), (rx1, ry1, rz), (rx0, ry1, rz), (rx0 + rh, ry0 + rh, rf), (rx1 - rh, ry0 + rh, rf)],
         [(0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4), (3, 2, 1, 0)], "ziegel", "Trakt A Dach")
    for x in DACH["kamine"]:
        kiste(f"Kamin x{x:g}", x - 0.4, DACH["first_y"] - 0.35, x + 0.4, DACH["first_y"] + 0.35, zf - 1.2, zf + 1.0, "putz", "Trakt A Dach")
    for x in DACH["kamine"]:                                       # Kaminköpfe: Steinplatte, etwas breiter als der Schaft
        kiste(f"Kaminkopf x{x:g}", x - 0.52, DACH["first_y"] - 0.47, x + 0.52, DACH["first_y"] + 0.47, zf + 1.0, zf + 1.22, "stein", "Trakt A Dach")

    # ---------------- Fassadendetails Altbau (25.10.2026, Auftrag B): Gesimse, Sparrenköpfe, Rinne, Fallrohre, Gauben, Giebel, Portal ----------------
    def kante_box(name, achse, lage, a0, a1, aussen, z0, z1, vor, m, samm="Trakt A Dach", ab=0.0):
        """Quader entlang einer Fassadenkante, `vor` Meter vor der Wandfläche (ab `ab` dahinter beginnend), an den Enden um `vor` verlängert."""
        w = tuple(sorted((lage + aussen * ab, lage + aussen * vor)))
        if achse == "y": return kiste(name, a0 - vor, w[0], a1 + vor, w[1], z0, z1, m, samm)
        return kiste(name, w[0], a0 - vor, w[1], a1 + vor, z0, z1, m, samm)

    for (achse, lage, a0, a1, aussen) in FASSADENKANTEN:
        for i, ge in enumerate(GESIMSE):
            if i == len(GESIMSE) - 1 and (achse, lage) in TRAUFE_OHNE: continue
            kante_box(f"Gesims {i + 1} {achse}{lage:g}", achse, lage, a0, a1, aussen, ge["z0"], ge["z1"], ge["vor"], "gesims")
        if (achse, lage) in TRAUFE_OHNE: continue
        sp = SPARREN; n_sp = int((a1 - a0) / sp["abstand"]); start = a0 + ((a1 - a0) - (n_sp - 1) * sp["abstand"]) / 2
        for j in range(n_sp):                                      # Sparrenköpfe unter dem Überstand, dunkel, ohne Linie
            a = start + j * sp["abstand"]
            kante_box(f"Sparren {achse}{lage:g} {j}", achse, lage, a - sp["b"] / 2, a + sp["b"] / 2, aussen, ze - sp["h"], ze + 0.02, sp["tiefe"], "sparren", ab=0.05)
    # Dachrinne (Zink, ohne Linie) an den Traufen, die Kamera (a) sieht; Fallrohre an den Fassadenkanten
    for name, (x0, y0, x1, y1) in (("Rinne SE West", (7.8, -u - 0.14, 24.6, -u)), ("Rinne SE Ost", (36.6, -u - 0.14, 61.8, -u)),
                                     ("Rinne Eckrisalit West", (-u, -ECK_VOR - u - 0.14, 7.8, -ECK_VOR - u)),
                                     ("Rinne Giebel West", (24.6 - 0.14, RISALIT_SE[1] - u, 24.6, -u)), ("Rinne Giebel Ost", (36.6, RISALIT_SE[1] - u, 36.6 + 0.14, -u)),
                                     ("Rinne Stirn West", (-u - 0.14, -ECK_VOR - u, -u, A["y1"] + u))):
        kiste(name, x0, y0, x1, y1, ze - 0.16, ze + 0.02, "zink", "Trakt A Dach")
    for i, (achse, lage, stelle) in enumerate(FALLROHRE):
        x, y = (stelle, lage - 0.12) if achse == "y" else (lage - 0.12, stelle)
        einordnen(wz.zylinder(0.07, ze - 0.1 + SOCKEL, (x, y, (ze - 0.1 - SOCKEL) / 2), M["zink"], "hinten", v=8, name=f"Fallrohr {i + 1}"), "Trakt A Dach")
    # Giebelgauben auf der SE-Dachfläche: Körper, Satteldächlein, Fenster mit weißem Rahmen
    ga = GAUBE; gy = ga["y"]; z_dach = lambda y: ze + (y + u) * tan
    for i, gx in enumerate(GAUBEN):
        b2 = ga["b"] / 2; zb0 = z_dach(gy) - 0.7; zb1 = z_dach(gy) + 1.5; yb1 = gy + ga["tiefe"]
        kiste(f"Gaube {i + 1}", gx - b2, gy, gx + b2, yb1, zb0, zb1, "putz", "Trakt A Dach")
        gd = 0.22; top = zb1 + 0.7
        netz(f"Gaube {i + 1} Dach", [(gx - b2 - gd, gy - gd, zb1 - 0.05), (gx + b2 + gd, gy - gd, zb1 - 0.05), (gx + b2 + gd, yb1, zb1 - 0.05), (gx - b2 - gd, yb1, zb1 - 0.05),
                                     (gx, gy - gd, top), (gx, yb1, top)], [(0, 4, 5, 3), (1, 2, 5, 4), (0, 1, 4), (2, 3, 5)], "ziegel", "Trakt A Dach")
        fb, fh = ga["fenster"]; fz0 = z_dach(gy) + 0.15; fz1 = fz0 + fh
        kiste(f"Gaube {i + 1} Fenster", gx - fb / 2, gy - 0.03, gx + fb / 2, gy, fz0, fz1, "glas", "Trakt A Dach")
        for a in (gx - fb / 2, gx + fb / 2 - 0.1): kiste("Rahmen", a, gy - 0.05, a + 0.1, gy - 0.03, fz0, fz1, "rahmen", "Trakt A Dach")
        for zz in (fz0, fz1 - 0.1): kiste("Rahmen", gx - fb / 2, gy - 0.05, gx + fb / 2, gy - 0.03, zz, zz + 0.1, "rahmen", "Trakt A Dach")
        kiste("Pfosten", gx - 0.04, gy - 0.05, gx + 0.04, gy - 0.03, fz0, fz1, "rahmen", "Trakt A Dach")
    # Giebel des Mittelrisalits: senkrechte Holzverschalung in zwei Tönen (ohne Linie), Rundfenster, Giebelbalkon mit Holzbrüstung und Tür
    gdk = GIEBEL_DEKOR; yg = RISALIT_SE[1]; st = gdk["streifen"]; hx_i = (RISALIT_SE[2] - RISALIT_SE[0]) / 2
    xs_ = RISALIT_SE[0] + 0.02; j = 0
    while xs_ + st <= RISALIT_SE[2] - 0.02:
        weit = max(abs(xs_ - xm), abs(xs_ + st - xm)); zt = gz1 + (hx_i - weit) * tan - 0.04
        kiste(f"Giebelholz {j}", xs_, yg - 0.03, xs_ + st, yg, gz1, zt, "holz_gruen" if j % 2 else "rahmen", "Trakt A Dach")
        xs_ += st; j += 1
    rr, rz = gdk["rundfenster"]
    einordnen(wz.zylinder(rr + 0.1, 0.05, (xm, yg - 0.045, rz), M["rahmen"], "hinten", dreh=(math.radians(90), 0, 0), v=20, name="Rundfenster Ring"), "Trakt A Dach")
    einordnen(wz.zylinder(rr, 0.05, (xm, yg - 0.07, rz), M["glas"], "hinten", dreh=(math.radians(90), 0, 0), v=20, name="Rundfenster"), "Trakt A Dach")
    tb, th_ = gdk["tuer"]
    kiste("Giebeltuer", xm - tb / 2, yg - 0.06, xm + tb / 2, yg - 0.03, gz1, gz1 + th_, "glas", "Trakt A Dach")
    for a in (xm - tb / 2, xm + tb / 2 - 0.1): kiste("Rahmen", a, yg - 0.08, a + 0.1, yg - 0.06, gz1, gz1 + th_, "rahmen", "Trakt A Dach")
    kiste("Rahmen", xm - tb / 2, yg - 0.08, xm + tb / 2, yg - 0.06, gz1 + th_ - 0.1, gz1 + th_, "rahmen", "Trakt A Dach")

    def balkon(name, x0, x1, y_wand, tiefe_b, z_boden, h_br, samm, bal=0.2):
        """Balkon vor einer Wand bei y_wand (nach −y): Platte, Eckpfosten mit Kugel, Handlauf (Linie) und dunkle Baluster (ohne Linie)."""
        yv = y_wand - tiefe_b
        kiste(f"{name} Platte", x0, yv, x1, y_wand, z_boden, z_boden + 0.2, "gesims", samm)
        for (px, py) in ((x0 + 0.08, yv + 0.08), (x1 - 0.08, yv + 0.08)):
            kiste(f"{name} Pfosten", px - 0.07, py - 0.07, px + 0.07, py + 0.07, z_boden + 0.2, z_boden + 0.2 + h_br, "holz_dunkel", samm)
            einordnen(wz.kugel(0.13, (px, py, z_boden + 0.2 + h_br + 0.12), M["stein"], "hinten", name=f"{name} Kugel"), samm)
        zh = z_boden + 0.2 + h_br
        kiste(f"{name} Handlauf", x0, yv, x1, yv + 0.1, zh - 0.08, zh, "holz_dunkel", samm)
        for xs in (x0, x1 - 0.1): kiste(f"{name} Handlauf Seite", xs, yv, xs + 0.1, y_wand, zh - 0.08, zh, "holz_dunkel", samm)
        n_b = int((x1 - x0 - 0.4) / bal)
        for i in range(n_b + 1):
            bx = x0 + 0.2 + i * (x1 - x0 - 0.4) / max(n_b, 1)
            kiste(f"{name} Baluster", bx - 0.025, yv + 0.03, bx + 0.025, yv + 0.08, z_boden + 0.2, zh - 0.08, "sparren", samm)
        for xs in (x0 + 0.03, x1 - 0.08):
            for i in range(1, int(tiefe_b / bal)):
                by = yv + i * bal
                kiste(f"{name} Baluster", xs, by - 0.025, xs + 0.05, by + 0.025, z_boden + 0.2, zh - 0.08, "sparren", samm)

    gb0, gb1, gbt = gdk["balkon"]; balkon("Giebelbalkon", gb0, gb1, yg, gbt, gz1, 0.95, "Trakt A Dach")
    # Portal: Pilaster mit Kapitell, Balkon im 1. OG als Vordach (Konsolen), Wandleuchten, Schild, drei Stufen, Pflanzkübel mit Formgehölz
    pd = PORTAL_DEKOR; px0, px1, pt = pd["balkon"]; pw = pd["pilaster"]; um = (PORTAL["x0"] + PORTAL["x1"]) / 2
    for seite in (-1, 1):
        a0 = PORTAL["x0"] - 0.2 - pw if seite < 0 else PORTAL["x1"] + 0.2
        kiste("Pilaster", a0, yg - pd["pilaster_vor"], a0 + pw, yg, -SOCKEL, 3.55, "fasche", "Trakt A EG")
        kiste("Pilaster Kapitell", a0 - 0.08, yg - pd["pilaster_vor"] - 0.06, a0 + pw + 0.08, yg, 3.55, 3.78, "stein", "Trakt A EG")
        kiste("Pilaster Fuss", a0 - 0.06, yg - pd["pilaster_vor"] - 0.04, a0 + pw + 0.06, yg, -SOCKEL, -SOCKEL + 0.4, "stein", "Trakt A EG")
        lx = a0 - 0.5 if seite < 0 else a0 + pw + 0.25
        kiste("Wandleuchte", lx, yg - 0.24, lx + 0.25, yg, 2.3, 2.66, "fenster_warm", "Trakt A EG")
        kiste("Wandleuchte Kappe", lx - 0.03, yg - 0.3, lx + 0.28, yg, 2.66, 2.72, "sparren", "Trakt A EG")
        kiste("Portal Konsole", a0 + 0.1, yg - 1.0, a0 + pw - 0.1, yg, 3.4, 3.95, "stein", "Trakt A 1OG")
    balkon("Portalbalkon", px0, px1, yg, pt, 3.95, pd["bruestung"], "Trakt A 1OG", bal=pd["baluster"])
    # Loggia (25.10.2026, Korrekturrunde): vor dem Balkon eine Arkade mit drei Rundbögen auf vier Pfeilern, darüber eine Platte
    # (= Austritt des 2. OG mit Brüstung). Bogenfeld als ein Prisma mit drei Ausschnitten; die 1.-OG-Fenster des Risalits bleiben dahinter sichtbar.
    lg = LOGGIA; yv = yg - pt; pfeiler = lg["pfeiler"]; n_b = 3; lichte = ((px1 - px0) - (n_b + 1) * pfeiler) / n_b; R = lichte / 2
    zs_ = lg["z_kaempfer"]; zo = zs_ + R + lg["ueber_bogen"]
    for i in range(n_b + 1):
        xp = px0 + i * (lichte + pfeiler)
        kiste(f"Loggia Pfeiler {i + 1}", xp, yv - 0.05, xp + pfeiler, yv + lg["tiefe"], 4.15, zs_, "gesims", "Trakt A 1OG")
    pts = [(px0, zs_)]
    for i in range(n_b):
        xl = px0 + pfeiler + i * (lichte + pfeiler); cx_ = xl + R
        pts.append((xl, zs_)); pts += [(cx_ + R * math.cos(math.radians(a)), zs_ + R * math.sin(math.radians(a))) for a in range(170, 0, -10)]
        pts.append((xl + lichte, zs_))
    pts += [(px1, zs_), (px1, zo), (px0, zo)]
    prisma("Loggia Bogenfeld", pts, "y", yv - 0.05, yv + lg["tiefe"], "gesims", "Trakt A 1OG")
    balkon("Loggia Austritt 2OG", px0, px1, yg, pt + 0.05, zo, pd["bruestung"], "Trakt A 2OG", bal=pd["baluster"])
    sx0 = PORTAL["x1"] + 0.2 + pw + 0.7                            # Schild „Haus Föhrenhang": weiße Tafel, drei Textbalken (Schrift bei 17 px/m unlesbar)
    kiste("Schild Haus", sx0, yg - 0.04, sx0 + 0.95, yg, 1.5, 2.25, "rtw", "Trakt A EG")
    for i, (zs, lb_) in enumerate(((2.08, 0.55), (1.92, 0.75), (1.68, 0.4))):
        kiste(f"Schild Text {i + 1}", sx0 + 0.1, yg - 0.05, sx0 + 0.1 + lb_, yg - 0.04, zs, zs + 0.05, "schrift", "Trakt A EG")
    sb_ = pd["stufen_b"]; st_ = pd["stufe"]; sh = SOCKEL / pd["stufen"]
    for i in range(pd["stufen"]):                                  # Stufen: oberste schmal, unterste weit, ganze Portalbreite
        kiste(f"Stufe {i + 1}", um - sb_ / 2, yg - st_ * (i + 1), um + sb_ / 2, yg, -sh * (i + 1), -sh * i, "stein", "Trakt A EG")
    for seite in (-1, 1):                                          # Pflanzkübel mit Formgehölz (Kugel)
        kx = um + seite * (sb_ / 2 + 0.75)
        kiste("Kuebel Portal", kx - 0.36, yg - 1.5, kx + 0.36, yg - 0.78, -SOCKEL, -SOCKEL + 0.72, "stein", "Trakt A EG")
        einordnen(wz.kugel(0.45, (kx, yg - 1.14, -SOCKEL + 0.72 + 0.4), M["hecke"], "hinten", name="Formgehoelz"), "Buesche")

    # Trakt N: Flachdach, Attika, Dachgarten, Holzlamellen, Vordach
    zn = N["geschosse"] * GESCHOSS
    kiste("Dach N", N["x0"], N["y0"], N["x1"], N["y1"], zn - 0.4, zn, "beton", "Trakt N Dach")
    for (x0, y0, x1, y1) in ((N["x0"], N["y0"], N["x1"], N["y0"] + 0.3), (N["x0"], N["y1"] - 0.3, N["x1"], N["y1"]), (N["x1"] - 0.3, N["y0"], N["x1"], N["y1"])):
        kiste("Attika", x0, y0, x1, y1, zn, zn + ATTIKA_N, "attika", "Trakt N Dach")
    for i, (x0, y0) in enumerate(((64, -3), (64, 6), (76, -3), (76, 6))):
        kiste(f"Hochbeet {i + 1}", x0, y0, x0 + 6, y0 + 1.5, zn, zn + 0.7, "beet", "Trakt N Dach")
    for i, (x, y) in enumerate(((70, 14), (80, 14))):
        kiste(f"Bank Dachgarten {i + 1}", x - 0.9, y - 0.25, x + 0.9, y + 0.25, zn, zn + 0.45, "holz", "Trakt N Dach")
    for i, (x, y) in enumerate(((68, 2), (82, 10))):
        kiste(f"Kuebel {i + 1}", x - 0.5, y - 0.5, x + 0.5, y + 0.5, zn, zn + 0.6, "beton", "Trakt N Dach")
        baum(f"Felsenbirne {i + 1}", x, y, 1.3, "laub", "laub", "Trakt N Dach", hoehe=3.8, z=zn + 0.6)
    for i, x in enumerate([N["x0"] + 0.4 + 0.6 * j for j in range(int((N["x1"] - N["x0"] - 0.8) / 0.6) + 1)]):   # Lamellen SE, 1. OG: flache Holzstreifen
        kiste(f"Lamelle SE {i + 1}", x, N["y0"] - 0.32, x + 0.14, N["y0"] - 0.2, GESCHOSS + 0.42, zn - 0.42, "lamelle", "Trakt N 1OG")   # ohne eigene Linie (25.10.)
    for name, z0 in (("Lamellenschiene SE unten", GESCHOSS + 0.28), ("Lamellenschiene SE oben", zn - 0.42)):   # Schienen mit Linie: das Raster liest als Schirm
        kiste(name, N["x0"] + 0.3, N["y0"] - 0.34, N["x1"] - 0.3, N["y0"] - 0.18, z0, z0 + 0.14, "holz_dunkel", "Trakt N 1OG")
    for i, y in enumerate([AUFNAHME_GLAS["y0"] + 0.3 + 0.6 * j for j in range(16)]):                          # Lamellen NE vor der Glasfront
        kiste(f"Lamelle NE {i + 1}", N["x1"] + 0.2, y, N["x1"] + 0.32, y + 0.1, 0.3, zn - 0.3, "lamelle", "Trakt N EG")
    V = VORDACH
    kiste("Vordach", V["x0"], V["y0"], V["x1"], V["y1"], V["unterkante"], V["unterkante"] + V["dicke"], "beton", "Trakt N EG")
    for i, y in enumerate((V["y0"] + 1.0, V["y1"] - 1.0)):
        kiste(f"Vordach Stuetze {i + 1}", V["x1"] - 0.8, y - 0.15, V["x1"] - 0.5, y + 0.15, -SOCKEL, V["unterkante"], "stuetze", "Trakt N EG")

    # ---------------- Räume: Bodenplatte mit Namen, Innenwände mit Türen ----------------
    # Außenwand-Intervalle (Achse, Lage, a0, a1): hier entstehen keine Innenwände
    AUSSEN = [("y", A["y0"], A["x0"], RISALIT_SE[0]), ("y", A["y0"], RISALIT_SE[2], A["x1"]), ("y", RISALIT_SE[1], RISALIT_SE[0], RISALIT_SE[2]),
              ("y", A["y1"], A["x0"], RISALIT_NW[0]), ("y", A["y1"], RISALIT_NW[2], A["x1"]), ("y", RISALIT_NW[3], RISALIT_NW[0], RISALIT_NW[2]),
              ("x", A["x0"], A["y0"], A["y1"]), ("x", RISALIT_SE[0], RISALIT_SE[1], A["y0"]), ("x", RISALIT_SE[2], RISALIT_SE[1], A["y0"]),
              ("x", RISALIT_NW[0], A["y1"], RISALIT_NW[3]), ("x", RISALIT_NW[2], A["y1"], RISALIT_NW[3]),
              ("y", N["y0"], N["x0"], N["x1"]), ("y", N["y1"], N["x0"], N["x1"]), ("x", N["x1"], N["y0"], N["y1"]),
              ("x", N["x0"], N["y0"], A["y0"]), ("x", N["x0"], A["y1"], N["y1"])]

    def abziehen(zus, o0, o1):
        neu = []
        for a0, a1 in zus:
            if o1 <= a0 + 1e-6 or o0 >= a1 - 1e-6: neu.append((a0, a1)); continue
            if o0 > a0 + 1e-6: neu.append((a0, o0))
            if o1 < a1 - 1e-6: neu.append((o1, a1))
        return neu

    def innenwaende(g):
        z = GESCHOSSE[g]; raeume = RAEUME[g]
        aussen = AUSSEN + ([("x", A["x1"], A["y0"], A["y1"])] if g == "2OG" else [])
        segmente = {}           # (Achse, Lage) -> [(a0, a1)]
        for (name, x0, y0, x1, y1, boden, tueren) in raeume:
            trakt = "N" if x0 >= N["x0"] else "A"
            p = netz(f"{g} {name}", [(x0, y0, z + 0.01), (x1, y0, z + 0.01), (x1, y1, z + 0.01), (x0, y1, z + 0.01)], [(0, 1, 2, 3)], boden, f"Trakt {trakt} {g}")
            p["raum"] = name; p["geschoss"] = g
            for (achse, lage, a0, a1) in (("y", y0, x0, x1), ("y", y1, x0, x1), ("x", x0, y0, y1), ("x", x1, y0, y1)):
                segmente.setdefault((achse, round(lage, 3)), []).append((min(a0, a1), max(a0, a1)))
        tueren = {}
        for (name, x0, y0, x1, y1, boden, tl) in raeume:
            for (achse, lage, mitte, breite, art) in tl:
                tueren.setdefault((achse, round(lage, 3)), []).append((mitte, breite, art, name))
        for (achse, lage), iv in segmente.items():
            iv.sort(); zus = []
            for a0, a1 in iv:
                if zus and a0 <= zus[-1][1] + 1e-6: zus[-1] = (zus[-1][0], max(zus[-1][1], a1))
                else: zus.append((a0, a1))
            for (ac, la, o0, o1) in aussen:
                if ac == achse and abs(la - lage) < 1e-6: zus = abziehen(zus, o0, o1)
            for (mitte, breite, art, name) in tueren.get((achse, lage), []):
                if art == "offen": zus = abziehen(zus, mitte - breite / 2, mitte + breite / 2)
            d = A["innen"]
            for (a0, a1) in zus:
                if a1 - a0 < 0.2: continue
                im_n = (achse == "y" and a0 >= N["x0"] - 1e-6) or (achse == "x" and lage > N["x0"] + 1e-6)
                hoch = RAUMHOEHE["N" if im_n else "A"]; samm = f"Trakt {'N' if im_n else 'A'} {g}"
                name = f"Wand {g} {achse}{lage:g} {a0:g}-{a1:g}"
                oeffnungen = []
                for (mitte, breite, art, raum) in tueren.get((achse, lage), []):
                    if art == "offen" or mitte - breite / 2 < a0 - 1e-6 or mitte + breite / 2 > a1 + 1e-6: continue
                    th = TUER["h"] if breite < 2.5 else PORTAL["h"]
                    oeffnungen.append((mitte - breite / 2, mitte + breite / 2, z - 0.02, z + th))
                    tuerblatt(g, achse, lage, mitte, breite, art, raum, samm, z, th)
                wandnetz(name, achse, lage - d / 2, lage + d / 2, a0, a1, z, z + hoch, oeffnungen, "wand", samm)

    def tuerblatt(g, achse, lage, mitte, breite, art, raum, samm, z, th):
        m = "glas" if art == "glas" else "tuer"
        name = f"Tuer {g} {raum} {achse}{lage:g}"
        d = 0.05
        if art == "auf":           # Blatt um 90° in den Raum geschwenkt (Raum liegt auf der Seite weg vom Flur)
            seite = -1 if (achse == "y" and lage <= FLUR[0] + 1e-6) else 1
            if achse == "y": kiste(name, mitte - breite / 2, lage + seite * d, mitte - breite / 2 + d, lage + seite * (d + breite), z, z + th, m, samm)
            else: kiste(name, lage + seite * d, mitte - breite / 2, lage + seite * (d + breite), mitte - breite / 2 + d, z, z + th, m, samm)
        elif achse == "y": kiste(name, mitte - breite / 2, lage - d / 2, mitte + breite / 2, lage + d / 2, z, z + th, m, samm)
        else: kiste(name, lage - d / 2, mitte - breite / 2, lage + d / 2, mitte + breite / 2, z, z + th, m, samm)

    for g in GESCHOSSE: innenwaende(g)

    # Treppenhäuser und Lifte als Schächte (durchgehende Kerne, Treppen als Blöcke mit Läufen angedeutet)
    for (name, x0, y0, x1, y1, art) in (("S1", 25.2, 10, 30.6, 19, "treppe"), ("S2", 54, 10, 57.6, 16, "treppe"), ("S3", 61.2, 14, 66, 18, "treppe"),
                                         ("L1 Betten", 30.6, 10, 33.4, 12.5, "lift"), ("L1 Personen", 33.6, 10, 35.2, 12.0, "lift"), ("L2 Betten", 57.6, 10, 60.4, 12.5, "lift")):
        zmax = 3 * GESCHOSS if name != "S3" else 2 * GESCHOSS
        if art == "lift":
            kiste(f"Schacht {name}", x0, y0, x1, y1, -SOCKEL, zmax + RAUMHOEHE["A"], "lift", "Kerne")
        else:
            for g, z in GESCHOSSE.items():
                if z >= zmax: break
                lauf = (y1 - y0 - 0.4) / 2
                kiste(f"Treppe {name} {g} Lauf 1", x0 + 0.2, y0 + 0.2, (x0 + x1) / 2 - 0.05, y0 + 0.2 + lauf, z, z + 1.0, "sockel", "Kerne")
                kiste(f"Treppe {name} {g} Podest", x0 + 0.2, y1 - 0.2 - lauf, x1 - 0.2, y1 - 0.2, z + 1.9, z + 2.1, "sockel", "Kerne")
                kiste(f"Treppe {name} {g} Lauf 2", (x0 + x1) / 2 + 0.05, y0 + 0.2, x1 - 0.2, y0 + 0.2 + lauf, z + 2.1, z + 3.1, "sockel", "Kerne")

    # ---------------- Grobe Klötze im Probe-Flur (1. OG) und Sockelband ----------------
    z1 = GESCHOSSE["1OG"]
    kiste("Tresen Stuetzpunkt 1OG", 28.3, 6.3, 30.3, 6.95, z1, z1 + 1.05, "holz", "Moebel Flur 1OG")   # 3,1 m hinter der Öffnungskante, 5 m vor Kamera (b): bei 70–80 % der Bildbreite, nicht angeschnitten
    kiste("Pflegewagen 1OG", 44.0, 9.2, 44.7, 9.8, z1, z1 + 0.95, "petrol", "Moebel Flur 1OG")
    kiste("Sitzbank Flur 1OG", 48.0, 9.5, 50.0, 9.95, z1 + 0.42, z1 + 0.47, "holz", "Moebel Flur 1OG")
    kiste("Sitzbank Flur 1OG Fuss", 48.1, 9.6, 49.9, 9.9, z1, z1 + 0.42, "petrol", "Moebel Flur 1OG")
    for i, (x, y) in enumerate(((33.0, 8.2), (52.0, 9.0))):          # Silhouetten: Figur als Kapsel 1,7 m
        einordnen(wz.zylinder(0.22, 1.45, (x, y, z1 + 0.725), M["figur"], "hinten", v=12, name=f"Silhouette {i + 1}"), "Moebel Flur 1OG")
        einordnen(wz.kugel(0.12, (x, y, z1 + 1.58), M["figur"], "hinten", name=f"Silhouette {i + 1} Kopf"), "Moebel Flur 1OG")
    for (y, s) in ((FLUR[0], +1), (FLUR[1], -1)):                     # Sockel Mint 1,1 m an den Flurwänden, an den Türen unterbrochen
        oeffnungen = [(mitte - breite / 2 - 0.1, mitte + breite / 2 + 0.1, z1 - 0.1, z1 + 1.2)
                      for (name, x0, y0, x1, y1, boden, tl) in RAEUME["1OG"] for (achse, lage, mitte, breite, art) in tl
                      if achse == "y" and abs(lage - y) < 1e-6]
        w = sorted((y + s * (A["innen"] / 2 + 0.004), y + s * (A["innen"] / 2 + 0.012)))
        wandnetz(f"Sockel Flur 1OG y{y:g}", "y", w[0], w[1], A["x0"] + 0.5, A["x1"] - 0.5, z1, z1 + 1.1, oeffnungen, "paneel", "Moebel Flur 1OG")

    # ---------------- Himmel (Bänder, werden je Kamera ausgerichtet) und Sonne ----------------
    bpy.ops.object.light_add(type='SUN'); sonne = bpy.context.object; sonne.name = "Sonne"
    sonne.data.energy = 12.0; sonne.data.angle = math.radians(1.0)
    sc.world = bpy.data.worlds.new("Welt"); sc.world.use_nodes = True
    bpy.ops.object.camera_add(location=(0, -50, 10)); kam = bpy.context.object; kam.name = "Kamera"; sc.camera = kam
    kam.data.sensor_width = 36; kam.data.sensor_fit = 'HORIZONTAL'

    os.makedirs(BAU, exist_ok=True)
    for m in M.values(): m.use_fake_user = True
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    import logging; logging.disable(logging.INFO)          # der glTF-Export meldet sonst jedes Objekt
    bpy.ops.export_scene.gltf(filepath=BAU + "haus_blockout.glb", export_format='GLB', export_apply=True, export_lights=False, export_cameras=False)
    print("GEBAUT", BLEND, "Objekte:", len(bpy.data.objects), flush=True)


# ======================================================================================================
# Rendern: Durchgänge wie ebenen.py (Fläche, Linie, Sonne), je Durchgang die .blend neu geladen
# ======================================================================================================
def sonnenrichtung(azimut, hoehe):
    """Lichtrichtung in lokalen Koordinaten: Nord = (0,71 / 0,71), Azimut im Uhrzeigersinn ab Nord."""
    n = (0.7071, 0.7071); e = (0.7071, -0.7071)
    a, h = math.radians(azimut), math.radians(hoehe)
    von = (math.sin(a) * e[0] + math.cos(a) * n[0], math.sin(a) * e[1] + math.cos(a) * n[1])
    return (-von[0] * math.cos(h), -von[1] * math.cos(h), -math.sin(h))


def kamera_stellen(sc, k, aufloesung=(B, H)):
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    kam = bpy.data.objects["Kamera"]; sc.camera = kam
    ox, oy, oz = k["ort"]; zx, zy, zz = k["ziel"]
    gier = math.atan2(zy - oy, zx - ox)
    kam.location = k["ort"]; kam.rotation_euler = (math.radians(90), 0, gier - math.radians(90))
    kam.data.type = 'PERSP'; kam.data.lens = k["brennweite"]; kam.data.shift_x = 0; kam.data.shift_y = 0
    kam.data.clip_start = 0.3; kam.data.clip_end = 2000
    sc.render.resolution_x, sc.render.resolution_y = aufloesung
    bpy.context.view_layer.update()
    p = world_to_camera_view(sc, kam, Vector(k["ziel"]))          # Ziel in die Bildmitte: Verschiebung statt Neigung
    kam.data.shift_y = (p.y - 0.5) * aufloesung[1] / aufloesung[0]
    bpy.context.view_layer.update()
    return gier


def himmel_setzen(sc, k, gier, M):
    """Himmelsbänder als große Fläche quer zur Blickrichtung, 900 m entfernt (nur für diesen Render)."""
    import bpy
    sys.path.insert(0, HIER); import werkzeug as wz
    farben = k["himmel"]; abstand = 900.0; hoehe = 700.0
    ox, oy, _ = k["ort"]
    cx, cy = ox + math.cos(gier) * abstand, oy + math.sin(gier) * abstand
    n = len(farben)
    for i, f in enumerate(farben):
        m = bpy.data.materials.get(f"himmel_{i}") or wz.material(f"himmel_{i}", (0.9, 0.9, 0.9), 0.9)   # unbenutzte Materialien überleben das Speichern nicht
        z0 = -100 + (n - 1 - i) * hoehe / n; z1 = z0 + hoehe / n
        o = wz.platte(3000.0, z1 - z0, (cx, cy, (z0 + z1) / 2), m, "hinten", dreh=(math.radians(90), 0, gier + math.radians(90)), name=f"Himmel {i}")
        o.data.materials[0] = m
    # Wolken: flache Linsen (oben rund, unten flach) 10 m vor der Himmelsebene, Farben Morgenlicht-Abwandlungen, ohne Linie
    rx, ry = math.sin(gier), -math.cos(gier)                       # „rechts" quer zur Blickrichtung
    def kumulus(laenge, hoehe, zr):
        """Comic-Wolke als Umriss (a seitlich, b Höhe über der Unterkante): eine Kette überlappender Kreise, zur Mitte hin größer,
        unten an der Grundlinie abgeschnitten (flache Unterkante, runde Enden). Wo zwei Kreise sich schneiden, entsteht die Kerbe.
        Ein Vieleck; Freestyle zeichnet den Umriss."""
        re = hoehe * 0.3; kreise = [(-laenge / 2 + re, re, re)]      # Endkreise sitzen auf der Grundlinie: runde Enden statt senkrechter Schnitte
        a = -laenge / 2 + hoehe * 0.75
        while a < laenge / 2 - hoehe * 0.75:
            lage_ = min(1.0, abs(a) / (laenge / 2)); r = hoehe * (0.34 + 0.32 * (1 - lage_ ** 2)) * zr.uniform(0.85, 1.15)
            r = min(r, 0.66 * hoehe); kreise.append((a, r * zr.uniform(0.45, 0.6), r)); a += r * zr.uniform(0.9, 1.25)
        mitte_ = (kreise[-1][0] + laenge / 2 - re) / 2                   # Lückenfüller vor dem rechten Endkreis (sonst hing er als Blase daneben)
        kreise.append((mitte_, 0.22 * hoehe, 0.45 * hoehe)); kreise.append((laenge / 2 - re, re, re))
        oben, unten = [], []; n = 180; u0, u1 = kreise[0][0] - kreise[0][2], kreise[-1][0] + kreise[-1][2]
        for j in range(n + 1):
            u = u0 + (u1 - u0) * j / n; top = None; bot = None
            for (cu, cv, r) in kreise:
                if abs(u - cu) < r:
                    w = math.sqrt(r * r - (u - cu) ** 2)
                    top = cv + w if top is None else max(top, cv + w); bot = cv - w if bot is None else min(bot, cv - w)
            if top is None: continue
            oben.append((u, top)); unten.append((u, max(0.0, bot)))
        return oben + unten[::-1]

    for i, (seit, z, laenge, dicke, mat) in enumerate(k.get("wolken", ())):
        m = bpy.data.materials.get(mat) or wz.material(mat, (0.95, 0.95, 0.95), 0.9)
        wx, wy = ox + math.cos(gier) * (abstand - 10) + rx * seit, oy + math.sin(gier) * (abstand - 10) + ry * seit
        if stil():                                                 # Stile tag/blau: Kumulus mit Umriss
            form = kumulus(laenge, dicke, random.Random(i + 3))
        else:                                                      # alte Probe: flache Linse (oben rund, unten flach)
            form = []
            for j in range(24):
                t = 2 * math.pi * j / 24; form.append((laenge / 2 * math.cos(t), dicke * (math.sin(t) if math.sin(t) > 0 else 0.35 * math.sin(t))))
        v = [(wx + rx * a, wy + ry * a, z + b) for (a, b) in form]
        me = bpy.data.meshes.new(f"Wolke {i}"); me.from_pydata(v, [], [tuple(range(len(v)))]); me.update()
        o = bpy.data.objects.new(f"Wolke {i}", me); o.data.materials.append(m); sc.collection.objects.link(o)


def durchgang(kamera_name, art, ortho=None):
    """Ein Render-Durchgang in einem frischen Prozess: lädt die .blend, stellt Kamera und Licht, rendert nach BAU."""
    sys.path.insert(0, HIER)
    import bpy
    import werkzeug as wz
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.context.scene
    wz.cycles_geraet(sc)
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    sc.render.dither_intensity = 0.0; sc.render.resolution_percentage = 100
    M = {m.name: m for m in bpy.data.materials}
    if ortho:
        k = dict(KAMERAS["aussen"]); k.update(ortho); aufl = ortho["aufloesung"]
        kam = bpy.data.objects["Kamera"]; sc.camera = kam
        kam.data.type = 'ORTHO'; kam.data.ortho_scale = ortho["breite"]; kam.data.shift_x = kam.data.shift_y = 0
        kam.location = (ortho["mitte"][0], ortho["mitte"][1], 200.0); kam.rotation_euler = (0, 0, 0)
        kam.data.clip_start = 200.0 - ortho["schnitt"]; kam.data.clip_end = 400.0
        sc.render.resolution_x, sc.render.resolution_y = aufl
        for name in ortho["verstecken"]:
            c = bpy.data.collections.get(name)
            if c: c.hide_render = True
        gier = math.radians(90)
    else:
        k = dict(KAMERAS[kamera_name]); aufl = (B, H)
        if stil(): k.update(stil()["kamera"])
        gier = kamera_stellen(sc, k, aufl)
    pal = dict(PALETTE)
    if stil(): pal.update(stil()["palette"]); pal.update({f"himmel_{i}": f for i, f in enumerate(k["himmel"])})
    himmel_setzen(sc, k, gier, M)
    sonne = bpy.data.objects["Sonne"]
    from mathutils import Vector
    sonne.rotation_euler = Vector(sonnenrichtung(*k["sonne"])).to_track_quat('-Z', 'Y').to_euler()

    def emission_ueberall(farbe_von):
        for m in bpy.data.materials:
            if not m.node_tree: continue
            nt = m.node_tree; aus = nt.nodes.get("Material Output")
            if aus is None: continue
            em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.0
            em.inputs["Color"].default_value = (*farbe_von(m.name), 1)
            for l in list(aus.inputs["Surface"].links): nt.links.remove(l)
            nt.links.new(em.outputs["Emission"], aus.inputs["Surface"])

    def stufen_nach_richtung(m):
        """Wie ebenen.py: Lokalfarbe × Faktor aus der Flächennormalen (oben heller, ±x dunkler), auf 0,04 gerundet."""
        nt = m.node_tree; em = [n for n in nt.nodes if n.type == 'EMISSION'][-1]
        basis = tuple(em.inputs["Color"].default_value)
        geo = nt.nodes.new("ShaderNodeNewGeometry"); xyz = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], xyz.inputs["Vector"])

        def rechne(op, a, b=None, wert=None):
            n = nt.nodes.new("ShaderNodeMath"); n.operation = op; nt.links.new(a, n.inputs[0])
            if b is not None: nt.links.new(b, n.inputs[1])
            if wert is not None: n.inputs[1].default_value = wert
            return n.outputs[0]
        fx = rechne('MULTIPLY', rechne('ABSOLUTE', xyz.outputs["X"]), wert=-0.14)
        fz = rechne('MULTIPLY', xyz.outputs["Z"], wert=0.10)
        faktor = rechne('SNAP', rechne('ADD', rechne('ADD', fz, fx), wert=1.0), wert=0.04)
        mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
        mix.inputs["Factor"].default_value = 1.0; mix.inputs[6].default_value = basis
        grau = nt.nodes.new("ShaderNodeCombineColor")
        for i in range(3): nt.links.new(faktor, grau.inputs[i])
        nt.links.new(grau.outputs["Color"], mix.inputs[7]); nt.links.new(mix.outputs[2], em.inputs["Color"])

    def welt(farbe, staerke=1.0):
        bg = sc.world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (*farbe, 1); bg.inputs[1].default_value = staerke

    def sichtbar(ohne_material=()):
        for o in bpy.data.objects:
            if o.type == 'MESH':
                o.hide_render = bool({m.name for m in o.data.materials if m} & set(ohne_material))

    sonne.hide_render = art != "sun"
    if art == "flat":
        emission_ueberall(lambda n: hex_lin(pal[n]) if n in pal else (0.5, 0.5, 0.5))
        for m in bpy.data.materials:
            if m.node_tree and m.name not in OHNE_SCHATTIERUNG and m.node_tree.nodes.get("Material Output"): stufen_nach_richtung(m)
        welt(hex_lin(k["himmel"][0])); sichtbar(); proben = PROBEN["flat"]
    elif art == "lines":
        emission_ueberall(lambda n: (1, 1, 1)); welt((1, 1, 1))
        sichtbar(OHNE_LINIE | (set() if stil() else {"wolke_hell", "wolke_warm"}))   # Linsenwolken der alten Probe bleiben ohne Umriss
        if not ortho and k.get("linien_nur"):           # Innenkameras: alles außerhalb der genannten Sammlungen aus dem Linien-Durchgang nehmen
            for c in bpy.data.collections:
                if c.name not in k["linien_nur"]: c.hide_render = True
        if not ortho:                                   # hinter der Kamera: Freestyle zeichnet sonst lose Striche (README)
            import bmesh
            kam = sc.camera; blick = kam.matrix_world.to_quaternion() @ Vector((0, 0, -1)); ko = kam.matrix_world.translation
            ebene = ko + blick * 0.45                   # Schnittebene knapp vor der Kamera (clip_start 0,3); Schnittkanten liegen außerhalb des Bildes
            for o in bpy.data.objects:
                if o.type != 'MESH' or o.hide_render: continue
                tiefen = [(o.matrix_world @ Vector(v) - ebene).dot(blick) for v in o.bound_box]
                if max(tiefen) < 0: o.hide_render = True                       # ganz hinter der Kamera: weg
                elif min(tiefen) < 0:                                          # reicht hinter die Kamera (Flurwände, Decke, Sockelband): kappen
                    bm = bmesh.new(); bm.from_mesh(o.data)
                    inv = o.matrix_world.inverted()
                    co_l = inv @ ebene; no_l = (inv.to_3x3() @ blick).normalized()
                    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-4, plane_co=co_l, plane_no=no_l, clear_inner=True)
                    bm.to_mesh(o.data); bm.free(); o.data.update()
        sc.render.resolution_x, sc.render.resolution_y = aufl[0] * UEBER, aufl[1] * UEBER
        sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'
        vl = sc.view_layers[0]; vl.use_freestyle = True
        fs = vl.freestyle_settings; fs.crease_angle = math.radians(120); fs.use_culling = True
        ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("linie")
        ls.select_silhouette = True; ls.select_crease = True; ls.select_border = True; ls.select_contour = True
        boden = bpy.data.collections.get("Boden")       # Gelände verdeckt, liefert aber keine Linien (siehe bauen)
        if boden: ls.select_by_collection = True; ls.collection = boden; ls.collection_negation = 'EXCLUSIVE'
        if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new("claire")
        ls.linestyle.color = (0, 0, 0); ls.linestyle.alpha = 1.0; ls.linestyle.thickness = 1.5 * UEBER; ls.linestyle.caps = "ROUND"
        if stil():                                      # Stilprobe: Umriss dick (Silhouette, Kontur, Rand), Binnenlinie (Knick) dünn
            ls.select_crease = False; ls.linestyle.thickness = stil()["kontur"] * UEBER
            li = fs.linesets.new("innen"); li.select_by_visibility = True
            li.select_silhouette = li.select_border = li.select_contour = False; li.select_crease = True
            if boden: li.select_by_collection = True; li.collection = boden; li.collection_negation = 'EXCLUSIVE'
            li.linestyle = bpy.data.linestyles.new("innen"); li.linestyle.color = (0, 0, 0); li.linestyle.caps = "ROUND"
            li.linestyle.thickness = stil()["innen"] * UEBER
        proben = PROBEN["lines"]
    elif art == "sun":
        for m in bpy.data.materials:
            if not m.node_tree: continue
            b = m.node_tree.nodes.get("Principled BSDF")
            if b is None: continue
            b.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1); b.inputs["Roughness"].default_value = 0.7
            if m.name in IMMER_SCHATTEN: b.inputs["Base Color"].default_value = (0, 0, 0, 1)   # Fußschatten: immer Schattenstufe
            if m.name in OHNE_SCHATTIERUNG and m.name not in IMMER_SCHATTEN:   # Himmel, Fernes, warme Fenster gelten als beleuchtet
                b.inputs["Emission Color"].default_value = (1, 1, 1, 1); b.inputs["Emission Strength"].default_value = 1.0
        welt((0, 0, 0), 0.0); sc.cycles.max_bounces = 0; sichtbar(SONNE_AUS_MATERIAL); proben = PROBEN["sun"]
        for o in bpy.data.objects:                 # Bäume werfen keinen Schatten (OHNE_SCHATTEN), bleiben aber selbst besonnt
            if o.type == 'MESH' and any(c.name in OHNE_SCHATTEN for c in o.users_collection) and not (stil() or {}).get("baumschatten"):
                o.visible_shadow = False
    else:
        raise SystemExit("unbekannter Durchgang " + art)
    sc.cycles.samples = proben; sc.cycles.use_denoising = art == "sun"
    sc.render.filepath = BAU + f"{kamera_name}{stil_endung()}_{art}.png"
    t = time.time(); bpy.ops.render.render(write_still=True)
    if art == "lines":
        from PIL import Image
        Image.open(sc.render.filepath).convert("RGB").reduce(UEBER).save(sc.render.filepath)
    print(f"RENDER {kamera_name} {art} {time.time() - t:.1f}s", flush=True)


def komposit(kamera_name, ziel, k, mit_sonne=True, max_kb=300):
    """Lokalfarbe, Schattenseite eine Stufe dunkler (Richtung Petrol), Sonnenfleck getönt, darüber die Tusche."""
    import numpy as np
    from PIL import Image, ImageFilter
    sys.path.insert(0, HIER); import komposit as ko
    lade = lambda n: np.asarray(Image.open(BAU + f"{kamera_name}{stil_endung()}_{n}.png").convert("RGB")).astype(np.float32) / 255
    flach = lade("flat"); t = ko.tinte(lade("lines"))[..., None]
    s = stil() or {}
    schattenfarbe = ko.hexc(s.get("schatten", "#2C5560")); tinte = ko.hexc(s.get("tinte", "#1E2A30"))
    mit_sonne = mit_sonne and s.get("mit_sonne", True)
    if "duoton" in s:                                  # Blaue Stunde: Helligkeit der Lokalfarbe auf eine Blau-Skala, ein Rest Eigenfarbe;
        pal = dict(s["palette"], **{f"himmel_{i}": f for i, f in enumerate(k["himmel"])})   # leuchtende Flächen behalten ihre Farbe
        leuchtet = np.zeros(flach.shape[:2], bool)
        for n in s["leuchten"]: leuchtet |= np.abs(flach - ko.hexc(pal[n])).max(axis=2) < 0.04
        dunkel, hell = ko.hexc(s["duoton"][0]), ko.hexc(s["duoton"][1])
        l = ko.luma(flach)[..., None] ** 1.15
        blau = dunkel * (1 - l) + hell * l
        blau = blau * (1 - s["eigen"]) + flach * s["eigen"]
        flach = np.where(leuchtet[..., None], flach, blau)
    if mit_sonne:
        ls = ko.luma(lade("sun"))
        licht = np.clip((ls - 0.35) / 0.08 + 0.5, 0, 1)
        licht = np.asarray(Image.fromarray((licht * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))).astype(np.float32) / 255
        licht = ko.weich(licht, 0.7)[..., None]
        schatten = (1 - licht) * k["schatten"]
        flach = flach * (1 - schatten) + schattenfarbe * schatten        # Schattenseite: flache Stufe
        flach = flach * (1 - licht * k["anteil"]) + ko.hexc(k["licht"]) * licht * k["anteil"]
    bild = flach * (1 - t) + tinte * t
    im = Image.fromarray((np.clip(bild, 0, 1) * 255 + 0.5).astype(np.uint8))
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    if ziel.endswith(".jpg"):
        for q in (88, 82, 76, 70, 62, 55):
            im.save(ziel, quality=q, optimize=True, subsampling=1)
            if os.path.getsize(ziel) <= max_kb * 1024: break
    else:
        im.convert("P", palette=Image.ADAPTIVE, colors=128).save(ziel, optimize=True)
    print("gespeichert", os.path.relpath(ziel, WURZEL), f"{os.path.getsize(ziel) // 1024} kB")


def unterprozess(args):
    t = time.time()
    r = subprocess.run([sys.executable, os.path.abspath(__file__), *args], capture_output=True, text=True)
    for z in r.stdout.splitlines():
        if z.startswith(("RENDER", "CYCLES", "GEBAUT", "FEHLER")): print("  " + z, flush=True)
    if r.returncode:
        print(r.stdout[-3000:], r.stderr[-3000:]); sys.exit(r.returncode)
    return time.time() - t


GRUNDRISS = {   # Draufsicht: Schnitt 1,6 m über dem Geschossboden, Geschosse darüber und Dächer ausgeblendet
    "eg": dict(schnitt=GESCHOSSE["EG"] + 1.6, verstecken=("Trakt A 1OG", "Trakt A 2OG", "Trakt A Dach", "Trakt N 1OG", "Trakt N Dach", "Baeume", "Stadt")),
    "1og": dict(schnitt=GESCHOSSE["1OG"] + 1.6, verstecken=("Trakt A 2OG", "Trakt A Dach", "Trakt N Dach", "Baeume", "Stadt")),
    "2og": dict(schnitt=GESCHOSSE["2OG"] + 1.6, verstecken=("Trakt A Dach", "Baeume", "Stadt")),
}


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    befehl = sys.argv[1]
    if befehl == "bauen":
        bauen()
    elif befehl == "render":
        name = sys.argv[2]
        if "--stil" in sys.argv:                  # Stilprobe: der Name geht über die Umgebung an die Unterprozesse
            i = sys.argv.index("--stil"); os.environ["HAUS_STIL"] = sys.argv[i + 1]; del sys.argv[i:i + 2]
            if not stil(): raise SystemExit("unbekannter Stil, bekannt: " + ", ".join(STILE))
        if len(sys.argv) > 3:                     # Unterprozess: ein Durchgang
            durchgang(name, sys.argv[3]); return
        arten = ("flat", "sun", "lines") if (stil() or {}).get("mit_sonne", True) else ("flat", "lines")
        zeiten = {art: unterprozess(["render", name, art]) for art in arten}
        k = dict(KAMERAS[name]); k.update((stil() or {}).get("kamera", {}))
        komposit(name, DOCS + (f"stil_{os.environ['HAUS_STIL']}.jpg" if stil() else f"probe_{name}.jpg"), k)
        print("ZEITEN", " ".join(f"{a} {t:.0f}s" for a, t in zeiten.items()), f"gesamt {sum(zeiten.values()):.0f}s")
    elif befehl == "grundriss":
        g = sys.argv[2]
        if g == "alle":
            for gg in GRUNDRISS: unterprozess(["grundriss", gg])
            return
        if len(sys.argv) > 3:
            o = dict(GRUNDRISS[g], mitte=(45.0, 6.5), breite=104.0, aufloesung=(1600, 600))
            durchgang("grundriss_" + g, sys.argv[3], ortho=o); return
        zeiten = {art: unterprozess(["grundriss", g, art]) for art in ("flat", "lines")}
        k = dict(KAMERAS["aussen"]); komposit("grundriss_" + g, DOCS + f"grundriss_{g}.png", k, mit_sonne=False, max_kb=200)
        print("ZEITEN", " ".join(f"{a} {t:.0f}s" for a, t in zeiten.items()))
    else:
        print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
