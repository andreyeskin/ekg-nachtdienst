"""Die Figuren von Kapitel 1 als einfache 3D-Grundkörper (ligne claire, siehe docs/ART_BIBLE.md §5).

Schwester Marlene (rund, kompakt, Thermoskanne), Herr Konrad Baum (weiches Rechteck, gebeugt,
Schiebermütze) und Oberarzt Dr. Falk (hoch, dreieckig, Hände in den Taschen). Jede Figur ist eine
Funktion, die Position, Drehung und Haltung entgegennimmt und ein `Figur`-Objekt zurückgibt.

Alle Teile hängen an einem Leer-Objekt (Wurzel); Kopfteile an einem zweiten Leer-Objekt, damit
der Kopf als Ganzes geneigt werden kann. Flächen und Linie kommen aus denselben Render-Durchgängen
wie die Räume (ebenen_figuren.py); hier wird nur Geometrie gebaut.

Zwei Sammlungen: "figuren" (Körper, Kleidung — Freestyle zeichnet die Kontur) und "figuren_fein"
(Augen, Brauen, Mund, Brillen, Ketten — nur Fläche in Tintenfarbe, keine zusätzliche Kontur, sonst
würden die kleinen Formen doppelt so dick).
"""
import math
import bpy
import bmesh
from mathutils import Vector, Euler

# Farben der Figuren (Materialname -> sRGB). Die Raum-Palette liegt in ebenen_aufnahme.py; hier nur,
# was den Figuren gehört. Rost ist der eine Akzent pro Bild: Marlenes Thermoskanne.
FARBEN = {
    "fig_haut": "#EBC4A0", "fig_tinte": "#1E2A30", "fig_rost": "#B5552D",
    "fig_kasack": "#426E73", "fig_haar_marlene": "#7A4A2C", "fig_socke": "#BFD9CF",
    "fig_clog": "#C99A5B", "fig_schild": "#F7F1E4", "fig_dunkel": "#2C3E46",
    "fig_kittel": "#F7F1E4", "fig_haar_grau": "#B9BDB8", "fig_messing": "#C99A5B",
    "fig_fleck": "#E4D2B2", "fig_metall": "#8A9598", "fig_hose": "#8A9598",
    "fig_strick": "#5A4228", "fig_hemd": "#BFD9CF", "fig_muetze": "#525A66",
    "fig_armband": "#B5302A", "fig_tuete": "#F7F1E4", "fig_hemd_falk": "#8CA4B6", "fig_krawatte": "#2B3A50",
    # Lehrsaal (docs/raeume/lehrsaal.md §2): Dr. Wieser — Kobaltblau nur bei ihr (Lineal, Sneaker), dunkler Rollkragen,
    # graues Haar mit dunkler Strähne; Jonas — Senfgelb nur bei ihm (Socken), T-Shirt, Jeans, Kopfhörer; die rote
    # Extremitätenklemme an seinem rechten Arm ist das eine Rost-Objekt des Raums, die anderen Klemmen gelb/grün/schwarz
    "fig_kobalt": "#2F5DA8", "fig_rollkragen": "#2C3E46", "fig_hose_wieser": "#3E4A55", "fig_haar_wieser": "#A9AEAA",
    "fig_straehne": "#3A3F44", "fig_senf": "#D9A441", "fig_shirt_jonas": "#5B6770", "fig_jeans": "#6F7580",
    "fig_haar_jonas": "#4E3B2A", "fig_klemme_rot": "#B5552D", "fig_klemme_gelb": "#E8D44D", "fig_klemme_gruen": "#1F6B5A",
    "fig_klemme_schwarz": "#1E2A30", "fig_sohle": "#F7F1E4",
}
# Kasack, Strickjacke, Mütze und Haar tragen die Farben, die die Porträts (art/portraits) zeigen, damit die
# Ganzkörperfiguren dieselben Leute bleiben; Rost (Kanne) bleibt der eine Akzent im Raum Aufnahme.

# Wo jede Figur im Raum steht — die EINE Stelle für Ort (Meter, Weltkoordinaten der Szene), Drehung (Grad) und
# Haltung. ebenen_figuren.aufbau() und figuren_zeichnen.py lesen hier. Falk: ort=None heißt „am Platzhalter
# platz_falk der Szene“ (szene_monitor.py); ein Tupel überschreibt ihn.
PLATZ = {
    "marlene": dict(ort=(-3.05, -0.5, 0.0), drehung=20, haltung="tresen", tresen=1.09),  # hinter dem Tresen (Oberkante der Ablage 1,09 m)
    "herrk": dict(ort=(2.4, -0.75, 0.0), drehung=-8, haltung="sitzen"),                  # dritter Stuhl der Wartereihe
    "falk": dict(ort=None, drehung=-14, haltung="taschen"),                              # rechts vom großen Schirm
    # Lehrsaal (szene_lehrsaal.py: Rückwand y=0, Raum nach −y; die Raumbeschreibung misst y in den Raum hinein).
    # Dr. Wieser links neben dem Kopfende der Liege, linker Fuß auf dem Tritt, Körper zu Jonas gedreht, Kopf zur Kamera;
    # Jonas auf der Liegefläche (0,75 m), Körperachse entlang der um 20° gedrehten Liege, Kopf zur Rückwand.
    "wieser": dict(ort=(-0.45, -2.05, 0.0), drehung=35, haltung="tritt"),
    "jonas": dict(ort=(0.6, -2.4, 0.75), drehung=20, haltung="liegen"),
}
TINTE = "fig_tinte"


def _lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c)


def material(name):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*_lin(FARBEN[name]), 1)
        b.inputs["Roughness"].default_value = 0.8
    return m


