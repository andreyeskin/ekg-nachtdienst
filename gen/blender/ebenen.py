"""Render-Durchgänge für einen Raum.

    python3 gen/blender/ebenen.py <raum> <durchgang>      z. B.  ebenen.py monitor flat
    python3 gen/blender/ebenen.py <raum> alle             der Standardsatz, je Durchgang ein frischer Prozess

Die Szene kommt aus szene_<raum>.py (siehe werkzeug.py für ihre Schnittstelle).
Zwischenergebnisse: bau/blender/<raum>/ · Klickzonen: art/szenen/<raum>/hitboxes.json

Durchgänge
  flat      Lokalfarbe (reine Emission, kein Licht), je Flächenrichtung in Stufen heller/dunkler
            (oben hell, Seiten dunkler, keine Verläufe) — schreibt auch die Klickzonen
  lines     Freestyle-Linie, doppelt aufgelöst gerendert und verkleinert (glatte Kanten)
  linesmid  Linie nur des Mittelgrunds (Kontur der Ebene ohne Striche des Hintergrunds)
  mask      Maske des Mittelgrunds
  sun       nur direkte Sonne, graue Materialien, keine Streuung
  ao        Umgebungsverdeckung als Helligkeit (für eine flache Kontaktschatten-Stufe im Komposit)
  kontakt   Schatten unter Möbeln wie von einer Deckenleuchte: Licht senkrecht von oben, nur auf nach oben
            gewandten Flächen ausgewertet (Boden, Tischplatten) — geometrische, flache Formen statt AO-Flecken
  *bg       flatbg, linesbg, sunbg, aobg, kontaktbg: dasselbe ohne Mittel- und Vordergrund
            (kontaktbg: Möbel unsichtbar, werfen aber Schatten — der Schatten liegt so im Hintergrund)
  boxes     nur die Klickzonen
"""
import importlib
import json
import math
import os
import subprocess
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(HIER))
STANDARD = ["flat", "lines", "linesmid", "mask", "flatbg", "linesbg", "sun", "sunbg", "ao", "aobg", "kontakt", "kontaktbg"]
B, H = 1600, 900
LINIE = 1.5          # Strichstärke in Pixeln der fertigen Bühne
UEBER = 2            # Überabtastung der Linien-Durchgänge


def alle(raum):
    for d in STANDARD:
        t = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), raum, d], capture_output=True, text=True)
        print(f"{d:9s} {time.time() - t:5.1f}s", flush=True)
        for z in r.stdout.splitlines():
            if z.startswith(("KLICKZONEN", "FEHLER")): print("  " + z)
        if r.returncode:
            print(r.stdout[-3000:], r.stderr[-3000:]); sys.exit(r.returncode)


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "alle":
    alle(sys.argv[1]); sys.exit(0)

if len(sys.argv) < 3:
    print(__doc__); sys.exit(1)
RAUM, DURCHGANG = sys.argv[1], sys.argv[2]
OUT = os.path.join(WURZEL, "bau", "blender", RAUM) + os.sep
ZIEL = os.path.join(WURZEL, "art", "szenen", RAUM) + os.sep
os.makedirs(OUT, exist_ok=True); os.makedirs(ZIEL, exist_ok=True)

sys.path.insert(0, HIER)
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

import werkzeug as wz  # noqa: E402

szene = importlib.import_module("szene_" + RAUM)
# Ebenen und Zonen: aus werkzeug.py oder (ältere Szenen) aus LAYER/HIT der Szene; Namen vereinheitlicht
_NAMEN = {"bg": "hinten", "mid": "mitte", "fg": "vorn"}
EBENE = {n: _NAMEN.get(e, e) for n, e in {**getattr(szene, "LAYER", {}), **wz.EBENE}.items()}
ZONE = {**getattr(szene, "HIT", {}), **wz.ZONE}
PALETTE = szene.PALETTE
OHNE_LINIE = getattr(szene, "OHNE_LINIE", set())
SONNE_AUS = getattr(szene, "SONNE_AUS", set())
OHNE_SCHATTIERUNG = getattr(szene, "OHNE_SCHATTIERUNG", set())
sc = bpy.context.scene
kamera = sc.camera


