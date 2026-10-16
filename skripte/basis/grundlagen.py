"""Grundlagen für alle Teile: Fachmaß, Spiel, Wandstärken, Schrift und STL-Export.
Alle Maße in mm. Wird von allen anderen Skripten benutzt.
"""
import numpy as np
import trimesh
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from manifold3d import CrossSection, FillRule, set_circular_segments

set_circular_segments(48)                 # Kreise aus 48 Segmenten (wichtig für identische Ergebnisse)

FACH_B, FACH_H = 32, 26                   # Innenmaß eines Fachs
LUFT = 0.4                                # Spiel Schublade ↔ Fach (pro Seite)
SW = 1.2                                  # Wandstärke Schublade
FRONT_T = 2.0                             # Dicke Schubladenfront
DB = FACH_B - 2 * LUFT                    # Breite Schubladen-Korpus
DH = FACH_H - 2 * LUFT                    # Höhe Schubladen-Korpus
SCHRIFT = FontProperties(family="DejaVu Sans", weight="bold")

def text_cs(txt, hoehe):
    """Text als 2D-Form, zentriert, Höhe des Textes = hoehe."""
    tp = TextPath((0, 0), txt, size=1, prop=SCHRIFT)
    polys = [p for p in tp.to_polygons() if len(p) > 2]
    cs = CrossSection([[tuple(pt) for pt in p] for p in polys], FillRule.EvenOdd)
    (x0, y0), (x1, y1) = cs.bounds()[:2], cs.bounds()[2:]
    k = hoehe / (y1 - y0)
    return cs.translate([-(x0 + x1) / 2, -(y0 + y1) / 2]).scale([k, k])

def text_cs_einzeln(txt, hoehe):
    """Wie text_cs, aber jeder Buchstabe einzeln vereinigt – nötig, wenn sich Buchstaben überlappen (z. B. „KA“)."""
    from matplotlib.textpath import text_to_path
    cs = CrossSection()
    for i, z in enumerate(txt):
        if z == " ":
            continue
        x = text_to_path.get_text_width_height_descent(txt[:i], SCHRIFT, ismath=False)[0] / SCHRIFT.get_size_in_points() if i else 0
        tp = TextPath((0, 0), z, size=1, prop=SCHRIFT)
        polys = [p for p in tp.to_polygons() if len(p) > 2]
        if polys:
            cs += CrossSection([[tuple(pt) for pt in p] for p in polys], FillRule.EvenOdd).translate([x, 0])
    (x0, y0), (x1, y1) = cs.bounds()[:2], cs.bounds()[2:]
    k = hoehe / (y1 - y0)
    return cs.translate([-(x0 + x1) / 2, -(y0 + y1) / 2]).scale([k, k])

def stern(r_aussen, r_innen, n=5):
    pts = []
    for i in range(2 * n):
        r = r_aussen if i % 2 == 0 else r_innen
        w = np.pi / 2 + i * np.pi / n
        pts.append((r * np.cos(w), r * np.sin(w)))
    return CrossSection([pts])

def export(m, name):
    """Manifold als STL speichern; gibt das trimesh-Objekt zum Prüfen zurück."""
    mm = m.to_mesh()
    t = trimesh.Trimesh(mm.vert_properties[:, :3], mm.tri_verts, process=False)
    t.export(name)
    return t
