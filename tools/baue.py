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

SKRIPTE = ["sprache.js", "ekg.js", "szene.js", "dialog.js", "mappe.js", "stand.js",
           "raetsel_zirkel.js", "raetsel_reizleitung.js", "raetsel_schirme.js", "raetsel_ampel.js",
           "motor/fenster.js", "motor/szenenbild.js", "motor/fall.js",
           "faelle/aufnahme_baum.js",
           "spiel.js", "huelle.js"]
SPRACHEN = ("de", "en", "ru")


def lies(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def kunst_aktuell():
    """Bilder neu zeichnen, wenn der Zeichner jünger ist als sein Ergebnis."""
    quelle = os.path.join(WURZEL, "gen", "kunst.py")
    ziel = os.path.join(BAU, "kunst.json")
    if os.path.exists(ziel) and os.path.getmtime(ziel) >= os.path.getmtime(quelle):
        return
    os.makedirs(BAU, exist_ok=True)
    import subprocess
    subprocess.run([sys.executable, quelle], check=True)


def baue(ziel=None):
    kunst_aktuell()
    html = lies(os.path.join(WEB, "index.html"))
    css = lies(os.path.join(WEB, "stil.css"))
    kunst = json.load(open(os.path.join(BAU, "kunst.json"), encoding="utf-8"))
    ekg = json.load(open(os.path.join(DATEN, "ekg_daten.json"), encoding="utf-8"))

    # Nur die Aufnahmen mitnehmen, die das Spiel wirklich anfasst, plus Reserve.
    # Jede Konstante, deren Name auf _EKG endet (AUFNAHME_EKG, SCHIRM_..._EKG),
    # nennt eine Aufnahme, die das Spiel zeigt.
    gebraucht = set()
    for js in SKRIPTE:
        # Konstanten *_EKG = N (Kapitel), aufnahme: N (Fall-Tabellen der Rätsel) und haupt: N (Fälle, KONZEPT §6)
        for m in re.finditer(r"(?:\b[A-Z][A-Z0-9_]*_EKG\s*=|\baufnahme:|\bhaupt:)\s*(\d+)", lies(os.path.join(WEB, js))):
            gebraucht.add(int(m.group(1)))
    fehlt = gebraucht - {r["id"] for r in ekg}
    if fehlt:
        print("Aufnahmen fehlen in den Daten:", sorted(fehlt))
        sys.exit(1)
    auswahl = [r for r in ekg if r["id"] in gebraucht] or ekg[:4]
    # Für den Wiederspielwert: je Rhythmusgruppe eine weitere Aufnahme
    gesehen = {r["rhythmus"] for r in auswahl}
    for r in ekg:
        if r["rhythmus"] not in gesehen:
            auswahl.append(r)
            gesehen.add(r["rhythmus"])

    woerter = {}
    textordner = os.path.join(WURZEL, "text")
    if os.path.isdir(textordner):
        for sprache in ("en", "ru"):
            pfad = os.path.join(textordner, sprache + ".json")
            if os.path.exists(pfad):
                tisch = json.load(open(pfad, encoding="utf-8"))
                woerter[sprache] = {k: v for k, v in tisch.items() if v}
    # Texte über IDs (KONZEPT §6.2): text/<sprache>/<fall>.json — alle Fälle einer Sprache in einen Tisch.
    texte = {}
    for sprache in SPRACHEN:
        ordner = os.path.join(textordner, sprache)
        texte[sprache] = {}
        if os.path.isdir(ordner):
            for datei in sorted(os.listdir(ordner)):
                if datei.endswith(".json"):
                    tisch = json.load(open(os.path.join(ordner, datei), encoding="utf-8"))
                    doppelt = set(tisch) & set(texte[sprache])
                    if doppelt:
                        print("Text-ID doppelt in", sprache, ":", sorted(doppelt)[:5])
                        sys.exit(1)
                    texte[sprache].update({k: v for k, v in tisch.items() if v})
    for sprache in ("en", "ru"):
        fehlt = sorted(set(texte["de"]) - set(texte[sprache]))
        if fehlt:
            print("Übersetzung fehlt (%s): %d IDs, z. B. %s" % (sprache, len(fehlt), fehlt[:5]))
            sys.exit(1)

    daten = ("window.KUNST=" + json.dumps(kunst, ensure_ascii=False, separators=(",", ":")) + ";\n"
             "window.WOERTER=" + json.dumps(woerter, ensure_ascii=False, separators=(",", ":")) + ";\n"
             "window.TEXTE=" + json.dumps(texte, ensure_ascii=False, separators=(",", ":")) + ";\n"
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
