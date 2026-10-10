"""Figuren-Ebene und Porträts in ligne claire — dieselben Durchgänge wie die Räume
(Fläche, Freestyle-Linie, Sonne), zusammengesetzt wie in komposit.py.

    python3 ebenen_figuren.py probe      # alle drei Figuren auf neutraler Bühne -> bau/blender/figuren/probe.png
    python3 ebenen_figuren.py raum       # Aufnahme: Marlene + Herr K -> art/szenen/aufnahme/figuren/{marlene,herrk}.png + figuren.json
    python3 ebenen_figuren.py monitor    # Monitorzimmer: Dr. Falk -> art/szenen/monitor/figuren/falk.png + figuren.json
    python3 ebenen_figuren.py portraits  # Brustbilder -> art/portraits/{marlene,herr_k,falk}.png (400x440, Alpha)

Der Raum wird aus seiner Szenendatei aufgebaut (Aufnahme: exec von szene_aufnahme.py; Monitorzimmer: Import
von szene_monitor.py, werkzeug-Schnittstelle), die Raumobjekte werden als Holdout gerendert: die Figur hat
dort Alpha 0, wo Tresen oder Stuhl sie verdecken. Danach: ebenen.py <raum> flat schreibt hitboxes.json neu,
also die Figuren immer NACH den Raum-Durchgängen rendern (sie vereinigen ihre Klickzone dort hinein).
"""
import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, HIER)
MODE = sys.argv[1] if len(sys.argv) > 1 else "probe"
OUT = os.path.join(WURZEL, "bau", "blender", "figuren") + os.sep; os.makedirs(OUT, exist_ok=True)
SZENE = os.path.join(WURZEL, "art", "szenen", "aufnahme") + os.sep
PORTRAITS = os.path.join(WURZEL, "art", "portraits") + os.sep

hexc = lambda s: tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))
def srgb_to_lin(c): return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)

# Raum-Palette wie in ebenen_aufnahme.py (dort verbindlich), ergänzt um die Figurenfarben
PAL = {
    "wall": "#EFE6D3", "wall_low": "#BFD9CF", "ceiling": "#EEE7DA", "floor": "#DCD3C0",
    "wood": "#C99A5B", "paper": "#F7F1E4", "cork": "#B98B5A", "dark": "#2C3E46", "mid": "#2C5560",
    "metal": "#8A9598", "glass": "#EAF1F2", "slat": "#F4EBD8", "screen": "#CDEBDA", "lampshade": "#2C3E46",
    "accent": "#B5552D", "dawn": "#F8E7BF", "corridor": "#F3D9A8", "ground": "#CFD9C2", "buehne": "#EFE6D3",
}
INK = np.array(hexc("#1E2A30"), np.float32); LICHT = np.array(hexc("#FFF6DC"), np.float32)
STUFE = 1440 / 1600          # Bühne im Spiel: 1440 px breit -> 44 CSS-px Mindestziel = 49 Bühnen-px
MIN_ZIEL = int(math.ceil(44 / STUFE))

import bpy
from mathutils import Vector
import figuren
PAL.update(figuren.FARBEN)


# ------------------------------------------------------------------ Durchgänge (wieder-eintrittsfähig)
def _knoten(m):
    nt = m.node_tree; out = nt.nodes.get("Material Output"); b = nt.nodes.get("Principled BSDF")
    return nt, out, b

def material_flach(farbe_hex=None, weiss=False, schwarz=False):
    """Alle Materialien auf reine Emission: Lokalfarbe (Fläche), Weiß (Linienpass) oder Schwarz."""
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt, out, b = _knoten(m)
        if out is None: continue
        em = nt.nodes.get("ebene_em") or nt.nodes.new("ShaderNodeEmission"); em.name = "ebene_em"
        col = PAL.get(m.name)
        if weiss: c = (1, 1, 1)
        elif schwarz: c = (0, 0, 0)
        else: c = srgb_to_lin(hexc(col)) if col else (0.5, 0.5, 0.5)
        em.inputs["Color"].default_value = (*c, 1); em.inputs["Strength"].default_value = 1.0
        for l in list(out.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])

