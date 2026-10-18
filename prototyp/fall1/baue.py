# -*- coding: utf-8 -*-
"""Baut den spielbaren Prototyp von Fall 1 („Darf Herr Baum heim?", docs/REDESIGN_FALL1.md) als eine Datei.

    python3 prototyp/fall1/baue.py        → bau/prototyp_fall1.html

Eingebettet: web/stil.css, web/ekg.js, web/raetsel_zirkel.js (unverändert aus dem Spiel), prototyp/bewegung/leben.js,
prototyp/fall1/{fall1.css, motor.js, daten.js}; Bilder aus art/ als base64 (Raumebenen, Figuren, Porträts), das
Szenenbild am Tresen wie gen/kunst.py als JPEG ≤ 300 kB; die Kurve aus data/ekg_daten.json (LUDB 39, Ableitung II,
mit Annotation). Das Spiel (web/, text/, tools/) bleibt unverändert."""
import base64
import io
import json
import os
import re

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HIER = os.path.join(WURZEL, "prototyp", "fall1")
SZENE = os.path.join(WURZEL, "art", "szenen", "aufnahme")
BAU = os.path.join(WURZEL, "bau")
TRESEN = os.path.join(WURZEL, "art", "szenenbilder", "aufnahme_tresen_neu_beleuchtet",
                      "openai_gpt-image-2.5-sunburst_20261013-1920.png")      # wie gen/kunst.py SZENENBILDER
MAX_KB = 300


def lies(*teile):
    with open(os.path.join(WURZEL, *teile), encoding="utf-8") as f:
        return f.read()


def uri(pfad, typ="image/png"):
    with open(pfad, "rb") as f:
        return "data:" + typ + ";base64," + base64.b64encode(f.read()).decode("ascii")


def tresen_jpeg():
    from PIL import Image
    bild = Image.open(TRESEN).convert("RGB")
    for q in (85, 80, 75, 70, 65):
        puffer = io.BytesIO()
        bild.save(puffer, "JPEG", quality=q, optimize=True, progressive=True)
        roh = puffer.getvalue()
        if len(roh) <= MAX_KB * 1024:
            break
    print("Szenenbild Tresen: %dx%d, JPEG q%d, %d kB" % (bild.width, bild.height, q, len(roh) // 1024))
    return "data:image/jpeg;base64," + base64.b64encode(roh).decode("ascii")


def ekg_39():
    alle = json.loads(lies("data", "ekg_daten.json"))
    e = next(x for x in alle if x["id"] == 39)
    return {"id": 39, "sig": {"werte": [round(v, 4) for v in e["sig"]["werte"]], "fs": e["sig"]["fs"],
                              "lead": e["sig"].get("lead", "ii")},
            "schlaege": e["schlaege"], "mess": e["mess"], "rhythmus": e.get("rhythmus")}


def main():
    assets = {
        "hintergrund": uri(os.path.join(SZENE, "hintergrund.png")),
        "mittelgrund": uri(os.path.join(SZENE, "mittelgrund.png")),
        "tuete": uri(os.path.join(SZENE, "figuren", "tuete.png")),
        "marleneFig": uri(os.path.join(SZENE, "figuren", "marlene.png")),
        "herrkFig": uri(os.path.join(SZENE, "figuren", "herrk.png")),
        "portraits": {n: uri(os.path.join(WURZEL, "art", "portraits", n + ".png")) for n in ("marlene", "herr_k", "falk")},
        "tresen": tresen_jpeg(),
        "ekg39": ekg_39(),
    }
    teile = {
        "STIL_CSS": lies("web", "stil.css"),
        "PROTO_CSS": lies("prototyp", "fall1", "fall1.css"),
        "ASSETS": json.dumps(assets, ensure_ascii=False, separators=(",", ":")),
        "EKG_JS": lies("web", "ekg.js"),
        "ZIRKEL_JS": lies("web", "raetsel_zirkel.js"),
        "LEBEN_JS": lies("prototyp", "bewegung", "leben.js"),
        "MOTOR_JS": lies("prototyp", "fall1", "motor.js"),
        "DATEN_JS": lies("prototyp", "fall1", "daten.js"),
    }
    for name, inhalt in teile.items():
        assert "</script" not in inhalt.lower() or name in ("STIL_CSS", "PROTO_CSS"), name + " enthält </script>"
        assert "{{" not in inhalt, name + " enthält {{"
    vorlage = lies("prototyp", "fall1", "fall1.html")
    html = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: teile[m.group(1)], vorlage)
    assert "{{" not in html, "offener Platzhalter"
    os.makedirs(BAU, exist_ok=True)
    ziel = os.path.join(BAU, "prototyp_fall1.html")
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(html)
    print(ziel, round(os.path.getsize(ziel) / 1024), "kB")


if __name__ == "__main__":
    main()
