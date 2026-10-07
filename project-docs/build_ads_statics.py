#!/usr/bin/env python3
"""Build the 5 static Facebook ads — layout v5.
Photo-forward: full-bleed image, small text block in the top-left clear zone,
each photo cropped (x_bias) so the person sits away from the text column.
Feed 1080x1080 + story 1080x1920 + CTA-label variants on Ad 1.
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
SUB = (205, 214, 224)
URLCOL = (163, 177, 192)
DARK = (5, 10, 14)

# x_bias shifts the crop window: LOW = person moves RIGHT (away from the left
# text column), HIGH = person moves LEFT.
ADS = [
    dict(key="ad1-dan", img=f"{BASE}/dan.jpg", x_bias=0.08,
         headline=[("$10/hr work.", "w"), ("\n$100/hr job.", "e")],
         sub="A Right Hand takes those hours back."),
    dict(key="ad2-vanessa", img=f"{BASE}/vanessa.jpg", x_bias=0.0,
         headline=[("Burned by a VA? ", "w"), ("Try a Right Hand.", "e")],
         sub="The test tells you what to hand off first."),
    dict(key="ad3-chris", img=f"{BASE}/chris.jpg", x_bias=0.05,
         headline=[("If you took a week off, ", "w"), ("would the business stop?", "e")],
         sub="Hand the first process to a Right Hand."),
    dict(key="ad4-sofia", img=f"{BASE}/sofia.jpg", x_bias=0.3,
         headline=[("You didn\u2019t leave your job ", "w"), ("to be your own assistant.", "e")],
         sub="Find your recoverable hours in 2 minutes."),
    dict(key="ad5-destination", img=OPW, x_bias=0.52,
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


def cover(img, w, h, x_bias=0.5):
    iw, ih = img.size
    s = max(w / iw, h / ih)
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = int((nw - w) * x_bias)
    return img.crop((x, 0, x + w, min(h, nh)))


def scrims(w, h):
    """Soft top gradient for the headline, soft bottom for the CTA. Clear middle."""
    ov = Image.new("L", (1, h))
    px = ov.load()
    for y in range(h):
        t = y / h
        if t < 0.30:
            a = int(185 * (1 - t / 0.30) ** 1.1) + 25
        elif t > 0.74:
            a = int(190 * ((t - 0.74) / 0.26) ** 1.1) + 25
        else:
            a = 25
        px[0, y] = min(225, a)
    return Image.new("RGB", (w, h), DARK), ov.resize((w, h))


def wrap_segments(draw, segments, fnt, maxw):
    words = []
    for t, c in segments:
        tokens = t.replace("\n", " \n ").split(" ")
        for wd in tokens:
            if wd == "\n":
                words.append(("\n", c))
            elif wd:
                words.append((wd, c))
    lines, cur, curw = [], [], 0.0
    space = draw.textlength(" ", font=fnt)
    for wd, c in words:
        if wd == "\n":
            lines.append(cur)
            cur, curw = [], 0.0
            continue
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
    wp, hp = int(tw + 132), int(fsize * 2.45)
    pill = Image.new("RGBA", (wp, hp), (0, 0, 0, 0))
    d = ImageDraw.Draw(pill)
    d.rounded_rectangle([0, 0, wp - 1, hp - 1], radius=hp // 2, fill=EMERALD)
    d.text((52, (hp - f.size) / 2 - 4), label, font=f, fill=DARK)
    ax = 52 + tw + 30
    ay = hp / 2
    d.line([(ax, ay - 10), (ax + 18, ay), (ax, ay + 10)], fill=DARK, width=6, joint="curve")
    return pill


def build(ad, W, H, name, cta_label=CTA_LABEL):
    canvas = cover(Image.open(ad["img"]).convert("RGB"), W, H, x_bias=ad["x_bias"])
    canvas = Image.blend(canvas, Image.new("RGB", (W, H), DARK), 0.10)
    dark, alpha = scrims(W, H)
    canvas.paste(dark, (0, 0), alpha)
    d = ImageDraw.Draw(canvas)

    m = int(W * 0.068)
    textw = int(W * 0.60)          # text column: left 60%, person lives in the right 40%

    fe = jakarta(int(W * 0.020), 700)
    draw_tracked(d, (m, int(H * 0.045)), "PARETO TALENT", fe, MINT, int(W * 0.005))
    ew = sum(d.textlength(c, font=fe) + int(W * 0.005) for c in "PARETO TALENT")
    draw_tracked(d, (m + ew + int(W * 0.010), int(H * 0.045)), "·  FREE TEST", fe, SUB, int(W * 0.005))

    size = int(W * 0.056)          # smaller headline
    max_lines = 2
    while size > int(W * 0.040):
        fh = jakarta(size, 800)
        lines = wrap_segments(d, ad["headline"], fh, textw)
        if len(lines) <= max_lines:
            break
        size -= 3
    fh = jakarta(size, 800)
    lines = wrap_segments(d, ad["headline"], fh, textw)
    lead = int(size * 1.15)
    y = int(H * 0.098)
    for line in lines:
        x = m
        for wd, c in line:
            d.text((x, y), wd, font=fh, fill=EMERALD if c == "e" else WHITE)
            x += d.textlength(wd + " ", font=fh)
        y += lead

    y += int(size * 0.28)
    fs = dmsans(int(W * 0.026), 500)
    for line in wrap_segments(d, [(ad["sub"], "s")], fs, textw):
        x = m
        for wd, c in line:
            d.text((x, y), wd, font=fs, fill=SUB)
            x += d.textlength(wd + " ", font=fs)
        y += int(W * 0.04)

    pill = cta_pill(cta_label, int(W * 0.028))
    py = H - int(H * 0.052) - pill.size[1]
    canvas.paste(pill, (m, py), pill)

    fsize = int(W * 0.019)
    while fsize > 13 and d.textlength(URL_TEXT, font=dmsans(fsize, 500)) > textw:
        fsize -= 1
    d.text((m, py + pill.size[1] + int(H * 0.016)), URL_TEXT, font=dmsans(fsize, 500), fill=URLCOL)

    canvas.save(f"{OUT}/{name}", quality=92)
    print("saved", name)


for ad in ADS:
    build(ad, 1080, 1080, f"{ad['key']}-feed-1080x1080.png")
    build(ad, 1080, 1920, f"{ad['key']}-story-1080x1920.png")

os.makedirs(f"{OUT}/cta-variants", exist_ok=True)
import glob
for old in glob.glob(f"{OUT}/cta-variants/*.png"):
    os.remove(old)
for label in CTA_VARIANTS:
    fn = "variant-" + label.lower().replace(" ", "-")[:40].replace("—", "-") + ".png"
    build(ADS[0], 1080, 1080, f"cta-variants/{fn}", cta_label=label)

sheet = Image.new("RGB", (540 * 5, 540), (11, 17, 25))
for i, ad in enumerate(ADS):
    im = Image.open(f"{OUT}/{ad['key']}-feed-1080x1080.png").resize((540, 540))
    sheet.paste(im, (540 * i, 0))
sheet.save("/tmp/ads_review.png")

vsheet = Image.new("RGB", (360 * 5, 360), (11, 17, 25))
for i, label in enumerate(CTA_VARIANTS):
    fn = "variant-" + label.lower().replace(" ", "-")[:40].replace("—", "-") + ".png"
    im = Image.open(f"{OUT}/cta-variants/{fn}").resize((360, 360))
    vsheet.paste(im, (360 * i, 0))
vsheet.save("/tmp/cta_variants_review.png")

ssheet = Image.new("RGB", (243 * 5, 432), (11, 17, 25))
for i, ad in enumerate(ADS):
    im = Image.open(f"{OUT}/{ad['key']}-story-1080x1920.png").resize((243, 432))
    ssheet.paste(im, (243 * i, 0))
ssheet.save("/tmp/ads_review_story.png")
print("sheets ok")
