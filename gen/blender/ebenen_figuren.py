"""Figuren-Ebene und Porträts in ligne claire — dieselben Durchgänge wie die Räume
(Fläche, Freestyle-Linie, Sonne), zusammengesetzt wie in komposit.py.

    python3 ebenen_figuren.py probe      # alle drei Figuren auf neutraler Bühne -> bau/blender/figuren/probe.png
    python3 ebenen_figuren.py raum       # Aufnahme: Blockout von Marlene + Herr K -> bau/blender/figuren/blockout/aufnahme/
    python3 ebenen_figuren.py monitor    # Monitorzimmer: Blockout von Dr. Falk -> bau/blender/figuren/blockout/monitor/
    python3 ebenen_figuren.py lehrsaal   # Lehrsaal: Blockout von Dr. Wieser + Jonas -> bau/blender/figuren/blockout/lehrsaal/
    python3 ebenen_figuren.py portraits [wer …]  # Brustbild-Blockouts -> bau/blender/figuren/portrait_<wer>_blockout.png (400x440, Alpha)

Die Figuren im Spiel (art/szenen/<raum>/figuren/) und die Porträts (art/portraits/) entstehen aus diesen Blockouts
über figuren_zeichnen.py (Kontext-Feinschliff, dann deterministisches Einsetzen); aufbau(raum) hier ist die
gemeinsame Szene dafür. Orte der Figuren: figuren.PLATZ.

Der Raum wird aus seiner Szenendatei aufgebaut (Aufnahme: exec von szene_aufnahme.py; Monitorzimmer: Import
von szene_monitor.py, werkzeug-Schnittstelle), die Raumobjekte werden als Holdout gerendert: die Figur hat
dort Alpha 0, wo Tresen oder Stuhl sie verdecken. Die Sonne kommt aus `szene.sonne_stellen()`, Objekte in
`SONNE_AUS` (Leuchtflächen vor dem Fenster) werfen keinen Schatten — wie in ebenen.py. Danach: ebenen.py <raum> flat schreibt hitboxes.json neu,
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
LINIE = 1.5                   # Freestyle-Strichstärke (px); figuren_zeichnen.py skaliert sie mit dem Ausschnitt
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
    ls.linestyle.color = (0, 0, 0); ls.linestyle.alpha = 1.0; ls.linestyle.thickness = LINIE
    fs.crease_angle = math.radians(120)
    ls.select_by_collection = sammlung is not None
    if sammlung is not None: ls.collection = sammlung; ls.collection_negation = 'INCLUSIVE'

def render_grund(bx, by):
    sc = bpy.context.scene
    import werkzeug; werkzeug.cycles_geraet(sc)
    if os.environ.get("BLENDER_THREADS"):      # z. B. BLENDER_THREADS=2, wenn nebenan ein zweiter Render läuft
        sc.render.threads_mode = 'FIXED'; sc.render.threads = max(1, int(os.environ["BLENDER_THREADS"]))
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

def pass_sonne(pfad, sichtbar, richtung=None, energie=14.0, stellen=None):
    """Sonnen-Durchgang. stellen(sonne): die Sonne der Szene (szene.sonne_stellen) — dann haben Figur und Raum
    dasselbe Licht; sonst Richtung/Energie von Hand (probe, portraits)."""
    material_grau(); welt((0, 0, 0), 0.0)
    sc = bpy.context.scene; sc.cycles.max_bounces = 0
    sonne = next((o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN'), None)
    if sonne is None:
        bpy.ops.object.light_add(type='SUN'); sonne = bpy.context.object
    if stellen is not None: stellen(sonne)
    else:
        sonne.data.energy = energie; sonne.data.angle = math.radians(0.6)
        sonne.rotation_euler = Vector(richtung).to_track_quat('-Z', 'Y').to_euler()
    sonne.data.color = (1, 1, 1)
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

FIGNAMEN = {"marlene", "herrk", "falk", "wieser", "jonas"}
ZUORDNUNG = {}      # Objektname -> Figurname für Raumobjekte, die wie eine Figur gezeichnet werden (Herrn K.s Tüte)
def ist_fig(o): return o.name in ZUORDNUNG or o.name.split("_")[0] in FIGNAMEN
def fig_name(o): return ZUORDNUNG.get(o.name) or o.name.split("_")[0]

class Raumfigur:
    """Raumobjekte, die als eigene Figurendatei gezeichnet werden (Tüte): nur Name und Teile, kein Kopf."""
    def __init__(self, name, teile): self.name, self.teile = name, teile


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
def figuren_durchgaenge(figs, raum_sichtbar, sonne_sichtbar, sonne_stellen, sonne_name):
    """Je Figur drei Durchgänge (Fläche mit Raum als Holdout, Fläche frei, Linie hinter dem Raum) und einmal
    die Sonne des Raums über allem. raum_sichtbar(o): Raumobjekt wird gerendert (Platzhalter nie);
    sonne_sichtbar(o): wirft im Sonnen-Durchgang Schatten (SONNE_AUS der Szene nicht)."""
    koerper = bpy.data.collections["figuren"]
    for name in figs:
        pass_flach(OUT + f"{name}_flat.png", lambda o, n=name: (fig_name(o) == n) if ist_fig(o) else ("holdout" if raum_sichtbar(o) else False))
        pass_flach(OUT + f"{name}_frei.png", lambda o, n=name: (fig_name(o) == n) if ist_fig(o) else False)
        pass_linien(OUT + f"{name}_lines.png", lambda o, n=name: (fig_name(o) == n) if ist_fig(o) else raum_sichtbar(o), koerper)
    pass_sonne(OUT + sonne_name, lambda o: True if ist_fig(o) else sonne_sichtbar(o), stellen=sonne_stellen)


def figuren_ebene(raum, figs, cam, sonne_name, klasse, unten=None, einst=None, ziel=None):
    """Komposit je Figur -> <ziel>/figuren/<name>.png + figuren.json (Bühnenposition, Atem-Klasse) und
    hitboxes.json (Klickzone der Figur: sichtbarer Teil ∪ bestehende Zone, mindestens 44 CSS-px).
    ziel: Standard art/szenen/<raum>/ (ins Spiel); die Raumebenen für die Vorschau kommen immer von dort."""
    szene_dir = os.path.join(WURZEL, "art", "szenen", raum) + os.sep
    ziel = ziel or szene_dir; os.makedirs(ziel + "figuren", exist_ok=True)
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
        speichern(img.crop((x0, y0, x1, y1)), ziel + f"figuren/{name}.png")
        silhouette(img.crop((x0, y0, x1, y1)), OUT + f"{name}_silhouette.png", 120)
        platz[name] = {"datei": f"{name}.png", "x": x0, "y": y0, "breite": x1 - x0, "hoehe": y1 - y0}
        if klasse.get(name, "atmet"): platz[name]["klasse"] = klasse.get(name, "atmet")
        k = bildkasten(fig, cam, 1600, 900)
        alt = hit.get(name, k)
        r = [min(alt[0], x0), min(alt[1], y0), max(alt[2], x1), max(alt[3], y1)]
        for i in (0, 1):
            if r[i + 2] - r[i] < MIN_ZIEL:
                m = (r[i] + r[i + 2]) // 2; r[i], r[i + 2] = m - MIN_ZIEL // 2, m + MIN_ZIEL // 2
        hit[name] = [max(0, r[0]), max(0, r[1]), min(1600, r[2]), min(900, r[3])]
        print("FIGUR", name, platz[name], "| Kasten", k, "| Klickzone", hit[name])
    json.dump(platz, open(ziel + "figuren/figuren.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(hit, open(ziel + "hitboxes.json", "w", encoding="utf-8"), indent=1)
    # Vorschau: Raumebenen + Figuren übereinander (nur zur Kontrolle)
    try:
        vor = Image.open(szene_dir + "hintergrund.png").convert("RGBA"); vor.alpha_composite(Image.open(szene_dir + "mittelgrund.png").convert("RGBA"))
        for name, p in platz.items():
            vor.alpha_composite(Image.open(ziel + f"figuren/{name}.png").convert("RGBA"), (p["x"], p["y"]))
        vp = (ziel + "vorschau.png") if ziel != szene_dir else (OUT + f"{raum}_vorschau.png")
        vor.save(vp); print("saved", vp)
    except Exception as e:
        print("keine Vorschau:", e)


def raum_einstellung(raum):
    """Licht-Einstellung des Raums aus komposit.py (Lichtfarbe, Anteil, Schwelle, Weichheit)."""
    try:
        import komposit
        return komposit.EINSTELLUNG.get(raum, komposit.STANDARD)
    except Exception:
        return None


# ------------------------------------------------------------------ Raum mit Figuren aufbauen
def aufbau(raum):
    """Baut den Raum aus seiner Szenendatei (Kamera, Licht) und stellt die Figuren an die Orte aus figuren.PLATZ.
    Gibt zurück: cam, figs {name: Figur}, raum_sichtbar(o), sonne_sichtbar(o), sonne (Richtung), energie,
    klasse (Atem-Klassen), unten (Auslauf unter der Tresenkante), kontext {name: [Objektnamen, die als
    Vorlage mitgerendert werden, z. B. der Tresen vor Marlene]}, verdecker {name: None (jedes Raumobjekt vor
    der Figur verdeckt sie) oder [Objektnamen] (nur diese) — Herr K sitzt IM Stuhl, Armlehnen und Tüte liegen
    fast in seiner Tiefe und schnitten sonst Löcher in die gezeichneten Ärmel}.
    Gemeinsam für die Modi raum/monitor hier und für figuren_zeichnen.py."""
    P = figuren.PLATZ
    if raum == "aufnahme":
        ns = {"__file__": os.path.join(HIER, "szene_aufnahme.py"), "__name__": "szene_aufnahme"}
        _argv = sys.argv; sys.argv = ["x", "lit"]                    # die Szenendatei liest ihren Modus aus argv
        try: exec(open(ns["__file__"], encoding="utf-8").read(), ns)
        finally: sys.argv = _argv
        sc = bpy.context.scene; render_grund(1600, 900); G, tag = ns["G"], ns["_tag"]
        bpy.data.objects["bag"].data.materials[0] = G["paper"]; bpy.data.objects["folder"].data.materials[0] = G["paper"]
        # Marlene hinter dem Tresen, dem Raum zugewandt, leicht zur Tür gedreht; Herr K auf dem dritten Stuhl,
        # etwas zur Tür gedreht; die Tüte steht schon im Mittelgrund (Raumobjekt, er hält sie nicht)
        m, k = P["marlene"], P["herrk"]
        figs = {"marlene": figuren.marlene(m["ort"], drehung=m["drehung"], haltung=m["haltung"], tag=tag, fein=0.0055, tresen=m["tresen"]),
                "herrk": figuren.herr_k(k["ort"], drehung=k["drehung"], haltung=k["haltung"], tag=tag, fein=0.0055, tuete=False)}
        # Herrn K.s Tüte (Raumobjekte der Zone "tuete", im Raumrender Platzhalter): eigene Figurendatei, nach ihm gezeichnet
        tuete = [bpy.data.objects[n] for n in ns["HIT"].get("tuete", [])]
        for o in tuete: ZUORDNUNG[o.name] = "tuete"
        figs["tuete"] = Raumfigur("tuete", tuete)
        import werkzeug as wz
        nie = set(wz.PLATZHALTER) - set(ZUORDNUNG)
        aus = set(ns.get("SONNE_AUS", set()))                          # Leuchtflächen draußen schatten nie ab
        return dict(cam=sc.camera, figs=figs, raum_sichtbar=lambda o: o.name not in nie,
                    sonne_sichtbar=lambda o: o.name not in aus and o.name not in nie,
                    sonne_stellen=ns.get("sonne_stellen", lambda s: None),   # dieselbe Sonne wie ebenen.py (sonst die der Szene)
                    klasse={"marlene": "atmet", "herrk": "atmet langsam", "tuete": None}, unten={"marlene": 3},
                    kontext={"marlene": ["desk", "desk_top", "desk_panel", "desk_wange"], "herrk": [], "tuete": []},   # Bank bleibt Raumobjekt: Kontext zeichnet sie sonst doppelt
                    verdecker={"marlene": None, "herrk": [], "tuete": []}, dinge={"tuete"},
                    getrennt={"tuete": "herrk"})                      # Klickzonen, die sich nicht überlappen dürfen
    if raum == "monitor":
        import importlib
        import werkzeug as wz
        szene = importlib.import_module("szene_monitor")      # baut Raum, Kamera (mit Verschiebung) und Sonne
        PAL.update(szene.PALETTE)
        sc = bpy.context.scene; render_grund(1600, 900)
        f = P["falk"]; ort = f["ort"]
        if ort is None:                                       # am Platzhalter der Szene (rechts vom großen Schirm)
            pl = bpy.data.objects["platz_falk"]               # Lage aus dem Welt-Kasten (location ist nach transform_apply 0)
            bb = [pl.matrix_world @ Vector(v) for v in pl.bound_box]
            ort = (sum(v.x for v in bb) / 8, sum(v.y for v in bb) / 8, 0.0)
        figs = {"falk": figuren.falk(ort, drehung=f["drehung"], haltung=f["haltung"], fein=0.0055)}
        nie = set(wz.PLATZHALTER)
        return dict(cam=sc.camera, figs=figs, raum_sichtbar=lambda o: o.name not in nie,
                    sonne_sichtbar=lambda o: o.name not in nie and o.name not in szene.SONNE_AUS,
                    sonne_stellen=getattr(szene, "sonne_stellen", lambda s: None),   # dieselbe Sonne wie ebenen.py (sonst die der Szene)
                    klasse={"falk": "atmet langsam"}, unten={}, kontext={"falk": []}, verdecker={"falk": None})
    if raum == "lehrsaal":
        import importlib
        import werkzeug as wz
        szene = importlib.import_module("szene_lehrsaal")     # Raum, Kamera (mit Verschiebung), Sonne
        PAL.update(szene.PALETTE)
        sc = bpy.context.scene; render_grund(1600, 900)
        w, j = P["wieser"], P["jonas"]
        figs = {"wieser": figuren.wieser(w["ort"], drehung=w["drehung"], haltung=w["haltung"], fein=0.0055),
                "jonas": figuren.jonas(j["ort"], drehung=j["drehung"], haltung=j["haltung"], fein=0.0055)}
        nie = set(wz.PLATZHALTER)
        # Nichts im Raum steht vor den beiden (Wieser vor dem Tritt, Jonas AUF der Liege): keine Verdeckung, sonst
        # schnitten Tritt und Polsterkante Löcher in die gezeichneten Figuren. Die Zonen `jonas` und `liege` (Fußende,
        # Elektroden-Aufgabe) bleiben getrennt.
        # Der Tritt steht in Wiesers Vorlage mit (Kontext zeichnet den Fuß sonst auf den Boden) und wird beim Einsetzen
        # aus ihrem Bild geschnitten, wo ihr Blockout ihn nicht deckt (`ausschneiden`): im Raum steht er im Mittelgrund.
        tritt = ["tritt", "tritt_flaeche"]
        # Jonas' vier Extremitätenklemmen zeichnet klemmen_setzen.py in sein Quellbild (Kontext setzt so kleine Dinge
        # nicht an die Gelenke); die Blockout-Klemmen in figuren.jonas() sind nur die Vorlage dafür.
        return dict(cam=sc.camera, figs=figs, raum_sichtbar=lambda o: o.name not in nie,
                    sonne_sichtbar=lambda o: o.name not in nie and o.name not in szene.SONNE_AUS,
                    sonne_stellen=getattr(szene, "sonne_stellen", lambda s: None),
                    klasse={"wieser": "atmet", "jonas": "atmet"}, unten={}, kontext={"wieser": tritt, "jonas": []},
                    verdecker={"wieser": [], "jonas": []}, ausschneiden={"wieser": tritt}, getrennt={"jonas": "liege"},
                    ausrichten={"jonas": False, "wieser": False}, weicht={"projektion": "wieser"})
        # ausrichten: Kontext hält hier die Lage der Vorlage; die Kopf-Ausrichtung verschöbe Wieser samt gezeichnetem Tritt
        # neben den echten (ausschneiden träfe dann daneben) und bei Jonas sind die obersten Zeilen Knie und Kopf zugleich.
    raise SystemExit(f"unbekannter Raum {raum}")


# ================================================================== raum / monitor: Blockout-Figuren (nur noch Vorschau)
# Die Figuren im Spiel kommen aus figuren_zeichnen.py (Blockout -> Kontext -> einsetzen). Diese Modi rendern die
# reinen Blockout-Figuren nach bau/blender/figuren/blockout/<raum>/ — zum Prüfen von Haltung und Platz, nicht ins Spiel.
if MODE in ("raum", "monitor", "lehrsaal"):
    raum = "aufnahme" if MODE == "raum" else MODE
    A = aufbau(raum)
    figuren_durchgaenge(A["figs"], A["raum_sichtbar"], A["sonne_sichtbar"], A["sonne_stellen"], f"{raum}_sun.png")
    figuren_ebene(raum, A["figs"], A["cam"], f"{raum}_sun.png", A["klasse"], unten=A["unten"], einst=raum_einstellung(raum),
                  ziel=os.path.join(OUT, "blockout", raum) + os.sep)

# ================================================================== portraits
elif MODE == "portraits":
    BX, BY = 400, 440
    for wer, bau in figuren.FIGUREN.items():
        if len(sys.argv) > 2 and wer not in sys.argv[2:]: continue      # portraits wieser jonas: nur diese
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
        speichern(img, OUT + f"portrait_{wer}_blockout.png", 128)      # Vorlage für Kontext (figuren_zeichnen.py portrait)
        klein = Image.new("RGBA", (92, 100), (247, 241, 228, 255)); klein.alpha_composite(img.resize((92, 101), Image.LANCZOS).crop((0, 0, 92, 100)))
        klein.save(OUT + f"portrait_{wer}_klein.png")
elif __name__ == "__main__" and MODE != "modul":
    print("unbekannter Modus", MODE)
