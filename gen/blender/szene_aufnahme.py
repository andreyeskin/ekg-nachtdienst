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
    "accent": mat("accent", (0.76, 0.09, 0.36), 0.5),  # Rost: genau ein Objekt — die Betablocker-Schachtel in der Tüte
    # Fenster und Draußen (Sonnenaufgang): Rahmen, Lamellen, Himmelsbänder, Sonne, Silhouetten
    "rahmen": mat("rahmen", (0.85, 0.82, 0.76), 0.6), "lamelle": mat("lamelle", (0.55, 0.68, 0.62), 0.6),
    "band": mat("band", (0.85, 0.82, 0.76), 0.7),
    "himmel_oben": mat("himmel_oben", (0.9, 0.85, 0.7), 0.9), "himmel_mitte": mat("himmel_mitte", (0.9, 0.8, 0.6), 0.9), "himmel_unten": mat("himmel_unten", (0.9, 0.75, 0.5), 0.9),
    "sonne": mat("sonne", (1.0, 0.95, 0.8), 0.9), "baum": mat("baum", (0.45, 0.6, 0.52), 0.9), "stamm": mat("stamm", (0.3, 0.25, 0.2), 0.9),
    "bau": mat("bau", (0.85, 0.82, 0.76), 0.9), "bau_dach": mat("bau_dach", (0.3, 0.35, 0.37), 0.9), "bau_fenster": mat("bau_fenster", (0.3, 0.35, 0.37), 0.9),
    # Geräte: dunkles Glas (die Kurve zeichnet der Code), Polster, Streifen aus dem Drucker
    "glas_dunkel": mat("glas_dunkel", (0.08, 0.1, 0.11), 0.3), "polster": mat("polster", (0.22, 0.24, 0.25), 0.7),
    "schachtel": mat("schachtel", (0.85, 0.82, 0.76), 0.8), "schachtel_mint": mat("schachtel_mint", (0.55, 0.68, 0.62), 0.8),
    "pc_schirm": mat("pc_schirm", (0.9, 0.9, 0.9), 0.3),
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

def torus(R, r, loc, m, layer, hit=None, rot=(0, 0, 0), name="torus"):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=32, minor_segments=10)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    return _tag(o, layer, hit)

# ---------------- комната: задняя стена y=0, камера смотрит вдоль +y ----------------
W, H, DEPTH = 10.0, 3.0, 9.0
# Raum als EIN Netz mit Fensterloch (werkzeug.raum_huelle): Wand/Decke, Wand/Wand, Wand/Boden sind echte Kanten.
# Getrennte Kisten gaben dort keine Linie, eine flackernde (linke Wandoberkante genau in der Deckenfläche) oder
# lose Striche (Kanten, die hinter die Kamera reichen) — die Streulinien oben links und über dem Fenster.
from werkzeug import loch, raum_huelle, fenster, jalousie, himmel_baender, schirmflaeche
_WX0, _WX1, _WZ0, _WZ1 = -1.25, 1.45, 1.35, 2.75
_wall = _tag(loch(raum_huelle(-W / 2, W / 2, H, G["wall"], G["floor"], G["ceiling"], 7.0, name="room"),
                  (_WX1 - _WX0, 0.8, _WZ1 - _WZ0), ((_WX0 + _WX1) / 2, 0.15, (_WZ0 + _WZ1) / 2)), "bg")
# снаружи: земля и небо для рассеянного света (в прямом солнечном проходе не мешают)
box((40, 30, 0.1), (0, 16, -0.05), mat("ground", (0.35, 0.42, 0.3), 0.9), "bg", bevel=0, name="ground")
# Deckenkante: schmale Leiste am Übergang Wand/Decke, damit die Tuschelinie den Stoß zeigt
# (2 mm unter der Decke und nur bis vor die Kamera, sonst flackert bzw. verrutscht ihre Oberkante)
_CZ, _CT = H - 0.032, 7.0
box((W, 0.06, 0.06), (0, -0.03, _CZ), G["cornice"], "bg", bevel=0, name="cornice_back")
box((0.06, _CT, 0.06), (-W / 2 + 0.03, -_CT / 2, _CZ), G["cornice"], "bg", bevel=0, name="cornice_left")
box((0.06, _CT, 0.06), (W / 2 - 0.03, -_CT / 2, _CZ), G["cornice"], "bg", bevel=0, name="cornice_right")
# нижняя тёмная панель стены (как в прототипе) и рейка
box((W, 0.03, 1.05), (0, -0.015, 0.525), G["wall_low"], "bg", bevel=0, name="wainscot")
box((W, 0.05, 0.05), (0, -0.025, 1.075), G["wood"], "bg", bevel=0.005, name="wainscot_rail")

