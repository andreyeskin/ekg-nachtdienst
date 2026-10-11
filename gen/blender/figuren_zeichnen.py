"""Figuren der Räume in ligne claire — zwei Schritte, getrennt, damit der teure nur einmal läuft.

(a) teuer, einmal je Figur (Blender + fal.ai Flux Kontext):
    python3 figuren_zeichnen.py vorlage aufnahme              # Blockout-Ausschnitte (4x Bühnenmaßstab, grüner Grund)
                                                              #   -> bau/blender/figuren/vorlage_<name>.png + art/figuren_quelle/<name>.json
    python3 figuren_zeichnen.py malen marlene --seed 7         # Kontext -> bau/blender/figuren/ki_marlene_s7.png, _frei.png (freigestellt), _pruef.png
    python3 figuren_zeichnen.py malen marlene --seed 7 --uebernehmen   # geprüft -> art/figuren_quelle/marlene.png (volle Auflösung, Alpha)
    Optionen: --portrait (Endpunkt kontext/max/multi, das Porträt aus art/portraits/ als zweites Bild — gleiche Person),
              --stil DATEI (Stilphrase, Standard stil/figur_<name>.txt), --guidance 3.5, --birefnet (Freistellen über fal
              statt Farbschlüssel), --dry-run.

(b) billig, beliebig oft, ohne fal (Blender nur für Masken: Tiefe des Raums, Tiefe der Figur, Sonne — je 4–16 Proben):
    python3 figuren_zeichnen.py einsetzen aufnahme [--skala 1]
      -> art/szenen/aufnahme/figuren/{marlene,herrk}.png + figuren.json, Klickzone der Figur in hitboxes.json,
         Vorschau bau/blender/figuren/aufnahme_vorschau.png. Verdeckung durch den Raum (Tresen vor Marlene, Stuhl bei
         Herrn K) aus dem Tiefenvergleich, Sonnenlicht und Lichtfarbe aus komposit.EINSTELLUNG des Raums, auf Bühnengröße
         (--skala 2: doppelte Auflösung für Retina), 160 Farben, Alpha getrennt.

Porträts (Brustbilder, 400x440, art/portraits/):
    python3 figuren_zeichnen.py portrait marlene --seed 3                       # Blockout (ebenen_figuren.py portraits) -> Kontext
    python3 figuren_zeichnen.py portrait marlene --seed 3 --bearbeiten --stil stil/portrait_marlene_dutt.txt
                                                                               # bestehendes Porträt umzeichnen (Gesicht bleibt)
    jeweils -> bau/blender/figuren/portrait_<wer>_s<seed>.png; --uebernehmen -> art/portraits/<wer>.png (400x440, 160 Farben)

Figurenorte: figuren.PLATZ (eine Stelle je Figur). Raum und Figuren kommen aus ebenen_figuren.aufbau(raum).
Threads: BLENDER_THREADS=2 begrenzt Cycles (wenn nebenan ein zweiter Render läuft). Schlüssel für fal: FAL_KEY oder
der Proxy der Cloud-Umgebung (wie in malen.py).
"""
import argparse
import datetime
import json
import math
import os
import shutil
import sys
import time
import urllib.request

import numpy as np
from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, HIER)
OUT = os.path.join(WURZEL, "bau", "blender", "figuren") + os.sep; os.makedirs(OUT, exist_ok=True)
QUELLE = os.path.join(WURZEL, "art", "figuren_quelle") + os.sep
PORTRAITS = os.path.join(WURZEL, "art", "portraits") + os.sep
STIL = os.path.join(HIER, "stil") + os.sep

SKALA = 4                                  # Vorlage und Masken: Vielfaches des Bühnenmaßstabs (1600x900)
GRUEN = "#2FBF3A"                          # flacher Grund der Vorlage; kommt in keiner Figur vor (Farbschlüssel)
RAND = 0.10                                # Rand um die Figur in der Vorlage (Anteil der Figurgröße)
SEITEN = {"9:21": 9 / 21, "9:16": 9 / 16, "2:3": 2 / 3, "3:4": 3 / 4, "1:1": 1.0, "4:3": 4 / 3, "3:2": 1.5, "16:9": 16 / 9}
STUFE = 1440 / 1600; MIN_ZIEL = int(math.ceil(44 / STUFE))       # Klickzone: 44 CSS-px bei 1440 px Bühnenbreite
PORTRAIT_NAME = {"marlene": "marlene", "herrk": "herr_k", "falk": "falk"}   # Figurname -> Datei in art/portraits/

hexc = lambda s: tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))
def hexa(s): return np.array(hexc(s), np.float32)


# ================================================================== Bildhilfen (ohne Blender)
def lade(p, alpha=False):
    return np.asarray(Image.open(p).convert("RGBA" if alpha else "RGB")).astype(np.float32) / 255

def luma(a): return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

def bild(a, modus="RGBA"): return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), modus)

def weich(m, r):
    if r <= 0: return m
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255

