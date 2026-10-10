"""«Nachtdienst», сцена «Aufnahme» (приёмная, 06:40) — 3D-основа под движок игры.
Фронтальная камера, кадр 1600x900. Запуск: python3 scene.py [preview|lit|bg|masks|boxes]"""
import bpy, math, sys, json, time, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

MODE = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "preview"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "bau", "blender", "aufnahme") + os.sep
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, color, rough=0.6, metallic=0.0, emission=None, strength=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if emission:
        b.inputs["Emission Color"].default_value = (*emission, 1); b.inputs["Emission Strength"].default_value = strength
    return m

# светлоты заданы осознанно: стены светлые, мебель тёмная, чтобы силуэты читались после постеризации
G = {
    "wall": mat("wall", (0.62, 0.60, 0.55), 0.85), "wall_low": mat("wall_low", (0.30, 0.36, 0.36), 0.8),
    "ceiling": mat("ceiling", (0.25, 0.25, 0.24), 0.9), "cornice": mat("cornice", (0.7, 0.68, 0.62), 0.8), "floor": mat("floor", (0.50, 0.48, 0.44), 0.35),
    "dark": mat("dark", (0.07, 0.08, 0.09), 0.5), "mid": mat("mid", (0.22, 0.24, 0.25), 0.55),
    "wood": mat("wood", (0.36, 0.26, 0.17), 0.5), "paper": mat("paper", (0.90, 0.86, 0.78), 0.8),
    "cork": mat("cork", (0.42, 0.30, 0.18), 0.9), "metal": mat("metal", (0.45, 0.47, 0.48), 0.35, 0.7),
    "glass": mat("glass", (0.85, 0.9, 1.0), 0.05), "slat": mat("slat", (0.75, 0.72, 0.66), 0.6),
    "screen": mat("screen", (0.05, 0.12, 0.08), 0.3, emission=(0.22, 0.9, 0.55), strength=5.0),
    "lampshade": mat("lampshade", (0.12, 0.13, 0.14), 0.5),
    "accent": mat("accent", (0.76, 0.09, 0.36), 0.5),  # маджента: кружка, папка — один акцент
}
_g = G["glass"].node_tree.nodes["Principled BSDF"]; _g.inputs["Alpha"].default_value = 0.08

LAYER = {}  # obj name -> слой: 'bg' | 'mid' | 'fg'
HIT = {}    # id зоны -> список объектов

def _tag(o, layer, hit=None):
    LAYER[o.name] = layer
    if hit: HIT.setdefault(hit, []).append(o.name)
    return o

def smooth(o, angle=35):
    try: bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle))
    except Exception:
        try: bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))
        except Exception: bpy.ops.object.shade_smooth()

def box(size, loc, m, layer, hit=None, bevel=0.015, rot=(0, 0, 0), name="box"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    if bevel:
        md = o.modifiers.new("bevel", 'BEVEL'); md.width = min(bevel, min(size) * 0.3); md.segments = 3; md.limit_method = 'ANGLE'
    return _tag(o, layer, hit)

def cyl(r, h, loc, m, layer, hit=None, rot=(0, 0, 0), v=40, name="cyl", bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc, rotation=rot, vertices=v)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); smooth(o)
    if bevel:
        md = o.modifiers.new("bevel", 'BEVEL'); md.width = bevel; md.segments = 3; md.limit_method = 'ANGLE'
    return _tag(o, layer, hit)

def sphere(r, loc, m, layer, hit=None, name="sph"):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=3, location=loc)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    return _tag(o, layer, hit)