# ---------------- Fenster: Laibung aus der Wand, Rahmen mit zwei Flügeln und Griff, Fensterbank; davor die
# Jalousie, halb hochgezogen, Lamellen schräg offen — dahinter der Sonnenaufgang als flache Bänder ----------------
WX0, WX1, WZ0, WZ1 = _WX0, _WX1, _WZ0, _WZ1
fenster(WX0, WX1, WZ0, WZ1, G["rahmen"], G["dark"], griff_z=1.78)
jalousie(WX0 + 0.03, WX1 - 0.03, WZ1 - 0.01, 2.1, G["lamelle"], G["band"], G["rahmen"], y=0.0, pitch=0.1, breite=0.07, neigung=12, schnur=0.7)
# Draußen: drei Himmelsbänder (Morgenlicht, nach unten wärmer), eine flache Sonnenscheibe knapp über den
# Dächern, links ein Klinikflügel mit Flachdach, rechts zwei Baumkronen. Alles niedrig (nie im Sonnenweg).
AUSSEN = []
AUSSEN += himmel_baender(40.0, [(-20.0, 3.3, G["himmel_unten"]), (3.3, 6.0, G["himmel_mitte"]), (6.0, 14.0, G["himmel_oben"])])
# Lage in Fensterkoordinaten (Kamera 1,3/-7,5/1,35): Dachkante des Flügels bei ~1,72 m, sein rechtes Ende bei x≈-0,35;
# Sonne im rechten Flügel bei (0,55 / 1,85), Baumkronen rechts bis ~1,8 m — alles unter der Jalousie (2,1 m)
AUSSEN.append(cyl(0.69, 0.05, (-3.4, 39.5, 4.5), G["sonne"], "bg", rot=(math.radians(90), 0, 0), v=64, name="aussen_sonne"))
AUSSEN.append(box((10.4, 3.0, 2.9), (-10.8, 24.0, 1.45), G["bau"], "bg", bevel=0, name="aussen_bau"))
AUSSEN.append(box((10.7, 3.3, 0.16), (-10.8, 24.0, 2.98), G["bau_dach"], "bg", bevel=0, name="aussen_dach"))
for i in range(7):
    AUSSEN.append(box((0.8, 0.05, 0.5), (-15.4 + i * 1.4, 22.47, 2.25), G["bau_fenster"], "bg", bevel=0, name=f"aussen_bau_fenster_{i}"))
