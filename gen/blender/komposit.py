"""Ligne claire композит: плоский цвет × 3 уровня света (тень/база/свет) + одна линия туши."""
import sys, numpy as np
from PIL import Image, ImageFilter
import os
HIER = os.path.dirname(os.path.abspath(__file__)); WURZEL = os.path.dirname(os.path.dirname(HIER))
D = os.path.join(WURZEL, "bau", "blender", "aufnahme") + os.sep
ZIEL = os.path.join(WURZEL, "art", "szenen", "aufnahme") + os.sep; os.makedirs(ZIEL, exist_ok=True)
hexc = lambda s: np.array([int(s[i:i+2], 16) / 255 for i in (1, 3, 5)], np.float32)
INK = hexc("#1E2A30"); SHADOW_TINT = hexc("#2C5560"); LIGHT_TINT = hexc("#FFF6DC")

def load(n):
    if not os.path.exists(D + n): return None
    return np.asarray(Image.open(D + n).convert("RGB")).astype(np.float32) / 255

def luma(a): return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
def compose(flat_n, amb_n, sun_n, lines_n, out_n, mask_n=None, shadow_t=0.0, sun_t=0.35, ao_n=None, ao_t=0.62):
    flat, amb, sun, lines = load(flat_n), load(amb_n), load(sun_n), load(lines_n)
    h, w = flat.shape[:2]
    if amb is None: amb = np.ones_like(flat)   # без рассеянного прохода: тени нет
    # мягкая тень от рассеянного света: сильно сглажено, крупные формы
    la = luma(amb); lo, hi = np.percentile(la, 1), np.percentile(la, 99); la = np.clip((la - lo) / (hi - lo + 1e-6), 0, 1)
    la = np.asarray(Image.fromarray((la * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(21)).filter(ImageFilter.GaussianBlur(2.0))).astype(np.float32) / 255
    # прямое солнце: жёсткие геометричные полосы от жалюзи, лёгкое сглаживание
    ls = luma(sun); ls = np.clip(ls / (np.percentile(ls, 99.5) + 1e-6), 0, 1)
    ls = np.asarray(Image.fromarray((ls * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))).astype(np.float32) / 255
    # тень относительно локальной освещённости: только там, где заметно темнее окружения (под мебелью, углы)
    shadow = (la < shadow_t).astype(np.float32)[..., None]   # только по-настоящему тёмное: под мебелью, в проёме
    # Kontaktschatten aus dem AO-Pass: eine flache Schattenstufe unter Möbeln und in Ecken
    ao = load(ao_n) if ao_n else None
    if ao is not None:
        lao = luma(ao)
        lao = np.asarray(Image.fromarray((lao * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32) / 255
        shadow = np.maximum(shadow, (lao < ao_t).astype(np.float32)[..., None])
    light = (ls > sun_t).astype(np.float32)[..., None]
    # мягкие края уровней (1 px), чтобы не было лесенки
    def soft(m): return np.asarray(Image.fromarray((m[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32)[..., None] / 255
    shadow, light = soft(shadow), soft(light)
    col = flat
    col = col * (1 - shadow) + (col * 0.86 * (1 - 0.16) + SHADOW_TINT * 0.16 * 0.86) * shadow
    col = col * (1 - light) + (col * (1 - 0.32) + LIGHT_TINT * 0.32) * light
    # линия туши: одна толщина, цвет чернил (не чёрный)
    ink = 1 - (0.2126 * lines[..., 0] + 0.7152 * lines[..., 1] + 0.0722 * lines[..., 2])
    ink = np.clip(ink * 1.3, 0, 1)[..., None]
    col = col * (1 - ink) + INK * ink
    img = Image.fromarray((np.clip(col, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    if mask_n:
        m = np.asarray(Image.open(D + mask_n).convert("L")).astype(np.float32) / 255
        m = (m > 0.5).astype(np.uint8) * 255
        # расширить маску на 2 px, чтобы линия контура осталась на слое
        m = np.asarray(Image.fromarray(m).filter(ImageFilter.MaxFilter(5)))
        a = np.asarray(img); a = a.copy(); a[..., 3] = m; img = Image.fromarray(a)
    img.save(ZIEL + out_n); print("saved", ZIEL + out_n)

compose("pass_flat.png", "pass_amb.png", "pass_sun.png", "pass_lines.png", "vorschau.png", ao_n="pass_ao.png")
if "--layers" in sys.argv:
    compose("pass_flat_bg.png", "pass_ambbg.png", "pass_sunbg.png", "pass_lines_bg.png", "hintergrund.png", ao_n="pass_aobg.png")
    compose("pass_flat.png", "pass_amb.png", "pass_sun.png", "pass_lines.png", "mittelgrund.png", mask_n="mask_mid.png", ao_n="pass_ao.png")