def _sammlung(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


class Figur:
    """Ein Figurenbau: Wurzel-Leerobjekt, Teile, Kopf. `tag(obj, "fig", hit)` wird für jedes Teil
    gerufen, wenn die Szene eine Ebenen-Markierung verlangt (siehe szene_aufnahme._tag)."""

    def __init__(self, name, ort=(0, 0, 0), drehung=0.0, tag=None, hit=None, fein=1.0):
        self.name, self.tag, self.hit = name, tag, hit
        self.fein = fein                       # Strichstärke der Gesichtslinien (m), je nach Bildmaßstab
        self.teile, self.kopf = [], None
        self.koerper = _sammlung("figuren"); self.feinteile = _sammlung("figuren_fein")
        self.wurzel = bpy.data.objects.new(name, None)
        self.koerper.objects.link(self.wurzel)
        self.wurzel.location = ort; self.wurzel.rotation_euler = (0, 0, math.radians(drehung))

    # ---------------------------------------------------------------- Grundkörper
    def _aufnehmen(self, o, mat, eltern=None, fein=False, name=None):
        o.name = f"{self.name}_{name or mat}"
        for c in list(o.users_collection): c.objects.unlink(o)
        (self.feinteile if fein else self.koerper).objects.link(o)
        if o.type == 'MESH':
            o.data.materials.clear(); o.data.materials.append(material(mat))
        o.parent = eltern or self.wurzel
        self.teile.append(o)
        if self.tag: self.tag(o, "fig", self.hit)
        return o

    def _glatt(self, o, winkel=40):
        bpy.context.view_layer.objects.active = o; o.select_set(True)
        try: bpy.ops.object.shade_smooth_by_angle(angle=math.radians(winkel))
        except Exception: bpy.ops.object.shade_smooth()
        o.select_set(False)

    def kugel(self, r, ort, mat, skala=(1, 1, 1), rot=(0, 0, 0), eltern=None, fein=False, name=None, seg=48):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=seg, ring_count=seg // 2, location=ort, rotation=rot)
        o = bpy.context.object; o.scale = skala; self._glatt(o)
        return self._aufnehmen(o, mat, eltern, fein, name)

    def kappe(self, r, ort, mat, skala=(1, 1, 1), rot=(0, 0, 0), ebene=((0, 0, 0), (0, 0, 1)), eltern=None, name=None):
        """Offene Kugelschale (Haar, Mützenkrone): alles hinter der Ebene (lokal, Normale zeigt zum
        erhaltenen Teil) wird entfernt. Der offene Rand wird von Freestyle als Linie gezeichnet."""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=48, ring_count=24, location=ort, rotation=rot)
        o = bpy.context.object; o.scale = skala
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                               plane_co=Vector(ebene[0]), plane_no=Vector(ebene[1]).normalized(), clear_inner=True)
        bm.to_mesh(o.data); bm.free(); self._glatt(o)
        return self._aufnehmen(o, mat, eltern, False, name)

    def quader(self, groesse, ort, mat, rot=(0, 0, 0), fase=0.01, eltern=None, fein=False, name=None):
        bpy.ops.mesh.primitive_cube_add(size=1, location=ort, rotation=rot)
        o = bpy.context.object; o.scale = groesse; bpy.ops.object.transform_apply(scale=True)
        if fase:
            md = o.modifiers.new("fase", 'BEVEL'); md.width = min(fase, min(groesse) * 0.3); md.segments = 3; md.limit_method = 'ANGLE'
        return self._aufnehmen(o, mat, eltern, fein, name)

    def zylinder(self, r, h, ort, mat, rot=(0, 0, 0), v=32, eltern=None, fein=False, name=None):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=ort, rotation=rot, vertices=v)
        o = bpy.context.object; self._glatt(o)
        return self._aufnehmen(o, mat, eltern, fein, name)

    def kegel(self, r_unten, r_oben, h, ort, mat, skala=(1, 1, 1), rot=(0, 0, 0), eltern=None, name=None):
        bpy.ops.mesh.primitive_cone_add(radius1=r_unten, radius2=r_oben, depth=h, location=ort, rotation=rot, vertices=48)
        o = bpy.context.object; o.scale = skala; self._glatt(o)
        return self._aufnehmen(o, mat, eltern, False, name)

    def glied(self, p0, p1, r, mat, kappen=True, eltern=None, name=None):
        """Gliedmaße: Zylinder von p0 nach p1 mit Kugeln an beiden Enden (Gelenke)."""
        p0, p1 = Vector(p0), Vector(p1); d = p1 - p0
        rot = d.to_track_quat('Z', 'Y').to_euler()
        o = self.zylinder(r, d.length, (p0 + p1) / 2, mat, rot=rot, eltern=eltern, name=name)
        if kappen:
            self.kugel(r, p0, mat, eltern=eltern, name=name, seg=24); self.kugel(r, p1, mat, eltern=eltern, name=name, seg=24)
        return o

    def rohr(self, punkte, r, mat, eltern=None, fein=True, name=None, glatt=True, kappen=True):
        """Runder Strich entlang einer Kurve (Brauen, Mund, Kette, Schlauch) — als Mesh."""
        cu = bpy.data.curves.new("rohr", 'CURVE'); cu.dimensions = '3D'
        cu.bevel_depth = r; cu.bevel_resolution = 3; cu.fill_mode = 'FULL'; cu.use_fill_caps = kappen; cu.resolution_u = 10
        sp = cu.splines.new('BEZIER' if glatt else 'POLY')
        if glatt:
            sp.bezier_points.add(len(punkte) - 1)
            for bp, p in zip(sp.bezier_points, punkte):
                bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = 'AUTO'
        else:
            sp.points.add(len(punkte) - 1)
            for sp_p, p in zip(sp.points, punkte): sp_p.co = (*p, 1)
        tmp = bpy.data.objects.new("rohr_tmp", cu); bpy.context.scene.collection.objects.link(tmp)
        bpy.context.view_layer.update()
        me = bpy.data.meshes.new_from_object(tmp.evaluated_get(bpy.context.evaluated_depsgraph_get()))
        bpy.data.objects.remove(tmp, do_unlink=True); bpy.data.curves.remove(cu)
        o = bpy.data.objects.new("rohr", me); bpy.context.scene.collection.objects.link(o)
        for p in me.polygons: p.use_smooth = True
        return self._aufnehmen(o, mat, eltern, fein, name)

    def ring(self, R, r, ort, mat, rot=(0, 0, 0), eltern=None, fein=True, name=None):
        bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=ort, rotation=rot, major_segments=32, minor_segments=8)
        o = bpy.context.object; self._glatt(o)
        return self._aufnehmen(o, mat, eltern, fein, name)

    def leer(self, ort, rot=(0, 0, 0), eltern=None, name="kopf"):
        e = bpy.data.objects.new(f"{self.name}_{name}", None); self.koerper.objects.link(e)
        e.location = ort; e.rotation_euler = rot; e.parent = eltern or self.wurzel
        self.teile.append(e)
        return e

    # ---------------------------------------------------------------- Gesicht
    @staticmethod
    def vorne(skala, x, z, tief=0.0):
        """y der Vorderfläche eines achsparallelen Ellipsoids (Mittelpunkt 0) an der Stelle x, z; `tief` schiebt nach vorn."""
        a, b, c = skala
        q = 1 - (x / a) ** 2 - (z / c) ** 2
        return -b * math.sqrt(max(q, 0.0)) - tief

    def gesicht(self, kopf, skala, augen=(0.04, 0.01), augenform=(0.016, 0.006, 0.009), brauen=None, mund=None,
                nase=(0.013, 0.013, 0.02), nase_z=-0.02, lider=False, falten=False, brauen_mat=TINTE, brauen_r=None):
        """Augen als dunkle Flächen, Brauen und Mund als Striche, Nase als Form — wenige klare Teile.
        brauen: (dx, dz_innen, dz_aussen, neigung) · mund: (breite, z, hoehe der Mitte: + lächeln, - traurig)."""
        ax, az = augen; f = self.fein; br = brauen_r or f * 1.3
        for s in (-1, 1):
            y = self.vorne(skala, s * ax, az, augenform[1] * 0.55)
            self.kugel(1, (s * ax, y, az), TINTE, skala=augenform, eltern=kopf, fein=True, name="auge", seg=24)
            if lider:        # schwere Lider: Strich dicht über dem Auge, leicht nach außen fallend
                w = augenform[0]
                pts = [(s * (ax - w), self.vorne(skala, s * (ax - w), az + 0.008, f), az + 0.009),
                       (s * ax, self.vorne(skala, s * ax, az + 0.011, f), az + 0.012),
                       (s * (ax + w * 1.05), self.vorne(skala, s * (ax + w * 1.05), az + 0.006, f), az + 0.006)]
                self.rohr(pts, f * 0.9, TINTE, eltern=kopf, name="lid")
            if falten:       # Lachfalten: zwei kurze Bögen am äußeren Augenwinkel
                xo = s * (ax + augenform[0] + 0.012)
                for dz in (-0.004, -0.016):
                    pts = [(xo - s * 0.004, self.vorne(skala, xo - s * 0.004, az + dz, f * 0.6), az + dz + 0.004),
                           (xo + s * 0.006, self.vorne(skala, xo + s * 0.006, az + dz, f * 0.6), az + dz - 0.005)]
                    self.rohr(pts, f * 0.55, TINTE, eltern=kopf, name="falte")
        if brauen:
            dx, zi, za, neig = brauen
            for s in (-1, 1):
                xi, xa = s * (ax - dx), s * (ax + dx)
                pts = [(xi, self.vorne(skala, xi, zi, f), zi), (s * ax, self.vorne(skala, s * ax, (zi + za) / 2 + neig, f), (zi + za) / 2 + neig),
                       (xa, self.vorne(skala, xa, za, f), za)]
                self.rohr(pts, br, brauen_mat, eltern=kopf, name="braue")
        if nase:
            y = self.vorne(skala, 0, nase_z, nase[1] * 0.35)
            self.kugel(1, (0, y, nase_z), "fig_haut", skala=nase, eltern=kopf, name="nase", seg=24)
        if mund:
            b, z, h = mund
            pts = [(-b / 2, self.vorne(skala, -b / 2, z, f), z), (0, self.vorne(skala, 0, z - h, f), z - h), (b / 2, self.vorne(skala, b / 2, z, f), z)]
            self.rohr(pts, f, TINTE, eltern=kopf, name="mund")

    def ohren(self, kopf, skala, z=0.0, groesse=(0.012, 0.022, 0.03), y=0.0):
        for s in (-1, 1):
            self.kugel(1, (s * skala[0], y, z), "fig_haut", skala=groesse, eltern=kopf, name="ohr", seg=24)

    def brille(self, eltern, ort, R=0.022, abstand=0.036, rot=(math.radians(90), 0, 0), kette=None, buegel=None):
        """Zwei Ringe und ein Steg; optional Bügel (Punkte je Seite, s wird mit x multipliziert) und Kette."""
        x, y, z = ort
        for s in (-1, 1):
            self.ring(R, self.fein * 0.9, (x + s * abstand, y, z), TINTE, rot=rot, eltern=eltern, name="brille")
        self.rohr([(x - abstand + R, y, z + 0.002), (x, y - 0.004, z + 0.006), (x + abstand - R, y, z + 0.002)], self.fein * 0.9, TINTE, eltern=eltern, name="steg")
        if buegel:
            for s in (-1, 1):
                self.rohr([(x + s * bx, by, bz) for bx, by, bz in buegel], self.fein * 0.8, TINTE, eltern=eltern, name="buegel")
        if kette:
            for s in (-1, 1):
                self.rohr([(x + s * kx, ky, kz) for kx, ky, kz in kette], self.fein * 0.6, "fig_metall", eltern=eltern, name="kette")

    def hand(self, ort, mat="fig_haut", r=0.042, skala=(1.0, 1.1, 0.7), rot=(0, 0, 0), eltern=None):
        return self.kugel(r, ort, mat, skala=skala, rot=rot, eltern=eltern, name="hand", seg=24)