def hex_lin(s):
    c = [int(s[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


def welt(farbe, staerke=1.0):
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*farbe, 1); bg.inputs[1].default_value = staerke


def sichtbarkeit(ohne_ebenen=(), ohne_material=(), ohne_namen=()):
    """Eine Stelle entscheidet, was gerendert wird — sonst hebt eine Regel die andere wieder auf."""
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        mats = {m.name for m in o.data.materials if m}
        o.hide_render = (o.name in wz.PLATZHALTER or EBENE.get(o.name) in ohne_ebenen
                         or o.name in ohne_namen or bool(mats & set(ohne_material)))


def lichter(nur_sonne):
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.hide_render = not (nur_sonne and o.data.type == 'SUN')


def emission_ueberall(farbe_von):
    """Jedes Material leuchtet in einer festen Farbe (farbe_von(materialname) -> lineares RGB)."""
    for m in bpy.data.materials:
        if not m.node_tree: continue
        nt = m.node_tree; aus = nt.nodes.get("Material Output")
        if aus is None: continue
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.0
        em.inputs["Color"].default_value = (*farbe_von(m.name), 1)
        for l in list(aus.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(em.outputs["Emission"], aus.inputs["Surface"])


def stufen_nach_richtung(m):
    """Volumen ohne Linie: Lokalfarbe × Faktor aus der Flächennormalen — oben (+Z) heller, Seiten (±X)
    dunkler, auf 0,04 gerundet, damit keine Verläufe entstehen (ligne claire bleibt flach)."""
    nt = m.node_tree; em = [n for n in nt.nodes if n.type == 'EMISSION'][-1]
    basis = tuple(em.inputs["Color"].default_value)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    xyz = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], xyz.inputs["Vector"])

    def rechne(op, a, b=None, wert=None):
        n = nt.nodes.new("ShaderNodeMath"); n.operation = op
        nt.links.new(a, n.inputs[0])
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


def flach():
    emission_ueberall(lambda n: hex_lin(PALETTE[n]) if n in PALETTE else (0.5, 0.5, 0.5))
    for m in bpy.data.materials:
        if m.node_tree and m.name not in OHNE_SCHATTIERUNG and m.node_tree.nodes.get("Material Output"):
            stufen_nach_richtung(m)
    lichter_aus()
    welt(hex_lin(getattr(szene, "HIMMEL", "#F8E7BF")))


def lichter_aus():
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.hide_render = True


def linien(ohne_ebenen=()):
    emission_ueberall(lambda n: (1, 1, 1)); lichter_aus(); welt((1, 1, 1))
    sichtbarkeit(ohne_ebenen=ohne_ebenen, ohne_material=OHNE_LINIE)
    sc.render.resolution_x, sc.render.resolution_y = B * UEBER, H * UEBER
    sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'
    vl = sc.view_layers[0]; vl.use_freestyle = True
    fs = vl.freestyle_settings; fs.crease_angle = math.radians(120)
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("linie")
    ls.select_silhouette = True; ls.select_crease = True; ls.select_border = True; ls.select_contour = True
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new("claire")
    ls.linestyle.color = (0, 0, 0); ls.linestyle.alpha = 1.0; ls.linestyle.thickness = LINIE * UEBER
    ls.linestyle.caps = "ROUND"          # Stoßstellen der Striche (Freestyle teilt Kanten) ohne Lücke


def grau_sonne(ohne_ebenen=()):
    """Nur direkte Sonne auf grauen Flächen: hell = Sonnenfleck, sonst schwarz."""
    for m in bpy.data.materials:
        if not m.node_tree: continue
        b = m.node_tree.nodes.get("Principled BSDF")
        if b is None: continue
        for l in list(b.inputs["Base Color"].links): m.node_tree.links.remove(l)
        b.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1); b.inputs["Emission Strength"].default_value = 0.0
        b.inputs["Roughness"].default_value = 0.7; b.inputs["Metallic"].default_value = 0.0
        if "Alpha" in b.inputs: b.inputs["Alpha"].default_value = 1.0
    lichter(True); welt((0, 0, 0), 0.0); sc.cycles.max_bounces = 0
    sichtbarkeit(ohne_ebenen=ohne_ebenen, ohne_namen=SONNE_AUS)
    if hasattr(szene, "sonne_stellen"):
        for o in bpy.data.objects:
            if o.type == 'LIGHT' and o.data.type == 'SUN': szene.sonne_stellen(o)


