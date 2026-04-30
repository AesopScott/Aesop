#!/usr/bin/env python3
"""generate_og_images.py
Generates 1200x630 Open Graph images for every live Aesop course.
Reads course-registry.json (icon, accent, status) and courses-data.json
(name, description, category, tier, module count).
Output: assets/og/courses/{course-id}.png

Design: bold left accent stripe, large watermark letterform from course name,
description text shown for per-course uniqueness, category-keyed visual style.

Called by .github/workflows/generate-og-images.yml
"""

import json
import sys
import math
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
NAVY_MID  = (17,  35,  55)
NAVY_DEEP = ( 8,  16,  26)
GOLD      = (201, 160,  90)
GOLD_DIM  = (140, 108,  55)
WHITE     = (255, 255, 255)
WHITE_DIM = (200, 210, 220)

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


def blend(base, overlay, alpha):
    """Blend overlay color onto base at given alpha (0-1)."""
    return tuple(int(base[i] * (1 - alpha) + overlay[i] * alpha) for i in range(3))


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


def draw_watermark_letter(img, letter, font_paths, accent, size=420):
    """Draw a large semi-transparent letterform in bottom-right as watermark."""
    # Create a separate layer for the watermark
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d     = ImageDraw.Draw(layer)

    font = None
    for p in font_paths:
        if Path(p).exists():
            try:
                font = ImageFont.truetype(p, size)
                break
            except Exception:
                continue

    if font is None:
        return img  # skip if no font found

    bb  = d.textbbox((0, 0), letter, font=font)
    lw  = bb[2] - bb[0]
    lh  = bb[3] - bb[1]

    # Position: bottom-right, partially off-screen for dramatic effect
    tx = W - lw * 0.65
    ty = H - lh * 0.82

    # Draw with low opacity accent color
    fill = (*accent, 28)  # very subtle
    d.text((tx, ty), letter, font=font, fill=fill)

    # Merge watermark layer onto the image
    img_rgba = img.convert("RGBA")
    merged   = Image.alpha_composite(img_rgba, layer)
    return merged.convert("RGB")


def draw_category_pattern(draw, category, accent):
    """Draw a subtle background pattern keyed to course category."""
    cat = (category or "").lower()

    if "development" in cat or "code" in cat or "developer" in cat:
        # Circuit-like grid of small dots in top-right
        for gx in range(W - 380, W - 60, 30):
            for gy in range(90, 320, 30):
                # horizontal dot grid
                col = blend(NAVY, accent, 0.06)
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=col)
        # a few "trace" lines
        for gy in range(120, 300, 60):
            col = blend(NAVY, accent, 0.08)
            draw.line([(W - 350, gy), (W - 90, gy)], fill=col, width=1)

    elif "security" in cat or "pentest" in cat:
        # Hexagonal dot pattern
        for row in range(10):
            for col in range(10):
                gx = W - 360 + col * 36 + (row % 2) * 18
                gy = 100 + row * 32
                if gx < W - 60:
                    c = blend(NAVY, accent, 0.07)
                    draw.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=c)

    elif "youth" in cat or "young" in cat or "k-12" in cat or "kids" in cat:
        # Playful scattered dots in varied sizes
        import random
        rng = random.Random(42)
        for _ in range(40):
            gx = W - 400 + rng.randint(0, 320)
            gy = 100 + rng.randint(0, 300)
            r  = rng.randint(3, 8)
            c  = blend(NAVY, accent, 0.09)
            draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=c)

    elif "society" in cat or "ethics" in cat or "policy" in cat or "governance" in cat:
        # Concentric arc segments (like ripples) in top-right
        for i in range(4):
            r  = 80 + i * 60
            c  = blend(NAVY, accent, 0.06 - i * 0.01)
            draw.arc([W - r - 40, 86 - r // 2, W - 40 + r, 86 + r * 1.2],
                     start=-30, end=60, fill=c, width=2)

    else:
        # Default: subtle dot grid
        for gx in range(W - 320, W - 80, 28):
            for gy in range(100, 300, 28):
                c = blend(NAVY, accent, 0.05)
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=c)


