"""Приёмная в стиле ligne claire: проходы flat / lit / lines / mask / boxes поверх базовой геометрии."""
import bpy, sys, json, math, time, os
from mathutils import Vector
MODE = sys.argv[1] if len(sys.argv) > 1 else "flat"
HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))
OUT = os.path.join(WURZEL, "bau", "blender", "aufnahme") + os.sep; os.makedirs(OUT, exist_ok=True)
base = open(os.path.join(HIER, "szene_aufnahme.py"), encoding="utf-8").read().split("# (рендер-проходы")[0]
_MODE, _OUT = MODE, OUT
sys.argv = ["x", "lit"]  # базовый скрипт ничего не рендерит до маркера
exec(base)
MODE, OUT = _MODE, _OUT   # базовый файл перезаписывает MODE и OUT
sc = bpy.context.scene

hexc = lambda s: tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))
# палитра ligne claire: приглушённая, светлая, один ржавый акцент
PAL = {
    "wall": "#EFE6D3", "cornice": "#F7F1E4", "wall_low": "#BFD9CF", "ceiling": "#DDD6C4", "floor": "#DCD3C0",
    "wood": "#C99A5B", "paper": "#F7F1E4", "cork": "#B98B5A", "dark": "#2C3E46", "mid": "#2C5560",
    "metal": "#8A9598", "glass": "#EAF1F2", "slat": "#F4EBD8", "screen": "#CDEBDA", "lampshade": "#2C3E46",
    "accent": "#B5552D", "dawn": "#F8E7BF", "corridor": "#F3D9A8", "ground": "#CFD9C2",
}
# пакет (Tüte) — объект истории: белая бумага, ручка ржавая; папка на стойке обычная бумага
bpy.data.objects["bag"].data.materials[0] = G["paper"]
bpy.data.objects["folder"].data.materials[0] = G["paper"]

def srgb_to_lin(c): return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)

# лёгкий поворот камеры: три четверти, чуть справа, чтобы была глубина, но всё читалось
cam = sc.camera; cam.location = (1.3, -7.5, 1.35)
cam.rotation_euler = (Vector((-0.45, 0.0, 1.2)) - cam.location).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = 30

def hide_layer(layers_hidden):
    for o in bpy.data.objects:
        if o.name in LAYER: o.hide_render = LAYER[o.name] in layers_hidden

def set_flat():
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt = m.node_tree; out = nt.nodes.get("Material Output"); b = nt.nodes.get("Principled BSDF")
        if out is None: continue
        col = PAL.get(m.name)
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.0
        base = (*srgb_to_lin(hexc(col)), 1) if col else (0.5, 0.5, 0.5, 1)
        if m.name in ("dawn", "corridor", "screen", "glass"):
            em.inputs["Color"].default_value = base
        else:
            # Volumen ohne Linie: Faktor nach Flächenrichtung, in Stufen (ligne claire: flach, nicht weich)
            geo = nt.nodes.new("ShaderNodeNewGeometry")
            sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Normal"], sep.inputs["Vector"])
            # oben (+Z) hell, vorn (-Y) neutral, Seiten (±X) dunkler, unten dunkel
            absx = nt.nodes.new("ShaderNodeMath"); absx.operation = 'ABSOLUTE'; nt.links.new(sep.outputs["X"], absx.inputs[0])
            fz = nt.nodes.new("ShaderNodeMath"); fz.operation = 'MULTIPLY'; fz.inputs[1].default_value = 0.10; nt.links.new(sep.outputs["Z"], fz.inputs[0])
            fx = nt.nodes.new("ShaderNodeMath"); fx.operation = 'MULTIPLY'; fx.inputs[1].default_value = -0.14; nt.links.new(absx.outputs[0], fx.inputs[0])
            fsum = nt.nodes.new("ShaderNodeMath"); fsum.operation = 'ADD'; nt.links.new(fz.outputs[0], fsum.inputs[0]); nt.links.new(fx.outputs[0], fsum.inputs[1])
            fac = nt.nodes.new("ShaderNodeMath"); fac.operation = 'ADD'; fac.inputs[1].default_value = 1.0; nt.links.new(fsum.outputs[0], fac.inputs[0])
            # auf Stufen runden (0.04), damit keine Verläufe entstehen
            snap = nt.nodes.new("ShaderNodeMath"); snap.operation = 'SNAP'; snap.inputs[1].default_value = 0.04; nt.links.new(fac.outputs[0], snap.inputs[0])
            mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'; mix.inputs["Factor"].default_value = 1.0
            mix.inputs[6].default_value = base
            comb = nt.nodes.new("ShaderNodeCombineColor")
            for i in range(3): nt.links.new(snap.outputs[0], comb.inputs[i])
            nt.links.new(comb.outputs["Color"], mix.inputs[7])
            nt.links.new(mix.outputs[2], em.inputs["Color"])
        for l in list(out.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.hide_render = True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (*srgb_to_lin(hexc("#F8E7BF")), 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def set_grey():
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        b = m.node_tree.nodes.get("Principled BSDF")
        if b is None: continue
        for l in list(b.inputs["Base Color"].links): m.node_tree.links.remove(l)
        b.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1); b.inputs["Emission Strength"].default_value = 0.0
        b.inputs["Roughness"].default_value = 0.7; b.inputs["Metallic"].default_value = 0.0
    # окно и коридор остаются светящимися, они — источники
    for n in ("dawn", "corridor"):
        bpy.data.materials[n].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 6.0 if n == "dawn" else 2.0
    # утро: сильнее заполняющий свет, комната светлая; солнце низкое сквозь жалюзи
    for o in bpy.data.objects:
        if o.type == 'LIGHT' and o.data.type == 'AREA' and o.data.size > 5: o.data.energy = 90; o.data.color = (0.92, 0.95, 1.0)
        if o.type == 'LIGHT' and o.data.type == 'SUN':
            o.data.energy = 14.0; o.data.angle = math.radians(0.6)
            o.rotation_euler = Vector((-0.30, -0.80, -0.52)).to_track_quat('-Z', 'Y').to_euler()  # из-за окна, низко, к камере
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.6, 0.8, 1); sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6

