"""Gemeinsames Werkzeug aller Szenen: Materialien, Grundkörper, Ebenen und Klickzonen.

Eine Szene (szene_<raum>.py) importiert dieses Modul, baut beim Import ihre Geometrie
und legt folgende Namen auf Modulebene ab — mehr braucht ebenen.py nicht:

  PALETTE      Materialname -> Hex-Farbe (Lokalfarbe im Flächen-Durchgang)
  HIMMEL       Hex-Farbe des Welt-Hintergrunds im Flächen-Durchgang
  OHNE_LINIE   Materialnamen, deren Objekte keine Tuschelinie bekommen
  OHNE_SCHATTIERUNG  Materialnamen ohne Helligkeitsstufen nach Flächenrichtung (Lichtquellen, Schirme)
  SONNE_AUS    Objektnamen, die im Sonnen-Durchgang verschwinden (Leuchtflächen vor dem Fenster)
  sonne_stellen(sonne)  richtet die Sonne für den Licht-Durchgang aus (optional)
"""
import math

import bpy

EBENE = {}   # Objektname -> 'hinten' | 'mitte' | 'vorn'
ZONE = {}    # Klickzone -> [Objektnamen]
MAT = {}     # Materialname -> Material
PLATZHALTER = set()   # Objekte nur für Klickzonen, nie gerendert


def leeren():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    EBENE.clear(); ZONE.clear(); MAT.clear(); PLATZHALTER.clear()


def material(name, farbe, rauh=0.6, metall=0.0, leuchten=None, staerke=1.0):
    """Principled-Material; die Lokalfarbe für den Flächen-Durchgang kommt aus PALETTE[name]."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*farbe, 1); b.inputs["Roughness"].default_value = rauh
    b.inputs["Metallic"].default_value = metall
    if leuchten:
        b.inputs["Emission Color"].default_value = (*leuchten, 1); b.inputs["Emission Strength"].default_value = staerke
    MAT[name] = m
    return m


def markiere(o, ebene, zone=None):
    if ebene: EBENE[o.name] = ebene
    if zone: ZONE.setdefault(zone, []).append(o.name)
    return o


def glaetten(o, winkel=35):
    try: bpy.ops.object.shade_smooth_by_angle(angle=math.radians(winkel))
    except Exception:
        try: bpy.ops.object.shade_auto_smooth(angle=math.radians(winkel))
        except Exception: bpy.ops.object.shade_smooth()


def _fase(o, breite):
    md = o.modifiers.new("fase", 'BEVEL'); md.width = breite; md.segments = 3; md.limit_method = 'ANGLE'


def kiste(groesse, ort, m, ebene, zone=None, fase=0.015, dreh=(0, 0, 0), name="kiste"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ort, rotation=dreh)
    o = bpy.context.object; o.name = name; o.scale = groesse
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    if fase: _fase(o, min(fase, min(groesse) * 0.3))
    return markiere(o, ebene, zone)


def zylinder(r, h, ort, m, ebene, zone=None, dreh=(0, 0, 0), v=40, name="zylinder", fase=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=ort, rotation=dreh, vertices=v)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); glaetten(o)
    if fase: _fase(o, fase)
    return markiere(o, ebene, zone)


def kegel(r1, r2, h, ort, m, ebene, zone=None, dreh=(0, 0, 0), v=40, name="kegel"):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=h, location=ort, rotation=dreh, vertices=v)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); glaetten(o)
    return markiere(o, ebene, zone)


def kugel(r, ort, m, ebene, zone=None, name="kugel"):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=3, location=ort)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth()
    return markiere(o, ebene, zone)


def loch(wand, groesse, ort):
    """Schneidet eine Öffnung in ein Objekt (Boolesch, angewandt) — ein Netz ohne Nähte für Freestyle."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=ort)
    stanze = bpy.context.object; stanze.scale = groesse; bpy.ops.object.transform_apply(scale=True)
    if wand.data.materials:   # Schnittflächen (Laibung) bekommen das erste Material, kein leerer Platz
        stanze.data.materials.append(wand.data.materials[0])
    md = wand.modifiers.new("loch", 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.object = stanze
    bpy.context.view_layer.objects.active = wand; bpy.ops.object.modifier_apply(modifier="loch")
    bpy.data.objects.remove(stanze, do_unlink=True)
    return wand


def platzhalter(zone, groesse, ort, name=None):
    """Unsichtbare Fläche nur für die Klickzone (z. B. der Platz, an dem eine Figur steht)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=ort)
    o = bpy.context.object; o.name = name or ("platz_" + zone); o.scale = groesse
    bpy.ops.object.transform_apply(scale=True)
    o.hide_render = True; o.display_type = 'WIRE'
    PLATZHALTER.add(o.name)
    return markiere(o, None, zone)


def raum_huelle(x0, x1, z1, wand, boden, decke, tiefe, staerke=0.3, name="raum"):
    """Ein Raum als EIN Netz: Rückwand (Innenfläche y=0), Seitenwände x0/x1, Boden z=0, Decke z1.
    Zur Kamera (−y) offen und `tiefe` Meter lang — er muss VOR der Kamera enden: Kanten, die hinter
    die Kamera reichen, projiziert Freestyle falsch (lose Striche an Decke und Boden). Weil alle Raumkanten echte Netzkanten sind, zeichnet Freestyle die
    Fugen Wand/Decke, Wand/Wand und Wand/Boden als saubere Linie — getrennte, sich durchdringende
    Kisten liefern dort keine Kante (oder flackernde, wo Flächen genau aufeinanderliegen)."""
    s = staerke
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (s - tiefe) / 2, z1 / 2))
    o = bpy.context.object; o.name = name
    o.scale = (x1 - x0 + 2 * s, tiefe + s, z1 + 2 * s); bpy.ops.object.transform_apply(scale=True)
    loch(o, (x1 - x0, tiefe + 2, z1), ((x0 + x1) / 2, -tiefe / 2 - 1, z1 / 2))
    o.data.materials.clear()   # der Boolesche Schnitt hinterlässt einen leeren Materialplatz
    for m in (wand, boden, decke): o.data.materials.append(m)
    for p in o.data.polygons:   # Material nach Flächenrichtung: nach oben Boden, nach unten Decke
        p.material_index = 1 if p.normal.z > 0.9 else 2 if p.normal.z < -0.9 else 0
    return markiere(o, "hinten")
