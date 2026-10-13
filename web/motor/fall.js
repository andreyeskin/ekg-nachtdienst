/* Motor: Fälle laden und spielen (KONZEPT §6).

   Ein Fall ist ein reines Datenobjekt (web/faelle/<id>.js). Dieser Motor kennt keinen Patienten:
   er liest Dialogbäume, Klickfelder, Aufgaben, Karten und den Stand aus den Daten, wertet
   Bedingungen aus und führt Wirkungen aus. Alle Texte sind IDs (text/de/<fall>.json), gefüllt
   mit Platzhaltern aus den Werten des Falls und den Messungen der Spielerin — nie aus Literalen.

   Bedingungen (String, Array = alle müssen gelten, „a | b" = eine von beiden, „!" verneint):
     hat:MARKE          Marke des Falls gesetzt           karte:ID       Karte in der Mappe
     pflicht            alle Pflichtfragen gestellt       wert:NAME      Z.werte[NAME] vorhanden
     mind:N:a,b,c       mindestens N dieser Karten        raum:NAME      Spielerin steht in NAME
   Wirkungen (String oder Array, Platzhalter {…} werden vorher gefüllt):
     setze:M · loesche:M · karte:KEY · zeit:+N · melde:TEXTID[:warnung] · felder
     aufgabe:KEY · dialog:BAUM.KNOTEN (nach dem laufenden Dialog) · szenenbild:KEY[>BAUM.KNOTEN]
     szenenbild:weg
   Zustand je Fall: Z.faelle[id].marken. Messwerte (hf, pq, rr, qrs) liegen in Z.werte, weil die
   Befundmappe sie über Kapitel hinweg braucht.                                                 */
