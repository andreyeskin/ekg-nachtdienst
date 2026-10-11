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
SCHIRME = {}  # Schirmname -> (Objektname, Ebene): Bildflächen, auf die das Spiel laufende Kurven legt


def leeren():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    EBENE.clear(); ZONE.clear(); MAT.clear(); PLATZHALTER.clear(); SCHIRME.clear()


def schirmflaeche(name, o, ebene="hintergrund"):
    """Merkt eine Bildschirmfläche (dünne Kiste, Vorderseite = lokale −y-Seite) vor: ebenen.py exportiert ihre
    vier Bildecken nach art/szenen/<raum>/schirme.json, das Spiel zeichnet dort die laufende Kurve (nie das Bild)."""
    SCHIRME[name] = (o.name, ebene)
    return o


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


def platte(breite, tiefe, ort, m, ebene, zone=None, dreh=(0, 0, 0), name="platte"):
    """Eine einzelne Fläche ohne Dicke (ungedreht in der XY-Ebene): Lamellen, Himmelsbänder. Eine hauchdünne
    Kiste gäbe zwei Striche übereinander, eine Fläche genau eine Kontur."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=ort, rotation=dreh)
    o = bpy.context.object; o.name = name; o.scale = (breite, tiefe, 1); bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    return markiere(o, ebene, zone)


FUGE = 0.002   # Abstand zu Laibung und Wand: deckungsgleiche Flächen flimmern, eine 2-mm-Fuge sieht niemand


def fenster(x0, x1, z0, z1, rahmen, griff, ebene="hinten", zone=None, y=0.08, tiefe=0.07, breite=0.07,
            pfosten=0.09, kaempfer=None, fluegel=0.05, bank=(0.22, 0.05), griff_z=None, name="fenster"):
    """Fenster in einer Wandöffnung x0..x1 / z0..z1 (Innenfläche der Wand y=0, Öffnung nach +y, Laibung
    aus der Wand selbst): Blendrahmen in der Laibung (y..y+tiefe), Pfosten in der Mitte, optional ein
    Kämpfer (Höhe z), je Licht ein Flügelrahmen, der etwas in den Raum vorsteht, ein Griff am rechten
    unteren Flügel neben dem Pfosten, Fensterbank vor der Wand. Gibt die Glasflächen als (x0, x1, z0, z1) zurück."""
    f = FUGE; xm = (x0 + x1) / 2; ym = y + tiefe / 2; b = breite
    kiste((b, tiefe, z1 - z0 - 2 * f), (x0 + f + b / 2, ym, (z0 + z1) / 2), rahmen, ebene, zone, fase=0.01, name=name + "_rahmen")
    kiste((b, tiefe, z1 - z0 - 2 * f), (x1 - f - b / 2, ym, (z0 + z1) / 2), rahmen, ebene, zone, fase=0.01, name=name + "_rahmen")
    kiste((x1 - x0 - 2 * b - 2 * f, tiefe, b), (xm, ym, z1 - f - b / 2), rahmen, ebene, zone, fase=0.01, name=name + "_rahmen")
    kiste((x1 - x0 - 2 * b - 2 * f, tiefe, b), (xm, ym, z0 + f + b / 2), rahmen, ebene, zone, fase=0.01, name=name + "_rahmen")
    ix0, ix1, iz0, iz1 = x0 + f + b, x1 - f - b, z0 + f + b, z1 - f - b
    kiste((pfosten, tiefe, iz1 - iz0), (xm, ym, (iz0 + iz1) / 2), rahmen, ebene, zone, fase=0.01, name=name + "_pfosten")
    spalten = [(ix0, xm - pfosten / 2), (xm + pfosten / 2, ix1)]
    zeilen = [(iz0, iz1)]
    if kaempfer is not None:
        kiste((ix1 - ix0, tiefe, 0.08), (xm, ym, kaempfer), rahmen, ebene, zone, fase=0.01, name=name + "_kaempfer")
        zeilen = [(iz0, kaempfer - 0.04), (kaempfer + 0.04, iz1)]
    glas = []
    for (gx0, gx1) in spalten:
        for (gz0, gz1) in zeilen:   # Flügelrahmen: bündig mit dem Licht, 4 cm vor dem Blendrahmen
            fy = y - 0.04 + 0.03; ft = 0.06
            kiste((fluegel, ft, gz1 - gz0), (gx0 + fluegel / 2, fy, (gz0 + gz1) / 2), rahmen, ebene, zone, fase=0.006, name=name + "_fluegel")
            kiste((fluegel, ft, gz1 - gz0), (gx1 - fluegel / 2, fy, (gz0 + gz1) / 2), rahmen, ebene, zone, fase=0.006, name=name + "_fluegel")
            kiste((gx1 - gx0 - 2 * fluegel, ft, fluegel), (gx0 + (gx1 - gx0) / 2, fy, gz1 - fluegel / 2), rahmen, ebene, zone, fase=0.006, name=name + "_fluegel")
            kiste((gx1 - gx0 - 2 * fluegel, ft, fluegel), (gx0 + (gx1 - gx0) / 2, fy, gz0 + fluegel / 2), rahmen, ebene, zone, fase=0.006, name=name + "_fluegel")
            glas.append((gx0 + fluegel, gx1 - fluegel, gz0 + fluegel, gz1 - fluegel))
    # Griff: Rosette auf dem linken Holm des rechten unteren Flügels, Hebel zeigt nach unten (geschlossen)
    gx = spalten[1][0] + fluegel / 2; gz = griff_z if griff_z is not None else (zeilen[0][0] + zeilen[0][1]) / 2
    kiste((0.028, 0.02, 0.07), (gx, y - 0.04 - 0.01, gz), griff, ebene, zone, fase=0.004, name=name + "_griff")
    kiste((0.016, 0.016, 0.11), (gx, y - 0.04 - 0.028, gz - 0.045), griff, ebene, zone, fase=0.003, name=name + "_griff")
    # Fensterbank: vor der Wand, breiter als die Öffnung, Oberkante knapp über der Laibung
    kiste((x1 - x0 + 0.16, bank[0], bank[1]), (xm, -bank[0] / 2 - f, z0 + bank[1] / 2 + f), rahmen, ebene, zone, fase=0.008, name=name + "_bank")
    return glas


def jalousie(x0, x1, z_oben, z_unten, lamelle, band, kasten, ebene="hinten", zone=None, y=0.0, pitch=0.085,
             breite=0.075, neigung=20, schnur=0.75, name="jalousie"):
    """Lamellenjalousie vor dem Fenster, heruntergelassen bis z_unten: Kasten oben, jede Lamelle eine
    eigene Fläche mit Kontur, zwei Leiterbänder davor, Unterschiene, Zugschnur mit Griff rechts.
    neigung > 0: raumseitige Kante oben — von unten sieht man zwischen den Lamellen den Himmel."""
    xm = (x0 + x1) / 2; w = x1 - x0; a = math.radians(neigung)
    kiste((w, 0.08, 0.08), (xm, y, z_oben - 0.04), kasten, ebene, zone, fase=0.006, name=name + "_kasten")
    z = z_oben - 0.08 - pitch * 0.6
    while z > z_unten + 0.03:
        platte(w - 0.02, breite, (xm, y, z), lamelle, ebene, zone, dreh=(-a, 0, 0), name=name + "_lamelle")
        z -= pitch
    kiste((w - 0.02, 0.05, 0.022), (xm, y, z_unten + 0.011), kasten, ebene, zone, fase=0.004, name=name + "_schiene")
    yv = y - breite / 2 * math.cos(a) - 0.004   # knapp vor der Vorderkante der Lamellen
    for t in (0.28, 0.72):
        kiste((0.026, 0.004, z_oben - 0.08 - z_unten), (x0 + t * w, yv, (z_oben - 0.08 + z_unten) / 2), band, ebene, zone, fase=0, name=name + "_band")
    L = (z_oben - z_unten) * schnur
    kiste((0.012, 0.012, L), (x1 - 0.09, yv - 0.012, z_oben - 0.08 - L / 2), band, ebene, zone, fase=0, name=name + "_schnur")
    zylinder(0.014, 0.05, (x1 - 0.09, yv - 0.012, z_oben - 0.08 - L - 0.02), kasten, ebene, zone, v=16, name=name + "_schnurgriff")


def himmel_baender(y, baender, breite=300.0, name="himmel"):
    """Flacher Himmel als Farbbänder: `baender` = [(z_unten, z_oben, material), ...], senkrechte Flächen
    bei y. Niedrig genug halten, dass sie nie im Weg der Sonne stehen (Sonnen-Durchgang, Figuren)."""
    aus = []
    for i, (zu, zo, m) in enumerate(baender):
        aus.append(platte(breite, zo - zu, (0, y, (zu + zo) / 2), m, "hinten", dreh=(math.radians(90), 0, 0), name=f"{name}_{i}"))
    return aus


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
