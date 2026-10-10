# -*- coding: utf-8 -*-
"""Bildebenen für „Nachtdienst" — gezeichnet, nicht generiert.

Jede Szene besteht aus vier SVG-Ebenen (Hintergrund, Mittelgrund, Figuren,
Vordergrund). Die Geometrie wird gerechnet, nie geschätzt; deshalb sitzen
Licht, Schatten und Perspektive überall gleich.

Regeln aus docs/ART_BIBLE.md, hier als Code:
* vier Druckfarben, Tinte immer mit Deckkraft über Papier (Riso-Logik),
* drei Helligkeitszonen: dunkler Vordergrundrahmen → mittlerer Raum → Lichtinsel,
* die Lichtquelle ist im Bild sichtbar,
* genau ein Magenta-Objekt pro Bild: das, was die Geschichte weitertreibt,
* Phosphorgrün nur auf Bildschirmen,
* kein Text im Bild, keine gemalten EKG-Kurven.
"""
import json
import math
import os

B, H = 1600, 900                      # Bühnenmaß aller Ebenen

PAPIER    = "#F4E6D2"
TINTE     = "#10212B"
MAGENTA   = "#C2185B"
PHOSPHOR  = "#39E58C"
BERNSTEIN = "#E8A33D"
LINIE     = "#1E2A30"   # Tuschelinie der ligne-claire-Szenen (docs/ART_BIBLE.md)


# --------------------------------------------------------------- Werkzeug
def F(x):
    return f"{x:.1f}"


def pts(folge):
    return " ".join(f"{F(x)},{F(y)}" for x, y in folge)


def tinte(op):
    """Tinte in Deckkraft — so entstehen beim Risodruck die Zwischentöne."""
    return f'fill="{TINTE}" fill-opacity="{op:.3f}"'


def strich(op=0.92, breite=2.6, kappe="round"):
    return (f'fill="none" stroke="{TINTE}" stroke-opacity="{op:.2f}" '
            f'stroke-width="{breite}" stroke-linejoin="round" stroke-linecap="{kappe}"')


def rechteck(x, y, b, h, op, r=0):
    return f'<rect x="{F(x)}" y="{F(y)}" width="{F(b)}" height="{F(h)}" rx="{F(r)}" {tinte(op)}/>'


def farbfeld(x, y, b, h, farbe, op, r=0):
    return (f'<rect x="{F(x)}" y="{F(y)}" width="{F(b)}" height="{F(h)}" rx="{F(r)}" '
            f'fill="{farbe}" fill-opacity="{op:.3f}"/>')


def polygon(folge, op):
    return f'<polygon points="{pts(folge)}" {tinte(op)}/>'


def farbpolygon(folge, farbe, op, filter_=None):
    f = f' filter="url(#{filter_})"' if filter_ else ""
    return (f'<polygon points="{pts(folge)}" fill="{farbe}" fill-opacity="{op:.3f}"{f}/>')


def kreis(cx, cy, r, op):
    return f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{F(r)}" {tinte(op)}/>'


def bogen(x0, y0, x1, y1, hoehe, op=0.92, breite=2.6):
    """Leicht gekrümmte Linie — gegen den Lineal-Look."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - hoehe
    return (f'<path d="M{F(x0)},{F(y0)} Q{F(mx)},{F(my)} {F(x1)},{F(y1)}" '
            f'fill="none" stroke="{TINTE}" stroke-opacity="{op:.2f}" stroke-width="{breite}" '
            f'stroke-linecap="round"/>')


# --------------------------------------------------------------- Druckvorlage
def defs():
    """Filter und Muster: Papierkorn, Tintenzittern, Rasterpunkte, Weichzeichner."""
    return f"""<defs>
  <filter id="korn" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="4" stitchTiles="stitch" result="r"/>
    <feColorMatrix in="r" type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.42" intercept="0"/></feComponentTransfer>
  </filter>
  <filter id="zittern" x="-4%" y="-4%" width="108%" height="108%">
    <feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="2" seed="7" result="w"/>
    <feDisplacementMap in="SourceGraphic" in2="w" scale="3.4" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="zittern_fein" x="-4%" y="-4%" width="108%" height="108%">
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="19" result="w"/>
    <feDisplacementMap in="SourceGraphic" in2="w" scale="1.9" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="weich"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="weich_stark"><feGaussianBlur stdDeviation="30"/></filter>
  <filter id="weich_leicht"><feGaussianBlur stdDeviation="5"/></filter>
  <pattern id="raster" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <circle cx="3.5" cy="3.5" r="1.45" fill="{TINTE}"/>
  </pattern>
  <pattern id="raster_fein" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <circle cx="2.5" cy="2.5" r="0.8" fill="{TINTE}"/>
  </pattern>
  <radialGradient id="vignette" cx="52%" cy="46%" r="72%">
    <stop offset="55%" stop-color="{TINTE}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{TINTE}" stop-opacity="0.62"/>
  </radialGradient>
  <linearGradient id="glanz" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{PAPIER}" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="{PAPIER}" stop-opacity="0"/>
  </linearGradient>
