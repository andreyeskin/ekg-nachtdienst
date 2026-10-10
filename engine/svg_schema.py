# -*- coding: utf-8 -*-
"""SVG-Generatoren für Kurs A. Alle Kurven aus modell.kurve / modell.hump."""
import math
from modell import kurve, hump, F, pwelle_mess

INK = '#23272B'; TEAL = '#0E6B66'; MAG = '#B01267'; GRAU = '#8A6E62'; HELL = '#9AA2A8'
SVGSTIL = 'style="width:100%;height:auto;display:block;margin:6px 0 8px"'


def _x(t, dauer, x0=30, x1=744):
    return x0 + t * (x1 - x0) / dauer


def ekg_elemente(ps, qs, dauer=4400, y0=0, base=98, k=46, breit=False, pneg=None, tlag=None,
                 pp_lab=False, pq=None, p_mark=False, raster=True, farbe=INK, pamp=0.2):
    """Gibt SVG-Elemente (ohne <svg>) eines Rhythmusstreifens zurück."""
    b = base + y0
    s = []
    if raster:
        n = int(dauer // 200)
        for i in range(n + 1):
            x = _x(i * 200, dauer)
            s.append(f'<line x1="{F(x)}" y1="{y0+22}" x2="{F(x)}" y2="{b+22}" stroke="#F1DCD4" stroke-width="1"/>')
    pts = []
    t = 0.0
    while t <= dauer:
        v = kurve(t, ps, qs, breit, pneg, tlag, pamp)
        pts.append(f'{F(_x(t, dauer))},{F(b - v * k)}')
        t += 3
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{farbe}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>')
    if p_mark:
        for p in ps:
            s.append(f'<text x="{F(_x(p+45, dauer))}" y="{b-22}" text-anchor="middle" font-size="12" font-weight="700" fill="{TEAL}">P</text>')
    if pp_lab:
        for a, c in zip(ps, ps[1:]):
            xa, xc = _x(a + 45, dauer), _x(c + 45, dauer)
            yb = y0 + 26
            s.append(f'<path d="M{F(xa)},{yb-5} V{yb} H{F(xc)} V{yb-5}" fill="none" stroke="{GRAU}" stroke-width="1.4"/>')
            s.append(f'<text x="{F((xa+xc)/2)}" y="{yb-8}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{GRAU}">{c-a}</text>')
    if pq:
        for p, q in pq:
            xa, xc = _x(p, dauer), _x(q, dauer)
            yb = b + 26
            s.append(f'<path d="M{F(xa)},{yb-5} V{yb} H{F(xc)} V{yb-5}" fill="none" stroke="{MAG}" stroke-width="1.4"/>')
            s.append(f'<text x="{F((xa+xc)/2)}" y="{yb+14}" text-anchor="middle" font-size="12" font-weight="700" fill="{MAG}">{q-p}</text>')
    return ''.join(s)


def streifen(ps, qs, titel='', hoehe=None, **kw):
    h = hoehe or (166 if kw.get('pq') else 130)
    innen = ekg_elemente(ps, qs, **kw)
    t = f'<text x="8" y="{h-6}" font-size="11" fill="{GRAU}">{titel}</text>' if titel else ''
    return f'<svg class="blitz-svg" viewBox="0 0 760 {h}" role="img" aria-label="Rhythmusstreifen">{innen}{t}</svg>'


def leiter(ps, pqs, qs=None, breit=False, dauer=4400, titel='', dissoziiert=False, pq_lab=True):
    """Leiterdiagramm (A / AV / V) über dem zugehörigen Streifen — dieselben Daten."""
    s = [f'<text x="10" y="36" font-size="13" font-weight="800" fill="{GRAU}">A</text>',
         f'<text x="4" y="70" font-size="13" font-weight="800" fill="{GRAU}">AV</text>',
         f'<text x="10" y="106" font-size="13" font-weight="800" fill="{GRAU}">V</text>']
    for y in (20, 44, 92, 112):
        s.append(f'<line x1="28" y1="{y}" x2="748" y2="{y}" stroke="#E4D5CE" stroke-width="1"/>')
    if dissoziiert:
        conducted_q = []
        for p in ps:
            x = _x(p + 20, dauer)
            s.append(f'<line x1="{F(x)}" y1="20" x2="{F(x)}" y2="44" stroke="{TEAL}" stroke-width="3"/>')
            s.append(f'<line x1="{F(x)}" y1="44" x2="{F(x+7)}" y2="58" stroke="{TEAL}" stroke-width="3"/>')
            s.append(f'<line x1="{F(x+1)}" y1="62" x2="{F(x+13)}" y2="56" stroke="{MAG}" stroke-width="3"/>')
        for q in qs:
            x = _x(q + 10, dauer)
            s.append(f'<line x1="{F(x)}" y1="92" x2="{F(x)}" y2="112" stroke="{INK}" stroke-width="3"/>')
            s.append(f'<circle cx="{F(x)}" cy="104" r="5" fill="{MAG}"/>')
        s.append(f'<text x="748" y="128" text-anchor="end" font-size="11.5" fill="{MAG}">● Ersatzzentrum feuert unabhängig</text>')
        qs_eff = qs
        pq_pairs = None
    else:
        qs_eff = []
        pq_pairs = []
        for p, d in zip(ps, pqs):
            x = _x(p + 20, dauer)
            s.append(f'<line x1="{F(x)}" y1="20" x2="{F(x)}" y2="44" stroke="{TEAL}" stroke-width="3"/>')
            if d is None:
                s.append(f'<line x1="{F(x)}" y1="44" x2="{F(x+9)}" y2="62" stroke="{TEAL}" stroke-width="3"/>')
                s.append(f'<line x1="{F(x+2)}" y1="67" x2="{F(x+16)}" y2="59" stroke="{MAG}" stroke-width="3.2"/>')
            else:
                xq = _x(p + d + 10, dauer)
                s.append(f'<line x1="{F(x)}" y1="44" x2="{F(xq)}" y2="92" stroke="{TEAL}" stroke-width="3"/>')
                s.append(f'<line x1="{F(xq)}" y1="92" x2="{F(xq)}" y2="112" stroke="{INK}" stroke-width="3"/>')
                qs_eff.append(p + d)
                pq_pairs.append((p, p + d))
    strip = ekg_elemente(ps, qs_eff, dauer=dauer, y0=110, base=98, k=44, breit=breit,
                         pq=pq_pairs if pq_lab else None, p_mark=True)
    t = f'<text x="10" y="270" font-size="12" font-weight="700" fill="{INK}">{titel}</text>' if titel else ''
    return f'<svg viewBox="0 0 760 276" {SVGSTIL} role="img" aria-label="Leiterdiagramm {titel}">{"".join(s)}{strip}{t}</svg>'


def pwelle_panel(ra, la, v1_neg, x0, titel_ii='II', titel_v1='V1', komponenten=False):
    """Zoom auf eine P-Welle: links Abl. II (Summe RA+LA), rechts V1 (RA positiv, LA negativ)."""
    s = []
    kx, ky = 1.35, 230          # px/ms, px/mV
    base = 120

    def pfad(fn, xs, von=-20.0, bis=200.0):
        pts = []
        t = von
        while t <= bis:
            pts.append(f'{F(xs + (t + 20) * kx)},{F(base - fn(t) * ky)}')
            t += 1
        return ' '.join(pts)
    # Abl. II
    xa = x0
    s.append(f'<line x1="{F(xa)}" y1="{F(base-0.25*ky)}" x2="{F(xa+300)}" y2="{F(base-0.25*ky)}" stroke="{MAG}" stroke-width="1.3" stroke-dasharray="6 5"/>')
    s.append(f'<text x="{F(xa+300)}" y="{F(base-0.25*ky-5)}" text-anchor="end" font-size="11.5" fill="{MAG}">0,25 mV</text>')
    s.append(f'<line x1="{F(xa)}" y1="{base}" x2="{F(xa+300)}" y2="{base}" stroke="{HELL}" stroke-width="1"/>')
    xr0, xr1 = xa + 20 * kx, xa + 120 * kx
    s.append(f'<path d="M{F(xr0)},{base+22} V{base+28} H{F(xr1)} V{base+22}" fill="none" stroke="{GRAU}" stroke-width="1.4"/>')
    s.append(f'<text x="{F((xr0+xr1)/2)}" y="{base+43}" text-anchor="middle" font-size="11.5" fill="{GRAU}">100 msek</text>')
    if komponenten:
        s.append(f'<polyline points="{pfad(lambda t: hump(t, *ra), xa, ra[0], ra[0]+ra[1])}" fill="none" stroke="#3B7BBF" stroke-width="2" stroke-dasharray="5 4"/>')
        s.append(f'<polyline points="{pfad(lambda t: hump(t, *la), xa, la[0], la[0]+la[1])}" fill="none" stroke="{MAG}" stroke-width="2" stroke-dasharray="5 4"/>')
    s.append(f'<polyline points="{pfad(lambda t: hump(t, *ra) + hump(t, *la), xa)}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<text x="{F(xa)}" y="22" font-size="14" font-weight="800">{titel_ii}</text>')
    # V1
    xb = x0 + 330
    s.append(f'<line x1="{F(xb)}" y1="{base}" x2="{F(xb+230)}" y2="{base}" stroke="{HELL}" stroke-width="1"/>')
    s.append(f'<polyline points="{pfad(lambda t: 0.8*hump(t, *ra) - v1_neg*hump(t, *la), xb)}" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    s.append(f'<text x="{F(xb)}" y="22" font-size="14" font-weight="800">{titel_v1}</text>')
    return ''.join(s)


def pwelle_svg(ra, la, v1_neg, komponenten=False, unterschrift=''):
    u = f'<text x="10" y="196" font-size="12" font-weight="700" fill="{INK}">{unterschrift}</text>' if unterschrift else ''
    h = 204 if unterschrift else 180
    return (f'<svg class="blitz-svg" viewBox="0 0 760 {h}" role="img" aria-label="P-Welle in II und V1">'
            f'{pwelle_panel(ra, la, v1_neg, 30, komponenten=komponenten)}{u}</svg>')