for i, (bx, by, bz, br) in enumerate(((0.1, 28.0, 2.5, 0.9), (1.4, 28.5, 2.3, 1.1), (-0.9, 29.0, 2.1, 0.7), (2.6, 27.0, 2.7, 1.0))):
    AUSSEN.append(sphere(br, (bx, by, bz), G["baum"], "bg", name=f"aussen_baum_{i}"))
    AUSSEN.append(cyl(0.12, bz, (bx, by, bz / 2), G["stamm"], "bg", v=12, name=f"aussen_stamm_{i}"))

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
# Aufnahmetresen links: hohe Sichtblende zur Wartezone (1,05 m, Holz, Papier-Ablage obenauf), dahinter die
# niedrige Arbeitsfläche (0,75 m) mit Verwaltungs-PC (Rückseite zur Kamera), Tastatur und Gelenklampe;
# Marlenes Bürostuhl steht hinter ihr. Marlene steht bei (-3,05 / -0,5), vgl. ebenen_figuren.py.
DX0, DX1, DY = -4.1, -1.7, -1.3
SB0, SB1 = -1.7, -1.28                                   # Sichtblende y
box((DX1 - DX0, SB1 - SB0, 1.05), ((DX0 + DX1) / 2, (SB0 + SB1) / 2, 0.525), G["wood"], "mid", "marlene", bevel=0.012, name="desk")
box((DX1 - DX0 + 0.08, SB1 - SB0 + 0.1, 0.04), ((DX0 + DX1) / 2, (SB0 + SB1) / 2, 1.07), G["paper"], "mid", "marlene", bevel=0.012, name="desk_top")
box((DX1 - DX0 - 0.3, 0.02, 0.46), ((DX0 + DX1) / 2, SB0 - 0.005, 0.56), G["mid"], "mid", "marlene", bevel=0.006, name="desk_panel")   # Petrol-Blende vorn
box((0.04, 1.4, 1.05), (DX1 - 0.02, SB0 + 0.7, 0.525), G["wood"], "mid", "marlene", bevel=0.006, name="desk_wange")
box((DX1 - DX0 - 0.2, 0.7, 0.04), ((DX0 + DX1) / 2, SB1 + 0.35, 0.73), G["paper"], "mid", "marlene", bevel=0.01, name="work_top")
for x in (DX0 + 0.35, DX1 - 0.35):
    box((0.45, 0.6, 0.69), (x, SB1 + 0.33, 0.345), G["mid"], "mid", "marlene", bevel=0.01, name="work_block")
# Verwaltungs-PC: flacher Schirm, Rückseite zur Kamera (zeigt kein EKG), Fuß, Tastatur davor
PX, PY = -2.95, SB1 + 0.42
cyl(0.11, 0.015, (PX, PY, 0.76), G["dark"], "mid", "marlene", name="pc_fuss")
box((0.03, 0.03, 0.14), (PX, PY, 0.83), G["dark"], "mid", "marlene", bevel=0.004, name="pc_hals")
box((0.52, 0.03, 0.34), (PX, PY + 0.0, 1.07), G["dark"], "mid", "marlene", bevel=0.006, name="pc_schirm_gehaeuse")
box((0.48, 0.004, 0.30), (PX, PY + 0.017, 1.07), G["pc_schirm"], "mid", "marlene", bevel=0, name="pc_schirm")
box((0.42, 0.14, 0.02), (PX, PY - 0.3, 0.76), G["dark"], "mid", "marlene", bevel=0.005, name="tastatur")
# Gelenklampe: Klemme an der Rückkante der Sichtblende, Arm hoch und über die Arbeitsfläche, Schirm nach unten
LX, LY = -2.15, SB1 - 0.02
box((0.05, 0.08, 0.1), (LX, LY, 1.11), G["dark"], "mid", "marlene", bevel=0.005, name="lamp_clamp")
cyl(0.011, 0.42, (LX, LY, 1.35), G["dark"], "mid", "marlene", v=12, name="lamp_arm1")
_a, _b = Vector((LX, LY, 1.56)), Vector((LX - 0.2, LY + 0.42, 1.5))
cyl(0.011, (_b - _a).length, (_a + _b) / 2, G["dark"], "mid", "marlene", v=12, name="lamp_arm2").rotation_euler = (_b - _a).to_track_quat('Z', 'Y').to_euler()
bpy.ops.mesh.primitive_cone_add(radius1=0.14, radius2=0.03, depth=0.14, location=(_b.x, _b.y, _b.z - 0.05), rotation=(math.radians(10), math.radians(-8), 0))
cone = bpy.context.object; cone.name = "lamp_head"; cone.data.materials.append(G["lampshade"]); cone.visible_shadow = False; _tag(cone, "mid", "marlene")
# Ablage obenauf: Klemmbrett ("folder", muss so heißen) und zwei Aufnahmebögen
box((0.26, 0.2, 0.012), (-3.9, DY - 0.16, 1.1), G["paper"], "mid", "marlene", bevel=0, rot=(0, 0, 0.12), name="folder")
box((0.03, 0.09, 0.02), (-3.9, DY - 0.07, 1.115), G["dark"], "mid", "marlene", bevel=0.003, rot=(0, 0, 0.12), name="folder_clip")
for k in range(2):
    box((0.3, 0.21, 0.01), (-2.75 + k * 0.03, DY - 0.2, 1.095 + k * 0.011), G["paper"], "mid", "marlene", bevel=0, rot=(0, 0, 0.08 * k - 0.05))
