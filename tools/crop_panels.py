#!/usr/bin/env python3
"""Batch-crop article figure panels for any lecture.

    python tools/crop_panels.py lectures/L<N>/crops.json

crops.json:
{
  "papers": {"land69a": "papers/land69a.pdf", ...},          # PDF paths, relative to crops.json
  "dpi": 220,
  "crops": {"p_land69a_fig3": ["land69a", 6, [0.12, 0.25, 0.88, 0.695]], ...},
  "combos": {"c_name": ["h" | "v", ["p_a", "p_b"]]}          # optional: join two panels
}
Page numbers are 1-based PDF pages; boxes are fractions of the page (left, top, right, bottom).
Crops are saved to lectures/L<N>/figures/<name>.png. Look at every crop afterwards:
no clipped labels, no neighbouring panels, no stray text.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crop_figure import render  # noqa: E402


def trim(im, pad=12):
    """Remove surrounding white margin, keep a small pad."""
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 25 else 0).getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))


def combine(out, name, direction, parts, gap=40):
    ims = [Image.open(out / f"{p}.png").convert("RGB") for p in parts]
    if direction == "h":
        h = max(i.height for i in ims)
        ims = [i.resize((int(i.width * h / i.height), h)) for i in ims]
        canvas = Image.new("RGB", (sum(i.width for i in ims) + gap * (len(ims) - 1), h), "white")
        x = 0
        for i in ims:
            canvas.paste(i, (x, 0)); x += i.width + gap
    else:
        w = max(i.width for i in ims)
        ims = [i.resize((w, int(i.height * w / i.width))) for i in ims]
        canvas = Image.new("RGB", (w, sum(i.height for i in ims) + gap * (len(ims) - 1)), "white")
        y = 0
        for i in ims:
            canvas.paste(i, (0, y)); y += i.height + gap
    canvas.save(out / f"{name}.png")


def main(spec_path):
    spec_path = Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text())
    base, out = spec_path.parent, spec_path.parent / "figures"
    out.mkdir(exist_ok=True)
    dpi = spec.get("dpi", 220)
    pages = {}
    for name, (paper, page, (l, t, r, b)) in spec["crops"].items():
        key = (paper, page)
        if key not in pages:
            pages[key] = render(base / spec["papers"][paper], page, dpi).convert("RGB")
        im = pages[key]
        w, h = im.size
        trim(im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))).save(out / f"{name}.png")
        print(name)
    for name, (direction, parts) in spec.get("combos", {}).items():
        combine(out, name, direction, parts)
        print(name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