# ---------------- комната: задняя стена y=0, камера смотрит вдоль +y ----------------
W, H, DEPTH = 10.0, 3.0, 9.0
# задняя стена с проёмом под окно: один меш с отверстием (булево), чтобы Freestyle не рисовал швы
_WX0, _WX1, _WZ0, _WZ1 = -1.25, 1.45, 1.35, 2.75
_wall = box((W + 2, 0.3, H + 0.4), (0, 0.15, H / 2), G["wall"], "bg", bevel=0, name="wall_back")
bpy.ops.mesh.primitive_cube_add(size=1, location=((_WX0 + _WX1) / 2, 0.15, (_WZ0 + _WZ1) / 2))
_hole = bpy.context.object; _hole.scale = (_WX1 - _WX0, 0.6, _WZ1 - _WZ0); bpy.ops.object.transform_apply(scale=True)
_md = _wall.modifiers.new("hole", 'BOOLEAN'); _md.operation = 'DIFFERENCE'; _md.object = _hole
bpy.context.view_layer.objects.active = _wall; bpy.ops.object.modifier_apply(modifier="hole")
bpy.data.objects.remove(_hole, do_unlink=True)
# снаружи: земля и небо для рассеянного света (в прямом солнечном проходе не мешают)
box((40, 30, 0.1), (0, 16, -0.05), mat("ground", (0.35, 0.42, 0.3), 0.9), "bg", bevel=0, name="ground")
box((W + 2, DEPTH + 2, 0.1), (0, -DEPTH / 2 + 0.5, -0.05), G["floor"], "bg", bevel=0, name="floor")
box((W + 2, DEPTH + 2, 0.1), (0, -DEPTH / 2 + 0.5, H + 0.05), G["ceiling"], "bg", bevel=0, name="ceiling")
# Deckenkante: schmale Leiste am Übergang Wand/Decke, damit die Tuschelinie den Stoß zeigt
box((W, 0.06, 0.06), (0, -0.03, H - 0.03), G["cornice"], "bg", bevel=0, name="cornice_back")
box((0.06, DEPTH + 2, 0.06), (-W / 2 + 0.03, -DEPTH / 2 + 0.5, H - 0.03), G["cornice"], "bg", bevel=0, name="cornice_left")
box((0.06, DEPTH + 2, 0.06), (W / 2 - 0.03, -DEPTH / 2 + 0.5, H - 0.03), G["cornice"], "bg", bevel=0, name="cornice_right")
box((0.3, DEPTH + 2, H), (-W / 2 - 0.15, -DEPTH / 2 + 0.5, H / 2), G["wall"], "bg", bevel=0, name="wall_left")
box((0.3, DEPTH + 2, H), (W / 2 + 0.15, -DEPTH / 2 + 0.5, H / 2), G["wall"], "bg", bevel=0, name="wall_right")
# нижняя тёмная панель стены (как в прототипе) и рейка
box((W, 0.03, 1.05), (0, -0.015, 0.525), G["wall_low"], "bg", bevel=0, name="wainscot")
box((W, 0.05, 0.05), (0, -0.025, 1.075), G["wood"], "bg", bevel=0.005, name="wainscot_rail")

# окно с жалюзи по центру задней стены: проём, за ним рассвет
WX0, WX1, WZ0, WZ1 = -1.25, 1.45, 1.35, 2.75
box((WX1 - WX0 + 0.16, 0.08, 0.08), ((WX0 + WX1) / 2, -0.04, WZ1 + 0.04), G["paper"], "bg", bevel=0.01, name="win_frame_top")
box((WX1 - WX0 + 0.16, 0.12, 0.08), ((WX0 + WX1) / 2, -0.06, WZ0 - 0.04), G["paper"], "bg", bevel=0.01, name="win_sill")
for x in (WX0 - 0.04, WX1 + 0.04):
    box((0.08, 0.08, WZ1 - WZ0), (x, -0.04, (WZ0 + WZ1) / 2), G["paper"], "bg", bevel=0.01)
# «дыра» в стене: вырезаем через булево? проще: стена сплошная, а окно — светящаяся плоскость перед ней
win = box((WX1 - WX0, 0.02, WZ1 - WZ0), ((WX0 + WX1) / 2, -0.12, (WZ0 + WZ1) / 2), mat("dawn", (1, 0.8, 0.55), emission=(1.0, 0.72, 0.38), strength=9.0), "bg", bevel=0, name="win_glow")
z = WZ0 + 0.06
while z < WZ1 - 0.03:
    box((WX1 - WX0 - 0.04, 0.02, 0.05), ((WX0 + WX1) / 2, -0.17, z), G["slat"], "bg", bevel=0, rot=(math.radians(-22), 0, 0))
    z += 0.125
box((0.02, 0.02, WZ1 - WZ0), ((WX0 + WX1) / 2, -0.19, (WZ0 + WZ1) / 2), G["slat"], "bg", bevel=0)  # шнур/разделитель

# пробковая доска слева, часы справа, дверь-проём справа
box((1.3, 0.05, 0.9), (-3.1, -0.03, 2.25), G["cork"], "bg", "pinnwand", bevel=0.01, name="pinboard")
box((1.36, 0.03, 0.96), (-3.1, -0.015, 2.25), G["wood"], "bg", "pinnwand", bevel=0.005, name="pinboard_frame")
for (dx, dz, w, h, rz) in ((-0.42, 0.22, 0.34, 0.26, 0.04), (0.0, 0.25, 0.3, 0.22, -0.05), (0.4, 0.2, 0.3, 0.24, 0.02), (-0.3, -0.2, 0.32, 0.24, -0.03), (0.25, -0.22, 0.36, 0.2, 0.05)):
    box((w, 0.01, h), (-3.1 + dx, -0.06, 2.25 + dz), G["paper"], "bg", "pinnwand", bevel=0, rot=(0, rz, 0))
