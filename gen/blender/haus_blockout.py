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
    ("N", "EG", "y", -6, 62.0, 69.5, 2.2, 3.0, "glas"),                                                 # Schockraum Oberlichter
    ("N", "EG", "y", 18, 62.0, 84.6, 1.0, 2.6, "glas"),                                                 # NW Band EG
    ("N", "1OG", "y", 18, 66.0, 85.2 - 0.6, 5.0, 6.6, "glas"),                                          # CPU Fensterband NW
    ("N", "1OG", "y", 18, 61.8, 65.4, 5.0, 6.6, "glas"),                                                # Warten Angehörige
    ("N", "1OG", "x", 85.2, -5.4, 6.4, 5.0, 6.6, "glas"),                                               # NE Band HKL-Arzt/Befundung
    ("N", "1OG", "x", 85.2, 7.3, 9.7, 4.9, 7.1, "glas"),                                                # Flurende 1. OG
]
BLIND_NW = {9, 10}                      # Achsen ohne NW-Fenster (Lifte L1, Blindfeld); Achse 8 liegt im Risalit

# Fassade SE (Antwort 3 des Nutzers, 23.10.2026): nicht 17 gleiche Achsen, sondern Rhythmus [PP] s s P s s [Risalit] s s P s s [PP].
# Eckrisalit nur am Westende (Achsen 1–2): das Ostende steckt im Winkel des Neubaus, dort tragen nur die Fensterpaare.
ECKRISALIT = (0.0, -0.5, 7.2, 0.0)         # x0, y0, x1, y1 — 0,5 m vor der SE-Flucht, eigener Sockel, Decken und Dachstreifen
FENSTERPAARE = {1, 2, 5, 13, 16, 17}       # Achsen mit gekoppelten Fenstern (SE und NW): zwei Flügel PAAR.b breit, Pfosten dazwischen
PAAR = dict(b=1.0, pfosten=0.3)            # Paar deckt xm ± 1,15 — bleibt 0,65 m von den Achsgrenzen (Innenwände bei x = 3,6·k) weg

# Umgebung (§5)
LINDEN = [(15.0, -10.0, 4.5), (46.0, -10.0, 4.5)]                 # (x, y, Kronenradius); nach außen gerückt (Antwort 4): bei x 18 deckte die Krone aus
                                                                  # Kamera (a) per Parallaxe noch das Portal (Blick diagonal), ab x 15 / y −10 ist der Risalit frei
KASTANIE = (50.0, 27.0, 6.0)
VORPLATZ = (20.0, -20.0, 41.0, -3.0)
PARKWEG = [(30.0, -20.0), (14.0, -34.0), (44.0, -52.0), (60.0, -70.0)]           # zwei Kehren
KLINIKSTRASSE = [(103.0, -80.0), (103.0, 40.0)]
RETTUNGSZUFAHRT = [(103.0, -1.0), (91.0, -1.0)]
PLATANEN = [(98.0, y, 4.0) for y in (-70, -50, -30, -10, 10, 30)]
PARKPLATZ = (70.0, 20.0, 100.0, 40.0)
WALDTOR = (48.0, 34.0)
TERRASSE_Y = -40.0           # bis hier eben (z −0,6), dann 6 % Gefälle nach Südost
TAL_Y = -200.0               # ab hier Talboden
WALD_Y = 35.0                # dahinter steigt der Waldhang mit 10 % …
WALD_STEIL = (60.0, 0.25)    # … und ab y 60 mit 25 % (Hügelrücken): sonst verschwinden die Waldbänder aus Kamera (a) hinter dem First
OSTHANG_X = 115.0            # östlich der Klinikstraße fällt das Gelände mit 8 % in die Talbiegung nach Nordost (bis −25 m)
HIMMEL_BAENDER = ["#F8E7BF", "#F6DCA4", "#F3CD8C"]            # oben → Horizont (§9 a)

