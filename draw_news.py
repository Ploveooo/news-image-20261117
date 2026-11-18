#!/usr/bin/env python3
"""Draw entry.png: a one-page news front page summing up the world news of
Tuesday 17 November 2026.

Six verified stories (see SOURCES.md), one per card. Each card has a flat
pictogram on a coloured band, a kicker, a headline and one short summary
line. The masthead names the day, and the footer names the day again, so the
date the image sums up is unmistakable.

Output: 1024x1024 PNG, well under 1 MiB. Run: python3 draw_news.py
Needs Pillow (build-time only). The entry program main.ts is stdlib-only
Node and just copies the finished entry.png to /output/entry.png.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (245, 240, 228)
INK = (25, 40, 62)
NAVY = (20, 33, 60)
RED = (192, 38, 44)
GOLD = (233, 185, 76)
CARD = (255, 255, 255)
EDGE = (200, 192, 176)
BODY = (72, 84, 106)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_SERIF = load("DejaVuSerif-Bold.ttf", 56)
F_TOP = load("DejaVuSans-Bold.ttf", 24)
F_KICK = load("DejaVuSans-Bold.ttf", 20)
F_HEAD = load("DejaVuSans-Bold.ttf", 26)
F_BODY = load("DejaVuSans.ttf", 19)
F_FOOT = load("DejaVuSans.ttf", 17)


def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(drw, cx, y, text, fnt, fill, gap=7):
    """Draw centred text with extra letter spacing."""
    widths = [fnt.getlength(ch) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        drw.text((x, y), ch, font=fnt, fill=fill)
        x += w + gap


# ---------------------------------------------------------------- pictograms
# Each draws a white flat pictogram centred on (cx, cy), roughly 110 px wide.

def pic_bridge(drw, cx, cy):
    # broken deck: left half level, right half dropped into the water
    drw.rectangle([cx - 56, cy + 14, cx - 2, cy + 22], fill=WHITE)
    drw.polygon([(cx + 2, cy + 14), (cx + 52, cy + 30),
                 (cx + 52, cy + 38), (cx + 2, cy + 22)], fill=WHITE)
    # arch over the gap
    drw.arc([cx - 34, cy - 52, cx + 34, cy + 14], 180, 360, fill=WHITE, width=5)
    # towers
    drw.rectangle([cx - 50, cy - 44, cx - 42, cy + 14], fill=WHITE)
    drw.rectangle([cx + 42, cy - 44, cx + 50, cy + 30], fill=WHITE)
    # water
    for dy in (48, 58):
        drw.line([cx - 56, cy + dy, cx + 56, cy + dy], fill=WHITE, width=3)


def pic_tanker(drw, cx, cy):
    # hull with a notch, funnel, and a burst above the deck
    drw.polygon([(cx - 54, cy + 6), (cx + 54, cy + 6), (cx + 42, cy + 34),
                 (cx - 42, cy + 34)], fill=WHITE)
    drw.rectangle([cx - 40, cy - 16, cx - 14, cy + 6], fill=WHITE)
    drw.rectangle([cx + 22, cy - 28, cx + 36, cy + 6], fill=WHITE)
    # blast star
    for k in range(6):
        a = math.radians(k * 60 + 15)
        x1 = cx - 6 + 14 * math.cos(a)
        y1 = cy - 44 + 14 * math.sin(a)
        x2 = cx - 6 + 24 * math.cos(a)
        y2 = cy - 44 + 24 * math.sin(a)
        drw.line([x1, y1, x2, y2], fill=WHITE, width=4)
    # waves
    for dy in (46, 56):
        drw.arc([cx - 54, cy + dy - 7, cx - 20, cy + dy + 7], 0, 180,
                fill=WHITE, width=4)
        drw.arc([cx - 14, cy + dy - 7, cx + 20, cy + dy + 7], 0, 180,
                fill=WHITE, width=4)
        drw.arc([cx + 26, cy + dy - 7, cx + 56, cy + dy + 7], 0, 180,
                fill=WHITE, width=4)


def pic_jet(drw, cx, cy):
    # fighter jet in profile, nose right
    drw.polygon([(cx - 52, cy), (cx + 20, cy - 12), (cx + 56, cy),
                 (cx + 20, cy + 12)], fill=WHITE)
    # swept wing
    drw.polygon([(cx - 6, cy - 8), (cx + 8, cy - 44), (cx + 22, cy - 8)],
                fill=WHITE)
    # tail fin
    drw.polygon([(cx - 40, cy - 4), (cx - 30, cy - 34), (cx - 18, cy - 4)],
                fill=WHITE)
    # cockpit
    drw.ellipse([cx + 22, cy - 7, cx + 38, cy + 3], fill=NAVY)
    # speed lines
    for dy in (-20, 0, 20):
        drw.line([cx - 56, cy + dy, cx - 36, cy + dy], fill=WHITE, width=3)


def pic_globe(drw, cx, cy):
    drw.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], outline=WHITE, width=6)
    drw.line([cx - 42, cy - 15, cx + 42, cy - 15], fill=WHITE, width=4)
    drw.line([cx - 46, cy + 15, cx + 46, cy + 15], fill=WHITE, width=4)
    drw.arc([cx - 20, cy - 46, cx + 20, cy + 46], 270, 90, fill=WHITE, width=4)
    drw.arc([cx - 20, cy - 46, cx + 20, cy + 46], 90, 270, fill=WHITE, width=4)
    # small leaf sprouting at the top
    drw.arc([cx + 18, cy - 66, cx + 44, cy - 40], 180, 360, fill=WHITE, width=4)


def pic_tent(drw, cx, cy):
    drw.polygon([(cx - 52, cy + 34), (cx, cy - 36), (cx + 52, cy + 34)],
                fill=WHITE)
    # door slit
    drw.polygon([(cx - 11, cy + 34), (cx, cy + 4), (cx + 11, cy + 34)],
                fill=(72, 84, 106))
    # aid cross above
    drw.rectangle([cx + 30, cy - 48, cx + 38, cy - 28], fill=WHITE)
    drw.rectangle([cx + 20, cy - 43, cx + 48, cy - 35], fill=WHITE)
    # ground line
    drw.line([cx - 56, cy + 44, cx + 56, cy + 44], fill=WHITE, width=4)


def pic_chart(drw, cx, cy):
    # axes
    drw.line([cx - 52, cy + 44, cx + 54, cy + 44], fill=WHITE, width=5)
    drw.line([cx - 52, cy + 44, cx - 52, cy - 50], fill=WHITE, width=5)
    # falling line with arrowhead
    pts = [(cx - 44, cy - 34), (cx - 16, cy - 18), (cx + 6, cy - 26),
           (cx + 30, cy + 2), (cx + 48, cy + 30)]
    drw.line(pts, fill=WHITE, width=6, joint="curve")
    drw.polygon([(cx + 48, cy + 30), (cx + 30, cy + 26), (cx + 44, cy + 12)],
                fill=WHITE)


STORIES = [
    dict(kicker="UKRAINE", accent=(46, 94, 140), pic=pic_bridge,
         head="Ukraine brings down Kerch Bridge road arch",
         body="The road arch fell into the strait; Russia says it shot down 1,441 drones overnight."),
    dict(kicker="MIDDLE EAST", accent=(179, 64, 42), pic=pic_tanker,
         head="U.S. strikes Qeshm Island; tankers hit mines",
         body="U.S. jets hit an IRGC missile site; Iran says three tankers struck mines in Hormuz."),
    dict(kicker="ASIA", accent=(31, 110, 107), pic=pic_jet,
         head="Russian jets breach Japan's airspace",
         body="Two suspected Russian planes entered airspace off Fukuoka; the first breach since 2024."),
    dict(kicker="CLIMATE", accent=(46, 125, 50), pic=pic_globe,
         head="COP31 draft urges faster fossil-fuel exit",
         body="Ministers in Antalya began answering a draft urging a faster fossil-fuel phaseout."),
    dict(kicker="GAZA", accent=(140, 107, 31), pic=pic_tent,
         head="West presses Israel to open Gaza aid routes",
         body="Four nations urged Israel to let aid in; WHO warned of illness as winter floods arrive."),
    dict(kicker="MARKETS", accent=(106, 76, 147), pic=pic_chart,
         head="Wall Street slides; Nasdaq enters correction",
         body="U.S. stocks fell sharply and Brent crude dropped 3.6% as supply outpaced demand."),
]


def draw_card(drw, x, y, w, h, story):
    drw.rectangle([x, y, x + w, y + h], fill=CARD, outline=EDGE, width=2)
    band_w = 150
    drw.rectangle([x + 2, y + 2, x + band_w, y + h - 2], fill=story["accent"])
    story["pic"](drw, x + band_w // 2 + 1, y + h // 2)
    tx = x + band_w + 18
    tw = w - band_w - 36
    cy = y + 16
    drw.text((tx, cy), story["kicker"], font=F_KICK, fill=story["accent"])
    cy += 30
    for line in wrap(story["head"], F_HEAD, tw)[:3]:
        drw.text((tx, cy), line, font=F_HEAD, fill=INK)
        cy += 33
    cy += 4
    for line in wrap(story["body"], F_BODY, tw)[:3]:
        drw.text((tx, cy), line, font=F_BODY, fill=BODY)
        cy += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    drw = ImageDraw.Draw(img)

    # ---- masthead ----
    drw.rectangle([0, 0, W, 148], fill=NAVY)
    tracked(drw, W // 2, 22, "THE WORLD IN ONE IMAGE", F_TOP, GOLD, gap=8)
    date = "TUESDAY, 17 NOVEMBER 2026"
    size = 56
    while size > 30:
        fnt = load("DejaVuSerif-Bold.ttf", size)
        if fnt.getlength(date) <= W - 48:
            break
        size -= 2
    dw = fnt.getlength(date)
    drw.text(((W - dw) / 2, 56), date, font=fnt, fill=WHITE)
    drw.rectangle([0, 142, W, 148], fill=RED)

    # ---- story grid: 2 columns x 3 rows ----
    gx, gy = 16, 164
    cw, ch, gap = 488, 252, 16
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_card(drw, gx + col * (cw + gap), gy + row * (ch + gap),
                  cw, ch, story)

    # ---- footer ----
    fy = gy + 3 * ch + 2 * gap
    drw.line([16, fy + 8, W - 16, fy + 8], fill=EDGE, width=2)
    foot = "Reported on 17 November 2026  ·  Sources: AP · Reuters · Al Jazeera · NHK · Dawn · RNZ"
    fw = F_FOOT.getlength(foot)
    drw.text(((W - fw) / 2, fy + 22), foot, font=F_FOOT, fill=BODY)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
