#!/usr/bin/env python3
"""malen.py — eine Blender-Vorlage von einem Bildgenerator ausmalen lassen. Blender rechnet das Licht, hier wird nur gemalt.

Modi:
  kontext  fal-ai/flux-pro/kontext: zeichnet unseren Render nach Anweisung um, Grundriss und Dinge bleiben (≈ 0,04 $/Bild);
           --max nimmt kontext/max (≈ 0,08 $). Mit --referenz BILD (ein- oder mehrmals) läuft kontext/max/multi: Vorlage +
           weitere Bilder (Stilreferenz, Porträts). Erfahrung aus der Probe am 11.10.2026: einbildig hält Kontext Aufbau und
           Licht, malt aber plastisch mit Mannequin-Gesichtern; multi mit dem Referenzbild malt das Referenzbild nach und
           verwirft die Vorlage; multi mit den Porträts trifft die Gesichter, verliert aber Mappe, Lampeninsel und Streifen.
  general  fal-ai/flux-general: Erzeugung mit ControlNet (Tiefe/Kanten aus dem Render) und optionalen LoRA-Stilen.
  openai   OpenAI GPT Image, Bildbearbeitung mit mehreren Eingabebildern (POST /v1/images/edits, multipart, Feld image[]
           mehrfach; Antwort data[0].b64_json; Dokumentation gelesen am 11.10.2026): Vorlage + Porträts (--portrait, mehrfach,
           von links nach rechts im Bild) + Stilreferenz (--referenz). Standardmodell gpt-image-2.5-sunburst (das Modell der
           Dokumentation „für Bearbeitungen mit hoher Treue"); weitere: gpt-image-2.5-flare, gpt-image-2, gpt-image-1.5,
           gpt-image-1, gpt-image-1-mini. Größe: 1024x1024 / 1536x1024 / 1024x1536 / auto; die Modelle ab gpt-image-2 nehmen
           auch BREITExHÖHE (beide Vielfache von 16, Seitenverhältnis 1:3..3:1, höchstens 3840x2160) — Standard hier 1536x864
           (16:9). quality low/medium/high/auto, bei 2.5 auch xhigh/max. input_fidelity (low/high) gibt es nur bei gpt-image-1
           und 1.5; die Modelle ab 2 lesen jede Eingabe in hoher Treue, der Parameter bleibt dort weg.
           Ergebnis: art/szenenbilder/<name>/openai_<modell>_<zeit>.png + .json (Modell, Prompt, Eingaben, Datum, Verbrauch).

Schlüssel: fal aus FAL_KEY oder vom Proxy der Cloud-Umgebung (*.fal.run); OpenAI aus OPENAI_API_KEY oder vom Proxy
(Netzwerk-Secret für api.openai.com, Pfad /v1/images/; abschalten mit OPENAI_PROXY_AUTH=0). Mit --dry-run wird nichts
gesendet, die Anfrage wird nur gezeigt.

Beispiele:
  python3 gen/blender/malen.py kontext --image art/szenenbilder/aufnahme_tresen/vorlage.png --style gen/blender/stil/szenenbild.txt --seed 7 --out bau/blender/szenenbilder/aufnahme_tresen/kontext_s7.png
  python3 gen/blender/malen.py kontext --image …/vorlage.png --referenz art/referenz/chatgpt_aufnahme_marlene.png --style … --out …
  python3 gen/blender/malen.py openai --image art/szenenbilder/aufnahme_tresen/vorlage.png \\
          --portrait art/portraits/marlene.png --portrait art/portraits/herr_k.png \\
          --referenz art/referenz/chatgpt_aufnahme_marlene.png --dry-run
"""
import argparse
import base64
import datetime
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))

STYLE_PRESETS = {
    # stilphrasen; werden unter die freigegebene Richtung angepasst
    "print_night": "hand-pulled screen print illustration, three ink colours on cream paper, coarse halftone only in shadows, "
                   "paper grain, slight misregistration, bold simplified shapes, one warm amber light source, navy and teal shadows, "
                   "no text, no letters, no ECG waveforms on screens, no people",
    "gouache_noir": "moody gouache painting, limited palette navy teal cream amber, visible brush texture, cinematic single light, "
                    "no text, no letters, no ECG waveforms on screens, no people",
}
STIL_SZENENBILD = os.path.join(HIER, "stil", "szenenbild.txt")

