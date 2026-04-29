#!/usr/bin/env python3
"""generate_og_images.py
Generates 1200x630 Open Graph images for every live Aesop course.
Reads course-registry.json (icon, accent, status) and courses-data.json
(name, description, category, tier, module count).
Output: assets/og/courses/{course-id}.png

Called by .github/workflows/generate-og-images.yml
"""

import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Paths ─────────────────────────────────────────────────────────────
ROOT          = Path(__file__).parent.parent.parent
REGISTRY_PATH = ROOT / "ai-academy" / "modules" / "course-registry.json"
DATA_PATH     = ROOT / "ai-academy" / "modules" / "courses-data.json"
OUT_DIR       = ROOT / "assets" / "og" / "courses"

W, H = 1200, 630

# ── Brand palette ─────────────────────────────────────────────────────
NAVY      = (13,  27,  42)
NAVY_DEEP = ( 8,  16,  26)
GOLD      = (201, 160,  90)
GOLD_DIM  = (160, 122,  65)
WHITE     = (255, 255, 255)

# ── Font paths — Liberation guaranteed on ubuntu-latest ───────────────
BOLD_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSans-Bold.ttf",
]
REG_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/opentype/noto/NotoSans-Regular.ttf",
]


def load_font(paths, size):
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def hex_to_rgb(h):
    h = h.lstrip("#")
    try:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        return GOLD


def wrap_text(text, font, max_w, draw):
    """Break text into lines that fit within max_w pixels."""
    words = text.split()
    lines, current = [], []
    for word in words:
        probe = " ".join(current + [word])
        bbox  = draw.textbbox((0, 0), probe, font=font)
        if bbox[2] - bbox[0] <= max_w or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def generate(course_id, course, reg):
    name      = course.get("name") or reg.get("title", course_id)
    category  = course.get("category", "")
    tier      = course.get("tier", "")
    mod_count = len(course.get("modules", [])) or reg.get("modCount", 0)
    accent    = hex_to_rgb(reg.get("accent", "#c9a05a"))

    # ── Canvas with vertical gradient ────────────────────────────────
    img  = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        row = tuple(int(NAVY[i] + (NAVY_DEEP[i] - NAVY[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=row)

    # ── Decorative circle: top-right corner ──────────────────────────
    cr = 340
    draw.ellipse([W - cr, -cr // 2, W + cr // 2, cr + 30], fill=(*accent, 16))
    draw.ellipse([W - cr // 2 + 20, -cr // 3, W + cr // 3, cr // 2],
                 fill=(*accent, 9))

    # ── Left accent bar ───────────────────────────────────────────────
    draw.rectangle([0, 0, 11, H], fill=accent)

    # ── Top label band ────────────────────────────────────────────────
    draw.rectangle([0, 0, W, 86], fill=NAVY_DEEP)
    draw.line([(12, 86), (W, 86)], fill=accent, width=1)

    # ── Bottom strip ──────────────────────────────────────────────────
    STRIP = 70
    draw.rectangle([0, H - STRIP, W, H], fill=NAVY_DEEP)
    draw.line([(12, H - STRIP), (W, H - STRIP)], fill=accent, width=1)

    # ── Dot grid: bottom-left, very subtle ───────────────────────────
    for gx in range(36, 320, 28):
        for gy in range(H - STRIP - 100, H - STRIP - 4, 28):
            draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(28, 48, 70))

    # ── Fonts ─────────────────────────────────────────────────────────
    f_label   = load_font(REG_PATHS,  21)
    f_brand   = load_font(BOLD_PATHS, 21)
    f_meta    = load_font(REG_PATHS,  27)
    f_badge   = load_font(BOLD_PATHS, 21)
    f_title_L = load_font(BOLD_PATHS, 68)
    f_title_M = load_font(BOLD_PATHS, 54)
    f_title_S = load_font(BOLD_PATHS, 44)

    TX   = 36          # left text margin (after accent bar)
    MAX_W = W - TX - 90

    # ── Top label: "AESOP AI Academy  /  Course" ─────────────────────
    draw.text((TX, 28), "AESOP AI Academy", font=f_label, fill=GOLD_DIM)
    lbl_w = draw.textbbox((0, 0), "AESOP AI Academy", font=f_label)[2]
    draw.text((TX + lbl_w + 16, 28), "/  Course", font=f_label, fill=GOLD_DIM)

    # ── Course name (auto-size to fit in ≤ 2 lines) ──────────────────
    TITLE_Y = 128
    for f_title in [f_title_L, f_title_M, f_title_S]:
        lines = wrap_text(name, f_title, MAX_W, draw)
        if len(lines) <= 2:
            break

    ty = TITLE_Y
    for line in lines[:2]:
        draw.text((TX, ty), line, font=f_title, fill=WHITE)
        ty += f_title.size + 10

    # ── Metadata row: Category  ·  Tier  ·  N Modules ────────────────
    META_Y = ty + 28
    parts  = [p for p in [category, tier] if p]
    if mod_count:
        parts.append(f"{mod_count} Modules")
    draw.text((TX, META_Y), "  ·  ".join(parts), font=f_meta, fill=GOLD)

    # ── Live badge ────────────────────────────────────────────────────
    badge_txt  = "● LIVE"
    bb         = draw.textbbox((0, 0), badge_txt, font=f_badge)
    bw, bh     = bb[2] - bb[0] + 28, bb[3] - bb[1] + 14
    bx         = W - bw - 36
    by         = META_Y
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6,
                            fill=(*NAVY_DEEP, 200), outline=accent, width=1)
    draw.text((bx + 14, by + 7), badge_txt, font=f_badge, fill=accent)

    # ── Bottom branding ───────────────────────────────────────────────
    brand   = "aesopacademy.org"
    brand_w = draw.textbbox((0, 0), brand, font=f_brand)[2]
    draw.text((W - brand_w - 36, H - STRIP + 22), brand,
              font=f_brand, fill=GOLD)

    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(REGISTRY_PATH, encoding="utf-8") as f:
        registry = json.load(f)
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)

    lookup = {c["id"]: c for c in raw.get("courses", [])}

    generated, errors = [], []

    for course_id, reg in registry.items():
        if course_id.startswith("_") or not isinstance(reg, dict):
            continue
        if reg.get("status") != "live":
            continue

        course = lookup.get(course_id, {})
        out    = OUT_DIR / f"{course_id}.png"

        try:
            img = generate(course_id, course, reg)
            img.save(out, "PNG", optimize=True)
            generated.append(course_id)
            print(f"  ✓  {course_id}")
        except Exception as e:
            print(f"  ✗  {course_id}: {e}", file=sys.stderr)
            errors.append(course_id)

    print(f"\nGenerated {len(generated)}, errored {len(errors)}")
    if errors:
        print("Errors:", ", ".join(errors))
    sys.exit(1 if errors and not generated else 0)


if __name__ == "__main__":
    main()
