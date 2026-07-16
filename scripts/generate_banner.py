#!/usr/bin/env python3
"""
Generate the profile README banner (dark + light variants).

Usage:
    python3 scripts/generate_banner.py --source /absolute/path/to/portrait.png

The source portrait is NOT stored in this repository. Keep your original
photo outside of version control and pass its path via --source. Only the
composed banner PNGs in assets/ are committed.

Requires: Pillow  (pip install pillow)
Fonts (Inter, SIL OFL 1.1) are bundled in assets/fonts/.
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"
OUTPUT_DIR = ROOT / "assets"

SCALE = 2
W, H = 1200 * SCALE, 400 * SCALE
RADIUS = 28 * SCALE
PAD = 60 * SCALE

PROFILE = {
    "eyebrow": "FULL-STACK WEB DEVELOPER",
    "name": "Wahyu Syahbani",
    "role": "Informatics Engineering Student, Universitas Pamulang",
    "location": "Jakarta, Indonesia",
    "email": "dev.wsyahbanii@gmail.com",
    "tags": ["PHP", "JavaScript", "MySQL", "REST API", "Admin Systems"],
}

PALETTES = {
    "dark": dict(
        bg_top=(10, 13, 24), bg_bottom=(14, 19, 36),
        accent_cyan=(56, 201, 248), accent_indigo=(129, 140, 248),
        text_primary=(243, 246, 250), text_muted=(148, 163, 184),
        pill_border=(255, 255, 255), pill_border_a=28,
        pill_fill=(255, 255, 255), pill_fill_a=10, pill_text=(203, 213, 225),
        dot_color=(148, 163, 184), dot_opacity=14,
        photo_frame=(255, 255, 255), glow_a=60,
        border_col=(255, 255, 255, 22),
    ),
    "light": dict(
        bg_top=(250, 251, 253), bg_bottom=(237, 242, 252),
        accent_cyan=(8, 130, 171), accent_indigo=(79, 70, 229),
        text_primary=(13, 20, 36), text_muted=(81, 94, 116),
        pill_border=(15, 23, 42), pill_border_a=22,
        pill_fill=(15, 23, 42), pill_fill_a=5, pill_text=(51, 65, 85),
        dot_color=(100, 116, 139), dot_opacity=10,
        photo_frame=(15, 23, 42), glow_a=26,
        border_col=(15, 23, 42, 18),
    ),
}


def font(weight, size):
    return ImageFont.truetype(str(FONT_DIR / f"Inter-{weight}.ttf"), size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_gradient_bg(top, bottom, w, h):
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        col = lerp(top, bottom, y / h)
        for x in range(w):
            px[x, y] = col
    return base


def add_radial_glow(img, center, radius, color, max_opacity):
    w, h = img.size
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for i in range(60, 0, -1):
        t = i / 60
        r = radius * t
        alpha = int(max_opacity * (1 - t) ** 1.6)
        gdraw.ellipse([center[0] - r, center[1] - r, center[0] + r, center[1] + r], fill=(*color, alpha))
    img.alpha_composite(glow)


def add_dot_grid(img, color, spacing, opacity):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(0, w, spacing):
        for y in range(0, h, spacing):
            od.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(*color, opacity))
    img.alpha_composite(overlay)


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return mask


def prep_photo(source_path, box_size):
    img = Image.open(source_path).convert("RGB")
    w, h = img.size
    crop = img.crop((int(w * 0.225), int(h * 0.16), int(w * 0.79), int(h * 0.79)))
    crop = ImageOps.autocontrast(crop, cutoff=1)
    return crop.resize((box_size, box_size), Image.LANCZOS)


def draw_tracked_text(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def build_banner(source_path, mode):
    c = PALETTES[mode]
    base = make_gradient_bg(c["bg_top"], c["bg_bottom"], W, H).convert("RGBA")
    add_dot_grid(base, c["dot_color"], 34 * SCALE, c["dot_opacity"])
    add_radial_glow(base, (W * 0.86, H * 0.08), 620 * SCALE // 2, c["accent_indigo"], c["glow_a"])
    add_radial_glow(base, (W * 0.14, H * 1.02), 520 * SCALE // 2, c["accent_cyan"], c["glow_a"])

    draw = ImageDraw.Draw(base)

    box = 264 * SCALE
    photo_x = PAD
    photo_y = (H - box) // 2
    photo_radius = 24 * SCALE

    ring_pad = 5 * SCALE
    ring = Image.new("RGBA", (box + ring_pad * 2, box + ring_pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(ring).rounded_rectangle(
        [0, 0, ring.size[0] - 1, ring.size[1] - 1],
        radius=photo_radius + ring_pad,
        outline=c["accent_cyan"] + (150,), width=int(2.4 * SCALE),
    )
    base.alpha_composite(ring, (photo_x - ring_pad, photo_y - ring_pad))

    photo = prep_photo(source_path, box).convert("RGBA")
    photo.putalpha(rounded_mask((box, box), photo_radius))
    base.alpha_composite(photo, (photo_x, photo_y))

    draw.rounded_rectangle(
        [photo_x, photo_y, photo_x + box, photo_y + box], radius=photo_radius,
        outline=(*c["photo_frame"], 46 if mode == "dark" else 30), width=int(1.6 * SCALE),
    )

    tx = photo_x + box + 64 * SCALE
    tw = W - tx - PAD

    eyebrow_font = font("SemiBold", 20 * SCALE)
    name_font = font("ExtraBold", 56 * SCALE)
    role_font = font("Medium", 24 * SCALE)
    meta_font = font("Regular", 19 * SCALE)
    pill_font = font("SemiBold", 16 * SCALE)
    pill_h = 38 * SCALE

    block_height = 38 * SCALE + 66 * SCALE + 40 * SCALE + 30 * SCALE + 40 * SCALE + pill_h
    cy = (H - block_height) // 2

    draw_tracked_text(draw, (tx, cy), PROFILE["eyebrow"], eyebrow_font, c["accent_cyan"], tracking=3.2 * SCALE)
    cy += 38 * SCALE

    draw.text((tx, cy), PROFILE["name"], font=name_font, fill=c["text_primary"])
    cy += 66 * SCALE

    draw.text((tx, cy), PROFILE["role"], font=role_font, fill=c["text_muted"])
    cy += 40 * SCALE

    draw.line([(tx, cy), (tx + 110 * SCALE, cy)], fill=c["accent_cyan"], width=int(3 * SCALE))
    cy += 30 * SCALE

    mx = tx
    meta_items = [PROFILE["location"], PROFILE["email"]]
    for i, item in enumerate(meta_items):
        draw.text((mx, cy), item, font=meta_font, fill=c["text_muted"])
        mx += draw.textlength(item, font=meta_font) + 20 * SCALE
        if i < len(meta_items) - 1:
            draw.ellipse([mx - 16 * SCALE, cy + 8 * SCALE, mx - 11 * SCALE, cy + 13 * SCALE], fill=c["text_muted"])
            mx += 24 * SCALE
    cy += 40 * SCALE

    px, py = tx, cy
    for tag in PROFILE["tags"]:
        tlen = draw.textlength(tag, font=pill_font)
        pw = int(tlen + 34 * SCALE)
        if px + pw > tx + tw:
            px = tx
            py += pill_h + 12 * SCALE
        pill_img = Image.new("RGBA", (pw, pill_h), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pill_img)
        pd.rounded_rectangle([0, 0, pw - 1, pill_h - 1], radius=pill_h // 2, fill=(*c["pill_fill"], c["pill_fill_a"]))
        pd.rounded_rectangle([0, 0, pw - 1, pill_h - 1], radius=pill_h // 2, outline=(*c["pill_border"], c["pill_border_a"]), width=int(1.4 * SCALE))
        pd.text((17 * SCALE, pill_h // 2), tag, font=pill_font, fill=c["pill_text"], anchor="lm")
        base.alpha_composite(pill_img, (int(px), int(py)))
        px += pw + 12 * SCALE

    outer_mask = rounded_mask((W, H), RADIUS)
    final = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    final.paste(base, (0, 0), outer_mask)
    ImageDraw.Draw(final).rounded_rectangle([1, 1, W - 2, H - 2], radius=RADIUS, outline=c["border_col"], width=int(1.6 * SCALE))
    return final


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to the source portrait (not committed)")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for mode in ("dark", "light"):
        banner = build_banner(args.source, mode)
        out = OUTPUT_DIR / f"header-{mode}.png"
        banner.save(out)
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
