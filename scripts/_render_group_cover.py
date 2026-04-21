#!/usr/bin/env python3
"""
Render the Free AI Education LinkedIn group cover as a pixel-perfect PNG
at 1536 × 768. Matches the HTML/canvas template in
free-ai-education-cover.html.

Fonts are fetched from Google Fonts' GitHub once and cached under
.fonts/. The PNG is written to free-ai-education-cover.png.
"""

from __future__ import annotations

import io
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "free-ai-education-cover.png"
FONT_CACHE = REPO_ROOT / ".fonts"
FONT_CACHE.mkdir(exist_ok=True)

# ── Canvas ──
W, H = 1536, 768
NAVY = (13, 27, 42)
NAVY_2 = (21, 42, 63)
GOLD = (201, 160, 90)
WHITE = (255, 255, 255)

FONTS = {
    "cinzel": (
        "Cinzel[wght].ttf",
        "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    ),
    "crimson_italic": (
        "CrimsonPro-Italic[wght].ttf",
        "https://github.com/google/fonts/raw/main/ofl/crimsonpro/CrimsonPro-Italic%5Bwght%5D.ttf",
    ),
}


def fetch_font(key: str) -> Path:
    filename, url = FONTS[key]
    local = FONT_CACHE / filename
    if local.exists():
        return local
    print(f"Fetching {filename} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "aesop-cover-builder"})
    with urllib.request.urlopen(req) as resp:
        local.write_bytes(resp.read())
    return local


def load_font(key: str, size: int, weight: int | None = None) -> ImageFont.FreeTypeFont:
    path = fetch_font(key)
    font = ImageFont.truetype(str(path), size=size)
    if weight is not None and hasattr(font, "set_variation_by_axes"):
        try:
            font.set_variation_by_axes([weight])
        except Exception:
            pass
    return font


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_diagonal_gradient(img: Image.Image, c1, c2_mid, c3) -> None:
    """Navy -> navy-2 -> navy linear gradient along the diagonal."""
    w, h = img.size
    px = img.load()
    # Diagonal distance in [0..1]
    max_d = w + h
    for y in range(h):
        for x in range(w):
            t = (x + y) / max_d
            if t <= 0.55:
                c = lerp_color(c1, c2_mid, t / 0.55)
            else:
                c = lerp_color(c2_mid, c3, (t - 0.55) / 0.45)
            px[x, y] = c


def apply_radial_glow(img: Image.Image, cx: int, cy: int, radius: int, color=(201, 160, 90), max_alpha: float = 0.14) -> None:
    """Additive gold glow. Simple falloff: alpha = max_alpha * max(0, 1 - d/radius)."""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = overlay.load()
    for y in range(h):
        dy = (y - cy) / radius
        for x in range(w):
            dx = (x - cx) / radius
            d = (dx * dx + dy * dy) ** 0.5
            if d >= 1.0:
                continue
            a = int(255 * max_alpha * (1 - d) ** 1.5)
            op[x, y] = (*color, a)
    img.alpha_composite(overlay)


def draw_tracked_text(draw, text, font, center_xy, color, tracking_px: float = 0.0, anchor: str = "mm"):
    """
    Draw text with per-character tracking. Pillow doesn't support letter-spacing
    natively so we measure each character and place it with extra gap.
    anchor: 'mm' = center,  'rm' = right-middle, 'lm' = left-middle.
    """
    cx, cy = center_xy
    # measure each char
    widths = []
    for ch in text:
        bbox = font.getbbox(ch)
        widths.append(bbox[2] - bbox[0])
    total = sum(widths) + tracking_px * (len(text) - 1)
    if anchor == "mm":
        x = cx - total / 2
    elif anchor == "rm":
        x = cx - total
    else:  # 'lm'
        x = cx
    # Ascent-based vertical offset: use font metrics for consistent baseline
    ascent, descent = font.getmetrics()
    # center vertically on cy — we offset by -ascent/2 to align mid-height
    y = cy - (ascent - descent) / 2 - descent
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=color)
        x += w + tracking_px


def main() -> int:
    # 1. Base canvas (RGBA so we can layer glow)
    img = Image.new("RGBA", (W, H), NAVY)

    # 2. Navy diagonal gradient
    grad = Image.new("RGB", (W, H), NAVY)
    draw_diagonal_gradient(grad, NAVY, NAVY_2, NAVY)
    img.paste(grad, (0, 0))
    img = img.convert("RGBA")

    # 3. Gold radial glow (soft, near the upper-center)
    apply_radial_glow(img, cx=W // 2, cy=int(H * 0.40), radius=640, color=GOLD, max_alpha=0.14)

    draw = ImageDraw.Draw(img)

    # 4. Fonts
    cinzel_title = load_font("cinzel", 140, weight=900)
    cinzel_eyebrow = load_font("cinzel", 14, weight=500)  # Cinzel doubles for eyebrow
    crimson_italic = load_font("crimson_italic", 34, weight=400)
    attribution_font = load_font("cinzel", 13, weight=400)

    # 5. Eyebrow (tracked uppercase, muted gold)
    eyebrow_color = (*GOLD, 166)  # ~0.65 alpha
    draw_tracked_text(
        draw,
        "A COMMUNITY HOSTED BY AESOP AI ACADEMY",
        cinzel_eyebrow,
        (W // 2, 200),
        eyebrow_color,
        tracking_px=4.9,
        anchor="mm",
    )

    # 6. Top rule
    draw.rectangle((W // 2 - 60, 239, W // 2 + 60, 241), fill=GOLD)

    # 7. Title — two lines, heavy serif with soft drop shadow
    # Render to a side image so we can apply a blur shadow under the text
    def text_with_shadow(txt, cx, cy, font, color, tracking):
        # Shadow layer (drawn once, Gaussian-ish via 3 offset draws to fake blur)
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        for dy in range(2, 8, 2):
            draw_tracked_text(
                sd, txt, font, (cx, cy + dy), (0, 0, 0, 90), tracking_px=tracking
            )
        from PIL import ImageFilter
        shadow = shadow.filter(ImageFilter.GaussianBlur(6))
        img.alpha_composite(shadow)
        # Main text
        draw2 = ImageDraw.Draw(img)
        draw_tracked_text(draw2, txt, font, (cx, cy), color, tracking_px=tracking)

    text_with_shadow("FREE AI", W // 2, 340, cinzel_title, WHITE, tracking=8.4)
    text_with_shadow("EDUCATION", W // 2, 480, cinzel_title, WHITE, tracking=8.4)

    # Re-grab draw handle (alpha_composite may invalidate)
    draw = ImageDraw.Draw(img)

    # 8. Bottom rule
    draw.rectangle((W // 2 - 60, 557, W // 2 + 60, 559), fill=GOLD)

    # 9. Subtitle — rendered as single string so italic kerning stays natural
    subtitle_text = "AI literacy belongs to everyone."
    ascent, descent = crimson_italic.getmetrics()
    sub_bbox = crimson_italic.getbbox(subtitle_text)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (W - sub_width) // 2 - sub_bbox[0]
    sub_y = 608 - (ascent - descent) / 2 - descent
    draw.text((sub_x, sub_y), subtitle_text, font=crimson_italic, fill=GOLD)

    # 10. Attribution bottom-right
    attr_color = (255, 255, 255, 97)  # ~0.38 alpha
    draw_tracked_text(
        draw,
        "aesopacademy.org",
        attribution_font,
        (W - 40, H - 28),
        attr_color,
        tracking_px=1.0,
        anchor="rm",
    )

    # 11. Flatten + save
    final = Image.new("RGB", (W, H), NAVY)
    final.paste(img, (0, 0), img)
    final.save(OUT_PATH, "PNG", optimize=True)
    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"Saved {OUT_PATH.relative_to(REPO_ROOT)}  ({W}×{H}, {size_kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
