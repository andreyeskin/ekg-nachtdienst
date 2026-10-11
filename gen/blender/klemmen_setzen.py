"""Die vier Extremitätenklemmen auf Jonas (Lehrsaal) zeichnet der Code in sein Quellbild — Flux Kontext setzt so
kleine Dinge nicht zuverlässig an Handgelenke und Knöchel (zwei Versuche: eine bunte Armbanduhr, sonst nichts).

    python3 gen/blender/klemmen_setzen.py            # art/figuren_quelle/jonas.png (an Ort und Stelle, deckend: wiederholbar)

Lage je Klemme in Pixeln des Quellbilds (1248 x 832, bau/blender/figuren/ki_jonas_s21.png), von Hand abgelesen:
Mitte des Gelenks, Richtung der Gliedmaße (Grad), Seite, zu der das kurze Leitungsende zeigt. Ampel-Regel
(docs/FACHREGELN.md, Lektion 2): rot = rechter Arm (das eine Rost-Objekt des Raums, docs/raeume/lehrsaal.md §3),
gelb = linker Arm, grün = linkes Bein, schwarz = rechtes Bein; seine rechte Seite liegt zur Kamera (unten im Bild).
Klemmen sitzen auf Haut: Handgelenke, Unterschenkel knapp über den Socken (Hosenbeine hochgekrempelt). Ligne claire:
flache Farbe, eine Tuschelinie, kein Verlauf. Nach einem neuen Kontext-Bild Lagen neu ablesen.
"""
import math
import os

from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))
QUELLE = os.path.join(WURZEL, "art", "figuren_quelle", "jonas.png")
TINTE = (30, 42, 48, 255)
KLEMMEN = [   # (Farbe, Mitte x, y, Winkel der Gliedmaße, Leitungsrichtung in Grad)
    ("#B5552D", (236, 506), 50, 140),    # rechtes Handgelenk (naher Arm, unten links): Leitung nach unten links zur Polsterkante
    ("#E8D44D", (800, 336), 23, -60),    # linkes Handgelenk (ferner Arm, oben rechts): Leitung nach oben rechts
    ("#1E2A30", (716, 650), 25, 120),    # rechter Unterschenkel (nahes Bein) über der Socke: Leitung nach unten
    ("#1F6B5A", (986, 528), 18, -70),    # linker Unterschenkel (fernes Bein) über der Socke: Leitung nach oben
]


def hexc(s): return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def klemme(img, farbe, mitte, winkel, leitung, laenge=0.028, breite=0.052, tief=0.022):
    """Klemme als gedrehtes Rechteck quer zur Gliedmaße (Maße in Anteilen der Bildhöhe), Leitungsstummel, Kontur."""
    h = img.height; L, B = laenge * h, breite * h
    ex, ey = math.cos(math.radians(winkel)), math.sin(math.radians(winkel))       # entlang der Gliedmaße
    nx, ny = -ey, ex                                                               # quer dazu
    cx, cy = mitte
    ecken = [(cx + sx * L / 2 * ex + sy * B / 2 * nx, cy + sx * L / 2 * ey + sy * B / 2 * ny) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    d = ImageDraw.Draw(img)
    lx, ly = math.cos(math.radians(leitung)), math.sin(math.radians(leitung))
    d.line([(cx, cy), (cx + lx * tief * h * 1.7, cy + ly * tief * h * 1.7)], fill=TINTE, width=max(2, int(h * 0.004)))
    d.polygon(ecken, fill=hexc(farbe), outline=TINTE, width=max(2, int(h * 0.0025)))
    # Klemmenkerbe: kurzer Strich quer über die Mitte (die Feder der Klemme)
    d.line([(cx - nx * B / 2 * 0.8, cy - ny * B / 2 * 0.8), (cx + nx * B / 2 * 0.8, cy + ny * B / 2 * 0.8)], fill=TINTE, width=max(1, int(h * 0.0018)))


def umfaerben(img, mitte, r, von, nach, toleranz=70):
    """Kontext malte an beiden Handgelenken ein rostfarbenes Band: am linken wird es gelb (Teil der gelben Klemme),
    sonst gäbe es zwei Rost-Objekte und die Ampel-Regel stimmte nicht. Nur im Umkreis r um `mitte`."""
    import numpy as np
    a = np.asarray(img).astype(np.int32); h, w = a.shape[:2]
    yy, xx = np.mgrid[:h, :w]; nah = (xx - mitte[0]) ** 2 + (yy - mitte[1]) ** 2 < r * r
    v = np.array(hexc(von)[:3]); d = np.abs(a[..., :3] - v).sum(-1)
    m = nah & (d < toleranz) & (a[..., 3] > 0)
    a[m, :3] = hexc(nach)[:3]
    return Image.fromarray(a.astype("uint8"), "RGBA")


def main():
    img = Image.open(QUELLE).convert("RGBA")
    img = umfaerben(img, KLEMMEN[1][1], 45, "#B5552D", KLEMMEN[1][0])
    for farbe, mitte, winkel, leitung in KLEMMEN:
        klemme(img, farbe, mitte, winkel, leitung)
    img.save(QUELLE, optimize=True)
    print("Klemmen gesetzt ->", os.path.relpath(QUELLE, WURZEL), img.size)


if __name__ == "__main__":
    main()