# ====================================================================== Marlene
def marlene(ort=(0, 0, 0), drehung=0.0, haltung="tresen", tag=None, hit="marlene", fein=0.0045, tresen=1.1):
    """Schwester Marlene, 54: runde Formfamilie, kompakt (1,62 m), Dutt mit Lesebrille, Kuli hinterm Ohr,
    Thermoskanne (Rost) in der linken Hand. Haltungen: "tresen" (rechte Hand liegt auf dem Tresen, der
    ~0,35 m vor ihr steht und `tresen` m hoch ist; die Kanne steht auf dem Tresen, die linke Hand bleibt
    daran), "stehen" (Kanne hängt in der Hand, andere Hand in der Hüfte)."""
    F = Figur("marlene", ort, drehung, tag, hit, fein)
    # Füße: grüne Socken in Clogs
    for s in (-1, 1):
        F.quader((0.1, 0.27, 0.07), (s * 0.1, -0.02, 0.035), "fig_clog", fase=0.02, name="clog")
        F.zylinder(0.052, 0.1, (s * 0.1, 0.02, 0.11), "fig_socke", name="socke")
        F.glied((s * 0.1, 0.02, 0.14), (s * 0.1, 0.0, 0.8), 0.07, "fig_kasack", name="bein")
    # Körper: eine Eiform, darauf eine kleinere für Brust und Schultern — rund, nicht breit
    F.kugel(1, (0, 0.0, 0.84), "fig_kasack", skala=(0.24, 0.18, 0.2), name="huefte")
    F.kugel(1, (0, 0.0, 1.05), "fig_kasack", skala=(0.235, 0.165, 0.31), name="rumpf")
    F.zylinder(0.052, 0.12, (0, -0.01, 1.35), "fig_haut", name="hals")
    # Namensschild (nur die Fläche, kein Text); folgt der Rumpfkrümmung
    F.quader((0.07, 0.006, 0.028), (-0.12, Figur.vorne((0.235, 0.165, 0.31), -0.12, 0.1, 0.005), 1.15), "fig_schild", fase=0, rot=(math.radians(-8), 0, math.radians(-40)), name="schild")
    # Kopf, rund, mit Hals leicht nach vorn
    kopf = F.leer((0, -0.005, 1.49), rot=(math.radians(4), 0, 0))
    KS = (0.115, 0.108, 0.12)
    F.kugel(1, (0, 0, 0), "fig_haut", skala=KS, eltern=kopf, name="kopf")
    F.ohren(kopf, KS, z=0.0)
    # Haar (kastanie, eine Farbe): offene Schale, Haaransatz sichtbar, seitlich und vorn zurückgekämmt
    F.kappe(1, (0, 0.012, 0.012), "fig_haar_marlene", skala=(0.121, 0.115, 0.122), ebene=((0, 0, 0.22), (0, 0.38, 0.92)), eltern=kopf, name="haar")
    for s in (-1, 1):   # Haarvolumen über den Ohren, nach hinten gestrichen
        F.kugel(1, (s * 0.1, 0.03, 0.03), "fig_haar_marlene", skala=(0.03, 0.07, 0.055), eltern=kopf, name="haarseite", seg=24)
    # Großer schiefer Knoten oben-hinten (zur Kamera hin): Kern, darum ein gewickelter Ring und drei Strähnen,
    # die als Tuschelinien erscheinen — ein Dutt, keine Haube
    DZ = (0.045, 0.055, 0.125); DR = (math.radians(-38), math.radians(22), 0)
    F.kugel(1, DZ, "fig_haar_marlene", skala=(0.052, 0.05, 0.046), eltern=kopf, name="dutt", seg=32)
    F.ring(0.05, 0.026, DZ, "fig_haar_marlene", rot=DR, eltern=kopf, fein=False, name="duttring")
    dm = Euler(DR).to_matrix()
    for k, (a0, a1) in enumerate(((0.2, 2.6), (2.9, 5.2), (1.4, 3.9))):
        pts = []
        for t in (a0, (a0 + a1) / 2, a1):
            lok = Vector((0.062 * math.cos(t), 0.062 * math.sin(t), 0.012 * (k - 1)))
            pts.append(tuple(Vector(DZ) + dm @ lok))
        F.rohr(pts, fein * 1.1, "fig_haar_marlene", eltern=kopf, fein=False, name="duttstraehne")
    # zwei lose Strähnen: eine aus dem Knoten, eine vor dem Ohr
    F.rohr([(0.085, 0.07, 0.1), (0.1, 0.085, 0.05), (0.095, 0.08, -0.01)], fein * 0.9, "fig_haar_marlene", eltern=kopf, name="straehne")
    F.rohr([(-0.1, -0.03, 0.06), (-0.112, -0.045, 0.0), (-0.105, -0.04, -0.05)], fein * 0.8, "fig_haar_marlene", eltern=kopf, name="straehne")
    # Lesebrille steckt schräg IM Knoten: Gläser vor dem Knoten, Bügel greifen ins Haar
    F.brille(kopf, (0.03, -0.005, 0.138), R=0.019, abstand=0.028, rot=(math.radians(52), 0, math.radians(12)),
             buegel=[(0.046, -0.002, 0.14), (0.06, 0.04, 0.13)])
    # Kuli hinterm linken Ohr (zur Kamera hin)
    F.zylinder(0.004, 0.14, (0.118, 0.0, 0.035), "fig_kasack", rot=(math.radians(-20), math.radians(8), 0), v=10, eltern=kopf, fein=True, name="kuli")
    # Gesicht: schwere Lider, Lachfalten, warmes halbes Lächeln, runde Nase
    F.gesicht(kopf, KS, augen=(0.042, 0.012), augenform=(0.019, 0.006, 0.011), brauen=(0.02, 0.036, 0.032, 0.008),
              mund=(0.06, -0.055, 0.012), nase=(0.014, 0.014, 0.018), nase_z=-0.02, lider=True, falten=True)
    # Arme: Ärmel hochgekrempelt (Oberarm Kasack, Unterarm Haut)
    F.kugel(1, (0, 0.0, 1.23), "fig_kasack", skala=(0.245, 0.15, 0.1), name="schultern")   # runde Schulterlinie auf dem Ei
    SL, SR = Vector((0.21, 0.0, 1.22)), Vector((-0.21, 0.0, 1.22))
    for s in (-1, 1): F.kugel(0.062, (s * 0.2, 0.0, 1.22), "fig_kasack", name="schulter", seg=24)
    if haltung == "tresen":
        # rechter Arm (-x): Ellbogen unten, Hand liegt flach auf dem Tresen; linke Hand um die Kanne auf dem Tresen
        ER, HR = Vector((-0.31, -0.13, tresen - 0.04)), Vector((-0.2, -0.46, tresen + 0.02))
        EL, HL = Vector((0.3, -0.18, tresen - 0.08)), Vector((0.31, -0.44, tresen + 0.07))
    else:
        ER, HR = Vector((-0.3, -0.03, 1.02)), Vector((-0.2, -0.1, 0.9))      # Hand in der Hüfte
        EL, HL = Vector((0.3, -0.03, 1.02)), Vector((0.26, -0.14, 0.86))     # Kanne hängt in der Hand
    for sch, el, ha, hand_mat in ((SR, ER, HR, "fig_haut"), (SL, EL, HL, "fig_haut")):
        F.glied(sch, el, 0.062, "fig_kasack", name="oberarm")
        F.zylinder(0.066, 0.05, el + (ha - el).normalized() * 0.04, "fig_kasack", rot=(ha - el).to_track_quat('Z', 'Y').to_euler(), name="krempel")
        F.glied(el, ha, 0.046, "fig_haut", name="unterarm")
    F.hand(HR, skala=(1.1, 1.25, 0.55) if haltung == "tresen" else (1, 1.1, 0.8))
    F.hand(HL, skala=(1.05, 1.05, 0.9))
    # Thermoskanne (Rost) — der eine Akzent; Deckel dunkel
    kz = tresen + 0.125 if haltung == "tresen" else HL.z - 0.1     # auf dem Tresen stehend bzw. hängend
    ky = HL.y - 0.01
    F.zylinder(0.043, 0.25, (HL.x, ky, kz), "fig_rost", name="kanne")
    F.zylinder(0.036, 0.045, (HL.x, ky, kz + 0.147), "fig_dunkel", name="kannendeckel")
    F.rohr([(HL.x + 0.04, ky, kz + 0.08), (HL.x + 0.075, ky, kz + 0.02), (HL.x + 0.04, ky, kz - 0.06)], 0.006, "fig_rost", fein=False, name="henkel")
    F.kopf = kopf; F.kopfmitte = (0, -0.005, 1.49); F.hoehe = 1.64
    return F


