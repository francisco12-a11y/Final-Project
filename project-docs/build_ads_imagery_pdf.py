#!/usr/bin/env python3
"""Ads & Imagery Pack PDF (L13 + L14).
Output: /home/fran/Descargas/Pareto_FinalProject_Ads_and_Imagery.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Table, TableStyle, KeepTogether)

OUT = "/home/fran/Descargas/Pareto_FinalProject_Ads_and_Imagery.pdf"

BRAND = HexColor("#10B981"); DEEP = HexColor("#065F46"); INK = HexColor("#0F172A")
BODY = HexColor("#334155"); MUTED = HexColor("#64748B"); LINE = HexColor("#E2E8F0")
SOFT = HexColor("#F5F9F7"); TINT = HexColor("#EAF6F1"); DARK = HexColor("#0B1526")
MINT = HexColor("#6EE7B7")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

_FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Lib", f"{_FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lib-B", f"{_FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lib-I", f"{_FDIR}/LiberationSans-Italic.ttf"))


def st(name, **kw):
    base = dict(fontName="Lib", fontSize=9.5, leading=13.5, textColor=BODY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "h2kick": st("h2kick", fontName="Lib-B", fontSize=8, leading=11,
                 textColor=DEEP, spaceAfter=2),
    "h2": st("h2", fontName="Lib-B", fontSize=13, leading=17, textColor=INK,
             spaceAfter=5),
    "h3": st("h3", fontName="Lib-B", fontSize=10.5, leading=14, textColor=INK,
             spaceBefore=6, spaceAfter=3),
    "body": st("body"),
    "muted": st("muted", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": st("cell", fontSize=8.5, leading=11.5, textColor=BODY),
    "cellB": st("cellB", fontName="Lib-B", fontSize=8.5, leading=11.5,
                textColor=INK),
    "mail": st("mail", fontSize=9, leading=13, textColor=BODY),
    "mono": st("mono", fontName="Lib", fontSize=8, leading=11.5,
               textColor=DEEP),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def on_page(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 26 * mm, PAGE_W, 26 * mm, stroke=0, fill=1)
    c.setFillColor(MINT)
    c.setFont("Lib-B", 8)
    c.drawString(MARGIN, PAGE_H - 10 * mm,
                 "P A R E T O   T A L E N T   ·   F I N A L   P R O J E C T")
    c.setFillColor(white)
    c.setFont("Lib-B", 16)
    c.drawString(MARGIN, PAGE_H - 17 * mm, "Ads & Imagery Pack")
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 9)
    c.drawString(MARGIN, PAGE_H - 22.5 * mm,
                 "FP | Francisco Buiras | 5 persona ads (L13) + imagery prompt pack (L14) · five different arguments, five matching heroes")
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    c.setFillColor(MUTED); c.setFont("Lib", 7.5)
    c.drawString(MARGIN, 8 * mm,
                 "Copy-paste the ad text into Meta; generate the creatives from the prompts; export to the Drive folder with FP naming.")
    c.drawRightString(PAGE_W - MARGIN, 8 * mm, f"Page {c.getPageNumber()}")
    c.restoreState()


def boxed(flows, bg=SOFT, border=LINE, pad=10):
    t = Table([[flows]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad - 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 2),
    ]))
    return t


def ad_card(num, persona, angle, url, primary, headline, desc, creative):
    flows = [
        P(f"<b>AD {num} · {persona}</b>", "cellB"),
        P(f"Angle: {angle}", "muted"),
        Spacer(1, 4),
        P(f"<b>Primary text</b>", "cellB"),
        P(primary.replace("\n\n", "<br/><br/>"), "mail"),
        Spacer(1, 4),
        P(f"<b>Headline:</b> {headline} &nbsp;&nbsp; <b>Description:</b> {desc} &nbsp;&nbsp; <b>CTA:</b> See My Result", "cell"),
        P(f"<b>URL:</b> {url}", "mono"),
        Spacer(1, 4),
        P(f"<b>Creative:</b> {creative}", "muted"),
    ]
    return KeepTogether([boxed(flows), Spacer(1, 6)])


ADS = [
    (1, "Dan — The Drowning Operator", "time recovery and ROI; the bottleneck math",
     "https://francisco12-a11y.github.io/Final-Project/?p=dan",
     "You didn't build a company to spend your week on inbox triage.\n\nRun the 2-minute test: answer six questions about your week and see exactly how many hours you could hand off, what they're worth at founder rates, and which two tasks to give away first.\n\nNo email needed to see your number. The math takes two minutes and it's uncomfortable on purpose.",
     "The 2-minute test that finds your 15 lost hours",
     "Free test · instant result · full system pack by email",
     "Dan portrait, dark desk lit by monitor, \"16 hrs/wk\" overlaid in emerald"),
    (2, "Vanessa — Burned by a VA", "done-for-you vetting and training; the handoff is the fix",
     "https://francisco12-a11y.github.io/Final-Project/?p=vanessa",
     "Most founders who work with us swore off hiring first.\n\nThe story is always the same: hire cheap, no systems, three months managing instead of saving. The fix is boring — vetting, training, and a written handoff.\n\nTake the 2-minute test and find out what to hand off, what to systemize, and whether you're ready for a Right Hand who arrives pre-vetted and trained 40+ hours on the AI stack.",
     "Burned by a VA? Test what to hand off first",
     "2 minutes · no email to see your number · starter kit included",
     "Vanessa portrait reviewing a stack of VA resumes, skeptical, emerald accent light"),
    (3, "Chris — Chaos at Scale", "systems; the first process to cut loose",
     "https://francisco12-a11y.github.io/Final-Project/?p=chris",
     "If you took a week off, would the business stop?\n\nFor most founders at your stage the honest answer is yes, and the reason is that every process lives in your head.\n\nThe 2-minute test shows you which task to document first and hand off forever — with the script that makes the handoff stick. Six questions, instant result, no email to see your number.",
     "What breaks first when you step away? Find out in 2 minutes",
     "Free founder test · ranked handoff list · systems included",
     "Chris portrait mid-gesture in front of a chaotic whiteboard, sticky notes"),
    (4, "Sofia — Solo Until Now", "permission and leverage; you didn't leave your job to be your own assistant",
     "https://francisco12-a11y.github.io/Final-Project/?p=sofia",
     "You protected margin by doing everything yourself. It worked — until the calendar filled with $10/hour work and growth stalled.\n\nThere's a number hiding in your week. The 2-minute test finds it: how many hours are really assistant work, what they cost you at founder rates, and which two to hand off first.\n\nTwenty minutes of math, two minutes of questions, and a full systems pack by email. No email needed to see your number.",
     "You didn't leave your job to be your own assistant",
     "Find your recoverable hours in 2 minutes · free",
     "Sofia portrait closing her laptop early, golden hour, relieved"),
    (5, "The Destination — what the hours become", "time destination; the hours aren't the point, what they become is",
     "https://francisco12-a11y.github.io/Final-Project/",
     "15 hours a week is a new sales channel. Or your kid's every game this season. Or the product work you keep postponing.\n\nRight now those hours are inbox, scheduling, and follow-ups — work a trained operator should own.\n\nTake the 2-minute test: six questions, your recoverable-hours number on the spot, and a full systems pack by email. If the number is big enough, we'll show you how to get every hour back.",
     "15 hours is a sales channel. Or your life back.",
     "Free 2-minute founder test · instant result · systems pack by email",
     "Dark graphic: \"15 hrs/wk\" oversized in emerald, subline \"what would you do with them?\" (Canva, no AI face)"),
]

story = []

story.append(P("Why these are five different ads", "h2"))
story.append(P(
    "Each ad names a different cause of pain — growth, burned-before, no systems, "
    "solo bootstrap, time-destination — and promises a different first win: hours "
    "back, clean vetting, the first documented process, permission to delegate, "
    "what the hours become. Same funnel, five doors. Each URL carries a persona "
    "parameter, and the landing hero changes to echo the ad that brought the visitor."))

for num, persona, angle, url, primary, headline, desc, creative in ADS:
    story.append(Spacer(1, 2))
    story.append(ad_card(num, persona, angle, url, primary, headline, desc, creative))

story.append(Spacer(1, 4))
story.append(P("Imagery prompt pack (L14)", "h2"))
story.append(boxed([
    P("<b>Style system — append to every prompt</b>", "cellB"),
    Spacer(1, 3),
    P("photorealistic, 35mm lens, shallow depth of field, dark moody lighting "
      "with a single emerald green accent light, slightly desaturated cinematic "
      "grade, no text, no logos", "mail"),
]))
story.append(Spacer(1, 6))

PROMPTS = [
    ("portrait-dan.jpg · site, 4:3",
     "A Latin American male founder in his late 30s at a home-office desk late at night, face lit by a monitor full of spreadsheets and chat windows, three devices on the desk, coffee mug, posture composed but visibly overloaded, eyes on the screen"),
    ("portrait-vanessa.jpg · site, 4:3",
     "A Latina founder in her early 40s sitting at an office desk reviewing a tall stack of printed resumes, arms crossed, skeptical half-smile, laptop open to a hiring site, one emerald desk lamp lighting the resumes"),
    ("portrait-chris.jpg · site, 4:3",
     "A male founder in his mid 30s standing in front of a whiteboard covered in arrows and sticky notes, phone pressed to his ear, gesturing at the board, home office at dusk, single emerald lamp glow on the board"),
    ("portrait-sofia.jpg · site, 4:3",
     "A Latina founder in her early 30s closing a laptop at a tidy desk in golden-hour window light, relieved half-smile, notebook and single coffee cup, the only dark room in an otherwise bright scene"),
    ("operator-wide.jpg · site, 21:9",
     "A wide cinematic shot of a professional operations specialist at a minimal standing desk in a dark room, three monitors showing clean calendars, inboxes and dashboards, emerald screen glow lighting the scene, the desk impeccably organized, sense of calm control"),
]
for name, prompt in PROMPTS:
    story.append(KeepTogether([
        P(f"<b>{name}</b>", "cellB"),
        boxed([P(prompt, "mail")], bg=SOFT),
        Spacer(1, 5),
    ]))

story.append(Spacer(1, 2))
story.append(P("Ad creatives (1:1 or 4:5)", "h3"))
story.append(P(
    "Ads 1–4: generate the matching portrait at 4:5 with the same prompts, then "
    "add text overlays in Canva — Ad 1: \"16 hrs/wk\" in emerald, subline \"doing "
    "a $10/hour job\". Ad 2: \"Never again.\" + \"unless someone else did the "
    "vetting\". Ad 3: \"If you took a week off…\" + \"would the business stop?\". "
    "Ad 4: \"You didn't leave your job for this.\" + \"reclaim your 15 hours\". "
    "Ad 5 is a pure graphic on #050A0E: \"15 hrs/wk\" oversized in #10B981, "
    "subline \"what would you do with them?\", spark logo bottom corner, DM Sans bold."))
story.append(Spacer(1, 4))
story.append(boxed([
    P("<b>Export + naming</b>", "cellB"),
    Spacer(1, 3),
    P("Creatives: FP_FranciscoBuiras_Ad1.png … Ad5.png into Drive folder "
      "FP_FranciscoBuiras_L13_Ads. Site images: portrait-dan.jpg, "
      "portrait-vanessa.jpg, portrait-chris.jpg, portrait-sofia.jpg, "
      "operator-wide.jpg into public/site-assets/ — swap instructions are in "
      "project-docs/imagery-prompts.md.", "cell"),
]))


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=32 * mm, bottomMargin=16 * mm,
        title="Ads & Imagery Pack — Pareto Final Project",
        author="Francisco Buiras",
        subject="Five persona ads and the imagery prompt pack for the lead magnet funnel",
        creator="FP | Francisco Buiras | Ads & Imagery",
    )
    frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 32 * mm - 16 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    doc.build(story)
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
