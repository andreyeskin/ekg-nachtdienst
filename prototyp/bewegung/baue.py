# -*- coding: utf-8 -*-
"""Baut den Bewegungs-Prototyp der Aufnahme als eine Datei (docs/REDESIGN_FALL1.md §10).

    python3 prototyp/bewegung/baue.py            → bau/prototyp_bewegung_de.html und _ru.html

Bilder aus art/szenen/aufnahme/ (base64), die Kurve am EKG-Wagen aus data/ekg_daten.json (LUDB 39,
Ableitung II, echte Werte; ART_BIBLE §6). Der Prototyp ändert nichts am Spiel."""
import base64
import json
import os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HIER = os.path.join(WURZEL, "prototyp", "bewegung")
SZENE = os.path.join(WURZEL, "art", "szenen", "aufnahme")
BAU = os.path.join(WURZEL, "bau")

TEXTE = {
    "de": {
        "TITEL": "Prototyp: Leben in der Aufnahme, 06:40",
        "BILD": "Aufnahme am frühen Morgen: Marlene hinter dem Tresen, Herr Baum auf der Bank, EKG-Wagen, Fenster mit Sonnenaufgang",
        "UHRZEIT": "Uhrzeit",
        "ZEIT_LAEUFT": "Zeit läuft",
        "HANDY": "Handy der Tochter",
        "EKG": "EKG schreiben",
        "VORBEI": "Jemand geht vorbei",
        "UHRBLICK": "Blick zur Uhr",
        "RUHE": "Bewegung aus",
        "LEGENDE": (
            "<p><b>Uhr:</b> Sekundenzeiger in Echtzeit, Stunde und Minute nach der Spielzeit.</p>"
            "<p><b>Figuren:</b> atmen, blinzeln, wechseln den Blick. Marlene schreibt, schaut auf, schaut zu ihm. "
            "Herr Baum schaut zur Uhr, je später es wird, desto öfter.</p>"
            "<p><b>Licht:</b> Keil durchs Fenster mit Staub, Wolken dämpfen ihn; bis 07:50 wird er blasser.</p>"
            "<p><b>Draußen:</b> Vögel, ein Mann mit Hund. <b>Flur:</b> ab und zu geht jemand vorbei.</p>"
            "<p><b>Vordergrund:</b> eine Pflegerin geht unscharf durchs Bild.</p>"
            "<p><b>EKG-Wagen:</b> Bereitschaft (Bernstein), erst beim Schreiben läuft die echte Kurve "
            "(LUDB 39, Ableitung II), das Papier kommt heraus.</p>"),
        "HINWEIS": "Bei „Bewegung reduzieren“ im System bleiben nur Uhr und Zustände. Nichts davon trägt Spielinhalt.",
    },
    "ru": {
        "TITEL": "Прототип: живая Aufnahme, 06:40",
        "BILD": "Приёмное отделение рано утром: Марлене за стойкой, господин Баум на скамейке, тележка ЭКГ, окно с рассветом",
        "UHRZEIT": "Время",
        "ZEIT_LAEUFT": "Время идёт",
        "HANDY": "Звонит дочь",
        "EKG": "Записать ЭКГ",
        "VORBEI": "Кто-то проходит",
        "UHRBLICK": "Взгляд на часы",
        "RUHE": "Без движения",
        "LEGENDE": (
            "<p><b>Часы:</b> секундная стрелка идёт в реальном времени, часы и минуты по игровому.</p>"
            "<p><b>Персонажи:</b> дышат, моргают, переводят взгляд. Марлене печатает, поднимает глаза, "
            "смотрит на него. Баум поглядывает на часы, и чем позже, тем чаще: он хочет домой.</p>"
            "<p><b>Свет:</b> луч из окна с пылинками, облака его приглушают; к 07:50 солнце выше, луч бледнеет.</p>"
            "<p><b>За окном:</b> птицы, мужчина с собакой. <b>Коридор:</b> иногда кто-то проходит.</p>"
            "<p><b>Передний план:</b> медсестра проходит размытым силуэтом.</p>"
            "<p><b>Тележка ЭКГ:</b> в ожидании горит жёлтый огонёк; только при записи идёт настоящая кривая "
            "(LUDB 39, отведение II) и выходит бумага. Сейчас в игре экран показывает ЭКГ ещё до того, как "
            "электроды наклеены, это ошибка.</p>"),
        "HINWEIS": "Если в системе включено «Уменьшить движение», остаются только часы и состояния. Движение не несёт учебного содержания.",
    },
}


def daten_uri(pfad, typ="image/png"):
    with open(pfad, "rb") as f:
        return "data:" + typ + ";base64," + base64.b64encode(f.read()).decode("ascii")


def ekg_39():
    alle = json.load(open(os.path.join(WURZEL, "data", "ekg_daten.json"), encoding="utf-8"))
    e = next(x for x in alle if x["id"] == 39)
    return json.dumps({"werte": [round(v, 3) for v in e["sig"]["werte"]], "fs": e["sig"]["fs"],
                       "frequenz": e["mess"]["frequenz"]}, separators=(",", ":"))


def main():
    vorlage = open(os.path.join(HIER, "aufnahme.html"), encoding="utf-8").read()
    leben = open(os.path.join(HIER, "leben.js"), encoding="utf-8").read()
    ersatz = {
        "BILD_HINTERGRUND": daten_uri(os.path.join(SZENE, "hintergrund.png")),
        "BILD_MITTELGRUND": daten_uri(os.path.join(SZENE, "mittelgrund.png")),
        "BILD_TUETE": daten_uri(os.path.join(SZENE, "figuren", "tuete.png")),
        "BILD_MARLENE": daten_uri(os.path.join(SZENE, "figuren", "marlene.png")),
        "BILD_HERRK": daten_uri(os.path.join(SZENE, "figuren", "herrk.png")),
        "EKG_39": ekg_39(),
        "LEBEN_JS": leben,
    }
    os.makedirs(BAU, exist_ok=True)
    for sprache, texte in TEXTE.items():
        html = vorlage.replace("{{SPRACHE}}", sprache)
        for k, v in texte.items():
            html = html.replace("{{T_" + k + "}}", v)
        for k, v in ersatz.items():
            html = html.replace("{{" + k + "}}", v)
        assert "{{" not in html, "offener Platzhalter"
        ziel = os.path.join(BAU, "prototyp_bewegung_" + sprache + ".html")
        with open(ziel, "w", encoding="utf-8") as f:
            f.write(html)
        print(ziel, round(os.path.getsize(ziel) / 1024), "kB")


if __name__ == "__main__":
    main()
