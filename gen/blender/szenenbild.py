"""Szenenbilder: illustrierte Nahaufnahmen für Gesprächsanfänge — ohne Klickzonen, in Ich-Perspektive.

    BLENDER_THREADS=2 python3 gen/blender/szenenbild.py aufnahme tresen           # Durchgänge + Vorlage
    python3 gen/blender/szenenbild.py aufnahme tresen --komposit                  # nur neu zusammensetzen (ohne Blender)
    BLENDER_THREADS=2 python3 gen/blender/szenenbild.py aufnahme tresen --durchgang sun,lampe   # nur diese Durchgänge, dann Komposit
    BLENDER_THREADS=2 python3 gen/blender/szenenbild.py aufnahme tresen --probe   # Fläche + Linie klein (Kamera prüfen)

Grundsatz: Blender rechnet das Licht, der Bildgenerator malt nur. Die Vorlage (`art/szenenbilder/<raum>_<einstellung>/
vorlage.png`) ist dasselbe Ligne-claire-Komposit wie die Räume — Lokalfarbe, Kontaktschatten, Sonnenstreifen, Lampeninsel,
Tuschelinie — nur aus einer anderen Kamera und mit den Figuren-Blockouts (figuren.py) im Raum. Daneben liegen die
Lichtmasken aus Blender (`sonne.png`, `lampe.png`), an denen `licht_pruefen.py` das gemalte Ergebnis misst, `quellen.png`
(Leuchtflächen: Himmel, Sonne, Flur — zählen dort nicht als Fremdlicht) und `tiefe.png` / `maske.png` (Figuren). `malen.py` malt die Vorlage aus (fal Kontext oder
OpenAI GPT Image, Stilphrase `stil/szenenbild.txt`).

Dieselbe Szene, dieselbe Sonne (`szene.sonne_stellen()`), dieselben Figuren wie im Raumbild; nur Kamera und Haltungen
kommen aus EINSTELLUNG hier. Zwischenergebnisse: bau/blender/szenenbilder/<raum>_<einstellung>/.
"""
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, HIER)

B, H = 1920, 1080          # Szenenbild 16:9
UEBER = 2                  # Überabtastung des Linien-Durchgangs
LINIE = 1.8                # Strichstärke in Pixeln des fertigen Bildes

