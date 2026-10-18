/* Prototyp Fall 1 „Darf Herr Baum heim?" — der Motor (docs/REDESIGN_FALL1.md).

   Schlank, aber vollständig spielbar: Zustand und Uhr, Bühne mit Leben (prototyp/bewegung/leben.js),
   Dialoge mit Bedingungen und Wirkungen, Fenster (Befundzeilen, Frage am Streifen, Auswahl), Zirkel aus dem
   Spiel (web/raetsel_zirkel.js), Verdachtsliste, Befundmappe mit Vergleich, Stand der Schicht, Menü, Titel,
   Epilog als Erzähler-Seite und ein Endbildschirm. Aussehen und Bedienung wie im Spiel (web/stil.css).
   Die Geschichte steht in daten.js (window.FALL1); dieser Motor kennt keine Repliken.

   Für den automatischen Durchlauf (pruefe.mjs) gibt es window.__prototyp: Zustand lesen, Tippen abschalten,
   eine Zirkelmessung programmatisch setzen. Die echte Bedienung (Ziehen mit Finger, Maus, Pencil) bleibt. */
(function (global) {
  "use strict";

  var d = global.document;
  var A = global.ASSETS || {};
  var NS = "http://www.w3.org/2000/svg";
  var FALK_MIN = 7 * 60 + 15;

  /* ------------------------------------------------------------ Texte: Platzhalter einsetzen (nur Deutsch) */
  function zahl(n) {
    if (Math.round(n) === n) return String(n);
    try { return n.toLocaleString("de-AT"); } catch (e) { return String(n); }
  }
  function fuelle(text, werte) {
    return String(text).replace(/\{(\w+)\}/g, function (ganz, k) {
      if (!werte || !Object.prototype.hasOwnProperty.call(werte, k) || werte[k] === undefined || werte[k] === null) return ganz;
      var w = werte[k];
      return typeof w === "number" ? zahl(w) : String(w);
    });
  }
  global.T = function (text, werte) {
    if (text === null || text === undefined) return "";
    return fuelle(String(text), werte);
  };
  function wert(x) { return typeof x === "function" ? x() : x; }

  /* ------------------------------------------------------------ Bausteine */
  function el(tag, klasse, eltern, text) {
    var e = d.createElement(tag);
    if (klasse) e.className = klasse;
    if (text !== undefined && text !== null) e.textContent = text;
    if (eltern) eltern.appendChild(e);
    return e;
  }
  function knopf(klasse, text, eltern, beiKlick) {
    var b = el("button", klasse, eltern, text);
    b.type = "button";
    if (beiKlick) b.addEventListener("click", beiKlick);
    return b;
  }
  function sv(name, attr, eltern) {
    var e = d.createElementNS(NS, name);
    for (var k in attr) if (Object.prototype.hasOwnProperty.call(attr, k)) e.setAttribute(k, attr[k]);
    if (eltern) eltern.appendChild(e);
    return e;
  }
  function fokus(e) { if (e && e.focus) { try { e.focus({ preventScroll: true }); } catch (x) { e.focus(); } } }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var ruhig = !!(global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var schnell = false;              /* Prüfmodus: kein Tippen, kurze Pausen */
  var bewegung = true;

  /* ------------------------------------------------------------ Zustand */
  var Z = null;
  function neuerZustand() {
    return {
      zeit: 6 * 60 + 40, f: {}, karten: [], werte: {}, verdacht: {}, verlauf: [], geaendert: {},
      falkDa: false, laeuft: false, texte: [], x: {}
    };
  }

  function zeitText(min) {
    var m = min === undefined ? Z.zeit : min, h = Math.floor(m / 60), mm = m % 60;
    return (h < 10 ? "0" : "") + h + ":" + (mm < 10 ? "0" : "") + mm;
  }

  /* ------------------------------------------------------------ Schnittstelle für die Geschichte */
  var P = {
    hat: function (f) { return !!Z.f[f]; },
    setze: function (f) { Z.f[f] = true; },
    loesche: function (f) { delete Z.f[f]; },
    get Z() { return Z; },
    vor: function (n) { if (n) stelleZeit(Z.zeit + n); },
    zeitMin: function (m) { if (Z.zeit < m) stelleZeit(m); },
    zeitText: function () { return zeitText(); },
    FALK_MIN: FALK_MIN,
    vars: function (extra) {
      var v = {}, k, F = global.FALL1;
      for (k in F.werte) if (Object.prototype.hasOwnProperty.call(F.werte, k)) v[k] = F.werte[k];
      v.mess_pq = SATZ.mess.pq;
      for (k in Z.werte) if (Object.prototype.hasOwnProperty.call(Z.werte, k)) v[k] = Z.werte[k];
      if (v.pq === undefined) v.pq = SATZ.mess.pq;          /* Falk liest den Streifen auch ungemessen */
      if (v.hf === undefined) v.hf = SATZ.mess.frequenz;
      v.zeit = zeitText();
      if (F.vars) F.vars(v);
      if (extra) for (k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) v[k] = extra[k];
      return v;
    },
    gemessen: function (was) { return Z.werte[was] !== undefined; },
    karte: function (id) { return karteDazu(id); },
    hatKarte: function (id) { return hatKarte(id); },
    verdacht: function (id, zustand, grund) { verdacht(id, zustand, grund); },
    leben: function (e) { try { if (global.Leben) global.Leben.ereignis(e); } catch (x) { console.error(x); } },
    melde: function (text, art) { melde(text, art); },
    dialog: function (baum, id, fertig) { dlgStarte(baum, id, fertig); },
    befund: function (opt) { befundzeilen(opt); },
    frage: function (opt) { frage(opt); },
    wahl: function (opt) { wahl(opt); },
    zirkel: function (opt) { zirkel(opt); },
    stand: function () { oeffneStand(); },
    epilog: function (absaetze, fertig) { epilogSeite(absaetze, fertig); },
    ende: function () { endeSeite(); },
    figurAus: function (name) {
      var g = svg && svg.querySelector('[data-figur="' + name + '"]');
      if (g) g.style.display = "none";
      if (name === "herrk" && tuete) tuete.style.display = "none";
    },
    handyLicht: function () { handyLicht(); },
    szenenbild: function (an) { szenenbild(an); },
    zeigeFelder: function () { global.setTimeout(zeigeFelder, 60); },
    offen: function () { return offen(); },
    leerlauf: function () { planeLeerlauf(); }
  };
  global.P = P;

  /* ------------------------------------------------------------ EKG-Daten (LUDB 39, data/ekg_daten.json) */
  var SATZ = A.ekg39 || { sig: { werte: [], fs: 250, lead: "ii" }, schlaege: [], mess: { pq: 0, frequenz: 0 } };

  /* ------------------------------------------------------------ Bühne */
  var flaeche = null, buehne = null, svg = null, felder = null, feldname = null, tuete = null, licht = null;
  var FELDER = [
    { name: "marlene", wo: [22, 368, 578, 707], etikett: "Tresen · Marlene" },
    { name: "wagen", wo: [868, 433, 1014, 739], etikett: "EKG-Wagen" },
    { name: "tuete", wo: [1183, 615, 1275, 732], etikett: "Das Sackerl" },
    { name: "herrk", wo: [1276, 400, 1430, 736], etikett: "Koje 3 · Herr Baum" }
  ];
  /* Raumbeschreibung für leben.js, wie in prototyp/bewegung/aufnahme.html (Koordinaten 1600 × 900). */
  function lebenCfg() {
    return {
      uhr: { cx: 1399, cy: 231, r: 55 },
      fenster: { scheiben: [[694, 296, 184, 100], [914, 296, 202, 100]], boden: 395 },
      flur: { x: 1561, y: 255, b: 39, h: 438 },
      wagen: { schirm: [899, 436, 74, 49], led: [988, 497], papier: [922, 506, 27, 71], papierMax: 150,
               ekg: { werte: SATZ.sig.werte, fs: SATZ.sig.fs, frequenz: SATZ.mess.frequenz } },
      licht: { keil: [[694, 300], [1116, 300], [933, 800], [173, 752]] },
      /* Im Redesign liegt das Handy im Sackerl (§10.1): Zeichen links unten neben der Figur. */
      handy: { figur: "herrk", pose: "tasche", x: -40, y: 252 },
      uhrBlick: { figur: "herrk", pose: "uhr" },
      figuren: {
        marlene: {
          x: 312, y: 368, b: 99, h: 109, haut: "#F4C58E", atem: { periode: 4.6, hub: 1.1 },
          kopf: { loch: [[16, 0], [82, 0], [82, 48], [64, 58], [34, 58], [16, 48]],
                  kopf: [[13, -6], [85, -6], [85, 51], [67, 64], [31, 64], [13, 51]], dreh: [49, 60] },
          augen: [[36, 30, 4, 2.6], [50, 30, 4, 2.6]],
          ruhe: "auf",
          blicke: { schirm: { r: -2.5, y: 1.4, tippt: true }, auf: { r: 0, y: 0 }, baum: { r: 2.6, y: -0.2 } },
          plan: function (pose) {
            var z = function (a, b) { return a + Math.random() * (b - a); };
            if (pose === "schirm") return Math.random() < 0.7 ? ["auf", z(1.5, 3)] : ["baum", z(1.6, 2.6)];
            return ["schirm", z(4, 9)];
          }
        },
        herrk: {
          x: 1276, y: 400, b: 154, h: 336, haut: "#E9BA8E", atem: { periode: 7.2, hub: 1.6 },
          kopf: { loch: [[30, 0], [120, 0], [120, 58], [100, 72], [50, 72], [30, 58]],
                  kopf: [[27, -6], [123, -6], [123, 61], [103, 80], [47, 80], [27, 61]], dreh: [75, 76] },
          augen: [[61.5, 35, 4.6, 2.7], [86, 34.5, 4.6, 2.7]],
          ruhe: "vor",
          blicke: { vor: { r: 0, y: 0 }, uhr: { r: 4.5, y: -1.4 }, tresen: { r: -3.2, y: 0.2 },
                    boden: { r: -1.2, y: 2 }, tasche: { r: -2.4, y: 2.8, schnell: true } },
          plan: function (pose, zeit) {
            var z = function (a, b) { return a + Math.random() * (b - a); };
            var ungeduld = Math.max(0, Math.min(1, (zeit - 400) / 50));
            if (pose !== "vor") return ["vor", z(5, 10) * (1 - 0.45 * ungeduld)];
            var w = Math.random();
            if (w < 0.3 + 0.4 * ungeduld) return ["uhr", z(1.4, 2.2)];
            if (w < 0.75) return ["tresen", z(1.8, 2.8)];
            return ["boden", z(2.5, 4)];
          }
        }
      }
    };
  }

  function baueBuehne() {
    flaeche = el("main", "flaeche", d.body);
    flaeche.id = "flaeche";
    buehne = el("div", "buehne", flaeche);
    buehne.id = "buehne";
    svg = sv("svg", { viewBox: "0 0 1600 900", preserveAspectRatio: "xMidYMid slice", id: "szene", role: "img",
                      "aria-label": "Aufnahme am frühen Morgen: Marlene hinter dem Tresen, Herr Baum in der Koje, EKG-Wagen, Fenster mit Sonnenaufgang" }, buehne);
    sv("defs", {}, svg);
    var hg = sv("g", { "data-ebene": "hintergrund" }, svg);
    sv("image", { href: A.hintergrund, x: 0, y: 0, width: 1600, height: 900 }, hg);
    var mg = sv("g", { "data-ebene": "mittelgrund" }, svg);
    sv("image", { href: A.mittelgrund, x: 0, y: 0, width: 1600, height: 900 }, mg);
    var fg = sv("g", { "data-ebene": "figuren" }, svg);
    tuete = sv("image", { href: A.tuete, x: 1189, y: 615, width: 76, height: 112 }, fg);
    licht = sv("circle", { cx: 1226, cy: 652, r: 24, fill: "#39E58C", "class": "handy-licht" }, fg);
    sv("g", { "data-ebene": "licht" }, svg);
    sv("g", { "data-ebene": "vordergrund" }, svg);
    sv("g", { "data-ebene": "stimmung" }, svg);
    felder = sv("g", { "class": "felder" }, svg);
    FELDER.forEach(function (f) {
      var r = sv("rect", { x: f.wo[0], y: f.wo[1], width: f.wo[2] - f.wo[0], height: f.wo[3] - f.wo[1],
                           "class": "feld", "data-feld": f.name, tabindex: "0", role: "button", "aria-label": f.etikett }, felder);
      r.addEventListener("click", function () { feldKlick(f.name); });
      r.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); feldKlick(f.name); } });
      r.addEventListener("pointerenter", function () { zeigeFeldname(f.etikett); });
      r.addEventListener("pointerleave", function () { zeigeFeldname(null); });
      r.addEventListener("focus", function () { zeigeFeldname(f.etikett); });
      r.addEventListener("blur", function () { zeigeFeldname(null); });
    });
    feldname = el("div", "feldname", flaeche);
    try {
      if (global.Leben) global.Leben.starte(svg, lebenCfg(), { marlene: A.marleneFig, herrk: A.herrkFig });
    } catch (e) { console.error(e); }
  }
  function zeigeFeldname(t) {
    if (!feldname) return;
    if (t) feldname.textContent = t;
    feldname.classList.toggle("an", !!t);
  }
  function feldKlick(name) {
    if (!Z || !Z.laeuft || offen()) return;
    zeigeFeldname(null);
    global.FALL1.feld(name === "tuete" ? "herrk" : name);
  }
  /* Szenenbild am Tresen (wie web/motor/szenenbild.js): ruhige Einblendung über der Bühne, Dialog darüber. */
  var szb = null;
  function szenenbild(an) {
    if (!A.tresen) return;
    if (!szb) {
      szb = el("div", "szenenbild", d.body);
      szb.setAttribute("aria-hidden", "true");
      var img = el("img", null, szb); img.src = A.tresen; img.alt = ""; img.draggable = false;
    }
    if (an) {
      szb.classList.add("da");
      global.requestAnimationFrame(function () { global.requestAnimationFrame(function () { szb.classList.add("an"); }); });
    } else {
      szb.classList.remove("an");
      global.setTimeout(function () { if (!szb.classList.contains("an")) szb.classList.remove("da"); }, schnell ? 0 : 700);
    }
  }
  function handyLicht() {
    if (!licht) return;
    licht.classList.add("an");
    global.setTimeout(function () { licht.classList.remove("an"); }, 3600);
  }

  /* Ein Spielfenster offen? Dann bleibt die Bühne stumm, und die Uhr wartet mit Falk. */
  function offen() {
    return !!d.querySelector(".dialog.an, .raetsel.an, .mappe.an, .huelle-hof.an, .seite.an, .titel:not(.weg)");
  }
  function sperre() {
    if (buehne) buehne.classList.toggle("stumm", offen());
  }
  /* Zirkel (web/raetsel_zirkel.js) ruft Szene.sperre/aktualisiere — hier nur Sperre und Leerlauf. */
  global.Szene = { sperre: function () { global.setTimeout(sperre, 0); }, aktualisiere: function () { planeLeerlauf(); } };

  var leerlaufPlan = null;
  function planeLeerlauf() {
    sperre();
    global.clearTimeout(leerlaufPlan);
    leerlaufPlan = global.setTimeout(function () {
      sperre();
      if (!Z || !Z.laeuft || offen()) return;
      try { global.FALL1.leerlauf(); } catch (e) { console.error(e); }
      auffrischen();
    }, schnell ? 20 : 120);
  }

  /* ------------------------------------------------------------ Uhr */
  function stelleZeit(m) {
    var vorher = Z.zeit;
    Z.zeit = m;
    try { if (global.Leben) global.Leben.zeit(m); } catch (e) {}
    if (global.FALL1.zeitGeht) global.FALL1.zeitGeht(vorher, m);
    auffrischen();
  }

  /* ------------------------------------------------------------ HUD */
  var hud = null, H = {};
  var SYMBOLE = {
    hinweis: '<path d="M9.5 18.5h5M10.5 21.5h3"/><path d="M12 2.8a6.2 6.2 0 0 0-3.7 11.2c.8.6 1.2 1.4 1.2 2.4v.1h5v-.1c0-1 .4-1.8 1.2-2.4A6.2 6.2 0 0 0 12 2.8z"/>',
    stand: '<path d="M5.5 4.5h13v17h-13z"/><path d="M9 2.5h6v4H9z"/><path d="M8.5 11.5l1.5 1.5 2.6-2.6M14.5 12h2M8.5 17l1.5 1.5 2.6-2.6M14.5 17.5h2"/>',
    mappe: '<path d="M2.5 5.5h7l2 2.5h10v12h-19z"/><path d="M6.5 12.5h11M6.5 16h7"/>',
    verdacht: '<circle cx="10" cy="10" r="6.5"/><path d="M14.8 14.8l6 6"/><path d="M7.5 10h5"/>',
    menue: '<path d="M4 6.5h16M4 12h16M4 17.5h16"/>'
  };
  var HOERER = '<svg class="hoerer" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.2l3.1 3.6-1.9 2.3a11.5 11.5 0 0 0 7.1 7.1l2.3-1.9 3.6 3.1-1.5 3c-.5 1-1.6 1.4-2.6 1.1A17.6 17.6 0 0 1 2.5 7.2c-.3-1 .1-2.1 1.1-2.6z"/></svg>';
  function symbol(n) { return '<svg class="symbol" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + SYMBOLE[n] + "</svg>"; }
  function hudKnopf(id, name, text, eltern, beiKlick) {
    var b = knopf("hud-knopf", null, eltern, beiKlick);
    b.id = id; b.innerHTML = symbol(name);
    if (text) { el("span", "hud-text", b, text); b.setAttribute("aria-label", text); b.title = text; }
    return b;
  }
  function baueHud() {
    hud = el("div", "hud", flaeche);
    hud.id = "hud";
    var links = el("div", "hud-gruppe", hud), uhr = el("div", "hud-uhr", links);
    H.zeit = el("span", "hud-zeit", uhr, "Dienst 1 · 06:40");
    H.zeit.id = "hud-zeit";
    var rechts = el("div", "hud-gruppe", hud);
    H.hinweis = hudKnopf("hud-hinweis", "hinweis", "Was geht hier?", rechts, zeigeFelder);
    H.stand = hudKnopf("hud-stand", "stand", "Stand", rechts, function () { if (!offen()) oeffneStand(); });
    H.verdacht = hudKnopf("hud-verdacht", "verdacht", "Verdacht", rechts, function () { if (!offen()) oeffneVerdacht(); });
    H.vzahl = el("span", "hud-zahl", H.verdacht, "0");
    H.mappe = hudKnopf("hud-mappe", "mappe", "Befundmappe", rechts, function () { if (!offen()) oeffneMappe(); });
    H.mzahl = el("span", "hud-zahl", H.mappe, "0");
    H.menue = hudKnopf("hud-menue", "menue", null, rechts, oeffneMenue);
    H.menue.title = "Menü (Esc)"; H.menue.setAttribute("aria-label", "Menü");
  }
  function zeigeFelder() {
    if (!felder || offen()) return;
    felder.classList.add("zeigen");
    global.setTimeout(function () { felder.classList.remove("zeigen"); }, 2400);
  }
  function auffrischen() {
    if (!hud || !Z) return;
    H.zeit.textContent = "Dienst 1 · " + zeitText();
    var n = Object.keys(Z.geaendert).length;
    H.vzahl.textContent = String(n);
    H.verdacht.classList.toggle("voll", n > 0);
    H.mzahl.textContent = String(Z.karten.length);
    H.mappe.classList.toggle("voll", Z.karten.length > 0);
  }

  /* ------------------------------------------------------------ Meldungen */
  var meldFeld = null, vdFeld = null;
  function melde(text, art) {
    if (!meldFeld) { meldFeld = el("div", "meldungen", d.body); meldFeld.setAttribute("aria-live", "polite"); }
    var m = el("div", "meldung" + (art ? " " + art : ""), meldFeld, text);
    Z.texte.push({ art: "meldung", text: text });
    global.setTimeout(function () { m.classList.add("weg"); }, schnell ? 600 : 4200);
    global.setTimeout(function () { if (m.parentNode) m.parentNode.removeChild(m); }, schnell ? 900 : 4900);
  }
  /* Verdachtsliste: stille Meldung unten links (§4.1). Liegt ein Dialog offen, steht sie über seinem Kasten. */
  function meldeVerdacht(text) {
    if (!vdFeld) { vdFeld = el("div", "vd-meldungen", d.body); vdFeld.setAttribute("aria-live", "polite"); }
    var m = el("div", "vd-meldung", vdFeld, text);
    vdLage();
    global.requestAnimationFrame(vdLage);
    global.setTimeout(function () { m.classList.add("weg"); }, schnell ? 600 : 5200);
    global.setTimeout(function () { if (m.parentNode) m.parentNode.removeChild(m); }, schnell ? 900 : 5900);
  }

  function vdLage() {
    if (!vdFeld) return;
    var kasten = d.querySelector(".dialog.an .dialog-innen"), unten = 16;
    if (kasten) unten = Math.max(16, global.innerHeight - kasten.getBoundingClientRect().top + 10);
    vdFeld.style.bottom = unten + "px";
  }

  /* ------------------------------------------------------------ Verdachtsliste (§4) */
  var ZUSTAND = {
    offen: "offen", dafuer: "spricht dafür", dagegen: "spricht dagegen", unwahrscheinlich: "unwahrscheinlich",
    beides: "nicht bewiesen, nicht ausgeschlossen", bewiesen: "bewiesen"
  };
  function eintrag(id) {
    if (!Z.verdacht[id]) Z.verdacht[id] = { zustand: "offen", gruende: [] };
    return Z.verdacht[id];
  }
  function verdacht(id, zustand, grund) {
    var def = null;
    global.FALL1.verdacht.forEach(function (e) { if (e.id === id) def = e; });
    if (!def) throw new Error("Verdacht unbekannt: " + id);
    var e = eintrag(id), alt = e.zustand;
    var g = grund ? T(grund, P.vars()) : null;
    /* Ein schwächerer Befund holt einen gestrichenen Eintrag nicht zurück: er sammelt nur den Grund. */
    if (zustand && !(zustand === "dagegen" && alt === "unwahrscheinlich")) e.zustand = zustand;
    var neuerGrund = g && e.gruende.indexOf(g) < 0;
    if (neuerGrund) e.gruende.push(g);
    if (e.zustand === alt && !neuerGrund) return;
    Z.geaendert[id] = true;
    Z.verlauf.push({ zeit: zeitText(), id: id, zustand: e.zustand, grund: g });
    var satz = def.kurz + ": " + ZUSTAND[e.zustand] + "." +
      (g ? " " + g.charAt(0).toUpperCase() + g.slice(1) + (/[.!?]$/.test(g) ? "" : ".") : "");
    meldeVerdacht(satz);
    Z.texte.push({ art: "verdacht", text: satz });
    auffrischen();
  }

  var vdHof = null;
  function oeffneVerdacht() {
    if (!vdHof) {
      vdHof = el("div", "raetsel verdacht-hof", d.body);
      vdHof.id = "verdacht-hof";
      vdHof.innerHTML = '<div class="raetsel-innen schmal"><div class="raetsel-kopf"><h2>Verdacht</h2>' +
        '<button class="knopf zu" type="button">Zurück</button></div>' +
        '<p class="raetsel-auftrag">Woran es liegen kann. Jeder Befund streicht oder verstärkt einen Eintrag.</p>' +
        '<ol class="vd-liste"></ol><h3 class="stand-ueber">Verlauf</h3><ul class="vd-verlauf"></ul></div>';
      vdHof.querySelector(".zu").addEventListener("click", schliesseVerdacht);
    }
    vdHof.querySelector(".vd-liste").innerHTML = global.FALL1.verdacht.map(function (def) {
      var e = eintrag(def.id), gr = e.gruende.slice(-2);
      return '<li class="vd-eintrag z-' + e.zustand + (Z.geaendert[def.id] ? " neu" : "") + '" data-verdacht="' + def.id + '">' +
        '<div class="vd-kopf"><span class="vd-name">' + esc(def.name) + '</span>' +
        '<span class="vd-zustand">' + zeichen(e.zustand) + esc(ZUSTAND[e.zustand]) + '</span></div>' +
        (gr.length ? '<ul class="vd-gruende">' + gr.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ul>" : "") +
        "</li>";
    }).join("");
    var verlauf = Z.verlauf.slice().reverse();
    vdHof.querySelector(".vd-verlauf").innerHTML = verlauf.length ? verlauf.map(function (v) {
      var def = null; global.FALL1.verdacht.forEach(function (e) { if (e.id === v.id) def = e; });
      return '<li><em>' + v.zeit + '</em> ' + esc(def.kurz) + ": " + esc(ZUSTAND[v.zustand]) + (v.grund ? ". " + esc(v.grund) : "") + "</li>";
    }).join("") : '<li class="leer">Noch nichts. Zu Beginn sind alle acht offen.</li>';
    Z.geaendert = {};
    vdHof.classList.add("an");
    auffrischen(); sperre();
    fokus(vdHof.querySelector(".zu"));
  }
  function zeichen(z) {
    return { offen: "○ ", dafuer: "↑ + ", dagegen: "↓ − ", unwahrscheinlich: "✕ ", beides: "◐ ", bewiesen: "● " }[z] || "";
  }
  function schliesseVerdacht() { if (vdHof) vdHof.classList.remove("an"); planeLeerlauf(); }

  /* ------------------------------------------------------------ Befundmappe */
  function hatKarte(id) { for (var i = 0; i < Z.karten.length; i++) if (Z.karten[i].id === id) return true; return false; }
  function karteDazu(id) {
    var def = global.FALL1.karten[id];
    if (!def) throw new Error("Karte unbekannt: " + id);
    if (hatKarte(id)) return false;
    Z.karten.push({ id: id, zeit: zeitText() });
    melde("Befund in der Mappe: " + T(wert(def.titel), P.vars()));
    auffrischen();
    return true;
  }
  var mHof = null, gewaehlt = [];
  function oeffneMappe() {
    if (!mHof) {
      mHof = el("div", "mappe", d.body);
      mHof.id = "mappe";
      mHof.innerHTML = '<div class="mappe-innen"><div class="mappe-kopf"><h2>Befundmappe</h2>' +
        '<div class="mappe-hilfe">Zwei Karten antippen und vergleichen.</div>' +
        '<button class="knopf zu" type="button">Schließen</button></div>' +
        '<div class="mappe-karten"></div><div class="mappe-fuss"><button class="knopf vergleich" type="button" disabled>Vergleichen</button></div>' +
        '<div class="mappe-vergleich"></div></div>';
      mHof.querySelector(".zu").addEventListener("click", schliesseMappe);
      mHof.querySelector(".vergleich").addEventListener("click", vergleiche);
    }
    gewaehlt = [];
    mHof.querySelector(".vergleich").disabled = true;
    mHof.querySelector(".mappe-vergleich").classList.remove("an");
    maleKarten();
    mHof.classList.add("an");
    sperre();
    fokus(mHof.querySelector(".zu"));
  }
  function schliesseMappe() { if (mHof) mHof.classList.remove("an"); planeLeerlauf(); }
  function karteText(k) {
    var def = global.FALL1.karten[k.id], v = P.vars();
    return { titel: T(wert(def.titel), v), text: T(wert(def.text), v), ekg: def.ekg };
  }
  function maleKarten() {
    var feld = mHof.querySelector(".mappe-karten");
    if (!Z.karten.length) { feld.innerHTML = '<p class="leer">Noch nichts gesammelt.</p>'; return; }
    feld.innerHTML = Z.karten.map(function (k, i) {
      var t = karteText(k);
      return '<article class="karte" data-i="' + i + '" data-karte="' + k.id + '" tabindex="0">' +
        '<div class="karte-kopf"><span class="karte-zeit">' + k.zeit + '</span><h3>' + esc(t.titel) + '</h3></div>' +
        (t.ekg ? '<canvas class="karte-ekg" height="110"></canvas>' : "") +
        '<p>' + esc(t.text).replace(/\n/g, "<br>") + '</p></article>';
    }).join("");
    Array.prototype.forEach.call(feld.getElementsByClassName("karte"), function (kel) {
      var i = +kel.dataset.i, t = karteText(Z.karten[i]);
      if (t.ekg) maleEkg(kel.querySelector(".karte-ekg"), t.ekg);
      kel.addEventListener("click", function () { waehleKarte(i, kel); });
      kel.addEventListener("keydown", function (e) { if (e.key === "Enter") waehleKarte(i, kel); });
    });
  }
  function maleEkg(leinwand, e) {
    if (!leinwand) return;
    leinwand.style.width = "100%";
    var s = global.EKG.Streifen(leinwand, { werte: SATZ.sig.werte, fs: SATZ.sig.fs, mmProS: e.mmProS || 25,
                                            von: e.von || 0, dauer: e.dauer || 4 });
    s.zeichne(); global.setTimeout(s.zeichne, 60);
  }
  function waehleKarte(i, kel) {
    var p = gewaehlt.indexOf(i);
    if (p >= 0) { gewaehlt.splice(p, 1); kel.classList.remove("gewaehlt"); }
    else {
      if (gewaehlt.length === 2) {
        var weg = gewaehlt.shift(), alt = mHof.querySelector('.karte[data-i="' + weg + '"]');
        if (alt) alt.classList.remove("gewaehlt");
      }
      gewaehlt.push(i); kel.classList.add("gewaehlt");
    }
    mHof.querySelector(".vergleich").disabled = gewaehlt.length !== 2;
    mHof.querySelector(".mappe-vergleich").classList.remove("an");
  }
  function vergleiche() {
    if (gewaehlt.length !== 2) return;
    var a = Z.karten[gewaehlt[0]], b = Z.karten[gewaehlt[1]], ta = karteText(a), tb = karteText(b);
    var satz = null;
    global.FALL1.vergleiche.forEach(function (v) {
      if ((v.a === a.id && v.b === b.id) || (v.a === b.id && v.b === a.id)) satz = T(wert(v.text), P.vars());
    });
    var feld = mHof.querySelector(".mappe-vergleich");
    feld.innerHTML = '<div class="verg-kopf"><h3>' + esc(ta.titel) + '</h3><h3>' + esc(tb.titel) + '</h3></div>' +
      '<div class="verg-paar"><div class="verg-eins"><canvas height="150"></canvas><p>' + esc(ta.text).replace(/\n/g, "<br>") + '</p></div>' +
      '<div class="verg-eins"><canvas height="150"></canvas><p>' + esc(tb.text).replace(/\n/g, "<br>") + '</p></div></div>' +
      '<p class="verg-frage">' + esc(satz || "Kein Vergleich für diese beiden. Versuch eine andere Paarung.") + '</p>';
    var lw = feld.getElementsByTagName("canvas");
    [ta, tb].forEach(function (t, i) { if (t.ekg) maleEkg(lw[i], t.ekg); else lw[i].style.display = "none"; });
    feld.classList.add("an");
    Z.texte.push({ art: "vergleich", text: satz || "" });
    try { feld.scrollIntoView({ block: "nearest" }); } catch (e) {}
  }

  /* ------------------------------------------------------------ Stand der Schicht */
  var sHof = null;
  function oeffneStand() {
    if (!sHof) {
      sHof = el("div", "raetsel stand", d.body);
      sHof.id = "stand-hof";
      sHof.innerHTML = '<div class="raetsel-innen schmal"><div class="raetsel-kopf"><h2>Stand der Schicht</h2>' +
        '<button class="knopf zu" type="button">Zurück</button></div>' +
        '<p class="stand-frage"></p><p class="stand-frist"></p><p class="stand-saetze"></p>' +
        '<div class="raetsel-knoepfe"><button class="knopf haupt stand-los" type="button" hidden></button></div></div>';
      sHof.querySelector(".zu").addEventListener("click", schliesseStand);
      sHof.querySelector(".stand-los").addEventListener("click", function () {
        var tu = sHof.__tu; sHof.__tu = null;
        sHof.classList.remove("an"); sperre();
        if (tu) tu();
      });
    }
    var s = global.FALL1.stand();
    sHof.querySelector(".stand-frage").textContent = s.frage;
    sHof.querySelector(".stand-frist").textContent = s.frist;
    sHof.querySelector(".stand-saetze").textContent = s.saetze.slice(0, 3).join(" ");
    var b = sHof.querySelector(".stand-los");
    b.hidden = !s.knopf;
    if (s.knopf) { b.textContent = s.knopf.text; sHof.__tu = s.knopf.tu; }
    sHof.classList.add("an");
    sperre();
    fokus(s.knopf ? b : sHof.querySelector(".zu"));
    Z.texte.push({ art: "stand", text: s.frage + " " + s.frist + " " + s.saetze.join(" ") });
  }
  function schliesseStand() { if (sHof) sHof.classList.remove("an"); planeLeerlauf(); }

  /* ------------------------------------------------------------ Dialog
     Knoten: { wer, text, regie, tu, warum, antworten, weiter, endeText, umleiten, dann }.
     Antworten: { text, wenn, tu, zu, warum, z (Minuten, Vorgabe 1), zitat, dann }.
     Die Rückmeldung (`warum`) steht als Streifen unter der Antwort direkt nach der Wahl (§5, nie im Figurenmund). */
  var Dlg = { hof: null, baum: null, knoten: null, tippt: null, voll: "", warum: null, zitat: null, fertig: null };
  var NAMEN = { marlene: "Marlene", herrk: "Herr Baum", falk: "Dr. Falk", tochter: "Sabine Baum · Telefon", spielerin: "Du", erzaehler: "" };
  var BILDER = {};
  function dlgBau() {
    var h = Dlg.hof = el("div", "dialog", d.body);
    h.id = "dialog";
    h.innerHTML = '<div class="dialog-innen"><div class="dialog-kopf"><div class="dialog-bild"></div><div class="dialog-name"></div>' +
      '<div class="dialog-hud"><button type="button" class="dialog-hud-knopf" data-panel="verdacht" title="Verdacht (V)" aria-label="Verdacht">' + symbol("verdacht") + '<span>Verdacht</span></button>' +
      '<button type="button" class="dialog-hud-knopf" data-panel="mappe" title="Befundmappe (M)" aria-label="Befundmappe">' + symbol("mappe") + '<span>Mappe</span></button></div></div>' +
      '<div class="dialog-zitat"></div><div class="dialog-regie"></div><div class="dialog-text"></div>' +
      '<div class="rueck dialog-warum"></div><div class="dialog-antworten"></div></div>';
    ["marlene", "herr_k", "falk"].forEach(function (n) {
      if (!A.portraits || !A.portraits[n]) return;
      var img = d.createElement("img");
      img.src = A.portraits[n]; img.alt = ""; img.draggable = false;
      BILDER[n === "herr_k" ? "herrk" : n] = img;
    });
    var tel = d.createElement("div"); tel.className = "hoerer-rahmen"; tel.innerHTML = HOERER;
    BILDER.tochter = tel;
    Array.prototype.forEach.call(h.querySelectorAll(".dialog-hud-knopf"), function (k) {
      k.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (k.dataset.panel === "verdacht") oeffneVerdacht(); else oeffneMappe();
      });
    });
    h.addEventListener("click", function (e) {
      if (e.target.closest(".dialog-antwort, .dialog-hud-knopf")) return;
      if (Dlg.tippt) fertigTippen();
    });
  }
  function dlgStarte(baum, id, fertig) {
    if (!Dlg.hof) dlgBau();
    Dlg.baum = baum; Dlg.fertig = fertig || null; Dlg.warum = null; Dlg.zitat = null;
    zeigeKnoten(id);
  }
  function zeigeKnoten(id) {
    var k = Dlg.baum[id];
    if (!k) throw new Error("Dialogknoten fehlt: " + id);
    if (k.umleiten) { var u = k.umleiten(); if (u && u !== id) { zeigeKnoten(u); return; } }
    Dlg.knoten = k; Dlg.id = id;
    var text = T(wert(k.text) || "", P.vars());
    var regie = k.regie ? T(wert(k.regie) || "", P.vars()) : "";
    if (k.tu) k.tu();
    if (k.warum) { Dlg.warum = T(wert(k.warum), P.vars()); Z.texte.push({ art: "warum", text: Dlg.warum, knoten: id }); }
    var wer = wert(k.wer) || "erzaehler";
    var h = Dlg.hof, bild = h.querySelector(".dialog-bild");
    bild.innerHTML = "";
    if (BILDER[wer]) bild.appendChild(BILDER[wer]);
    h.classList.toggle("ohne-bild", !BILDER[wer]);
    h.classList.toggle("telefon", wer === "tochter");
    h.classList.toggle("spielerin", wer === "spielerin");
    h.classList.toggle("erzaehler", wer === "erzaehler");
    h.setAttribute("data-wer", wer);
    h.setAttribute("data-knoten", id);
    h.querySelector(".dialog-name").textContent = NAMEN[wer] || "";
    var zt = h.querySelector(".dialog-zitat");
    zt.textContent = Dlg.zitat ? Dlg.zitat : "";
    Dlg.zitat = null;
    h.querySelector(".dialog-regie").textContent = regie;
    var w = h.querySelector(".dialog-warum");
    w.textContent = Dlg.warum || "";
    w.className = "rueck dialog-warum" + (Dlg.warum ? " fast an" : "");
    Z.texte.push({ art: "replik", wer: wer, text: text, knoten: id });
    h.classList.add("an");
    sperre();
    tippe(text);
    var feld = h.querySelector(".dialog-antworten");
    feld.innerHTML = "";
    global.requestAnimationFrame(vdLage);
    var liste = (wert(k.antworten) || []).filter(function (a) { return !a.wenn || a.wenn(); });
    if (liste.length) {
      liste.forEach(function (a, i) {
        var b = el("button", "dialog-antwort", feld);
        b.type = "button";
        var t = T(wert(a.text), P.vars());
        b.innerHTML = '<span class="nr">' + (i + 1) + "</span>" + esc(t);
        b.setAttribute("data-text", t);
        Z.texte.push({ art: "option", text: t, knoten: id });
        b.addEventListener("click", function (ev) { ev.stopPropagation(); waehle(a, t); });
      });
    } else {
      var b2 = el("button", "dialog-antwort weiter", feld, T(wert(k.endeText) || "Weiter", P.vars()));
      b2.type = "button";
      b2.addEventListener("click", function (ev) { ev.stopPropagation(); weiter(); });
    }
  }
  function waehle(a, t) {
    if (Dlg.tippt) { fertigTippen(); return; }
    var z = a.z === undefined ? 1 : a.z;
    if (z) P.vor(z);
    if (a.tu) a.tu();
    Dlg.warum = a.warum ? T(wert(a.warum), P.vars()) : null;
    if (Dlg.warum) Z.texte.push({ art: "warum", text: Dlg.warum });
    Dlg.zitat = a.zitat ? (a.zitat === true ? t : T(wert(a.zitat), P.vars())) : null;
    var ziel = wert(a.zu);
    if (ziel) zeigeKnoten(ziel); else dlgEnde(a.dann);
  }
  function weiter() {
    if (Dlg.tippt) { fertigTippen(); return; }
    var k = Dlg.knoten;
    Dlg.zitat = null;
    Dlg.warum = null;          /* die Rückmeldung gehört zur Antwort direkt nach der Wahl, nicht in die nächste Szene */
    var ziel = wert(k.weiter);
    if (ziel) zeigeKnoten(ziel); else dlgEnde(k.dann);
  }
  function dlgEnde(dann) {
    global.clearInterval(Dlg.tippt); Dlg.tippt = null;
    Dlg.hof.classList.remove("an");
    Dlg.knoten = null; Dlg.warum = null; Dlg.zitat = null;
    var f = Dlg.fertig; Dlg.fertig = null;
    global.requestAnimationFrame(vdLage);
    sperre();
    if (dann) dann();
    if (f) f();
    auffrischen();
    planeLeerlauf();
  }
  function tippe(text) {
    var feld = Dlg.hof.querySelector(".dialog-text"), antw = Dlg.hof.querySelector(".dialog-antworten");
    global.clearInterval(Dlg.tippt); Dlg.tippt = null;
    Dlg.voll = text;
    if (schnell || ruhig || !bewegung || !text) { feld.textContent = text; antw.classList.add("an"); global.requestAnimationFrame(vdLage); return; }
    feld.textContent = "";
    antw.classList.remove("an");
    var i = 0;
    Dlg.tippt = global.setInterval(function () {
      i += 2;
      feld.textContent = text.slice(0, i);
      if (i >= text.length) fertigTippen();
    }, 16);
  }
  function fertigTippen() {
    global.clearInterval(Dlg.tippt); Dlg.tippt = null;
    Dlg.hof.querySelector(".dialog-text").textContent = Dlg.voll;
    Dlg.hof.querySelector(".dialog-antworten").classList.add("an");
    global.requestAnimationFrame(vdLage);
  }

  /* ------------------------------------------------------------ Fenster */
  function fenster(id, klasse, schmal) {
    var hof = d.getElementById(id);
    if (hof) return hof;
    hof = el("div", "raetsel " + klasse, d.body);
    hof.id = id;
    hof.innerHTML = '<div class="raetsel-innen' + (schmal ? " schmal" : "") + '"><div class="raetsel-kopf"><h2></h2>' +
      '<button class="knopf zu" type="button">Zurück</button></div><p class="raetsel-auftrag"></p>' +
      '<div class="fenster-inhalt"></div><div class="rueck"></div><div class="raetsel-knoepfe"></div></div>';
    return hof;
  }
  function zuFenster(hof) { hof.classList.remove("an"); sperre(); }

  /* Befundzeilen: lesen, dann in die Mappe (kein Rätsel). */
  function befundzeilen(opt) {
    var hof = fenster("befund-hof", "befund", true);
    hof.querySelector("h2").textContent = opt.titel;
    hof.querySelector(".raetsel-auftrag").textContent = opt.text || "";
    hof.querySelector(".zu").hidden = true;
    hof.querySelector(".fenster-inhalt").innerHTML = '<ul class="befund-zeilen">' +
      opt.zeilen.map(function (z) { return "<li>" + esc(T(z, P.vars())) + "</li>"; }).join("") + "</ul>";
    hof.querySelector(".rueck").innerHTML = "";
    var kn = hof.querySelector(".raetsel-knoepfe");
    kn.innerHTML = "";
    knopf("knopf haupt uebernehmen", opt.knopf || "In die Mappe", kn, function () {
      zuFenster(hof);
      if (opt.fertig) opt.fertig();
      planeLeerlauf();
    });
    Z.texte.push({ art: "befund", text: opt.zeilen.join(" ") });
    hof.classList.add("an"); sperre();
    fokus(kn.firstChild);
  }

  /* Frage am Streifen (Rhythmusfrage): falsche Wahl zeigt die Rückmeldung und gibt die Knöpfe nach einer Pause
     wieder frei; die richtige zeigt sie und „Weiter". Kein Zurück: der Rhythmus ist ein Engpass (§3). */
  function frage(opt) {
    var hof = fenster("frage-hof", "frage", false);
    hof.querySelector("h2").textContent = opt.titel;
    hof.querySelector(".raetsel-auftrag").textContent = opt.text;
    hof.querySelector(".zu").hidden = true;
    var inhalt = hof.querySelector(".fenster-inhalt");
    inhalt.innerHTML = (opt.ekg ? '<div class="frage-bild"><canvas height="172" style="width:100%"></canvas></div>' : "") +
      '<div class="frage-wahl"></div>';
    var rueck = hof.querySelector(".rueck");
    rueck.className = "rueck"; rueck.innerHTML = "";
    var kn = hof.querySelector(".raetsel-knoepfe");
    kn.innerHTML = "";
    var weiterK = knopf("knopf haupt weiter", "Weiter", kn, function () {
      zuFenster(hof);
      if (opt.fertig) opt.fertig();
      planeLeerlauf();
    });
    weiterK.hidden = true;
    var wahlFeld = inhalt.querySelector(".frage-wahl");
    opt.antworten.forEach(function (a, i) {
      var b = knopf("knopf wahl", null, wahlFeld);
      b.innerHTML = '<span class="nr">' + (i + 1) + "</span>" + esc(a.text);
      b.setAttribute("data-text", a.text);
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(wahlFeld.children, function (c) { c.disabled = true; });
        b.classList.add(a.richtig ? "richtig" : "falsch");
        rueck.className = "rueck " + (a.richtig ? "gut" : "fast");
        rueck.innerHTML = "<strong>" + (a.richtig ? "Richtig." : "Nicht ganz.") + "</strong> " + esc(T(a.warum, P.vars()));
        Z.texte.push({ art: "warum", text: a.warum });
        if (opt.beiWahl) opt.beiWahl(a);
        if (a.richtig) { weiterK.hidden = false; fokus(weiterK); }
        else global.setTimeout(function () {
          Array.prototype.forEach.call(wahlFeld.children, function (c) { c.disabled = false; c.classList.remove("falsch"); });
        }, schnell ? 60 : 2200);
      });
    });
    hof.classList.add("an"); sperre();
    if (opt.ekg) {
      var s = global.EKG.Streifen(inhalt.querySelector("canvas"), { werte: SATZ.sig.werte, fs: SATZ.sig.fs,
        mmProS: opt.ekg.mmProS || 25, von: opt.ekg.von || 0, dauer: opt.ekg.dauer || 6 });
      global.requestAnimationFrame(s.zeichne);
      global.setTimeout(s.zeichne, 80);
    }
  }

  /* Auswahl ohne Bewertung (Was willst du messen?). */
  function wahl(opt) {
    var hof = fenster("wahl-hof", "wahl-hof", true);
    hof.querySelector("h2").textContent = opt.titel;
    hof.querySelector(".raetsel-auftrag").textContent = opt.text;
    var zu = hof.querySelector(".zu");
    zu.hidden = false;
    zu.onclick = function () { zuFenster(hof); if (opt.zu) opt.zu(); planeLeerlauf(); };
    var inhalt = hof.querySelector(".fenster-inhalt");
    inhalt.innerHTML = '<div class="frage-wahl"></div>';
    hof.querySelector(".rueck").innerHTML = "";
    var wahlFeld = inhalt.querySelector(".frage-wahl");
    opt.wahl.forEach(function (w, i) {
      var b = knopf("knopf wahl" + (w.fertig ? " erledigt" : ""), null, wahlFeld);
      b.innerHTML = '<span class="nr">' + (i + 1) + "</span>" + esc(w.text) + (w.fertig ? "  ✓" : "");
      b.setAttribute("data-text", w.text);
      b.addEventListener("click", function () { zuFenster(hof); w.tu(); });
    });
    var kn = hof.querySelector(".raetsel-knoepfe");
    kn.innerHTML = "";
    if (opt.genug) knopf("knopf genug", opt.genug, kn, function () { zu.onclick(); });
    hof.classList.add("an"); sperre();
  }

  /* Zirkel aus dem Spiel: Prüfung gegen die Annotation (Länge und Stelle), Toleranzen wie im Spiel. */
  var zirkelOffen = null;
  function zirkel(opt) {
    zirkelOffen = opt.was;
    global.Zirkel.starte({
      satz: SATZ, was: opt.was, toleranz: opt.toleranz, mmProS: opt.mmProS, von: opt.von, dauer: opt.dauer,
      titel: opt.titel, auftrag: opt.auftrag,
      deutung: function (ms) { return opt.deutung ? opt.deutung(ms) : ""; },
      fertig: function (erg) { zirkelOffen = null; opt.fertig(erg); planeLeerlauf(); }
    });
    var hof = d.getElementById("zirkel-hof");
    if (hof && !hof.__beobachtet) {
      hof.__beobachtet = true;
      hof.querySelector(".zu").addEventListener("click", function () { zirkelOffen = null; if (hof.__zu) hof.__zu(); });
      Array.prototype.forEach.call(hof.querySelectorAll(".knopf"), function (b) { b.style.minHeight = "44px"; });
    }
    if (hof) hof.__zu = opt.zu || null;
  }
  /* Für pruefe.mjs: die Strecke des ersten passenden Schlags (Annotation) genau oder mit Versatz setzen. */
  function miss(versatzMs) {
    var hof = d.getElementById("zirkel-hof");
    if (!zirkelOffen || !hof || !hof.classList.contains("an")) return null;
    var a = global.Zirkel.AUFGABEN[zirkelOffen], st = hof.__streifen.stand, sl = SATZ.schlaege;
    for (var i = 0; i < sl.length; i++) {
      var s1 = sl[i][a.von], s2 = a.folge ? (sl[i + 1] && sl[i + 1][a.bis]) : sl[i][a.bis];
      if (s1 === undefined || s2 === undefined) continue;
      if (s1 < st.von - 0.02 || s2 > st.von + st.dauer + 0.02) continue;
      var e = s2 + (versatzMs || 0) / 1000;
      global.Zirkel.__pruefe(Math.round((e - s1) * 1000), s1, e);
      return Math.round((s2 - s1) * 1000);
    }
    return null;
  }

  /* ------------------------------------------------------------ Seiten: Epilog (Erzähler) und Ende */
  function seite(id) {
    var s = d.getElementById(id);
    if (!s) { s = el("div", "seite", d.body); s.id = id; }
    s.innerHTML = "";
    return s;
  }
  function epilogSeite(absaetze, fertig) {
    var s = seite("epilog-seite");
    var karte = el("div", "seite-karte", s);
    el("p", "seite-ober", karte, "Epilog");
    el("h2", "seite-titel", karte, "Dienst 3 · eine Woche später");
    var text = el("div", "seite-text", karte);
    var kn = el("div", "raetsel-knoepfe", karte);
    var i = 0;
    var b = knopf("knopf haupt seite-weiter", "Weiter", kn, naechster);
    function naechster() {
      if (i < absaetze.length) {
        var p = el("p", "seite-absatz", text, absaetze[i]);
        Z.texte.push({ art: "replik", wer: "erzaehler", text: absaetze[i], knoten: "epilog" });
        i++;
        if (!ruhig && !schnell && bewegung) { p.classList.add("kommt"); global.requestAnimationFrame(function () { p.classList.remove("kommt"); }); }
        if (i === absaetze.length) b.textContent = "Zum Ende des Prototyps";
        return;
      }
      s.classList.remove("an");
      if (fertig) fertig();
    }
    s.classList.add("an"); sperre();
    naechster();
    fokus(b);
  }
  function endeSeite() {
    var s = seite("ende-seite");
    var karte = el("div", "seite-karte", s);
    el("p", "seite-ober", karte, "Prototyp Fall 1");
    el("h2", "seite-titel", karte, "Ende des Prototyps");
    el("p", "seite-klein", karte, "Spielzeit 06:40 bis " + zeitText() + " · " + Z.karten.length + " Karten in der Mappe. " +
      "So sind die Folgen dieses Durchgangs verteilt; ein zweiter Durchgang mit anderen Antworten zeigt die Varianten.");
    var F = global.FALL1, gesetzt = [], offenL = [];
    F.flags.forEach(function (f) { (Z.f[f.id] ? gesetzt : offenL).push(f); });
    el("h3", "stand-ueber", karte, "Gesetzt in diesem Durchgang");
    var ul = el("ul", "ende-flags hat", karte);
    ul.id = "ende-gesetzt";
    if (!gesetzt.length) el("li", "leer", ul, "Keine: der gerade Weg.");
    gesetzt.forEach(function (f) {
      var li = el("li", null, ul); li.setAttribute("data-flag", f.id);
      el("code", null, li, f.id); li.appendChild(d.createTextNode(" " + f.wenn));
    });
    el("h3", "stand-ueber", karte, "Nicht gesetzt");
    var ul2 = el("ul", "ende-flags offen", karte);
    offenL.forEach(function (f) {
      var li = el("li", null, ul2); li.setAttribute("data-flag", f.id);
      el("code", null, li, f.id); li.appendChild(d.createTextNode(" " + f.wenn));
    });
    if (F.ende) { var extra = F.ende(); if (extra) el("p", "seite-klein", karte, extra); }
    var kn = el("div", "raetsel-knoepfe", karte);
    var b = knopf("knopf haupt", "Noch einmal", kn, function () { global.location.reload(); });
    b.id = "noch-einmal";
    s.classList.add("an"); sperre();
    fokus(b);
  }

  /* ------------------------------------------------------------ Menü und Info */
  var menue = null, info = null;
  function huelleHof(id, klasse, titel, beiZu) {
    var h = el("div", "huelle-hof " + klasse, d.body);
    h.id = id;
    h.setAttribute("role", "dialog");
    var k = el("div", "huelle-karte", h), kopf = el("div", "huelle-kopf", k);
    el("h2", null, kopf, titel);
    if (beiZu) knopf("knopf zu", "Zurück", kopf, beiZu);
    h.addEventListener("click", function (e) { if (e.target === h && beiZu) beiZu(); });
    h.__innen = el("div", "huelle-innen", k);
    return h;
  }
  function oeffneMenue() {
    if (!Z || !Z.laeuft || offen()) return;
    if (!menue) {
      menue = huelleHof("menue-hof", "menue", "Pause", schliesseMenue);
      var t = menue.__innen;
      el("p", "menue-ort", t).id = "menue-ort";
      knopf("knopf gross haupt", "Fortsetzen", t, schliesseMenue).id = "menue-weiter";
      var bw = knopf("knopf gross umschalter", null, t, function () {
        bewegung = !bewegung;
        try { if (global.Leben) global.Leben.bewegung(bewegung); } catch (e) {}
        try { global.localStorage.setItem("fall1-bewegung", bewegung ? "an" : "aus"); } catch (e) {}
        zeigeBewegung();
      });
      bw.id = "menue-bewegung";
      el("span", null, bw, "Bewegung");
      el("span", "schalter", bw, "");
      knopf("knopf gross", "Von vorn", t, function () { global.location.reload(); }).id = "menue-neu";
      knopf("knopf gross", "Info & Quellen", t, zeigeInfo).id = "menue-info";
    }
    d.getElementById("menue-ort").textContent = "Dienst 1 · " + zeitText() + " · Aufnahme";
    zeigeBewegung();
    menue.classList.add("an"); sperre();
    fokus(d.getElementById("menue-weiter"));
  }
  function zeigeBewegung() {
    var b = d.getElementById("menue-bewegung");
    if (!b) return;
    b.setAttribute("aria-pressed", String(!bewegung));
    b.querySelector(".schalter").textContent = ruhig ? "System: reduziert" : (bewegung ? "an" : "aus");
  }
  function schliesseMenue() { if (info) info.classList.remove("an"); if (menue) menue.classList.remove("an"); planeLeerlauf(); }
  function zeigeInfo() {
    if (!info) {
      info = huelleHof("info-hof", "info", "Info & Quellen", function () { info.classList.remove("an"); sperre(); });
      var t = info.__innen;
      el("p", "info-lead", t, "Spielbarer Prototyp der neuen Geschichte von Fall 1 (docs/REDESIGN_FALL1.md): neue Dialoge, alte Raumgrafik, nur Deutsch. Das Spiel selbst ist unverändert.");
      var w = el("p", "info-warnung", t);
      el("strong", null, w, "Kein Medizinprodukt.");
      w.appendChild(d.createTextNode(" Lernsoftware für die Ausbildung, keine Grundlage für Behandlungsentscheidungen."));
      el("h3", "info-ueber", t, "Datenquelle der Kurve");
      var ul = el("ul", "info-quellen", t), li = el("li", "info-quelle", ul);
      el("span", "info-bank", li, "LUDB — Lobachevsky University Electrocardiography Database v1.0.1");
      el("span", "info-autoren", li, "Kalyakulina A., Yusipov I., Moskalenko V. et al. · PhysioNet");
      el("span", "info-lizenz", li, "Lizenz: Open Data Commons Attribution License v1.0 (ODC-By 1.0)");
      el("span", "info-adresse", li, "physionet.org/content/ludb/1.0.1/");
      el("p", "info-klein", t, "PhysioNet: Goldberger A. et al. (2000), Circulation 101(23):e215–e220. Aufnahme 39, Ableitung II, 10 s; geprüft wird gegen die Experten-Annotation.");
    }
    info.classList.add("an"); sperre();
    fokus(info.querySelector(".zu"));
  }

  /* ------------------------------------------------------------ Titel */
  var titel = null;
  function baueTitel() {
    titel = el("div", "titel", d.body);
    titel.id = "titel";
    var bild = el("div", "titel-bild", titel), eb = el("div", "titel-ebenen", bild);
    [A.hintergrund, A.mittelgrund].forEach(function (u) { if (!u) return; var i = el("img", null, eb); i.src = u; i.alt = ""; });
    el("p", "titel-hinweis", titel, "Spielbarer Prototyp: neue Geschichte, alte Raumgrafik, nur Deutsch.");
    var innen = el("div", "titel-innen", titel);
    el("p", "titel-ober", innen, "EKG-Lernspiel");
    el("h1", "titel-name", innen, "Nachtdienst");
    el("p", "titel-fall", innen, "Fall 1 · Darf Herr Baum heim?");
    var reihe = el("div", "titel-knoepfe", innen);
    knopf("knopf gross haupt", "Spielen", reihe, los).id = "titel-los";
    knopf("knopf gross", "Info & Quellen", reihe, zeigeInfo).id = "titel-info";
  }
  function los() {
    if (Z.laeuft) return;
    Z.laeuft = true;
    titel.classList.add("weg");
    global.setTimeout(function () { titel.hidden = true; }, schnell ? 0 : 460);
    sperre();
    global.FALL1.start();
  }

  /* ------------------------------------------------------------ Tastatur */
  function taste(e) {
    var k = e.key;
    var h = d.querySelector(".huelle-hof.an");
    if (h) {
      if (k === "Escape") { e.preventDefault(); if (h === info) { info.classList.remove("an"); sperre(); } else schliesseMenue(); }
      return;
    }
    if (mHof && mHof.classList.contains("an") && k === "Escape") { e.preventDefault(); schliesseMappe(); return; }
    if (vdHof && vdHof.classList.contains("an") && k === "Escape") { e.preventDefault(); schliesseVerdacht(); return; }
    if (Dlg.hof && Dlg.hof.classList.contains("an") && !d.querySelector(".raetsel.an, .mappe.an")) {
      if (k === "v" || k === "V") { oeffneVerdacht(); return; }
      if (k === "m" || k === "M") { oeffneMappe(); return; }
      if (k === " " || k === "Enter") {
        e.preventDefault();
        if (Dlg.tippt) fertigTippen();
        else { var w = Dlg.hof.querySelector(".dialog-antwort.weiter"); if (w) w.click(); }
      } else if (/^[1-9]$/.test(k)) {
        var b = Dlg.hof.querySelectorAll(".dialog-antwort")[+k - 1];
        if (b && !b.classList.contains("weiter")) { e.preventDefault(); b.click(); }
      }
      return;
    }
    var fe = d.querySelector(".raetsel.an:not(#zirkel-hof)");
    if (fe) {
      if (/^[1-9]$/.test(k)) {
        var c = fe.querySelectorAll(".frage-wahl .knopf")[+k - 1];
        if (c && !c.disabled) { e.preventDefault(); c.click(); }
      } else if (k === "Enter") {
        var u = fe.querySelector(".raetsel-knoepfe .knopf.haupt:not([hidden])");
        if (u && d.activeElement === d.body) { e.preventDefault(); u.click(); }
      } else if (k === "Escape") {
        var z = fe.querySelector(".zu:not([hidden])");
        if (z) { e.preventDefault(); z.click(); }
      }
      return;
    }
    if (k === "Escape") {
      if (mHof && mHof.classList.contains("an")) { e.preventDefault(); schliesseMappe(); return; }
      if (offen()) return;
      e.preventDefault(); oeffneMenue();
    } else if (!offen() && Z && Z.laeuft) {
      if (k === "h" || k === "H") zeigeFelder();
      else if (k === "s" || k === "S") oeffneStand();
      else if (k === "v" || k === "V") oeffneVerdacht();
      else if (k === "m" || k === "M") oeffneMappe();
    }
  }

  /* ------------------------------------------------------------ Maße (wie web/huelle.js) */
  function masse() {
    var r = d.documentElement, s = r.style;
    s.setProperty("--breite", r.clientWidth + "px");
    s.setProperty("--hoehe", r.clientHeight + "px");
  }

  /* ------------------------------------------------------------ Start */
  function start() {
    Z = neuerZustand();
    try { if (global.localStorage.getItem("fall1-bewegung") === "aus") bewegung = false; } catch (e) {}
    masse();
    global.addEventListener("resize", masse);
    global.addEventListener("orientationchange", function () { masse(); global.setTimeout(masse, 300); });
    global.addEventListener("keydown", taste);
    baueBuehne();
    baueHud();
    if (!bewegung) try { global.Leben.bewegung(false); } catch (e) {}
    try { global.Leben.zeit(Z.zeit); } catch (e) {}
    baueTitel();
    auffrischen();
    sperre();
  }

  global.__prototyp = {
    zustand: function () {
      var v = {};
      Object.keys(Z.verdacht).forEach(function (k) { v[k] = Z.verdacht[k].zustand; });
      return { zeit: zeitText(), minuten: Z.zeit, flags: Object.keys(Z.f), karten: Z.karten.map(function (k) { return k.id; }),
               werte: Z.werte, verdacht: v, falkDa: Z.falkDa, x: Z.x, offen: offen() };
    },
    schnell: function (an) { schnell = an !== false; },
    miss: miss,
    texte: function () { return Z.texte; },
    ruhig: function () { return ruhig; },
    bewegung: function () { return bewegung; },
    satz: function () { return { schlaege: SATZ.schlaege, mess: SATZ.mess }; }
  };

  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", start); else start();
})(window);