OPENAI_URL = "https://api.openai.com/v1/images/edits"
OPENAI_MODELLE = ["gpt-image-2.5-sunburst", "gpt-image-2.5-flare", "gpt-image-2", "gpt-image-1.5", "gpt-image-1", "gpt-image-1-mini", "chatgpt-image-latest"]
OPENAI_TREUE = {"gpt-image-1", "gpt-image-1.5", "gpt-image-1-mini"}      # nur diese kennen input_fidelity


def load_style(arg):
    if not arg: return ""
    if os.path.exists(arg): return open(arg, encoding="utf-8").read().strip()
    return STYLE_PRESETS.get(arg, arg)


def rel(p): return os.path.relpath(os.path.abspath(p), WURZEL)


# ---------------------------------------------------------------- OpenAI: multipart ohne weitere Abhängigkeiten
def multipart(felder, dateien):
    """felder: [(name, wert)], dateien: [(feldname, pfad)] -> (body, content-type)."""
    grenze = "----nachtdienst" + uuid.uuid4().hex; teile = []
    for name, wert in felder:
        teile.append(f"--{grenze}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{wert}\r\n".encode("utf-8"))
    for name, pfad in dateien:
        typ = mimetypes.guess_type(pfad)[0] or "application/octet-stream"
        kopf = f"--{grenze}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{os.path.basename(pfad)}\"\r\nContent-Type: {typ}\r\n\r\n"
        teile.append(kopf.encode("utf-8") + open(pfad, "rb").read() + b"\r\n")
    teile.append(f"--{grenze}--\r\n".encode("utf-8"))
    return b"".join(teile), f"multipart/form-data; boundary={grenze}"


def openai_prompt(a, style, n_portraits, n_referenz):
    """Erklärt dem Modell die Reihenfolge der Eingaben, dann die Stilphrase."""
    k = 1; teile = [f"Image {k} is the scene template: a flat rendered layout of the scene with the correct light and shadow, computed by a renderer."]
    if n_portraits:
        if n_portraits == 1: teile.append(f"Image {k + 1} is the portrait of the person in the scene: draw exactly this person (same face, hair, glasses, skin and clothing colours).")
        else: teile.append(f"Images {k + 1} to {k + n_portraits} are portraits of the people in the scene, in the order they appear from left to right: draw exactly these people (same faces, hair, glasses, skin and clothing colours).")
        k += n_portraits
    if n_referenz:
        teile.append((f"Image {k + 1} is" if n_referenz == 1 else f"Images {k + 1} to {k + n_referenz} are") + " a style reference: match its drawing style, line and colour treatment, but not its layout and not its light.")
    if a.prompt: teile.append(a.prompt)
    teile.append(style)
    return " ".join(teile)