def freistellen(rgb, grund=GRUEN, t0=0.10, t1=0.30):
    """Farbschlüssel: Abstand zur Grundfarbe -> Alpha (weiche Rampe), Farbe am Rand vom Grün befreit."""
    g = hexa(grund)
    d = np.sqrt(((rgb - g) ** 2).sum(-1))
    a = np.clip((d - t0) / (t1 - t0), 0, 1)
    a = a * a * (3 - 2 * a)
    col = rgb.copy(); m = a > 0.02
    col[m] = (rgb[m] - (1 - a[m])[:, None] * g) / a[m][:, None]       # Vordergrundfarbe aus der Mischung lösen
    rand = (a > 0.02) & (a < 0.98)                                       # Restgrün nur an der Kante dämpfen
    gr = col[..., 1]; mx = np.maximum(col[..., 0], col[..., 2])
    gr = np.where(rand, np.minimum(gr, mx + 0.02), gr); col[..., 1] = gr
    # vereinzelte Reste im Grund (Pixel mit kleinem Alpha ohne feste Nachbarn) fallen weg
    fest = np.asarray(Image.fromarray((a > 0.6).astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))).astype(bool)
    a = np.where(fest, a, 0)
    return np.concatenate([np.clip(col, 0, 1), a[..., None]], axis=-1)

def einpassen(rgba, groesse, rand=0.006):
    """Quellbild auf die Vorlagengröße: Höhe passend, Seitenverhältnis gehalten (Kontext liefert z. B. 752x1392 statt
    9:16), Breite mittig beschnitten oder aufgefüllt; ein schmaler Randstreifen wird transparent (Streupixel)."""
    h0, w0 = rgba.shape[:2]; r = max(1, int(rand * max(h0, w0)))
    rgba = rgba.copy(); rgba[:r, :, 3] = 0; rgba[-r:, :, 3] = 0; rgba[:, :r, 3] = 0; rgba[:, -r:, 3] = 0
    gw, gh = groesse; nw = int(round(w0 * gh / h0))
    s = vormultipliziert_skalieren(rgba, (nw, gh))
    out = np.zeros((gh, gw, 4), np.float32)
    if nw >= gw: o = (nw - gw) // 2; out[:] = s[:, o:o + gw]
    else: o = (gw - nw) // 2; out[:, o:o + nw] = s
    return out

def vormultipliziert_skalieren(rgba, groesse, resample=Image.LANCZOS):
    """Skalieren ohne dunkle Säume: RGB mit Alpha vormultipliziert, danach wieder gelöst."""
    a = rgba[..., 3:4]; pm = np.concatenate([rgba[..., :3] * a, a], axis=-1)
    kan = [Image.fromarray((np.clip(pm[..., i], 0, 1) * 255 + 0.5).astype(np.uint8)).resize(groesse, resample) for i in range(4)]
    out = np.stack([np.asarray(k).astype(np.float32) / 255 for k in kan], axis=-1)
    a2 = out[..., 3:4]; col = np.where(a2 > 1e-3, out[..., :3] / np.maximum(a2, 1e-3), 0)
    return np.concatenate([np.clip(col, 0, 1), np.clip(a2, 0, 1)], axis=-1)

def affin(rgba, s, dx, dy):
    """Ähnlichkeitsabbildung (Maßstab s um den Ursprung, dann Verschiebung dx, dy) — vormultipliziert."""
    h, w = rgba.shape[:2]; a = rgba[..., 3:4]; pm = np.concatenate([rgba[..., :3] * a, a], axis=-1)
    kan = []
    for i in range(4):
        im = Image.fromarray((np.clip(pm[..., i], 0, 1) * 255 + 0.5).astype(np.uint8))
        kan.append(im.transform((w, h), Image.AFFINE, (1 / s, 0, -dx / s, 0, 1 / s, -dy / s), resample=Image.BICUBIC))
    out = np.stack([np.asarray(k).astype(np.float32) / 255 for k in kan], axis=-1)
    a2 = out[..., 3:4]; col = np.where(a2 > 1e-3, out[..., :3] / np.maximum(a2, 1e-3), 0)
    return np.concatenate([np.clip(col, 0, 1), np.clip(a2, 0, 1)], axis=-1)

def naechste_fuellung(wert, bekannt, schritte):
    """Füllt unbekannte Pixel mit dem Wert des (etwa) nächsten bekannten — Schachbrett-Ausbreitung."""
    w = wert.copy(); k = bekannt.copy()
    for _ in range(schritte):
        if k.all(): break
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            ks = np.roll(k, (dy, dx), (0, 1)); ws = np.roll(w, (dy, dx), (0, 1))
            neu = ks & ~k; w[neu] = ws[neu]; k |= ks
    return w, k

def dilatiere(m, r):
    if r <= 0: return m
    im = Image.fromarray((m > 0.5).astype(np.uint8) * 255)
    k = 2 * int(r) + 1
    return np.asarray(im.filter(ImageFilter.MaxFilter(k))).astype(np.float32) / 255