def material_grau():
    """Sonnenpass: alles gleich grau und matt, damit nur Licht und Schatten zählen."""
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt, out, b = _knoten(m)
        if out is None or b is None: continue
        for l in list(b.inputs["Base Color"].links): nt.links.remove(l)
        b.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1); b.inputs["Emission Strength"].default_value = 0.0
        b.inputs["Roughness"].default_value = 0.7; b.inputs["Metallic"].default_value = 0.0
        for l in list(out.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(b.outputs["BSDF"], out.inputs["Surface"])

def welt(farbe, staerke):
    sc = bpy.context.scene
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World"); sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*farbe, 1); bg.inputs[1].default_value = staerke

def lichter(an):
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.hide_render = not an(o)

def freestyle(an, sammlung=None):
    sc = bpy.context.scene; vl = sc.view_layers[0]
    sc.render.use_freestyle = an; vl.use_freestyle = an
    if not an: return
    sc.render.line_thickness_mode = 'ABSOLUTE'
    fs = vl.freestyle_settings
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("ls")
    ls.select_silhouette = True; ls.select_crease = True; ls.select_border = True; ls.select_contour = True
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("claire") if not len(bpy.data.linestyles) else bpy.data.linestyles[0]
    ls.linestyle.color = (0, 0, 0); ls.linestyle.alpha = 1.0; ls.linestyle.thickness = 1.5
    fs.crease_angle = math.radians(120)
    ls.select_by_collection = sammlung is not None
    if sammlung is not None: ls.collection = sammlung; ls.collection_negation = 'INCLUSIVE'

def render_grund(bx, by):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.render.resolution_x, sc.render.resolution_y = bx, by; sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    sc.render.use_motion_blur = False

def render(pfad, samples, denoise, alpha=False):
    sc = bpy.context.scene
    sc.cycles.samples = samples; sc.cycles.use_denoising = denoise; sc.render.filepath = pfad
    sc.render.film_transparent = alpha; sc.render.image_settings.color_mode = 'RGBA' if alpha else 'RGB'
    t = time.time(); bpy.ops.render.render(write_still=True); print(f"RENDER {os.path.basename(pfad)} {time.time() - t:.1f}s", flush=True)

def pass_flach(pfad, sichtbar):
    """Flächenpass mit Alpha: `sichtbar(o)` -> True (rendern), False (verstecken), "holdout" (Loch)."""
    material_flach(); lichter(lambda o: False); welt((0, 0, 0), 0.0)
    sc = bpy.context.scene; sc.cycles.max_bounces = 0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        s = sichtbar(o); o.hide_render = (s is False); o.is_holdout = (s == "holdout")
    freestyle(False); render(pfad, 4, False, alpha=True)

def pass_linien(pfad, sichtbar, sammlung):
    material_flach(weiss=True); lichter(lambda o: False); welt((1, 1, 1), 1.0)
    sc = bpy.context.scene; sc.cycles.max_bounces = 0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        o.is_holdout = False; o.hide_render = not sichtbar(o)
        if o.data.materials and o.data.materials[0].name == "slat": o.hide_render = True   # wie im Raum: Lamellen ohne Kontur
    freestyle(True, sammlung); render(pfad, 4, False)

def pass_sonne(pfad, sichtbar, richtung, energie=14.0):
    material_grau(); welt((0, 0, 0), 0.0)
    sc = bpy.context.scene; sc.cycles.max_bounces = 0
    sonne = next((o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN'), None)
    if sonne is None:
        bpy.ops.object.light_add(type='SUN'); sonne = bpy.context.object
    sonne.data.energy = energie; sonne.data.angle = math.radians(0.6); sonne.data.color = (1, 1, 1)
    sonne.rotation_euler = Vector(richtung).to_track_quat('-Z', 'Y').to_euler()
    lichter(lambda o: o is sonne)
    for n in ("dawn", "corridor"):
        if n in bpy.data.materials: bpy.data.materials[n].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        o.is_holdout = False; o.hide_render = not sichtbar(o)
    if "win_glow" in bpy.data.objects: bpy.data.objects["win_glow"].hide_render = True
    freestyle(False); render(pfad, 16, True)


# ------------------------------------------------------------------ Komposit (Logik aus komposit.py, mit Alpha)
def lade(p, alpha=False):
    im = Image.open(p).convert("RGBA" if alpha else "RGB")
    return np.asarray(im).astype(np.float32) / 255

def luma(a): return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

def weich(m, r=0.7):
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255

def komposit(flach, frei, sonne, linien, sun_t=0.35, unten=0, licht_farbe=None, anteil=0.32, weich_r=0.7):
    """flach: RGBA mit Holdout (Alpha = sichtbarer Teil), frei: RGBA ohne Raum (volle Figur),
    sonne/linien: RGB. `unten` zieht die sichtbare Alpha um n px nach unten in den verdeckten Teil
    (weicher Auslauf unter der Tresenkante, damit die Atem-Animation keine harte Kante zeigt).
    Lichtfarbe, Anteil, Schwelle und Weichheit wie in komposit.EINSTELLUNG des Raums."""
    col = frei[..., :3]; voll = frei[..., 3]; a = flach[..., 3]
    L = LICHT if licht_farbe is None else np.array(hexc(licht_farbe), np.float32)
    ls = luma(sonne); ls = np.clip(ls / (np.percentile(ls, 99.5) + 1e-6), 0, 1)
    ls = np.asarray(Image.fromarray((ls * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))).astype(np.float32) / 255
    licht = weich((ls > sun_t).astype(np.float32), weich_r)[..., None]
    col = col * (1 - licht) + (col * (1 - anteil) + L * anteil) * licht
    ink = np.clip((1 - luma(linien)) * 1.3, 0, 1)
    if unten:
        for k in range(1, unten + 1):
            v = np.zeros_like(a); v[k:] = a[:-k] * (1 - k / (unten + 1))
            a = np.maximum(a, v)
        a = np.minimum(a, voll)
    alpha = np.maximum(a, ink)
    col = col * (1 - ink[..., None]) + INK * ink[..., None]
    out = np.concatenate([np.clip(col, 0, 1), alpha[..., None]], axis=-1)
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")

def speichern(img, pfad, farben=160):
    """Quantisiertes PNG mit Alpha (klein; wie die Raumebenen)."""
    q = img.quantize(colors=farben, method=Image.Quantize.FASTOCTREE)
    os.makedirs(os.path.dirname(pfad), exist_ok=True); q.save(pfad, optimize=True)
    print("saved", pfad, os.path.getsize(pfad) // 1024, "kB")

def silhouette(img, pfad, breite=160):
    """Daumennagel-Test der Art Bible: schwarz gefüllt, klein — ist die Figur noch zu erkennen?"""
    a = np.asarray(img)[..., 3]
    s = np.zeros(a.shape + (4,), np.uint8); s[..., 3] = a; s[..., :3] = 30
    im = Image.fromarray(s, "RGBA"); h = int(im.height * breite / im.width)
    hinter = Image.new("RGBA", (breite, h), (244, 230, 210, 255)); hinter.alpha_composite(im.resize((breite, h), Image.LANCZOS))
    hinter.save(pfad)


# ------------------------------------------------------------------ Kameras
def kamera(ort, ziel, brennweite):
    sc = bpy.context.scene
    bpy.ops.object.camera_add(location=ort); cam = bpy.context.object; sc.camera = cam
    cam.rotation_euler = (Vector(ziel) - Vector(ort)).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = brennweite; cam.data.sensor_width = 36; cam.data.sensor_fit = 'AUTO'
    return cam

def bildkasten(fig, cam, bx, by):
    """Bildschirm-Rechteck [x0, y0, x1, y1] aller Mesh-Teile einer Figur."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; bpy.context.view_layer.update(); xs, ys = [], []
    for o in fig.teile:
        if o.type != 'MESH': continue
        for v in o.bound_box:
            p = world_to_camera_view(sc, cam, o.matrix_world @ Vector(v)); xs.append(p.x * bx); ys.append((1 - p.y) * by)
    return [max(0, int(min(xs))), max(0, int(min(ys))), min(bx, int(math.ceil(max(xs)))), min(by, int(math.ceil(max(ys))))]

def ist_fig(o): return o.name.split("_")[0] in ("marlene", "herrk", "falk")
def fig_name(o): return o.name.split("_")[0]


# ================================================================== probe
if MODE == "probe":
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    render_grund(1600, 900)
    boden = bpy.data.materials.new("buehne"); boden.use_nodes = True
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0)); bpy.context.object.data.materials.append(boden); bpy.context.object.name = "boden"
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.1, 0.24)); stuhl = bpy.context.object; stuhl.scale = (0.5, 0.5, 0.48); stuhl.name = "stuhl"; stuhl.data.materials.append(boden)
    figs = [figuren.marlene((-1.6, 0, 0), drehung=12, haltung="stehen", fein=0.0055),
            figuren.herr_k((0, 0, 0), drehung=-8, haltung="sitzen", fein=0.0055, tuete=True),
            figuren.falk((1.6, 0, 0), drehung=-10, fein=0.0055)]
    cam = kamera((0.3, -6.6, 1.15), (0.0, 0, 0.95), 32)
    koerper = bpy.data.collections["figuren"]
    pass_flach(OUT + "probe_flat.png", lambda o: True if ist_fig(o) else False)
    pass_linien(OUT + "probe_lines.png", lambda o: True, koerper)
    pass_sonne(OUT + "probe_sun.png", lambda o: True, (0.5, 0.6, -0.7), energie=8.0)
    flach = lade(OUT + "probe_flat.png", True)
    img = komposit(flach, flach, lade(OUT + "probe_sun.png"), lade(OUT + "probe_lines.png"))
    hinter = Image.new("RGBA", img.size, (239, 230, 211, 255)); hinter.alpha_composite(img); hinter.save(OUT + "probe.png")
    silhouette(img, OUT + "probe_silhouette.png", 480)
    print("saved", OUT + "probe.png")

# ------------------------------------------------------------------ Figurenebene eines Raums
def figuren_durchgaenge(figs, raum_sichtbar, sonne_sichtbar, sonne_richtung, energie, sonne_name):
    """Je Figur drei Durchgänge (Fläche mit Raum als Holdout, Fläche frei, Linie hinter dem Raum) und einmal
    die Sonne des Raums über allem. raum_sichtbar(o): Raumobjekt wird gerendert (Platzhalter nie)."""
    koerper = bpy.data.collections["figuren"]
    for name in figs:
        pass_flach(OUT + f"{name}_flat.png", lambda o, n=name: (fig_name(o) == n) if ist_fig(o) else ("holdout" if raum_sichtbar(o) else False))
        pass_flach(OUT + f"{name}_frei.png", lambda o, n=name: (fig_name(o) == n) if ist_fig(o) else False)
        pass_linien(OUT + f"{name}_lines.png", lambda o, n=name: (fig_name(o) == n) if ist_fig(o) else raum_sichtbar(o), koerper)
    pass_sonne(OUT + sonne_name, lambda o: True if ist_fig(o) else sonne_sichtbar(o), sonne_richtung, energie=energie)


def figuren_ebene(raum, figs, cam, sonne_name, klasse, unten=None, einst=None):
    """Komposit je Figur -> art/szenen/<raum>/figuren/<name>.png + figuren.json (Bühnenposition, Atem-Klasse);
    Klickzone der Figur (sichtbarer Teil ∪ bestehende Zone, mindestens 44 CSS-px) in hitboxes.json."""
    szene_dir = os.path.join(WURZEL, "art", "szenen", raum) + os.sep
    e = einst or {}
    sonne = lade(OUT + sonne_name)
    hit = json.load(open(szene_dir + "hitboxes.json", encoding="utf-8"))
    platz = {}
    for name, fig in figs.items():
        img = komposit(lade(OUT + f"{name}_flat.png", True), lade(OUT + f"{name}_frei.png", True), sonne,
                       lade(OUT + f"{name}_lines.png"), sun_t=e.get("schwelle", 0.35), unten=(unten or {}).get(name, 0),
                       licht_farbe=e.get("licht"), anteil=e.get("anteil", 0.32), weich_r=e.get("weich", 0.7))
        a = np.asarray(img)[..., 3]; ys, xs = np.nonzero(a > 8)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        speichern(img.crop((x0, y0, x1, y1)), szene_dir + f"figuren/{name}.png")
        silhouette(img.crop((x0, y0, x1, y1)), OUT + f"{name}_silhouette.png", 120)
        platz[name] = {"datei": f"{name}.png", "x": x0, "y": y0, "breite": x1 - x0, "hoehe": y1 - y0,
                       "klasse": klasse.get(name, "atmet")}
        k = bildkasten(fig, cam, 1600, 900)
        alt = hit.get(name, k)
        r = [min(alt[0], x0), min(alt[1], y0), max(alt[2], x1), max(alt[3], y1)]
        for i in (0, 1):
            if r[i + 2] - r[i] < MIN_ZIEL:
                m = (r[i] + r[i + 2]) // 2; r[i], r[i + 2] = m - MIN_ZIEL // 2, m + MIN_ZIEL // 2
        hit[name] = [max(0, r[0]), max(0, r[1]), min(1600, r[2]), min(900, r[3])]
        print("FIGUR", name, platz[name], "| Kasten", k, "| Klickzone", hit[name])
    json.dump(platz, open(szene_dir + "figuren/figuren.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(hit, open(szene_dir + "hitboxes.json", "w", encoding="utf-8"), indent=1)
    # Vorschau: Raumebenen + Figuren übereinander (nur zur Kontrolle)
    try:
        vor = Image.open(szene_dir + "hintergrund.png").convert("RGBA"); vor.alpha_composite(Image.open(szene_dir + "mittelgrund.png").convert("RGBA"))
        for name, p in platz.items():
            vor.alpha_composite(Image.open(szene_dir + f"figuren/{name}.png").convert("RGBA"), (p["x"], p["y"]))
        vor.save(OUT + f"{raum}_vorschau.png"); print("saved", OUT + f"{raum}_vorschau.png")
    except Exception as e:
        print("keine Vorschau:", e)


def raum_einstellung(raum):
    """Licht-Einstellung des Raums aus komposit.py (Lichtfarbe, Anteil, Schwelle, Weichheit)."""
    try:
        import komposit
        return komposit.EINSTELLUNG.get(raum, komposit.STANDARD)
    except Exception:
        return None


# ================================================================== raum: Aufnahme
if MODE == "raum":
    base = open(os.path.join(HIER, "szene_aufnahme.py"), encoding="utf-8").read()
    _argv, _MODE, _OUT = sys.argv, MODE, OUT; sys.argv = ["x", "lit"]; exec(base)
    sys.argv, MODE, OUT = _argv, _MODE, _OUT      # die Szenendatei überschreibt MODE und OUT
    sc = bpy.context.scene; render_grund(1600, 900)
    bpy.data.objects["bag"].data.materials[0] = G["paper"]; bpy.data.objects["folder"].data.materials[0] = G["paper"]
    cam = sc.camera   # Kamera wie in der Szene (ebenen.py rendert mit derselben)
    # Marlene hinter dem Tresen (Tresenrückkante y = -0,83), dem Raum zugewandt, leicht zur Tür gedreht;
    # Herr K auf dem dritten Stuhl (x = 2,4), etwas zur Tür gedreht; die Tüte steht schon im Mittelgrund
    figs = {"marlene": figuren.marlene((-3.05, -0.5, 0), drehung=20, haltung="tresen", tag=_tag, fein=0.0055, tresen=1.1),
            "herrk": figuren.herr_k((2.4, -0.75, 0), drehung=-8, haltung="sitzen", tag=_tag, fein=0.0055, tuete=False)}
    # Sonne wie im Raum (szene_aufnahme.sonne_stellen): von hinter dem Fenster, tief, zur Kamera
    figuren_durchgaenge(figs, lambda o: True, lambda o: True, (-0.30, -0.80, -0.52), 14.0, "raum_sun.png")
    figuren_ebene("aufnahme", figs, cam, "raum_sun.png", {"marlene": "atmet", "herrk": "atmet langsam"},
                  unten={"marlene": 3}, einst=raum_einstellung("aufnahme"))

# ================================================================== monitor: Dr. Falk
elif MODE == "monitor":
    import importlib
    import werkzeug as wz
    szene = importlib.import_module("szene_monitor")      # baut Raum, Kamera (mit Verschiebung) und Sonne
    PAL.update(szene.PALETTE)
    sc = bpy.context.scene; render_grund(1600, 900); cam = sc.camera
    # Falk steht am Platzhalter der Szene (rechts vom großen Schirm), Hände in den Taschen, dem Schirm zugewandt
    pl = bpy.data.objects["platz_falk"]                     # Lage aus dem Welt-Kasten (location ist nach transform_apply 0)
    bb = [pl.matrix_world @ Vector(v) for v in pl.bound_box]
    px, py = sum(v.x for v in bb) / 8, sum(v.y for v in bb) / 8
    figs = {"falk": figuren.falk((px, py, 0), drehung=-14, haltung="taschen", fein=0.0055)}
    nie = set(wz.PLATZHALTER)
    figuren_durchgaenge(figs, lambda o: o.name not in nie, lambda o: o.name not in nie and o.name not in szene.SONNE_AUS,
                        (0.25, -0.75, -0.6), 12.0, "monitor_sun.png")   # Sonne wie in szene_monitor.py
    figuren_ebene("monitor", figs, cam, "monitor_sun.png", {"falk": "atmet langsam"}, einst=raum_einstellung("monitor"))

# ================================================================== portraits
elif MODE == "portraits":
    BX, BY = 400, 440
    for wer, bau in figuren.FIGUREN.items():
        bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
        render_grund(BX, BY)
        fig = bau((0, 0, 0), drehung=0, haltung="stehen" if wer != "falk" else "taschen", fein=0.0035)
        kx, ky, kz = fig.kopfmitte
        ziel = Vector((kx, ky, kz - 0.1)); phi = math.radians(26); d = 1.1
        cam = kamera(ziel + Vector((-math.sin(phi) * d, -math.cos(phi) * d, 0.06)), ziel, 60)
        koerper = bpy.data.collections["figuren"]
        pass_flach(OUT + f"portrait_{wer}_flat.png", lambda o: True)
        pass_linien(OUT + f"portrait_{wer}_lines.png", lambda o: True, koerper)
        pass_sonne(OUT + f"portrait_{wer}_sun.png", lambda o: True, (0.55, 0.75, -0.6), energie=6.0)
        flach = lade(OUT + f"portrait_{wer}_flat.png", True)
        img = komposit(flach, flach, lade(OUT + f"portrait_{wer}_sun.png"), lade(OUT + f"portrait_{wer}_lines.png"), sun_t=0.45)
        speichern(img, PORTRAITS + f"{wer}.png", 128)
        klein = Image.new("RGBA", (92, 100), (247, 241, 228, 255)); klein.alpha_composite(img.resize((92, 101), Image.LANCZOS).crop((0, 0, 92, 100)))
        klein.save(OUT + f"portrait_{wer}_klein.png")
else:
    print("unbekannter Modus", MODE)