# Marlenes Bürostuhl hinter ihr (Sitz Petrol-Polster, Fußkreuz)
SX, SY = -3.55, -0.22
for k in range(5):
    a = math.radians(20) + k * 2 * math.pi / 5
    box((0.28, 0.045, 0.03), (SX + 0.14 * math.cos(a), SY + 0.14 * math.sin(a), 0.06), G["dark"], "mid", "marlene", bevel=0.006, rot=(0, 0, a), name="stuhlfuss")
cyl(0.028, 0.34, (SX, SY, 0.25), G["metal"], "mid", "marlene", v=16, name="stuhlsaeule")
box((0.46, 0.44, 0.07), (SX, SY, 0.46), G["polster"], "mid", "marlene", bevel=0.028, rot=(0, 0, math.radians(20)), name="sitz")
box((0.04, 0.04, 0.26), (SX - 0.07, SY + 0.21, 0.6), G["dark"], "mid", "marlene", bevel=0.006, rot=(0, 0, math.radians(20)), name="lehnenstuetze")
box((0.42, 0.06, 0.4), (SX - 0.09, SY + 0.25, 0.86), G["polster"], "mid", "marlene", bevel=0.028, rot=(math.radians(6), 0, math.radians(20)), name="lehne")

# EKG-Wagen (zwischen Tresen und Wartezone, in Reichweite der Stühle): zwei Böden auf vier Pfosten mit Rollen,
# obenauf das Gerät mit geneigtem Schirm (dunkles Glas: die Kurve zeichnet der Code über die Fläche
# "wagen_schirm"), Papierstreifen aus dem Drucker vorn, Patientenkabel aufgerollt am Haken seitlich
CX, CY = 0.55, -1.55
box((0.56, 0.46, 0.05), (CX, CY, 0.92), G["mid"], "mid", "wagen", bevel=0.012, name="cart_top")
box((0.56, 0.46, 0.04), (CX, CY, 0.24), G["mid"], "mid", "wagen", bevel=0.012, name="cart_shelf")
for dx in (-0.23, 0.23):
    for dy in (-0.18, 0.18):
        cyl(0.012, 0.9, (CX + dx, CY + dy, 0.5), G["metal"], "mid", "wagen", v=10)
        sphere(0.035, (CX + dx, CY + dy, 0.035), G["dark"], "mid", "wagen")
box((0.5, 0.36, 0.11), (CX, CY, 1.0), G["dark"], "mid", "wagen", bevel=0.014, name="ecg_machine")
box((0.34, 0.03, 0.25), (CX, CY - 0.12, 1.185), G["dark"], "mid", "wagen", bevel=0.008, rot=(math.radians(-14), 0, 0), name="ecg_screen_frame")
SCHIRM_W = box((0.30, 0.004, 0.19), (CX, CY - 0.137, 1.19), G["glas_dunkel"], "mid", "wagen", bevel=0, rot=(math.radians(-14), 0, 0), name="ecg_screen")
schirmflaeche("wagen_schirm", SCHIRM_W, "mittelgrund")
box((0.22, 0.02, 0.01), (CX + 0.02, CY - 0.19, 0.985), G["mid"], "mid", "wagen", bevel=0, name="printer_slot")
# Streifen: aus dem Schlitz heraus, über die Kante, hängt vorn herunter (zwei Flächen)
box((0.12, 0.08, 0.003), (CX + 0.02, CY - 0.22, 0.99), G["paper"], "mid", "wagen", bevel=0, rot=(math.radians(10), 0, 0), name="strip")
box((0.12, 0.003, 0.3), (CX + 0.02, CY - 0.262, 0.84), G["paper"], "mid", "wagen", bevel=0, rot=(math.radians(4), 0, 0), name="strip_hang")
# Kabel: vom Gerät seitlich zum Haken, dort aufgerollt
box((0.03, 0.06, 0.03), (CX + 0.28, CY - 0.05, 0.88), G["dark"], "mid", "wagen", bevel=0.004, name="hook")
torus(0.085, 0.008, (CX + 0.3, CY - 0.05, 0.78), G["dark"], "mid", "wagen", rot=(0, math.radians(90), 0), name="cable_coil")
torus(0.08, 0.008, (CX + 0.31, CY - 0.04, 0.775), G["dark"], "mid", "wagen", rot=(0, math.radians(90), math.radians(12)), name="cable_coil2")
cyl(0.005, 0.2, (CX + 0.25, CY - 0.1, 0.955), G["dark"], "mid", "wagen", v=8, rot=(math.radians(20), math.radians(70), 0), name="cable")

