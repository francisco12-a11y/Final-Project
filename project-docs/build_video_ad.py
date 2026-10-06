#!/usr/bin/env python3
"""Slideshow video ad — 1080x1920 MP4, 6 slides, Ken Burns zoom on photos.
Text overlays are pre-rendered once per slide (static, sharp) while only the
photo layer zooms. Silent: Fran adds music in CapCut (one import).
Output: /home/fran/Descargas/FP_FranciscoBuiras_L13_Ads/FP_FranciscoBuiras_VideoAd_1080x1920.mp4
Slides also exported to .../slides/ (they double as the Meta carousel).
"""
import os
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/fran/Descargas/FP_FranciscoBuiras_L13_Ads/base-images"
OPW = "/home/fran/Descargas/FP_FranciscoBuiras_L14_Imagery/operator-week.jpg"
OUTDIR = "/home/fran/Descargas/FP_FranciscoBuiras_L13_Ads"
SLIDES = f"{OUTDIR}/slides"
FONTS = "/tmp/adfonts"
W, H, FPS = 1080, 1920, 30
os.makedirs(SLIDES, exist_ok=True)

EMERALD = (16, 185, 129)
MINT = (110, 231, 183)
WHITE = (240, 244, 248)
SUB = (195, 206, 218)
DARK = (5, 10, 14)
PANEL = (11, 17, 25)
URL_TEXT = "francisco12-a11y.github.io/Final-Project"


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


def top_scrim(w, h):
    ov = Image.new("L", (1, h))
    px = ov.load()
    for y in range(h):
        t = y / h
        a = int(245 * (1 - min(1, t / 0.46)) ** 1.15) + 20
        px[0, y] = min(250, a)
    return Image.new("RGB", (w, h), DARK), ov.resize((w, h))


def wrap(draw, text, fnt, maxw):
    words = text.split(" ")
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_headline(d, text, y, size=88, maxw=912, emerald_part=None):
    """White headline with an emerald tail. emerald_part = substring that renders emerald."""
    fh = jakarta(size, 800)
    # split into white part + emerald part at the marker
    if emerald_part and emerald_part in text:
        white_txt = text[: text.index(emerald_part)].strip()
        em_txt = emerald_part
    else:
        white_txt, em_txt = text, None
    wl = wrap(d, white_txt, fh, maxw) if white_txt else []
    el = wrap(d, em_txt, fh, maxw) if em_txt else []
    for ln in wl:
        d.text((84, y), ln, font=fh, fill=WHITE)
        y += int(size * 1.14)
    for ln in el:
        d.text((84, y), ln, font=fh, fill=EMERALD)
        y += int(size * 1.14)
    return y


def draw_sub(d, text, y, size=38):
    fs = dmsans(size, 500)
    for ln in wrap(d, text, fs, 912):
        d.text((84, y), ln, font=fs, fill=SUB)
        y += int(size * 1.35)
    return y


def eyebrow(d, y=96):
    fe = jakarta(27, 700)
    x = draw_tracked(d, (84, y), "PARETO TALENT", fe, MINT, 6)
    draw_tracked(d, (x + 14, y), "·  FREE TEST", fe, SUB, 6)