# Vordergrund von Render (a): Büsche (x, y, Radius) auf Terrasse und Hang, Wiesenflecken zufällig im Bildausschnitt
BUESCHE = [(-8.0, -44.0, 1.6), (-4.5, -45.5, 1.2), (6.0, -41.0, 1.4), (9.0, -42.5, 1.0), (22.0, -36.0, 1.3),
           (0.0, -56.0, 1.8), (3.5, -57.5, 1.3), (-14.0, -50.0, 1.5), (30.0, -27.0, 1.2), (34.0, -45.0, 1.4)]
WIESENFLECKEN = dict(bereich=(-40.0, -70.0, 90.0, -5.0), anzahl=18, radius=(4.0, 11.0))

# Wald (§5): nahes Band als dichte Baumgruppen (zwei Reihen), Mitte und Ferne als Silhouettenbänder (ein Netz je Band).
# Tiefenstaffelung: vorn Laub (grün, besonnt), Mitte Petrol (Kamm im Schatten, die dunkle Form), hinten Papier (Dunst).
WALD_NAH = dict(x0=-10.0, x1=150.0, reihen=((38.0, 44.0), (45.0, 52.0)), abstand=6.0, hoehe=(17.0, 26.0))
WALD_WEST = dict(x0=-62.0, x1=-24.0, y0=-40.0, y1=38.0, abstand=(8.0, 9.0), hoehe=(16.0, 24.0))
WALDBAENDER = [(76.0, -150.0, 185.0, "wald_mitte", (20.0, 28.0)), (106.0, -160.0, 205.0, "wald_fern", (22.0, 30.0))]   # (y, x0, x1, Material, Höhen)

# Stadt (§5): im Tal südöstlich (y < −200, von Kamera (a) nicht sichtbar) UND in der Talbiegung nordöstlich der Klinikstraße,
# die Kamera (a) rechts neben Trakt N über den Osthang sieht (Unterstadt mit dem zweiten Kirchturm). Nur Bänder, keine Linie.
STADT = [dict(x0=-120.0, x1=200.0, y0=-290.0, y1=-210.0, haeuser=40, tuerme=((20.0, -250.0, "helm"), (110.0, -250.0, "zwiebel"))),
         dict(x0=185.0, x1=345.0, y0=0.0, y1=140.0, haeuser=150, tuerme=((230.0, 40.0, "zwiebel"), (300.0, 55.0, "helm")))]   # Kamera (a) sieht 18–25° rechts von +x: y ≈ 0,32·(x+30)−62 … 0,51·(x+30)−62
HUEGEL = [(-110.0, -260.0, 70.0, 40.0), (190.0, -270.0, 80.0, 50.0), (380.0, 60.0, 190.0, 55.0), (470.0, -80.0, 200.0, 70.0)]   # (x, y, r, sichtbare Höhe); zwei lange Kämme schließen das Tal nach Osten

# Kameras (§9): Ort, Ziel, Brennweite; Sonne (Azimut °, Höhe °); Licht- und Himmelsfarben
KAMERAS = {
    "aussen": dict(ort=(-30.0, -62.0, 3.0), ziel=(34.0, 2.0, 7.0), brennweite=35, sonne=(80.0, 7.0),
                   licht="#FFF0C6", anteil=0.45, himmel=HIMMEL_BAENDER, schatten=0.14),
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
    "wiese": "#ACB98B", "wiese_hell": "#B9C59A", "weg": "#F7F1E4", "asphalt": "#B6BFB6", "pflaster": "#F7F1E4", "hecke": "#6F8A62",
    "stamm": "#2C3E46", "laub": "#6F8A62", "wald_nah": "#6F8A62", "wald_mitte": "#2C5560", "wald_fern": "#F7F1E4",
    "stadt": "#F7F1E4", "stadt_sand": "#EFE6D3", "stadt_dach": "#C9BDA2", "himmel_0": HIMMEL_BAENDER[0], "himmel_1": HIMMEL_BAENDER[1],
    "himmel_2": HIMMEL_BAENDER[2], "beet": "#C99A5B",
}
OHNE_LINIE = {"himmel_0", "himmel_1", "himmel_2", "wald_fern", "stadt", "stadt_sand", "stadt_dach", "wiese_hell"}
OHNE_SCHATTIERUNG = {"himmel_0", "himmel_1", "himmel_2", "glas", "wald_fern", "wald_mitte", "stadt", "stadt_sand", "stadt_dach", "wiese_hell"}
OHNE_SCHATTEN = {"Baeume"}               # Sammlungen, deren Objekte keinen Schatten werfen (Ligne claire: Licht nur als harte, geometrische Form;
                                         # Baumkronen zerlegten die Fassade sonst in Flecken). Büsche (Umgebung) werfen Schatten.