# ====================================================================== Herr K.
def herr_k(ort=(0, 0, 0), drehung=0.0, haltung="sitzen", tag=None, hit="herrk", fein=0.0045, tuete=False):
    """Herr Konrad Baum, 68: weiche Rechteck-Formfamilie, breiter Rücken, gebeugt, Schiebermütze.
    "sitzen": Ursprung ist die Stuhlmitte am Boden (Sitzfläche 0,48 m), Ellbogen auf den Knien, Hände
    gefaltet; "stehen": leicht gebeugt, Hände vorn. tuete=True legt die Plastiktüte neben den rechten Fuß."""
    F = Figur("herrk", ort, drehung, tag, hit, fein)
    RS = (0.27, 0.17, 0.3)     # Rumpf (Strickjacke), weich-rechteckig
    if haltung == "sitzen":
        neig = math.radians(26)
        F.kugel(1, (0, 0.04, 0.58), "fig_hose", skala=(0.24, 0.22, 0.11), name="becken")
        for s in (-1, 1):
            F.glied((s * 0.12, 0.02, 0.56), (s * 0.135, -0.4, 0.53), 0.078, "fig_hose", name="schenkel")
            F.glied((s * 0.135, -0.4, 0.53), (s * 0.145, -0.37, 0.1), 0.066, "fig_hose", name="schienbein")
            F.zylinder(0.05, 0.06, (s * 0.145, -0.37, 0.08), "fig_haut", name="knoechel")
            F.quader((0.11, 0.26, 0.07), (s * 0.15, -0.42, 0.035), "fig_dunkel", fase=0.025, name="pantoffel")
        rumpf_mitte = Vector((0, -0.04, 0.9))
        kopf_ort, kopf_rot = (0, -0.235, 1.33), (math.radians(-10), 0, 0)
        hals = ((0, -0.17, 1.12), (0, -0.215, 1.22))
    else:
        neig = math.radians(12)
        for s in (-1, 1):
            F.glied((s * 0.12, 0.0, 0.1), (s * 0.12, 0.0, 0.8), 0.075, "fig_hose", name="bein")
            F.zylinder(0.05, 0.06, (s * 0.12, 0.0, 0.08), "fig_haut", name="knoechel")
            F.quader((0.11, 0.26, 0.07), (s * 0.125, -0.04, 0.035), "fig_dunkel", fase=0.025, name="pantoffel")
        F.kugel(1, (0, 0.0, 0.82), "fig_hose", skala=(0.24, 0.2, 0.14), name="becken")
        rumpf_mitte = Vector((0, -0.03, 1.1))
        kopf_ort, kopf_rot = (0, -0.16, 1.55), (math.radians(-4), 0, 0)
        hals = ((0, -0.1, 1.36), (0, -0.14, 1.44))
    rot = (neig, 0, 0)
    rumpf = F.leer(rumpf_mitte, rot=rot, name="rumpf")
    F.kugel(1, (0, 0, 0), "fig_strick", skala=RS, eltern=rumpf, name="rumpf")
    F.quader((0.46, 0.2, 0.3), (0, 0.04, -0.02), "fig_strick", fase=0.08, eltern=rumpf, name="ruecken")   # breiter Rücken, weiche Kanten
    # Patientenhemd unter der offenen Strickjacke: Mint-Streifen vorn, Kragen
    F.kugel(1, (0, 0.0, 0.0), "fig_hemd", skala=(0.075, 0.18, 0.31), eltern=rumpf, name="hemd")
    F.zylinder(0.07, 0.03, (0, -0.02, 0.29), "fig_hemd", eltern=rumpf, name="kragen")
    for s in (-1, 1):   # Strickjackenkante: zwei Striche
        F.rohr([(s * 0.055, Figur.vorne(RS, s * 0.055, 0.26, 0.004), 0.26), (s * 0.06, Figur.vorne(RS, s * 0.06, -0.05, 0.004), -0.05), (s * 0.07, Figur.vorne(RS, s * 0.07, -0.26, 0.004), -0.26)], fein * 0.7, "fig_dunkel", eltern=rumpf, name="kante")
    F.glied(hals[0], hals[1], 0.055, "fig_haut", name="hals")
    # Schultern (in Rumpfkoordinaten) und Arme
    SCH = [rumpf.matrix_basis @ Vector((s * 0.2, 0.0, 0.19)) for s in (-1, 1)]
    for p in SCH: F.kugel(0.07, p, "fig_strick", name="schulter", seg=24)
    if haltung == "sitzen":
        ELL = [Vector((s * 0.23, -0.33, 0.8)) for s in (-1, 1)]
        HAND = [Vector((s * 0.05, -0.52, 0.64)) for s in (-1, 1)]
    else:
        ELL = [Vector((s * 0.28, -0.08, 0.98)) for s in (-1, 1)]
        HAND = [Vector((s * 0.07, -0.26, 0.86)) for s in (-1, 1)]
    for s, sch, el, ha in zip((-1, 1), SCH, ELL, HAND):
        F.glied(sch, el, 0.068, "fig_strick", name="oberarm")
        F.glied(el, ha, 0.058, "fig_strick", name="unterarm")
        F.hand(ha, skala=(1.0, 1.2, 0.8), r=0.044)
        if s == 1:   # rotes Fadenarmband der Enkelin am linken Handgelenk
            d = (ha - el).normalized(); w = ha - d * 0.07
            F.ring(0.06, 0.004, w, "fig_armband", rot=d.to_track_quat('Z', 'Y').to_euler(), name="armband")
    # Kopf: breit, weiche Rechteckform; Ohren, Hörgerät rechts (-x)
    kopf = F.leer(kopf_ort, rot=kopf_rot)
    KS = (0.112, 0.106, 0.124)
    F.kugel(1, (0, 0, 0), "fig_haut", skala=KS, eltern=kopf, name="kopf")
    F.quader((0.18, 0.16, 0.15), (0, 0.0, -0.035), "fig_haut", fase=0.05, eltern=kopf, name="kiefer")   # schwere Wangen/Kiefer
    F.ohren(kopf, KS, z=-0.005, groesse=(0.012, 0.024, 0.034))
    F.kugel(1, (-0.108, 0.018, 0.0), "fig_schild", skala=(0.006, 0.012, 0.017), eltern=kopf, fein=True, name="hoergeraet", seg=16)
    for s in (-1, 1):   # graue Haarbüschel unter der Mütze
        F.kugel(1, (s * 0.098, 0.015, 0.045), "fig_haar_grau", skala=(0.028, 0.055, 0.035), eltern=kopf, name="haarbueschel", seg=24)
    # Schiebermütze: flache Krone, überhängend; Schirm vorn, leicht nach unten
    F.kappe(1, (0, 0.012, 0.055), "fig_muetze", skala=(0.13, 0.13, 0.072), ebene=((0, 0, 0.02), (0, 0, 1)), eltern=kopf, name="muetze")
    F.quader((0.12, 0.08, 0.012), (0, -0.14, 0.072), "fig_muetze", fase=0.012, rot=(math.radians(10), 0, 0), eltern=kopf, name="schirm")
    F.kugel(1, (0, -0.06, 0.08), "fig_muetze", skala=(0.11, 0.09, 0.03), eltern=kopf, name="muetzenfront", seg=24)
    # Gesicht: buschige graue Brauen, tiefe Augen, Tränensäcke, Mund waagerecht, kräftige Nase
    F.gesicht(kopf, KS, augen=(0.04, 0.012), augenform=(0.017, 0.006, 0.0095), brauen=(0.022, 0.036, 0.04, 0.006),
              mund=(0.052, -0.062, -0.008), nase=(0.017, 0.016, 0.026), nase_z=-0.022, brauen_mat="fig_haar_grau", brauen_r=fein * 2.0)
    for s in (-1, 1):   # Tränensäcke
        F.rohr([(s * 0.025, Figur.vorne(KS, s * 0.025, -0.003, fein * 0.6), -0.003), (s * 0.044, Figur.vorne(KS, s * 0.044, -0.006, fein * 0.6), -0.006), (s * 0.058, Figur.vorne(KS, s * 0.058, 0.0, fein * 0.6), 0.0)], fein * 0.55, TINTE, eltern=kopf, name="sack")
    if tuete:
        F.quader((0.26, 0.2, 0.34), (-0.4, -0.42, 0.17), "fig_tuete", fase=0.01, name="tuete")
        F.rohr([(-0.46, -0.42, 0.33), (-0.4, -0.42, 0.44), (-0.34, -0.42, 0.33)], 0.006, "fig_tuete", fein=False, name="tuetenhenkel")
    F.kopf = kopf; F.kopfmitte = kopf_ort; F.hoehe = 1.45 if haltung == "sitzen" else 1.68
    return F