def verdeckung(ohne_ebenen=()):
    """Umgebungsverdeckung (Reichweite 0,7 m) als Emission; das Komposit schneidet daraus eine Schattenstufe."""
    lichter_aus(); welt((1, 1, 1))
    for m in bpy.data.materials:
        if not m.node_tree: continue
        nt = m.node_tree; aus = nt.nodes.get("Material Output")
        if aus is None: continue
        ao = nt.nodes.new("ShaderNodeAmbientOcclusion"); ao.samples = 8; ao.inputs["Distance"].default_value = 0.7
        em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(ao.outputs["AO"], em.inputs["Color"])
        for l in list(aus.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(em.outputs["Emission"], aus.inputs["Surface"])
    sichtbarkeit(ohne_ebenen=ohne_ebenen)


def von_oben(nur_schatten_von=()):
    """Kontaktschatten: Sonne senkrecht von oben; Wände und Decke werfen keinen Schatten. Ausgewertet wird
    nur auf Flächen, die nach oben zeigen — alles andere bleibt weiß. Ebenen in nur_schatten_von sind für
    die Kamera unsichtbar, werfen aber ihren Schatten (Hintergrund-Variante)."""
    lichter_aus(); welt((0, 0, 0), 0.0); sc.cycles.max_bounces = 0
    for m in bpy.data.materials:
        if not m.node_tree: continue
        nt = m.node_tree; aus = nt.nodes.get("Material Output")
        if aus is None: continue
        geo = nt.nodes.new("ShaderNodeNewGeometry"); xyz = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(geo.outputs["Normal"], xyz.inputs["Vector"])
        oben = nt.nodes.new("ShaderNodeMath"); oben.operation = 'GREATER_THAN'; oben.inputs[1].default_value = 0.7
        nt.links.new(xyz.outputs["Z"], oben.inputs[0])
        diffus = nt.nodes.new("ShaderNodeBsdfDiffuse"); diffus.inputs["Color"].default_value = (1, 1, 1, 1)
        weiss = nt.nodes.new("ShaderNodeEmission"); weiss.inputs["Color"].default_value = (1, 1, 1, 1)
        pfad = nt.nodes.new("ShaderNodeLightPath")   # weiß nur für die Kamera, sonst hellt es den Schatten auf
        nt.links.new(pfad.outputs["Is Camera Ray"], weiss.inputs["Strength"])
        mix = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(oben.outputs[0], mix.inputs[0])
        nt.links.new(weiss.outputs[0], mix.inputs[1]); nt.links.new(diffus.outputs[0], mix.inputs[2])
        for l in list(aus.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(mix.outputs[0], aus.inputs["Surface"])
    bpy.ops.object.light_add(type='SUN'); oben_licht = bpy.context.object
    oben_licht.data.energy = 30.0; oben_licht.data.angle = math.radians(2.0); oben_licht.rotation_euler = (0, 0, 0)
    sichtbarkeit()
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        ebene = EBENE.get(o.name)
        o.visible_shadow = ebene != "hinten"            # Raum, Wandschmuck: kein Schatten von oben
        o.visible_camera = ebene not in nur_schatten_von


def maske():
    emission_ueberall(lambda n: (0, 0, 0)); lichter_aus(); welt((0, 0, 0))
    weiss = bpy.data.materials.new("maske_weiss"); weiss.use_nodes = True
    wn = weiss.node_tree; e = wn.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = (1, 1, 1, 1)
    for l in list(wn.nodes["Material Output"].inputs["Surface"].links): wn.links.remove(l)
    wn.links.new(e.outputs["Emission"], wn.nodes["Material Output"].inputs["Surface"])
    for o in bpy.data.objects:
        if o.type == 'MESH' and EBENE.get(o.name) == "mitte":
            for i in range(len(o.data.materials)): o.data.materials[i] = weiss
    sichtbarkeit()


def render(name, proben, entrauschen=False):
    sc.cycles.samples = proben; sc.cycles.use_denoising = entrauschen
    pfad = OUT + name; sc.render.filepath = pfad
    t = time.time(); bpy.ops.render.render(write_still=True)
    if sc.render.resolution_x != B:          # überabgetastet: auf Bühnengröße mitteln
        from PIL import Image
        Image.open(pfad).convert("RGB").reduce(UEBER).save(pfad)
    print(f"RENDER {name} {time.time() - t:.1f}s", flush=True)


def klickzonen():
    """Klickzonen = Bildrechteck der Objekte je Zone, in Bühnenpixeln (1600x900)."""
    sc.render.resolution_x, sc.render.resolution_y = B, H
    dg = bpy.context.evaluated_depsgraph_get()
    zonen = {}
    for zone, namen in ZONE.items():
        xs, ys = [], []
        for n in namen:
            o = bpy.data.objects[n].evaluated_get(dg)
            for v in o.bound_box:
                p = world_to_camera_view(sc, kamera, o.matrix_world @ Vector(v))
                xs.append(p.x * B); ys.append((1 - p.y) * H)
        zonen[zone] = [max(0, round(min(xs))), max(0, round(min(ys))), min(B, round(max(xs))), min(H, round(max(ys)))]
    with open(ZIEL + "hitboxes.json", "w", encoding="utf-8") as f:
        json.dump(zonen, f, indent=1)
    print("KLICKZONEN", json.dumps(zonen), flush=True)


sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = B, H, 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
sc.render.dither_intensity = 0.0     # kein Rauschen: es würde im Komposit zu Tintenkorn verstärkt

HINTEN = ("mitte", "vorn")
if DURCHGANG == "flat":
    flach(); sichtbarkeit(); render("pass_flat.png", 4); klickzonen()
elif DURCHGANG == "flatbg":
    flach(); sichtbarkeit(ohne_ebenen=HINTEN); render("pass_flat_bg.png", 4)
elif DURCHGANG == "lines":
    linien(); render("pass_lines.png", 4)
elif DURCHGANG == "linesbg":
    linien(ohne_ebenen=HINTEN); render("pass_lines_bg.png", 4)
elif DURCHGANG == "linesmid":
    linien(ohne_ebenen=("hinten", "vorn")); render("pass_lines_mid.png", 4)
elif DURCHGANG == "mask":
    maske(); render("mask_mid.png", 4)
elif DURCHGANG == "sun":
    grau_sonne(); render("pass_sun.png", 16, True)
elif DURCHGANG == "sunbg":
    grau_sonne(ohne_ebenen=HINTEN); render("pass_sunbg.png", 16, True)
elif DURCHGANG == "ao":
    verdeckung(); render("pass_ao.png", 24, True)
elif DURCHGANG == "aobg":
    verdeckung(ohne_ebenen=HINTEN); render("pass_aobg.png", 24, True)
elif DURCHGANG == "kontakt":
    von_oben(); render("pass_kontakt.png", 8)
elif DURCHGANG == "kontaktbg":
    von_oben(nur_schatten_von=HINTEN); render("pass_kontaktbg.png", 8)
elif DURCHGANG == "boxes":
    klickzonen()
else:
    print("FEHLER: unbekannter Durchgang", DURCHGANG); sys.exit(2)