(function (global) {
  "use strict";

  var api = null, faelle = {}, baeume = {}, nach = [];

  /* ---------------------------------------------------------------- Zustand */
  function zustand(f) {
    var Z = api.Z;
    if (!Z.faelle) Z.faelle = {};
    if (!Z.faelle[f.id]) Z.faelle[f.id] = { marken: {} };
    if (!Z.faelle[f.id].marken) Z.faelle[f.id].marken = {};
    return Z.faelle[f.id];
  }
  function hat(f, m) { return !!zustand(f).marken[m]; }
  function setze(f, m) { zustand(f).marken[m] = true; api.sichere(); }
  function loesche(f, m) { delete zustand(f).marken[m]; api.sichere(); }

  function fehlendePflicht(f) {
    return (f.pflicht || []).filter(function (p) { return !hat(f, p.marke); });
  }
  function kernzahl(f) {
    var n = 0;
    (f.kern || []).forEach(function (id) { if (global.Mappe.hat(id)) n++; });
    return n;
  }

  /* Platzhalter für Texte und Wirkungen: feste Werte des Falls, Messungen, Uhrzeit, Pflichtstand. */
  function vars(f) {
    var v = {}, k;
    for (k in (f.werte || {})) if (f.werte.hasOwnProperty(k)) v[k] = f.werte[k];
    for (k in api.Z.werte) if (api.Z.werte.hasOwnProperty(k) && typeof api.Z.werte[k] !== "object") v[k] = api.Z.werte[k];
    var s = api.satz(f.aufnahme.haupt);
    if (s && s.mess) for (k in s.mess) if (s.mess.hasOwnProperty(k)) v["mess_" + k] = s.mess[k];
    v.zeit = api.zeitText();
    v.minuten = api.Z.zeit;
    var fehlt = fehlendePflicht(f);
    v.n_fehlt = fehlt.length;
    v.fehlt = fehlt.map(function (p) { return T(p.name); }).join(", ");
    v.n_kern = kernzahl(f);
    return v;
  }
  function fuelle(text, v) {
    return String(text).replace(/\{(\w+)\}/g, function (ganz, name) {
      return v.hasOwnProperty(name) ? String(v[name]) : ganz;
    });
  }

  /* ---------------------------------------------------------------- Bedingungen */
  var ZAHL = /^(\w+)\s*(<=|>=|<|>|=)\s*(-?\d+(?:\.\d+)?)$/;
  function einzeln(f, c, extra) {
    c = c.trim();
    if (!c) return true;
    if (c.charAt(0) === "!") return !einzeln(f, c.slice(1), extra);
    var m = ZAHL.exec(c);
    if (m) {                                   /* hf<50, pq>200, minuten<420 — gegen Werte, nie gegen Literale im Text */
      var v = vars(f), k;
      if (extra) for (k in extra) if (extra.hasOwnProperty(k)) v[k] = extra[k];
      var a = +v[m[1]], b = +m[3];
      if (isNaN(a)) return false;
      return m[2] === "<" ? a < b : m[2] === ">" ? a > b : m[2] === "<=" ? a <= b : m[2] === ">=" ? a >= b : a === b;
    }
    if (c.indexOf("{") >= 0) c = fuelle(c, vars(f));
    var t = c.split(":"), art = t[0], rest = t.slice(1).join(":");
    switch (art) {
      case "hat": return hat(f, rest);
      case "karte": return global.Mappe.hat(rest);
      case "pflicht": return fehlendePflicht(f).length === 0;
      case "wert": return api.Z.werte[rest] !== undefined && api.Z.werte[rest] !== null;
      case "raum": return global.Szene.aktueller() === rest;
      case "mind": {
        var n = +t[1], ids = (t[2] || "").split(","), z = 0;
        ids.forEach(function (id) { if (global.Mappe.hat(id.trim())) z++; });
        return z >= n;
      }
      default: throw new Error("Unbekannte Bedingung: " + c);
    }
  }
  function pruefe(f, cond, extra) {
    if (cond === undefined || cond === null) return true;
    if (Array.isArray(cond)) return cond.every(function (c) { return pruefe(f, c, extra); });
    if (typeof cond === "function") return !!cond();
    var teile = String(cond).split("|");
    if (teile.length > 1) return teile.some(function (c) { return einzeln(f, c, extra); });
    return einzeln(f, cond, extra);
  }
  /* Erste passende Regel einer Liste [{wenn, …}] */
  function erste(f, regeln, extra) {
    for (var i = 0; i < (regeln || []).length; i++) if (pruefe(f, regeln[i].wenn, extra)) return regeln[i];
    return null;
  }

  /* ---------------------------------------------------------------- Texte */
  function tx(f, spec, extra) {
    if (spec === undefined || spec === null) return "";
    var v = vars(f);
    if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) v[k] = extra[k];
    if (Array.isArray(spec)) {
      var r = erste(f, spec);
      return r ? T(r.text, v) : "";
    }
    return T(spec, v);
  }

  /* ---------------------------------------------------------------- Wirkungen */
  function wirke(f, wirkungen, extra) {
    if (!wirkungen) return;
    if (!Array.isArray(wirkungen)) wirkungen = [wirkungen];
    var v = vars(f);
    if (extra) for (var k in extra) if (extra.hasOwnProperty(k)) v[k] = extra[k];
    wirkungen.forEach(function (w) {
      if (typeof w === "function") { w(); return; }
      if (typeof w === "object") {             /* { wenn, tu }: bedingte Wirkung */
        if (pruefe(f, w.wenn)) wirke(f, w.tu, extra);
        return;
      }
      w = fuelle(w, v);
      var t = w.split(":"), art = t[0], rest = t.slice(1).join(":");
      switch (art) {
        case "setze": setze(f, rest); break;
        case "loesche": loesche(f, rest); break;
        case "karte": api.befund(karte(f, rest)); break;
        case "zeit": api.zeitVor(parseInt(rest, 10) || 0); break;
        case "melde": api.melde(T(t[1], v), t[2]); break;
        case "felder": if (rest === "zeigen") global.Szene.zeigeFelder(2400); else global.Szene.aktualisiere(); break;
        case "aufgabe": global.setTimeout(function () { aufgabe(f, rest); }, 60); break;
        case "dialog": dialogSpaeter(f, rest); break;
        case "szenenbild": szenenbild(f, rest); break;
        default: throw new Error("Unbekannte Wirkung: " + w);
      }
    });
    regeln(f);
    klassen(f);
    global.Szene.aktualisiere();
    api.kopf();
    api.sichere();
  }
  /* Bühnenklassen des Raums (z. B. „Herr Baum ist oben") — nach jeder Wirkung, nicht nur beim Betreten. */
  function klassen(f) {
    var r = f.raum;
    if (!r || !r.klassen || global.Szene.aktueller() !== r.id) return;
    var b = document.getElementById("buehne");
    Object.keys(r.klassen).forEach(function (kl) { b.classList.toggle(kl, pruefe(f, r.klassen[kl])); });
  }
  /* Regeln des Falls: laufen nach jeder Wirkung, z. B. „Anamnese-Karte, sobald alle Pflichtfragen gestellt sind". */
  var inRegeln = false;
  function regeln(f) {
    if (inRegeln) return;
    inRegeln = true;
    try {
      (f.regeln || []).forEach(function (r) { if (pruefe(f, r.wenn)) wirke(f, r.tu); });
    } finally { inRegeln = false; }
  }

  /* ---------------------------------------------------------------- Dialoge */
  function baumName(f, name) { return f.kuerzel + "." + name; }
  function zerlege(f, ziel) {          /* „marlene.start" → {baum, knoten} */
    var i = ziel.indexOf(".");
    return { baum: baumName(f, ziel.slice(0, i)), knoten: ziel.slice(i + 1) };
  }
  function dialogStart(f, ziel) {
    var z = zerlege(f, ziel);
    global.Dialog.starte(z.baum, z.knoten, function () { laufeNach(f); });
  }
  /* Ein Dialog nach dem laufenden: in die Warteschlange, die beim Schließen abgearbeitet wird. */
  function dialogSpaeter(f, ziel) {
    if (global.Dialog.laeuft()) nach.push(function () { dialogStart(f, ziel); });
    else global.setTimeout(function () { dialogStart(f, ziel); }, 60);
  }
  function laufeNach(f) {
    var liste = nach; nach = [];
    liste.forEach(function (fn) { fn(); });
    global.Szene.aktualisiere();
  }
  function szenenbild(f, rest) {
    if (rest === "weg") { global.Szenenbild.verberge(); return; }
    var t = rest.split(">"), name = t[0], ziel = t[1];
    global.Szenenbild.zeige(name, ziel ? function () { dialogStart(f, ziel); } : null);
  }

  function knotenBauen(f, figur, k) {
    var n = { wer: k.wer || figur };
    if (k.umleiten) n.umleiten = function () { var r = erste(f, k.umleiten); return r ? r.zu : null; };
    n.text = function () { return tx(f, k.text); };
    n.tu = function () {
      if (k.tu) wirke(f, k.tu);
      if (k.nach) { var w = k.nach; nach.push(function () { wirke(f, w); }); }
    };
    if (k.antworten) {
      n.antworten = k.antworten.map(function (a) {
        var b = { zu: a.zu === undefined ? null : a.zu };
        b.text = function () { return tx(f, a.text); };
        if (a.wenn !== undefined) b.wenn = function () { return pruefe(f, a.wenn); };
        if (a.baum) b.baum = baumName(f, a.baum);
        b.tu = function () {
          if (a.tu) wirke(f, a.tu);
          if (a.nach) { var w = a.nach; nach.push(function () { wirke(f, w); }); }
        };
        return b;
      });
    } else if (k.weiter) {
      n.weiter = k.weiter;
      if (k.weiterBaum) n.weiterBaum = baumName(f, k.weiterBaum);
    } else {
      n.endeText = k.ende || "Danke.";
    }
    return n;
  }
  function dialogeBauen(f) {
    Object.keys(f.dialoge || {}).forEach(function (name) {
      var d = f.dialoge[name], figur = d.figur || name, baum = {};
      Object.keys(d.knoten).forEach(function (id) { baum[id] = knotenBauen(f, figur, d.knoten[id]); });
      baeume[baumName(f, name)] = baum;
    });
  }

  /* ---------------------------------------------------------------- Karten */
  var SYMBOLE = {
    tabletten: '<svg viewBox="0 0 220 80" style="width:100%;height:auto">' +
      '<rect x="8" y="14" width="56" height="52" rx="4" fill="#F4E6D2" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="16" y="24" width="40" height="5" fill="#C2185B"/>' +
      '<rect x="16" y="36" width="30" height="4" fill="#10212B" opacity=".45"/>' +
      '<rect x="78" y="20" width="52" height="46" rx="4" fill="#F4E6D2" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="86" y="30" width="36" height="4" fill="#10212B" opacity=".45"/>' +
      '<rect x="144" y="26" width="48" height="40" rx="4" fill="#F4E6D2" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="152" y="36" width="32" height="4" fill="#10212B" opacity=".45"/></svg>',
    bogen: '<svg viewBox="0 0 220 80" style="width:100%;height:auto">' +
      '<rect x="66" y="6" width="88" height="68" fill="#FBF2E3" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="92" y="2" width="36" height="10" fill="#C99A5B" stroke="#10212B" stroke-width="2"/>' +
      '<rect x="76" y="24" width="68" height="4" fill="#10212B" opacity=".5"/>' +
      '<rect x="76" y="34" width="52" height="4" fill="#10212B" opacity=".35"/>' +
      '<rect x="76" y="44" width="60" height="4" fill="#10212B" opacity=".35"/>' +
      '<rect x="76" y="54" width="40" height="4" fill="#10212B" opacity=".35"/>' +
      '<rect x="76" y="62" width="24" height="5" fill="#C2185B"/></svg>',
    stethoskop: '<svg viewBox="0 0 220 80" style="width:100%;height:auto" fill="none" stroke="#10212B" stroke-width="3" stroke-linecap="round">' +
      '<path d="M78 8v26a32 32 0 0 0 64 0V8"/><path d="M110 66v4"/>' +
      '<path d="M110 66c0 0-2 6 8 6s12-10 24-10c10 0 14 6 14 6"/>' +
      '<circle cx="160" cy="66" r="9" fill="#C99A5B"/></svg>',
    notiz: '<svg viewBox="0 0 220 80" style="width:100%;height:auto">' +
      '<rect x="40" y="8" width="140" height="64" fill="#FBF2E3" stroke="#10212B" stroke-width="2"/>' +
      '<path d="M52 26h116M52 38h96M52 50h108M52 62h60" stroke="#10212B" stroke-width="3" opacity=".45" stroke-linecap="round"/>' +
      '<rect x="164" y="56" width="10" height="10" fill="#C2185B"/></svg>'
  };
  function karte(f, key) {
    var k = f.karten[key];
    if (!k) throw new Error("Karte fehlt: " + key);
    var v = vars(f), aus = { id: k.id, titel: k.titel, text: k.text, vars: v, zeit: api.zeitText() };
    /* Textvarianten (z. B. nach Messwert) werden beim Anlegen entschieden; gespeichert wird die ID. */
    if (Array.isArray(k.text)) { var r = erste(f, k.text); aus.text = r ? r.text : ""; }
    if (Array.isArray(k.titel)) { var rt = erste(f, k.titel); aus.titel = rt ? rt.text : ""; }
    if (k.ekg) {
      aus.ekg = {};
      for (var p in k.ekg) if (k.ekg.hasOwnProperty(p)) aus.ekg[p] = k.ekg[p];
      aus.ekg.satz = k.ekg.satz === "haupt" ? f.aufnahme.haupt : k.ekg.satz;
    }
    if (k.symbol) aus.symbol = SYMBOLE[k.symbol] || k.symbol;
    if (k.vergleich) aus.vergleich = k.vergleich;          /* IDs; die Mappe füllt sie mit vars */
    return aus;
  }

  /* ---------------------------------------------------------------- Aufgaben */
  /* Deutung eines Messwerts: Regeln wie { wenn: "hf<50", text } — mit ms (gemessen) und hf (60 000 : ms). */
  function deutung(f, d, ms) {
    if (!d) return "";
    var extra = { ms: ms };
    if (d.aus === "hf") extra.hf = Math.round(60000 / ms);
    var r = erste(f, d.regeln, extra);
    if (!r) return "";
    var v = vars(f);
    for (var k in extra) if (extra.hasOwnProperty(k)) v[k] = extra[k];
    return T(r.text, v);
  }
  function aufgabe(f, key) {
    var a = f.aufgaben[key];
    if (!a) throw new Error("Aufgabe fehlt: " + key);
    if (a.einmal && !hat(f, a.einmal)) { setze(f, a.einmal); wirke(f, a.vorher); }
    var s = api.satz(f.aufnahme.haupt), v = vars(f);
    if (a.art === "frage") {
      global.Fenster.frage({
        titel: a.titel, text: a.text, vars: v,
        ekg: a.ekg ? { satz: s, mmProS: a.ekg.mmProS, von: a.ekg.von, dauer: a.ekg.dauer } : null,
        antworten: a.antworten,
        fertig: function () { wirke(f, a.fertig); }
      });
    } else if (a.art === "wahl") {
      global.Fenster.waehle({
        titel: a.titel, text: Array.isArray(a.text) ? (erste(f, a.text) || {}).text : a.text, vars: v,
        hinweis: a.hinweis,
        wahl: a.wahl.map(function (w) {
          return { text: w.text, fertig: global.Mappe.hat(w.karte), tu: function () { aufgabe(f, w.aufgabe); } };
        })
      });
    } else if (a.art === "zirkel") {
      global.Zirkel.starte({
        satz: s, was: a.was, toleranz: a.toleranz, mmProS: a.mmProS, von: a.von, dauer: a.dauer,
        titel: T(a.titel, v), auftrag: T(a.auftrag, v),
        deutung: function (ms) { return deutung(f, a.deutung, ms); },
        fertig: function (erg) {
          api.Z.werte[a.was] = erg.wahrheit;
          if (a.was === "rr") api.Z.werte.hf = Math.round(60000 / erg.wahrheit);
          wirke(f, a.fertig);
        }
      });
    } else if (a.art === "befundzeilen") {
      global.Fenster.befundzeilen({
        titel: a.titel, text: a.text, zeilen: a.zeilen, vars: v, knopf: a.knopf,
        fertig: function () { wirke(f, a.fertig); }
      });
    } else throw new Error("Unbekannte Aufgabenart: " + a.art);
  }

  /* ---------------------------------------------------------------- Raum */
  function raumBauen(f) {
    var r = f.raum, kunst = api.kunst;
    var def = {
      titel: r.titel, ebenen: kunst.szenen[r.id], ersatzfarbe: r.ersatzfarbe,
      beiBetreten: function () { api.betreten(r.id); klassen(f); },
      felder: (r.felder || []).map(function (fd) {
        var feld = { id: fd.id, name: T(fd.name), punkte: api.zone(r.id, fd.zone || fd.id, fd.rueckfall) };
        if (fd.sichtbar !== undefined) feld.sichtbar = function () { return pruefe(f, fd.sichtbar); };
        if (fd.erledigt !== undefined) feld.erledigt = function () { return pruefe(f, fd.erledigt); };
        feld.bei = function () { var rg = erste(f, fd.bei); if (rg) wirke(f, rg.tu); };
        return feld;
      }),
      ausgaenge: (r.ausgaenge || []).map(function (ag) {
        return {
          name: T(ag.name), nach: ag.nach, punkte: api.zone(r.id, ag.zone || "ausgang", ag.rueckfall),
          wenn: function () { return pruefe(f, ag.wenn); },
          gesperrt: function () { var rg = erste(f, ag.gesperrt); if (rg) wirke(f, rg.tu); }
        };
      })
    };
    global.Szene.registriere(r.id, def);
  }

  /* ---------------------------------------------------------------- Stand der Schicht */
  function stand(id) {
    var f = faelle[id], aus = { hat: [], offen: [], fuss: "" };
    api.Z.befunde.forEach(function (b) { aus.hat.push(T(b.titel, b.vars) + " <em>" + b.zeit + "</em>"); });
    (f.stand.hat || []).forEach(function (z) { if (pruefe(f, z.wenn)) aus.hat.push(tx(f, z.text)); });
    (f.stand.offen || []).forEach(function (z) { if (pruefe(f, z.wenn)) aus.offen.push(tx(f, z.text)); });
    var fu = erste(f, f.stand.fuss || []);
    if (fu) aus.fuss = tx(f, fu.text);
    aus.titel = f.stand.titel;
    return aus;
  }

  /* ---------------------------------------------------------------- Schnittstelle */
  function start(schnittstelle) { api = schnittstelle; }
  function lade(f) {
    faelle[f.id] = f;
    dialogeBauen(f);
    raumBauen(f);
    return f;
  }
  function epilog(id, fertig) {
    var f = faelle[id], z = zerlege(f, f.epilog);
    global.Dialog.starte(z.baum, z.knoten, function () { laufeNach(f); if (fertig) fertig(); });
  }

  global.Fall = {
    start: start, lade: lade, baeume: function () { return baeume; },
    hat: function (id, m) { return hat(faelle[id], m); },
    setze: function (id, m) { setze(faelle[id], m); },
    pruefe: function (id, c) { return pruefe(faelle[id], c); },
    wirke: function (id, w) { wirke(faelle[id], w); },
    vars: function (id) { return vars(faelle[id]); },
    stand: stand, epilog: epilog,
    fehlendePflicht: function (id) { return fehlendePflicht(faelle[id]).map(function (p) { return p.marke; }); },
    __aufgabe: function (id, key) { aufgabe(faelle[id], key); },
    __faelle: faelle
  };
})(window);
