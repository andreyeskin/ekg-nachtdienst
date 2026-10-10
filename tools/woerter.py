# -*- coding: utf-8 -*-
"""Sammelt alle deutschen Sätze, die im Spiel sichtbar werden, und prüft die
Übersetzungen.

    python3 tools/woerter.py            — zeigt, was in en/ru fehlt
    python3 tools/woerter.py --neu      — schreibt fehlende Einträge als
                                          leere Felder in die Sprachdateien

Der deutsche Satz ist der Schlüssel (siehe web/sprache.js). Gesammelt wird aus
zwei Quellen: direkte T("…")-Aufrufe und die Textfelder der Spieldaten.
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(WURZEL, "web")
TEXT = os.path.join(WURZEL, "text")
DATEIEN = ["spiel.js", "dialog.js", "mappe.js", "stand.js", "raetsel_zirkel.js", "raetsel_reizleitung.js", "raetsel_schirme.js",
           "raetsel_ampel.js", "szene.js"]

# Felder, deren Inhalt der Spieler zu sehen bekommt
FELDER = ["text", "warum", "titel", "auftrag", "name", "wie", "anfang", "ende",
          "endeText", "fuss", "hinweis", "deutung", "frage", "lage", "danach", "ampel"]

STRING = r'"((?:[^"\\]|\\.)*)"'
KETTE = re.compile(r'%s(?:\s*\+\s*%s)*' % (STRING, STRING))


def ketten(ausdruck):
    """„a" + „b" → ab. Nur reine Zeichenkettenketten, sonst nichts."""
    teile = re.findall(STRING, ausdruck)
    if not teile:
        return None
    # Wenn zwischen den Teilen etwas anderes steht als + und Leerraum, ist es keine reine Kette
    rest = re.sub(STRING, "", ausdruck)
    if re.sub(r'[\s+]', "", rest):
        return None
    return "".join(t.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\") for t in teile)


def sammle_aus(quelle):
    gefunden = []
    # 1 · T( … ) — Argument bis zum passenden Komma oder zur schließenden Klammer
    for m in re.finditer(r'\bT\(\s*', quelle):
        i = m.end()
        tiefe, start, in_str, esc = 0, i, False, False
        while i < len(quelle):
            c = quelle[i]
            if in_str:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': in_str = False
            elif c == '"': in_str = True
            elif c in "([{": tiefe += 1
            elif c in ")]}":
                if tiefe == 0: break
                tiefe -= 1
            elif c == "," and tiefe == 0: break
            i += 1
        ausdruck = quelle[start:i]
        t = ketten(ausdruck)
        if t:
            gefunden.append(t)
        else:
            # z. B. T(bedingung ? "A" : "B") — jede Zeichenkette einzeln
            for einzeln in re.findall(STRING, ausdruck):
                gefunden.append(einzeln.replace('\\"', '"'))
    # 2 · Textfelder der Daten
    for feld in FELDER:
        for m in re.finditer(r'\b%s:\s*(%s(?:\s*\+\s*%s)*)' % (feld, STRING, STRING), quelle):
            t = ketten(m.group(1))
            if t:
                gefunden.append(t)
    # 2b · rueck("art", "Titel", "Text") — die beiden hinteren Felder sind sichtbar
    for m in re.finditer(r'rueck\(\s*"[^"]*"\s*,\s*(%s)\s*,\s*(%s)?' % (STRING, STRING), quelle):
        for g in m.groups():
            if g:
                t = ketten(g)
                if t:
                    gefunden.append(t)

    # 3 · push/melde mit reinen Zeichenketten
    for ruf in ["offen.push", "hat.push", "melde"]:
        for m in re.finditer(r'%s\(\s*(%s(?:\s*\+\s*%s)*)\s*\)' % (re.escape(ruf), STRING, STRING), quelle):
            t = ketten(m.group(1))
            if t:
                gefunden.append(t)
    return gefunden


def sammle():
    alle = []
    for d in DATEIEN:
        p = os.path.join(WEB, d)
        if os.path.exists(p):
            alle += sammle_aus(open(p, encoding="utf-8").read())
    html = os.path.join(WEB, "index.html")
    if os.path.exists(html):
        h = open(html, encoding="utf-8").read()
        alle += re.findall(r'data-t[^>]*>([^<]+)<', h)
        alle += re.findall(r'title="([^"]+)"', h)
    # Ordnen, Doppelte weg, Unsinn aussortieren
    sauber, gesehen = [], set()
    for t in alle:
        t = t.strip()
        if not t or t in gesehen:
            continue
        if len(t) < 2 or re.fullmatch(r'[\W\d\s]+', t):
            continue
        gesehen.add(t)
        sauber.append(t)
    return sauber


def lies(sprache):
    p = os.path.join(TEXT, sprache + ".json")
    if not os.path.exists(p):
        return {}
    return json.load(open(p, encoding="utf-8"))


def schreibe(sprache, tisch):
    os.makedirs(TEXT, exist_ok=True)
    p = os.path.join(TEXT, sprache + ".json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(tisch, f, ensure_ascii=False, indent=1, sort_keys=True)
    return p


if __name__ == "__main__":
    saetze = sammle()
    print(len(saetze), "deutsche Sätze im Spiel")
    neu = "--neu" in sys.argv
    fehler = 0
    for sprache in ("en", "ru"):
        tisch = lies(sprache)
        fehlt = [t for t in saetze if not tisch.get(t)]
        ueberzaehlig = [t for t in tisch if t not in saetze]
        print(f"\n{sprache}: {len(tisch)} Einträge · {len(fehlt)} fehlen · {len(ueberzaehlig)} verwaist")
        for t in fehlt[:200]:
            print("   FEHLT:", t[:110])
        for t in ueberzaehlig[:20]:
            print("   VERWAIST:", t[:110])
        if neu:
            for t in fehlt:
                tisch.setdefault(t, "")
            print("   geschrieben:", schreibe(sprache, tisch))
        fehler += len(fehlt)
    sys.exit(1 if (fehler and not neu) else 0)