cyl(0.30, 0.05, (2.75, -0.03, 2.35), G["paper"], "bg", "uhr", rot=(math.radians(90), 0, 0), bevel=0.01, name="clock")
cyl(0.32, 0.03, (2.75, -0.01, 2.35), G["dark"], "bg", "uhr", rot=(math.radians(90), 0, 0), name="clock_rim")
# Zeiger werden NICHT gerendert: sie kommen als SVG-Overlay (#uhr-std, #uhr-min) aus gen/kunst.py
# und folgen der Spielzeit. Nur Zifferblatt und Mittelpunkt hier.
cyl(0.012, 0.02, (2.75, -0.07, 2.35), G["dark"], "bg", "uhr", rot=(math.radians(90), 0, 0), v=12, name="clock_pin")
# дверной проём в правой части задней стены: тёмный коридор с тёплым светом в глубине
box((1.0, 0.4, 2.2), (4.0, 0.1, 1.1), G["dark"], "bg", "ausgang", bevel=0, name="door_hole")
box((1.1, 0.06, 0.1), (4.0, -0.05, 2.25), G["wood"], "bg", "ausgang", bevel=0.005, name="door_frame_top")
for x in (3.47, 4.53):
    box((0.08, 0.06, 2.2), (x, -0.05, 1.1), G["wood"], "bg", "ausgang", bevel=0.005)
box((0.4, 0.02, 0.9), (4.0, 0.28, 1.2), mat("corridor", (1, 0.7, 0.4), emission=(1.0, 0.62, 0.28), strength=3.0), "bg", "ausgang", bevel=0, name="corridor_glow")

# ---------------- средний план ----------------
# стойка регистратуры слева (за ней стоит Марлене — 2D-фигура)
DX0, DX1, DY = -4.1, -1.7, -1.3
box((DX1 - DX0, 0.8, 1.05), ((DX0 + DX1) / 2, DY, 0.525), G["wood"], "mid", "marlene", bevel=0.02, name="desk")
box((DX1 - DX0 + 0.1, 0.95, 0.05), ((DX0 + DX1) / 2, DY, 1.075), G["paper"], "mid", "marlene", bevel=0.015, name="desk_top")
box((DX1 - DX0 - 0.3, 0.04, 0.5), ((DX0 + DX1) / 2, DY - 0.42, 0.6), G["mid"], "mid", "marlene", bevel=0.01, name="desk_panel")
# настольная лампа (тёплый свет), кружка-акцент, папки
LX, LY = -2.1, DY + 0.15
cyl(0.1, 0.02, (LX, LY, 1.11), G["dark"], "mid", "marlene"); cyl(0.012, 0.45, (LX, LY, 1.33), G["dark"], "mid", "marlene", v=12)
bpy.ops.mesh.primitive_cone_add(radius1=0.17, radius2=0.04, depth=0.17, location=(LX - 0.06, LY - 0.1, 1.5), rotation=(math.radians(28), 0, math.radians(30)))
cone = bpy.context.object; cone.data.materials.append(G["lampshade"]); cone.visible_shadow = False; _tag(cone, "mid", "marlene")
cyl(0.045, 0.1, (-3.5, DY - 0.15, 1.15), G["mid"], "mid", "marlene", name="mug")  # nur Marlenes Kanne ist Rost
for k in range(3):
    box((0.3, 0.22, 0.015), (-2.9 + k * 0.02, DY + 0.1, 1.11 + k * 0.016), G["paper"], "mid", "marlene", bevel=0, rot=(0, 0, 0.1 * k - 0.1))
box((0.26, 0.2, 0.02), (-3.9, DY + 0.05, 1.11), G["accent"], "mid", "marlene", bevel=0, name="folder")

# ЭКГ-тележка в центре
CX, CY = 0.35, -1.6
box((0.55, 0.45, 0.06), (CX, CY, 0.95), G["mid"], "mid", "wagen", bevel=0.01, name="cart_top")
box((0.55, 0.45, 0.04), (CX, CY, 0.25), G["mid"], "mid", "wagen", bevel=0.01, name="cart_shelf")
for dx in (-0.22, 0.22):
    for dy in (-0.17, 0.17):
        cyl(0.012, 0.9, (CX + dx, CY + dy, 0.5), G["metal"], "mid", "wagen", v=10)
        sphere(0.035, (CX + dx, CY + dy, 0.035), G["dark"], "mid", "wagen")
