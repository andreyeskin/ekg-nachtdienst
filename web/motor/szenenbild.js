/* Motor: Szenenbild — eine illustrierte Nahaufnahme für einen Gesprächsanfang.

   Ein Szenenbild hat keine Klickzonen. Es legt sich mit ruhiger Einblendung über die Bühne
   (dieselbe Lage wie die Bühne: 16:9, mittig, Rest Tinte); der Dialog liegt darüber, das Bild
   bleibt sichtbar. Nach dem Gesprächsabschnitt blendet es wieder aus, und der Raum ist da.
   Die Bilder kommen komprimiert aus kunst.json (gen/kunst.py, SZENENBILDER) — nie aus dem Netz.

     Szenenbild.zeige("aufnahme_tresen", function () { … })   // ruft weiter, sobald es steht
     Szenenbild.verberge()                                      // blendet aus
     Szenenbild.offen()                                         // für Prüfungen                 */
(function (global) {
  "use strict";

  var BILDER = {}, hof = null, bild = null, aktuell = null, aus = null;
  var EINBLENDEN_MS = 650;

  function lade(bilder) { BILDER = bilder || {}; }

  function bau() {
    hof = document.createElement("div");
    hof.className = "szenenbild";
    hof.setAttribute("aria-hidden", "true");
    bild = document.createElement("img");
    bild.alt = ""; bild.draggable = false; bild.decoding = "async";
    hof.appendChild(bild);
    document.body.appendChild(hof);
  }

  function zeige(name, dann) {
    if (!BILDER[name]) { if (dann) dann(); return false; }
    if (!hof) bau();
    global.clearTimeout(aus);
    aktuell = name;
    hof.setAttribute("data-bild", name);
    bild.src = BILDER[name];
    hof.classList.add("da");
    /* Erst das nächste Bild, dann die Einblendung — sonst springt es ohne Übergang. */
    global.requestAnimationFrame(function () {
      global.requestAnimationFrame(function () { hof.classList.add("an"); });
    });
    if (dann) global.setTimeout(dann, EINBLENDEN_MS);
    return true;
  }

  function verberge() {
    if (!hof || !aktuell) return;
    aktuell = null;
    hof.classList.remove("an");
    aus = global.setTimeout(function () {
      if (!aktuell) { hof.classList.remove("da"); hof.removeAttribute("data-bild"); }
    }, 700);
  }

  global.Szenenbild = {
    lade: lade, zeige: zeige, verberge: verberge,
    offen: function () { return !!aktuell; },
    aktuelles: function () { return aktuell; }
  };
})(window);