def openai(a):
    key = os.environ.get("OPENAI_API_KEY")
    if not key and os.environ.get("OPENAI_PROXY_AUTH", "1") == "1" and not a.dry_run:
        # Wie bei fal: Den Schlüssel setzt der Proxy der Cloud-Umgebung (Secret für api.openai.com,
        # Pfad /v1/images/). Der Client braucht nur irgendeinen Authorization-Kopf.
        key = "proxy-injected"
    dry = a.dry_run or not key
    style = load_style(a.style or STIL_SZENENBILD)
    portraits = [p for p in (a.portrait or [])]; referenz = [p for p in (a.referenz or [])]
    for p in [a.image] + portraits + referenz:
        if not os.path.exists(p): sys.exit(f"Eingabe fehlt: {p}")
    prompt = openai_prompt(a, style, len(portraits), len(referenz))
    felder = [("model", a.model), ("prompt", prompt), ("n", str(a.n)), ("size", a.size), ("quality", a.quality), ("output_format", "png")]
    if a.model in OPENAI_TREUE and a.input_fidelity: felder.append(("input_fidelity", a.input_fidelity))
    if a.background: felder.append(("background", a.background))
    dateien = [("image[]", p) for p in [a.image] + portraits + referenz]
    name = a.name or os.path.basename(os.path.dirname(os.path.abspath(a.image))) or "szenenbild"
    ziel_dir = os.path.join(WURZEL, "art", "szenenbilder", name); kennung = f"openai_{a.model}_{datetime.datetime.now().strftime('%Y%m%d-%H%M')}"
    bericht = {"modus": "openai", "endpunkt": OPENAI_URL, "modell": a.model, "prompt": prompt,
               "parameter": {k: v for k, v in felder if k not in ("prompt", "model")},
               "eingaben": [{"feld": f, "datei": rel(p), "bytes": os.path.getsize(p)} for f, p in dateien],
               "stil": rel(a.style) if a.style and os.path.exists(a.style) else rel(STIL_SZENENBILD),
               "datum": datetime.datetime.now().isoformat(timespec="minutes")}
    if dry:
        print("DRY RUN" + ("" if key else " (kein OPENAI_API_KEY)"), "POST", OPENAI_URL)
        print(json.dumps(bericht, ensure_ascii=False, indent=1))
        print(f"-> {rel(os.path.join(ziel_dir, kennung + '.png'))} (+ .json)"); return
    body, typ = multipart(felder, dateien)
    req = urllib.request.Request(OPENAI_URL, data=body, method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": typ, "Content-Length": str(len(body))})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=a.timeout) as r: antwort = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print("OpenAI antwortete", e.code, e.read().decode("utf-8", "replace")[:1500]); sys.exit(1)
    bilder = antwort.get("data") or []
    if not bilder or not bilder[0].get("b64_json"):
        print("Kein Bild in der Antwort:", json.dumps(antwort)[:800]); sys.exit(1)
    os.makedirs(ziel_dir, exist_ok=True); ausgaben = []
    for i, b in enumerate(bilder):
        pfad = os.path.join(ziel_dir, kennung + (f"_{i + 1}" if len(bilder) > 1 else "") + ".png")
        open(pfad, "wb").write(base64.b64decode(b["b64_json"])); ausgaben.append(rel(pfad))
        if b.get("revised_prompt"): bericht.setdefault("revised_prompt", []).append(b["revised_prompt"])
    bericht.update({"ausgaben": ausgaben, "verbrauch": antwort.get("usage"), "antwort": {k: antwort.get(k) for k in ("size", "quality", "output_format", "background", "created")},
                    "dauer_s": round(time.time() - t)})
    json.dump(bericht, open(os.path.join(ziel_dir, kennung + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("gespeichert", *ausgaben, f"({bericht['dauer_s']} s, usage {json.dumps(antwort.get('usage'))})")


# ---------------------------------------------------------------- fal.ai
def fal(a):
    key = os.environ.get("FAL_KEY")
    if not key and os.environ.get("FAL_PROXY_AUTH", "1") == "1" and not a.dry_run:
        # Der Proxy der Cloud-Umgebung („Netzwerk-Secret") ersetzt den Schlüssel: der Client braucht irgendeinen
        # Authorization-Kopf, der Proxy setzt für erlaubte Hosts den echten ein.
        os.environ["FAL_KEY"] = "proxy-injected"; key = "proxy"
    dry = a.dry_run or not key
    style = load_style(a.style or "print_night")
    full_prompt = (a.prompt + ". " if a.prompt else "") + style
    if not a.out: sys.exit("--out fehlt")
    try:
        import fal_client
    except ImportError:
        print("pip install fal-client", file=sys.stderr); sys.exit(2)

    if a.mode == "kontext":
        prompt = "Repaint this exact scene, keep the layout, furniture, camera and light positions unchanged. Style: " + full_prompt
        basis = "fal-ai/flux-pro/kontext" + ("/max" if a.max else "")
        if a.referenz:
            endpoint = basis + "/multi" if a.max else "fal-ai/flux-pro/kontext/max/multi"   # mehrere Bilder gibt es nur bei max
            prompt = ("The first image is the scene to paint. " + ("The second image is" if len(a.referenz) == 1 else "The following images are")
                      + " a style reference: match its drawing style, line and colour treatment, but not its layout and not its light. " + prompt)
            payload = {"prompt": prompt, "image_urls": None if dry else [fal_client.encode_file(p) for p in [a.image] + a.referenz]}
        else:
            endpoint = basis
            payload = {"prompt": prompt, "image_url": None if dry else fal_client.encode_file(a.image)}
        payload.update({"seed": a.seed, "guidance_scale": a.guidance, "num_inference_steps": a.steps, "output_format": "png", "safety_tolerance": "2"})
        if a.aspect: payload["aspect_ratio"] = a.aspect
    else:
        endpoint = "fal-ai/flux-general"
        payload = {
            "prompt": full_prompt, "negative_prompt": a.negative,
            "seed": a.seed, "num_inference_steps": a.steps, "guidance_scale": a.guidance,
            "image_size": a.size, "num_images": 1, "output_format": "png",
            "reference_image_url": None if dry else fal_client.encode_file(a.image),
            "reference_strength": a.strength,
        }
        if a.depth:
            payload["controlnets"] = [{
                "path": "InstantX/FLUX.1-dev-Controlnet-Union",   # union: depth / canny / pose
                "control_image_url": None if dry else fal_client.encode_file(a.depth),
                "conditioning_scale": a.control_scale, "control_mode": "depth",
            }]
        if a.lora:
            payload["loras"] = []
            for l in a.lora:
                url, _, scale = l.partition("|"); payload["loras"].append({"path": url, "scale": float(scale or 1.0)})

    if dry:
        shown = {k: ("<data-uri>" if isinstance(v, str) and v.startswith("data:") else (["<data-uri>"] * len(v) if isinstance(v, list) and v and str(v[0]).startswith("data:") else v))
                 for k, v in payload.items()}
        print("DRY RUN" + ("" if key else " (kein FAL_KEY)"), endpoint); print(json.dumps(shown, ensure_ascii=False, indent=1)); return

    t = time.time()
    result = fal_client.subscribe(endpoint, arguments=payload, with_logs=False)
    imgs = result.get("images") or []
    if isinstance(result, dict) and result.get("detail") and not imgs:
        print("fal.ai antwortete mit einem Fehler:", result.get("detail")); sys.exit(1)
    if not imgs: print("Kein Bild in der Antwort:", json.dumps(result)[:500]); sys.exit(1)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    urllib.request.urlretrieve(imgs[0]["url"], a.out)
    json.dump({"modus": a.mode, "endpunkt": endpoint, "prompt": payload["prompt"], "seed": result.get("seed", a.seed), "guidance": a.guidance,
               "steps": a.steps, "eingaben": [rel(p) for p in [a.image] + (a.referenz or [])], "stil": rel(a.style) if a.style and os.path.exists(a.style) else a.style,
               "datum": datetime.datetime.now().isoformat(timespec="minutes"), "ausgabe": rel(a.out)},
              open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"saved {a.out} ({imgs[0].get('width')}x{imgs[0].get('height')}) seed={result.get('seed', a.seed)} {time.time()-t:.0f}s")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["kontext", "general", "openai"])
    ap.add_argument("--image", required=True, help="unser Render (PNG/JPG): die Vorlage mit Aufbau und Licht")
    ap.add_argument("--depth", help="Tiefenkarte aus Blender (general, ControlNet depth)")
    ap.add_argument("--prompt", default="", help="zusätzliche Beschreibung der Szene")
    ap.add_argument("--style", default=None, help="Voreinstellung oder Datei mit der Stilphrase (openai: stil/szenenbild.txt, fal: print_night)")
    ap.add_argument("--negative", default="text, letters, numbers, signage, watermark, ECG trace, people, photo-realistic, blurry")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--steps", type=int, default=28)
    ap.add_argument("--guidance", type=float, default=3.5)
    ap.add_argument("--aspect", default=None, help="kontext: aspect_ratio, z. B. 16:9")
    ap.add_argument("--max", action="store_true", help="kontext: Endpunkt kontext/max (teurer, hält Stil und Anweisung genauer)")
    ap.add_argument("--strength", type=float, default=0.65, help="general: Stärke reference/img2img 0..1")
    ap.add_argument("--control-scale", type=float, default=0.7, help="general: Gewicht ControlNet 0..1")
    ap.add_argument("--lora", action="append", default=[], help="general: LoRA-URL (mehrfach), Form url|scale")
    ap.add_argument("--size", default=None, help="general: image_size (landscape_16_9); openai: size (1536x864)")
    ap.add_argument("--referenz", action="append", help="Stilreferenz-Bild (kontext: max/multi; openai: letztes Eingabebild), mehrfach möglich")
    ap.add_argument("--portrait", action="append", help="openai: Porträt einer Person im Bild (von links nach rechts), mehrfach")
    ap.add_argument("--model", default=OPENAI_MODELLE[0], help="openai: " + ", ".join(OPENAI_MODELLE))
    ap.add_argument("--quality", default="high", help="openai: low/medium/high/auto, bei gpt-image-2.5 auch xhigh/max")
    ap.add_argument("--input-fidelity", default="high", help="openai: nur gpt-image-1/1.5 (low/high); sonst weggelassen")
    ap.add_argument("--background", default=None, help="openai: transparent/opaque/auto")
    ap.add_argument("--n", type=int, default=1, help="openai: Anzahl Bilder")
    ap.add_argument("--name", help="openai: Zielordner art/szenenbilder/<name>/ (Standard: Ordnername der Vorlage)")
    ap.add_argument("--timeout", type=int, default=600, help="openai: Sekunden")
    ap.add_argument("--out", help="fal: Zieldatei (PNG)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.mode == "openai":
        a.size = a.size or "1536x864"; openai(a)
    else:
        a.size = a.size or "landscape_16_9"; fal(a)


if __name__ == "__main__":
    main()
