#!/usr/bin/env python3
"""Lichtprüfung: liegt das Licht im gemalten Bild dort, wo Blender es gerechnet hat?

    python3 gen/blender/licht_pruefen.py <ergebnis.png> <sonne.png> [--aus vergleich.png] [--lampe lampe.png]
                                         [--quellen quellen.png] [--vorlage vorlage.png] [--json]

<sonne.png> ist die Sonnenmaske aus szenenbild.py (weiß = Sonnenlicht). Liegen daneben `quellen.png` (Leuchtflächen: Fenster,
Sonne, Flur) und `vorlage.png` (das Blender-Komposit), werden sie ohne weitere Angabe mitgelesen. Das gemalte Bild wird auf die
Maske gebracht (Seitenverhältnis: Mitte beschneiden) und auf 640 px Breite verkleinert.

„Helle Flächen" eines Bildes sind die lokal hellen Stellen: Helligkeit minus ihr großräumiger Mittelwert (Hochpass, σ = 4 % der
Breite), in Einheiten der Streuung. So zählen Sonnenstreifen und Lichtflecken, nicht helle Wände als solche. Tuschelinien und
Kanten (Fensterrahmen, Papier) stecken in beiden Bildern; wo die Vorlage vorliegt, zählt als **Fremdlicht** nur, was das gemalte
Bild heller macht als die Vorlage an derselben Stelle — großflächig (Öffnung 9 px), außerhalb der Lichtzone (Sonnenmaske ±6 %
der Breite, Lampenmaske ebenso) und nicht auf einer Leuchtfläche. Genau das waren die Fehler des Referenzbilds aus dem
Generator: Jalousiestreifen auf einer Wand, auf die keine Sonne fällt.

Gemessen wird
  kontrast      helle Flächen in der Sonnenmaske minus daneben in der Zone (Streuungseinheiten): > 0,3 — die Sonnenflächen sind
                im Bild heller als ihre Umgebung, das Licht liegt, wo Blender es hat (zum Vergleich: derselbe Wert der Vorlage)
  korrelation   Pearson-r zwischen Sonnenmaske (leicht weich) und hellen Flächen in der Lichtzone — Form der Flecken
  versatz       Verschiebung (px, Anteil der Breite) der besten Deckung (Kreuzkorrelation in der Zone): klein = die Streifen
                liegen an derselben Stelle, groß = das Licht wurde verschoben
  richtung      Hauptrichtung der Kanten (Strukturtensor) der Blender-Streifen gegen die der gemalten hellen Flächen in der Zone
  fremdlicht    Anteil des Bildes (‰), der großflächig heller ist als die Vorlage, außerhalb aller Lichtzonen und Leuchtflächen
  lampe         Kontrast in der Lampenmaske gegen ihre Umgebung (wenn --lampe)

Urteil: RICHTIG = Kontrast > 0,3, Versatz < 3 %, Richtung < 20°, Fremdlicht < 15 ‰; TEILWEISE = drei davon; sonst FALSCH.
Die Korrelation ist nur Auskunft (bei dünnen Masken — Fensterbank, Wagenoberseite — bleibt sie auch für die Vorlage klein). Schreibt ein Vergleichsbild: Bild | Blender-Masken (Sonne gelb, Lampe orange, Leuchtflächen
blau) | Überlagerung (Maskenkanten magenta, gemalte helle Flächen grün, Fremdlicht rot) | helle Flächen.
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


def oeffnen(m, k):
    b = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    return (np.asarray(b) > 127)


def einpassen(bild, groesse):
    """Bild auf das Seitenverhältnis der Maske beschneiden (Mitte), dann skalieren."""
    w, h = bild.size; zw, zh = groesse; r = zw / zh
    if w / h > r: nw = int(h * r); bild = bild.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < r: nh = int(w / r); bild = bild.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return bild.resize(groesse, Image.LANCZOS)


def helle_flaechen(rgb, zw):
    L = luma(rgb); hp = L - weich_f(L, 0.04 * zw)
    return hp / (hp.std() + 1e-6)


def pearson(a, b, m=None):
    if m is not None: a, b = a[m], b[m]
    if a.size < 50: return 0.0
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
    return int(ix - maxv), int(iy - maxv)


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


def lade_maske(pfad, groesse):
    return np.asarray(Image.open(pfad).convert("L").resize(groesse, Image.LANCZOS)).astype(np.float32) / 255


def pruefen(ergebnis, sonne, lampe=None, quellen=None, vorlage=None):
    maske_img = Image.open(sonne).convert("L")
    zw = BREITE; zh = int(round(maske_img.height * zw / maske_img.width)); groesse = (zw, zh)
    maske = lade_maske(sonne, groesse)
    rgb = np.asarray(einpassen(Image.open(ergebnis).convert("RGB"), groesse)).astype(np.float32) / 255
    hp = helle_flaechen(rgb, zw)
    hp_vor = helle_flaechen(np.asarray(einpassen(Image.open(vorlage).convert("RGB"), groesse)).astype(np.float32) / 255, zw) if vorlage else None
    mw = weich(maske, 2.0)
    innen = maske > 0.5
    zone = dilatiere(innen.astype(np.float32), 0.06 * zw) > 0.5
    aussen = zone & ~innen
    kontrast = float(hp[innen].mean() - hp[aussen].mean()) if innen.sum() > 50 and aussen.sum() > 50 else 0.0
    kontrast_vor = float(hp_vor[innen].mean() - hp_vor[aussen].mean()) if hp_vor is not None and innen.sum() > 50 and aussen.sum() > 50 else None
    glatt = weich_f(np.clip(hp, 0, None), 0.01 * zw)             # helle Flächen ohne Linien- und Kantenrauschen
    r_zone = pearson(weich(maske, 0.01 * zw), glatt, zone)
    hz = np.where(zone, glatt, 0.0)
    dx, dy = versatz(weich(maske, 0.01 * zw), hz, int(0.08 * zw))
    wb, _ = richtung(mw, zone.astype(np.float32)); wg, _ = richtung(np.clip(hp, 0, None) / 3, zone.astype(np.float32))
    dw = winkel_diff(wb, wg)
    # Fremdlicht: großflächig hell (und heller als die Vorlage), außerhalb der Lichtzonen und Leuchtflächen
    lichtzonen = zone.copy()
    lampe_m = lade_maske(lampe, groesse) if lampe else None
    if lampe_m is not None: lichtzonen |= dilatiere((lampe_m > 0.3).astype(np.float32), 0.06 * zw) > 0.5
    if quellen: lichtzonen |= dilatiere((lade_maske(quellen, groesse) > 0.5).astype(np.float32), 0.01 * zw) > 0.5
    hell = oeffnen((hp > 1.0).astype(np.float32), 9)
    neu = hell & (hp - hp_vor > 0.8) if hp_vor is not None else hell
    fremd_m = neu & ~lichtzonen
    fremd = float(fremd_m.mean() * 1000)
    aus = dict(kontrast=round(kontrast, 2), kontrast_vorlage=(round(kontrast_vor, 2) if kontrast_vor is not None else None),
               korrelation_zone=round(r_zone, 3), versatz_px=[dx, dy], versatz_anteil=round(math.hypot(dx, dy) / zw, 3),
               richtung_blender=round(wb, 1), richtung_bild=round(wg, 1), richtung_diff=round(dw, 1),
               fremdlicht_promille=round(fremd, 1), maske_anteil=round(float(innen.mean()), 3))
    if lampe_m is not None:
        li = lampe_m > 0.3; lz = dilatiere(li.astype(np.float32), 0.06 * zw) > 0.5; la = lz & ~li
        aus["lampe_kontrast"] = round(float(hp[li].mean() - hp[la].mean()), 2) if li.sum() > 50 and la.sum() > 50 else None
    punkte = [kontrast > 0.3, aus["versatz_anteil"] < 0.03, dw < 20, fremd < 15]     # die Korrelation ist nur Auskunft:
    aus["punkte"] = int(sum(punkte))                                                   # bei dünnen Masken bleibt sie klein
    aus["urteil"] = "RICHTIG" if all(punkte) else ("TEILWEISE" if sum(punkte) >= 3 else "FALSCH")
    return aus, dict(rgb=rgb, maske=maske, hp=hp, zone=zone, hell=hell, fremd=fremd_m, lampe=lampe_m,
                     quellen=(lade_maske(quellen, groesse) if quellen else None))


def vergleichsbild(aus, d, pfad):
    rgb, maske, hp, zone, hell, fremd = d["rgb"], d["maske"], d["hp"], d["zone"], d["hell"], d["fremd"]
    h, w = maske.shape
    m_img = np.full((h, w, 3), 0.35, np.float32); m_img[zone] = 0.45
    if d["quellen"] is not None:
        q = d["quellen"][..., None]; m_img = m_img * (1 - q * 0.8) + np.array([0.45, 0.6, 0.85]) * q * 0.8
    if d["lampe"] is not None:
        l = d["lampe"][..., None]; m_img = m_img * (1 - l) + np.array([1.0, 0.6, 0.25]) * l
    m_img = m_img * (1 - maske[..., None]) + np.array([1.0, 0.93, 0.6]) * maske[..., None]
    kante = np.asarray(Image.fromarray((maske * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES)).astype(np.float32) / 255
    kante = dilatiere((kante > 0.2).astype(np.float32), 1)
    ueber = rgb * 0.75 + 0.1
    ueber = ueber * (1 - hell[..., None] * 0.5) + np.array([0.2, 0.9, 0.3]) * hell[..., None] * 0.5
    ueber = ueber * (1 - fremd[..., None] * 0.7) + np.array([0.95, 0.15, 0.1]) * fremd[..., None] * 0.7
    ueber = ueber * (1 - kante[..., None]) + np.array([0.85, 0.1, 0.55]) * kante[..., None]
    hp_img = np.repeat(np.clip(hp / 3 + 0.5, 0, 1)[..., None], 3, -1)
    teile = [rgb, m_img, ueber, hp_img]
    out = Image.new("RGB", (w * 2 + 10, h * 2 + 10 + 48), (255, 255, 255))
    for i, t in enumerate(teile):
        out.paste(Image.fromarray((np.clip(t, 0, 1) * 255 + 0.5).astype(np.uint8)), ((i % 2) * (w + 10), (i // 2) * (h + 10)))
    z = ImageDraw.Draw(out)
    kv = f" (Vorlage {aus['kontrast_vorlage']:.2f})" if aus.get("kontrast_vorlage") is not None else ""
    text = (f"{aus['urteil']} ({aus['punkte']}/4)  Kontrast {aus['kontrast']:.2f}{kv}  Korrelation Zone {aus['korrelation_zone']:.2f}  "
            f"Versatz {aus['versatz_px']} px ({aus['versatz_anteil'] * 100:.1f} %)  Richtung {aus['richtung_blender']:.0f}°/{aus['richtung_bild']:.0f}° "
            f"(Diff {aus['richtung_diff']:.0f}°)  Fremdlicht {aus['fremdlicht_promille']:.1f} ‰"
            + (f"  Lampe {aus['lampe_kontrast']:.2f}" if aus.get("lampe_kontrast") is not None else ""))
    z.text((8, h * 2 + 16), text, fill=(30, 42, 48))
    z.text((8, h * 2 + 32), "oben: Bild | Blender-Masken (Sonne gelb, Lampe orange, Leuchtflächen blau, Zone grau)   unten: Maskenkanten magenta, helle Flächen grün, Fremdlicht rot | helle Flächen (Hochpass)", fill=(90, 90, 90))
    out.save(pfad); print("Vergleichsbild", pfad)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--") and (sys.argv[sys.argv.index(a) - 1] not in ("--aus", "--lampe", "--quellen", "--vorlage"))]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    ergebnis, sonne = args[0], args[1]
    opt = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
    aus_pfad = opt("--aus") or os.path.splitext(ergebnis)[0] + "_licht.png"
    daneben = lambda n: (p := os.path.join(os.path.dirname(os.path.abspath(sonne)), n)) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(sonne)), n)) else None
    lampe = opt("--lampe") or daneben("lampe.png"); quellen = opt("--quellen") or daneben("quellen.png"); vorlage = opt("--vorlage") or daneben("vorlage.png")
    aus, d = pruefen(ergebnis, sonne, lampe, quellen, vorlage)
    vergleichsbild(aus, d, aus_pfad)
    if "--json" in sys.argv:
        print(json.dumps(aus, ensure_ascii=False))
    else:
        print(f"Urteil: {aus['urteil']} ({aus['punkte']}/4 Kriterien)")
        print(f"  Kontrast (in der Sonnenmaske heller als daneben): {aus['kontrast']:.2f}" + (f" — Vorlage {aus['kontrast_vorlage']:.2f}" if aus.get("kontrast_vorlage") is not None else ""))
        print(f"  Korrelation Maske~helle Flächen in der Zone: {aus['korrelation_zone']:.2f}")
        print(f"  Versatz der besten Deckung: {aus['versatz_px']} px = {aus['versatz_anteil'] * 100:.1f} % der Breite")
        print(f"  Streifenrichtung: Blender {aus['richtung_blender']:.0f}°, Bild {aus['richtung_bild']:.0f}°, Unterschied {aus['richtung_diff']:.0f}°")
        print(f"  Fremdlicht (großflächig heller als die Vorlage, außerhalb der Lichtzonen): {aus['fremdlicht_promille']:.1f} ‰ des Bildes")
        if aus.get("lampe_kontrast") is not None:
            print(f"  Lampeninsel: Kontrast gegen ihre Umgebung {aus['lampe_kontrast']:.2f}")


if __name__ == "__main__":
    main()