</defs>"""


def ebene(inhalt, versatz=(0, 0), filter_=None, klasse=""):
    """Eine Druckplatte: minimaler Versatz wie beim Risodruck, optional Tintenzittern."""
    f = f' filter="url(#{filter_})"' if filter_ else ""
    dx, dy = versatz
    return (f'<svg viewBox="0 0 {B} {H}" class="ebene {klasse}" preserveAspectRatio="xMidYMid slice" '
            f'xmlns="http://www.w3.org/2000/svg">{defs()}'
            f'<g transform="translate({F(dx)},{F(dy)})"{f}>{inhalt}</g></svg>')


def korn(op=0.30):
    return (f'<rect x="-20" y="-20" width="{B+40}" height="{H+40}" filter="url(#korn)" '
            f'opacity="{op}" style="mix-blend-mode:multiply"/>')


def rasterflaeche(folge, op=0.5, fein=False):
    m = "raster_fein" if fein else "raster"
    return f'<polygon points="{pts(folge)}" fill="url(#{m})" opacity="{op:.2f}"/>'


# ============================================================ Bausteine
def jalousie(x, y, b, h, licht=0.9, schlitz=22):
    """Fenster mit Lamellen. Die Lamellen stehen halb offen, dazwischen das Licht."""
    s = [farbfeld(x - 6, y - 6, b + 12, h + 12, BERNSTEIN, 0.55 * licht),
         farbfeld(x - 26, y - 26, b + 52, h + 52, BERNSTEIN, 0.30 * licht, r=6)]
    s.append(f'<g filter="url(#weich)">{farbfeld(x - 40, y - 40, b + 80, h + 80, BERNSTEIN, 0.4 * licht)}</g>')
    n = int(h / schlitz)
    for i in range(n + 1):
        yy = y + i * schlitz
        s.append(polygon([(x, yy), (x + b, yy - 3), (x + b, yy + schlitz * 0.62), (x, yy + schlitz * 0.62 + 3)], 0.74))
        s.append(farbpolygon([(x, yy + schlitz * 0.62 + 3), (x + b, yy + schlitz * 0.62),
                              (x + b, yy + schlitz - 1), (x, yy + schlitz + 2)], BERNSTEIN, 0.85 * licht))
    s.append(f'<rect x="{F(x)}" y="{F(y)}" width="{F(b)}" height="{F(h)}" {strich(0.85, 4)}/>')
    s.append(rechteck(x + b / 2 - 3, y, 6, h, 0.6))
    return "".join(s)


def lichtschacht(x0, y0, x1, y1, laenge, neigung, op, farbe=BERNSTEIN, weich="weich"):
    """Lichtkeil aus einem Fensterspalt — Richtung in Grad, Länge in px."""
    a = math.radians(neigung)
    dx, dy = math.cos(a) * laenge, math.sin(a) * laenge
    spreizung = laenge * 0.17
    folge = [(x0, y0), (x1, y1), (x1 + dx, y1 + dy + spreizung), (x0 + dx, y0 + dy - spreizung * 0.3)]
    return farbpolygon(folge, farbe, op, filter_=weich)


def stuhl(x, bodeny, breite=130, sitzhoehe=52):
    """Wartestuhl, Dreiviertelansicht von vorn-links.

    Aufbau wie beim echten Stuhl: vier Beine, Sitzplatte mit Dicke, Luft
    zwischen Sitz und Lehne, Lehne leicht nach hinten geneigt. Die Tiefe
    entsteht durch den Versatz (tx, ty) zwischen Vorder- und Hinterkante.
    """
    tx, ty = breite * 0.22, breite * 0.13          # Fluchtversatz nach hinten
    sy = bodeny - sitzhoehe
    s = []
    # Hinterbeine zuerst (liegen hinten)
    for bx in (x + tx + 10, x + tx + breite - 16):
        s.append(rechteck(bx, sy - ty, 6, bodeny - sy + ty - 2, 0.62))
    # Lehne: oben etwas breiter, nach hinten geneigt
    lh = sitzhoehe * 1.35
    s.append(f'<path d="M{F(x + tx + 8)},{F(sy - ty - 18)} '
             f'L{F(x + tx + breite - 8)},{F(sy - ty - 18)} '
             f'L{F(x + tx + breite - 2)},{F(sy - ty - 18 - lh)} '
             f'Q{F(x + tx + breite / 2)},{F(sy - ty - 26 - lh)} {F(x + tx + 2)},{F(sy - ty - 18 - lh)} Z" '
             f'{tinte(0.74)}/>')
    s.append(f'<path d="M{F(x + tx + 2)},{F(sy - ty - 18 - lh)} '
             f'Q{F(x + tx + breite / 2)},{F(sy - ty - 26 - lh)} {F(x + tx + breite - 2)},{F(sy - ty - 18 - lh)}" '
             f'{strich(0.5, 3)}/>')
    # Sitzplatte: Oberseite hell, Kante dunkel
    oben = [(x, sy), (x + breite, sy), (x + breite + tx, sy - ty), (x + tx, sy - ty)]
    s.append(polygon(oben, 0.42))
    s.append(f'<path d="M{F(x)},{F(sy)} L{F(x + breite)},{F(sy)} L{F(x + breite + tx)},{F(sy - ty)} '
             f'L{F(x + tx)},{F(sy - ty)} Z" {strich(0.6, 2.2)}/>')
    s.append(polygon([(x, sy), (x + breite, sy), (x + breite, sy + 10), (x, sy + 10)], 0.78))
    s.append(polygon([(x + breite, sy), (x + breite + tx, sy - ty), (x + breite + tx, sy - ty + 10),
                      (x + breite, sy + 10)], 0.66))
    # Vorderbeine
    for bx in (x + 8, x + breite - 14):
        s.append(rechteck(bx, sy + 8, 7, bodeny - sy - 8, 0.88))
    s.append(rechteck(x + 10, bodeny - 16, breite - 20, 5, 0.6))        # Querstrebe
    return "".join(s)


def ekg_wagen(x, bodeny, h=240):
    """Rollwagen mit Monitor. Der Bildschirm bleibt leer — Kurven zeichnet die Engine."""
    b = 148
    oben = bodeny - h
    s = [polygon([(x + 10, bodeny - 26), (x + b - 2, bodeny - 30), (x + b + 8, bodeny - 6), (x + 2, bodeny)], 0.84),
         rechteck(x + 16, oben + 96, 12, bodeny - oben - 120, 0.9),
         rechteck(x + b - 34, oben + 96, 12, bodeny - oben - 120, 0.9),
         polygon([(x + 4, oben + 86), (x + b - 4, oben + 80), (x + b + 4, oben + 104), (x - 2, oben + 110)], 0.86)]
    s.append(rechteck(x + 2, oben, b, 92, 0.95, r=8))                                   # Monitorgehäuse
    s.append(farbfeld(x + 12, oben + 10, b - 20, 62, PHOSPHOR, 0.16, r=3))              # Schirm
    s.append(f'<g filter="url(#weich_leicht)">{farbfeld(x + 12, oben + 10, b - 20, 62, PHOSPHOR, 0.22, r=3)}</g>')
    s.append(f'<rect x="{F(x + 12)}" y="{F(oben + 10)}" width="{F(b - 20)}" height="62" rx="3" '
             f'fill="none" stroke="{PHOSPHOR}" stroke-opacity="0.45" stroke-width="1.6"/>')
    for i, cx in enumerate((x + 24, x + 46, x + 68)):                                    # Knöpfe
        s.append(kreis(cx, oben + 82, 4.5, 0.65))
    for cx in (x + 24, x + b - 18):                                                      # Räder
        s.append(kreis(cx, bodeny - 2, 11, 0.9))
        s.append(kreis(cx, bodeny - 2, 4, 0.35))
    s.append(bogen(x + b - 12, oben + 62, x + b + 30, oben + 128, -16, 0.6, 3.2))        # Kabel am Haken
    s.append(bogen(x + b + 30, oben + 128, x + b - 6, oben + 170, 14, 0.6, 3.2))
    return "".join(s)


def tresen(x, y, b, h):
    """Aufnahmetresen: Front im Schatten, Platte im Licht."""
    s = [polygon([(x, y), (x + b, y - 10), (x + b + 26, y + 26), (x + 22, y + 38)], 0.30),   # Platte
         rasterflaeche([(x, y), (x + b, y - 10), (x + b + 26, y + 26), (x + 22, y + 38)], 0.18, fein=True),
         polygon([(x + 22, y + 34), (x + b + 26, y + 22), (x + b + 26, y + h), (x + 22, y + h)], 0.62),
         rasterflaeche([(x + 22, y + 60), (x + b + 26, y + 48), (x + b + 26, y + h), (x + 22, y + h)], 0.35)]
    s.append(f'<path d="M{F(x)},{F(y)} L{F(x + b)},{F(y - 10)} L{F(x + b + 26)},{F(y + 26)} '
             f'L{F(x + 22)},{F(y + 38)} Z" {strich(0.85, 3)}/>')
    s.append(rechteck(x + 60, y + 2, 86, 10, 0.5, r=2))                                      # Aktenstapel
    s.append(rechteck(x + 56, y - 6, 92, 10, 0.42, r=2))
    s.append(rechteck(x + 64, y - 14, 80, 9, 0.34, r=2))
    return "".join(s)


def tischlampe(x, y, arm=74):
    """Zweite sichtbare Lichtquelle: Schreibtischlampe mit warmem Kegel."""
    s = [f'<g filter="url(#weich)">{farbfeld(x - 70, y - 20, 210, 200, BERNSTEIN, 0.34)}</g>',
         rechteck(x - 18, y + 96, 44, 8, 0.9, r=3),
         bogen(x + 2, y + 96, x + arm * 0.7, y + 10, 30, 0.9, 5),
         polygon([(x + arm * 0.52, y + 6), (x + arm * 1.26, y - 6), (x + arm * 1.42, y + 34), (x + arm * 0.46, y + 40)], 0.92)]
    s.append(farbpolygon([(x + arm * 0.50, y + 38), (x + arm * 1.42, y + 32),
                          (x + arm * 1.9, y + 180), (x + arm * 0.05, y + 196)], BERNSTEIN, 0.30, filter_="weich"))
    s.append(f'<circle cx="{F(x + arm * 0.95)}" cy="{F(y + 34)}" r="9" fill="{BERNSTEIN}" fill-opacity="0.95"/>')
    return "".join(s)


def wanduhr(cx, cy, r=56):
    """Zifferblatt ohne Zahlen. Die Zeiger setzt die Engine (#uhr-std, #uhr-min)."""
    s = [kreis(cx, cy, r + 5, 0.92), f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{F(r)}" fill="{PAPIER}" fill-opacity="0.93"/>']
    for i in range(12):
        a = math.radians(i * 30 - 90)
        r1 = r - (13 if i % 3 == 0 else 7)
        s.append(f'<line x1="{F(cx + math.cos(a) * r1)}" y1="{F(cy + math.sin(a) * r1)}" '
                 f'x2="{F(cx + math.cos(a) * (r - 3))}" y2="{F(cy + math.sin(a) * (r - 3))}" '
                 f'stroke="{TINTE}" stroke-opacity="{0.85 if i % 3 == 0 else 0.5}" '
                 f'stroke-width="{4 if i % 3 == 0 else 2.2}" stroke-linecap="round"/>')
    s.append(f'<line id="uhr-std" x1="{F(cx)}" y1="{F(cy)}" x2="{F(cx)}" y2="{F(cy - r * 0.52)}" '
             f'stroke="{TINTE}" stroke-width="6" stroke-linecap="round" '
             f'transform="rotate(0 {F(cx)} {F(cy)})"/>')
    s.append(f'<line id="uhr-min" x1="{F(cx)}" y1="{F(cy)}" x2="{F(cx)}" y2="{F(cy - r * 0.78)}" '
             f'stroke="{TINTE}" stroke-width="3.4" stroke-linecap="round" '
             f'transform="rotate(0 {F(cx)} {F(cy)})"/>')
    s.append(kreis(cx, cy, 5, 0.95))
    return "".join(s)


def pinnwand(x, y, b, h, neigung=-1.2):
    """Korkwand mit angehefteten Zetteln — Formen, keine Schrift."""
    s = [rechteck(x - 6, y - 6, b + 12, h + 12, 0.86, r=4),
         farbfeld(x, y, b, h, BERNSTEIN, 0.22),
         rasterflaeche([(x, y), (x + b, y), (x + b, y + h), (x, y + h)], 0.22, fein=True)]
    zettel = [(18, 16, 84, 60, -3), (122, 24, 70, 50, 2.5), (30, 92, 96, 54, 1.5),
              (150, 86, 62, 62, -2), (210, 20, 58, 104, 1)]
    for zx, zy, zb, zh, zr in zettel:
        if zx + zb > b - 8:
            continue
        s.append(f'<g transform="rotate({zr} {F(x + zx + zb / 2)} {F(y + zy + zh / 2)})">'
                 f'{farbfeld(x + zx, y + zy, zb, zh, PAPIER, 0.9)}'
                 f'<rect x="{F(x + zx)}" y="{F(y + zy)}" width="{F(zb)}" height="{F(zh)}" {strich(0.5, 1.8)}/>'
                 f'{rechteck(x + zx + 8, y + zy + 12, zb - 20, 3, 0.3)}'
                 f'{rechteck(x + zx + 8, y + zy + 22, zb - 28, 3, 0.26)}'
                 f'{rechteck(x + zx + 8, y + zy + 32, zb - 16, 3, 0.26)}'
                 f'{kreis(x + zx + zb / 2, y + zy + 5, 4, 0.75)}</g>')
    return f'<g transform="rotate({neigung} {F(x + b / 2)} {F(y + h / 2)})">' + "".join(s) + "</g>"


def tuerrahmen_links(breite=168):
    """Vordergrundrahmen links: Türpfosten plus Sturz. Nahezu schwarz."""
    s = [polygon([(0, 0), (breite, 0), (breite - 26, H), (0, H)], 0.93),
         polygon([(0, 0), (B, 0), (B, 54), (0, 72)], 0.9),
         polygon([(breite - 26, 0), (breite + 10, 0), (breite - 16, H), (breite - 48, H)], 0.45)]
    return "".join(s)


def infusionsstaender(x, bodeny):
    s = [rechteck(x, bodeny - 430, 9, 430, 0.93),
         bogen(x + 4, bodeny - 430, x + 44, bodeny - 418, 14, 0.93, 8),
         polygon([(x + 30, bodeny - 412), (x + 70, bodeny - 416), (x + 62, bodeny - 300), (x + 38, bodeny - 298)], 0.9),
         bogen(x + 50, bodeny - 300, x + 20, bodeny - 150, -26, 0.8, 4)]
    for a in (-32, 0, 32):
        ar = math.radians(a + 90)
        s.append(f'<line x1="{F(x + 4)}" y1="{F(bodeny - 6)}" x2="{F(x + 4 + math.cos(ar) * 0)}" y2="{F(bodeny)}" '
                 f'stroke="{TINTE}" stroke-width="6"/>')
    s.append(polygon([(x - 54, bodeny + 4), (x + 62, bodeny + 4), (x + 50, bodeny + 16), (x - 42, bodeny + 16)], 0.9))
    return "".join(s)


# ============================================================ Figuren

def mit_rand(pfad_d, op, licht=(-5, -4), randfarbe=BERNSTEIN, randop=0.8, extra=""):
    """Eine Masse mit Lichtkante: dieselbe Form zuerst in Licht, zur Lampe hin
    versetzt, dann die Tinte darüber. Übrig bleibt ein Saum auf der Lichtseite —
    der Unterschied zwischen einer Silhouette und einem Körper."""
    dx, dy = licht
    return (f'<path d="{pfad_d}" fill="{randfarbe}" fill-opacity="{randop:.2f}" '
            f'transform="translate({F(dx)},{F(dy)})"{extra}/>'
            f'<path d="{pfad_d}" {tinte(op)}{extra}/>')


def falte(x0, y0, x1, y1, bauch, op=0.42, breite=2.6):
    """Stofffalte: eine kurze, leicht gebogene Linie, heller als die Tinte."""
    mx, my = (x0 + x1) / 2 + bauch, (y0 + y1) / 2
    return (f'<path d="M{F(x0)},{F(y0)} Q{F(mx)},{F(my)} {F(x1)},{F(y1)}" fill="none" '
            f'stroke="{PAPIER}" stroke-opacity="{op:.2f}" stroke-width="{F(breite)}" stroke-linecap="round"/>')


def hand(x, y, r, richtung=1, op=0.9):
    """Eine Hand, keine Kugel: Handrücken plus angedeutete Finger."""
    d = (f'M{F(x)},{F(y - r)} '
         f'C{F(x + r * 1.15 * richtung)},{F(y - r * 0.9)} {F(x + r * 1.3 * richtung)},{F(y + r * 0.5)} '
         f'{F(x + r * 0.7 * richtung)},{F(y + r)} '
         f'C{F(x + r * 0.2 * richtung)},{F(y + r * 1.25)} {F(x - r * 0.5 * richtung)},{F(y + r * 0.8)} '
         f'{F(x - r * 0.55 * richtung)},{F(y)} Z')
    s = [f'<path d="{d}" {tinte(op)}/>']
    for i in range(3):
        fy = y - r * 0.35 + i * r * 0.5
        s.append(f'<path d="M{F(x + r * 0.25 * richtung)},{F(fy)} L{F(x + r * 0.95 * richtung)},{F(fy + r * 0.12)}" '
                 f'fill="none" stroke="{PAPIER}" stroke-opacity="0.22" stroke-width="{F(r * 0.14)}" '
                 f'stroke-linecap="round"/>')
    return "".join(s)


def thermoskanne(x, fussy, hoehe=64, magenta=True):
    """Verbeulte Thermoskanne. Steht auf dem Tresen oder wird gehalten."""
    f_ = MAGENTA if magenta else TINTE
    op = 0.95 if magenta else 0.88
    b = hoehe * 0.47
    return (f'<rect x="{F(x)}" y="{F(fussy - hoehe)}" width="{F(b)}" height="{F(hoehe)}" rx="{F(b * 0.17)}" '
            f'fill="{f_}" fill-opacity="{op}"/>'
            f'<rect x="{F(x - b * 0.07)}" y="{F(fussy - hoehe - b * 0.22)}" width="{F(b * 1.14)}" '
            f'height="{F(b * 0.26)}" rx="{F(b * 0.09)}" fill="{f_}" fill-opacity="{op}"/>'
            f'<rect x="{F(x + b * 0.16)}" y="{F(fussy - hoehe * 0.74)}" width="{F(b * 0.64)}" '
            f'height="{F(hoehe * 0.09)}" fill="{PAPIER}" fill-opacity="0.45"/>'
            f'<path d="M{F(x + b)},{F(fussy - hoehe * 0.72)} q{F(b * 0.52)},{F(hoehe * 0.16)} 0,{F(hoehe * 0.33)}" '
            f'fill="none" stroke="{f_}" stroke-opacity="{op}" stroke-width="{F(b * 0.16)}"/>'
            f'<ellipse cx="{F(x + b / 2)}" cy="{F(fussy)}" rx="{F(b * 0.62)}" ry="{F(b * 0.13)}" '
            f'{tinte(0.22)}/>')


def marlene(x, bodeny, hoehe=330, akzent_magenta=False, kanne=True):
    """Runde Formfamilie, kompakte Silhouette, schiefer Dutt, Kuli hinterm Ohr.

    Hinter dem Tresen ist sie ab der Hüfte sichtbar; `bodeny` ist die Schnittkante.
    """
    e = hoehe / 330.0                      # Maßstab
    kx, ky = x, bodeny - hoehe             # Kopfmitte oben
    s = []
    # Rumpf: breite, weiche Trapezform, mit Lichtkante von der Lampe rechts
    rumpf = (f'M{F(x - 86 * e)},{F(bodeny)} '
             f'C{F(x - 92 * e)},{F(ky + 150 * e)} {F(x - 70 * e)},{F(ky + 96 * e)} {F(x - 44 * e)},{F(ky + 84 * e)} '
             f'L{F(x + 44 * e)},{F(ky + 84 * e)} '
             f'C{F(x + 72 * e)},{F(ky + 96 * e)} {F(x + 94 * e)},{F(ky + 150 * e)} {F(x + 88 * e)},{F(bodeny)} Z')
    s.append(mit_rand(rumpf, 0.80, licht=(6 * e, -3 * e), randop=0.7))
    s.append(rasterflaeche([(x - 86 * e, bodeny), (x - 30 * e, ky + 120 * e), (x - 6 * e, bodeny)], 0.3))
    # Falten im Kasack: Schulter zur Hüfte, Bauch, Ärmelansatz
    s.append(falte(x - 48 * e, ky + 104 * e, x - 30 * e, ky + 196 * e, -7 * e, 0.22, 3 * e))
    s.append(falte(x + 36 * e, ky + 102 * e, x + 52 * e, ky + 184 * e, 6 * e, 0.3, 3 * e))
    s.append(falte(x - 14 * e, ky + 150 * e, x + 20 * e, ky + 162 * e, 0, 0.16, 3 * e))
    # Ärmel hochgekrempelt: hellerer Ring am Oberarm
    s.append(f'<path d="M{F(x - 84 * e)},{F(ky + 150 * e)} q{F(16 * e)},{F(10 * e)} {F(34 * e)},{F(4 * e)}" '
             f'{strich(0.5, 5 * e)}/>')
    # Arm links: angewinkelt, hält die Thermoskanne
    s.append(f'<path d="M{F(x - 70 * e)},{F(ky + 128 * e)} C{F(x - 104 * e)},{F(ky + 176 * e)} '
             f'{F(x - 92 * e)},{F(ky + 212 * e)} {F(x - 52 * e)},{F(ky + 216 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.84" stroke-width="{F(26 * e)}" stroke-linecap="round"/>')
    if kanne:
        s.append(thermoskanne(x - 62 * e, ky + 248 * e, 62 * e, akzent_magenta))
    # Arm rechts: auf dem Tresen abgestützt
    s.append(f'<path d="M{F(x + 66 * e)},{F(ky + 126 * e)} C{F(x + 104 * e)},{F(ky + 160 * e)} '
             f'{F(x + 116 * e)},{F(ky + 192 * e)} {F(x + 120 * e)},{F(ky + 214 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.84" stroke-width="{F(24 * e)}" stroke-linecap="round"/>')
    s.append(f'<path d="M{F(x + 76 * e)},{F(ky + 138 * e)} C{F(x + 106 * e)},{F(ky + 168 * e)} '
             f'{F(x + 114 * e)},{F(ky + 192 * e)} {F(x + 117 * e)},{F(ky + 208 * e)}" fill="none" '
             f'stroke="{BERNSTEIN}" stroke-opacity="0.5" stroke-width="{F(4 * e)}" stroke-linecap="round"/>')
    s.append(hand(x + 122 * e, ky + 226 * e, 13 * e, 1, 0.9))
    # Hals und Kopf
    s.append(rechteck(x - 13 * e, ky + 66 * e, 26 * e, 26 * e, 0.8))
    kopf = (f'M{F(kx - 33 * e)},{F(ky + 46 * e)} '
            f'C{F(kx - 33 * e)},{F(ky + 16 * e)} {F(kx - 18 * e)},{F(ky + 10 * e)} {F(kx)},{F(ky + 11 * e)} '
            f'C{F(kx + 20 * e)},{F(ky + 12 * e)} {F(kx + 33 * e)},{F(ky + 22 * e)} {F(kx + 32 * e)},{F(ky + 50 * e)} '
            f'C{F(kx + 31 * e)},{F(ky + 72 * e)} {F(kx + 18 * e)},{F(ky + 84 * e)} {F(kx + 1 * e)},{F(ky + 84 * e)} '
            f'C{F(kx - 20 * e)},{F(ky + 84 * e)} {F(kx - 33 * e)},{F(ky + 70 * e)} {F(kx - 33 * e)},{F(ky + 46 * e)} Z')
    s.append(mit_rand(kopf, 0.86, licht=(5 * e, -3 * e), randop=0.72))
    # Dutt, schief, mit Lesebrille darin
    s.append(f'<ellipse cx="{F(kx - 26 * e)}" cy="{F(ky + 6 * e)}" rx="{F(26 * e)}" ry="{F(22 * e)}" '
             f'{tinte(0.92)} transform="rotate(-18 {F(kx - 26 * e)} {F(ky + 6 * e)})"/>')
    s.append(f'<path d="M{F(kx - 31 * e)},{F(ky + 26 * e)} C{F(kx - 42 * e)},{F(ky + 10 * e)} '
             f'{F(kx - 12 * e)},{F(ky - 6 * e)} {F(kx + 20 * e)},{F(ky + 18 * e)}" {strich(0.9, 6 * e)}/>')
    for bx in (-38, -14):                                  # Brille im Dutt
        s.append(f'<circle cx="{F(kx + bx * e)}" cy="{F(ky - 2 * e)}" r="{F(9 * e)}" fill="none" '
                 f'stroke="{PAPIER}" stroke-opacity="0.8" stroke-width="{F(2.6 * e)}"/>')
    s.append(f'<line x1="{F(kx - 29 * e)}" y1="{F(ky - 2 * e)}" x2="{F(kx - 23 * e)}" y2="{F(ky - 2 * e)}" '
             f'stroke="{PAPIER}" stroke-opacity="0.8" stroke-width="{F(2.6 * e)}"/>')
    # Kuli hinterm Ohr
    s.append(f'<line x1="{F(kx + 28 * e)}" y1="{F(ky + 38 * e)}" x2="{F(kx + 40 * e)}" y2="{F(ky + 60 * e)}" '
             f'stroke="{PHOSPHOR}" stroke-opacity="0.8" stroke-width="{F(4.5 * e)}" stroke-linecap="round"/>')
    # Gesicht im Gegenlicht: schwere Lider, Nasenrücken, kurze Mundlinie, Lachfalte
    s.append(f'<path d="M{F(kx - 16 * e)},{F(ky + 44 * e)} q{F(7 * e)},{F(-5 * e)} {F(14 * e)},{F(-1 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.55" stroke-width="{F(2.6 * e)}" stroke-linecap="round"/>')
    s.append(f'<path d="M{F(kx + 6 * e)},{F(ky + 42 * e)} q{F(7 * e)},{F(-5 * e)} {F(14 * e)},{F(-1 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.5" stroke-width="{F(2.6 * e)}" stroke-linecap="round"/>')
    s.append(f'<path d="M{F(kx + 2 * e)},{F(ky + 48 * e)} l{F(5 * e)},{F(11 * e)} l{F(-6 * e)},{F(2 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.34" stroke-width="{F(2.2 * e)}" stroke-linejoin="round"/>')
    s.append(f'<path d="M{F(kx - 6 * e)},{F(ky + 68 * e)} q{F(9 * e)},{F(4 * e)} {F(17 * e)},{F(-1 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.42" stroke-width="{F(2.4 * e)}" stroke-linecap="round"/>')
    s.append(f'<path d="M{F(kx + 22 * e)},{F(ky + 56 * e)} q{F(4 * e)},{F(7 * e)} {F(1 * e)},{F(12 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.26" stroke-width="{F(2 * e)}" stroke-linecap="round"/>')
    # Namensschild mit verblasstem Katzensticker
    s.append(farbfeld(x + 20 * e, ky + 118 * e, 34 * e, 16 * e, PAPIER, 0.75, r=2))
    s.append(f'<circle cx="{F(x + 28 * e)}" cy="{F(ky + 126 * e)}" r="{F(4.5 * e)}" fill="{BERNSTEIN}" fill-opacity="0.75"/>')
    return "".join(s)


def herr_k(x, bodeny, hoehe=300, tuete_magenta=True, tuete=True):
    """Weiche Rechteck-Formfamilie, gebeugter Bogen, Schiebermütze. Sitzt."""
    e = hoehe / 300.0
    ky = bodeny - hoehe
    s = []
    # Beine: sitzend, Knie nach vorn
    s.append(f'<path d="M{F(x - 26 * e)},{F(ky + 188 * e)} L{F(x + 74 * e)},{F(ky + 196 * e)} '
             f'L{F(x + 78 * e)},{F(ky + 232 * e)} L{F(x - 24 * e)},{F(ky + 226 * e)} Z" {tinte(0.88)}/>')
    s.append(f'<path d="M{F(x + 54 * e)},{F(ky + 200 * e)} L{F(x + 78 * e)},{F(ky + 200 * e)} '
             f'L{F(x + 86 * e)},{F(bodeny - 6)} L{F(x + 56 * e)},{F(bodeny - 6)} Z" {tinte(0.9)}/>')
    s.append(f'<path d="M{F(x + 20 * e)},{F(ky + 208 * e)} L{F(x + 46 * e)},{F(ky + 206 * e)} '
             f'L{F(x + 50 * e)},{F(bodeny - 6)} L{F(x + 20 * e)},{F(bodeny - 6)} Z" {tinte(0.86)}/>')
    for fx in (x + 22, x + 56):                                     # Hausschuhe
        s.append(f'<path d="M{F(fx * 1.0 if False else fx)},{F(bodeny - 6)} h{F(34 * e)} '
                 f'q{F(8 * e)},{F(10 * e)} {F(-6 * e)},{F(12 * e)} h{F(-30 * e)} z" {tinte(0.92)}/>')
    # Rumpf: gebeugter Bogen, breiter Rücken
    ruecken = (f'M{F(x - 34 * e)},{F(ky + 196 * e)} '
               f'C{F(x - 52 * e)},{F(ky + 120 * e)} {F(x - 44 * e)},{F(ky + 70 * e)} {F(x - 10 * e)},{F(ky + 56 * e)} '
               f'L{F(x + 34 * e)},{F(ky + 60 * e)} '
               f'C{F(x + 62 * e)},{F(ky + 86 * e)} {F(x + 70 * e)},{F(ky + 150 * e)} {F(x + 72 * e)},{F(ky + 198 * e)} Z')
    s.append(mit_rand(ruecken, 0.82, licht=(7 * e, -4 * e), randop=0.85))
    s.append(falte(x + 10 * e, ky + 90 * e, x + 34 * e, ky + 160 * e, 7 * e, 0.22, 3 * e))
    s.append(falte(x - 20 * e, ky + 104 * e, x - 10 * e, ky + 180 * e, -6 * e, 0.14, 3 * e))
    # Strickjacke unterm Patientenhemd: Kante
    s.append(f'<path d="M{F(x - 6 * e)},{F(ky + 66 * e)} C{F(x + 2 * e)},{F(ky + 130 * e)} '
             f'{F(x + 6 * e)},{F(ky + 170 * e)} {F(x + 10 * e)},{F(ky + 196 * e)}" {strich(0.55, 4 * e)}/>')
    s.append(rasterflaeche([(x - 34 * e, ky + 196 * e), (x - 44 * e, ky + 90 * e), (x - 8 * e, ky + 110 * e),
                            (x - 2 * e, ky + 196 * e)], 0.34))
    # Arme: Hände auf den Knien
    s.append(f'<path d="M{F(x + 44 * e)},{F(ky + 84 * e)} C{F(x + 76 * e)},{F(ky + 130 * e)} '
             f'{F(x + 74 * e)},{F(ky + 170 * e)} {F(x + 52 * e)},{F(ky + 190 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.86" stroke-width="{F(24 * e)}" stroke-linecap="round"/>')
    s.append(f'<path d="M{F(x - 16 * e)},{F(ky + 80 * e)} C{F(x - 30 * e)},{F(ky + 130 * e)} '
             f'{F(x - 10 * e)},{F(ky + 164 * e)} {F(x + 10 * e)},{F(ky + 178 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.86" stroke-width="{F(22 * e)}" stroke-linecap="round"/>')
    s.append(hand(x + 18 * e, ky + 188 * e, 12 * e, 1, 0.9))
    s.append(hand(x + 52 * e, ky + 190 * e, 12 * e, 1, 0.9))
    # Rotes Fadenarmband der Enkelin (Bernstein-Rot, kein Magenta)
    s.append(f'<path d="M{F(x + 44 * e)},{F(ky + 176 * e)} q{F(9 * e)},{F(6 * e)} {F(17 * e)},{F(1 * e)}" '
             f'fill="none" stroke="{BERNSTEIN}" stroke-opacity="0.95" stroke-width="{F(4.5 * e)}" stroke-linecap="round"/>')
    # Kopf, nach vorn gesenkt
    s.append(mit_rand(
        f'M{F(x - 22 * e)},{F(ky + 28 * e)} C{F(x - 22 * e)},{F(ky + 2 * e)} {F(x + 2 * e)},{F(ky - 6 * e)} '
        f'{F(x + 20 * e)},{F(ky - 2 * e)} C{F(x + 40 * e)},{F(ky + 3 * e)} {F(x + 47 * e)},{F(ky + 24 * e)} '
        f'{F(x + 44 * e)},{F(ky + 44 * e)} C{F(x + 41 * e)},{F(ky + 62 * e)} {F(x + 22 * e)},{F(ky + 68 * e)} '
        f'{F(x + 4 * e)},{F(ky + 64 * e)} C{F(x - 14 * e)},{F(ky + 60 * e)} {F(x - 22 * e)},{F(ky + 46 * e)} '
        f'{F(x - 22 * e)},{F(ky + 28 * e)} Z', 0.86, licht=(6 * e, -3 * e), randop=0.8))
    # Schiebermütze
    s.append(f'<path d="M{F(x - 22 * e)},{F(ky + 18 * e)} C{F(x - 26 * e)},{F(ky - 14 * e)} '
             f'{F(x + 34 * e)},{F(ky - 20 * e)} {F(x + 46 * e)},{F(ky + 10 * e)} '
             f'L{F(x + 48 * e)},{F(ky + 22 * e)} L{F(x - 20 * e)},{F(ky + 26 * e)} Z" {tinte(0.94)}/>')
    s.append(f'<path d="M{F(x - 22 * e)},{F(ky + 22 * e)} L{F(x - 58 * e)},{F(ky + 30 * e)} '
             f'q{F(-6 * e)},{F(8 * e)} {F(6 * e)},{F(10 * e)} L{F(x - 18 * e)},{F(ky + 30 * e)} Z" {tinte(0.94)}/>')
    # Hörgerät
    s.append(f'<path d="M{F(x + 40 * e)},{F(ky + 36 * e)} q{F(8 * e)},{F(4 * e)} {F(4 * e)},{F(14 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.7" stroke-width="{F(4 * e)}" stroke-linecap="round"/>')
    # Profil: Nase und Mundlinie im Gegenlicht
    s.append(f'<path d="M{F(x + 40 * e)},{F(ky + 26 * e)} l{F(8 * e)},{F(9 * e)} l{F(-9 * e)},{F(3 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.5" stroke-width="{F(3 * e)}" stroke-linejoin="round"/>')
    s.append(f'<path d="M{F(x + 28 * e)},{F(ky + 48 * e)} q{F(8 * e)},{F(3 * e)} {F(13 * e)},{F(-2 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.42" stroke-width="{F(2.6 * e)}" stroke-linecap="round"/>')
    # Plastiktüte neben dem Fuß: durchscheinend, man sieht, was drin ist
    if not tuete:
        return "".join(s)
    tx, tby = x - 86 * e, bodeny
    huelle = (f'M{F(tx)},{F(tby - 84 * e)} C{F(tx - 13 * e)},{F(tby - 32 * e)} {F(tx - 5 * e)},{F(tby)} '
              f'{F(tx + 28 * e)},{F(tby)} C{F(tx + 62 * e)},{F(tby)} {F(tx + 67 * e)},{F(tby - 36 * e)} '
              f'{F(tx + 56 * e)},{F(tby - 84 * e)} Z')
    s.append(f'<path d="{huelle}" fill="{PAPIER}" fill-opacity="0.34"/>')
    s.append(f'<clipPath id="tuete-k"><path d="{huelle}"/></clipPath><g clip-path="url(#tuete-k)">')
    s.append(farbfeld(tx + 6 * e, tby - 58 * e, 24 * e, 34 * e, PAPIER, 0.62, r=2))        # Tablettenschachteln
    s.append(f'<rect x="{F(tx + 6 * e)}" y="{F(tby - 58 * e)}" width="{F(24 * e)}" height="{F(34 * e)}" '
             f'rx="2" {strich(0.55, 2 * e)}/>')
    s.append(farbfeld(tx + 30 * e, tby - 48 * e, 20 * e, 30 * e, PAPIER, 0.5, r=2))
    s.append(f'<rect x="{F(tx + 30 * e)}" y="{F(tby - 48 * e)}" width="{F(20 * e)}" height="{F(30 * e)}" '
             f'rx="2" {strich(0.45, 2 * e)}/>')
    s.append(rechteck(tx + 10 * e, tby - 50 * e, 16 * e, 3 * e, 0.4))
    s.append(farbfeld(tx + 14 * e, tby - 24 * e, 26 * e, 20 * e, PAPIER, 0.7, r=1))        # Foto der Enkelin
    s.append(f'<rect x="{F(tx + 14 * e)}" y="{F(tby - 24 * e)}" width="{F(26 * e)}" height="{F(20 * e)}" '
             f'{strich(0.5, 1.8 * e)}/>')
    s.append(f'<circle cx="{F(tx + 27 * e)}" cy="{F(tby - 17 * e)}" r="{F(4 * e)}" {tinte(0.5)}/>')
    s.append(f'<path d="M{F(tx + 19 * e)},{F(tby - 5 * e)} q{F(8 * e)},{F(-9 * e)} {F(16 * e)},0" {strich(0.5, 2.4 * e)}/>')
    s.append("</g>")
    s.append(f'<path d="{huelle}" {strich(0.8, 2.6 * e)}/>')
    for hx in (4, 28):                                                                      # Henkel
        s.append(f'<path d="M{F(tx + hx * e)},{F(tby - 82 * e)} q{F(11 * e)},{F(-23 * e)} {F(22 * e)},{F(-1 * e)}" '
                 f'{strich(0.8, 3.4 * e)}/>')
    s.append(f'<path d="M{F(tx + 48 * e)},{F(tby - 78 * e)} C{F(tx + 54 * e)},{F(tby - 50 * e)} '
             f'{F(tx + 52 * e)},{F(tby - 20 * e)} {F(tx + 44 * e)},{F(tby - 4 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.5" stroke-width="{F(3 * e)}"/>')   # Lichtkante
    return "".join(s)



def falk(x, bodeny, hoehe=360, blick=-1):
    """Dreieckige, vertikale Formfamilie: hoher schmaler Umriss, langer Kittel,
    Hände in den Taschen. Steht leicht angelehnt, nie strammstehend."""
    e = hoehe / 360.0
    ky = bodeny - hoehe
    s = []
    # Beine: schmal, ein Fuß vor dem anderen
    s.append(rechteck(x - 22 * e, ky + 236 * e, 20 * e, hoehe - 236 * e - 6 * e, 0.9))
    s.append(rechteck(x + 6 * e, ky + 236 * e, 20 * e, hoehe - 236 * e - 6 * e, 0.86))
    for fx in (x - 30 * e, x + 2 * e):
        s.append(f'<path d="M{F(fx)},{F(bodeny - 8 * e)} h{F(34 * e)} q{F(7 * e)},{F(8 * e)} '
                 f'{F(-7 * e)},{F(9 * e)} h{F(-27 * e)} z" {tinte(0.93)}/>')
    # Kittel: Dreieck, unten breit, mit scharfem Saum
    kittel = (f'M{F(x - 4 * e)},{F(ky + 52 * e)} '
              f'C{F(x - 34 * e)},{F(ky + 70 * e)} {F(x - 46 * e)},{F(ky + 150 * e)} {F(x - 54 * e)},{F(ky + 266 * e)} '
              f'L{F(x + 52 * e)},{F(ky + 266 * e)} '
              f'C{F(x + 46 * e)},{F(ky + 148 * e)} {F(x + 34 * e)},{F(ky + 70 * e)} {F(x + 8 * e)},{F(ky + 52 * e)} Z')
    s.append(f'<path d="{kittel}" fill="{PHOSPHOR}" fill-opacity="0.22" '
             f'transform="translate({F(-6 * e)},{F(-3 * e)})"/>')
    s.append(f'<path d="{kittel}" {tinte(0.30)}/>')
    s.append(falte(x - 26 * e, ky + 96 * e, x - 38 * e, ky + 236 * e, -8 * e, 0.3, 3 * e))
    s.append(falte(x + 22 * e, ky + 100 * e, x + 34 * e, ky + 240 * e, 8 * e, 0.26, 3 * e))
    s.append(rasterflaeche([(x - 54 * e, ky + 266 * e), (x - 44 * e, ky + 140 * e),
                            (x - 10 * e, ky + 160 * e), (x - 12 * e, ky + 266 * e)], 0.22, fein=True))
    s.append(f'<path d="M{F(x - 4 * e)},{F(ky + 52 * e)} '
             f'C{F(x - 34 * e)},{F(ky + 70 * e)} {F(x - 46 * e)},{F(ky + 150 * e)} {F(x - 54 * e)},{F(ky + 266 * e)} '
             f'L{F(x + 52 * e)},{F(ky + 266 * e)} '
             f'C{F(x + 46 * e)},{F(ky + 148 * e)} {F(x + 34 * e)},{F(ky + 70 * e)} {F(x + 8 * e)},{F(ky + 52 * e)}" '
             f'{strich(0.9, 3 * e)}/>')
    s.append(f'<path d="M{F(x + 2 * e)},{F(ky + 56 * e)} L{F(x - 2 * e)},{F(ky + 266 * e)}" {strich(0.55, 3 * e)}/>')
    # Taschen mit Händen darin
    for px in (-40, 16):
        s.append(f'<path d="M{F(x + px * e)},{F(ky + 176 * e)} h{F(26 * e)}" {strich(0.6, 3 * e)}/>')
    s.append(f'<path d="M{F(x - 16 * e)},{F(ky + 78 * e)} C{F(x - 44 * e)},{F(ky + 118 * e)} '
             f'{F(x - 42 * e)},{F(ky + 156 * e)} {F(x - 32 * e)},{F(ky + 180 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.82" stroke-width="{F(21 * e)}" stroke-linecap="round"/>')
    s.append(f'<path d="M{F(x + 20 * e)},{F(ky + 78 * e)} C{F(x + 44 * e)},{F(ky + 118 * e)} '
             f'{F(x + 42 * e)},{F(ky + 156 * e)} {F(x + 30 * e)},{F(ky + 180 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.82" stroke-width="{F(21 * e)}" stroke-linecap="round"/>')
    # Stethoskop mit rissigem Schlauch
    s.append(f'<path d="M{F(x - 14 * e)},{F(ky + 58 * e)} C{F(x - 24 * e)},{F(ky + 110 * e)} '
             f'{F(x - 20 * e)},{F(ky + 140 * e)} {F(x - 12 * e)},{F(ky + 156 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.7" stroke-width="{F(6 * e)}"/>')
    s.append(f'<path d="M{F(x + 14 * e)},{F(ky + 58 * e)} C{F(x + 24 * e)},{F(ky + 104 * e)} '
             f'{F(x + 16 * e)},{F(ky + 130 * e)} {F(x + 2 * e)},{F(ky + 150 * e)}" '
             f'fill="none" stroke="{TINTE}" stroke-opacity="0.7" stroke-width="{F(6 * e)}"/>')
    s.append(f'<circle cx="{F(x - 12 * e)}" cy="{F(ky + 162 * e)}" r="{F(10 * e)}" {tinte(0.92)}/>')
    # Hals, Kopf, hoher Haaransatz, Brille an der Kette
    s.append(rechteck(x - 11 * e, ky + 30 * e, 22 * e, 26 * e, 0.8))
    s.append(f'<ellipse cx="{F(x + 3 * e * blick * -1)}" cy="{F(ky + 14 * e)}" rx="{F(28 * e)}" ry="{F(31 * e)}" '
             f'{tinte(0.86)}/>')
    s.append(f'<path d="M{F(x - 24 * e)},{F(ky - 6 * e)} C{F(x - 16 * e)},{F(ky - 28 * e)} '
             f'{F(x + 22 * e)},{F(ky - 28 * e)} {F(x + 28 * e)},{F(ky - 2 * e)}" {strich(0.92, 7 * e)}/>')
    for bx in (-13, 9):
        s.append(f'<circle cx="{F(x + bx * e)}" cy="{F(ky + 12 * e)}" r="{F(9 * e)}" fill="none" '
                 f'stroke="{PAPIER}" stroke-opacity="0.8" stroke-width="{F(2.6 * e)}"/>')
    s.append(f'<line x1="{F(x - 4 * e)}" y1="{F(ky + 12 * e)}" x2="{F(x)}" y2="{F(ky + 12 * e)}" '
             f'stroke="{PAPIER}" stroke-opacity="0.8" stroke-width="{F(2.4 * e)}"/>')
    s.append(f'<path d="M{F(x - 22 * e)},{F(ky + 16 * e)} C{F(x - 36 * e)},{F(ky + 34 * e)} '
             f'{F(x - 30 * e)},{F(ky + 54 * e)} {F(x - 16 * e)},{F(ky + 60 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.38" stroke-width="{F(2 * e)}"/>')
    s.append(f'<path d="M{F(x - 4 * e)},{F(ky + 26 * e)} q{F(7 * e)},{F(4 * e)} {F(1 * e)},{F(9 * e)}" '
             f'fill="none" stroke="{PAPIER}" stroke-opacity="0.3" stroke-width="{F(2 * e)}"/>')
    # Messingzirkel in der Hand, der im Spiel zum Werkzeug wird
    s.append(f'<path d="M{F(x + 34 * e)},{F(ky + 182 * e)} l{F(7 * e)},{F(42 * e)} '
             f'M{F(x + 34 * e)},{F(ky + 182 * e)} l{F(-8 * e)},{F(43 * e)}" '
             f'fill="none" stroke="{BERNSTEIN}" stroke-opacity="0.95" stroke-width="{F(4.6 * e)}" stroke-linecap="round"/>')
    s.append(f'<circle cx="{F(x + 34 * e)}" cy="{F(ky + 180 * e)}" r="{F(5.5 * e)}" fill="{BERNSTEIN}" fill-opacity="0.95"/>')
    # Kaffeefleck am Kittel
    s.append(f'<ellipse cx="{F(x + 16 * e)}" cy="{F(ky + 206 * e)}" rx="{F(9 * e)}" ry="{F(6 * e)}" '
             f'fill="{BERNSTEIN}" fill-opacity="0.35"/>')
    return "".join(s)


def portrait(wer):
    """Brustbild für den Dialog: 220×220, Kreisrahmen, eine Akzentfarbe."""
    g, cx, cy = [], 110, 118
    g.append(f'<circle cx="{cx}" cy="{cy}" r="104" fill="{PAPIER}"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="104" fill="url(#raster_fein)" opacity="0.16"/>')
    g.append(f'<g clip-path="url(#rund)">')
    if wer == "marlene":
        g.append(farbpolygon([(0, 150), (220, 130), (220, 230), (0, 230)], MAGENTA, 0.12))
        g.append(marlene(118, 262, hoehe=250, akzent_magenta=True))
    elif wer == "herr_k":
        g.append(farbpolygon([(0, 150), (220, 130), (220, 230), (0, 230)], BERNSTEIN, 0.14))
        g.append(herr_k(98, 408, hoehe=342, tuete=False))
    else:                                                   # Dr. Falk — dreieckige, vertikale Formfamilie
        e = 1.0
        g.append(farbpolygon([(0, 150), (220, 130), (220, 230), (0, 230)], BERNSTEIN, 0.10))
        g.append(f'<path d="M30,236 L72,112 C84,86 136,86 148,112 L196,236 Z" {tinte(0.84)}/>')
        g.append(f'<path d="M104,110 L104,236" {strich(0.5, 4)}/>')
        g.append(rechteck(96, 92, 24, 26, 0.8))
        g.append(f'<ellipse cx="110" cy="66" rx="34" ry="38" {tinte(0.86)}/>')
        g.append(f'<path d="M78,42 C86,18 136,16 144,44" {strich(0.92, 9)}/>')   # Haaransatz, hoch
        for bx in (94, 126):                                                      # Brille
            g.append(f'<circle cx="{bx}" cy="64" r="13" fill="none" stroke="{PAPIER}" '
                     f'stroke-opacity="0.85" stroke-width="3.2"/>')
        g.append(f'<line x1="107" y1="64" x2="113" y2="64" stroke="{PAPIER}" stroke-opacity="0.85" stroke-width="3"/>')
        g.append(f'<path d="M81,66 C66,78 70,104 84,112" fill="none" stroke="{PAPIER}" '
                 f'stroke-opacity="0.45" stroke-width="2.4"/>')                   # Brillenkette
        g.append(f'<path d="M139,66 C154,78 150,104 136,112" fill="none" stroke="{PAPIER}" '
                 f'stroke-opacity="0.45" stroke-width="2.4"/>')
        g.append(f'<path d="M96,92 C92,124 88,150 92,176" fill="none" stroke="{TINTE}" '
                 f'stroke-opacity="0.5" stroke-width="7"/>')                      # Stethoskop
        g.append(f'<circle cx="94" cy="182" r="11" {tinte(0.9)}/>')
        # Messingzirkel in der Hand
        g.append(f'<path d="M150,150 L164,206 M150,150 L140,208" fill="none" stroke="{BERNSTEIN}" '
                 f'stroke-opacity="0.95" stroke-width="5" stroke-linecap="round"/>')
        g.append(f'<circle cx="150" cy="148" r="6" fill="{BERNSTEIN}" fill-opacity="0.95"/>')
    g.append("</g>")
    g.append(f'<circle cx="{cx}" cy="{cy}" r="104" fill="none" stroke="{TINTE}" stroke-opacity="0.9" stroke-width="5"/>')
    innen = "".join(g)
    return (f'<svg viewBox="0 0 220 240" xmlns="http://www.w3.org/2000/svg" class="portrait">{defs()}'
            f'<clipPath id="rund"><circle cx="{cx}" cy="{cy}" r="104"/></clipPath>'
            f'<g filter="url(#zittern_fein)">{innen}</g>'
            f'<rect x="0" y="0" width="220" height="240" filter="url(#korn)" opacity="0.22" '
            f'style="mix-blend-mode:multiply"/></svg>')


# ============================================================ Szene 1 · Aufnahme 06:40
BODEN = 628


def aufnahme_hintergrund():
    s = [farbfeld(0, 0, B, H, PAPIER, 1.0)]
    # Wand: nach oben und zu den Seiten dunkler
    s.append(rechteck(0, 0, B, BODEN, 0.12))
    s.append(rasterflaeche([(0, 0), (B, 0), (B, 190), (0, 230)], 0.28))
    # Boden
    s.append(rechteck(0, BODEN, B, H - BODEN, 0.26))
    s.append(f'<line x1="0" y1="{BODEN}" x2="{B}" y2="{BODEN}" stroke="{TINTE}" stroke-opacity="0.6" stroke-width="3"/>')
    for i in range(1, 9):                                            # Fliesenfugen in Fluchtlinien
        x = 160 + i * 190
        s.append(f'<line x1="{F(x)}" y1="{BODEN}" x2="{F(x + (x - 800) * 0.55)}" y2="{H}" '
                 f'stroke="{TINTE}" stroke-opacity="0.16" stroke-width="2"/>')
    for i, yy in enumerate((690, 772, 870)):
        s.append(f'<line x1="0" y1="{yy}" x2="{B}" y2="{yy}" stroke="{TINTE}" stroke-opacity="0.13" stroke-width="2"/>')
    # Fenster mit Jalousie — die Lichtquelle, tief stehende Sonne
    s.append(jalousie(646, 86, 414, 304))
    # Lichtkeile quer durch den Raum, flach wie beim Sonnenaufgang
    for i in range(5):
        y0 = 136 + i * 58
        s.append(lichtschacht(1062, y0, 1062, y0 + 28, 620, 15 + i * 1.6, 0.17 - i * 0.013))
    # Lichtinsel auf dem Boden, rechts unter dem Fenster
    s.append(farbpolygon([(1000, BODEN + 10), (1520, BODEN - 4), (1600, 892), (1030, 900)],
                         BERNSTEIN, 0.32, filter_="weich"))
    s.append(farbpolygon([(1080, BODEN + 40), (1440, BODEN + 30), (1520, 848), (1110, 860)],
                         BERNSTEIN, 0.22, filter_="weich"))
    # Wanduhr rechts vom Fenster, Pinnwand über dem Tresen
    s.append(wanduhr(1268, 168))
    s.append(pinnwand(158, 112, 246, 164))
    # Flur-Durchgang hinten rechts: dunkle Öffnung mit kaltem Restlicht
    s.append(rechteck(1432, 236, 152, 392, 0.74))
    s.append(farbfeld(1440, 248, 136, 368, PAPIER, 0.09))
    s.append(farbpolygon([(1440, 616), (1576, 616), (1596, 700), (1424, 702)], PAPIER, 0.16, filter_="weich_leicht"))
    return ebene("".join(s) + korn(0.26), versatz=(0, 0), klasse="e-hintergrund")


def aufnahme_mittelgrund():
    s = [ekg_wagen(700, BODEN + 22)]
    # Stühle: Schlagschatten nach rechts, weil die Sonne von links kommt
    for sx in (1064, 1228, 1392):
        s.append(farbpolygon([(sx + 16, 708), (sx + 124, 706), (sx + 196, 798), (sx + 72, 804)],
                             TINTE, 0.17, filter_="weich_leicht"))
    for sx in (1064, 1228, 1392):
        s.append(stuhl(sx, 708))
    # Marlene steht hinter dem Tresen — also wird sie vor ihm gezeichnet
    s.append(f'<g id="fig-marlene" class="atmet">{marlene(402, 604, hoehe=312, kanne=False)}</g>')
    s.append(tresen(178, 486, 430, 152))
    s.append(thermoskanne(338, 500, 62, True))
    s.append(tischlampe(486, 404))
    return ebene("".join(s), versatz=(1.2, -0.8), filter_="zittern_fein", klasse="e-mittelgrund")


def aufnahme_figuren():
    s = [f'<ellipse cx="1288" cy="714" rx="104" ry="17" {tinte(0.28)}/>',
         f'<g id="fig-herrk" class="atmet langsam">{herr_k(1272, 712, hoehe=262, tuete_magenta=False)}</g>']
    return ebene("".join(s), versatz=(-0.9, 0.6), filter_="zittern_fein", klasse="e-figuren")


def aufnahme_vordergrund():
    s = [f'<g filter="url(#weich_leicht)">{tuerrahmen_links(176)}</g>']
    s.append(f'<g filter="url(#weich_leicht)">{infusionsstaender(1528, 892)}</g>')
    s.append(f'<rect x="0" y="0" width="{B}" height="{H}" fill="url(#vignette)"/>')
    # Staub im Lichtkeil
    punkte = [(820, 300, 3), (900, 362, 2), (986, 276, 2.5), (1062, 420, 2), (1140, 330, 3),
              (1220, 470, 2), (760, 420, 2.5), (1300, 392, 2), (880, 500, 2), (1040, 236, 2)]
    for px, py, pr in punkte:
        s.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="{BERNSTEIN}" fill-opacity="0.5"/>')
    return ebene("".join(s), versatz=(-2.2, 1.4), klasse="e-vordergrund")


# ============================================================ Szene 2 · Monitorzimmer 09:15
def monitor_hintergrund():
    s = [farbfeld(0, 0, B, H, PAPIER, 1.0)]
    s.append(rechteck(0, 0, B, 660, 0.18))
    s.append(rasterflaeche([(0, 0), (B, 0), (B, 240), (0, 280)], 0.30))
    s.append(rechteck(0, 660, B, H - 660, 0.3))
    s.append(f'<line x1="0" y1="660" x2="{B}" y2="660" stroke="{TINTE}" stroke-opacity="0.6" stroke-width="3"/>')
    # Fenster: kühler Vormittag, Licht flach und gleichmäßig
    s.append(f'<g>{farbfeld(60, 110, 300, 290, PAPIER, 0.92, r=3)}</g>')
    s.append(f'<rect x="60" y="110" width="300" height="290" rx="3" {strich(0.88, 5)}/>')
    s.append(rechteck(204, 110, 8, 290, 0.6))
    s.append(rechteck(60, 248, 300, 7, 0.6))
    s.append(f'<g filter="url(#weich_stark)">{farbfeld(20, 70, 380, 370, PAPIER, 0.8)}</g>')
    s.append(farbpolygon([(360, 400), (600, 400), (760, 660), (300, 660)], PAPIER, 0.26, filter_="weich"))
    s.append(rechteck(52, 396, 316, 14, 0.7))                                  # Fensterbank
    s.append(f'<line x1="68" y1="330" x2="352" y2="330" stroke="{TINTE}" stroke-opacity="0.13" stroke-width="3"/>')
    # Monitorwand: gewachsen statt gerastert — andere Größen, andere Höhen, einer aus
    schirme = [(506, 132, 296, 214, 0.17, -0.8), (838, 150, 238, 176, 0.13, 0.6),
               (1112, 118, 266, 196, 0.00, 1.4), (524, 392, 232, 170, 0.11, 0.9),
               (794, 372, 322, 232, 0.21, -0.5), (1156, 356, 212, 158, 0.09, 1.8)]
    for mx, my, mb, mh, glut, dreh in schirme:
        g = [rechteck(mx + mb * 0.42, my + mh, 26, 22, 0.7),                   # Wandarm
             rechteck(mx, my, mb, mh, 0.88, r=9),
             farbfeld(mx + 11, my + 11, mb - 22, mh - 44, PHOSPHOR if glut else TINTE, glut if glut else 0.5, r=3)]
        if glut:
            g.append(f'<g filter="url(#weich_leicht)">{farbfeld(mx + 11, my + 11, mb - 22, mh - 44, PHOSPHOR, glut * 0.8, r=3)}</g>')
            g.append(f'<rect x="{F(mx + 11)}" y="{F(my + 11)}" width="{F(mb - 22)}" height="{F(mh - 44)}" rx="3" '
                     f'fill="none" stroke="{PHOSPHOR}" stroke-opacity="0.38" stroke-width="1.6"/>')
            g.append(f'<circle cx="{F(mx + 20)}" cy="{F(my + mh - 15)}" r="4.5" fill="{PHOSPHOR}" fill-opacity="0.8"/>')
        else:
            g.append(f'<circle cx="{F(mx + 20)}" cy="{F(my + mh - 15)}" r="4.5" fill="{BERNSTEIN}" fill-opacity="0.75"/>')
        s.append(f'<g transform="rotate({dreh} {F(mx + mb / 2)} {F(my + mh / 2)})">' + "".join(g) + "</g>")
    # Kabel, die von den unteren Schirmen hinunterhängen
    for x0, x1 in ((600, 672), (880, 968), (1220, 1282)):
        s.append(bogen(x0, 600, x1, 628, -34, 0.45, 3))
    return ebene("".join(s) + korn(0.24), klasse="e-hintergrund")


def monitor_mittelgrund():
    s = [f'<ellipse cx="1238" cy="694" rx="78" ry="13" {tinte(0.24)}/>',
         f'<g id="fig-falk" class="atmet langsam">{falk(1232, 692, hoehe=330)}</g>']
    # Schreibtisch über die ganze Breite, Platte perspektivisch
    s.append(polygon([(300, 640), (1340, 626), (1420, 700), (250, 718)], 0.34))
    s.append(rasterflaeche([(300, 640), (1340, 626), (1420, 700), (250, 718)], 0.2, fein=True))
    s.append(polygon([(250, 714), (1420, 696), (1420, 790), (250, 812)], 0.66))
    s.append(f'<path d="M300,640 L1340,626 L1420,700 L250,718 Z" {strich(0.8, 3)}/>')
    # Tastatur, Maus, Kaffeebecher (Marlene war da — Magenta genau einmal)
    s.append(polygon([(520, 664), (760, 658), (772, 686), (528, 694)], 0.5))
    for r_ in range(3):
        for c in range(11):
            s.append(farbfeld(532 + c * 20, 666 + r_ * 8, 15, 5, PAPIER, 0.35, r=1))
    s.append(f'<ellipse cx="830" cy="676" rx="22" ry="13" {tinte(0.55)}/>')
    s.append(f'<rect x="402" y="616" width="52" height="60" rx="5" fill="{MAGENTA}" fill-opacity="0.92"/>')
    s.append(f'<path d="M454,630 q22,16 0,32" fill="none" stroke="{MAGENTA}" stroke-opacity="0.92" stroke-width="7"/>')
    s.append(farbfeld(408, 620, 40, 7, PAPIER, 0.4))
    # Drehstuhl, von hinten angeschnitten
    s.append(f'<path d="M980,790 C980,700 1180,700 1180,790 Z" {tinte(0.8)}/>')
    s.append(rechteck(1072, 788, 14, 70, 0.86))
    s.append(f'<path d="M1010,874 L1148,874" {strich(0.86, 9)}/>')
    s.append(tischlampe(1246, 556, arm=58))
    return ebene("".join(s), versatz=(1.4, -0.9), filter_="zittern_fein", klasse="e-mittelgrund")


def monitor_figuren():
    """Leer: Dr. Falk steht hinter dem Tisch und gehört deshalb in den Mittelgrund."""
    return ebene("", versatz=(-0.8, 0.5), klasse="e-figuren")


def monitor_vordergrund():
    s = [f'<g filter="url(#weich_leicht)">{polygon([(0, 0), (B, 0), (B, 46), (0, 62)], 0.9)}</g>']
    s.append(f'<g filter="url(#weich_leicht)">{polygon([(1468, 0), (B, 0), (B, H), (1430, H)], 0.9)}</g>')
    # Drehstuhllehne schneidet unten links an: Kopfstütze, Polsterfuge, Rahmen
    lehne = ('<path d="M-60,900 L-60,742 Q-56,678 24,668 L214,652 Q286,648 292,712 L310,900 Z" '
             f'{tinte(0.93)}/>'
             '<path d="M-40,760 Q130,742 282,730" fill="none" stroke="' + PAPIER + '" stroke-opacity="0.12" '
             'stroke-width="5"/>'
             '<path d="M-30,838 Q130,820 296,812" fill="none" stroke="' + PAPIER + '" stroke-opacity="0.09" '
             'stroke-width="5"/>')
    s.append(f'<g filter="url(#weich_leicht)">{lehne}</g>')
    s.append(f'<rect x="0" y="0" width="{B}" height="{H}" fill="url(#vignette)"/>')
    return ebene("".join(s), versatz=(-2.4, 1.6), klasse="e-vordergrund")


# ============================================================ Schema · Herz (Reizleitung)
# Ligne claire (docs/ART_BIBLE.md, Stand 10.10.2026): flache Lokalfarben, eine
# gleichmäßig dünne Tuschelinie, keine Schraffur, kein Verlauf, kein Text.
# Das Schema ist ein Lehrbild, kein Raum: Muskel, Höhlen, Gefäße, Klappenebene.
# Die Reizleitung selbst zeichnet das Rätsel (web/raetsel_reizleitung.js) —
# hier stehen nur ihre Wege und die Plätze, damit Bild und Spiel aus derselben
# Geometrie kommen.
LIGNE_CLAIRE = {
    "sand": "#EFE6D3", "papier": "#F7F1E4", "mint": "#BFD9CF", "petrol": "#2C5560",
    "tinte": "#1E2A30", "holz": "#C99A5B", "rost": "#B5552D",
}
HERZ_B, HERZ_H = 640, 600
HERZ_LINIE = 2.0                       # eine Linie, überall gleich


def _glatt(punkte, zu=True):
    """Catmull-Rom durch die Punkte, als kubische Bézier-Kurve — gerechnet, nicht gezogen."""
    n = len(punkte)
    if n < 3:
        return "M" + " L".join(f"{F(x)},{F(y)}" for x, y in punkte)

    def p(i):
        return punkte[i % n] if zu else punkte[max(0, min(n - 1, i))]

    d = [f"M{F(punkte[0][0])},{F(punkte[0][1])}"]
    for i in range(n if zu else n - 1):
        p0, p1, p2, p3 = p(i - 1), p(i), p(i + 1), p(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{F(c1[0])},{F(c1[1])} {F(c2[0])},{F(c2[1])} {F(p2[0])},{F(p2[1])}")
    if zu:
        d.append("Z")
    return " ".join(d)


def _rund(punkte, r=40):
    """Geschlossenes Vieleck mit abgerundeten Ecken (je Ecke eine quadratische Kurve,
    höchstens bis zur halben Kantenlänge) — glatt, ohne Überschwingen."""
    n = len(punkte)
    d = []
    for i in range(n):
        a, b, e = punkte[i - 1], punkte[i], punkte[(i + 1) % n]
        l1, l2 = math.dist(a, b), math.dist(b, e)
        k1, k2 = min(r, l1 / 2) / (l1 or 1), min(r, l2 / 2) / (l2 or 1)
        p1 = (b[0] + (a[0] - b[0]) * k1, b[1] + (a[1] - b[1]) * k1)
        p2 = (b[0] + (e[0] - b[0]) * k2, b[1] + (e[1] - b[1]) * k2)
        d.append(("M" if i == 0 else "L") + f"{F(p1[0])},{F(p1[1])} Q{F(b[0])},{F(b[1])} {F(p2[0])},{F(p2[1])}")
    return " ".join(d) + " Z"


def _versetzt(kette, mitte, abstand):
    """Punkte einer Höhlenwand um `abstand` nach außen (weg von der Höhlenmitte) — dort,
    unter der Innenschicht, liegt das Purkinje-Netz."""
    aus = []
    for x, y in kette:
        dx, dy = x - mitte[0], y - mitte[1]
        lang = math.hypot(dx, dy) or 1.0
        aus.append((x + dx / lang * abstand, y + dy / lang * abstand))
    return aus


def herz_schema():
    """Schematisches Herz von vorn: Vorhöfe, Kammern, Scheidewände, Klappenebene.

    Rückgabe: (svg, geo). `geo` enthält die Plätze für die fünf Bauteile, zwei
    Fehlplätze, die Bahnen der Reizleitung und die Flächen für die Erregung —
    alles in den Koordinaten der viewBox."""
    c = LIGNE_CLAIRE
    linie = (f'stroke="{c["tinte"]}" stroke-width="{HERZ_LINIE}" '
             'stroke-linejoin="round" stroke-linecap="round"')

    # Außenkontur des Herzmuskels, im Uhrzeigersinn ab der Mündung der oberen Hohlvene
    umriss_p = [(150, 118), (116, 146), (100, 196), (104, 240), (114, 278), (118, 326), (134, 392),
                (172, 456), (234, 512), (304, 556), (372, 578), (422, 566), (472, 524), (516, 454),
                (546, 372), (556, 306), (552, 276), (552, 232), (540, 184), (512, 146), (466, 124),
                (410, 120), (360, 128), (316, 118), (268, 108), (222, 110)]
    umriss = _glatt(umriss_p)

    # Höhlen (Blut): rechter/linker Vorhof, rechte/linke Kammer
    ra = [(160, 140), (132, 170), (124, 214), (132, 250), (156, 260), (232, 262), (284, 258),
          (296, 222), (290, 176), (268, 146), (220, 134)]
    la = [(334, 150), (328, 200), (334, 250), (356, 260), (518, 260), (532, 226), (522, 182),
          (494, 154), (446, 140), (386, 140)]
    rv = [(136, 298), (296, 298), (306, 346), (318, 404), (334, 464), (348, 510),
          (318, 516), (268, 494), (210, 452), (154, 398), (132, 344)]
    lv = [(346, 298), (526, 298), (526, 342), (514, 400), (490, 456), (452, 500),
          (406, 528), (378, 526), (366, 468), (356, 402), (348, 346)]

    band_y0, band_y1 = 266, 290       # Klappenebene: Bindegewebe, leitet nicht

    # Gefäße (liegen hinter dem Muskel)
    hohlvene = "M168,128 L164,12 L226,12 L222,128 Z"
    aorta = ("M332,132 C330,96 334,62 350,44 C372,20 430,14 470,30 C496,40 506,62 504,92 "
             "L462,96 C462,76 454,64 438,60 C412,54 392,62 384,82 C378,98 380,116 382,132 Z")
    lungenvenen = [
        "M536,170 C560,164 590,162 626,166 L626,196 C594,192 566,194 544,202 Z",
        "M548,222 C572,220 600,222 626,226 L626,254 C600,250 574,250 552,254 Z",
    ]

    # Segelklappen: zwei Segel je Seite, vom Klappenring in die Kammer
    segel = [[(170, band_y1), (188, band_y1), (184, 330)], [(246, band_y1), (264, band_y1), (252, 326)],
             [(400, band_y1), (418, band_y1), (412, 334)], [(474, band_y1), (492, band_y1), (480, 328)]]

    s = [f'<svg viewBox="0 0 {HERZ_B} {HERZ_H}" xmlns="http://www.w3.org/2000/svg" '
         'class="schema-herz" preserveAspectRatio="xMidYMid meet">',
         f'<defs><clipPath id="herz-umriss-clip"><path d="{umriss}"/></clipPath></defs>']
    s.append(f'<path d="{hohlvene}" fill="{c["sand"]}" {linie}/>')
    s.append(f'<path d="{aorta}" fill="{c["sand"]}" {linie}/>')
    for d in lungenvenen:
        s.append(f'<path d="{d}" fill="{c["sand"]}" {linie}/>')
    s.append(f'<path d="{umriss}" fill="{c["mint"]}"/>')
    for hoehle in (ra, la, rv, lv):
        s.append(f'<path d="{_rund(hoehle)}" fill="{c["sand"]}" {linie}/>')
    s.append(f'<g clip-path="url(#herz-umriss-clip)">'
             f'<rect x="0" y="{band_y0}" width="{HERZ_B}" height="{band_y1 - band_y0}" fill="{c["petrol"]}"/>'
             f'<line x1="0" y1="{band_y0}" x2="{HERZ_B}" y2="{band_y0}" {linie}/>'
             f'<line x1="0" y1="{band_y1}" x2="{HERZ_B}" y2="{band_y1}" {linie}/></g>')
    for sg in segel:
        s.append(f'<polygon points="{pts(sg)}" fill="{c["papier"]}" {linie}/>')
    s.append(f'<path d="{umriss}" fill="none" {linie}/>')
    s.append('</svg>')

    # ---- Plätze: fünf richtige, zwei falsche. Die Etage entscheidet, was ein falscher Platz bedeutet.
    plaetze = {
        "sinus":    {"x": 178, "y": 132, "etage": "vorhof"},   # rechter Vorhof, Mündung der oberen Hohlvene
        "av":       {"x": 300, "y": 238, "etage": "vorhof"},   # unten in der Vorhofscheidewand
        "his":      {"x": 322, "y": 306, "etage": "grenze"},   # durch die Klappenebene, Septumoberkante
        "schenkel": {"x": 336, "y": 412, "etage": "kammer"},   # Kammerscheidewand
        "purkinje": {"x": 376, "y": 540, "etage": "kammer"},   # Herzspitze, unter der Innenschicht
        "linker_vorhof": {"x": 468, "y": 176, "etage": "vorhof"},
        "klappenring":   {"x": 470, "y": 278, "etage": "grenze"},
    }

    # ---- Bahnen der Reizleitung: so liegen die Bauteile, wenn sie richtig sitzen
    his = "M304,248 C312,264 318,284 322,318"
    schenkel = ["M322,318 C322,360 326,414 340,498",          # rechter Schenkel, rechts am Septum
                "M324,318 C338,352 350,414 368,496"]          # linker Schenkel, links am Septum
    mitte_rv, mitte_lv = (238, 400), (436, 404)
    netz_r = _versetzt([(318, 514), (268, 492), (210, 450), (154, 396)], mitte_rv, 10)
    netz_l = _versetzt([(380, 524), (406, 526), (452, 500), (490, 456), (514, 400)], mitte_lv, 11)
    purkinje = [_glatt([(340, 498)] + netz_r, zu=False), _glatt([(368, 496)] + netz_l, zu=False)]
    aeste = []
    for kette, mitte in ((netz_r, mitte_rv), (netz_l, mitte_lv)):      # kurze Äste in die Wand
        for x, y in kette[1:]:
            dx, dy = x - mitte[0], y - mitte[1]
            lang = math.hypot(dx, dy) or 1.0
            aeste.append(f"M{F(x)},{F(y)} L{F(x + dx / lang * 13)},{F(y + dy / lang * 13)}")

    geo = {
        "viewBox": f"0 0 {HERZ_B} {HERZ_H}",
        "plaetze": plaetze,
        "teile": {
            "sinus": {"ellipse": [178, 132, 15, 9, -32]},
            "av": {"ellipse": [302, 242, 13, 8, 58]},
            "his": {"bahnen": [his]},
            "schenkel": {"bahnen": schenkel},
            "purkinje": {"bahnen": purkinje + aeste, "fein": True},
        },
        "punkte": {"sinus": [178, 132], "av": [302, 242], "his_anfang": [304, 248],
                   "his_ende": [322, 318], "sperre": [314, 278]},
        "wege": {
            "vorhof_av": "M178,132 C214,164 268,190 302,242",      # Vorhofmuskel bis zum AV-Knoten
            "vorhof_links": "M178,132 C262,106 430,110 514,222",   # über das Dach in den linken Vorhof
            "vorhof_unten": "M178,132 C150,180 150,230 196,258",   # an der Seitenwand hinunter
            "purkinje": purkinje,                                  # Hauptstränge ohne Äste
        },
        "flaechen": {"umriss": umriss, "band": [band_y0, band_y1]},
        "farben": c,
    }
    return "".join(s), geo


# ============================================================ Ausgabe
SZENEN = {
    "aufnahme": {
        "hintergrund": aufnahme_hintergrund,
        "mittelgrund": aufnahme_mittelgrund,
        "figuren": aufnahme_figuren,
        "vordergrund": aufnahme_vordergrund,
    },
    "monitor": {
        "hintergrund": monitor_hintergrund,
        "mittelgrund": monitor_mittelgrund,
        "figuren": monitor_figuren,
        "vordergrund": monitor_vordergrund,
    },
}


def png_ebene(pfad, extra=""):
    """Gerenderte Ebene (PNG) als SVG mit eingebettetem Bild — für Szenen aus der Blender-Pipeline.
    `extra`: weitere SVG-Elemente über dem Bild, in derselben Ebene (z. B. die Uhrzeiger)."""
    import base64
    with open(pfad, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return ('<svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" '
            'xmlns="http://www.w3.org/2000/svg"><image href="data:image/png;base64,' + b64 +
            '" x="0" y="0" width="1600" height="900"/>' + extra + '</svg>')


def uhr_teile(ordner):
    """Uhrzeiger (#uhr-std, #uhr-min) über einem gerenderten Zifferblatt; die Engine dreht sie nach der
    Spielzeit. Lage und Größe kommen aus hitboxes.json (Feld "uhr"). Sie gehören in dieselbe Ebene wie das
    Zifferblatt (Hintergrund), sonst wandern sie in der Parallaxe gegen die Uhr."""
    pfad = os.path.join(ordner, "hitboxes.json")
    if not os.path.exists(pfad):
        return ""
    hb = json.load(open(pfad, encoding="utf-8"))
    if "uhr" not in hb:
        return ""
    x0, y0, x1, y1 = hb["uhr"]
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) / 2 * 0.86
    dick = 5 if r > 45 else 3.5
    return (f'<line id="uhr-std" x1="{F(cx)}" y1="{F(cy)}" x2="{F(cx)}" y2="{F(cy - r * 0.52)}" '
            f'stroke="{LINIE}" stroke-width="{dick}" stroke-linecap="round" transform="rotate(0 {F(cx)} {F(cy)})"/>'
            f'<line id="uhr-min" x1="{F(cx)}" y1="{F(cy)}" x2="{F(cx)}" y2="{F(cy - r * 0.8)}" '
            f'stroke="{LINIE}" stroke-width="{dick * 0.6:.1f}" stroke-linecap="round" transform="rotate(0 {F(cx)} {F(cy)})"/>'
            f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{3 if r > 45 else 2.2}" fill="{LINIE}"/>')


def _png64(pfad):
    import base64
    with open(pfad, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def png_figuren(ordner):
    """Figurenebene aus einzelnen gerenderten Figuren (gen/blender/ebenen_figuren.py raum):
    figuren.json nennt je Figur Datei, Bühnenposition und Atem-Klasse; jede Figur wird ein eigenes
    <g id="fig-…" class="atmet">, damit die Engine sie einzeln atmen lassen kann."""
    with open(os.path.join(ordner, "figuren.json"), encoding="utf-8") as f:
        platz = json.load(f)
    g = []
    for name, p in platz.items():
        g.append(f'<g id="fig-{name}" class="{p.get("klasse", "atmet")}"><image href="data:image/png;base64,'
                 + _png64(os.path.join(ordner, p["datei"])) +
                 f'" x="{p["x"]}" y="{p["y"]}" width="{p["breite"]}" height="{p["hoehe"]}"/></g>')
    return ('<svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" '
            'xmlns="http://www.w3.org/2000/svg">' + "".join(g) + '</svg>')


def png_portrait(pfad):
    """Gerendertes Brustbild (400×440, Alpha) für den Dialog; das Papier dahinter kommt aus dem CSS."""
    return ('<svg viewBox="0 0 400 440" preserveAspectRatio="xMidYMid slice" class="portrait" '
            'xmlns="http://www.w3.org/2000/svg"><image href="data:image/png;base64,' + _png64(pfad) +
            '" x="0" y="0" width="400" height="440"/></svg>')


def baue():
    aus = {"szenen": {}, "portraits": {}}
    hier = os.path.dirname(os.path.abspath(__file__))
    for name, ebenen in SZENEN.items():
        aus["szenen"][name] = {k: f() for k, f in ebenen.items()}
        ordner = os.path.join(os.path.dirname(hier), "art", "szenen", name)
        if not os.path.isdir(ordner):
            continue                                    # kein Render: die gezeichneten SVG-Ebenen bleiben
        # Gerenderter Raum: jede Ebene kommt aus art/szenen/<name>/ — fehlt sie dort, bleibt sie leer
        for ebene in ("hintergrund", "mittelgrund", "figuren", "vordergrund"):
            pfad = os.path.join(ordner, ebene + ".png")
            if ebene == "figuren" and os.path.exists(os.path.join(ordner, "figuren", "figuren.json")):
                aus["szenen"][name][ebene] = png_figuren(os.path.join(ordner, "figuren"))
            elif os.path.exists(pfad):
                aus["szenen"][name][ebene] = png_ebene(pfad, uhr_teile(ordner) if ebene == "hintergrund" else "")
            else:
                aus["szenen"][name][ebene] = ""
        # Klickzonen (hitboxes.json) und Bildschirmflächen (schirme.json) wandern mit ins Spiel: spiel.js baut
        # daraus Klickfelder und legt auf die Schirme seine Leinwände mit laufenden Kurven — nichts doppelt gepflegt
        for datei, feld in (("hitboxes.json", "zonen"), ("schirme.json", "schirme")):
            pfad = os.path.join(ordner, datei)
            if os.path.exists(pfad):
                with open(pfad, encoding="utf-8") as f:
                    aus["szenen"][name][feld] = json.load(f)
    for wer in ("marlene", "herr_k", "falk"):
        pfad = os.path.join(os.path.dirname(hier), "art", "portraits", wer + ".png")
        aus["portraits"][wer] = png_portrait(pfad) if os.path.exists(pfad) else portrait(wer)
    return aus


if __name__ == "__main__":
    hier = os.path.dirname(os.path.abspath(__file__))
    ziel = os.path.join(os.path.dirname(hier), "bau")
    os.makedirs(ziel, exist_ok=True)
    daten = baue()
    herz, herz_geo = herz_schema()                 # Lehrbild fürs Rätsel „Reizleitung bauen“
    daten["schemata"] = {"herz": herz, "herz_geo": herz_geo}
    with open(os.path.join(ziel, "kunst.json"), "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False)
    groesse = sum(len(v) for s in daten["szenen"].values() for v in s.values())
    print("Szenen:", list(daten["szenen"]), "| Porträts:", list(daten["portraits"]),
          "| SVG gesamt:", round(groesse / 1024), "kB")