SONNE_AUS_MATERIAL = {"glas"}            # Glas lässt die Sonne durch (Sonnen-Durchgang ohne Scheiben)


def hexc(s):
    return tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))


def hex_lin(s):
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in hexc(s))


def gelaende_z(x, y):
    """Höhe des Geländes (§5): Terrasse eben, Hang 6 % nach Südost ab y −40, Waldhang 10 % ab y 35; östlich der
    Klinikstraße (x > 115) fällt alles mit 8 % in die Talbiegung nach Nordost (dort liegt die Unterstadt)."""
    if y >= WALD_STEIL[0]: z = 0.1 * (WALD_STEIL[0] - WALD_Y) + WALD_STEIL[1] * (y - WALD_STEIL[0])
    elif y >= WALD_Y: z = 0.1 * (y - WALD_Y)
    elif y >= A["y1"]: z = 0.0
    elif y >= 0: z = -SOCKEL * (1 - y / A["y1"])          # Übergang unter dem Haus (unsichtbar)
    elif y >= TERRASSE_Y: z = -SOCKEL
    elif y >= TAL_Y: z = -SOCKEL - 0.06 * (TERRASSE_Y - y)
    else: z = -SOCKEL - 0.06 * (TERRASSE_Y - TAL_Y)
    if x > OSTHANG_X: z -= min(0.08 * (x - OSTHANG_X), 25.0)
    return z


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
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
        if min(x1 - x0, y1 - y0, z1 - z0) < 1e-4: return None
        o = wz.kiste((x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), M[m], "hinten", fase=fase, name=name)
        return einordnen(o, samm)

    def netz(name, verts, faces, m, samm, glatt=False):
        me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
        o = bpy.data.objects.new(name, me); o.data.materials.append(M[m]); sc.collection.objects.link(o)
        wz.markiere(o, "hinten")
        return einordnen(o, samm)

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
    schritt, xa, xb, ya, yb = 5.0, -140.0, 480.0, -300.0, 160.0
    nx, ny = int((xb - xa) / schritt) + 1, int((yb - ya) / schritt) + 1
    verts = [(xa + i * schritt, ya + j * schritt, gelaende_z(xa + i * schritt, ya + j * schritt)) for j in range(ny) for i in range(nx)]
    faces = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i) for j in range(ny - 1) for i in range(nx - 1)]
    netz("Gelaende", verts, faces, "wiese", "Gelaende")

    def band(name, punkte, breite, m, samm="Gelaende", hoch=0.03):
        """Weg/Straße als Streifen, der dem Gelände folgt (Höhe aus gelaende_z + hoch)."""
        v, f = [], []
        for i, (x, y) in enumerate(punkte):
            p0 = punkte[max(i - 1, 0)]; p1 = punkte[min(i + 1, len(punkte) - 1)]
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]; l = math.hypot(dx, dy) or 1
            nx_, ny_ = -dy / l * breite / 2, dx / l * breite / 2
            for s in (1, -1):
                v.append((x + s * nx_, y + s * ny_, gelaende_z(x + s * nx_, y + s * ny_) + hoch))
        for i in range(len(punkte) - 1):
            f.append((2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1))
        return netz(name, v, f, m, samm)

    def flaeche(name, x0, y0, x1, y1, m, samm="Gelaende", hoch=0.02):
        z = gelaende_z((x0 + x1) / 2, (y0 + y1) / 2) + hoch
        return netz(name, [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [(0, 1, 2, 3)], m, samm)

    flaeche("Vorplatz", *VORPLATZ, "pflaster")
    band("Parkweg", PARKWEG, 3.0, "weg")
    band("Klinikstrasse", KLINIKSTRASSE, 6.0, "asphalt")
    band("Rettungszufahrt", RETTUNGSZUFAHRT, 5.0, "asphalt")
    flaeche("Abstellflaeche Rettung", 91.2, -4.0, 100.0, 2.0, "asphalt")
    flaeche("Parkplatz Personal", *PARKPLATZ, "asphalt")
    flaeche("Terrasse Cafeteria", 36.0, 16.0, 50.4, 20.0, "pflaster")
    kiste("Hecke Parkplatz", 69.0, 19.0, 101.0, 20.0, 0.0, 1.6, "hecke", "Umgebung")
    for i, (x, y) in enumerate(((16, -28), (40, -46))):          # Hecken an den Kehren des Parkwegs
        kiste(f"Hecke Parkweg {i + 1}", x - 6, y - 0.6, x + 6, y + 0.6, gelaende_z(x, y), gelaende_z(x, y) + 1.2, "hecke", "Umgebung")
    for i in range(6):                                            # Laternen am Parkweg alle 15 m (grob entlang der Kehren)
        t = i / 5; j = min(int(t * 3), 2); u = t * 3 - j
        x = PARKWEG[j][0] + (PARKWEG[j + 1][0] - PARKWEG[j][0]) * u; y = PARKWEG[j][1] + (PARKWEG[j + 1][1] - PARKWEG[j][1]) * u
        z = gelaende_z(x, y)
        einordnen(wz.zylinder(0.06, 3.5, (x + 1.8, y, z + 1.75), M["petrol"], "hinten", v=8, name=f"Laterne {i + 1}"), "Umgebung")
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

    def baum(name, x, y, r, art="laub", m="laub", samm="Baeume", hoehe=None, z=None):
        """laub: Stamm sichtbar, zwei Astansätze, Krone aus 5–7 Kugeln. foehre: hoher Stamm, lichter Schirm aus drei
        flachen Kugeln. fichte: vier gestapelte Kegel mit Lücken. Zufall je Baum aus dem Namen (reproduzierbar)."""
        zr = random.Random(name); z = gelaende_z(x, y) if z is None else z
        if art == "laub":
            h = hoehe or r * 2.6; hs = h * 0.36; rs = max(0.12, r * 0.07)
            stamm = wz.zylinder(rs, hs + 0.4, (x, y, z + (hs + 0.4) / 2), M["stamm"], "hinten", v=8, name=name + " Stamm")
            aeste = [stamm]
            for j in range(2):                                     # zwei Äste schräg in die Krone
                ang = zr.uniform(0, 2 * math.pi); neig = math.radians(zr.uniform(28, 42)); la = r * 0.55
                dreh = (neig * math.sin(ang), -neig * math.cos(ang), 0)
                mitte = (x + math.sin(neig) * la / 2 * math.cos(ang), y + math.sin(neig) * la / 2 * math.sin(ang), z + hs + math.cos(neig) * la / 2)
                aeste.append(wz.zylinder(rs * 0.5, la, mitte, M["stamm"], "hinten", dreh=dreh, v=6, name=name + " Ast"))
            einordnen(vereinen(aeste, name + " Stamm"), samm)
            zc = z + hs + (h - hs) * 0.5
            einordnen(krone_kugeln(name, x, y, zc, r, (h - hs) * 0.22, zr, 5 + zr.randint(0, 2), m), samm)
        elif art == "foehre":
            h = hoehe or r * 3.4; hs = h * 0.62; rs = max(0.14, r * 0.08)
            einordnen(wz.zylinder(rs, hs + 0.3, (x + zr.uniform(-0.3, 0.3), y, z + (hs + 0.3) / 2), M["stamm"], "hinten", v=8, name=name + " Stamm"), samm)
            einordnen(krone_kugeln(name, x, y, z + hs + (h - hs) * 0.45, r * 0.95, (h - hs) * 0.18, zr, 3, m, flach=(0.45, 0.6)), samm)
        else:                                                      # fichte: Etagen
            h = hoehe or r * 3.2; hs = h * 0.18; rs = max(0.12, r * 0.07)
            einordnen(wz.zylinder(rs, h * 0.6, (x, y, z + h * 0.3), M["stamm"], "hinten", v=8, name=name + " Stamm"), samm)
            teile = []; etagen = 4; z0 = z + hs
            for j in range(etagen):
                rj = r * (1.0 - 0.2 * j) * zr.uniform(0.9, 1.1); hj = (h - hs) / etagen * 1.45
                zj = z0 + (h - hs) / etagen * j
                teile.append(wz.kegel(rj, rj * 0.1 if j < etagen - 1 else 0.0, hj, (x, y, zj + hj / 2), M[m], "hinten", v=9, name=name))
            einordnen(vereinen(teile, name), samm)

    def busch(name, x, y, r, m="laub", samm="Umgebung"):
        zr = random.Random(name); z = gelaende_z(x, y)
        einordnen(krone_kugeln(name, x, y, z + r * 0.55, r, r * 0.2, zr, 3 + zr.randint(0, 2), m, flach=(0.6, 0.8)), samm)

    for i, (x, y, r) in enumerate(LINDEN): baum(f"Linde {i + 1}", x, y, r)
    baum("Kastanie", *KASTANIE)
    for i, (x, y, r) in enumerate(PLATANEN): baum(f"Platane {i + 1}", x, y, r)
    for i, (x, y, r) in enumerate(BUESCHE): busch(f"Busch {i + 1}", x, y, r)
    for i, (x, y) in enumerate(((38, 24), (54, 20))):
        kiste(f"Holzbank Garten {i + 1}", x - 0.9, y - 0.25, x + 0.9, y + 0.25, 0.0, 0.45, "holz", "Umgebung")
    for i, x in enumerate((26, 34)):                              # Bänke und Fahrradständer am Vorplatz
        kiste(f"Bank Vorplatz {i + 1}", x - 0.9, -8.0, x + 0.9, -7.5, -SOCKEL, -SOCKEL + 0.45, "holz", "Umgebung")
    kiste("Fahrradstaender", 21.0, -5.5, 24.0, -4.5, -SOCKEL, -SOCKEL + 0.8, "petrol", "Umgebung")
    zufall = random.Random(7)
    # Wiesenflecken: hellere Ellipsen auf der Wiese (ohne Linie, ohne Schattierung), folgen dem Gelände
    wf = WIESENFLECKEN; fx0, fy0, fx1, fy1 = wf["bereich"]
    for i in range(wf["anzahl"]):
        cx, cy = zufall.uniform(fx0, fx1), zufall.uniform(fy0, fy1); ra = zufall.uniform(*wf["radius"]); rb = ra * zufall.uniform(0.35, 0.7)
        dreh = zufall.uniform(0, math.pi); n = 12
        v = [(cx, cy, gelaende_z(cx, cy) + 0.015)]
        for j in range(n):
            t = 2 * math.pi * j / n; ex, ey = ra * math.cos(t), rb * math.sin(t)
            px, py = cx + ex * math.cos(dreh) - ey * math.sin(dreh), cy + ex * math.sin(dreh) + ey * math.cos(dreh)
            v.append((px, py, gelaende_z(px, py) + 0.015))
        netz(f"Wiesenfleck {i + 1}", v, [(0, 1 + j, 1 + (j + 1) % n) for j in range(n)], "wiese_hell", "Gelaende")
    # Wald (§5): nahes Band als dichte Gruppe in zwei Reihen (Laub, Föhren, Fichten gemischt), dahinter Silhouettenbänder
    wn = WALD_NAH
    for reihe, (y0, y1) in enumerate(wn["reihen"]):
        x = wn["x0"] + reihe * wn["abstand"] / 2
        while x < wn["x1"]:
            xx = x + zufall.uniform(-1.5, 1.5); yy = zufall.uniform(y0, y1); w = zufall.random()
            art = "laub" if w < 0.5 else ("foehre" if w < 0.8 else "fichte")
            baum(f"Wald {reihe + 1} {x:g}", xx, yy, zufall.uniform(3.5, 5.5), art, "wald_nah", hoehe=zufall.uniform(*wn["hoehe"]))
            x += wn["abstand"]
    ww = WALD_WEST
    for x in range(int(ww["x0"]), int(ww["x1"]), int(ww["abstand"][0])):     # Wald westlich (x < −20), rahmt Render (a) links
        for y in range(int(ww["y0"]), int(ww["y1"]), int(ww["abstand"][1])):
            w = zufall.random(); art = "laub" if w < 0.5 else ("foehre" if w < 0.8 else "fichte")
            baum(f"Wald W {x} {y}", x + zufall.uniform(-2, 2), y + zufall.uniform(-2, 2), zufall.uniform(3.5, 5.5), art, "wald_nah", hoehe=zufall.uniform(*ww["hoehe"]))

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
            v.append((x, y, basis - 3.0)); v.append((x, y, basis + top))
            if i: f.append((2 * i - 2, 2 * i, 2 * i + 1, 2 * i - 1))
        return netz(name, v, f, m, "Baeume")

    for i, (y, x0, x1, m, hoehen) in enumerate(WALDBAENDER): waldband(f"Waldband {i + 1}", y, x0, x1, m, hoehen)

    # ---------------- Stadt im Tal: ferne Kulisse (Papier/Sand, ohne Linie), Hügel ----------------
    def stadt(nr, st):
        zr = random.Random(100 + nr)
        for i in range(st["haeuser"]):
            x = zr.uniform(st["x0"], st["x1"]); y = zr.uniform(st["y0"], st["y1"]); b = zr.uniform(8, 22); t = zr.uniform(7, 14)
            if zr.random() < 0.5: b, t = t, b
            zg = gelaende_z(x + b / 2, y + t / 2); h = zr.uniform(6, 11); m = "stadt" if i % 3 else "stadt_sand"
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
    kiste("Sockel Eckrisalit", *ECKRISALIT, -SOCKEL, 0.0, "sockel", "Trakt A EG")
    kiste("Sockel Risalit NW", *RISALIT_NW, -SOCKEL, 0.0, "sockel", "Trakt A EG")
    kiste("Sockel N", N["x0"], N["y0"], N["x1"], N["y1"], -SOCKEL, 0.0, "sockel", "Trakt N EG")

    E = ECKRISALIT; tan_d = math.tan(math.radians(DACH["neigung"]))
    eck_oben = DACH["traufe"] + E[1] * tan_d - 0.1                 # Oberkante von Wand und Decke des Eckrisalits im 2. OG: unter der verlängerten Dachfläche

    def decke(name, x0, y0, x1, y1, z_unten, samm, oben=None):
        z_oben = z_unten + (GESCHOSS - RAUMHOEHE["A" if "A" in samm else "N"])
        kiste(name, x0, y0, x1, y1, z_unten, min(z_oben, oben) if oben else z_oben, "decke", samm)

    for g, z in GESCHOSSE.items():
        samm = f"Trakt A {g}"
        decke(f"Decke A {g}", A["x0"], A["y0"], A["x1"], A["y1"], z + RAUMHOEHE["A"], samm)
        decke(f"Decke Risalit SE {g}", *RISALIT_SE, z + RAUMHOEHE["A"], samm)
        decke(f"Decke Eckrisalit {g}", *ECKRISALIT, z + RAUMHOEHE["A"], samm, oben=eck_oben)
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
                im_eck = ECKRISALIT[0] <= xm <= ECKRISALIT[2]
                lage_se = RISALIT_SE[1] if im_risalit else (ECKRISALIT[1] if im_eck else A["y0"])
                for (x0, x1) in oeffnungen:
                    if g == "EG" and im_risalit: pass                   # Portal und hohe Fenster (SONDERFENSTER)
                    else: aus.append((g, "y", lage_se, x0, x1, z0, z1))
                    if k not in BLIND_NW and not (RISALIT_NW[0] <= xm <= RISALIT_NW[2]):
                        aus.append((g, "y", A["y1"], x0, x1, z0, z1))
        return aus

    FENSTER_ALLE = [("A", *f, "glas") for f in achsfenster()] + SONDERFENSTER + \
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
        return wandnetz(name, achse, w0, w1, a0, a1, z, oben or z + GESCHOSS, oeffnungen, "putz", f"Trakt {trakt} {g}")

    def scheibe(trakt, g, achse, lage, f0, f1, z0, z1, art, innen_seite):
        """Rahmen (Petrol) und Scheibe (Glas) in der Laibung, 0,3 m hinter der Außenflucht."""
        tiefe = 0.3 * innen_seite; d = 0.06
        m = {"glas": "glas", "portal": "glas", "tor": "tor"}[art]
        samm = f"Trakt {trakt} {g}"
        if achse == "y":
            kiste(f"Scheibe {achse}{lage:g} {f0:g} {g}", f0, lage + tiefe - d / 2, f1, lage + tiefe + d / 2, z0, z1, m, samm)
            for a in (f0, f1 - 0.08): kiste("Rahmen", a, lage + tiefe - 0.05, a + 0.08, lage + tiefe + 0.05, z0, z1, "rahmen", samm)
            for zz in (z0, z1 - 0.08): kiste("Rahmen", f0, lage + tiefe - 0.05, f1, lage + tiefe + 0.05, zz, zz + 0.08, "rahmen", samm)
        else:
            kiste(f"Scheibe {achse}{lage:g} {f0:g} {g}", lage + tiefe - d / 2, f0, lage + tiefe + d / 2, f1, z0, z1, m, samm)
            for a in (f0, f1 - 0.08): kiste("Rahmen", lage + tiefe - 0.05, a, lage + tiefe + 0.05, a + 0.08, z0, z1, "rahmen", samm)
            for zz in (z0, z1 - 0.08): kiste("Rahmen", lage + tiefe - 0.05, f0, lage + tiefe + 0.05, f1, zz, zz + 0.08, "rahmen", samm)

    for g in GESCHOSSE:
        # Trakt A: SE-Front mit Eckrisalit (West) und Mittelrisalit, NW-Front mit Treppenhausrisalit, Stirnwände x 0 und x 61,2
        aussenwand("A", g, "y", E[1], E[0], E[2], +1, oben=eck_oben if g == "2OG" else None)
        kiste(f"Eckrisalit Ruecksprung {g}", E[2] - A["aussen"], E[1] + A["aussen"], E[2], E[3], GESCHOSSE[g], GESCHOSSE[g] + GESCHOSS, "putz", f"Trakt A {g}")
        aussenwand("A", g, "y", A["y0"], E[2], RISALIT_SE[0], +1); aussenwand("A", g, "y", A["y0"], RISALIT_SE[2], A["x1"], +1)
        aussenwand("A", g, "y", RISALIT_SE[1], RISALIT_SE[0], RISALIT_SE[2], +1)
        aussenwand("A", g, "x", RISALIT_SE[0], RISALIT_SE[1], A["y0"], +1); aussenwand("A", g, "x", RISALIT_SE[2], RISALIT_SE[1], A["y0"], -1)
        aussenwand("A", g, "y", A["y1"], A["x0"], RISALIT_NW[0], -1); aussenwand("A", g, "y", A["y1"], RISALIT_NW[2], A["x1"], -1)
        aussenwand("A", g, "y", RISALIT_NW[3], RISALIT_NW[0], RISALIT_NW[2], -1)
        aussenwand("A", g, "x", RISALIT_NW[0], A["y1"], RISALIT_NW[3], +1); aussenwand("A", g, "x", RISALIT_NW[2], A["y1"], RISALIT_NW[3], -1)
        aussenwand("A", g, "x", A["x0"], E[1], A["y0"], +1, oben=eck_oben if g == "2OG" else None)   # Stirnwand: Stück im Eckrisalit …
        aussenwand("A", g, "x", A["x0"], A["y0"], A["y1"], +1)                                          # … und Hauptteil
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
    # Eckrisalit: die SE-Dachfläche läuft über ihm 0,5 m weiter hinaus (gleiche Neigung), als flaches Prisma mit Unterseite
    ex0, ex1, ey0, ey1 = E[0] - u, E[2] + u, E[1] - u, A["y0"] - u
    ez0 = ze + (ey0 - ey1) * tan
    netz("Dach Eckrisalit", [(ex0, ey0, ez0), (ex1, ey0, ez0), (ex1, ey1, ze), (ex0, ey1, ze),
                              (ex0, ey0, ez0 - 0.2), (ex1, ey0, ez0 - 0.2), (ex1, ey1, ze - 0.2), (ex0, ey1, ze - 0.2)],
         [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (3, 2, 6, 7), (0, 3, 7, 4), (1, 5, 6, 2)], "ziegel", "Trakt A Dach")
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
    for i, x in enumerate([N["x0"] + 0.4 + 0.6 * j for j in range(int((N["x1"] - N["x0"] - 0.8) / 0.6) + 1)]):   # Lamellen SE, 1. OG
        kiste(f"Lamelle SE {i + 1}", x, N["y0"] - 0.32, x + 0.1, N["y0"] - 0.2, GESCHOSS + 0.3, zn - 0.3, "lamelle", "Trakt N 1OG")
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
        k = KAMERAS[kamera_name]; aufl = (B, H)
        gier = kamera_stellen(sc, k, aufl)
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
        emission_ueberall(lambda n: hex_lin(PALETTE[n]) if n in PALETTE else (0.5, 0.5, 0.5))
        for m in bpy.data.materials:
            if m.node_tree and m.name not in OHNE_SCHATTIERUNG and m.node_tree.nodes.get("Material Output"): stufen_nach_richtung(m)
        welt(hex_lin(k["himmel"][0])); sichtbar(); proben = PROBEN["flat"]
    elif art == "lines":
        emission_ueberall(lambda n: (1, 1, 1)); welt((1, 1, 1)); sichtbar(OHNE_LINIE)
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
        if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new("claire")
        ls.linestyle.color = (0, 0, 0); ls.linestyle.alpha = 1.0; ls.linestyle.thickness = 1.5 * UEBER; ls.linestyle.caps = "ROUND"
        proben = PROBEN["lines"]
    elif art == "sun":
        for m in bpy.data.materials:
            if not m.node_tree: continue
            b = m.node_tree.nodes.get("Principled BSDF")
            if b is None: continue
            b.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1); b.inputs["Roughness"].default_value = 0.7
            if m.name in OHNE_SCHATTIERUNG:        # Himmel und Fernes gelten als beleuchtet (kein Schatten im Komposit)
                b.inputs["Emission Color"].default_value = (1, 1, 1, 1); b.inputs["Emission Strength"].default_value = 1.0
        welt((0, 0, 0), 0.0); sc.cycles.max_bounces = 0; sichtbar(SONNE_AUS_MATERIAL); proben = PROBEN["sun"]
        for o in bpy.data.objects:                 # Bäume werfen keinen Schatten (OHNE_SCHATTEN), bleiben aber selbst besonnt
            if o.type == 'MESH' and any(c.name in OHNE_SCHATTEN for c in o.users_collection): o.visible_shadow = False
    else:
        raise SystemExit("unbekannter Durchgang " + art)
    sc.cycles.samples = proben; sc.cycles.use_denoising = art == "sun"
    sc.render.filepath = BAU + f"{kamera_name}_{art}.png"
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
    lade = lambda n: np.asarray(Image.open(BAU + f"{kamera_name}_{n}.png").convert("RGB")).astype(np.float32) / 255
    flach = lade("flat"); t = ko.tinte(lade("lines"))[..., None]
    if mit_sonne:
        ls = ko.luma(lade("sun"))
        licht = np.clip((ls - 0.35) / 0.08 + 0.5, 0, 1)
        licht = np.asarray(Image.fromarray((licht * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))).astype(np.float32) / 255
        licht = ko.weich(licht, 0.7)[..., None]
        schatten = (1 - licht) * k["schatten"]
        flach = flach * (1 - schatten) + ko.SCHATTEN * schatten          # Schattenseite: flache Stufe
        flach = flach * (1 - licht * k["anteil"]) + ko.hexc(k["licht"]) * licht * k["anteil"]
    bild = flach * (1 - t) + ko.TINTE * t
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
        if len(sys.argv) > 3:                     # Unterprozess: ein Durchgang
            durchgang(name, sys.argv[3]); return
        zeiten = {art: unterprozess(["render", name, art]) for art in ("flat", "sun", "lines")}
        komposit(name, DOCS + f"probe_{name}.jpg", KAMERAS[name])
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
