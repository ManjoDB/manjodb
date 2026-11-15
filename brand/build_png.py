"""Renders the ManjoDB square logo PNG: the reverse mark centered on a full-bleed plum square.

Square corners by design: the PNG is a plain square, with no rounded tile and no transparency.
Geometry comes from logo/manjodb-mark-reverse.svg (written by build_logo.py), so the mark is never redrawn here.

Needs Playwright (npx playwright, with Edge) and Pillow. Run: python brand/build_png.py
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "logo" / "manjodb-mark-reverse.svg"
OUT = HERE / "logo" / "manjodb-logo-1024.png"

SIZE = 1024
PLUM = (0x2B, 0x0D, 0x3F)
# Mark grid is 56 x 64 units; its drawn content spans 4.5..51.5 x 4.25..59.75 (round caps and rings
# included), centered on (28, 32), the middle of the viewBox. Scale 11.5 makes the content 638 px tall.
SCALE = 11.5
VB_W, VB_H = 56, 64
CONTENT = (4.5, 4.25, 51.5, 59.75)  # left, top, right, bottom, in mark units


def mark_inner(svg: str) -> str:
    return re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)


def build_svg() -> str:
    w, h = VB_W * SCALE, VB_H * SCALE
    x, y = (SIZE - w) / 2, (SIZE - h) / 2
    inner = mark_inner(SRC.read_text(encoding="utf-8"))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">'
        f'<rect width="{SIZE}" height="{SIZE}" fill="#2B0D3F"/>'
        f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {VB_W} {VB_H}">{inner}</svg>'
        f"</svg>"
    )


def render(svg: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "logo.html"
        page.write_text(
            f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;background:#2B0D3F}}'
            f'svg{{display:block}}</style>{svg}',
            encoding="utf-8",
        )
        cmd = ["npx", "--no-install", "playwright", "screenshot", "--channel", "msedge",
               f"--viewport-size={SIZE},{SIZE}", "--wait-for-timeout=300",
               page.as_uri(), str(OUT)]
        subprocess.run(cmd, check=True, shell=(os.name == "nt"))


def verify() -> None:
    im = Image.open(OUT).convert("RGB")
    assert im.size == (SIZE, SIZE), f"size {im.size}"
    # Square corners: all four corner pixels must be the plum fill, with no cut-away tile.
    for pt in [(0, 0), (SIZE - 1, 0), (0, SIZE - 1), (SIZE - 1, SIZE - 1)]:
        assert im.getpixel(pt) == PLUM, f"corner {pt} is {im.getpixel(pt)}"
    # Centering: margins from the plum background to the drawn M must match left/right and top/bottom.
    px = im.load()
    xs, ys = [], []
    for yy in range(SIZE):
        for xx in range(SIZE):
            r, g, b = px[xx, yy]
            if abs(r - PLUM[0]) + abs(g - PLUM[1]) + abs(b - PLUM[2]) > 24:
                xs.append(xx)
                ys.append(yy)
    l, t, r_, b_ = min(xs), min(ys), max(xs), max(ys)
    print(f"{OUT.name}: {SIZE}x{SIZE}")
    print(f"M bounds x {l}..{r_}, y {t}..{b_}")
    print(f"margins: left {l}, right {SIZE - 1 - r_}, top {t}, bottom {SIZE - 1 - b_}")
    if abs(l - (SIZE - 1 - r_)) > 1 or abs(t - (SIZE - 1 - b_)) > 1:
        sys.exit("M is not centered within 1 px")


if __name__ == "__main__":
    render(build_svg())
    verify()