# Wartereihe: vier Sitze auf einem Traversenbalken (Klinik-Bank), Polster Petrol, Armlehnen Holz, zwei Füße.
# Herr Baum sitzt auf dem dritten Sitz (x = 2,4, y = -0,75), Sitzfläche 0,45..0,48 m; die Reihe endet vor der Tür.
BY, SITZE = -0.75, (1.1, 1.75, 2.4, 3.05)
box((SITZE[-1] - SITZE[0] + 0.56, 0.06, 0.05), ((SITZE[0] + SITZE[-1]) / 2, BY, 0.39), G["dark"], "mid", None, bevel=0.006, name="bank_balken")
for x in (SITZE[0] - 0.12, SITZE[-1] + 0.12):
    box((0.05, 0.05, 0.37), (x, BY, 0.185), G["dark"], "mid", None, bevel=0.005, name="bank_fuss")
    box((0.06, 0.5, 0.025), (x, BY, 0.0125), G["dark"], "mid", None, bevel=0.005, name="bank_kufe")
for i, x in enumerate(SITZE):
    hit = "herrk" if i == 2 else None   # nur sein Sitz ist eine Klickzone
    box((0.5, 0.48, 0.06), (x, BY, 0.45), G["polster"], "mid", hit, bevel=0.025, name="sitz_bank")
    box((0.5, 0.06, 0.42), (x, BY + 0.235, 0.7), G["polster"], "mid", hit, bevel=0.025, rot=(math.radians(-7), 0, 0), name="lehne_bank")
    box((0.04, 0.04, 0.26), (x, BY + 0.2, 0.52), G["dark"], "mid", hit, bevel=0.004, name="lehne_bank_stuetze")
for i in range(len(SITZE) + 1):
    x = SITZE[0] - 0.325 + i * 0.65
    box((0.04, 0.04, 0.22), (x, BY - 0.02, 0.52), G["dark"], "mid", None, bevel=0.004, name="armlehne_stuetze")
    box((0.05, 0.36, 0.028), (x, BY + 0.02, 0.645), G["wood"], "mid", None, bevel=0.01, name="armlehne")
# Plastiktüte (Herrn Baums Tabletten): weicher, oben zusammengesackter Körper, zwei Henkel, drei Schachteln
# schauen heraus — die Betablocker-Schachtel in Rost, das eine Rost-Objekt des Bildes. Steht vor der Bank links
# neben seinem Sitz ("bag" muss so heißen).
TX, TY = 1.82, -1.22
# Weicher Körper statt Kasten (zwei Ellipsoide: Bauch, zusammengesackte Öffnung) und flache, hohe Folienschlaufen
# statt Ringen — die Vorlage für figuren_zeichnen.py soll schon nach Tüte aussehen, nicht nach Kanister.
_tb = sphere(1.0, (TX, TY, 0.15), G["paper"], "mid", "tuete", name="bag"); _tb.scale = (0.17, 0.11, 0.165); _tb.rotation_euler = (0, 0, math.radians(14))
_to = sphere(1.0, (TX + 0.01, TY, 0.31), G["paper"], "mid", "tuete", name="bag_top"); _to.scale = (0.12, 0.085, 0.075); _to.rotation_euler = (0, math.radians(-6), math.radians(14))
for dx in (-0.05, 0.05):
    _th = torus(0.042, 0.0035, (TX + dx, TY, 0.44), G["paper"], "mid", "tuete", rot=(math.radians(90), 0, math.radians(14)), name="bag_handle"); _th.scale = (1.0, 1.0, 1.7)