def generate(course_id, course, reg):
    name      = course.get("name") or reg.get("title", course_id)
    desc      = course.get("description", "") or reg.get("desc", "")
    category  = course.get("category", "")
    tier      = course.get("tier", "")
    mod_count = len(course.get("modules", [])) or reg.get("modCount", 0)
    accent    = hex_to_rgb(reg.get("accent", "#c9a05a"))

    # ── Accent strip width: 72px bold left bar ────────────────────────
    STRIPE = 72

    # ── Canvas with vertical gradient ────────────────────────────────
    img  = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t   = y / H
        row = tuple(int(NAVY[i] + (NAVY_DEEP[i] - NAVY[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=row)

    # ── Bold left accent stripe with inner gradient ───────────────────
    for x in range(STRIPE):
        # Fade from accent at left edge to accent*0.5 at right edge
        fade = 1.0 - (x / STRIPE) * 0.45
        col  = tuple(int(accent[i] * fade) for i in range(3))
        draw.line([(x, 0), (x, H)], fill=col)

    # ── Thin accent line at right edge of stripe ──────────────────────
    draw.line([(STRIPE, 0), (STRIPE, H)], fill=GOLD_DIM, width=1)

    # ── Top label band ────────────────────────────────────────────────
    BAND_H = 88
    for y in range(BAND_H):
        t   = y / BAND_H
        row = blend(NAVY_DEEP, NAVY, t * 0.6)
        draw.line([(STRIPE + 1, y), (W, y)], fill=row)
    draw.line([(STRIPE + 1, BAND_H), (W, BAND_H)], fill=GOLD_DIM, width=1)

    # ── Bottom strip ──────────────────────────────────────────────────
    STRIP = 72
    draw.rectangle([STRIPE + 1, H - STRIP, W, H], fill=NAVY_DEEP)
    draw.line([(STRIPE + 1, H - STRIP), (W, H - STRIP)], fill=GOLD_DIM, width=1)

    # ── Category-specific background pattern (right side) ────────────
    draw_category_pattern(draw, category, accent)

    # ── Watermark letterform ──────────────────────────────────────────
    first_letter = name[0].upper() if name else "A"
    img = draw_watermark_letter(img, first_letter, BOLD_PATHS, accent, size=420)
    draw = ImageDraw.Draw(img)  # refresh draw handle after composite

    # ── Fonts ─────────────────────────────────────────────────────────
    f_label   = load_font(REG_PATHS,  22)
    f_brand   = load_font(BOLD_PATHS, 22)
    f_cat     = load_font(REG_PATHS,  24)
    f_desc    = load_font(REG_PATHS,  26)
    f_meta    = load_font(BOLD_PATHS, 22)
    f_title_L = load_font(BOLD_PATHS, 64)
    f_title_M = load_font(BOLD_PATHS, 52)
    f_title_S = load_font(BOLD_PATHS, 42)

    TX    = STRIPE + 28     # left text margin
    MAX_W = W - TX - 80

    # ── Top label: "AESOP AI Academy" ────────────────────────────────
    draw.text((TX, 28), "AESOP AI Academy", font=f_label, fill=GOLD_DIM)
    if category:
        lbl_w = draw.textbbox((0, 0), "AESOP AI Academy", font=f_label)[2]
        draw.text((TX + lbl_w + 14, 28), f"/  {category}", font=f_label, fill=GOLD_DIM)

    # ── Course name (auto-size to fit in ≤ 2 lines) ──────────────────
    TITLE_Y = 112
    chosen_font = f_title_S
    for f_title in [f_title_L, f_title_M, f_title_S]:
        lines = wrap_text(name, f_title, MAX_W, draw)
        if len(lines) <= 2:
            chosen_font = f_title
            break

    ty = TITLE_Y
    for line in lines[:2]:
        draw.text((TX, ty), line, font=chosen_font, fill=WHITE)
        ty += chosen_font.size + 8

    # ── Description: up to 2 lines ────────────────────────────────────
    DESC_Y  = ty + 22
    desc_lines = wrap_text(desc, f_desc, MAX_W - 40, draw)
    for line in desc_lines[:2]:
        draw.text((TX, DESC_Y), line, font=f_desc, fill=WHITE_DIM)
        DESC_Y += f_desc.size + 6

    # ── Metadata row ──────────────────────────────────────────────────
    META_Y = H - STRIP - 68
    parts  = [p for p in [tier] if p]
    if mod_count:
        parts.append(f"{mod_count} Modules")
    if parts:
        draw.text((TX, META_Y), "  ·  ".join(parts), font=f_cat, fill=GOLD)

    # ── Live badge ────────────────────────────────────────────────────
    badge_txt = "● LIVE"
    bb        = draw.textbbox((0, 0), badge_txt, font=f_meta)
    bw, bh    = bb[2] - bb[0] + 28, bb[3] - bb[1] + 14
    bx        = W - bw - 36
    by        = META_Y - 2
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6,
                            fill=NAVY_DEEP, outline=accent, width=2)
    draw.text((bx + 14, by + 7), badge_txt, font=f_meta, fill=accent)

    # ── Bottom branding ───────────────────────────────────────────────
    brand   = "aesopacademy.org"
    brand_w = draw.textbbox((0, 0), brand, font=f_brand)[2]
    draw.text((W - brand_w - 36, H - STRIP + 24),
              brand, font=f_brand, fill=GOLD)

    # ── Accent square in the stripe at vertical center ────────────────
    sq_y = H // 2 - 20
    draw.rectangle([16, sq_y, STRIPE - 16, sq_y + 40],
                   fill=blend(WHITE, accent, 0.3))

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
