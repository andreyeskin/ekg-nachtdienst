#!/usr/bin/env python3
"""Lichtprüfung: liegt das Licht im gemalten Bild dort, wo Blender es gerechnet hat?

    python3 gen/blender/licht_pruefen.py <ergebnis.png> <sonne.png> [--aus vergleich.png] [--lampe lampe.png] [--json]

<sonne.png> ist die Sonnenmaske aus szenenbild.py (weiß = Sonnenlicht). Das gemalte Bild wird auf die Maske gebracht
(Seitenverhältnis: Mitte beschneiden) und auf 640 px Breite verkleinert. „Helle Flächen" des Bildes sind die lokal
hellen Stellen: Helligkeit minus ihr großräumiger Mittelwert (Hochpass, σ = 4 % der Breite) — so zählen Sonnenstreifen
und Lichtflecken, nicht helle Wände als solche.

Gemessen wird
  korrelation   Pearson-r zwischen Sonnenmaske (leicht weich) und hellen Flächen, im ganzen Bild und in der Lichtzone
                (Maske ± 6 % der Breite): ≥ 0,35 in der Zone heißt, das Licht liegt im Wesentlichen richtig
  kontrast      mittlere Helligkeit (Hochpass, in Einheiten der Streuung) in der Maske minus daneben in der Zone:
                > 0 — die Sonnenflächen sind im Bild heller als ihre Umgebung
  versatz       Verschiebung (px, Anteil der Breite), bei der die Kreuzkorrelation am größten ist: klein = die Streifen
                liegen an derselben Stelle; groß = das Licht wurde verschoben
  richtung      Hauptrichtung der Kanten (Strukturtensor) der Blender-Streifen gegen die der gemalten hellen Flächen in
                der Zone, Unterschied in Grad: < 15° — die Streifen laufen gleich
  fremdlicht    Anteil der hellen Flächen des Bildes, die außerhalb der Lichtzone liegen (Streifen oder Flecken, die
                Blender nicht hat — etwa Jalousiestreifen auf einer Wand, auf die keine Sonne fällt)

Urteil: RICHTIG (Korrelation in der Zone ≥ 0,35, Kontrast > 0,3, Versatz < 3 %, Richtung < 15°, Fremdlicht < 40 %),
TEILWEISE (die Hälfte davon), FALSCH. Schreibt ein Vergleichsbild: Bild | Blender-Maske | Überlagerung (Maskenkanten
magenta, gemalte helle Flächen grün) | helle Flächen.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BREITE = 640


def luma(a): return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def weich(m, r):
    if r <= 0: return m
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255


def weich_f(m, r):
    """Gauß auf float ohne Beschneiden auf 0..1 (für den Hochpass)."""
    lo, hi = float(m.min()), float(m.max())
    if hi - lo < 1e-6: return m
    n = (m - lo) / (hi - lo)
    return weich(n, r) * (hi - lo) + lo


def dilatiere(m, r):
    if r <= 0: return m
    k = int(r) * 2 + 1
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(k))).astype(np.float32) / 255


def einpassen(bild, groesse):
    """Bild auf das Seitenverhältnis der Maske beschneiden (Mitte), dann skalieren."""
    w, h = bild.size; zw, zh = groesse; r = zw / zh
    if w / h > r: nw = int(h * r); bild = bild.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < r: nh = int(w / r); bild = bild.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return bild.resize(groesse, Image.LANCZOS)


def pearson(a, b, m=None):
    if m is not None: a, b = a[m], b[m]
    a = a - a.mean(); b = b - b.mean()
    n = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / n) if n > 0 else 0.0


def versatz(a, b, maxv):
    """Verschiebung (dx, dy) von b gegen a mit der größten Kreuzkorrelation (FFT), auf ±maxv px begrenzt."""
    a = a - a.mean(); b = b - b.mean()
    F = np.fft.rfft2(a) * np.conj(np.fft.rfft2(b)); c = np.fft.irfft2(F, s=a.shape)
    c = np.fft.fftshift(c); cy, cx = c.shape[0] // 2, c.shape[1] // 2
    fenster = c[cy - maxv:cy + maxv + 1, cx - maxv:cx + maxv + 1]
    iy, ix = np.unravel_index(np.argmax(fenster), fenster.shape)
    return int(ix - maxv), int(iy - maxv), float(fenster.max() / (c.max() + 1e-9))


def richtung(m, zone=None):
    """Hauptrichtung der Kanten (Grad, 0 = waagerechte Kanten, mod 180) und ihre Stärke (0..1: wie gerichtet)."""
    gy, gx = np.gradient(weich_f(m, 1.0))
    if zone is not None: gx, gy = gx * zone, gy * zone
    jxx, jyy, jxy = (gx * gx).sum(), (gy * gy).sum(), (gx * gy).sum()
    winkel = 0.5 * math.degrees(math.atan2(2 * jxy, jxx - jyy))      # Richtung des Gradienten (senkrecht zur Kante)
    staerke = math.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / (jxx + jyy + 1e-9)
    return (winkel + 90) % 180, float(staerke)                      # Kantenrichtung


def winkel_diff(a, b):
    d = abs(a - b) % 180
    return min(d, 180 - d)


def pruefen(ergebnis, sonne, lampe=None):
    maske_img = Image.open(sonne).convert("L")
    zw = BREITE; zh = int(round(maske_img.height * zw / maske_img.width))
    maske = np.asarray(maske_img.resize((zw, zh), Image.LANCZOS)).astype(np.float32) / 255
    bild = einpassen(Image.open(ergebnis).convert("RGB"), (zw, zh))
    rgb = np.asarray(bild).astype(np.float32) / 255
    L = luma(rgb)
    hp = L - weich_f(L, 0.04 * zw)                                  # helle Flächen: lokal heller als die Umgebung
    hp_n = hp / (hp.std() + 1e-6)
    mw = weich(maske, 2.0)
    zone = dilatiere((maske > 0.5).astype(np.float32), 0.06 * zw) > 0.5
    innen = maske > 0.5; aussen = zone & ~innen
    r_ganz = pearson(mw, hp_n); r_zone = pearson(mw, hp_n, zone) if zone.sum() > 100 else 0.0
    kontrast = float(hp_n[innen].mean() - hp_n[aussen].mean()) if innen.sum() > 50 and aussen.sum() > 50 else 0.0
    dx, dy, _ = versatz(mw, np.clip(hp_n, 0, None), int(0.08 * zw))
    wb, sb = richtung(mw, zone.astype(np.float32)); wg, sg = richtung(np.clip(hp_n, 0, None) / 3, zone.astype(np.float32))
    dw = winkel_diff(wb, wg)
    hell = hp_n > 1.0                                               # deutlich helle Flächen des Bildes
    fremd = float((hell & ~zone).sum() / max(hell.sum(), 1))
    aus = dict(korrelation=round(r_ganz, 3), korrelation_zone=round(r_zone, 3), kontrast=round(kontrast, 2),
               versatz_px=[dx, dy], versatz_anteil=round(math.hypot(dx, dy) / zw, 3),
               richtung_blender=round(wb, 1), richtung_bild=round(wg, 1), richtung_diff=round(dw, 1),
               fremdlicht=round(fremd, 3), maske_anteil=round(float(innen.mean()), 3))
    punkte = [r_zone >= 0.35, kontrast > 0.3, aus["versatz_anteil"] < 0.03, dw < 15, fremd < 0.4]
    aus["punkte"] = int(sum(punkte))
    aus["urteil"] = "RICHTIG" if all(punkte) else ("TEILWEISE" if sum(punkte) >= 3 else "FALSCH")
    if lampe and os.path.exists(lampe):
        lm = np.asarray(Image.open(lampe).convert("L").resize((zw, zh), Image.LANCZOS)).astype(np.float32) / 255
        lz = dilatiere((lm > 0.3).astype(np.float32), 0.06 * zw) > 0.5
        aus["lampe_korrelation_zone"] = round(pearson(weich(lm, 2.0), hp_n, lz), 3) if lz.sum() > 100 else None
    return aus, dict(rgb=rgb, maske=maske, hp=hp_n, zone=zone, hell=hell)


def vergleichsbild(aus, d, pfad):
    rgb, maske, hp, zone, hell = d["rgb"], d["maske"], d["hp"], d["zone"], d["hell"]
    h, w = maske.shape
    # Maske: gelb auf grau, Zone leicht markiert
    m_img = np.full((h, w, 3), 0.35, np.float32); m_img[zone] = 0.45
    m_img = m_img * (1 - maske[..., None]) + np.array([1.0, 0.93, 0.6]) * maske[..., None]
    # Überlagerung: Maskenkanten magenta, gemalte helle Flächen grün
    kante = np.abs(np.asarray(Image.fromarray((maske * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES))).astype(np.float32) / 255
    kante = dilatiere((kante > 0.2).astype(np.float32), 1)
    ueber = rgb * 0.75 + 0.1
    ueber = ueber * (1 - hell[..., None] * 0.5) + np.array([0.2, 0.9, 0.3]) * hell[..., None] * 0.5
    ueber = ueber * (1 - kante[..., None]) + np.array([0.85, 0.1, 0.55]) * kante[..., None]
    # helle Flächen als Grauwert
    hp_img = np.repeat(np.clip(hp / 3 + 0.5, 0, 1)[..., None], 3, -1)
    teile = [rgb, m_img, ueber, hp_img]
    out = Image.new("RGB", (w * 2 + 10, h * 2 + 10 + 48), (255, 255, 255))
    for i, t in enumerate(teile):
        out.paste(Image.fromarray((np.clip(t, 0, 1) * 255 + 0.5).astype(np.uint8)), ((i % 2) * (w + 10), (i // 2) * (h + 10)))
    z = ImageDraw.Draw(out)
    text = (f"{aus['urteil']} ({aus['punkte']}/5)  Korrelation Zone {aus['korrelation_zone']:.2f} (ganz {aus['korrelation']:.2f})  "
            f"Kontrast {aus['kontrast']:.2f}  Versatz {aus['versatz_px']} px ({aus['versatz_anteil'] * 100:.1f} %)  "
            f"Richtung Blender {aus['richtung_blender']:.0f}° / Bild {aus['richtung_bild']:.0f}° (Diff {aus['richtung_diff']:.0f}°)  "
            f"Fremdlicht {aus['fremdlicht'] * 100:.0f} %")
    z.text((8, h * 2 + 16), text, fill=(30, 42, 48))
    z.text((8, h * 2 + 32), "oben: Bild | Blender-Sonnenmaske (gelb, Zone grau)   unten: Maskenkanten magenta + helle Flächen grün | helle Flächen (Hochpass)", fill=(90, 90, 90))
    out.save(pfad); print("Vergleichsbild", pfad)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    ergebnis, sonne = args[0], args[1]
    aus_pfad = sys.argv[sys.argv.index("--aus") + 1] if "--aus" in sys.argv else os.path.splitext(ergebnis)[0] + "_licht.png"
    lampe = sys.argv[sys.argv.index("--lampe") + 1] if "--lampe" in sys.argv else None
    aus, d = pruefen(ergebnis, sonne, lampe)
    vergleichsbild(aus, d, aus_pfad)
    if "--json" in sys.argv:
        print(json.dumps(aus, ensure_ascii=False))
    else:
        print(f"Urteil: {aus['urteil']} ({aus['punkte']}/5 Kriterien)")
        print(f"  Korrelation Maske~helle Flächen: Zone {aus['korrelation_zone']:.2f}, ganzes Bild {aus['korrelation']:.2f}")
        print(f"  Kontrast (in der Maske heller als daneben): {aus['kontrast']:.2f}")
        print(f"  Versatz der besten Deckung: {aus['versatz_px']} px = {aus['versatz_anteil'] * 100:.1f} % der Breite")
        print(f"  Streifenrichtung: Blender {aus['richtung_blender']:.0f}°, Bild {aus['richtung_bild']:.0f}°, Unterschied {aus['richtung_diff']:.0f}°")
        print(f"  Fremdlicht (helle Flächen außerhalb der Lichtzone): {aus['fremdlicht'] * 100:.0f} %")
        if aus.get("lampe_korrelation_zone") is not None:
            print(f"  Lampeninsel: Korrelation in ihrer Zone {aus['lampe_korrelation_zone']:.2f}")


if __name__ == "__main__":
    main()