# ====================================================================== Dr. Falk
def falk(ort=(0, 0, 0), drehung=0.0, haltung="taschen", tag=None, hit="falk", fein=0.0045):
    """Oberarzt Dr. Falk, 61: dreieckig-vertikale Formfamilie (1,88 m), langer Kittel mit scharfem Saum,
    Hände in den Taschen, Brille an der Kette, Stethoskop, Kaffeefleck, Messingzirkel in der Brusttasche."""
    F = Figur("falk", ort, drehung, tag, hit, fein)
    for s in (-1, 1):
        F.quader((0.1, 0.29, 0.06), (s * 0.11, -0.03, 0.03), "fig_dunkel", fase=0.02, name="schuh")
        F.glied((s * 0.1, 0.0, 0.06), (s * 0.09, 0.0, 0.72), 0.06, "fig_dunkel", name="bein")
    # Kittel: Kegelstumpf, oben schmal, unten weit — der scharfe Saum ist die Kante des Stumpfs
    KH, KZ0 = 0.9, 0.66
    F.kegel(0.3, 0.165, KH, (0, 0.0, KZ0 + KH / 2), "fig_kittel", skala=(1.0, 0.62, 1.0), name="kittel")
    F.kugel(1, (0, 0.0, KZ0 + KH - 0.01), "fig_kittel", skala=(0.172, 0.106, 0.085), name="kittelschulter")
    def kittel_y(x, z, tief=0.0):
        r = 0.165 + (0.3 - 0.165) * (KZ0 + KH - z) / KH
        return Figur.vorne((r, r * 0.62, 1), x, 0, tief)
    # Kittelöffnung: Strich in der Mitte, Revers als zwei flache Keile, Brusttasche links (+x), Taschen unten
    F.rohr([(0, kittel_y(0, 1.33, 0.004), 1.33), (0.005, kittel_y(0.005, 1.1, 0.004), 1.1), (0.01, kittel_y(0.01, KZ0 + 0.02, 0.004), KZ0 + 0.02)], fein * 0.8, "fig_dunkel", name="oeffnung")
    # Hemd (blaugrau) und dunkle Krawatte im V des Kittels, Kragenspitzen am Hals — wie im Porträt
    F.quader((0.12, 0.008, 0.22), (0, kittel_y(0, 1.45, 0.001), 1.45), "fig_hemd_falk", fase=0.003, rot=(math.radians(-6), 0, 0), name="hemd")
    F.quader((0.028, 0.008, 0.2), (0.0, kittel_y(0, 1.42, 0.003), 1.42), "fig_krawatte", fase=0.004, rot=(math.radians(-6), 0, 0), name="krawatte")
    F.quader((0.034, 0.008, 0.03), (0.0, kittel_y(0, 1.535, 0.003), 1.535), "fig_krawatte", fase=0.004, rot=(math.radians(-6), 0, 0), name="knoten")
    for s in (-1, 1):
        F.quader((0.045, 0.008, 0.055), (s * 0.032, kittel_y(s * 0.032, 1.53, 0.002), 1.53), "fig_hemd_falk", fase=0.003, rot=(math.radians(-6), 0, s * math.radians(28)), name="kragen")
    for s in (-1, 1):
        F.quader((0.06, 0.01, 0.17), (s * 0.045, kittel_y(s * 0.045, 1.45, 0.004), 1.45), "fig_kittel", fase=0.004, rot=(math.radians(-6), 0, s * math.radians(32)), name="revers")
        F.quader((0.13, 0.01, 0.1), (s * 0.19, kittel_y(s * 0.19, 1.0, 0.004), 1.0), "fig_kittel", fase=0.004, rot=(math.radians(-5), 0, 0), name="tasche")
    F.quader((0.085, 0.01, 0.1), (0.1, kittel_y(0.1, 1.37, 0.004), 1.37), "fig_kittel", fase=0.004, rot=(math.radians(-6), 0, 0), name="brusttasche")
    # Zirkel schaut aus der Brusttasche: zwei Messingschenkel, Gelenk oben
    zy = kittel_y(0.1, 1.44, 0.012)
    F.rohr([(0.085, zy, 1.4), (0.1, zy, 1.48)], fein * 1.2, "fig_messing", name="zirkel", glatt=False)
    F.rohr([(0.115, zy, 1.4), (0.1, zy, 1.48)], fein * 1.2, "fig_messing", name="zirkel", glatt=False)
    F.kugel(0.008, (0.1, zy, 1.485), "fig_messing", fein=True, name="zirkelgelenk", seg=16)
    # Kaffeefleck rechts unten am Kittel (-x)
    F.kugel(1, (-0.09, kittel_y(-0.09, 1.12, 0.002), 1.12), "fig_fleck", skala=(0.028, 0.004, 0.02), rot=(0, 0, math.radians(15)), name="fleck", seg=24)
    # Arme hängen eng am Körper, Unterarme verschwinden in den Taschen
    for s in (-1, 1):
        sch = Vector((s * 0.175, 0.0, 1.52)); el = Vector((s * 0.215, -0.03, 1.24)); ha = Vector((s * 0.19, kittel_y(s * 0.19, 1.03, 0.0) + 0.01, 1.03))
        F.kugel(0.07, sch, "fig_kittel", name="schulter", seg=24)
        F.glied(sch, el, 0.058, "fig_kittel", name="oberarm")
        F.glied(el, ha, 0.05, "fig_kittel", name="unterarm", kappen=False)
        F.kugel(0.05, el, "fig_kittel", name="ellbogen", seg=24)
    # Stethoskop um den Hals, Bruststück hängt rechts (-x) herunter
    F.rohr([(-0.08, -0.075, 1.43), (-0.12, -0.02, 1.53), (0.0, 0.07, 1.57), (0.12, -0.02, 1.53), (0.1, -0.085, 1.42), (0.085, -0.1, 1.3)], 0.0085, "fig_dunkel", fein=False, name="schlauch")
    F.rohr([(-0.08, -0.075, 1.43), (-0.1, -0.09, 1.36), (-0.14, -0.1, 1.3)], 0.0085, "fig_dunkel", fein=False, name="schlauch")
    F.zylinder(0.024, 0.012, (0.085, -0.1, 1.29), "fig_metall", rot=(math.radians(90), 0, 0), name="bruststueck")
    F.glied((0, 0.0, 1.54), (0, -0.01, 1.64), 0.048, "fig_haut", name="hals")
    # Kopf: schmal und lang, leicht nach vorn geneigt (er schaut auf Dinge herab)
    kopf = F.leer((0, -0.012, 1.77), rot=(math.radians(7), 0, 0))
    KS = (0.094, 0.104, 0.128)
    F.kugel(1, (0, 0, 0), "fig_haut", skala=KS, eltern=kopf, name="kopf")
    F.quader((0.12, 0.11, 0.1), (0, 0.0, -0.06), "fig_haut", fase=0.04, eltern=kopf, name="kinn")   # langes Kinn
    F.ohren(kopf, KS, z=-0.01, groesse=(0.012, 0.022, 0.032))
    # Graues Haar: hoher, zurückweichender Ansatz (Schale, Ebene nach vorn-unten geneigt), kurz an den Seiten
    F.kappe(1, (0, 0.012, 0.012), "fig_haar_grau", skala=(0.098, 0.108, 0.125), ebene=((0, 0, 0.33), (0, 0.4, 0.92)), eltern=kopf, name="haar")
    for s in (-1, 1):
        F.kugel(1, (s * 0.086, 0.025, -0.01), "fig_haar_grau", skala=(0.022, 0.06, 0.05), eltern=kopf, name="schlaefe", seg=24)
    # Gesicht: schmale Augen, dünne Brauen, Mund gerade und schmal, lange Nase
    F.gesicht(kopf, KS, augen=(0.037, 0.016), augenform=(0.015, 0.005, 0.006), brauen=(0.02, 0.042, 0.046, 0.0),
              mund=(0.046, -0.064, -0.003), nase=(0.013, 0.016, 0.03), nase_z=-0.018, brauen_mat="fig_haar_grau", brauen_r=fein * 1.1)
    for s in (-1, 1):   # Nasolabialfalten
        F.rohr([(s * 0.022, Figur.vorne(KS, s * 0.022, -0.03, fein * 0.6), -0.03), (s * 0.036, Figur.vorne(KS, s * 0.036, -0.07, fein * 0.6), -0.07)], fein * 0.5, TINTE, eltern=kopf, name="falte")
    # Brille auf der Nase, Bügel zu den Ohren, Kette von den Bügelenden hinter den Hals
    by = Figur.vorne(KS, 0.037, 0.016, 0.01)
    F.brille(kopf, (0, by, 0.016), R=0.021, abstand=0.037,
             buegel=[(0.058, by + 0.004, 0.018), (0.094, 0.0, 0.012)],
             kette=[(0.096, 0.005, 0.005), (0.105, 0.035, -0.08), (0.07, 0.075, -0.15), (0.0, 0.095, -0.18)])
    F.kopf = kopf; F.kopfmitte = (0, -0.012, 1.77); F.hoehe = 1.9
    return F


