/* Szenen-Engine: ein Raum aus vier Ebenen, anklickbare Bereiche, weicher Wechsel.
   Läuft auch ohne Grafik — fehlt eine Ebene, wird eine Fläche gezeichnet.      */
(function (global) {
  "use strict";

  var raeume = {}, aktuell = null, buehne = null, hinweisBalken = null;
  var ebenenNamen = ["hintergrund", "mittelgrund", "figuren", "vordergrund"];
  var tiefe = { hintergrund: 2, mittelgrund: 5, figuren: 8, vordergrund: 14 };
  var zeiger = { x: 0, y: 0 }, drift = 0, laeuft = null, gesperrt = false;

  function el(tag, klasse, eltern) {
    var e = document.createElement(tag);
    if (klasse) e.className = klasse;
    if (eltern) eltern.appendChild(e);
    return e;
  }

  function start(behaelter) {
    buehne = behaelter;
    buehne.classList.add("buehne");
    ebenenNamen.forEach(function (n) {
      var d = el("div", "ebene ebene-" + n, buehne);
      d.dataset.ebene = n;
    });
    var svgNS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", "0 0 1600 900");
    svg.setAttribute("preserveAspectRatio", "xMidYMid slice");
    svg.setAttribute("class", "felder");
    buehne.appendChild(svg);
    hinweisBalken = el("div", "feldname", buehne);
    buehne.addEventListener("pointermove", function (e) {
      var r = buehne.getBoundingClientRect();
      zeiger.x = (e.clientX - r.left) / r.width * 2 - 1;
      zeiger.y = (e.clientY - r.top) / r.height * 2 - 1;
    });
    buehne.addEventListener("pointerleave", function () { zeiger.x = 0; zeiger.y = 0; });
    schiebe();
  }

  /* Parallaxe: Zeigerposition plus eine sehr langsame Eigenbewegung,
     damit ein stehendes Bild atmet statt zu stehen. */
  function schiebe() {
    drift += 0.0022;
    var dx = zeiger.x + Math.sin(drift) * 0.22, dy = zeiger.y + Math.cos(drift * 0.7) * 0.14;
    if (buehne) {
      var kinder = buehne.getElementsByClassName("ebene");
      for (var i = 0; i < kinder.length; i++) {
        var t = tiefe[kinder[i].dataset.ebene] || 4;
        kinder[i].style.transform = "translate3d(" + (-dx * t).toFixed(2) + "px," +
                                    (-dy * t * 0.5).toFixed(2) + "px,0)";
      }
    }
    laeuft = global.requestAnimationFrame(schiebe);
  }

  function registriere(name, def) { raeume[name] = def; }

  function felder(def) {
    var svg = buehne.querySelector(".felder");
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var liste = (def.felder || []).concat(def.ausgaenge || []);
    liste.forEach(function (f) {
      if (f.sichtbar && !f.sichtbar()) return;
      var p = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      p.setAttribute("points", f.punkte.map(function (q) { return q[0] + "," + q[1]; }).join(" "));
      if (f.id) p.setAttribute("data-feld", f.id);
      if (f.nach) p.setAttribute("data-nach", f.nach);
      p.setAttribute("class", "feld" + (f.nach ? " ausgang" : "") + (f.erledigt && f.erledigt() ? " erledigt" : ""));
      p.addEventListener("pointerenter", function () {
        hinweisBalken.textContent = f.name;
        hinweisBalken.classList.add("an");
      });
      p.addEventListener("pointerleave", function () { hinweisBalken.classList.remove("an"); });
      p.addEventListener("click", function (ev) {
        ev.stopPropagation();
        if (gesperrt) return;
        hinweisBalken.classList.remove("an");
        if (f.nach) {
          if (f.wenn && !f.wenn()) { if (f.gesperrt) f.gesperrt(); return; }
          zeige(f.nach);
        } else if (f.bei) f.bei();
      });
      svg.appendChild(p);
    });
  }

  function zeige(name, sofort) {
    var def = raeume[name];
    if (!def) return;
    function setzen() {
      aktuell = name;
      ebenenNamen.forEach(function (n) {
        var d = buehne.querySelector(".ebene-" + n);
        var inhalt = def.ebenen && def.ebenen[n];
        d.innerHTML = inhalt || "";
        if (!inhalt && n === "hintergrund") d.style.background = def.ersatzfarbe || "#24323A";
        else if (!inhalt) d.style.background = "transparent";
        else d.style.background = "";
      });
      felder(def);
      if (def.beiBetreten) def.beiBetreten();
      buehne.classList.remove("blende");
    }
    if (sofort) { setzen(); return; }
    buehne.classList.add("blende");
    global.setTimeout(setzen, 400);
  }

  function aktualisiereFelder() { if (aktuell) felder(raeume[aktuell]); }

  var zeigenAus = null;
  function zeigeFelder(ms) {
    var svg = buehne && buehne.querySelector(".felder");
    if (!svg) return;
    svg.classList.add("zeigen");
    global.clearTimeout(zeigenAus);
    zeigenAus = global.setTimeout(function () { svg.classList.remove("zeigen"); }, ms || 1600);
  }

  global.Szene = {
    start: start, zeigeFelder: zeigeFelder, registriere: registriere, zeige: zeige, aktueller: function () { return aktuell; },
    aktualisiere: aktualisiereFelder,
    sperre: function (an) { gesperrt = an; if (buehne) buehne.classList.toggle("stumm", !!an); },
    raum: function (n) { return raeume[n]; }
  };
})(window);
