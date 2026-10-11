/* „Nachtdienst" — die Hülle um das Spiel: Vollbild-Bühne, HUD, Pausenmenü,
   Titelbildschirm, Info & Quellen und der Hinweis im Hochformat.

   Grundsatz: Es soll aussehen wie ein Spiel, nicht wie eine Webseite. Die
   Bühne (1600 × 900) füllt den Bildschirm im Verhältnis 16:9; was übrig
   bleibt, ist Tinte (ART_BIBLE §2). Über der Bühne liegt nur das HUD: Uhr,
   drei Symbolknöpfe und ≡. Alles andere (Sprache, Vollbild, Quellen) steckt
   im Menü — ≡ oder Escape, solange kein Dialog und kein Rätsel offen ist.

   Die Namensnennung der Datenquellen ist Lizenzpflicht (ODC-By, CC BY) und
   bleibt unter „Info & Quellen" vom Titel und vom Menü aus erreichbar.

   Die Symbole zeichnet der Code (SVG-Pfade unten), kein Text in Bildern.
   Nichts blinkt (ART_BIBLE §2, Regel 3).                                    */
(function (global) {
  "use strict";

  var d = global.document;
  var NACH_LADEN = "nachtdienst-nach-laden";     /* sessionStorage: wohin nach einem Sprachwechsel */
  var KUNST = null, DATEN = null;
  var laeuft = false;                           /* Spiel.start ist erfolgt */
  var flaeche = null, hud = null, titel = null, menue = null, info = null, sprachHof = null, frageHof = null;
  var el$ = {};                                 /* HUD-Teile */
  var urls = [];
  var vollbildVersucht = false, eigenerWechsel = false, vollbildMerken = false;

  /* Symbole, 24 × 24, Strich in currentColor — harte Ecken wie die übrige Oberfläche. */
  var SYMBOLE = {
    hinweis: '<path d="M9.5 18.5h5M10.5 21.5h3"/><path d="M12 2.8a6.2 6.2 0 0 0-3.7 11.2c.8.6 1.2 1.4 1.2 2.4v.1h5v-.1c0-1 .4-1.8 1.2-2.4A6.2 6.2 0 0 0 12 2.8z"/>',
    stand: '<path d="M5.5 4.5h13v17h-13z"/><path d="M9 2.5h6v4H9z"/><path d="M8.5 11.5l1.5 1.5 2.6-2.6M14.5 12h2M8.5 17l1.5 1.5 2.6-2.6M14.5 17.5h2"/>',
    mappe: '<path d="M2.5 5.5h7l2 2.5h10v12h-19z"/><path d="M6.5 12.5h11M6.5 16h7"/>',
    menue: '<path d="M4 6.5h16M4 12h16M4 17.5h16"/>'
  };
  /* Hinweis im Hochformat: das Gerät hochkant (gestrichelt), ein Bogen, das Gerät quer. */
  var QUER = '<svg class="quer-bild" viewBox="0 0 72 64" aria-hidden="true" focusable="false">' +
    '<rect x="6" y="4" width="26" height="40" rx="3" class="alt"/>' +
    '<rect x="24" y="32" width="42" height="26" rx="3"/><path d="M60 37.5v15"/>' +
    '<path d="M40 8.5a18 18 0 0 1 17.5 16"/><path d="M53 21.5l4.5 4 3.5-5"/></svg>';

  /* Datenquellen, sinngemäß nach ATTRIBUTION.md. Namen, Autoren und Lizenzbezeichnungen bleiben unübersetzt. */
  var QUELLEN = [
    { kurz: "ludb", bank: "LUDB — Lobachevsky University Electrocardiography Database v1.0.1",
      autoren: "Kalyakulina A., Yusipov I., Moskalenko V. et al. · PhysioNet",
      lizenz: "Open Data Commons Attribution License v1.0 (ODC-By 1.0)",
      adresse: "physionet.org/content/ludb/1.0.1/" },
    { kurz: "ptbxl", bank: "PTB-XL v1.0.3",
      autoren: "Wagner P., Strodthoff N., Bousseljot R.-D. et al. · PhysioNet",
      lizenz: "Creative Commons Attribution 4.0 (CC BY 4.0)",
      adresse: "physionet.org/content/ptb-xl/1.0.3/" },
    { kurz: "chapman", bank: "Chapman-Shaoxing / Ningbo — 12-lead ECG database for arrhythmia study",
      autoren: "Zheng J. et al. · Chapman University, Shaoxing People’s Hospital, Ningbo First Hospital · PhysioNet",
      lizenz: "Creative Commons Attribution 4.0 (CC BY 4.0)",
      adresse: "physionet.org/content/ecg-arrhythmia/1.0.0/" }
  ];

  /* ------------------------------------------------------------ Bausteine */
  function el(tag, klasse, eltern, text) {
    var e = d.createElement(tag);
    if (klasse) e.className = klasse;
    if (text !== undefined && text !== null) e.textContent = text;
    if (eltern) eltern.appendChild(e);
    return e;
  }
  function knopf(klasse, text, eltern, beiKlick, id) {
    var b = el("button", klasse, eltern, text);
    b.type = "button";
    if (id) b.id = id;
    if (beiKlick) b.addEventListener("click", beiKlick);
    return b;
  }
  function symbol(name) {
    return '<svg class="symbol" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + SYMBOLE[name] + "</svg>";
  }
  function merke(name, wert) {
    try { if (wert === null) global.sessionStorage.removeItem(name); else global.sessionStorage.setItem(name, wert); }
    catch (e) {}
  }
  function lies(name) { try { return global.sessionStorage.getItem(name); } catch (e) { return null; } }
  function fokus(e) { if (e && e.focus) { try { e.focus({ preventScroll: true }); } catch (x) { e.focus(); } } }

  /* Ein Fenster der Hülle: abgedunkelter Grund, darauf eine Karte aus Papier. Tippen auf den Grund schließt. */
  function hof(id, klasse, kopfText, mitZurueck, beiZu) {
    var h = el("div", "huelle-hof " + klasse, d.body);
    h.id = id;
    h.setAttribute("role", "dialog");
    h.setAttribute("aria-modal", "true");
    var karte = el("div", "huelle-karte", h);
    var kopf = el("div", "huelle-kopf", karte);
    var h2 = el("h2", null, kopf, kopfText);
    h2.id = id + "-titel";
    h.setAttribute("aria-labelledby", h2.id);
    if (mitZurueck) knopf("knopf zu", T("Zurück"), kopf, beiZu);
    h.addEventListener("click", function (e) { if (e.target === h) beiZu(); });
    h.__innen = el("div", "huelle-innen", karte);
    return h;
  }
  function auf(h, ziel) {
    if (!h.classList.contains("an")) h.__vorher = d.activeElement;
    h.classList.add("an");
    sperre();
    fokus(ziel || h.querySelector(".huelle-innen button:not([hidden])") || h.querySelector("button"));
  }
  function zu(h) {
    if (!h || !h.classList.contains("an")) return;
    h.classList.remove("an");
    sperre();
    var v = h.__vorher; h.__vorher = null;
    if (v && d.contains(v) && !v.closest("[inert]")) fokus(v);
  }
  function titelOffen() { return !!titel && !titel.hidden && !titel.classList.contains("weg"); }
  /* Das oberste offene Fenster der Hülle — in dieser Reihenfolge liegen sie übereinander. */
  function oberstes() {
    var liste = [frageHof, sprachHof, info, menue];
    for (var i = 0; i < liste.length; i++) if (liste[i] && liste[i].classList.contains("an")) return liste[i];
    return titelOffen() ? titel : null;
  }
  /* Solange die Hülle offen ist, bleiben Bühne und HUD stumm (auch für die Tabulatortaste). */
  function sperre() {
    if (!flaeche) return;
    if (oberstes()) flaeche.setAttribute("inert", ""); else flaeche.removeAttribute("inert");
  }
  /* Ein Spielfenster (Dialog, Rätsel, Mappe, Stand) ist offen? Dann gehört Escape ihm. */
  function spielFensterOffen() { return !!d.querySelector(".dialog.an, .raetsel.an, .mappe.an"); }

  /* ------------------------------------------------------------ Maße
     Die sichtbare Fenstergröße in px — auf dem iPad zuverlässiger als 100vh (Werkzeugleisten). */
  function masse() {
    var r = d.documentElement, s = r.style;
    s.setProperty("--breite", r.clientWidth + "px");
    s.setProperty("--hoehe", r.clientHeight + "px");
  }

  /* ------------------------------------------------------------ Vollbild */
  function eigenstaendig() {
    try {
      return !!global.navigator.standalone ||
        (global.matchMedia && global.matchMedia("(display-mode: standalone), (display-mode: fullscreen)").matches);
    } catch (e) { return false; }
  }
  function vollbildMoeglich() {
    var e = d.documentElement;
    return !eigenstaendig() && !!(e.requestFullscreen || e.webkitRequestFullscreen) &&
      d.fullscreenEnabled !== false && d.webkitFullscreenEnabled !== false;
  }
  function imVollbild() { return !!(d.fullscreenElement || d.webkitFullscreenElement); }
  function vollbild(an) {
    vollbildMerken = false;
    try {
      if (an && !imVollbild() && vollbildMoeglich()) {
        var e = d.documentElement, p;
        p = e.requestFullscreen ? e.requestFullscreen({ navigationUI: "hide" }) : e.webkitRequestFullscreen();
        if (p && p.then) p.then(escapeBehalten, function () {});
        else escapeBehalten();
      } else if (!an && imVollbild()) {
        eigenerWechsel = true;
        var q = d.exitFullscreen ? d.exitFullscreen() : d.webkitExitFullscreen();
        if (q && q.then) q.then(null, function () {});
      }
    } catch (x) { /* kein Vollbild (z. B. iPhone): still weiterspielen */ }
  }
  /* Chromium: Escape bleibt beim Spiel (öffnet das Menü); Escape lange halten verlässt das Vollbild. */
  function escapeBehalten() {
    try {
      var k = global.navigator.keyboard;
      if (k && k.lock) k.lock(["Escape"]).then(null, function () {});
    } catch (e) {}
  }
  function vollbildGewechselt() {
    zeigeVollbild();
    var war = eigenerWechsel;
    eigenerWechsel = false;
    /* Hat der Browser das Vollbild beendet (Escape in Safari), pausiert das Spiel wie jedes andere. */
    if (!imVollbild() && !war && laeuft && !oberstes() && !spielFensterOffen()) oeffneMenue();
  }
  function zeigeVollbild() {
    var b = menue && menue.querySelector("#menue-vollbild");
    if (!b) return;
    b.hidden = !vollbildMoeglich();
    var an = imVollbild();
    b.setAttribute("aria-pressed", an ? "true" : "false");
    b.querySelector(".schalter").textContent = an ? T("an") : T("aus");
  }

  /* ------------------------------------------------------------ HUD */
  function hudKnopf(id, name, text, tipp, eltern, beiKlick) {
    var b = knopf("hud-knopf", null, eltern, beiKlick, id);
    b.innerHTML = symbol(name);
    if (text) el("span", "hud-text", b, text);
    b.title = tipp;
    b.setAttribute("aria-label", text || tipp);
    return b;
  }
  function baueHud() {
    hud = el("div", "hud", flaeche);
    hud.id = "hud";
    var links = el("div", "hud-gruppe", hud);
    var uhr = el("div", "hud-uhr", links);
    el$.zeit = el("span", "hud-zeit", uhr, "06:40");
    el$.zeit.id = "hud-zeit";
    el$.ort = el("span", "hud-ort", uhr, T("Aufnahme"));
    el$.ort.id = "hud-ort";
    var rechts = el("div", "hud-gruppe", hud);
    el$.hinweis = hudKnopf("hud-hinweis", "hinweis", T("Was geht hier?"), T("Zeigt, was anklickbar ist") + " (H)", rechts,
      function () { if (laeuft) global.Szene.zeigeFelder(2400); });
    el$.stand = hudKnopf("hud-stand", "stand", T("Stand"), T("Was hast du, was ist offen") + " (S)", rechts,
      function () { if (laeuft) global.Stand.oeffne(); });
    el$.mappe = hudKnopf("hud-mappe", "mappe", T("Befundmappe"), T("Befundmappe"), rechts,
      function () { if (laeuft) global.Mappe.oeffne(); });
    el$.zahl = el("span", "hud-zahl", el$.mappe, "0");
    el$.menue = hudKnopf("hud-menue", "menue", null, T("Menü") + " (Esc)", rechts, oeffneMenue);
  }
  /* Aufgerufen von spiel.js (kopfAuffrischen) nach jeder Änderung an Zeit, Raum oder Mappe. */
  function anzeige(w) {
    if (!hud) return;
    if (w.zeit) el$.zeit.textContent = w.zeit;
    if (w.ort !== undefined) { el$.ort.textContent = w.ort; el$.ort.hidden = !w.ort; }
    if (w.befunde !== undefined) {
      el$.zahl.textContent = String(w.befunde);
      el$.mappe.classList.toggle("voll", w.befunde > 0);
      el$.mappe.setAttribute("aria-label", T("Befundmappe") + " · " + w.befunde);
      el$.mappe.title = T("Befundmappe") + " · " + w.befunde;
    }
  }

  /* ------------------------------------------------------------ Sprache */
  function sprachKnoepfe(eltern) {
    var reihe = el("div", "sprachen", eltern);
    reihe.setAttribute("role", "group");
    reihe.setAttribute("aria-label", "Sprache / Language / Язык");
    global.Sprache.SPRACHEN.forEach(function (sp) {
      var b = knopf("knopf sprache", sp.name, reihe, function () { waehleSprache(sp.kurz); });
      b.setAttribute("data-sprache", sp.kurz);
      b.setAttribute("lang", sp.kurz);
      b.setAttribute("aria-pressed", sp.kurz === global.Sprache.jetzt() ? "true" : "false");
    });
    return reihe;
  }
  function sprachName() {
    var k = global.Sprache.jetzt(), n = k;
    global.Sprache.SPRACHEN.forEach(function (sp) { if (sp.kurz === k) n = sp.name; });
    return n;
  }
  /* Ein Sprachwechsel lädt neu (spiel.js: neuZeichnen) — danach geht es dort weiter, wo man war. */
  function waehleSprache(kurz) {
    if (kurz === global.Sprache.jetzt()) {
      if (sprachHof) zu(sprachHof);
      return;
    }
    if (laeuft) {
      merke(NACH_LADEN, JSON.stringify({ ziel: "menue", voll: imVollbild() || vollbildMerken }));
      global.Sprache.setze(kurz);                    /* sichert den Spielstand und lädt neu */
    } else {
      /* Vor dem Start nichts sichern — sonst überschriebe der leere Zustand den gespeicherten. */
      global.Sprache.setze(kurz, true);
      try { global.location.reload(); } catch (e) {}
    }
  }
  function zeigeSprache() {
    if (!sprachHof) {
      sprachHof = hof("sprache-hof", "sprachwahl-hof", T("Sprache"), true, function () { zu(sprachHof); });
      sprachKnoepfe(sprachHof.__innen).classList.add("senkrecht");
    }
    auf(sprachHof, sprachHof.querySelector('[aria-pressed="true"]'));
  }

  /* ------------------------------------------------------------ Rückfrage */
  function frage(text, ja, beiJa) {
    if (!frageHof) {
      frageHof = hof("frage-neu-hof", "rueckfrage", T("Neues Spiel"), false, function () { zu(frageHof); });
      frageHof.__text = el("p", "rueckfrage-text", frageHof.__innen);
      var reihe = el("div", "rueckfrage-knoepfe", frageHof.__innen);
      frageHof.__ja = knopf("knopf gross haupt", "", reihe, function () {
        var f = frageHof.__beiJa; frageHof.__beiJa = null;
        frageHof.classList.remove("an"); frageHof.__vorher = null; sperre();
        if (f) f();
      }, "frage-ja");
      knopf("knopf gross", T("Abbrechen"), reihe, function () { zu(frageHof); }, "frage-nein");
    }
    frageHof.__text.textContent = text;
    frageHof.__ja.textContent = ja;
    frageHof.__beiJa = beiJa;
    auf(frageHof, frageHof.querySelector("#frage-nein"));
  }
  function frageNeu() {
    frage(T("Schicht von vorn beginnen? Die Befundmappe wird geleert."), T("Von vorn beginnen"), function () {
      if (laeuft) { schliesseMenue(); global.Spiel.vonVorn(); }
      else los(true);
    });
  }

  /* ------------------------------------------------------------ Pausenmenü */
  function baueMenue() {
    menue = hof("menue-hof", "menue", T("Pause"), false, schliesseMenue);
    var innen = menue.__innen;
    el$.menueOrt = el("p", "menue-ort", innen);
    knopf("knopf gross haupt", T("Fortsetzen"), innen, schliesseMenue, "menue-weiter");
    knopf("knopf gross", T("Neues Spiel"), innen, frageNeu, "menue-neu");
    var zeile = el("div", "menue-zeile", innen);
    el("span", "menue-etikett", zeile, T("Sprache"));
    sprachKnoepfe(zeile);
    var vb = knopf("knopf gross umschalter", null, innen, function () { vollbild(!imVollbild()); }, "menue-vollbild");
    el("span", null, vb, T("Vollbild"));
    el("span", "schalter", vb, "");
    knopf("knopf gross", T("Info & Quellen"), innen, zeigeInfo, "menue-info");
    zeigeVollbild();
  }
  function oeffneMenue() {
    if (!laeuft || titelOffen() || spielFensterOffen()) return;
    if (!menue) baueMenue();
    el$.menueOrt.textContent = el$.zeit.textContent + (el$.ort.textContent ? " · " + el$.ort.textContent : "");
    zeigeVollbild();
    auf(menue, menue.querySelector("#menue-weiter"));
  }
  function schliesseMenue() {
    if (info) zu(info);
    if (menue) zu(menue);
    /* War vor dem Sprachwechsel Vollbild an, kommt es mit diesem Tippen zurück. */
    if (vollbildMerken) vollbild(true);
  }

  /* ------------------------------------------------------------ Info & Quellen */
  function baueInfo() {
    info = hof("info-hof", "info", T("Info & Quellen"), true, function () { zu(info); });
    var t = info.__innen;
    el("p", "info-lead", t, T("Nachtdienst ist ein Lernspiel zum EKG. Alle Kurven stammen aus echten Aufnahmen offener Datenbanken, alle geprüften Zeiten aus deren Experten-Annotation."));
    var warnung = el("p", "info-warnung", t);
    el("strong", null, warnung, T("Kein Medizinprodukt."));
    warnung.appendChild(d.createTextNode(" " + T("Lernsoftware für die Ausbildung, keine Grundlage für Behandlungsentscheidungen.")));
    el("h3", "info-ueber", t, T("Datenquellen"));
    var liste = el("ul", "info-quellen", t);
    QUELLEN.forEach(function (q) {
      var li = el("li", "info-quelle", liste);
      li.setAttribute("data-quelle", q.kurz);
      el("span", "info-bank", li, q.bank);
      el("span", "info-autoren", li, q.autoren);
      el("span", "info-lizenz", li, T("Lizenz: {lizenz}", { lizenz: q.lizenz }));
      el("span", "info-adresse", li, q.adresse);
    });
    el("p", "info-klein", t, "PhysioNet: Goldberger A. et al. (2000), Circulation 101(23):e215–e220.");
    el("p", "info-klein", t, T("Für das Spiel wurden Aufnahmen ausgewählt, auf Ausschnitte gekürzt und neu abgetastet."));
    el("p", "info-klein", t, T("Keine Abbildungen, Tabellen oder Textpassagen aus Lehrbüchern."));
  }
  function zeigeInfo() {
    if (!info) baueInfo();
    auf(info, info.querySelector(".zu"));
    info.querySelector(".huelle-karte").scrollTop = 0;
  }

  /* ------------------------------------------------------------ Titelbildschirm */
  /* Hintergrund: die Aufnahme, ruhig — als Bilder, nicht als lebende Szene (keine Klickfelder, keine
     doppelten IDs, kein Atmen). Die SVG-Ebenen aus kunst.json werden zu Blob-Adressen. */
  function titelBild(eltern) {
    var s = KUNST && KUNST.szenen && KUNST.szenen.aufnahme;
    if (!s || !global.Blob || !global.URL || !global.URL.createObjectURL) return;
    var rahmen = el("div", "titel-bild", eltern), ebenen = el("div", "titel-ebenen", rahmen);
    ["hintergrund", "mittelgrund", "figuren"].forEach(function (n) {
      if (!s[n]) return;
      try {
        var u = global.URL.createObjectURL(new global.Blob([s[n]], { type: "image/svg+xml" }));
        urls.push(u);
        var img = el("img", null, ebenen);
        img.alt = ""; img.decoding = "async"; img.draggable = false;
        img.src = u;
      } catch (e) {}
    });
  }
  /* Unter dem Titel läuft nichts: eine ruhige Kurve, Herrn Baums echte Aufnahme (data/, Ableitung II). */
  function titelKurve(eltern) {
    var id = global.Spiel && global.Spiel.KAPITEL2_EKG && global.Spiel.KAPITEL2_EKG.baum, satz = null;
    (DATEN || []).forEach(function (r) { if (r.id === id) satz = r; });
    if (!satz || !satz.sig) return;
    var fs = satz.sig.fs, w = satz.sig.werte, von = Math.round(1.0 * fs), bis = Math.min(w.length, Math.round(4.6 * fs));
    if (bis - von < 10) return;
    var min = Infinity, max = -Infinity, i;
    for (i = von; i < bis; i++) { if (w[i] < min) min = w[i]; if (w[i] > max) max = w[i]; }
    var B = 600, H = 70, rand = 6, punkte = [];
    for (i = von; i < bis; i++) {
      punkte.push(((i - von) / (bis - von - 1) * B).toFixed(1) + "," +
                  (rand + (max - w[i]) / ((max - min) || 1) * (H - 2 * rand)).toFixed(1));
    }
    var ns = "http://www.w3.org/2000/svg", svg = d.createElementNS(ns, "svg");
    svg.setAttribute("class", "titel-kurve");
    svg.setAttribute("viewBox", "0 0 " + B + " " + H);
    svg.setAttribute("preserveAspectRatio", "none");
    svg.setAttribute("aria-hidden", "true");
    var linie = d.createElementNS(ns, "polyline");
    linie.setAttribute("points", punkte.join(" "));
    svg.appendChild(linie);
    eltern.appendChild(svg);
  }
  function baueTitel() {
    titel = el("div", "titel", d.body);
    titel.id = "titel";
    titelBild(titel);
    var innen = el("div", "titel-innen", titel);
    el("p", "titel-ober", innen, T("EKG-Lernspiel"));
    el("h1", "titel-name", innen, "Nachtdienst");
    titelKurve(innen);
    var reihe = el("div", "titel-knoepfe", innen);
    var stand = global.Spiel && global.Spiel.hatStand ? global.Spiel.hatStand() : null;
    if (stand) {
      knopf("knopf gross haupt", T("Weiterspielen"), reihe, function () { los(false); }, "titel-weiter");
      el("p", "titel-stand", reihe, T("Gespeichert: {zeit} Uhr · {n} in der Befundmappe", { zeit: stand.zeit, n: stand.befunde }));
    }
    knopf("knopf gross" + (stand ? "" : " haupt"), T("Neues Spiel"), reihe,
      function () { if (stand) frageNeu(); else los(true); }, "titel-neu");
    var sp = knopf("knopf gross", null, reihe, zeigeSprache, "titel-sprache");
    el("span", null, sp, T("Sprache"));
    el("span", "schalter", sp, sprachName());
    knopf("knopf gross", T("Info & Quellen"), reihe, zeigeInfo, "titel-info");
    /* Beim ersten Tippen auf einen Knopf: Vollbild anfordern (wo es das gibt). */
    titel.addEventListener("click", function (e) {
      if (vollbildVersucht || !e.target.closest || !e.target.closest("button")) return;
      vollbildVersucht = true;
      vollbild(true);
    }, true);
  }
  function los(neu) {
    if (laeuft) return;
    laeuft = true;
    global.Spiel.start(KUNST, DATEN, neu ? { neu: true } : null);
    if (titel) {
      titel.classList.add("weg");
      global.setTimeout(function () {
        titel.hidden = true;
        var b = titel.querySelector(".titel-bild");
        if (b) b.parentNode.removeChild(b);
        urls.forEach(function (u) { try { global.URL.revokeObjectURL(u); } catch (e) {} });
        urls = [];
      }, 480);
    }
    sperre();
  }

  /* ------------------------------------------------------------ Hochformat */
  function baueQuer() {
    var q = el("div", "quer-hinweis", d.body);
    q.id = "quer-hinweis";
    q.setAttribute("role", "alert");
    q.innerHTML = QUER;
    el("p", "quer-text", q, T("Bitte quer halten"));
    el("p", "quer-klein", q, T("Nachtdienst läuft im Querformat."));
  }

  /* ------------------------------------------------------------ Tastatur
     Fangphase auf window: Die Hülle sieht jede Taste zuerst. Ist ein Fenster der Hülle offen,
     erreicht keine Taste das Spiel dahinter (Ziffern, Enter, H, S); Tab und Enter auf dem
     fokussierten Knopf wirken trotzdem, weil nur die Weitergabe, nicht die Wirkung gestoppt wird. */
  function taste(e) {
    var oben = oberstes();
    if (oben) {
      if (e.key === "Escape" || e.key === "Esc") {
        e.preventDefault();
        if (oben === menue) schliesseMenue();
        else if (oben !== titel) zu(oben);
      }
      e.stopPropagation();
      return;
    }
    if (!laeuft || (e.key !== "Escape" && e.key !== "Esc")) return;
    /* Mappe und Stand haben keinen eigenen Escape — hier schließt er sie. Dialoge und Rätsel regeln es selbst. */
    var mappe = d.querySelector(".mappe.an"), stand = d.querySelector("#stand-hof.an");
    if (mappe || stand) {
      e.preventDefault(); e.stopPropagation();
      if (stand) global.Stand.schliesse(); else global.Mappe.schliesse();
      return;
    }
    if (spielFensterOffen()) return;
    e.preventDefault();
    oeffneMenue();
  }

  /* ------------------------------------------------------------ Start */
  function start(kunst, ekgDaten) {
    KUNST = kunst; DATEN = ekgDaten;
    flaeche = d.getElementById("flaeche");
    masse();
    global.addEventListener("resize", masse);
    global.addEventListener("orientationchange", function () { masse(); global.setTimeout(masse, 300); });
    global.addEventListener("keydown", taste, true);
    d.addEventListener("fullscreenchange", vollbildGewechselt);
    d.addEventListener("webkitfullscreenchange", vollbildGewechselt);

    baueHud();
    baueQuer();

    /* Nach einem Sprachwechsel aus dem Menü geht es ohne Titel weiter, mit offenem Menü. */
    var nach = null;
    try { nach = JSON.parse(lies(NACH_LADEN) || "null"); } catch (e) {}
    merke(NACH_LADEN, null);
    if (nach && nach.ziel === "menue" && global.Spiel.hatStand()) {
      vollbildMerken = !!nach.voll;        /* war Vollbild an, holt „Fortsetzen“ es zurück */
      vollbildVersucht = true;
      los(false);
      oeffneMenue();
      return;
    }
    /* Sonst der Titel; das erste Tippen dort fordert das Vollbild an. */
    baueTitel();
    sperre();
  }

  global.Huelle = {
    start: start, anzeige: anzeige, oeffneMenue: oeffneMenue, schliesseMenue: schliesseMenue,
    zeigeInfo: zeigeInfo, laeuft: function () { return laeuft; }
  };
})(window);