# Je Raum und Einstellung: Kamera (Ort in Metern, Augenhöhe), Gier (Grad, + nach rechts), Neigung (Grad, − nach unten),
# Brennweite (mm, Sensor 36 mm) und die Figuren mit Ort, Haltung und Blick (`blick="kamera"`: zur Kamera gedreht,
# `drehung` ein fester Winkel). Figuren ohne Eintrag stehen wie in figuren.PLATZ.
EINSTELLUNG = {
    "aufnahme": {
        # Ich-Perspektive über den Tresen, nach dem Vorbild art/referenz/chatgpt_aufnahme_marlene.png: Marlene groß links,
        # reicht die Mappe zur Kamera, hinter ihr das Fenster mit der tiefen Sonne, rechts klein Herr K. auf der Bank, der
        # EKG-Wagen daneben. Geometrie des Raums: der Tresen (x −4,1…−1,7) liegt ganz links vom Fenster (x −1,25…1,45),
        # und die Gelenklampe steht am rechten Tresenende (x −2,15). Von einer Kamera rechts der Lampe liegt das Fenster
        # immer rechts neben Marlene; von einer Kamera links der Lampe hängt der Lampenarm vor ihrem Gesicht. Der
        # Kompromiss: die Spielerin steht links vor dem Tresen (zwischen PC und Lampe), schaut schräg nach rechts an der
        # Lampe vorbei; Marlene steht am äußersten rechten Tresenende, die linke Schulter schon über der Wange. So beginnt
        # das Fenster an ihrer linken Schulter, die Sonnenscheibe steht dicht neben ihr, Herr K. passt auf dem ersten Sitz
        # (der Bank nächstes Ende zum Fenster) mit 32 mm gerade noch ganz ins Bild. Was Blender für diese Kamera ergibt:
        # die Sonne (szene.sonne_stellen, nach links-vorn) erreicht hinter dem Tresen nur Marlenes linke Schulter und den
        # ausgestreckten Arm; Streifen liegen auf dem Wagen, der Fensterbank und dem rechten Ende der Ablage.
        "tresen": dict(
            kamera=(-2.5, -2.5, 1.58), gier=40.0, neigung=-9.0, brennweite=30.0,
            figuren={
                "marlene": dict(ort=(-1.66, -0.45, 0.0), haltung="reicht_mappe", blick="kamera", tresen=1.09,
                                kanne_welt=(-2.18, -1.40, 1.09 + 0.125)),  # Kanne (Raumkoordinaten) abgestellt auf der Ablage der Sichtblende (1,09 m), vor der Lampenklemme — links neben der Mappe wie im Vorbild
                # (nicht auf die Arbeitsfläche dahinter: dort liefe der Blick knapp durch den Spalt zwischen Fase der
                # Sichtblende und Plattenunterseite, und Freestyle zeichnete die verdeckte Kanne durch die Platte)
                "herrk": dict(ort=(1.1, -0.75, 0.0), drehung=-14),   # erster Sitz der Wartereihe (im Spiel: dritter), Tüte daneben
            },
            # Raumobjekte nur für dieses Szenenbild verschieben (Klickzonen-Gruppen aus szene_aufnahme.HIT, Versatz in
            # Metern): der EKG-Wagen von vor der Bank unter das rechte Fensterende, die Tüte neben Herrn K.s ersten Sitz.
            objekte={"wagen": (-0.45, 0.85, 0.0), "tuete": (-1.27, 0.17, 0.0)},
            # Die Sonnenscheibe draußen ist Kulisse (40 m hinter dem Fenster): sie wird so gerückt, dass sie aus dieser
            # Kamera an dieser Stelle der Fensterebene (x, z in Metern) steht — tief, dicht neben Marlenes Schulter. Das
            # Licht selbst kommt unverändert aus szene.sonne_stellen().
            sonne_im_fenster=(-0.7, 1.52),
            lampe_ziel=(-1.95, -1.4, 1.09),       # wohin die Tischlampe leuchtet: Ablage der Sichtblende bei Kanne und Mappe
            # Licht im Komposit: Sonne wie komposit.EINSTELLUNG["aufnahme"], dazu die Lampe als warme Insel
            licht=dict(sonne="#FFF0C6", anteil=0.5, schwelle=0.35, weich=0.6, lampe="#FFE3B0", lampe_anteil=0.38,
                       lampe_schwelle=0.18, lampe_weich=6.0, kontakt=True),
        ),
    },
}

TINTE = np.array([0x1E / 255, 0x2A / 255, 0x30 / 255], np.float32)
SCHATTEN = np.array([0x2C / 255, 0x55 / 255, 0x60 / 255], np.float32)


def hexc(s): return np.array([int(s[i:i + 2], 16) / 255 for i in (1, 3, 5)], np.float32)


# ================================================================== Bildhilfen
def lade(p, alpha=False, grau=False):
    im = Image.open(p).convert("RGBA" if alpha else ("L" if grau else "RGB"))
    return np.asarray(im).astype(np.float32) / 255


def luma(a): return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def weich(m, r):
    if r <= 0: return m
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255


def median(m, k):
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(k))).astype(np.float32) / 255


def oeffnen(m, k):
    b = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    return (np.asarray(b) > 127).astype(np.float32)


def bild(a, modus="RGB"): return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), modus)


def grau_png(m, pfad): Image.fromarray((np.clip(m, 0, 1) * 255 + 0.5).astype(np.uint8), "L").save(pfad, optimize=True)


# ================================================================== Blender-Teil
def blender_laden():
    global bpy, Vector, ef, fz, figuren, wz
    import bpy
    from mathutils import Vector
    import figuren_zeichnen as fz
    fz.blender_laden()                     # importiert ebenen_figuren als Modul (argv „modul") und figuren
    ef, figuren = fz.ef, fz.figuren
    import werkzeug as wz


