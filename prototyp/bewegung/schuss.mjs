/* Prüft den Bewegungs-Prototyp: lädt ohne Fehler, Ereignisse laufen, Schnappschüsse.
   node prototyp/bewegung/schuss.mjs bau/prototyp_bewegung_de.html bau/prototyp_schuss */
import { starteBrowser } from "../../tools/browser.mjs";
import fs from "node:fs";
import path from "node:path";

const datei = path.resolve(process.argv[2]), ziel = path.resolve(process.argv[3] || "bau/prototyp_schuss");
fs.mkdirSync(ziel, { recursive: true });
const browser = await starteBrowser();
const fehler = [];
async function lauf(name, opt, fn) {
  const kontext = await browser.newContext(opt);
  const seite = await kontext.newPage();
  seite.on("pageerror", (e) => fehler.push(name + ": " + e.message));
  seite.on("console", (m) => { if (m.type() === "error") fehler.push(name + ": " + m.text()); });
  await seite.goto("file://" + datei);
  await seite.waitForTimeout(600);
  await fn(seite);
  await kontext.close();
}
await lauf("normal", { viewport: { width: 1340, height: 900 } }, async (s) => {
  await s.screenshot({ path: path.join(ziel, "1_start.png") });
  await s.click("[data-ereignis=handy]"); await s.waitForTimeout(700);
  await s.screenshot({ path: path.join(ziel, "2_handy.png"), clip: { x: 900, y: 150, width: 440, height: 520 } });
  await s.click("#ekg"); await s.waitForTimeout(5200);
  await s.screenshot({ path: path.join(ziel, "3_ekg.png"), clip: { x: 520, y: 220, width: 300, height: 260 } });
  await s.click("[data-ereignis=vorbei]"); await s.waitForTimeout(1300);
  await s.screenshot({ path: path.join(ziel, "4_vorbei.png") });
  await s.fill("#zeit", "470"); await s.dispatchEvent("#zeit", "input"); await s.waitForTimeout(400);
  await s.screenshot({ path: path.join(ziel, "5_0750.png") });
  const n = await s.evaluate(() => document.querySelectorAll(".lider").length);
  if (n !== 2) fehler.push("Lider: " + n);
});
await lauf("ruhig", { viewport: { width: 1024, height: 768 }, reducedMotion: "reduce" }, async (s) => {
  const r = await s.evaluate(() => Leben.ruhig());
  if (!r) fehler.push("reduced motion nicht erkannt");
  await s.screenshot({ path: path.join(ziel, "6_ipad_ruhig.png") });
});
await browser.close();
console.log(fehler.length ? "FEHLER:\n" + fehler.join("\n") : "Prototyp: keine Fehler.");