box((0.5, 0.3, 0.12), (CX, CY, 1.04), G["dark"], "mid", "wagen", bevel=0.01, name="ecg_machine")
box((0.36, 0.02, 0.24), (CX, CY - 0.1, 1.24), G["dark"], "mid", "wagen", bevel=0.008, rot=(math.radians(-12), 0, 0), name="ecg_screen_frame")
box((0.32, 0.005, 0.2), (CX, CY - 0.115, 1.24), G["screen"], "mid", "wagen", bevel=0, rot=(math.radians(-12), 0, 0), name="ecg_screen")
# бумажная лента, свисающая с аппарата (маленький намёк на ЭКГ-бумагу)
box((0.1, 0.004, 0.3), (CX + 0.18, CY - 0.16, 0.86), G["paper"], "mid", "wagen", bevel=0, rot=(math.radians(8), 0, 0), name="strip")
cyl(0.004, 1.2, (CX - 0.1, CY + 0.1, 0.5), G["dark"], "mid", "wagen", v=8, rot=(0, math.radians(12), 0), name="cable")

# ряд стульев справа; на третьем сидит господин Баум (2D-фигура); рядом пакет
def chair(x, y, hit):
    box((0.5, 0.5, 0.06), (x, y, 0.45), G["mid"], "mid", hit, bevel=0.015)
    box((0.5, 0.06, 0.42), (x, y + 0.22, 0.69), G["mid"], "mid", hit, bevel=0.015)
    for dx in (-0.2, 0.2):
        for dy in (-0.2, 0.2):
            cyl(0.016, 0.42, (x + dx, y + dy, 0.21), G["metal"], "mid", hit, v=10)
    box((0.04, 0.5, 0.02), (x - 0.26, y, 0.62), G["wood"], "mid", hit, bevel=0.005)
    box((0.04, 0.5, 0.02), (x + 0.26, y, 0.62), G["wood"], "mid", hit, bevel=0.005)
# Stuhlreihe endet vor der Tür (Türrahmen ab x=3.47): freier Durchgang bleibt
for i, x in enumerate((1.1, 1.75, 2.4, 3.05)):
    chair(x, -0.75, "herrk" if i == 2 else None)
box((0.26, 0.2, 0.34), (2.02, -1.15, 0.17), G["paper"], "mid", "tuete", bevel=0.01, name="bag")
box((0.08, 0.02, 0.12), (2.02, -1.26, 0.38), G["paper"], "mid", "tuete", bevel=0, name="bag_handle")

# ---------------- свет: рассвет 06:40 ----------------
# свет из окна (тёплый, низкий, сквозь жалюзи к камере)
bpy.ops.object.light_add(type='SUN'); sun = bpy.context.object
sun.rotation_euler = (math.radians(68), 0, math.radians(-15)); sun.data.energy = 5.0; sun.data.color = (1.0, 0.74, 0.40); sun.data.angle = math.radians(1.2)
# заполняющий холодный свет, чтобы тени были синими, а не чёрными
bpy.ops.object.light_add(type='AREA', location=(0, -5.5, 2.9)); fill = bpy.context.object
fill.data.energy = 60; fill.data.size = 7; fill.data.color = (0.55, 0.68, 0.95); fill.rotation_euler = (math.radians(15), 0, 0)
# тёплый свет лампы на стойке
bpy.ops.object.light_add(type='SPOT', location=(LX - 0.1, LY - 0.18, 1.42)); sp = bpy.context.object
sp.data.energy = 260; sp.data.color = (1.0, 0.76, 0.42); sp.data.spot_size = math.radians(85); sp.data.spot_blend = 0.6; sp.data.shadow_soft_size = 0.06
sp.rotation_euler = (Vector((LX - 0.6, LY - 0.9, 1.07)) - sp.location).to_track_quat('-Z', 'Y').to_euler()
# свечение экрана ЭКГ-аппарата
bpy.ops.object.light_add(type='AREA', location=(CX, CY - 0.3, 1.25)); ml = bpy.context.object
ml.data.energy = 6; ml.data.color = (0.3, 0.95, 0.55); ml.data.size = 0.3; ml.rotation_euler = (math.radians(-90), 0, 0)
# тёплый свет из коридора
bpy.ops.object.light_add(type='POINT', location=(4.0, 0.2, 1.6)); cp = bpy.context.object
cp.data.energy = 60; cp.data.color = (1.0, 0.62, 0.3); cp.data.shadow_soft_size = 0.3
sc.world = bpy.data.worlds.new("World"); sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.12, 0.16, 0.24, 1); bg.inputs[1].default_value = 0.35

# ---------------- камера: фронтальная, по центру ----------------
bpy.ops.object.camera_add(location=(0, -7.6, 1.25), rotation=(math.radians(90), 0, 0)); cam = bpy.context.object; sc.camera = cam
cam.data.lens = 31; cam.data.sensor_width = 36; cam.data.shift_y = 0.0

# (рендер-проходы задаёт ebenen_aufnahme.py)