def aufbau(raum, e):
    """Raum aus der Szenendatei, Figuren nach EINSTELLUNG (sonst figuren.PLATZ), Kamera. Gibt die Namen zurück, die
    nie gerendert werden (reine Platzhalter), die Leuchtflächen draußen (werfen keinen Schatten), sonne_stellen und die
    Palette/Schattierungs-Ausnahmen der Szene."""
    if raum != "aufnahme":
        raise SystemExit(f"Szenenbilder gibt es bisher nur für die Aufnahme (nicht {raum})")
    ns = {"__file__": os.path.join(HIER, "szene_aufnahme.py"), "__name__": "szene_aufnahme"}
    _argv = sys.argv; sys.argv = ["x", "lit"]
    try: exec(open(ns["__file__"], encoding="utf-8").read(), ns)
    finally: sys.argv = _argv
    sc = bpy.context.scene; ef.render_grund(B, H); G, tag = ns["G"], ns["_tag"]
    bpy.data.objects["bag"].data.materials[0] = G["paper"]; bpy.data.objects["folder"].data.materials[0] = G["paper"]
    ef.PAL.update(ns["PALETTE"])
    kam = Vector(e["kamera"])
    figs = {}
    for name, bau in (("marlene", figuren.marlene), ("herrk", figuren.herr_k)):
        p = dict(figuren.PLATZ[name]); p.update(e["figuren"].get(name, {}))
        ort = Vector(p["ort"])
        if p.get("blick") == "kamera":                      # Gesicht (lokal −y) zur Kamera
            d = kam - ort; p["drehung"] = math.degrees(math.atan2(d.x, -d.y)) + p.get("drehung_dazu", 0.0)
        if name == "marlene" and "kanne_welt" in p:            # Kanne in Raumkoordinaten -> Figurkoordinaten
            kw = Vector(p["kanne_welt"]) - ort; r = -math.radians(p["drehung"])
            p["kanne"] = (kw.x * math.cos(r) - kw.y * math.sin(r), kw.x * math.sin(r) + kw.y * math.cos(r), kw.z)
        extra = {k: p[k] for k in ("tresen", "kanne") if k in p and name == "marlene"}
        figs[name] = bau(tuple(ort), drehung=p["drehung"], haltung=p["haltung"], tag=tag, fein=0.0055, **extra)
        print(f"FIGUR {name} ort={tuple(round(v, 2) for v in ort)} drehung={p['drehung']:.1f} haltung={p['haltung']}")
    tuete = [bpy.data.objects[n] for n in ns["HIT"].get("tuete", [])]
    for o in tuete: ef.ZUORDNUNG[o.name] = "tuete"
    for gruppe, (dx, dy, dz) in e.get("objekte", {}).items():      # Raumobjekte nur für dieses Bild umstellen
        for n in ns["HIT"].get(gruppe, []):
            o = bpy.data.objects[n]; o.location = (o.location.x + dx, o.location.y + dy, o.location.z + dz)
        print(f"OBJEKTE {gruppe} um ({dx:+.2f}, {dy:+.2f}, {dz:+.2f}) verschoben")
    nie = set(wz.PLATZHALTER) - set(ef.ZUORDNUNG)
    aus = set(ns.get("SONNE_AUS", set()))
    # Tresenplatte fein unterteilen (Subdivision „simple", nur im Szenenbild): aus der Nahkamera ließ Freestyle in einem
    # schmalen Band Kanten hinter der Platte durch (Hinterkante der Arbeitsfläche, Marlenes Beine, Striche auf der
    # Ablage); mit der unterteilten Platte (viele kleine statt zwei großer Flächen) hält die Sichtbarkeitsprüfung
    # dicht. Geometrie und Linienbild der Platte ändern sich nicht (ebene Flächen bleiben eben, keine Falten).
    platte = bpy.data.objects.get("desk_top")
    if platte is not None:
        md = platte.modifiers.new("unterteilen", 'SUBSURF'); md.subdivision_type = 'SIMPLE'; md.levels = md.render_levels = 4
    # Lampe: der Spot sitzt im Lampenkopf und leuchtet auf die Arbeitsfläche vor Marlene (Lampeninsel um Kanne und Mappe).
    # Die Szene stellt ihn für ihre eigene Vorschau anders; hier zählt, was man im Bild sieht.
    kopf = bpy.data.objects.get("lamp_head")
    spot = next((o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SPOT'), None)
    if kopf is not None and spot is not None:
        spot.location = (kopf.location.x, kopf.location.y, kopf.location.z - 0.06)
        ziel = Vector(e.get("lampe_ziel", (kopf.location.x + 0.3, kopf.location.y - 0.15, 0.75)))
        spot.rotation_euler = (ziel - spot.location).to_track_quat('-Z', 'Y').to_euler()
        spot.data.spot_size = math.radians(70); spot.data.spot_blend = 0.6; spot.data.energy = 120
    # Sonnenscheibe draußen (Kulisse) auf den Strahl Kamera -> Fensterpunkt legen, in ihrer alten Entfernung
    scheibe = bpy.data.objects.get("aussen_sonne")
    if scheibe is not None and e.get("sonne_im_fenster"):
        fx, fz_ = e["sonne_im_fenster"]; richtung = (Vector((fx, 0.0, fz_)) - kam)
        scheibe.location = kam + richtung * ((scheibe.location.y - kam.y) / richtung.y)
    # Kamera: Augenhöhe, Gier nach rechts, Neigung nach unten
    bpy.ops.object.camera_add(location=tuple(kam)); cam = bpy.context.object; sc.camera = cam
    cam.rotation_euler = (math.radians(90 + e["neigung"]), 0, math.radians(-e["gier"]))
    cam.data.lens = e["brennweite"]; cam.data.sensor_width = 36; cam.data.sensor_fit = 'HORIZONTAL'
    cam.data.clip_start = 0.05
    ebene = {**ns.get("LAYER", {}), **wz.EBENE}
    return dict(figs=figs, nie=nie, aus=aus, sonne_stellen=ns.get("sonne_stellen", lambda s: None), ns=ns,
                hinten={n for n, eb in ebene.items() if eb in ("bg", "hinten")},
                ohne_linie=set(ns.get("OHNE_LINIE", set())), ohne_schattierung=set(ns.get("OHNE_SCHATTIERUNG", set())),
                himmel=ns.get("HIMMEL", "#F8E7BF"), spot=spot.name if spot else None)


def stufen(ohne):
    """Wie ebenen.stufen_nach_richtung: Lokalfarbe × Faktor aus der Flächennormalen (oben heller, Seiten dunkler),
    auf 0,04 gerundet — nur Raummaterialien, die Figuren bleiben flach wie in ebenen_figuren.py."""
    for m in bpy.data.materials:
        if not m.use_nodes or m.name in ohne or m.name.startswith("fig_") or m.name not in ef.PAL: continue
        nt = m.node_tree; em = nt.nodes.get("ebene_em")
        if em is None or nt.nodes.get("stufen_mix"): continue
        basis = tuple(em.inputs["Color"].default_value)
        geo = nt.nodes.new("ShaderNodeNewGeometry"); xyz = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], xyz.inputs["Vector"])

        def rechne(op, a, wert):
            n = nt.nodes.new("ShaderNodeMath"); n.operation = op; nt.links.new(a, n.inputs[0]); n.inputs[1].default_value = wert; return n.outputs[0]
        fx = rechne('MULTIPLY', rechne('ABSOLUTE', xyz.outputs["X"], 0), -0.14)
        fz_ = rechne('MULTIPLY', xyz.outputs["Z"], 0.10)
        add = nt.nodes.new("ShaderNodeMath"); add.operation = 'ADD'; nt.links.new(fz_, add.inputs[0]); nt.links.new(fx, add.inputs[1])
        faktor = rechne('SNAP', rechne('ADD', add.outputs[0], 1.0), 0.04)
        mix = nt.nodes.new("ShaderNodeMix"); mix.name = "stufen_mix"; mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
        mix.inputs["Factor"].default_value = 1.0; mix.inputs[6].default_value = basis
        grau = nt.nodes.new("ShaderNodeCombineColor")
        for i in range(3): nt.links.new(faktor, grau.inputs[i])
        nt.links.new(grau.outputs["Color"], mix.inputs[7]); nt.links.new(mix.outputs[2], em.inputs["Color"])


