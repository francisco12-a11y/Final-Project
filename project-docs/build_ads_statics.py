#!/usr/bin/env python3
"""Build the 5 static Facebook ads (feed 1080x1080 + story 1080x1920).
Layout v2: split panel — text lives on a solid dark panel, never over the person.
Brand: Pareto Talent — dark #050A0E, emerald #10B981, Plus Jakarta Sans / DM Sans.
Output: /home/fran/Descargas/FP_FranciscoBuiras_L13_Ads/statics/
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/fran/Descargas/FP_FranciscoBuiras_L13_Ads/base-images"
OPW = "/home/fran/Descargas/FP_FranciscoBuiras_L14_Imagery/operator-week.jpg"
OUT = "/home/fran/Descargas/FP_FranciscoBuiras_L13_Ads/statics"
FONTS = "/tmp/adfonts"
URL_TEXT = "francisco12-a11y.github.io/Final-Project"
CTA_LABEL = "Take the 2-Minute Test"
os.makedirs(OUT, exist_ok=True)

EMERALD = (16, 185, 129)
MINT = (110, 231, 183)
WHITE = (240, 244, 248)
SUB = (195, 206, 218)
URLCOL = (148, 163, 184)
DARK = (5, 10, 14)

ADS = [
    dict(key="ad1-dan", img=f"{BASE}/dan.jpg",
         headline=[("$10/hr work. ", "w"), ("$100/hr job.", "e")],
         sub="A Right Hand takes those hours back. Find yours in 2 minutes."),
    dict(key="ad2-vanessa", img=f"{BASE}/vanessa.jpg",
         headline=[("Burned by a VA? ", "w"), ("Try a Right Hand.", "e")],
         sub="The 2-minute test tells you what to hand off first."),
    dict(key="ad3-chris", img=f"{BASE}/chris.jpg",
         headline=[("If you took a week off, would ", "w"), ("the business stop?", "e")],
         sub="Hand the first process to a Right Hand."),
    dict(key="ad4-sofia", img=f"{BASE}/sofia.jpg",
         headline=[("You didn\u2019t leave your job to be ", "w"), ("your own assistant.", "e")],
         sub="Find your recoverable hours in 2 minutes."),
    dict(key="ad5-destination", img=OPW,
         headline=[("15 hours is a sales channel. ", "w"), ("Or your life back.", "e")],
         sub="Free 2-minute founder test."),
]


def font(path, size, weight=None, axes=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    if axes is not None:
        try:
            f.set_variation_by_axes(axes)
        except Exception:
            pass
    return f


def jakarta(size, weight=800):
    return font(f"{FONTS}/jakarta.ttf", size, weight=weight)


def dmsans(size, weight=500):
    return font(f"{FONTS}/dmsans.ttf", size, axes=[14, weight])


def cover(img, w, h, bias=0.5):
    iw, ih = img.size
    s = max(w / iw, h / ih)
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = int((nh - h) * bias)
    return img.crop((x, y, x + w, y + h))


def wrap_segments(segments, fnt, maxw, draw):
    words = []
    for text, c in segments:
        for wd in text.split(" "):
            if wd:
                words.append((wd, c))
    lines, cur, curw = [], [], 0.0
    space = draw.textlength(" ", font=fnt)
    for wd, c in words:
        wl = draw.textlength(wd, font=fnt)
        add = wl if not cur else wl + space
        if cur and curw + add > maxw:
            lines.append(cur)
            cur, curw = [(wd, c)], wl
        else:
            cur.append((wd, c))
            curw += add
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, xy, text, fnt, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def cta_pill(label, fsize=36):
    f = jakarta(fsize, 800)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = tmp.textlength(label, font=f)
    w_pill = int(tw + 150)
    h_pill = 96
    pill = Image.new("RGBA", (w_pill, h_pill), (0, 0, 0, 0))
    d = ImageDraw.Draw(pill)
    d.rounded_rectangle([0, 0, w_pill - 1, h_pill - 1], radius=h_pill // 2, fill=EMERALD)
    d.text((62, (h_pill - f.size) / 2 - 4), label, font=f, fill=DARK)
    ax = 62 + tw + 34
    ay = h_pill / 2
    d.line([(ax, ay - 11), (ax + 20, ay), (ax, ay + 11)], fill=DARK, width=7, joint="curve")
    return pill


def build(ad, W, H, name, horizontal=True):
    """horizontal=True (feed): photo right, text panel left.
    horizontal=False (story): photo top, text panel bottom."""
    canvas = Image.new("RGB", (W, H), DARK)

    if horizontal:
        pw = int(W * 0.44)                       # photo width
        photo = cover(Image.open(ad["img"]).convert("RGB"), pw, H, bias=0.32)
        canvas.paste(photo, (W - pw, 0))
        d = ImageDraw.Draw(canvas)
        d.rectangle([W - pw - 6, 0, W - pw, H], fill=EMERALD)  # seam
        px0, py0, pw_, ph_ = 0, 0, W - pw - 6, H
        m = int(W * 0.058)
    else:
        ph = int(H * 0.40)                       # photo height
        photo = cover(Image.open(ad["img"]).convert("RGB"), W, ph, bias=0.3)
        canvas.paste(photo, (0, 0))
        d = ImageDraw.Draw(canvas)
        d.rectangle([0, ph, W, ph + 6], fill=EMERALD)
        px0, py0, pw_, ph_ = 0, ph + 6, W, H - ph - 6
        m = int(W * 0.075)

    tw_, th_ = pw_, ph_
    d = ImageDraw.Draw(canvas)

    # eyebrow
    fe = jakarta(int(W * 0.022), 700)
    ey = py0 + int(th_ * 0.075)
    draw_tracked(d, (px0 + m, ey), "PARETO TALENT", fe, MINT, int(W * 0.0055))
    ew = sum(d.textlength(c, font=fe) + int(W * 0.0055) for c in "PARETO TALENT")
    draw_tracked(d, (px0 + m + ew + int(W * 0.011), ey), "·  FREE TEST", fe, SUB, int(W * 0.0055))

    # headline (auto-size to fit the panel)
    maxw = tw_ - 2 * m
    size = int(W * 0.062)
    max_lines = 4 if horizontal else 3
    while size > int(W * 0.038):
        fhl = jakarta(size, 800)
        lines = wrap_segments(ad["headline"], fhl, maxw, d)
        if len(lines) <= max_lines:
            break
        size -= 3
    fh = jakarta(size, 800)
    lines = wrap_segments(ad["headline"], fh, maxw, d)
    lead = int(size * 1.16)

    # subline
    fs = dmsans(int(W * 0.0265), 500)
    sub_lines = wrap_segments([(ad["sub"], "s")], fs, maxw, d)
    sub_lead = int(W * 0.038)

    # url line (auto-fit inside the panel)
    usize = int(W * 0.0225)
    while usize > 14:
        fu = dmsans(usize, 500)
        if d.textlength(URL_TEXT, font=fu) <= maxw:
            break
        usize -= 1
    fu = dmsans(usize, 500)

    # CTA pill
    pill = cta_pill(CTA_LABEL, int(W * 0.033))
    psc = int(pill.size[0] * 0.78)  # scale pill for panel width if needed
    while pill.size[0] > maxw:
        pill = pill.resize((int(pill.size[0] * 0.92), int(pill.size[1] * 0.92)))

    # stack everything vertically centered in the panel between eyebrow and bottom
    url_y = py0 + th_ - int(th_ * 0.07) - fu.size
    pill_y = url_y - int(W * 0.018) - pill.size[1]
    sub_h = len(sub_lines) * sub_lead
    head_h = len(lines) * lead
    sub_y = pill_y - int(W * 0.036) - sub_h
    head_y = sub_y - int(size * 0.42) - head_h
    if head_y < ey + fe.size + int(W * 0.05):   # squeeze from top if overcrowded
        head_y = ey + fe.size + int(W * 0.05)

    for line in lines:
        x = px0 + m
        for wd, c in line:
            d.text((x, head_y), wd, font=fh, fill=EMERALD if c == "e" else WHITE)
            x += d.textlength(wd + " ", font=fh)
        head_y += lead

    yy = sub_y
    for line in sub_lines:
        x = px0 + m
        for wd, c in line:
            d.text((x, yy), wd, font=fs, fill=SUB)
            x += d.textlength(wd + " ", font=fs)
        yy += sub_lead

    canvas.paste(pill, (px0 + m, pill_y), pill)
    d.text((px0 + m, url_y), URL_TEXT, font=fu, fill=URLCOL)

    canvas.save(f"{OUT}/{name}", quality=92)
    print("saved", name)


for ad in ADS:
    build(ad, 1080, 1080, f"{ad['key']}-feed-1080x1080.png", horizontal=True)
    build(ad, 1080, 1920, f"{ad['key']}-story-1080x1920.png", horizontal=False)

# contact sheets for review
sheet = Image.new("RGB", (540 * 5, 540), (11, 17, 25))
for i, ad in enumerate(ADS):
    im = Image.open(f"{OUT}/{ad['key']}-feed-1080x1080.png").resize((540, 540))
    sheet.paste(im, (540 * i, 0))
sheet.save("/tmp/ads_review.png")
sheet2 = Image.new("RGB", (243 * 5, 432), (11, 17, 25))
for i, ad in enumerate(ADS):
    im = Image.open(f"{OUT}/{ad['key']}-story-1080x1920.png").resize((243, 432))
    sheet2.paste(im, (243 * i, 0))
sheet2.save("/tmp/ads_review_story.png")
print("sheets ok")