# ====================================================================== Dr. Wieser
def wieser(ort=(0, 0, 0), drehung=0.0, haltung="tritt", tag=None, hit="wieser", fein=0.0045):
    """Dr. Nora Wieser, 41 (1,72 m): schmale Ovale (Kopf, Rumpf, Ärmel), Gegenakzent der harte Winkel des rechten
    Ellbogens — der Arm hält das blaue EKG-Lineal hoch. Kittel offen über dunklem Rollkragen, kurzes graues Haar mit
    dunkler Strähne, keine Brille, kein Stethoskop (liegt über der Stuhllehne), kobaltblaue Sneaker.
    "tritt": linker Fuß (lokal +x, vorn) auf einem 0,25 m hohen Tritt, der nicht Teil der Figur ist; der Kopf dreht
    sich um −drehung zurück, also zur Kamera, während der Körper zur Liege zeigt. "stehen": beide Füße am Boden."""
    F = Figur("wieser", ort, drehung, tag, hit, fein)
    # Beine (dunkle Hose) und Sneaker (Kobalt, helle Sohle)
    def sneaker(ort, rot=(0, 0, 0)):
        F.quader((0.1, 0.27, 0.055), (ort[0], ort[1], ort[2] + 0.0475), "fig_kobalt", fase=0.02, rot=rot, name="sneaker")
        F.quader((0.1, 0.27, 0.02), (ort[0], ort[1], ort[2] + 0.01), "fig_sohle", fase=0.006, rot=rot, name="sohle")
    sneaker((-0.1, 0.0, 0.0))
    F.glied((-0.1, 0.0, 0.08), (-0.09, 0.0, 0.9), 0.062, "fig_hose_wieser", name="bein")
    if haltung == "tritt":
        knie, fuss = Vector((0.24, -0.3, 0.6)), Vector((0.3, -0.27, 0.33))
        F.glied((0.1, 0.0, 0.9), knie, 0.066, "fig_hose_wieser", name="schenkel")
        F.glied(knie, fuss, 0.058, "fig_hose_wieser", name="schienbein")
        sneaker((0.3, -0.29, 0.25), rot=(0, 0, math.radians(8)))
    else:
        sneaker((0.1, 0.0, 0.0))
        F.glied((0.1, 0.0, 0.08), (0.09, 0.0, 0.9), 0.062, "fig_hose_wieser", name="bein")
    # Rumpf: schmale Ovale — Hüfte, Rollkragen-Oberkörper; darüber der offene Kittel als hinten geschlossene Schale
    F.kugel(1, (0, 0.0, 0.93), "fig_hose_wieser", skala=(0.19, 0.14, 0.14), name="huefte")
    F.kugel(1, (0, 0.0, 1.2), "fig_rollkragen", skala=(0.185, 0.125, 0.3), name="rumpf")
    F.kappe(1, (0, 0.0, 1.2), "fig_kittel", skala=(0.215, 0.15, 0.34), ebene=((0, -0.03, 0), (0, 1, 0)), name="kittel")
    F.kappe(1, (0, 0.0, 0.8), "fig_kittel", skala=(0.21, 0.145, 0.3), ebene=((0, -0.05, 0), (0, 1, 0)), name="kittelsaum")
    for s in (-1, 1):   # Revers
        F.quader((0.055, 0.01, 0.16), (s * 0.06, Figur.vorne((0.185, 0.125, 0.3), s * 0.06, 0.2, 0.006), 1.4), "fig_kittel", fase=0.004,
                 rot=(math.radians(-6), 0, s * math.radians(30)), name="revers")
    F.zylinder(0.058, 0.09, (0, -0.005, 1.53), "fig_rollkragen", name="kragen")
    # Schultern und Arme (Kittelärmel, Hände Haut)
    F.kugel(1, (0, 0.0, 1.42), "fig_kittel", skala=(0.21, 0.13, 0.08), name="schultern")
    SR, SL = Vector((-0.2, 0.0, 1.42)), Vector((0.2, 0.0, 1.42))
    for p in (SR, SL): F.kugel(0.06, p, "fig_kittel", name="schulter", seg=24)
    ER, HR = Vector((-0.27, -0.1, 1.17)), Vector((-0.21, -0.31, 1.3))        # rechter Arm: harter Winkel, Lineal neben dem Kinn
    EL, HL = Vector((0.3, 0.0, 1.17)), Vector((0.27, -0.14, 0.95))           # linker Arm hängt leicht vor
    for sch, el, ha in ((SR, ER, HR), (SL, EL, HL)):
        F.glied(sch, el, 0.056, "fig_kittel", name="oberarm")
        F.glied(el, ha, 0.048, "fig_kittel", name="unterarm")
    F.hand(HR, r=0.04, skala=(1.0, 1.1, 0.8)); F.hand(HL, r=0.04, skala=(1.0, 1.15, 0.7))
    # Das blaue Lineal zwischen zwei Fingern, hochgehalten
    F.quader((0.045, 0.004, 0.19), (HR.x + 0.01, HR.y - 0.03, HR.z + 0.09), "fig_kobalt", fase=0, rot=(math.radians(8), 0, math.radians(25)), name="lineal")
    F.glied((0, -0.005, 1.56), (0, -0.01, 1.6), 0.046, "fig_haut", name="hals")
    # Kopf: schmales Oval, zur Kamera zurückgedreht
    kopf = F.leer((0, -0.01, 1.62), rot=(math.radians(3), 0, math.radians(-drehung if haltung == "tritt" else 0)))
    KS = (0.09, 0.1, 0.12)
    F.kugel(1, (0, 0, 0), "fig_haut", skala=KS, eltern=kopf, name="kopf")
    F.ohren(kopf, KS, z=-0.005, groesse=(0.011, 0.02, 0.03))
    # kurzes graues Haar, zurückgekämmt; eine dunkle Strähne vorn
    F.kappe(1, (0, 0.012, 0.012), "fig_haar_wieser", skala=(0.1, 0.106, 0.125), ebene=((0, 0, 0.2), (0, 0.42, 0.9)), eltern=kopf, name="haar")
    for s in (-1, 1):
        F.kugel(1, (s * 0.088, 0.02, 0.02), "fig_haar_wieser", skala=(0.024, 0.06, 0.055), eltern=kopf, name="schlaefe", seg=24)
    # Die dunkle Strähne steht nur in der Stilphrase: als Grundkörper (Rohr auf der Haarschale) zeichnete Kontext
    # sie als Stab auf dem Kopf.
    # Gesicht: neutral-wach, Brauen leicht hoch („und?"), schmaler Mund; Brauen dünn, Nase klein, Augen groß —
    # mit dicken Brauen und großer Nase zeichnete Kontext aus dem Blockout einen Mann
    F.gesicht(kopf, KS, augen=(0.036, 0.014), augenform=(0.018, 0.005, 0.0105), brauen=(0.018, 0.042, 0.046, 0.004),
              mund=(0.04, -0.058, 0.004), nase=(0.009, 0.011, 0.018), nase_z=-0.018, brauen_r=fein * 0.75)
    F.kopf = kopf; F.kopfmitte = (0, -0.01, 1.62); F.hoehe = 1.72
    return F


