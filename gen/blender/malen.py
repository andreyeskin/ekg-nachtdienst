#!/usr/bin/env python3
"""malen.py — «дорисовать» 3D-черновик из Blender через fal.ai (Flux).

Два режима:
  kontext  — fal-ai/flux-pro/kontext: берёт наш рендер и перерисовывает его по инструкции,
             сохраняя планировку и предметы. Самый простой и дешёвый путь (≈ $0.04/картинка).
  general  — fal-ai/flux-general: генерация с ControlNet (глубина/контуры из нашего рендера)
             и опциональными LoRA-стилями (≈ $0.075/мегапиксель).

Ключ берётся из переменной окружения FAL_KEY (секрет облачного окружения, не из чата).
Без ключа скрипт работает как --dry-run: печатает, что отправил бы.

Примеры:
  python3 malen.py kontext --image render.png --style stil_riso.txt --seed 7 --out out.png
  python3 malen.py general --image render.png --depth depth.png --prompt "..." --out out.png
"""
import argparse, json, os, sys, time, urllib.request

STYLE_PRESETS = {
    # стилевые фразы; правятся под утверждённое направление
    "print_night": "hand-pulled screen print illustration, three ink colours on cream paper, coarse halftone only in shadows, "
                   "paper grain, slight misregistration, bold simplified shapes, one warm amber light source, navy and teal shadows, "
                   "no text, no letters, no ECG waveforms on screens, no people",
    "gouache_noir": "moody gouache painting, limited palette navy teal cream amber, visible brush texture, cinematic single light, "
                    "no text, no letters, no ECG waveforms on screens, no people",
}

def load_style(arg):
    if not arg: return ""
    if os.path.exists(arg): return open(arg, encoding="utf-8").read().strip()
    return STYLE_PRESETS.get(arg, arg)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["kontext", "general"])
    ap.add_argument("--image", required=True, help="наш рендер (PNG/JPG), структура сцены")
    ap.add_argument("--depth", help="карта глубины из Blender (для general, ControlNet depth)")
    ap.add_argument("--prompt", default="", help="описание сцены")
    ap.add_argument("--style", default="print_night", help="пресет или файл со стилевой фразой")
    ap.add_argument("--negative", default="text, letters, numbers, signage, watermark, ECG trace, people, photo-realistic, blurry")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--steps", type=int, default=28)
    ap.add_argument("--guidance", type=float, default=3.5)
    ap.add_argument("--strength", type=float, default=0.65, help="general: сила reference/img2img 0..1")
    ap.add_argument("--control-scale", type=float, default=0.7, help="general: вес ControlNet 0..1")
    ap.add_argument("--lora", action="append", default=[], help="general: URL LoRA (можно несколько), формат url[:scale]")
    ap.add_argument("--size", default="landscape_16_9")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    key = os.environ.get("FAL_KEY")
    dry = a.dry_run or not key
    style = load_style(a.style)
    full_prompt = (a.prompt + ". " if a.prompt else "") + style

    try:
        import fal_client
    except ImportError:
        print("pip install fal-client", file=sys.stderr); sys.exit(2)

    if a.mode == "kontext":
        endpoint = "fal-ai/flux-pro/kontext"
        payload = {
            "prompt": "Repaint this exact scene, keep the layout, furniture, camera and light positions unchanged. Style: " + full_prompt,
            "image_url": None if dry else fal_client.encode_file(a.image),
            "seed": a.seed, "guidance_scale": a.guidance, "num_inference_steps": a.steps,
            "output_format": "png",
        }
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
        shown = {k: (v if not (isinstance(v, str) and v.startswith("data:")) else "<data-uri>") for k, v in payload.items()}
        print("DRY RUN (нет FAL_KEY)" if not key else "DRY RUN", endpoint); print(json.dumps(shown, ensure_ascii=False, indent=1)); return

    t = time.time()
    result = fal_client.subscribe(endpoint, arguments=payload, with_logs=False)
    imgs = result.get("images") or []
    if not imgs: print("Нет изображений в ответе:", json.dumps(result)[:500]); sys.exit(1)
    urllib.request.urlretrieve(imgs[0]["url"], a.out)
    print(f"saved {a.out} ({imgs[0].get('width')}x{imgs[0].get('height')}) seed={result.get('seed', a.seed)} {time.time()-t:.0f}s")

if __name__ == "__main__":
    main()
