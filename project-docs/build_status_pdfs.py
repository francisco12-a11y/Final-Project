#!/usr/bin/env python3
"""Builds two status PDFs:
1. Pareto_FinalProject_Whats_Done.pdf
2. Pareto_FinalProject_Whats_Missing.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Table, TableStyle)

BRAND = HexColor("#10B981"); DEEP = HexColor("#065F46"); INK = HexColor("#0F172A")
BODY = HexColor("#334155"); MUTED = HexColor("#64748B"); LINE = HexColor("#E2E8F0")
SOFT = HexColor("#F5F9F7"); TINT = HexColor("#EAF6F1"); DARK = HexColor("#0B1526")
MINT = HexColor("#6EE7B7"); AMBER = HexColor("#D97706")

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
    "h2": st("h2", fontName="Lib-B", fontSize=13, leading=17, textColor=INK,
             spaceAfter=5),
    "body": st("body"),
    "muted": st("muted", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": st("cell", fontSize=9.5, leading=13.5, textColor=BODY),
    "cellB": st("cellB", fontName="Lib-B", fontSize=9.5, leading=13.5,
                textColor=INK),
    "check": st("check", fontName="Lib-B", fontSize=11, leading=15,
                textColor=INK),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def header(c, doc_title, subtitle, accent):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 26 * mm, PAGE_W, 26 * mm, stroke=0, fill=1)
    c.setFillColor(accent)
    c.setFont("Lib-B", 8)
    c.drawString(MARGIN, PAGE_H - 10 * mm,
                 "P A R E T O   T A L E N T   ·   F I N A L   P R O J E C T")
    c.setFillColor(white)
    c.setFont("Lib-B", 16)
    c.drawString(MARGIN, PAGE_H - 17 * mm, doc_title)
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 9)
    c.drawString(MARGIN, PAGE_H - 22.5 * mm, subtitle)
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    c.setFillColor(MUTED); c.setFont("Lib", 7.5)
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


def checklist(items, color, checked=True, with_owner=False):
    rows = []
    for item in items:
        if with_owner:
            owner, title, detail = item
            title = f"{title} &nbsp;<font size=7.5 color={AMBER.hexval().replace('0x','#')}>[{owner}]</font>"
        else:
            title, detail = item
        mark = "\u2713" if checked else "\u25A1"
        rows.append([Paragraph(mark, st("m", fontName="Lib-B", fontSize=10,
                                        textColor=color)),
                     Paragraph(f"<b>{title}</b>", st("t", fontName="Lib-B",
                                                     fontSize=9.5,
                                                     textColor=INK)),
                     Paragraph(detail, st("d", fontSize=8.5, leading=12,
                                          textColor=MUTED))])
    t = Table(rows, colWidths=[16, 175, CONTENT_W - 16 - 175 - 10])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
    ]))
    return t


DONE_ITEMS = [
    ("Strategy + offer locked",
     "ICP, four personas, qualification rules, MAGIC title (Oct 3)"),
    ("Funnel pages live",
     "Landing with persona heroes + 2-minute test (L7) · booking page with live GHL calendar (L9) · thank-you page (L10)"),
    ("Real Pareto branding",
     "Their logo, exact design tokens, Plus Jakarta Sans + DM Sans — scraped from paretotalent.com"),
    ("Lead magnet live",
     "The Right Hand Starter Kit PDF hosted on the site (L6); the test personalizes your Week 1"),
    ("Qualifying form embedded + styled + smart",
     "FB-Qualifying form, dark themed, on the landing (L8) — conditional logic inside the form routes by revenue"),
    ("Routing verified",
     "Pre-revenue / Under $10K → thank-you page · everything else → booking page with the calendar — tested through the landing"),
    ("GHL pipeline + 6 workflows + 9 emails",
     "Opt-in, qualified follow-up, nurture, booking reminders, post-call thank-you, no-show handler — confirmed working (L11/L12 source)"),
    ("No-show automation",
     "No-show Handler tags the contact; the post-call workflow re-queues them into the booking chase instead of a wrong thank-you email"),
    ("Business Map live",
     "Notion page public with the Mermaid journey map (L3)"),
    ("Second Brain complete",
     "Hire book, BC7 days 1–9, competitor teardowns, ICP + personas in Obsidian (L1)"),
    ("Research doc",
     "FP_FranciscoBuiras_L02_Research.pdf — competitor teardowns, ICP, personas, decision record (L2)"),
    ("SOP written",
     "FP_FranciscoBuiras_L05_SOP.pdf — the repeatable launch process (L5)"),
    ("Ads copy ×5",
     "Five different arguments, one per persona + the destination angle, each with its landing hero (L13 copy)"),
    ("Imagery done and wired",
     "All six photos generated, optimized and live on the landing: 4 founder personas, the operator shot and the VA bench (L14)"),
    ("Loom script",
     "FP_FranciscoBuiras_L15_LoomScript.pdf — six timed beats, ~300 words (L15 prep)"),
    ("ClickUp structure + CSV",
     "7 milestones, 24 tasks ready to import (L4 prep)"),
    ("Walkthrough draft",
     "FP_FranciscoBuiras_Walkthrough_Draft.md — all 9 Parts written, ready to paste into Google Docs"),
]

MISSING_ITEMS = [
    ("Fran", "Final test pass + screenshots → L11/L12",
     "Incognito: qualified answers → booking page, Pre-revenue/Under $10K → thank-you; book a test call, mark it No Show, screenshot the no-show chain; export every workflow's execution log. Upload to the L11/L12 Drive folders"),
    ("Fran", "Delete the test contacts",
     "All the Router Test entries + your +1 480 555 7878 tests — the pipeline screenshots must be clean"),
    ("Fran", "Renumber the duplicate E9",
     "Two emails carry E9 (post-call thank-you and the no-show reschedule). Rename one to E10 in GHL so the index matches"),
    ("Fran", "Kit PDF → Drive (L6)",
     "Upload FP_FranciscoBuiras_L06_RightHandStarterKit.pdf to the L6 folder, share as Anyone with the link"),
    ("Fran", "Ad creatives export → L13",
     "Portraits + overlays per the imagery pack → FP_FranciscoBuiras_Ad1–Ad5 → L13 Drive folder"),
    ("Fran", "Imagery folder → L14",
     "The six finals already on the site — export the originals to the L14 Drive folder"),
    ("Fran", "ClickUp import (L4)",
     "Create the list, Import → CSV (lead-magnet-launch.csv), share publicly"),
    ("Fran", "Second Brain link (L1) + H1–H9 links",
     "Collect the public links for the index"),
    ("Fran", "Record the Loom (2 min)",
     "Script ready — rehearse the two page-jumps in beat 3"),
    ("Fran", "EXTRA: build the GHL funnel",
     "2-step qualified-path funnel (steps in the Extra Mile section) — screenshot it for the walkthrough's extra-mile answer"),
    ("Fran", "Assemble + submit",
     "Paste the walkthrough draft into Google Docs, add links + screenshots, export FP_FranciscoBuiras_ParetoBootcamp.pdf, submit at bootcamp.paretotalent.com/finalproject. Aim Oct 7, 6:00 pm"),
]


def build_done():
    OUT = "/home/fran/Descargas/Pareto_FinalProject_Whats_Done.pdf"
    story = [
        P("Everything already built and live — Oct 6", "h2"),
        Spacer(1, 4),
        checklist(DONE_ITEMS, BRAND, checked=True),
        Spacer(1, 10),
        boxed([P("<b>The funnel's main line is operational end to end:</b> ad → landing → "
                 "8-question test → styled GHL form → automatic qualified/unqualified routing → "
                 "calendar or nurture → pipeline → 5 workflows → 9 emails.", "cell")],
              bg=TINT, border=HexColor("#BFE8D9")),
    ]

    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=32 * mm, bottomMargin=16 * mm,
        title="What We Have Done — Pareto Final Project",
        author="Francisco Buiras",
        subject="Completed work inventory for the Pareto final project",
        creator="FP | Francisco Buiras | Status",
    )
    frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 32 * mm - 16 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                          onPage=lambda c, d: (header(c, "What We Have Done",
                          "FP | Francisco Buiras | 17 deliverables done · photography wired · as of October 6", BRAND), None))])
    doc.build(story)
    print("OK ->", OUT)


def build_missing():
    OUT = "/home/fran/Descargas/Pareto_FinalProject_Whats_Missing.pdf"
    story = [
        P("What's left before submission — Oct 7, end of day", "h2"),
        Spacer(1, 4),
        checklist(MISSING_ITEMS, AMBER, checked=False, with_owner=True),
        Spacer(1, 10),
        boxed([
            P("<b>The critical path:</b> two-path test → screenshots → walkthrough assembly → submit. "
              "Everything else flexes; that chain doesn't.", "cell"),
        ], bg=SOFT),
        Spacer(1, 10),
        P("THE EXTRA MILE — what this project adds that was never asked for", "h2"),
        Spacer(1, 4),
        P("<b>1 · A second GHL funnel for the qualified path (the build-in-progress extra).</b> "
          "Sites → Funnels → New Funnel, name it FP | Francisco Buiras | Qualified Path Funnel. "
          "Step 1 (Opt-in): drag in the FB-Qualifying form element plus the kit hook copy. "
          "Step 2 (Booking): blank page with the calendar element and the three guarantees. "
          "In the form's conditional logic, point the qualified outcome at Step 2's URL; everything "
          "else keeps going to the thank-you page. One hour of work, and it proves native GHL "
          "funnel skills on top of the custom site.", "cell"),
        Spacer(1, 4),
        P("<b>2 · No-show re-engagement, automated.</b> A No-show Handler workflow tags missed "
          "calls, and the post-call workflow re-queues them into the booking chase instead of "
          "sending a thank-you to an empty chair.", "cell"),
        Spacer(1, 4),
        P("<b>3 · The post-call sequence.</b> The pipeline moves to Call Done by itself one day "
          "after the appointment, and the founder gets the next-steps email while the matching "
          "team starts.", "cell"),
        Spacer(1, 4),
        P("<b>4 · The kit travels to the call.</b> Qualified founders bring the completed Starter "
          "Kit to the Matching Call — the lead magnet becomes Pareto's own sales tool.", "cell"),
        Spacer(1, 4),
        P("<b>5 · Persona-matched ad destinations.</b> Each of the five ads lands on a hero that "
          "echoes its exact angle, not one generic homepage.", "cell"),
        Spacer(1, 4),
        P("<b>6 · An interactive test as the front door.</b> Instead of a static PDF gate, the "
          "2-minute test computes the founder's own recoverable hours and personalizes the kit's "
          "Week 1 before anyone gives an email.", "cell"),
        Spacer(1, 10),
        boxed([
            P("<b>Index link map (paste into the submission PDF):</b>", "cellB"),
            Spacer(1, 3),
            P("L1 Second Brain · L2 Research PDF · L3 Notion map · L4 ClickUp board · L5 SOP PDF · "
              "L6 Kit PDF · L7–L10 site pages · L11/L12 screenshot folders · L13 ads folder · "
              "L14 imagery folder · L15 Loom · H1–H9 homework", "cell"),
        ]),
    ]

    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=32 * mm, bottomMargin=16 * mm,
        title="What's Missing — Pareto Final Project",
        author="Francisco Buiras",
        subject="Remaining work before submission, by owner, with the critical path",
        creator="FP | Francisco Buiras | Status",
    )
    frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 32 * mm - 16 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                          onPage=lambda c, d: (header(c, "What's Missing",
                          "FP | Francisco Buiras | 11 items left + the extra-mile funnel · deadline October 7, end of day", AMBER), None))])
    doc.build(story)
    print("OK ->", OUT)


if __name__ == "__main__":
    build_done()
    build_missing()
