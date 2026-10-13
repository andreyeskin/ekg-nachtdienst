/* Sprachen: Deutsch ist die Quelle, Englisch und Russisch sind Übersetzungen.

   Der deutsche Satz ist zugleich der Schlüssel. Das hat zwei Vorteile: Der Code
   bleibt lesbar, und fehlt eine Übersetzung, erscheint der deutsche Satz statt
   einer leeren Stelle oder eines Schlüsselnamens.

   T("Zwei Befunde fehlen noch.")                → übersetzt
   T("PQ-Zeit: {ms} ms", { ms: 228 })            → übersetzt und eingesetzt
*/
(function (global) {
  "use strict";

  var SCHLUESSEL = "nachtdienst-sprache";
  var WOERTER = {};                 /* { en: {de-Satz: Übersetzung}, ru: {…} } — alter Weg: der deutsche Satz ist der Schlüssel */
  var TEXTE = {};                   /* { de: {id: Satz}, en: {…}, ru: {…} } — neuer Weg (KONZEPT §6.2): feste IDs je Fall,
                                       text/<sprache>/<fall>.json. T() nimmt beides, bis die alten Sätze migriert sind. */
  var jetzt = "de";
  var SPRACHEN = [
    { kurz: "de", name: "Deutsch" },
    { kurz: "en", name: "English" },
    { kurz: "ru", name: "Русский" }
  ];
  var fehlend = {};                 /* für das Prüfwerkzeug */

  function lade(woerter, texte) { WOERTER = woerter || {}; TEXTE = texte || {}; }
  function istId(text) { return !!(TEXTE.de && TEXTE.de.hasOwnProperty(text)); }

  function erkenne() {
    try {
      var g = global.localStorage.getItem(SCHLUESSEL);
      if (g && istBekannt(g)) return g;
    } catch (e) {}
    var n = (global.navigator && (global.navigator.language || global.navigator.userLanguage)) || "de";
    n = String(n).slice(0, 2).toLowerCase();
    return istBekannt(n) ? n : "de";
  }

  function istBekannt(k) {
    for (var i = 0; i < SPRACHEN.length; i++) if (SPRACHEN[i].kurz === k) return true;
    return false;
  }

  function setze(kurz, ohneNeuzeichnen) {
    if (!istBekannt(kurz)) return;
    jetzt = kurz;
    try { global.localStorage.setItem(SCHLUESSEL, kurz); } catch (e) {}
    if (global.document && global.document.documentElement) {
      global.document.documentElement.setAttribute("lang", kurz);
    }
    uebersetzeHtml();
    if (!ohneNeuzeichnen && global.Spiel && global.Spiel.neuZeichnen) global.Spiel.neuZeichnen();
  }

  /* Platzhalter {name} einsetzen; Zahlen nach Landesart formatieren. */
  function fuelle(text, werte) {
    if (!werte) return text;
    return text.replace(/\{(\w+)\}/g, function (ganz, name) {
      if (!werte.hasOwnProperty(name)) return ganz;
      var w = werte[name];
      return (typeof w === "number") ? zahl(w) : String(w);
    });
  }

  function zahl(n) {
    if (typeof n !== "number" || !isFinite(n)) return String(n);
    if (Math.round(n) === n) {
      /* Ganze Zahlen: Tausendertrennung nur ab fünf Stellen, sonst stört es beim Messen. */
      if (Math.abs(n) < 10000) return String(n);
    }
    try { return n.toLocaleString(jetzt === "ru" ? "ru-RU" : jetzt === "en" ? "en-GB" : "de-AT"); }
    catch (e) { return String(n); }
  }

  function T(text, werte) {
    if (text === null || text === undefined) return "";
    text = String(text);
    if (istId(text)) {                                   /* ID-Weg: erst die Sprache, dann Englisch, dann Deutsch */
      var t = TEXTE[jetzt] && TEXTE[jetzt][text];
      if (!t && jetzt !== "de") { fehlend[text] = true; t = (TEXTE.en && TEXTE.en[text]) || TEXTE.de[text]; }
      return fuelle(t || TEXTE.de[text], werte);
    }
    if (jetzt === "de") return fuelle(text, werte);
    var tisch = WOERTER[jetzt] || {};
    var uebersetzt = tisch[text];
    if (uebersetzt === undefined) {
      fehlend[text] = true;
      uebersetzt = (WOERTER.en && WOERTER.en[text]) || text;   /* erst Englisch, dann Deutsch */
    }
    return fuelle(uebersetzt, werte);
  }

  /* Feste Beschriftungen im HTML: <button data-t>Zurück</button> */
  function uebersetzeHtml(wurzel) {
    var d = global.document;
    if (!d) return;
    var liste = (wurzel || d).querySelectorAll("[data-t]");
    for (var i = 0; i < liste.length; i++) {
      var el = liste[i];
      if (!el.dataset.tQuelle) el.dataset.tQuelle = el.textContent.trim();
      el.textContent = T(el.dataset.tQuelle);
      if (el.dataset.tTitel === undefined && el.title) el.dataset.tTitel = el.title;
      if (el.dataset.tTitel) el.title = T(el.dataset.tTitel);
    }
  }

  function waehler(behaelter, beiWechsel) {
    var d = global.document;
    var s = d.createElement("select");
    s.className = "sprachwahl";
    s.setAttribute("aria-label", "Sprache / Language / Язык");
    SPRACHEN.forEach(function (sp) {
      var o = d.createElement("option");
      o.value = sp.kurz; o.textContent = sp.name;
      if (sp.kurz === jetzt) o.selected = true;
      s.appendChild(o);
    });
    s.addEventListener("change", function () {
      setze(s.value);
      if (beiWechsel) beiWechsel(s.value);
    });
    behaelter.appendChild(s);
    return s;
  }

  global.Sprache = {
    lade: lade, setze: setze, T: T, zahl: zahl, waehler: waehler,
    uebersetzeHtml: uebersetzeHtml,
    jetzt: function () { return jetzt; },
    starte: function (woerter, texte) { lade(woerter, texte); setze(erkenne(), true); },
    fehlende: function () { return Object.keys(fehlend); },
    istId: istId, texte: function () { return TEXTE; },
    SPRACHEN: SPRACHEN
  };
  global.T = T;
})(window);
