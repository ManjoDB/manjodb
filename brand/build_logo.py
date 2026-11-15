# Generates every ManjoDB logo file from one geometry (Commit Lanes identity).
import os
OUT = os.path.join(os.path.dirname(__file__), "logo")

PLUM, INK, PAPER = "#2B0D3F", "#1C0E2A", "#F7EEFF"
LIGHT = dict(rail="#6E3AD9", branch="#D81B73", vertex=INK, word=INK)
DARK = dict(rail="#B98CFF", branch="#FF4FA0", vertex=PAPER, word=PAPER)

# Mark geometry (56 x 64 units): two rails (lanes), one branch through the
# middle lane, three commit vertices: branch point, commit, merge point.
DOTS = [(10, 18), (28, 45), (46, 18)]
RAILS = "M10 7V57M46 7V57"
BRANCH = "M10 18C10 31 28 31 28 45C28 31 46 31 46 18"

def mark(c, uid, stroke=5.5, ring=True):
    r_knock = 5.1 if ring else 5.9
    knock = "".join(f'<circle cx="{x}" cy="{y}" r="{r_knock}"/>' for x, y in DOTS)
    if ring:
        dots = f'<g fill="none" stroke="{c["vertex"]}" stroke-width="2.8">' + "".join(
            f'<circle cx="{x}" cy="{y}" r="4.1"/>' for x, y in DOTS) + "</g>"
    else:
        dots = f'<g fill="{c["vertex"]}">' + "".join(
            f'<circle cx="{x}" cy="{y}" r="4.6"/>' for x, y in DOTS) + "</g>"
    return (f'<mask id="k{uid}" maskUnits="userSpaceOnUse" x="-4" y="-4" width="64" height="72">'
            f'<rect x="-4" y="-4" width="64" height="72" fill="#fff"/><g fill="#000">{knock}</g></mask>'
            f'<g fill="none" stroke-linecap="round" stroke-width="{stroke}" mask="url(#k{uid})">'
            f'<path d="{RAILS}" stroke="{c["rail"]}"/><path d="{BRANCH}" stroke="{c["branch"]}"/></g>{dots}')

# Wordmark "manjodb": monoline lettering drawn with the mark's own vocabulary.
# x-height 50..100, ascender 20, descender 125. d and b stems rhyme with the rails.
WORD = ("M5 50V100M5 66A16 16 0 0 1 37 66V100M37 66A16 16 0 0 1 69 66V100"   # m
        "M141 75A25 25 0 1 1 91 75A25 25 0 1 1 141 75M141 50V100"           # a
        "M163 50V100M163 70A20 20 0 0 1 203 70V100"                         # n
        "M225 50V112A13 13 0 0 1 212 125"                                   # j
        "M297 75A25 25 0 1 1 247 75A25 25 0 1 1 297 75"                     # o
        "M369 75A25 25 0 1 1 319 75A25 25 0 1 1 369 75M369 20V100"          # d
        "M391 20V100M441 75A25 25 0 1 1 391 75A25 25 0 1 1 441 75")         # b

def word(color):
    return (f'<path d="{WORD}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="225" cy="29" r="6" fill="none" stroke="{color}" stroke-width="5.5"/>')

def svg(vb, body, title="ManjoDB", w=None, h=None):
    size = f' width="{w}" height="{h}"' if w else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{size} role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')

def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

write("manjodb-mark.svg", svg("0 0 56 64", mark(LIGHT, "l")))
write("manjodb-mark-reverse.svg", svg("0 0 56 64", mark(DARK, "d")))
mono = dict(rail="currentColor", branch="currentColor", vertex="currentColor", word="currentColor")
write("manjodb-mark-mono.svg", svg("0 0 56 64", mark(mono, "m")))
write("manjodb-wordmark.svg", svg("-4 12 454 120", word(INK)))
write("manjodb-wordmark-reverse.svg", svg("-4 12 454 120", word(PAPER)))
# Lockup: rails run ascender (20) to baseline (100), like the d and b stems.
def lockup(c, uid):
    return (f'<g transform="translate(0 8.8) scale(1.6)">{mark(c, uid)}</g>'
            f'<g transform="translate(122 0)">{word(c["word"])}</g>')
write("manjodb-lockup.svg", svg("-2 12 572 120", lockup(LIGHT, "l")))
write("manjodb-lockup-reverse.svg", svg("-2 12 572 120", lockup(DARK, "d")))
# App icon and favicon: plum tile. Favicon uses solid vertices and heavier lanes.
write("manjodb-app-icon.svg", svg("0 0 512 512",
      f'<rect width="512" height="512" rx="112" fill="{PLUM}"/>'
      f'<g transform="translate(88 64) scale(6)">{mark(DARK, "a")}</g>'))
write("favicon.svg", svg("0 0 64 64",
      f'<rect width="64" height="64" rx="14" fill="{PLUM}"/>'
      f'<g transform="translate(9.6 6.4) scale(0.8)">{mark(DARK, "f", stroke=7.5, ring=False)}</g>'))
print("\n".join(sorted(os.listdir(OUT))))
