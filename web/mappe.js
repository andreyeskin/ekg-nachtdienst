/* Befundmappe: das Inventar. Gesammelt werden keine Schlüssel, sondern Befunde.
   Kernmechanik: zwei Karten nebeneinanderlegen und vergleichen.              */
(function (global) {
  "use strict";

  var Z = null, satzFinden = null, hof = null, gewaehlt = [];

  function bau() {
    hof = document.createElement("div");
    hof.className = "mappe";
    hof.innerHTML =
      '<div class="mappe-innen">' +
      '  <div class="mappe-kopf"><h2>' + T("Befundmappe") + '</h2>' +
      '    <div class="mappe-hilfe">' + T("Zwei Karten antippen und vergleichen — so liest man EKG.") + '</div>' +
      '    <button class="knopf zu" type="button">' + T("Schließen") + '</button></div>' +
      '  <div class="mappe-karten"></div>' +
      '  <div class="mappe-fuss"><button class="knopf vergleich" type="button" disabled>' + T("Vergleichen") + '</button></div>' +
      '  <div class="mappe-vergleich"></div>' +
      '</div>';
    document.body.appendChild(hof);
    hof.querySelector(".zu").addEventListener("click", schliesse);
    hof.querySelector(".vergleich").addEventListener("click", vergleiche);
  }

  /* Karten aus dem Fallmotor tragen Text-IDs und ihre Platzhalterwerte (k.vars); ältere Karten den fertigen Satz. */
  function karteHtml(k, i) {
    return '<article class="karte" data-i="' + i + '" tabindex="0">' +
      '<div class="karte-kopf"><span class="karte-zeit">' + (k.zeit || "") + '</span>' +
      '<h3>' + T(k.titel, k.vars) + '</h3></div>' +
      (k.ekg ? '<canvas class="karte-ekg" height="110"></canvas>' : '<div class="karte-symbol">' + (k.symbol || "") + '</div>') +
      '<p>' + T(k.text, k.vars) + '</p></article>';
  }

  function maleKarten() {
    var feld = hof.querySelector(".mappe-karten");
    if (!Z.befunde.length) {
      feld.innerHTML = '<p class="leer">' + T("Noch nichts gesammelt. Sieh dich um, miss nach, frag jemanden.") + '</p>';
      return;
    }
    feld.innerHTML = Z.befunde.map(karteHtml).join("");
    Array.prototype.forEach.call(feld.getElementsByClassName("karte"), function (el) {
      var i = +el.dataset.i, k = Z.befunde[i];
      if (k.ekg) maleEkg(el.querySelector(".karte-ekg"), k.ekg);
      el.addEventListener("click", function () { waehle(i, el); });
      el.addEventListener("keydown", function (e) { if (e.key === "Enter") waehle(i, el); });
      if (gewaehlt.indexOf(i) >= 0) el.classList.add("gewaehlt");
    });
  }

  function maleEkg(leinwand, e) {
    var satz = satzFinden(e.satz);
    if (!satz || !leinwand) return;
    leinwand.style.width = "100%";
    var s = global.EKG.Streifen(leinwand, {
      werte: satz.sig.werte, fs: satz.sig.fs, mmProS: e.mmProS || 25,
      von: e.von || 0, dauer: e.dauer || 4, kalibrierung: e.eich !== false
    });
    s.zeichne();
    global.setTimeout(s.zeichne, 60);
    return s;
  }

  function waehle(i, el) {
    var p = gewaehlt.indexOf(i);
    if (p >= 0) { gewaehlt.splice(p, 1); el.classList.remove("gewaehlt"); }
    else {
      if (gewaehlt.length === 2) {
        var weg = gewaehlt.shift();
        var alt = hof.querySelector('.karte[data-i="' + weg + '"]');
        if (alt) alt.classList.remove("gewaehlt");
      }
      gewaehlt.push(i); el.classList.add("gewaehlt");
    }
    hof.querySelector(".vergleich").disabled = gewaehlt.length !== 2;
    hof.querySelector(".mappe-vergleich").classList.remove("an");
  }

  function vergleiche() {
    if (gewaehlt.length !== 2) return;
    var a = Z.befunde[gewaehlt[0]], b = Z.befunde[gewaehlt[1]];
    var feld = hof.querySelector(".mappe-vergleich");
    var f = frage(a, b);
    feld.innerHTML =
      '<div class="verg-kopf"><h3>' + T(a.titel, a.vars) + '</h3><h3>' + T(b.titel, b.vars) + '</h3></div>' +
      '<div class="verg-paar">' +
      '  <div class="verg-eins"><canvas height="150"></canvas><p>' + T(a.text, a.vars) + '</p></div>' +
      '  <div class="verg-eins"><canvas height="150"></canvas><p>' + T(b.text, b.vars) + '</p></div>' +
      '</div>' +
      '<p class="verg-frage">' + (f ? T(f.text, f.vars) : T("Was ist anders? Sieh zuerst auf den Rhythmus, dann auf die Zeiten.")) + '</p>';
    var lw = feld.getElementsByTagName("canvas");
    [a, b].forEach(function (k, i) {
      if (k.ekg) maleEkg(lw[i], k.ekg);
      else lw[i].style.display = "none";
    });
    feld.classList.add("an");
    feld.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  /* Die Vergleichsfrage gehört der Karte, die sie stellt — samt ihren Platzhalterwerten; gemessene Zahlen der
     anderen Karte (hf, pq …) liegen in deren vars und werden dazugelegt. */
  function frage(a, b) {
    var von = null, text = null;
    if (a.vergleich && a.vergleich[b.id]) { von = a; text = a.vergleich[b.id]; }
    else if (b.vergleich && b.vergleich[a.id]) { von = b; text = b.vergleich[a.id]; }
    if (!von) return null;
    var vars = {}, k, quelle = von === a ? b : a;
    for (k in (quelle.vars || {})) if (quelle.vars.hasOwnProperty(k)) vars[k] = quelle.vars[k];
    for (k in (von.vars || {})) if (von.vars.hasOwnProperty(k)) vars[k] = von.vars[k];
    if (global.Spiel && global.Spiel.zustand) {
      var w = global.Spiel.zustand.werte;
      for (k in w) if (w.hasOwnProperty(k) && typeof w[k] !== "object") vars[k] = w[k];
    }
    return { text: text, vars: vars };
  }

  function oeffne() {
    if (!hof) bau();
    gewaehlt = [];
    hof.querySelector(".vergleich").disabled = true;
    hof.querySelector(".mappe-vergleich").classList.remove("an");
    maleKarten();
    hof.classList.add("an");
    if (global.Szene) global.Szene.sperre(true);
  }

  function schliesse() {
    if (hof) hof.classList.remove("an");
    if (global.Szene) global.Szene.sperre(false);
  }

  function fuegeHinzu(k) {
    if (hat(k.id)) return false;
    Z.befunde.push(k);
    if (global.Spiel && global.Spiel.melde) {
      global.Spiel.melde(T("Befund in der Mappe: {was}", { was: T(k.titel, k.vars) }));
    }
    if (global.Spiel && global.Spiel.sichere) global.Spiel.sichere();
    if (global.Spiel && global.Spiel.zaehlerAuffrischen) global.Spiel.zaehlerAuffrischen();
    return true;
  }

  function hat(id) {
    for (var i = 0; i < Z.befunde.length; i++) if (Z.befunde[i].id === id) return true;
    return false;
  }

  global.Mappe = {
    start: function (zustand, finder) { Z = zustand; satzFinden = finder; },
    oeffne: oeffne, schliesse: schliesse, fuegeHinzu: fuegeHinzu, hat: hat,
    anzahl: function () { return Z ? Z.befunde.length : 0; }
  };
})(window);