def draw_tracked(d, xy, text, fnt, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking
    return x


def cta_pill(label="Take the 2-Minute Test", fsize=40):
    f = jakarta(fsize, 800)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = tmp.textlength(label, font=f)
    wp, hp = int(tw + 160), 104
    pill = Image.new("RGBA", (wp, hp), (0, 0, 0, 0))
    d = ImageDraw.Draw(pill)
    d.rounded_rectangle([0, 0, wp - 1, hp - 1], radius=hp // 2, fill=EMERALD)
    d.text((66, (hp - f.size) / 2 - 4), label, font=f, fill=DARK)
    ax = 66 + tw + 36
    d.line([(ax, hp / 2 - 12), (ax + 22, hp / 2), (ax, hp / 2 + 12)], fill=DARK, width=8, joint="curve")
    return pill


def photo_slide(img_path, headline, em, sub, bias=0.5, name="s.png", dur=3.0):
    photo = cover(Image.open(img_path).convert("RGB"), W, H, bias=bias)
    canvas = Image.blend(photo, Image.new("RGB", (W, H), DARK), 0.15)
    dark, alpha = top_scrim(W, H)
    canvas.paste(dark, (0, 0), alpha)
    d = ImageDraw.Draw(canvas)
    eyebrow(d)
    y = 190
    y = draw_headline(d, headline, y, emerald_part=em)
    y = draw_sub(d, sub, y + 14)
    canvas.save(f"{SLIDES}/{name}")
    return canvas, f"{SLIDES}/{name}"


def card_slide(headline, em, sub, shot_path, card_w, name, dur=3.0):
    canvas = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(canvas)
    d.ellipse([84, 150, 116, 182], fill=EMERALD)
    eyebrow(d, y=210)
    y = 300
    y = draw_headline(d, headline, y, size=84, emerald_part=em)
    y = draw_sub(d, sub, y + 10)
    shot = Image.open(shot_path).convert("RGB")
    sw = card_w
    sh = int(shot.size[1] * sw / shot.size[0])
    shot = shot.resize((sw, sh), Image.LANCZOS)
    pad = 22
    card = Image.new("RGB", (sw + pad * 2, sh + pad * 2), PANEL)
    card.paste(shot, (pad, pad))
    dd = ImageDraw.Draw(card)
    dd.rounded_rectangle([0, 0, card.size[0] - 1, card.size[1] - 1], radius=26, outline=EMERALD, width=3)
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card.size[0] - 1, card.size[1] - 1], radius=26, fill=255)
    cy = min(y + 40, H - card.size[1] - 200)
    canvas.paste(card, ((W - card.size[0]) // 2, cy), mask)
    canvas.save(f"{SLIDES}/{name}")
    return canvas, f"{SLIDES}/{name}"


def end_slide(name):
    canvas = Image.new("RGB", (W, H), DARK)
    d = ImageDraw.Draw(canvas)
    d.ellipse([84, 620, 128, 664], fill=EMERALD)
    eyebrow(d, y=680)
    y = 760
    y = draw_headline(d, "Take the 2-minute test.", y, size=104)
    y = draw_sub(d, "Free. The Right Hand Starter Kit is yours either way.", y + 20, size=42)
    pill = cta_pill()
    canvas.paste(pill, (84, y + 60), pill)
    fu = dmsans(30, 500)
    d.text((84, y + 60 + 150), URL_TEXT, font=fu, fill=SUB)
    canvas.save(f"{SLIDES}/{name}")
    return canvas, f"{SLIDES}/{name}"


# ---------- render the 6 slides ----------
photo_slides = [
    dict(img_path=f"{BASE}/dan.jpg", headline="$10/hr work. $100/hr job.", em="$100/hr job.",
         sub="Take the test. See your 15 lost hours.", bias=0.42, name="s1-hook.png", dur=3.2),
    dict(img_path=f"{OPW.rsplit(chr(47), 1)[0]}/va-bench.jpg", headline="Inbox. Calendar. Follow-ups.", em=None,
         sub="The assistant job is eating your week.", bias=0.4, name="s2-pain.png", dur=2.6),
]
s1, s1p = photo_slide(**photo_slides[0])
s2, s2p = photo_slide(**photo_slides[1])
s3, s3p = card_slide("A test does the math.", None,
                     "Six questions. Two minutes. No email to see your number.",
                     "/tmp/slide_q1.png", 900, "s3-test.png")
s4, s4p = card_slide("37 hrs/wk = $31,820/mo.", "$31,820/mo.",
                     "Your real number, on the spot.",
                     "/tmp/slide_result.png", 860, "s4-number.png")
s5, s5p = photo_slide(OPW, "A Right Hand takes the hours back.", "Right Hand",
                      "Vetted · AI-trained · matched in 24 hours.", bias=0.5, name="s5-rh.png")
s6, s6p = end_slide("s6-cta.png")

SLIDE_DEFS = [
    (s1, s1p, photo_slides[0]["dur"], True),
    (s2, s2p, photo_slides[1]["dur"], True),
    (s3, s3p, 3.0, False),
    (s4, s4p, 3.8, False),
    (s5, s5p, 2.8, True),
    (s6, s6p, 3.6, False),
]

# ---------- assemble with Ken Burns ----------
writer = imageio_ffmpeg.write_frames(
    f"{OUTDIR}/FP_FranciscoBuiras_VideoAd_1080x1920.mp4", (W, H), fps=FPS,
    pix_fmt_out="yuv420p", output_params=["-crf", "21", "-preset", "medium"],
)
writer.send(None)
total = sum(d for _, _, d, _ in SLIDE_DEFS)
n = 0
for base, overlay_path, dur, zoom in SLIDE_DEFS:
    frames = int(dur * FPS)
    ov = Image.open(overlay_path).convert("RGBA")
    for i in range(frames):
        p = i / max(1, frames - 1)
        if zoom:
            z = 1.0 + 0.065 * p
            cw, ch = int(W / z), int(H / z)
            x0 = (W - cw) // 2
            y0 = int((H - ch) * 0.45)
            frame = base.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
        else:
            frame = base.copy()
        frame.paste(ov, (0, 0), ov)
        writer.send(np.asarray(frame))
        n += 1
        if n % 90 == 0:
            print(f"frame {n} / {int(total * FPS)}")
writer.close()
print("DONE", total, "s,", n, "frames")
print(f"{OUTDIR}/FP_FranciscoBuiras_VideoAd_1080x1920.mp4", os.path.getsize(f"{OUTDIR}/FP_FranciscoBuiras_VideoAd_1080x1920.mp4"), "bytes")