def stufen_weg():
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        em = m.node_tree.nodes.get("ebene_em")
        if em:
            for l in list(em.inputs["Color"].links): m.node_tree.links.remove(l)


def pass_linien(pfad, sichtbar, fein):
    """Freestyle über alles außer der Sammlung der Gesichtsteile (sonst doppelt so dick), doppelt aufgelöst."""
    sc = bpy.context.scene
    ef.material_flach(weiss=True); ef.lichter(lambda o: False); ef.welt((1, 1, 1), 1.0); sc.cycles.max_bounces = 0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        o.is_holdout = False; o.hide_render = not sichtbar(o)
        if o.data.materials and o.data.materials[0] and o.data.materials[0].name == "slat": o.hide_render = True
    ef.LINIE = LINIE * UEBER
    ef.freestyle(True, None)
    vl = sc.view_layers[0]; ls = vl.freestyle_settings.linesets[0]
    ls.select_by_collection = fein is not None
    if fein is not None: ls.collection = fein; ls.collection_negation = 'EXCLUSIVE'
    sc.render.resolution_x, sc.render.resolution_y = B * UEBER, H * UEBER
    try: ef.render(pfad, 4, False)
    finally:
        sc.render.resolution_x, sc.render.resolution_y = B, H; ef.LINIE = 1.5
        ls.select_by_collection = False
    Image.open(pfad).convert("RGB").reduce(UEBER).save(pfad)