box((0.09, 0.03, 0.13), (TX - 0.05, TY - 0.02, 0.39), G["accent"], "mid", "tuete", bevel=0.004, rot=(0, math.radians(-18), math.radians(20)), name="schachtel_rost")
box((0.1, 0.035, 0.12), (TX + 0.05, TY + 0.03, 0.38), G["schachtel_mint"], "mid", "tuete", bevel=0.004, rot=(math.radians(8), math.radians(14), math.radians(10)), name="schachtel_mint")
box((0.08, 0.03, 0.11), (TX + 0.0, TY - 0.05, 0.37), G["schachtel"], "mid", "tuete", bevel=0.004, rot=(math.radians(-10), 0, math.radians(30)), name="schachtel")
# Die Tüte kommt als gezeichnete Figur aus figuren_zeichnen.py (art/szenen/aufnahme/figuren/tuete.png): im Raumrender
# unsichtbar wie ein Platzhalter, Klickzone bleibt; die Grundkörper dienen dort als Vorlage und Holdout.
import werkzeug as _wz
_wz.PLATZHALTER.update(HIT["tuete"])

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

# ---------------- Einstellungen für ebenen.py (vorher in ebenen_aufnahme.py) ----------------
# leichte Dreiviertelansicht von rechts: Tiefe, und trotzdem bleibt alles lesbar
cam.location = (1.3, -7.5, 1.35); cam.data.lens = 30
cam.rotation_euler = (Vector((-0.45, 0.0, 1.2)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
# Lokalfarben (docs/ART_BIBLE.md §2): Aufnahme = der warme Raum — Sand, Holz, Mint-Sockel, warmes Linoleum,
# Petrol nur für Polster und Geräte; Rost einmal (Schachtel in der Tüte); Morgenlicht draußen in drei Stufen
PALETTE = {
    "wall": "#EFE6D3", "cornice": "#F7F1E4", "wall_low": "#BFD9CF", "ceiling": "#E4DCC8", "floor": "#C9BDA2",
    "wood": "#C99A5B", "paper": "#F7F1E4", "cork": "#B98B5A", "dark": "#2C3E46", "mid": "#2C5560",
    "metal": "#8A9598", "glass": "#EAF1F2", "slat": "#F4EBD8", "screen": "#FFF8F4", "lampshade": "#2C3E46",
    "accent": "#B5552D", "corridor": "#F3D9A8", "ground": "#CFD9C2",
    "rahmen": "#F7F1E4", "lamelle": "#BFD9CF", "band": "#F7F1E4",
    "himmel_oben": "#F8E7BF", "himmel_mitte": "#F6DCA4", "himmel_unten": "#F3CD8C", "sonne": "#FFF6DC",
    "baum": "#2C5560", "stamm": "#2C5560", "bau": "#F7F1E4", "bau_dach": "#2C5560", "bau_fenster": "#2C5560",
    "glas_dunkel": "#1E2A30", "polster": "#2C5560", "schachtel": "#F7F1E4", "schachtel_mint": "#BFD9CF", "pc_schirm": "#F7F1E4",
}
HIMMEL = "#F8E7BF"
OHNE_LINIE = {"himmel_oben", "himmel_mitte", "himmel_unten"}      # Himmelsbänder stoßen ohne Strich aneinander
OHNE_SCHATTIERUNG = {"corridor", "screen", "glass", "himmel_oben", "himmel_mitte", "himmel_unten", "sonne",
                     "baum", "stamm", "bau", "bau_dach", "bau_fenster", "glas_dunkel", "pc_schirm"}  # Lichtquellen, Draußen, Schirme bleiben flach
SONNE_AUS = {o.name for o in AUSSEN}                             # Draußen schattet die Sonne nie ab


def sonne_stellen(s):
    """Sonnenaufgang: tief, von draußen durch die Jalousie zur Kamera hin. Azimut wie in ebenen_figuren.py
    (dort fest verdrahtet), etwas steiler, damit die Streifen der Lamellen auf dem sichtbaren Boden liegen."""
    s.data.energy = 14.0; s.data.angle = math.radians(0.6)
    s.rotation_euler = Vector((-0.30, -0.80, -0.66)).to_track_quat('-Z', 'Y').to_euler()
