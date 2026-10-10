/* Findet Chromium, egal in welcher Sitzung dieses Repository ausgecheckt ist.
   Reihenfolge: playwright-core aus node_modules → irgendein vorinstalliertes
   Chromium unter /opt/pw-browsers → der von Playwright mitgelieferte Pfad.    */
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

function suchePlaywright() {
  const kandidaten = [];
  let d = process.cwd();
  for (let i = 0; i < 4; i++) { kandidaten.push(path.join(d, "node_modules")); d = path.dirname(d); }
  kandidaten.push("/home/claude/patho1/node_modules");      // gewachsene Umgebung
  for (const k of kandidaten) {
    const p = path.join(k, "playwright-core", "index.mjs");
    if (fs.existsSync(p)) return p;
  }
  return null;
}

function sucheChromium() {
  if (process.env.CHROMIUM) return process.env.CHROMIUM;
  const wurzeln = [process.env.PLAYWRIGHT_BROWSERS_PATH, "/opt/pw-browsers"].filter(Boolean);
  for (const w of wurzeln) {
    if (!fs.existsSync(w)) continue;
    const direkt = path.join(w, "chromium");
    if (fs.existsSync(direkt) && fs.statSync(direkt).isFile()) return direkt;
    for (const e of fs.readdirSync(w)) {
      for (const unter of ["chrome-linux/chrome", "chrome-linux/headless_shell"]) {
        const p = path.join(w, e, unter);
        if (fs.existsSync(p)) return p;
      }
    }
  }
  return null;                                              // Playwright nimmt seinen eigenen
}

export async function starteBrowser(optionen = {}) {
  let pfad = suchePlaywright();
  if (!pfad) {
    console.log("playwright-core fehlt — wird installiert …");
    execSync("npm install --no-save playwright-core", { stdio: "inherit" });
    pfad = suchePlaywright();
    if (!pfad) throw new Error("playwright-core ließ sich nicht installieren.");
  }
  const { chromium } = await import(pfad);
  const exe = sucheChromium();
  return chromium.launch(Object.assign(
    { args: ["--no-sandbox"] },
    exe ? { executablePath: exe } : {},
    optionen
  ));
}
