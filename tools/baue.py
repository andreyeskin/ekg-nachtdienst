# -*- coding: utf-8 -*-
"""Bündelt das Spiel zu einer einzigen HTML-Datei ohne äußere Anfragen.

Aufruf:  python3 tools/baue.py [ziel.html]
Ergebnis: bau/nachtdienst.html — doppelklickbar, auch auf dem iPad in
Documents oder Safari lauffähig, ohne Server, ohne Netz.
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(WURZEL, "web")
BAU = os.path.join(WURZEL, "bau")
DATEN = os.path.join(WURZEL, "data") if os.path.isdir(os.path.join(WURZEL, "data")) else BAU

SKRIPTE = ["ekg.js", "szene.js", "dialog.js", "mappe.js", "raetsel_zirkel.js", "spiel.js"]


def lies(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def baue(ziel=None):
    html = lies(os.path.join(WEB, "index.html"))
    css = lies(os.path.join(WEB, "stil.css"))
    kunst = json.load(open(os.path.join(BAU, "kunst.json"), encoding="utf-8"))
    ekg = json.load(open(os.path.join(DATEN, "ekg_daten.json"), encoding="utf-8"))

    # Nur die Aufnahmen mitnehmen, die das Spiel wirklich anfasst, plus Reserve
    gebraucht = set()
    for js in SKRIPTE:
        for m in re.finditer(r"AUFNAHME_EKG\s*=\s*(\d+)", lies(os.path.join(WEB, js))):
            gebraucht.add(int(m.group(1)))
    auswahl = [r for r in ekg if r["id"] in gebraucht] or ekg[:4]
    # Für den Wiederspielwert: je Rhythmusgruppe eine weitere Aufnahme
    gesehen = {r["rhythmus"] for r in auswahl}
    for r in ekg:
        if r["rhythmus"] not in gesehen:
            auswahl.append(r)
            gesehen.add(r["rhythmus"])

    daten = ("window.KUNST=" + json.dumps(kunst, ensure_ascii=False, separators=(",", ":")) + ";\n"
             "window.EKG_DATEN=" + json.dumps(auswahl, ensure_ascii=False, separators=(",", ":")) + ";")

    html = html.replace('<link rel="stylesheet" href="stil.css">',
                        "<style>\n" + css + "\n</style>")
    html = html.replace('<script src="daten.js"></script>',
                        "<script>\n" + daten + "\n</script>")
    for js in SKRIPTE:
        html = html.replace('<script src="%s"></script>' % js,
                            "<script>\n" + lies(os.path.join(WEB, js)) + "\n</script>")

    rest = re.findall(r'(?:src|href)="(?!data:)([^"]+)"', html)
    aussen = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
    os.makedirs(BAU, exist_ok=True)
    ziel = ziel or os.path.join(BAU, "nachtdienst.html")
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(html)
    print("%s | %.2f MB | Aufnahmen: %d | offene Verweise: %s | extern: %s"
          % (os.path.basename(ziel), os.path.getsize(ziel) / 1e6, len(auswahl), rest or "keine", aussen or "keine"))
    if rest or aussen:
        sys.exit(1)
    return ziel


if __name__ == "__main__":
    baue(sys.argv[1] if len(sys.argv) > 1 else None)