# ====================================================================== Jonas
def jonas(ort=(0, 0, 0), drehung=0.0, haltung="liegen", tag=None, hit="jonas", fein=0.0045):
    """Jonas Prem, 24 (1,80 m): lange Rechtecke (Rumpf, Beine), Gegenakzent der runde Kopf mit den Kopfhörern um den
    Hals. "liegen": Ursprung ist die Liegefläche unter der Körpermitte, lokale +y-Achse zum Kopfende, Gesicht nach
    oben. Lage zum EKG (docs/FACHREGELN.md, Lektion 2): flach und entspannt auf dem Rücken, beide Beine gestreckt und
    nicht übereinander, Arme locker neben dem Körper; T-Shirt bis unter die Achseln hochgeschoben (Brust frei — die
    Brustwandelektroden sind die Aufgabe der Spielerin), Hosenbeine hochgekrempelt, Klemmen auf der Haut: Handgelenke
    und Unterschenkel knapp über den Knöcheln. Ampel-Regel je Körperseite: rechter Arm ROT (lokal −x; das Rost-Objekt),
    linker Arm GELB, linkes Bein GRÜN, rechtes Bein SCHWARZ. Die Leitungen dazu sind Raumobjekte (szene_lehrsaal.py),
    hier nur kurze Stummel. Socken senfgelb, die Schuhe stehen unter der Liege.
    "stehen": aufrecht, Kopfhörer um den Hals (Porträt-Blockout)."""
    F = Figur("jonas", ort, drehung, tag, hit, fein)
    if haltung == "liegen":
        F.kugel(1, (0, -0.02, 0.09), "fig_jeans", skala=(0.2, 0.17, 0.1), name="becken")
        F.quader((0.36, 0.42, 0.18), (0, 0.22, 0.09), "fig_haut", fase=0.07, name="bauch")           # Brust und Bauch frei
        F.quader((0.42, 0.14, 0.21), (0, 0.5, 0.1), "fig_shirt_jonas", fase=0.05, name="shirt")       # T-Shirt, gerollt unter den Achseln
        SCH = [Vector((s * 0.2, 0.55, 0.1)) for s in (-1, 1)]
        for p in SCH: F.kugel(0.065, p, "fig_shirt_jonas", name="schulter", seg=24)
        # Arme locker neben dem Körper, Handflächen oben; rechts (−x) rot, links (+x) gelb am Handgelenk
        for s in (-1, 1):
            el, ha = Vector((s * 0.3, 0.25, 0.06)), Vector((s * 0.33, -0.06, 0.06))
            F.glied(SCH[0 if s < 0 else 1], el, 0.052, "fig_shirt_jonas", name="oberarm")
            F.glied(el, ha, 0.044, "fig_haut", name="unterarm")
            F.hand(ha, r=0.042, skala=(1.0, 1.2, 0.6))
        def klemme(ort, mat, nach):
            F.quader((0.04, 0.06, 0.036), ort, mat, fase=0.005, name="klemme")
            F.rohr([ort, (ort[0] + nach[0] * 0.5, ort[1] + nach[1] * 0.5, ort[2] - 0.02), (ort[0] + nach[0], ort[1] + nach[1], ort[2] - 0.045)],
                   fein * 0.9, "fig_dunkel", fein=False, name="klemmenkabel")
        klemme((-0.33, 0.02, 0.09), "fig_klemme_rot", (-0.06, 0.0))
        klemme((0.33, 0.02, 0.09), "fig_klemme_gelb", (0.06, 0.0))
        # Beine gestreckt, leicht auseinander; Jeans bis zur Wade hochgekrempelt, darunter Haut, Füße in senfgelben Socken
        for s, mat in ((-1, "fig_klemme_schwarz"), (1, "fig_klemme_gruen")):
            F.glied((s * 0.11, -0.05, 0.08), (s * 0.14, -0.6, 0.075), 0.075, "fig_jeans", name="schenkel")
            F.zylinder(0.08, 0.05, (s * 0.14, -0.6, 0.075), "fig_jeans", rot=(math.radians(90), 0, 0), name="krempel")
            F.glied((s * 0.14, -0.62, 0.07), (s * 0.15, -0.86, 0.065), 0.058, "fig_haut", name="schienbein")
            F.kugel(1, (s * 0.15, -0.91, 0.1), "fig_senf", skala=(0.05, 0.07, 0.11), name="fuss")
            klemme((s * 0.15, -0.78, 0.1), mat, (s * 0.06, 0.0))
        # Hals, Kopfhörer um den Hals (Bügel als Ring, zwei Muscheln), Kabel zur Hosentasche (links)
        F.glied((0, 0.6, 0.09), (0, 0.7, 0.1), 0.05, "fig_haut", name="hals")
        F.ring(0.085, 0.012, (0, 0.64, 0.085), "fig_dunkel", rot=(math.radians(90), 0, 0), fein=False, name="kopfhoerer")
        for s in (-1, 1):
            F.kugel(1, (s * 0.1, 0.62, 0.07), "fig_dunkel", skala=(0.03, 0.04, 0.045), name="muschel", seg=24)
        F.rohr([(0.11, 0.6, 0.05), (0.19, 0.42, 0.12), (0.2, 0.15, 0.1), (0.2, 0.0, 0.12)], fein * 0.7, "fig_dunkel", name="kopfhoererkabel")
        kopf_ort, kopf_rot = (0, 0.8, 0.11), (math.radians(-84), 0, 0)      # Gesicht nach oben, Scheitel zum Kopfende
        F.hoehe = 0.45
    else:
        for s in (-1, 1):
            F.kugel(1, (s * 0.11, -0.04, 0.05), "fig_senf", skala=(0.05, 0.13, 0.05), name="fuss")
            F.glied((s * 0.11, 0.0, 0.08), (s * 0.1, 0.0, 0.95), 0.07, "fig_jeans", name="bein")
        F.kugel(1, (0, 0.0, 0.98), "fig_jeans", skala=(0.2, 0.15, 0.1), name="becken")
        F.quader((0.38, 0.2, 0.5), (0, 0.0, 1.27), "fig_shirt_jonas", fase=0.07, name="rumpf")
        for s in (-1, 1):
            F.kugel(0.065, (s * 0.2, 0.0, 1.5), "fig_shirt_jonas", name="schulter", seg=24)
            F.glied((s * 0.2, 0.0, 1.5), (s * 0.24, -0.02, 1.22), 0.052, "fig_shirt_jonas", name="oberarm")
            F.glied((s * 0.24, -0.02, 1.22), (s * 0.23, -0.08, 0.98), 0.044, "fig_haut", name="unterarm")
            F.hand((s * 0.23, -0.09, 0.95), r=0.042)
        F.glied((0, 0.0, 1.52), (0, -0.01, 1.6), 0.05, "fig_haut", name="hals")
        F.ring(0.085, 0.012, (0, -0.01, 1.52), "fig_dunkel", rot=(math.radians(10), 0, 0), fein=False, name="kopfhoerer")
        for s in (-1, 1):
            F.kugel(1, (s * 0.1, -0.03, 1.5), "fig_dunkel", skala=(0.03, 0.04, 0.045), name="muschel", seg=24)
        kopf_ort, kopf_rot = (0, -0.01, 1.68), (math.radians(2), 0, 0)
        F.hoehe = 1.8
    # Kopf: rund (Gegenakzent zu den langen Rechtecken), dunkles kurzes Haar, ein paar abstehende Strähnen
    kopf = F.leer(kopf_ort, rot=kopf_rot)
    KS = (0.105, 0.105, 0.118)
    F.kugel(1, (0, 0, 0), "fig_haut", skala=KS, eltern=kopf, name="kopf")
    F.ohren(kopf, KS, z=-0.005, groesse=(0.011, 0.021, 0.03))
    F.kappe(1, (0, 0.012, 0.014), "fig_haar_jonas", skala=(0.11, 0.112, 0.122), ebene=((0, 0, 0.18), (0, 0.4, 0.9)), eltern=kopf, name="haar")
    for s in (-1, 1):
        F.kugel(1, (s * 0.095, 0.02, 0.01), "fig_haar_jonas", skala=(0.025, 0.065, 0.06), eltern=kopf, name="schlaefe", seg=24)
    # Gesicht: entspannt, halbes Lächeln, offene Augen (er redet mit der Decke)
    F.gesicht(kopf, KS, augen=(0.038, 0.012), augenform=(0.017, 0.005, 0.0095), brauen=(0.02, 0.038, 0.04, 0.002),
              mund=(0.05, -0.058, 0.01), nase=(0.012, 0.013, 0.022), nase_z=-0.018)
    F.kopf = kopf; F.kopfmitte = kopf_ort
    return F


FIGUREN = {"marlene": marlene, "herr_k": herr_k, "falk": falk, "wieser": wieser, "jonas": jonas}
