# Profile Banner

The README header is a static PNG banner (dark + light variants) generated with Python/Pillow.
It replaces the previous ASCII-art animated SVG terminal with a clean, professional identity card:
portrait photo, name, role, location, and a tech-tag row.

## Regenerate

```bash
pip install pillow
python3 scripts/generate_banner.py --source /absolute/path/to/portrait.jpg
```

This writes `assets/header-dark.png` and `assets/header-light.png`.

## Portrait privacy

Do not commit the original, uncropped source portrait to this repository.
Keep it outside version control and pass its path via `--source`. Only the
composed banner PNGs (which contain the cropped, final result) belong in `assets/`.

## Editing content

Profile text (name, role, location, email, tags) lives in the `PROFILE` dict at
the top of `scripts/generate_banner.py`. Update it there and re-run the script;
do not hand-edit the generated PNGs.

## Fonts

Banners use [Inter](https://github.com/rsms/inter) (SIL Open Font License 1.1),
bundled in `assets/fonts/` so the script runs without extra downloads.

## Crop tuning

The portrait crop box (`prep_photo` in `scripts/generate_banner.py`) is tuned
for a roughly square source image with the subject's head starting around 16-20%
from the top. Adjust the crop fractions there if you change the source photo's
framing.
