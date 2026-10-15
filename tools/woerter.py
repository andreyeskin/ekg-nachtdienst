# -*- coding: utf-8 -*-
"""Sammelt alle deutschen Sätze, die im Spiel sichtbar werden, und prüft die
Übersetzungen.

    python3 tools/woerter.py              — zeigt, was in en/ru fehlt
    python3 tools/woerter.py --neu        — schreibt fehlende Einträge als
                                            leere Felder in die Sprachdateien
    python3 tools/woerter.py --aufraeumen — entfernt verwaiste Sätze aus en/ru

Zwei Wege (KONZEPT §6.2):
  alt  — der deutsche Satz ist der Schlüssel (web/sprache.js, text/en.json, text/ru.json);
  neu  — feste IDs je Fall (text/de/<fall>.json als Quelle, text/en/…, text/ru/… mit denselben
         Schlüsseln). Geprüft wird: jede ID aus web/faelle/*.js hat einen deutschen Text, jede
         deutsche ID hat en und ru, keine ID ist verwaist.
Der Durchlauf (tools/durchlauf.mjs) bricht ab, wenn eine ID ohne Übersetzung bleibt.
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(WURZEL, "web")
TEXT = os.path.join(WURZEL, "text")
DATEIEN = ["spiel.js", "dialog.js", "mappe.js", "stand.js", "raetsel_zirkel.js", "raetsel_reizleitung.js", "raetsel_schirme.js",
           "raetsel_ampel.js", "szene.js", "huelle.js", "motor/fenster.js", "motor/fall.js", "motor/szenenbild.js"]
FAELLE = os.path.join(WEB, "faelle")
ID_MUSTER = re.compile(r'^[a-z][a-z0-9_]*\.[a-z0-9_.]+$')

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
    # Ordnen, Doppelte weg, Unsinn aussortieren; IDs (neuer Weg) gehören nicht in die Satzlisten
    sauber, gesehen = [], set()
    for t in alle:
        t = t.strip()
        if not t or t in gesehen:
            continue
        if len(t) < 2 or re.fullmatch(r'[\W\d\s]+', t) or ID_MUSTER.match(t):
            continue
        gesehen.add(t)
        sauber.append(t)
    return sauber


# ------------------------------------------------------------------ Texte über IDs
def lies_ids(sprache):
    """Alle Fall-Texte einer Sprache: {id: satz}, aus text/<sprache>/*.json."""
    ordner = os.path.join(TEXT, sprache)
    tisch = {}
    if os.path.isdir(ordner):
        for datei in sorted(os.listdir(ordner)):
            if datei.endswith(".json"):
                tisch.update(json.load(open(os.path.join(ordner, datei), encoding="utf-8")))
    return tisch


def ids_im_code():
    """Jede Zeichenkette in web/faelle/*.js, die wie eine Text-ID aussieht — auch hinter melde: und
    szenenbild:…>baum.…"""
    ids = set()
    if not os.path.isdir(FAELLE):
        return ids
    for datei in os.listdir(FAELLE):
        if not datei.endswith(".js"):
            continue
        quelle = open(os.path.join(FAELLE, datei), encoding="utf-8").read()
        quelle = re.sub(r'/\*.*?\*/', '', quelle, flags=re.S)        # Kommentare enthalten Anführungszeichen
        quelle = re.sub(r'^\s*//.*$', '', quelle, flags=re.M)
        m = re.search(r'\bkuerzel:\s*"([a-z0-9_]+)"', quelle)
        vorsatz = (m.group(1) + ".") if m else ""                     # nur Text-IDs dieses Falls, keine Dialogziele
        for s in re.findall(STRING, quelle):
            for teil in re.split(r'[:>]', s):
                if ID_MUSTER.match(teil) and teil.startswith(vorsatz):
                    ids.add(teil)
    return ids


def pruefe_ids():
    de = lies_ids("de")
    benutzt = ids_im_code()
    fehler = 0
    ohne_text = sorted(benutzt - set(de))
    verwaist = sorted(set(de) - benutzt)
    print(f"\nIDs: {len(de)} deutsche Texte · {len(benutzt)} im Code")
    for t in ohne_text:
        print("   OHNE TEXT (de):", t)
    for t in verwaist:
        print("   VERWAIST (ID):", t)
    fehler += len(ohne_text)
    for sprache in ("en", "ru"):
        tisch = lies_ids(sprache)
        fehlt = [k for k in de if not tisch.get(k)]
        extra = [k for k in tisch if k not in de]
        falsch = [k for k in de if tisch.get(k) and set(re.findall(r'\{\w+\}', de[k])) != set(re.findall(r'\{\w+\}', tisch[k]))]
        print(f"   {sprache}: {len(tisch)} Einträge · {len(fehlt)} fehlen · {len(extra)} ohne deutsches Gegenstück · {len(falsch)} mit anderen Platzhaltern")
        for k in fehlt[:50]:
            print("      FEHLT:", k)
        for k in falsch[:50]:
            print("      PLATZHALTER:", k)
        fehler += len(fehlt) + len(falsch)
    return fehler


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
    print(len(saetze), "deutsche Sätze im Spiel (alter Weg)")
    neu = "--neu" in sys.argv
    aufraeumen = "--aufraeumen" in sys.argv
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
        if aufraeumen and ueberzaehlig:
            for t in ueberzaehlig:
                del tisch[t]
            print("   entfernt:", len(ueberzaehlig), "→", schreibe(sprache, tisch))
        fehler += len(fehlt)
    fehler_ids = pruefe_ids()
    sys.exit(1 if ((fehler and not neu) or fehler_ids) else 0)