def speichern_quantisiert(img, pfad, farben=160):
    """RGB auf `farben` Farben, Alpha bleibt als eigener 8-Bit-Kanal (wie die Raumebenen: flache Flächen, weiche Kante)."""
    rgb = np.asarray(img.convert("RGB")).copy(); a = img.getchannel("A")
    rgb[np.asarray(a) == 0] = (128, 128, 128)                 # Unsichtbares frisst keine Palette
    q = Image.fromarray(rgb).quantize(colors=farben, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    q.putalpha(a); os.makedirs(os.path.dirname(pfad), exist_ok=True); q.save(pfad, optimize=True)
    print("saved", os.path.relpath(pfad, WURZEL), os.path.getsize(pfad) // 1024, "kB", q.size)

def seitenverhaeltnis(w, h):
    """Nächstes erlaubtes Kontext-Seitenverhältnis (im Logarithmus) zum Kasten w x h."""
    return min(SEITEN, key=lambda k: abs(math.log(SEITEN[k]) - math.log(w / h)))


# ================================================================== fal.ai
def fal_laden(dry):
    key = os.environ.get("FAL_KEY")
    if not key and os.environ.get("FAL_PROXY_AUTH", "1") == "1" and not dry:
        os.environ["FAL_KEY"] = "proxy-injected"          # der Proxy der Cloud-Umgebung ersetzt den Schlüssel
    try:
        import fal_client
    except ImportError:
        print("pip install fal-client", file=sys.stderr); sys.exit(2)
    return fal_client

def fal_bild(endpunkt, payload, ziel, dry=False):
    """Ruft einen fal-Endpunkt, lädt das erste Bild nach `ziel`, gibt die Antwort zurück."""
    fc = fal_laden(dry)
    if dry:
        shown = {k: ("<data-uri>" if isinstance(v, str) and v.startswith("data:") else
                     (["<data-uri>"] * len(v) if isinstance(v, list) else v)) for k, v in payload.items()}
        print("DRY RUN", endpunkt); print(json.dumps(shown, ensure_ascii=False, indent=1)); return None
    t = time.time()
    antwort = fc.subscribe(endpunkt, arguments=payload, with_logs=False)
    bilder = antwort.get("images") or ([antwort["image"]] if antwort.get("image") else [])
    if not bilder:
        print("fal.ai: kein Bild in der Antwort:", json.dumps(antwort)[:600]); sys.exit(1)
    urllib.request.urlretrieve(bilder[0]["url"], ziel)
    print(f"fal {endpunkt}: saved {os.path.relpath(ziel, WURZEL)} ({bilder[0].get('width')}x{bilder[0].get('height')}) "
          f"seed={antwort.get('seed')} {time.time() - t:.0f}s")
    return antwort

def stil_text(pfad):
    return open(pfad, encoding="utf-8").read().strip()


# ================================================================== Blender-Teil (nur vorlage / einsetzen)
def blender_laden():
    global bpy, Vector, ef, figuren
    import bpy
    from mathutils import Vector
    _argv = sys.argv; sys.argv = ["x", "modul"]           # ebenen_figuren liest seinen Modus aus argv
    try:
        import ebenen_figuren as ef
    finally:
        sys.argv = _argv
    import figuren

def rahmen(kasten, S):
    """Render-Rahmen: nur der Kasten (Bühnen-px) bei S-facher Auflösung."""
    sc = bpy.context.scene; x0, y0, x1, y1 = kasten
    sc.render.resolution_x, sc.render.resolution_y = 1600 * S, 900 * S; sc.render.resolution_percentage = 100
    sc.render.use_border = True; sc.render.use_crop_to_border = True
    sc.render.border_min_x, sc.render.border_max_x = x0 / 1600, x1 / 1600
    sc.render.border_min_y, sc.render.border_max_y = 1 - y1 / 900, 1 - y0 / 900
    ef.LINIE = 1.2 * S

def rahmen_aus():
    sc = bpy.context.scene; sc.render.use_border = False; sc.render.use_crop_to_border = False
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900; ef.LINIE = 1.5

def auf_groesse(a, groesse):
    """Render-Ausschnitte können um ein Pixel abweichen — auf die Sollgröße bringen."""
    h, w = a.shape[:2]
    if (w, h) == groesse: return a
    return vormultipliziert_skalieren(a, groesse) if a.shape[-1] == 4 else \
        np.asarray(Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).resize(groesse, Image.LANCZOS)).astype(np.float32) / 255

def pass_tiefe(pfad, sichtbar, nah=4.0, fern=10.0):
    """Tiefe entlang der Kameraachse als Grauwert (nah..fern -> 0..1), 16 Bit; wo nichts ist, Weiß (= fern)."""
    sc = bpy.context.scene
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt, out, b = ef._knoten(m)
        if out is None: continue
        em = nt.nodes.get("ebene_em") or nt.nodes.new("ShaderNodeEmission"); em.name = "ebene_em"
        cd = nt.nodes.get("tiefe_cd") or nt.nodes.new("ShaderNodeCameraData"); cd.name = "tiefe_cd"
        mr = nt.nodes.get("tiefe_mr") or nt.nodes.new("ShaderNodeMapRange"); mr.name = "tiefe_mr"
        mr.inputs["From Min"].default_value = nah; mr.inputs["From Max"].default_value = fern
        nt.links.new(cd.outputs["View Z Depth"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], em.inputs["Color"])
        em.inputs["Strength"].default_value = 1.0
        for l in list(out.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    ef.lichter(lambda o: False); ef.welt((1, 1, 1), 1.0); sc.cycles.max_bounces = 0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        o.is_holdout = False; o.hide_render = not sichtbar(o)
    ef.freestyle(False)
    sc.view_settings.view_transform = 'Raw'; sc.render.image_settings.color_depth = '16'
    try:                                                   # wie ef.render, aber einkanalig 16 Bit
        sc.cycles.samples = 4; sc.cycles.use_denoising = False; sc.render.filepath = pfad
        sc.render.film_transparent = False; sc.render.image_settings.color_mode = 'BW'
        t = time.time(); bpy.ops.render.render(write_still=True); print(f"RENDER {os.path.basename(pfad)} {time.time() - t:.1f}s", flush=True)
    finally:
        sc.view_settings.view_transform = 'Standard'; sc.render.image_settings.color_depth = '8'; sc.render.image_settings.color_mode = 'RGB'
        for m in bpy.data.materials:                      # Farb-Eingang wieder frei für material_flach
            if not m.use_nodes: continue
            em = m.node_tree.nodes.get("ebene_em")
            if em:
                for l in list(em.inputs["Color"].links): m.node_tree.links.remove(l)

def tiefe_lesen(pfad):
    """-> Tiefe 0..1 und Maske „hier ist Geometrie“ (nicht am fernen Ende)."""
    im = Image.open(pfad); a = np.asarray(im)
    skala = 65535.0 if a.dtype == np.uint16 else 255.0
    a = a.astype(np.float32) / skala
    if a.ndim == 3: a = a[..., 0]
    return a, a < 0.995

def fig_sichtbar(name):
    return lambda o: (ef.fig_name(o) == name) if ef.ist_fig(o) else False


# ================================================================== vorlage
def vorlage(raum, nur=None, neu=False):
    blender_laden(); A = ef.aufbau(raum); figs = A["figs"]; koerper = bpy.data.collections["figuren"]
    for name, fig in figs.items():
        if nur and name not in nur: continue
        alt = QUELLE + f"{name}.json"
        if os.path.exists(alt) and not neu:
            try: schon = json.load(open(alt, encoding="utf-8")).get("datei")
            except Exception: schon = None
            if schon:   # Quellbild schon übernommen: sein Ausschnitt muss bleiben (sonst passt das Bild nicht mehr) — --neu erzwingt
                print("VORLAGE", name, "übersprungen: Quelle vorhanden, Ausschnitt bleibt (--neu zum Erneuern)"); continue
        # 1. Kasten der sichtbaren Figur (1x, Raum als Holdout), Rand, erlaubtes Seitenverhältnis
        ef.pass_flach(OUT + f"{name}_kasten.png", lambda o, n=name: (ef.fig_name(o) == n) if ef.ist_fig(o) else ("holdout" if A["raum_sichtbar"](o) else False))
        a = lade(OUT + f"{name}_kasten.png", True)[..., 3]; ys, xs = np.nonzero(a > 0.3)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1; w, h = x1 - x0, y1 - y0
        verdeckt = bool(A["kontext"].get(name))            # Raumobjekt vor/unter der Figur: Vorlage zeigt es mit
        r = RAND * max(w, h)
        x0, x1 = x0 - r, x1 + r; y0 -= r; y1 += r * (2.6 if name == "marlene" else 1.0)   # Marlene: Tresen unter der Kante zeigen
        sv = seitenverhaeltnis(x1 - x0, y1 - y0); ziel = SEITEN[sv]
        w, h = x1 - x0, y1 - y0
        if w / h < ziel: d = h * ziel - w; x0 -= d / 2; x1 += d / 2
        else: d = w / ziel - h; y0 -= d / 2; y1 += d / 2
        x0, y0 = max(0, int(round(x0))), max(0, int(round(y0))); x1, y1 = min(1600, int(round(x1))), min(900, int(round(y1)))
        kasten = [x0, y0, x1, y1]
        # 2. Vorlage: Figur + Kontextobjekte, flache Farben, Linie — bei SKALA auf grünem Grund
        kontext = set(A["kontext"].get(name, []))
        rahmen(kasten, SKALA)
        sicht = lambda o, n=name, k=kontext: (ef.fig_name(o) == n) if ef.ist_fig(o) else (o.name in k)
        ef.pass_flach(OUT + f"{name}_vorlage_flat.png", sicht)
        gelinkt = []
        eigene = [o.name for o in bpy.data.objects if o.type == 'MESH' and ef.ist_fig(o) and ef.fig_name(o) == name]
        for n in list(kontext) + eigene:                   # Linie (Freestyle) nur für die Sammlung "figuren": Kontext und Raum-Figuren (Tüte) dazulinken
            o = bpy.data.objects[n]
            if o.name not in koerper.objects: koerper.objects.link(o); gelinkt.append(o)
        try: ef.pass_linien(OUT + f"{name}_vorlage_lines.png", sicht, koerper)
        finally:
            for o in gelinkt: koerper.objects.unlink(o)
        rahmen_aus()
        groesse = ((x1 - x0) * SKALA, (y1 - y0) * SKALA)
        flach = auf_groesse(lade(OUT + f"{name}_vorlage_flat.png", True), groesse)
        linien = auf_groesse(lade(OUT + f"{name}_vorlage_lines.png"), groesse)
        ink = np.clip((1 - luma(linien)) * 1.3, 0, 1)[..., None]
        col = hexa(GRUEN) * (1 - flach[..., 3:4]) + flach[..., :3] * flach[..., 3:4]
        col = col * (1 - ink) + ef.INK * ink
        pfad = OUT + f"vorlage_{name}.png"; bild(col, "RGB").save(pfad)
        meta = {"raum": raum, "kasten": kasten, "skala": SKALA, "grund": GRUEN, "seitenverhaeltnis": sv,
                "verdeckt": verdeckt, "art": "ding" if name in A.get("dinge", set()) else "figur",
                "vorlage": os.path.relpath(pfad, WURZEL), "datei": None}
        if os.path.exists(alt):                             # Herkunft eines schon übernommenen Bildes behalten
            try: meta.update({k: v for k, v in json.load(open(alt, encoding="utf-8")).items() if k in ("datei", "seed", "endpunkt", "stil", "prompt", "datum")})
            except Exception: pass
        os.makedirs(QUELLE, exist_ok=True); json.dump(meta, open(alt, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("VORLAGE", name, kasten, sv, groesse, "->", os.path.relpath(pfad, WURZEL))


# ================================================================== malen
def malen(name, a):
    meta = json.load(open(QUELLE + f"{name}.json", encoding="utf-8"))
    vor = os.path.join(WURZEL, meta["vorlage"])
    if not os.path.exists(vor): sys.exit(f"Vorlage fehlt: {vor} — erst `vorlage {meta['raum']}`")
    stil = a.stil or (STIL + f"figur_{PORTRAIT_NAME.get(name, name)}.txt")
    rahmen_datei = STIL + ("figur_rahmen_ding.txt" if meta.get("art") == "ding" else "figur_rahmen.txt")
    prompt = stil_text(rahmen_datei) + " " + stil_text(stil)
    fc = fal_laden(a.dry_run)
    portrait_pfad = PORTRAITS + f"{PORTRAIT_NAME.get(name, name)}.png"
    if a.bearbeiten:                                       # fertige Figur nachbessern (z. B. ein Requisit): Quelle = Kontext-Bild
        quelle = a.quelle or vor
        if not a.stil: sys.exit("--bearbeiten braucht --stil (Datei mit der Änderung)")
        prompt = stil_text(stil) + " Keep everything else exactly identical, including the flat uniform bright green background; no text, no letters, no scribbles."
        if a.portrait:                                     # mit Porträt als Identitätsbild (Gesicht nachzeichnen)
            endpunkt = "fal-ai/flux-pro/kontext/max/multi"
            payload = {"prompt": prompt, "image_urls": None if a.dry_run else [fc.encode_file(quelle), fc.encode_file(portrait_pfad)]}
        else:
            endpunkt = "fal-ai/flux-pro/kontext"
            payload = {"prompt": prompt, "image_url": None if a.dry_run else fc.encode_file(quelle)}
    elif a.portrait:
        endpunkt = "fal-ai/flux-pro/kontext/max/multi"
        prompt = ("The first image is a plain 3D mannequin; the second image is the finished portrait of the same person. "
                  "Draw the mannequin as a full figure of exactly that person (same face, hair, glasses, skin and clothing colours). " + prompt)
        payload = {"prompt": prompt, "image_urls": None if a.dry_run else [fc.encode_file(vor), fc.encode_file(portrait_pfad)]}
    else:
        endpunkt = "fal-ai/flux-pro/kontext"
        payload = {"prompt": prompt, "image_url": None if a.dry_run else fc.encode_file(vor)}
    payload.update({"seed": a.seed, "guidance_scale": a.guidance, "output_format": "png", "aspect_ratio": meta["seitenverhaeltnis"],
                    "safety_tolerance": "2"})
    kennung = f"ki_{name}_s{a.seed}" + ("p" if a.portrait else "") + ("e" if a.bearbeiten else "")
    roh = OUT + kennung + ".png"
    if a.aus:                                              # schon geholtes Bild: nur freistellen/übernehmen (kein fal)
        roh = os.path.join(WURZEL, a.aus) if not os.path.isabs(a.aus) else a.aus; kennung = os.path.splitext(os.path.basename(roh))[0]
    elif fal_bild(endpunkt, payload, roh, a.dry_run) is None: return
    rgb = lade(roh)
    if a.birefnet:
        fal_bild("fal-ai/birefnet/v2", {"image_url": fc.encode_file(roh), "model": "General Use (Light)", "operating_resolution": "1024x1024",
                                        "output_format": "png", "refine_foreground": True}, OUT + kennung + "_frei.png")
        frei = lade(OUT + kennung + "_frei.png", True)
    else:
        frei = freistellen(rgb, meta["grund"])
    bild(frei).save(OUT + kennung + "_frei.png")
    # Prüfbild: Vorlage | Kontext | freigestellt auf Sand
    v = Image.open(vor).convert("RGB").resize(bild(rgb, "RGB").size); f = bild(frei)
    sand = Image.new("RGBA", f.size, (239, 230, 211, 255)); sand.alpha_composite(f)
    pr = Image.new("RGB", (v.width * 3 + 20, v.height), (255, 255, 255))
    pr.paste(v, (0, 0)); pr.paste(bild(rgb, "RGB"), (v.width + 10, 0)); pr.paste(sand.convert("RGB"), (v.width * 2 + 20, 0))
    pr.save(OUT + kennung + "_pruef.png"); print("PRUEF", os.path.relpath(OUT + kennung + "_pruef.png", WURZEL))
    if a.uebernehmen:
        shutil.copyfile(OUT + kennung + "_frei.png", QUELLE + f"{name}.png")
        meta.update({"datei": f"{name}.png", "seed": a.seed, "endpunkt": endpunkt, "stil": os.path.relpath(stil, WURZEL),
                     "prompt": prompt, "datum": datetime.date.today().isoformat(), "freistellen": "birefnet" if a.birefnet else "farbschluessel",
                     "roh": os.path.relpath(roh, WURZEL), "bearbeitet_aus": (os.path.relpath(a.quelle, WURZEL) if a.bearbeiten and a.quelle else None)})
        json.dump(meta, open(QUELLE + f"{name}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("ÜBERNOMMEN ->", os.path.relpath(QUELLE + f"{name}.png", WURZEL))


# ================================================================== einsetzen
def einsetzen(raum, skala_aus=1):
    blender_laden(); A = ef.aufbau(raum); figs = A["figs"]
    try:
        import komposit; e = komposit.EINSTELLUNG.get(raum, komposit.STANDARD)
    except Exception:
        e = dict(licht="#FFF6DC", anteil=0.32, schwelle=0.35, weich=0.7)
    szene_dir = os.path.join(WURZEL, "art", "szenen", raum) + os.sep
    hit = json.load(open(szene_dir + "hitboxes.json", encoding="utf-8"))
    platz = {}
    for name, fig in figs.items():
        mp = QUELLE + f"{name}.json"
        if not (os.path.exists(mp) and os.path.exists(QUELLE + f"{name}.png")):
            print("KEINE QUELLE für", name, "— übersprungen"); continue
        meta = json.load(open(mp, encoding="utf-8")); S = meta["skala"]; x0, y0, x1, y1 = meta["kasten"]
        groesse = ((x1 - x0) * S, (y1 - y0) * S)
        rahmen(meta["kasten"], S)
        verd = (A.get("verdecker") or {}).get(name)          # None: jedes Raumobjekt; Liste: nur diese
        pass_tiefe(OUT + f"{name}_tiefe_raum.png", lambda o, v=verd: False if ef.ist_fig(o) else (A["raum_sichtbar"](o) and (v is None or o.name in v)))
        pass_tiefe(OUT + f"{name}_tiefe_fig.png", fig_sichtbar(name))
        ef.pass_flach(OUT + f"{name}_frei.png", fig_sichtbar(name))            # Blockout-Alpha: Ausrichtung, Umgriff
        ef.pass_sonne(OUT + f"{name}_sonne.png", lambda o, n=name: (ef.fig_name(o) == n) if ef.ist_fig(o) else A["sonne_sichtbar"](o),
                      stellen=A["sonne_stellen"])
        rahmen_aus()
        # --- Masken
        zr, kr = tiefe_lesen(OUT + f"{name}_tiefe_raum.png"); zf, kf = tiefe_lesen(OUT + f"{name}_tiefe_fig.png")
        zr = auf_groesse(zr[..., None], groesse)[..., 0]; kr = auf_groesse(kr.astype(np.float32)[..., None], groesse)[..., 0] > 0.5
        zf = auf_groesse(zf[..., None], groesse)[..., 0]; kf = auf_groesse(kf.astype(np.float32)[..., None], groesse)[..., 0] > 0.5
        frei_a = auf_groesse(lade(OUT + f"{name}_frei.png", True), groesse)[..., 3]
        fy = np.nonzero(frei_a.max(1) > 0.5)[0]; fig_h = (fy.max() - fy.min() + 1) if len(fy) else groesse[1]
        umgriff = max(48, int(0.12 * fig_h))               # so weit darf die gezeichnete Figur über den Blockout hinaus (Ärmel, Mantel)
        kf = np.asarray(Image.fromarray(kf.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(5))) > 127   # Kantenpixel (Tiefe mit dem fernen Grund gemischt) nicht ausbreiten
        zf_voll, _ = naechste_fuellung(zf, kf, umgriff + 4)
        verdeckt = kr & (zr < zf_voll - 0.004)             # Raum liegt vor der Figur (4 mm je 0,001 bei nah..fern = 6 m)
        sichtbar = 1 - dilatiere(verdeckt.astype(np.float32), 0)
        frei_a = auf_groesse(lade(OUT + f"{name}_frei.png", True), groesse)[..., 3]
        zone = dilatiere(frei_a, umgriff)                  # Figur ± Umgriff: nichts, was Kontext dazuerfand (Stuhl, Schatten)
        if len(fy): zone[fy.max() + int(0.02 * fig_h) + 1:, :] = 0   # unter der Fußlinie des Blockouts nichts (Bodenschatten)
        if os.environ.get("FIGUREN_DEBUG"):
            bild(np.stack([verdeckt, zone, kf], -1).astype(np.float32), "RGB").save(OUT + f"{name}_debug_masken.png")
        # --- Quellbild: auf Vorlagengröße (Seitenverhältnis halten), Randstreifen weg, am Blockout ausrichten (Kopf oben, Fußlinie)
        q = einpassen(lade(QUELLE + f"{name}.png", True), groesse)
        q = ausrichten(q, frei_a, voll=not meta.get("verdeckt"))
        alpha = q[..., 3] * zone * sichtbar
        unten = (A["unten"] or {}).get(name, 0) * S
        if unten:                                          # Auslauf unter die Tresenkante: die Atem-Animation zeigt sonst eine Kante
            a = alpha.copy()
            for k in range(1, unten + 1):
                v = np.zeros_like(alpha); v[k:] = alpha[:-k] * (1 - k / (unten + 1)); a = np.maximum(a, v)
            alpha = np.minimum(a, q[..., 3] * zone)
        # --- Raumlicht: Sonnenfleck wie komposit.farbe (Schwelle, Weichheit, Lichtfarbe, Anteil des Raums)
        ls = luma(auf_groesse(lade(OUT + f"{name}_sonne.png"), groesse))
        licht = np.clip((ls - e["schwelle"]) / 0.08 + 0.5, 0, 1)
        licht = np.asarray(Image.fromarray((licht * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))).astype(np.float32) / 255
        licht = weich(licht, e["weich"] * S)[..., None] * e["anteil"]
        col = q[..., :3] * (1 - licht) + hexa(e["licht"]) * licht
        fertig = np.concatenate([col, alpha[..., None]], axis=-1)
        # --- auf Bühnengröße, beschneiden, speichern
        klein = vormultipliziert_skalieren(fertig, ((x1 - x0) * skala_aus, (y1 - y0) * skala_aus))
        ka = klein[..., 3]; ys, xs = np.nonzero(ka > 8 / 255)
        if len(ys) == 0: print("LEER", name); continue
        cx0, cy0, cx1, cy1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        img = bild(klein[cy0:cy1, cx0:cx1])
        speichern_quantisiert(img, szene_dir + f"figuren/{name}.png")
        ef.silhouette(img, OUT + f"{name}_silhouette.png", 120)
        bx, by = x0 + cx0 / skala_aus, y0 + cy0 / skala_aus
        bw, bh = (cx1 - cx0) / skala_aus, (cy1 - cy0) / skala_aus
        rund = (lambda v: int(round(v))) if skala_aus == 1 else (lambda v: round(v, 1))
        platz[name] = {"datei": f"{name}.png", "x": rund(bx), "y": rund(by), "breite": rund(bw), "hoehe": rund(bh)}
        if A["klasse"].get(name, "atmet"): platz[name]["klasse"] = A["klasse"].get(name, "atmet")   # Gegenstände atmen nicht
        # --- Klickzone: sichtbare Figur ∪ bestehende Zone, mindestens 44 CSS-px
        k = [int(bx), int(by), int(math.ceil(bx + bw)), int(math.ceil(by + bh))]
        alt = hit.get(name, k)
        r = [min(alt[0], k[0]), min(alt[1], k[1]), max(alt[2], k[2]), max(alt[3], k[3])]
        for i in (0, 1):
            if r[i + 2] - r[i] < MIN_ZIEL:
                m = (r[i] + r[i + 2]) // 2; r[i], r[i + 2] = m - MIN_ZIEL // 2, m + MIN_ZIEL // 2
        hit[name] = [max(0, r[0]), max(0, r[1]), min(1600, r[2]), min(900, r[3])]
        andere = (A.get("getrennt") or {}).get(name)       # z. B. Tüte neben Herrn K: Zonen dürfen sich nicht überlappen
        if andere in hit:
            z, w = hit[name], hit[andere]
            if z[0] < w[2] and w[0] < z[2] and z[1] < w[3] and w[1] < z[3]:
                if z[0] < w[0]: z[2] = min(z[2], w[0] - 1)   # links daneben: rechte Kante vor der anderen Zone
                else: z[0] = max(z[0], w[2] + 1)
                if z[2] - z[0] < MIN_ZIEL: z[0] = max(0, z[2] - MIN_ZIEL)
        print("FIGUR", name, platz[name], "| Klickzone", hit[name])
    if not platz: sys.exit("nichts eingesetzt")
    os.makedirs(szene_dir + "figuren", exist_ok=True)
    json.dump(platz, open(szene_dir + "figuren/figuren.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(hit, open(szene_dir + "hitboxes.json", "w", encoding="utf-8"), indent=1)
    try:    # Vorschau: Raumebenen + Figuren (nur zur Kontrolle)
        vor = Image.open(szene_dir + "hintergrund.png").convert("RGBA"); vor.alpha_composite(Image.open(szene_dir + "mittelgrund.png").convert("RGBA"))
        for name, p in platz.items():
            f = Image.open(szene_dir + f"figuren/{name}.png").convert("RGBA")
            if skala_aus != 1: f = f.resize((int(round(p["breite"])), int(round(p["hoehe"]))), Image.LANCZOS)
            vor.alpha_composite(f, (int(round(p["x"])), int(round(p["y"]))))
        vor.save(OUT + f"{raum}_vorschau.png"); print("saved", os.path.relpath(OUT + f"{raum}_vorschau.png", WURZEL))
    except Exception as ex:
        print("keine Vorschau:", ex)


def zeilen(m):
    """Erste und letzte Zeile mit echtem Inhalt (mindestens 0,4 % der Breite) — einzelne Streupixel am Bildrand
    (Kontext malt dort gern Reste) zählen nicht, sonst stimmt die Höhe nicht und die Füße schweben."""
    n = m.sum(1); z = np.nonzero(n >= max(4, int(0.004 * m.shape[1])))[0]
    return (int(z.min()), int(z.max())) if len(z) else (None, None)

def ausrichten(q, ref, voll):
    """Richtet das KI-Bild am Blockout aus: Kopfoberkante und Kopfmitte decken sich; ist die Figur ganz zu sehen,
    auch die Höhe (Füße auf der Bodenlinie). Kontext verschiebt die Figur sonst um einige Prozent."""
    ka = q[..., 3] > 0.5; ra = ref > 0.5
    ky, kx = np.nonzero(ka); ry, rx = np.nonzero(ra)
    if len(ky) < 50 or len(ry) < 50: return q
    (kt, kb), (rt, rb) = zeilen(ka), zeilen(ra)
    def kopfmitte(ys, xs, t, b):
        m = ys < t + 0.12 * (b - t); return xs[m].mean()
    s = float(np.clip((rb - rt) / max(kb - kt, 1), 0.7, 1.4)) if voll else 1.0
    dy = rt - s * kt; dx = kopfmitte(ry, rx, rt, rb) - s * kopfmitte(ky, kx, kt, kb)
    print(f"AUSRICHTEN s={s:.3f} dx={dx:.1f} dy={dy:.1f}")
    if abs(s - 1) < 0.002 and abs(dx) < 0.5 and abs(dy) < 0.5: return q
    return affin(q, s, dx, dy)


# ================================================================== portrait
def portrait(wer, a):
    datei = PORTRAIT_NAME.get(wer, wer)
    quelle = PORTRAITS + f"{datei}.png" if a.bearbeiten else OUT + f"portrait_{datei}_blockout.png"
    if a.quelle: quelle = a.quelle
    if not os.path.exists(quelle): sys.exit(f"Quelle fehlt: {quelle}" + ("" if a.bearbeiten else " — erst `ebenen_figuren.py portraits`"))
    stil = a.stil or (STIL + f"portrait_{datei}.txt")
    if a.bearbeiten:
        prompt = stil_text(stil)
        bildquelle = Image.open(quelle).convert("RGBA"); cream = Image.new("RGBA", bildquelle.size, (253, 245, 228, 255))
        cream.alpha_composite(bildquelle); tmp = OUT + f"portrait_{datei}_eingabe.png"; cream.convert("RGB").save(tmp); quelle = tmp
    else:
        prompt = "Repaint this exact portrait, keep the pose, framing and colours unchanged. Style: " + stil_text(stil)
    fc = fal_laden(a.dry_run)
    payload = {"prompt": prompt, "image_url": None if a.dry_run else fc.encode_file(quelle), "seed": a.seed,
               "guidance_scale": a.guidance, "output_format": "png", "safety_tolerance": "2"}
    roh = OUT + f"portrait_{datei}_s{a.seed}.png"
    if a.aus: roh = a.aus
    elif fal_bild("fal-ai/flux-pro/kontext", payload, roh, a.dry_run) is None: return
    im = Image.open(roh).convert("RGB")
    # auf 400x440 (Mitte beschneiden, dann skalieren); Hintergrund bleibt — die Porträts im Spiel sind deckend auf Creme
    zw, zh = 400, 440; r = zw / zh
    if im.width / im.height > r: nw = int(im.height * r); im = im.crop(((im.width - nw) // 2, 0, (im.width - nw) // 2 + nw, im.height))
    else: nh = int(im.width / r); im = im.crop((0, (im.height - nh) // 2, im.width, (im.height - nh) // 2 + nh))
    fertig = im.resize((zw, zh), Image.LANCZOS).convert("RGBA")
    fertig.save(OUT + f"portrait_{datei}_s{a.seed}_400.png")
    if a.uebernehmen:
        q = fertig.quantize(colors=160, method=Image.Quantize.FASTOCTREE); q.save(PORTRAITS + f"{datei}.png", optimize=True)
        print("ÜBERNOMMEN ->", os.path.relpath(PORTRAITS + f"{datei}.png", WURZEL), os.path.getsize(PORTRAITS + f"{datei}.png") // 1024, "kB")


# ================================================================== Aufruf
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modus", choices=["vorlage", "malen", "einsetzen", "portrait"])
    ap.add_argument("was", help="Raum (vorlage, einsetzen) oder Figur (malen, portrait)")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--guidance", type=float, default=3.5)
    ap.add_argument("--stil", help="Stilphrase (Datei); Standard stil/figur_<name>.txt bzw. stil/portrait_<wer>.txt")
    ap.add_argument("--portrait", action="store_true", help="malen: Porträt als zweites Bild (kontext/max/multi)")
    ap.add_argument("--birefnet", action="store_true", help="malen: Freistellen über fal-ai/birefnet/v2 statt Farbschlüssel")
    ap.add_argument("--bearbeiten", action="store_true", help="portrait: bestehendes Porträt umzeichnen statt Blockout; malen: fertige Figur (--quelle) nachbessern")
    ap.add_argument("--uebernehmen", action="store_true", help="Ergebnis ins Repository übernehmen (art/figuren_quelle bzw. art/portraits)")
    ap.add_argument("--skala", type=int, default=1, help="einsetzen: Auflösung der Figur-PNGs als Vielfaches der Bühne")
    ap.add_argument("--aus", help="malen/portrait: schon geholtes Kontext-Bild verwenden statt fal aufzurufen")
    ap.add_argument("--quelle", help="--bearbeiten: dieses Bild umzeichnen (Standard: art/portraits/<wer>.png bzw. die Vorlage)")
    ap.add_argument("--nur", action="append", help="vorlage: nur diese Figur(en)")
    ap.add_argument("--neu", action="store_true", help="vorlage: Ausschnitt auch für Figuren mit übernommener Quelle neu bestimmen")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.modus == "vorlage": vorlage(a.was, nur=a.nur, neu=a.neu)
    elif a.modus == "malen": malen(a.was, a)
    elif a.modus == "einsetzen": einsetzen(a.was, a.skala)
    elif a.modus == "portrait": portrait(a.was, a)


if __name__ == "__main__":
    main()