def set_lines():
    set_flat()
    for o in bpy.data.objects:   # ламели жалюзи без контуров: иначе слишком много линий рядом с центром кадра
        if o.type == 'MESH' and o.data.materials and o.data.materials[0].name == "slat": o.hide_render = True
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        em = [n for n in m.node_tree.nodes if n.type == 'EMISSION']
        if em:
            for l in list(em[-1].inputs["Color"].links): m.node_tree.links.remove(l)   # kein Flächen-Shading im Linienpass
            em[-1].inputs["Color"].default_value = (1, 1, 1, 1)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'
    vl = sc.view_layers[0]; vl.use_freestyle = True
    ls = vl.freestyle_settings.linesets[0] if len(vl.freestyle_settings.linesets) else vl.freestyle_settings.linesets.new("ls")
    ls.select_silhouette = True; ls.select_crease = True; ls.select_border = True; ls.select_contour = True
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("claire") if not len(bpy.data.linestyles) else bpy.data.linestyles[0]
    ls.linestyle.color = (0, 0, 0); ls.linestyle.alpha = 1.0; ls.linestyle.thickness = 1.5
    vl.freestyle_settings.crease_angle = math.radians(120)

sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.render.resolution_x, sc.render.resolution_y = 1600, 900
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'

def render(path, samples, denoise):
    sc.cycles.samples = samples; sc.cycles.use_denoising = denoise; sc.render.filepath = path
    t = time.time(); bpy.ops.render.render(write_still=True); print(f"RENDER {path.split('/')[-1]} {time.time()-t:.0f}s", flush=True)

if MODE == "flat":
    set_flat(); render(OUT + "pass_flat.png", 4, False)
elif MODE == "lines":
    set_lines(); render(OUT + "pass_lines.png", 4, False)
elif MODE in ("sun", "sunbg", "amb", "ambbg"):
    set_grey()
    if MODE.endswith("bg"): hide_layer(("mid", "fg"))
    only_sun = MODE.startswith("sun")
    bpy.data.objects["win_glow"].hide_render = only_sun   # светящаяся плоскость окна не должна заслонять солнце
    for o in bpy.data.objects:
        if o.type == 'LIGHT': o.hide_render = (o.data.type != 'SUN') if only_sun else (o.data.type == 'SUN')
    for n in ("dawn", "corridor"):
        bpy.data.materials[n].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.0 if only_sun else 3.0
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.0 if only_sun else 0.6
    sc.cycles.max_bounces = 0 if only_sun else 4
    render(OUT + f"pass_{MODE}.png", 16 if only_sun else 40, True)
elif MODE == "flatbg":
    set_flat(); hide_layer(("mid", "fg")); render(OUT + "pass_flat_bg.png", 4, False)
elif MODE == "linesbg":
    set_lines(); hide_layer(("mid", "fg")); render(OUT + "pass_lines_bg.png", 4, False)
elif MODE in ("ao", "aobg"):
    # Kontaktschatten: Ambient Occlusion als Emission, später hart geschnitten
    set_flat()
    if MODE.endswith("bg"): hide_layer(("mid", "fg"))
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        nt = m.node_tree; out = nt.nodes.get("Material Output")
        if out is None: continue
        ao = nt.nodes.new("ShaderNodeAmbientOcclusion"); ao.samples = 8; ao.inputs["Distance"].default_value = 0.7
        em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(ao.outputs["AO"], em.inputs["Color"])
        for l in list(out.inputs["Surface"].links): nt.links.remove(l)
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    render(OUT + f"pass_{MODE}.png", 24, True)
elif MODE == "mask":
    set_flat()
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        em = [n for n in m.node_tree.nodes if n.type == 'EMISSION']
        if em:
            for l in list(em[-1].inputs["Color"].links): m.node_tree.links.remove(l)
            em[-1].inputs["Color"].default_value = (0, 0, 0, 1)
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    white = bpy.data.materials.new("w"); white.use_nodes = True
    wn = white.node_tree; e = wn.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = (1, 1, 1, 1)
    for l in list(wn.nodes["Material Output"].inputs["Surface"].links): wn.links.remove(l)
    wn.links.new(e.outputs["Emission"], wn.nodes["Material Output"].inputs["Surface"])
    for o in bpy.data.objects:
        if o.type == 'MESH' and LAYER.get(o.name) == "mid":
            o.data.materials.clear(); o.data.materials.append(white)
    render(OUT + "mask_mid.png", 4, False)
if MODE in ("flat", "boxes"):
    from bpy_extras.object_utils import world_to_camera_view
    boxes = {}
    for hit, names in HIT.items():
        xs, ys = [], []
        for n in names:
            o = bpy.data.objects[n]
            for v in o.bound_box:
                p = world_to_camera_view(sc, cam, o.matrix_world @ Vector(v)); xs.append(p.x * 1600); ys.append((1 - p.y) * 900)
        boxes[hit] = [max(0, round(min(xs))), max(0, round(min(ys))), min(1600, round(max(xs))), min(900, round(max(ys)))]
    json.dump(boxes, open(os.path.join(WURZEL, "art", "szenen", "aufnahme", "hitboxes.json"), "w"), indent=1); print("HITBOXES", boxes)
