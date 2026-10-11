"""Ligne-claire-Komposit: Lokalfarbe, eine flache Kontaktschatten-Stufe (aus dem AO-Durchgang), das Sonnenlicht
als harte (oder weiche) Form, darüber eine Tuschelinie.

    python3 gen/blender/komposit.py <raum>            nur art/szenen/<raum>/vorschau.png
    python3 gen/blender/komposit.py <raum> --layers   dazu hintergrund.png und mittelgrund.png (mit Alpha)

Liest die Durchgänge aus bau/blender/<raum>/ (ebenen.py).
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))


def hexc(s):
    return np.array([int(s[i:i + 2], 16) / 255 for i in (1, 3, 5)], np.float32)


TINTE = hexc("#1E2A30"); SCHATTEN = hexc("#2C5560")
# je Raum: Farbe und Deckkraft des Sonnenlichts, Schwelle im Sonnen-Durchgang, Weichheit der Kante (px);
# Kontaktschatten (eine Stufe dunkler, Richtung Petrol) aus dem AO-Durchgang (Schwelle `ao`, 0 = aus)
# und/oder aus dem Durchgang „kontakt" (Licht von oben, geometrische Formen unter Möbeln)
STANDARD = dict(licht="#FFF6DC", anteil=0.32, schwelle=0.35, weich=0.7, ao=0.62, kontakt=False)
EINSTELLUNG = {
    "aufnahme": dict(licht="#FFF0C6", anteil=0.5, schwelle=0.35, weich=0.5, ao=0.0, kontakt=True),   # 06:40, warm, hart; Schatten von oben statt AO-Flecken
    # 09:15, kühl, weicher. AO bleibt aus: der helle, offene Raum erreicht nirgends tiefe Verdeckung
    # (Minimum ~0,6), die Schwelle schnitt nur Flecken an Wandecken aus — dafür Schatten von oben.
    "monitor": dict(licht="#FBFDF8", anteil=0.42, schwelle=0.30, weich=1.2, ao=0.0, kontakt=True),
    # 08:10, neutrales Vormittagslicht von rechts, harte Fensterflecken auf Boden, Wagen und Liege; Schatten von oben
    "lehrsaal": dict(licht="#FFFBEF", anteil=0.42, schwelle=0.32, weich=0.8, ao=0.0, kontakt=True),
}


def lade(d, name, grau=False):
    pfad = d + name
    if not os.path.exists(pfad): return None
    return np.asarray(Image.open(pfad).convert("L" if grau else "RGB")).astype(np.float32) / 255


def luma(a): return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def weich(m, r):
    if r <= 0: return m
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255


def tinte(linien):
    """Linien-Durchgang (schwarz auf weiß) -> Deckkraft der Tusche; feinster Rest unter 3 % fällt weg."""
    t = 1 - luma(linien)
    return np.clip((t - 0.03) / 0.97 * 1.25, 0, 1)


def oeffnen(m, k):
    """Morphologisches Öffnen: Flächen schmaler als k px (Striche, Punkte) fallen weg, große bleiben."""
    b = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    return (np.asarray(b) > 127).astype(np.float32)


def schattenmaske(ao, kontakt, e):
    sch = None
    if ao is not None and e["ao"] > 0:
        la = np.asarray(Image.fromarray((luma(ao) * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9))
                        .filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32) / 255
        # ohne Öffnen blieben dünne Striche stehen — z. B. in der Nische zwischen Fenstersturz und Deckenleiste
        sch = oeffnen((la < e["ao"]).astype(np.float32), 7)
    if kontakt is not None and e["kontakt"]:
        k = oeffnen((luma(kontakt) < 0.5).astype(np.float32), 5)
        sch = k if sch is None else np.maximum(sch, k)
    return sch


def farbe(flach, sonne, ao, kontakt, e):
    """Lokalfarbe, Kontaktschatten, Sonnenfleck. Fehlt ein Durchgang, entfällt sein Beitrag."""
    flach = flach.copy()
    sch = schattenmaske(ao, kontakt, e)
    if sch is not None:   # Kontaktschatten: eine flache Stufe, keine Verläufe
        sch = weich(sch, 0.7)[..., None]
        flach = flach * (1 - sch) + (flach * 0.86 * 0.84 + SCHATTEN * 0.16 * 0.86) * sch
    if sonne is None: return flach
    ls = luma(sonne)
    licht = np.clip((ls - e["schwelle"]) / 0.08 + 0.5, 0, 1)      # schmale Rampe statt harter Stufe
    licht = np.asarray(Image.fromarray((licht * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))).astype(np.float32) / 255
    licht = weich(licht, e["weich"])[..., None] * e["anteil"]
    return flach * (1 - licht) + hexc(e["licht"]) * licht


def speichern(bild, pfad):
    bild.save(pfad, optimize=True); print("gespeichert", os.path.relpath(pfad, WURZEL), f"{os.path.getsize(pfad) // 1024} kB")


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        print(__doc__); sys.exit(1)
    raum = sys.argv[1]
    d = os.path.join(WURZEL, "bau", "blender", raum) + os.sep
    ziel = os.path.join(WURZEL, "art", "szenen", raum) + os.sep; os.makedirs(ziel, exist_ok=True)
    e = EINSTELLUNG.get(raum, STANDARD)

    def ganz(flach_n, sonne_n, ao_n, kontakt_n, linien_n):
        col = farbe(lade(d, flach_n), lade(d, sonne_n), lade(d, ao_n), lade(d, kontakt_n), e)
        t = tinte(lade(d, linien_n))[..., None]
        return col * (1 - t) + TINTE * t

    def rgb(a): return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))

    speichern(rgb(ganz("pass_flat.png", "pass_sun.png", "pass_ao.png", "pass_kontakt.png", "pass_lines.png")), ziel + "vorschau.png")
    if "--layers" not in sys.argv: return
    speichern(rgb(ganz("pass_flat_bg.png", "pass_sunbg.png", "pass_aobg.png", "pass_kontaktbg.png", "pass_lines_bg.png")), ziel + "hintergrund.png")

    # Mittelgrund: Farbe aus dem vollen Bild, Linie nur aus dem Mittelgrund-Durchgang, damit keine Striche
    # des Hintergrunds mitwandern (die Ebenen verschieben sich in der Parallaxe gegeneinander).
    col = farbe(lade(d, "pass_flat.png"), lade(d, "pass_sun.png"), lade(d, "pass_ao.png"), lade(d, "pass_kontakt.png"), e)
    t = tinte(lade(d, "pass_lines_mid.png"))
    maske = lade(d, "mask_mid.png", grau=True)
    col = col * (1 - t[..., None]) + TINTE * t[..., None]
    col = TINTE * (1 - maske[..., None]) + col * maske[..., None]   # außerhalb des Objekts nur Tusche
    alpha = np.clip(np.maximum(maske, t), 0, 1)
    rgba = np.dstack([np.clip(col, 0, 1), alpha])
    speichern(Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA"), ziel + "mittelgrund.png")


if __name__ == "__main__":
    main()
