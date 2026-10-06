#!/usr/bin/env python3
"""Build the 5 static Facebook ads — layout v3.
Full-bleed photo, text locked to the top clear zone (never over the person),
CTA pill + landing URL bottom-left. Feed 1080x1080 + story 1080x1920.
Also renders a CTA-label variant sheet on Ad 1 for Fran to pick from.
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
    dict(key="ad1-dan", img=f"{BASE}/dan.jpg", bias=0.45,
         headline=[("$10/hr work. ", "w"), ("$100/hr job.", "e")],
         sub="A Right Hand takes those hours back."),
    dict(key="ad2-vanessa", img=f"{BASE}/vanessa.jpg", bias=0.35,
         headline=[("Burned by a VA? ", "w"), ("Try a Right Hand.", "e")],
         sub="The 2-minute test tells you what to hand off first."),
    dict(key="ad3-chris", img=f"{BASE}/chris.jpg", bias=0.3,
         headline=[("If you took a week off, would ", "w"), ("the business stop?", "e")],
         sub="Hand the first process to a Right Hand."),
    dict(key="ad4-sofia", img=f"{BASE}/sofia.jpg", bias=0.35,
         headline=[("You didn\u2019t leave your job to be ", "w"), ("your own assistant.", "e")],
         sub="Find your recoverable hours in 2 minutes."),
    dict(key="ad5-destination", img=OPW, bias=0.5,
         headline=[("15 hours is a sales channel. ", "w"), ("Or your life back.", "e")],
         sub="Free 2-minute founder test."),
]

CTA_VARIANTS = ["Take the 2-Minute Test", "Get Your Number", "Meet Your Right Hand",
                "Start the Test — It's Free", "See My Result"]


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


def cover(img, w, h, y_bias=0.5):
    iw, ih = img.size
    s = max(w / iw, h / ih)
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    return img.crop(((nw - w) // 2, int((nh - h) * y_bias), (nw - w) // 2 + w, int((nh - h) * y_bias) + h))


def scrim(w, h):
    """Dark band top (for headline), soft dark at bottom (for CTA/URL), clear middle."""
    ov = Image.new("L", (1, h))
    px = ov.load()
    for y in range(h):
        t = y / h
        if t < 0.42:
            a = int(235 * (1 - t / 0.42) ** 1.1) + 40
        elif t > 0.72:
            a = int(210 * ((t - 0.72) / 0.28) ** 1.1) + 40
        else:
            a = 40
        px[0, y] = min(245, a)
    return Image.new("RGB", (w, h), DARK), ov.resize((w, h))


def wrap_segments(draw, segments, fnt, maxw):
    words = []
    for t, c in segments:
        for wd in t.split(" "):
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


def cta_pill(label, fsize):
    f = jakarta(fsize, 800)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = tmp.textlength(label, font=f)
    wp, hp = int(tw + 150), int(fsize * 2.6)
    pill = Image.new("RGBA", (wp, hp), (0, 0, 0, 0))
    d = ImageDraw.Draw(pill)
    d.rounded_rectangle([0, 0, wp - 1, hp - 1], radius=hp // 2, fill=EMERALD)
    d.text((60, (hp - f.size) / 2 - 4), label, font=f, fill=DARK)
    ax = 60 + tw + 32
    ay = hp / 2
    d.line([(ax, ay - 11), (ax + 20, ay), (ax, ay + 11)], fill=DARK, width=7, joint="curve")
    return pill


def build(ad, W, H, name, cta_label=CTA_LABEL):
    canvas = cover(Image.open(ad["img"]).convert("RGB"), W, H, y_bias=ad["bias"])
    canvas = Image.blend(canvas, Image.new("RGB", (W, H), DARK), 0.15)
    dark, alpha = scrim(W, H)
    canvas.paste(dark, (0, 0), alpha)
    d = ImageDraw.Draw(canvas)

    m = int(W * 0.078)
    maxw = W - 2 * m

    fe = jakarta(int(W * 0.024), 700)
    draw_tracked(d, (m, int(H * 0.048)), "PARETO TALENT", fe, MINT, int(W * 0.006))
    ew = sum(d.textlength(c, font=fe) + int(W * 0.006) for c in "PARETO TALENT")
    draw_tracked(d, (m + ew + int(W * 0.012), int(H * 0.048)), "·  FREE TEST", fe, SUB, int(W * 0.006))

    size = int(W * 0.088)
    max_lines = 3
    while size > int(W * 0.05):
        fh = jakarta(size, 800)
        lines = wrap_segments(d, ad["headline"], fh, maxw)
        if len(lines) <= max_lines:
            break
        size -= 4
    fh = jakarta(size, 800)
    lines = wrap_segments(d, ad["headline"], fh, maxw)
    lead = int(size * 1.14)
    y = int(H * 0.105)
    for line in lines:
        x = m
        for wd, c in line:
            d.text((x, y), wd, font=fh, fill=EMERALD if c == "e" else WHITE)
            x += d.textlength(wd + " ", font=fh)
        y += lead

    y += int(size * 0.3)
    fs = dmsans(int(W * 0.034), 500)
    for line in wrap_segments(d, [(ad["sub"], "s")], fs, maxw):
        x = m
        for wd, c in line:
            d.text((x, y), wd, font=fs, fill=SUB)
            x += d.textlength(wd + " ", font=fs)
        y += int(W * 0.048)

    pill = cta_pill(cta_label, int(W * 0.033))
    py = H - int(H * 0.075) - pill.size[1]
    canvas.paste(pill, (m, py), pill)

    fsize = int(W * 0.0225)
    while fsize > 14 and d.textlength(URL_TEXT, font=dmsans(fsize, 500)) > maxw:
        fsize -= 1
    d.text((m, py + pill.size[1] + int(H * 0.018)), URL_TEXT, font=dmsans(fsize, 500), fill=URLCOL)

    canvas.save(f"{OUT}/{name}", quality=92)
    print("saved", name)


for ad in ADS:
    build(ad, 1080, 1080, f"{ad['key']}-feed-1080x1080.png")
    build(ad, 1080, 1920, f"{ad['key']}-story-1080x1920.png")

# CTA label variants on Ad 1 (feed) for Fran to pick
os.makedirs(f"{OUT}/cta-variants", exist_ok=True)
for label in CTA_VARIANTS:
    build(ADS[0], 1080, 1080, f"cta-variants/variant-{label.lower().replace(' ', '-').replace('—', '-').replace('--', '-')[:40]}.png", cta_label=label)

sheet = Image.new("RGB", (540 * 5, 540), (11, 17, 25))
for i, ad in enumerate(ADS):
    im = Image.open(f"{OUT}/{ad['key']}-feed-1080x1080.png").resize((540, 540))
    sheet.paste(im, (540 * i, 0))
sheet.save("/tmp/ads_review.png")

vsheet = Image.new("RGB", (360 * 5, 360), (11, 17, 25))
for i, label in enumerate(CTA_VARIANTS):
    fn = f"variant-{label.lower().replace(' ', '-').replace('—', '-').replace('--', '-')[:40]}.png"
    im = Image.open(f"{OUT}/cta-variants/{fn}").resize((360, 360))
    vsheet.paste(im, (360 * i, 0))
vsheet.save("/tmp/cta_variants_review.png")
print("sheets ok")