def pass_lampe(pfad, sichtbar, spot):
    """Nur die Tischlampe (Objektname `spot`) auf grauen Flächen: die Lampeninsel."""
    sc = bpy.context.scene
    ef.material_grau(); ef.welt((0, 0, 0), 0.0); sc.cycles.max_bounces = 0
    ef.lichter(lambda o: o.name == spot)                 # nach Name: bpy liefert je Zugriff einen neuen Wrapper, `is` greift nicht
    for n in ("dawn", "corridor", "screen", "sonne"):
        if n in bpy.data.materials:
            b = bpy.data.materials[n].node_tree.nodes.get("Principled BSDF")
            if b: b.inputs["Emission Strength"].default_value = 0.0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        o.is_holdout = False; o.hide_render = not sichtbar(o)
    ef.freestyle(False); ef.render(pfad, 16, True)


def pass_kontakt(pfad, sichtbar, hinten):
    """Wie ebenen.von_oben: Sonne senkrecht von oben, Schatten nur auf nach oben gewandten Flächen; der Hintergrund
    (Raumhülle, Wandschmuck, Fenster — Ebene `hinten`) wirft keinen Schatten — flache Formen unter Möbeln und Figuren."""
    sc = bpy.context.scene
    ef.lichter(lambda o: False); ef.welt((0, 0, 0), 0.0); sc.cycles.max_bounces = 0
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt = m.node_tree; aus = nt.nodes.get("Material Output")
        if aus is None: continue
        geo = nt.nodes.new("ShaderNodeNewGeometry"); xyz = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], xyz.inputs["Vector"])
        oben = nt.nodes.new("ShaderNodeMath"); oben.operation = 'GREATER_THAN'; oben.inputs[1].default_value = 0.7; nt.links.new(xyz.outputs["Z"], oben.inputs[0])
        diffus = nt.nodes.new("ShaderNodeBsdfDiffuse"); diffus.inputs["Color"].default_value = (1, 1, 1, 1)
        weiss = nt.nodes.new("ShaderNodeEmission"); weiss.inputs["Color"].default_value = (1, 1, 1, 1)
        pfad_n = nt.nodes.new("ShaderNodeLightPath"); nt.links.new(pfad_n.outputs["Is Camera Ray"], weiss.inputs["Strength"])
        mix = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(oben.outputs[0], mix.inputs[0])
        nt.links.new(weiss.outputs[0], mix.inputs[1]); nt.links.new(diffus.outputs[0], mix.inputs[2])
        for l in list(aus.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(mix.outputs[0], aus.inputs["Surface"])
    bpy.ops.object.light_add(type='SUN'); oben_licht = bpy.context.object; oben_licht.name = "kontakt_sonne"
    oben_licht.data.energy = 30.0; oben_licht.data.angle = math.radians(2.0); oben_licht.rotation_euler = (0, 0, 0)
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        o.is_holdout = False; o.hide_render = not sichtbar(o)
        o.visible_shadow = o.name not in hinten
    ef.freestyle(False)
    try: ef.render(pfad, 8, False)
    finally:
        bpy.data.objects.remove(oben_licht, do_unlink=True)
        for o in bpy.data.objects:
            if o.type == 'MESH': o.visible_shadow = True


QUELLEN = {"himmel_oben", "himmel_mitte", "himmel_unten", "sonne", "corridor", "screen"}   # Leuchtflächen (Materialnamen)


def pass_maske(pfad, sichtbar, weiss=lambda n: n.startswith("fig_")):
    """Materialien, für die weiss(name) gilt, weiß; alles andere schwarz (Figuren bzw. Leuchtflächen)."""
    ef.material_flach(schwarz=True)
    for m in bpy.data.materials:
        if m.use_nodes and weiss(m.name):
            em = m.node_tree.nodes.get("ebene_em")
            if em: em.inputs["Color"].default_value = (1, 1, 1, 1)
    sc = bpy.context.scene; ef.lichter(lambda o: False); ef.welt((0, 0, 0), 1.0); sc.cycles.max_bounces = 0
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        o.is_holdout = False; o.hide_render = not sichtbar(o)
    ef.freestyle(False); ef.render(pfad, 4, False)


def rendern(raum, einstellung, e, out, probe=False):
    blender_laden(); A = aufbau(raum, e)
    nie, aus = A["nie"], A["aus"]
    sichtbar = lambda o: o.name not in nie
    ohne_linie = A["ohne_linie"]
    sichtbar_linie = lambda o: o.name not in nie and not any(m and m.name in ohne_linie for m in o.data.materials)
    sichtbar_sonne = lambda o: o.name not in nie and o.name not in aus
    fein = bpy.data.collections.get("figuren_fein")
    if probe:   # klein, nur Fläche und Linie: Kamera und Haltung prüfen; mit --licht auch die Sonne (gelb getönt)
        global B, H, UEBER, LINIE; B, H, UEBER, LINIE = B // 4, H // 4, 1, 1.0
        ef.render_grund(B, H)
        ef.material_flach(); stufen(A["ohne_schattierung"]); ef.pass_flach(out + "probe_flat.png", sichtbar); stufen_weg()
        pass_linien(out + "probe_lines.png", sichtbar_linie, fein)
        flach = lade(out + "probe_flat.png", True); linien = lade(out + "probe_lines.png")
        col = hexc(A["himmel"]) * (1 - flach[..., 3:4]) + flach[..., :3] * flach[..., 3:4]
        if "--licht" in sys.argv:
            ef.pass_sonne(out + "probe_sun.png", sichtbar_sonne, stellen=A["sonne_stellen"])
            L = e["licht"]; s = (luma(lade(out + "probe_sun.png")) > L["schwelle"]).astype(np.float32)[..., None]
            col = col * (1 - s * 0.7) + np.array([1.0, 0.85, 0.1], np.float32) * s * 0.7
        t = np.clip((1 - luma(linien)) * 1.3, 0, 1)[..., None]
        bild(col * (1 - t) + TINTE * t).save(out + "probe.png"); print("saved", out + "probe.png"); return
    nur = sys.argv[sys.argv.index("--durchgang") + 1].split(",") if "--durchgang" in sys.argv else None   # einzelne Durchgänge
    will = lambda n: nur is None or n in nur
    if will("flat"):
        ef.material_flach(); stufen(A["ohne_schattierung"])
        ef.pass_flach(out + "pass_flat.png", sichtbar); stufen_weg()
        open(out + "himmel.txt", "w").write(A["himmel"])
    if will("lines"): pass_linien(out + "pass_lines.png", sichtbar_linie, fein)
    if will("tiefe"): fz.pass_tiefe(out + "pass_tiefe.png", sichtbar, nah=0.3, fern=12.0)
    if will("maske"): pass_maske(out + "pass_maske.png", sichtbar)
    if will("quellen"): pass_maske(out + "pass_quellen.png", sichtbar, weiss=lambda n: n in QUELLEN)
    if will("kontakt"): pass_kontakt(out + "pass_kontakt.png", sichtbar, A["hinten"])
    if will("sun"): ef.pass_sonne(out + "pass_sun.png", sichtbar_sonne, stellen=A["sonne_stellen"])
    if will("lampe"): pass_lampe(out + "pass_lampe.png", sichtbar, A["spot"])


# ================================================================== Komposit (ohne Blender)
def komposit(e, out, ziel):
    L = e["licht"]
    flach = lade(out + "pass_flat.png", True)
    himmel = open(out + "himmel.txt").read().strip() if os.path.exists(out + "himmel.txt") else "#F8E7BF"
    col = hexc(himmel) * (1 - flach[..., 3:4]) + flach[..., :3] * flach[..., 3:4]
    # Kontaktschatten: eine flache Stufe Richtung Petrol (wie komposit.farbe)
    if L.get("kontakt") and os.path.exists(out + "pass_kontakt.png"):
        k = oeffnen((luma(lade(out + "pass_kontakt.png")) < 0.5).astype(np.float32), 5)
        sch = weich(k, 0.8)[..., None]
        col = col * (1 - sch) + (col * 0.86 * 0.84 + SCHATTEN * 0.16 * 0.86) * sch
    # Sonne: schmale Rampe an der Schwelle, Median gegen Rauschen, leicht weich — dieselbe Rechnung wie im Raum
    ls = luma(lade(out + "pass_sun.png"))
    sonne = median(np.clip((ls - L["schwelle"]) / 0.08 + 0.5, 0, 1), 5)
    sonne = weich(sonne, L["weich"])
    col = col * (1 - sonne[..., None] * L["anteil"]) + hexc(L["sonne"]) * sonne[..., None] * L["anteil"]
    # Lampe: weiche warme Insel auf der Arbeitsfläche (Spot, normiert auf sein Maximum)
    lampe = np.zeros_like(ls)
    if os.path.exists(out + "pass_lampe.png"):
        ll = luma(lade(out + "pass_lampe.png")); ll = ll / (np.percentile(ll, 99.7) + 1e-6)
        lampe = weich(median(np.clip((ll - L["lampe_schwelle"]) / 0.25, 0, 1), 5), L["lampe_weich"])
        col = col * (1 - lampe[..., None] * L["lampe_anteil"]) + hexc(L["lampe"]) * lampe[..., None] * L["lampe_anteil"]
    # Tusche
    t = np.clip(((1 - luma(lade(out + "pass_lines.png"))) - 0.03) / 0.97 * 1.25, 0, 1)[..., None]
    col = col * (1 - t) + TINTE * t
    os.makedirs(ziel, exist_ok=True)
    bild(col).save(ziel + "vorlage.png", optimize=True)
    grau_png(sonne, ziel + "sonne.png"); grau_png(lampe, ziel + "lampe.png")
    for n in ("pass_maske.png", "pass_quellen.png", "pass_tiefe.png"):
        if os.path.exists(out + n):
            Image.open(out + n).convert("L").save(ziel + n.replace("pass_", ""), optimize=True)
    for n in ("vorlage.png", "sonne.png", "lampe.png"):
        print("gespeichert", os.path.relpath(ziel + n, WURZEL), f"{os.path.getsize(ziel + n) // 1024} kB")


def main():
    if len(sys.argv) < 3 or sys.argv[1].startswith("-"):
        print(__doc__); sys.exit(1)
    raum, einstellung = sys.argv[1], sys.argv[2]
    e = EINSTELLUNG.get(raum, {}).get(einstellung)
    if e is None: sys.exit(f"keine Einstellung {raum}/{einstellung} (siehe EINSTELLUNG in szenenbild.py)")
    e = dict(e)
    for k, wandeln in (("kamera", lambda s: tuple(float(v) for v in s.split(","))), ("gier", float), ("neigung", float), ("brennweite", float)):
        if f"--{k}" in sys.argv: e[k] = wandeln(sys.argv[sys.argv.index(f"--{k}") + 1])   # zum Ausprobieren (--probe)
    name = f"{raum}_{einstellung}"
    if "--name" in sys.argv: name = sys.argv[sys.argv.index("--name") + 1]
    out = os.path.join(WURZEL, "bau", "blender", "szenenbilder", name) + os.sep; os.makedirs(out, exist_ok=True)
    ziel = os.path.join(WURZEL, "art", "szenenbilder", name) + os.sep
    t = time.time()
    if "--probe" in sys.argv:
        rendern(raum, einstellung, e, out, probe=True); return
    if "--komposit" not in sys.argv:
        rendern(raum, einstellung, e, out)
    komposit(e, out, ziel)
    print(f"fertig {time.time() - t:.0f}s")


if __name__ == "__main__":
    main()
