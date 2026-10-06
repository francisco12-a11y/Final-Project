#!/usr/bin/env python3
"""GHL Funnel (Extra Mile) PDF — Part 6 structure + click-by-click build guide.
Output: /home/fran/Descargas/FP_FranciscoBuiras_GHL_Funnel_ExtraMile.pdf
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

OUT = "/home/fran/Descargas/FP_FranciscoBuiras_GHL_Funnel_ExtraMile.pdf"

BRAND = HexColor("#10B981"); DEEP = HexColor("#065F46"); INK = HexColor("#0F172A")
BODY = HexColor("#334155"); MUTED = HexColor("#64748B"); LINE = HexColor("#E2E8F0")
SOFT = HexColor("#F5F9F7"); TINT = HexColor("#EAF6F1"); TINT_LINE = HexColor("#BFE8D9")
DARK = HexColor("#0B1526"); MINT = HexColor("#6EE7B7")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

_FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Lib", f"{_FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lib-B", f"{_FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lib-I", f"{_FDIR}/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DVS", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))


def st(name, **kw):
    base = dict(fontName="Lib", fontSize=9.5, leading=13.5, textColor=BODY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "h2kick": st("h2kick", fontName="Lib-B", fontSize=8, leading=11, textColor=DEEP, spaceAfter=2),
    "h2": st("h2", fontName="Lib-B", fontSize=13.5, leading=17, textColor=INK, spaceAfter=5),
    "h3": st("h3", fontName="Lib-B", fontSize=10.5, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3),
    "body": st("body"),
    "muted": st("muted", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": st("cell", fontSize=8.5, leading=11.5, textColor=BODY),
    "cellB": st("cellB", fontName="Lib-B", fontSize=8.5, leading=11.5, textColor=INK),
    "copy": st("copy", fontName="Lib-I", fontSize=9, leading=13, textColor=INK),
    "copyStars": st("copyStars", fontName="DVS", fontSize=9, leading=13, textColor=INK),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def boxed(rows, fill=SOFT, line=LINE, width="full"):
    t = Table([[r] for r in rows], colWidths=[CONTENT_W] if width == "full" else None)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.8, line),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def on_page(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 26 * mm, PAGE_W, 26 * mm, stroke=0, fill=1)
    c.setFillColor(MINT)
    c.setFont("Lib-B", 8)
    c.drawString(MARGIN, PAGE_H - 10 * mm, "P A R E T O   T A L E N T   ·   F I N A L   P R O J E C T")
    c.setFillColor(white)
    c.setFont("Lib-B", 16)
    c.drawString(MARGIN, PAGE_H - 17 * mm, "GHL Funnel · Extra Mile")
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 9)
    c.drawString(MARGIN, PAGE_H - 22.5 * mm,
                 "FP | Francisco Buiras | Part 6 · funnel structure + the GHL-native rebuild, click by click")
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    c.setFillColor(MUTED); c.setFont("Lib", 7.5)
    c.drawString(MARGIN, 8 * mm,
                 "Build in GHL, then screenshot: funnel step list, step editors, form conditional logic, WF1 filter, one submission per path.")
    c.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=32 * mm, bottomMargin=16 * mm,
                      title="FP | Francisco Buiras | GHL Funnel Extra Mile",
                      author="Francisco Buiras")
frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 48 * mm, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])

story = []

# ---------- 1. structure ----------
story.append(P("PART 6 · WHAT THE RUBRIC ASKS AND WHERE EACH PIECE LIVES", "h2kick"))
story.append(P("The funnel structure", "h2"))
story.append(P(
    "Part 6 allows any tool. The lead-magnet funnel already exists and runs end to end: the landing page "
    "(built with Claude Code, hosted on GitHub Pages) sells the magnet, FB-Qualifying qualifies, and the "
    "form's conditional logic routes qualified founders to the booking page and everyone else to the "
    "thank-you page. The extra mile is rebuilding that same funnel natively in GoHighLevel, so the whole "
    "flow also runs inside GHL with no external pages."))
story.append(Spacer(1, 4))
rows = [
    [P("<b>Part 6 requirement</b>", "cellB"), P("<b>Where it lives</b>", "cellB"), P("<b>Screenshot for the doc</b>", "cellB")],
    [P("Hero · What's inside · Who it's for · Proof with real Pareto numbers · CTA with the form", "cell"),
     P("Landing page (Claude Code): francisco12-a11y.github.io/Final-Project", "cell"),
     P("Full-page screenshot of the landing", "cell")],
    [P("Proof with real Pareto numbers", "cell"),
     P("Same page: 4.9 · 100+ founders, 10–15 hrs/week, 4.3x ROI, 3 matches in 24h, Freedom 40, $200/hr math", "cell"),
     P("Proof strip + guarantee cards", "cell")],
    [P("Qualifying form: contact details + Part 4 questions", "cell"),
     P("FB-Qualifying form embedded on the landing (name, email, phone, revenue, hours, founder)", "cell"),
     P("Form builder + conditional logic screen", "cell")],
    [P("Qualified → booking page with your calendar embedded", "cell"),
     P("qualified.html with the Matching Call calendar (Nl5jVEH9F0pMSkjCDTas)", "cell"),
     P("Booking page with calendar visible", "cell")],
    [P("Not qualified → thank-you page that confirms and delivers", "cell"),
     P("thank-you.html; the kit lands by email (E1, PDF attached)", "cell"),
     P("Thank-you page + kit email", "cell")],
    [P("EXTRA MILE: the same funnel, 100% inside GHL", "cell"),
     P("Funnel `FP | Francisco Buiras | Qualified Path Funnel`: Opt-in → Booking → Thank You (this guide)", "cell"),
     P("Funnel step list + each step editor", "cell")],
]
t = Table(rows, colWidths=[CONTENT_W * 0.38, CONTENT_W * 0.40, CONTENT_W * 0.22])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), TINT),
    ("BOX", (0, 0), (-1, -1), 0.8, TINT_LINE),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, TINT_LINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 10))

# ---------- 2. the one rule ----------
story.append(boxed([
    P("<b>The one rule before you start</b>", "cellB"),
    Spacer(1, 2),
    P("Do not touch FB-Qualifying's conditional logic. Its targets (qualified.html / thank-you.html) are "
      "what the live landing uses right now. A form has one set of redirect rules, so the funnel gets a "
      "<b>copy</b> of the form with its own targets. Workflow 1 then listens to both forms, and no "
      "submission source is ever missed.", "cell"),
]))
story.append(Spacer(1, 10))

# ---------- 3. click-by-click ----------
story.append(P("BUILD, IN THIS ORDER", "h2kick"))
story.append(P("Click-by-click", "h2"))

steps = [
    ("1", "Duplicate the form.",
     "Sites → Forms → FB-Qualifying → ⋮ menu → <b>Duplicate</b>. Rename the copy "
     "<b>FP | Francisco Buiras | Qualifying Form – Funnel</b>. Open it and verify every question still "
     "binds the SAME custom fields (duplication can loosen them into standalone questions). Revenue: "
     "Required ON. Leave its conditional logic as-is for now; you point it at the funnel steps in step 6."),
    ("2", "Create the funnel.",
     "Sites → Funnels → + New Funnel → start from blank. Name it "
     "<b>FP | Francisco Buiras | Qualified Path Funnel</b>. If you already created it earlier, use that one."),
    ("3", "Build the Booking step (Step 2) first.",
     "In the step list, rename/add a step of type Website called <b>Booking</b>. Open the editor: dark "
     "background, the headline and sub from the copy blocks below, then add the <b>Calendar</b> element "
     "and select your Matching Call calendar. Add the three guarantees as a row of cards or short text "
     "blocks. This step is your qualified destination inside GHL."),
    ("4", "Build the Thank You step (Step 3).",
     "+ Add Step → type Website, name <b>Thank You</b>. Dark background, headline and body from the copy "
     "blocks. It confirms the opt-in and promises the kit by email."),
    ("5", "Build the Opt-in step (Step 1).",
     "Back to Step 1, name <b>Opt-in</b>. Dark background. Hero headline + sub + proof strip from the copy "
     "blocks, then drag in the <b>Form</b> element and select <b>FP | Francisco Buiras | Qualifying Form – Funnel</b> "
     "(the copy — never the original). Add the form headline above it."),
    ("6", "Point the funnel form's conditional logic at the funnel steps.",
     "Copy each step's URL from the funnel builder (step settings → preview/share URL). In the funnel form "
     "copy's conditional logic: the qualified rule (Revenue is not Pre-revenue AND is not Under $10K, or "
     "your existing two-rule layout inverted) → the <b>Booking</b> step URL. Pre-revenue and Under $10K "
     "rules + the default/no-match destination → the <b>Thank You</b> step URL. Save."),
    ("7", "Add the funnel form to Workflow 1's trigger.",
     "Automation → Workflows → FP | Francisco Buiras | Opt-in Workflow → click the Form Submitted trigger "
     "→ Filters → Form <b>is any of</b> → add the funnel form next to FB-Qualifying. Publish."),
    ("8", "Test both paths, then test the original landing.",
     "Open the funnel's Opt-in preview URL incognito and submit the matrix below. Then submit once through "
     "the real landing and confirm it still lands on qualified.html / thank-you.html. Nothing in the "
     "original flow should have moved."),
]
for n, title, body in steps:
    story.append(KeepTogether([
        P(f"<b>{n}. {title}</b>", "h3"),
        P(body, "cell"),
    ]))
story.append(Spacer(1, 10))

# ---------- 4. copy blocks ----------
story.append(P("COPY BLOCKS — PASTE THESE EXACT LINES", "h2kick"))
story.append(P("Copy for each step", "h2"))
story.append(boxed([
    P("<b>Opt-in · hero</b>", "cellB"), Spacer(1, 2),
    P('H1: "You\'re the CEO and your own assistant. Hand off the second job."', "copy"),
    P('Sub: "Take the 2-minute test. See how many hours a week you could get back from the assistant '
      'job, then get the Right Hand Starter Kit by email."', "copy"),
    P('Proof line: "★★★★★ 4.9 · Trusted by 100+ founders"', "copyStars"),
    P('Chips: "10–15 hrs/week recoverable" · "4.3x ROI on a Right Hand" · "3 matches within 24 hours"', "copy"),
    P('Form headline: "First, a quick check so the call is worth your time"', "copy"),
]))
story.append(Spacer(1, 6))
story.append(boxed([
    P("<b>Booking · qualified destination</b>", "cellB"), Spacer(1, 2),
    P('H1: "The assistant job ends here."', "copy"),
    P('Sub: "Book your Matching Call. Bring the kit; your Week 1 list is your first job description."', "copy"),
    P("Guarantees: <b>Freedom 40</b> — follow the onboarding plan and if you don't reclaim 40 hours in "
      "your first 30 days, the next month is on us. <b>Matching Guarantee</b> — 3+ hand-picked candidates "
      "within 24 hours; no contracts, no payment unless you pick someone. <b>Lifetime Replacement</b> — a "
      "free replacement with no waiting period, for as long as you work together.", "copy"),
]))
story.append(Spacer(1, 6))
story.append(boxed([
    P("<b>Thank You · not-qualified destination</b>", "cellB"), Spacer(1, 2),
    P('H1: "The kit is yours."', "copy"),
    P('Body: "Your answers tell us a Matching Call can wait. The Right Hand Starter Kit is in your inbox '
      'right now, and the delegation email series starts tomorrow. Retake the test each quarter — when the '
      'numbers change, the calendar will be here."', "copy"),
]))
story.append(Spacer(1, 10))

# ---------- 5. style ----------
story.append(KeepTogether([
    P("STYLE VALUES — MATCH THE LANDING", "h2kick"),
    P("Colors and type", "h2"),
    boxed([
        P("Background <b>#050A0E</b> (cards #0B1119 / #0F1923) · Headings <b>#F0F4F8</b> · Body text "
          "<b>#94A3B8</b> · Accent <b>#10B981</b> · Button background #10B981 with text <b>#050A0E</b> · "
          "Radius 12–16 · Headings Plus Jakarta Sans · Body DM Sans. The calendar keeps its own green button "
          "with white text (the site's convention).", "cell"),
    ]),
]))
story.append(Spacer(1, 10))

# ---------- 6. test matrix ----------
story.append(P("TEST MATRIX + SCREENSHOT CHECKLIST", "h2kick"))
story.append(P("Prove it works", "h2"))
tests = [
    "Funnel Opt-in preview URL, incognito, Revenue $10K-$50K → Booking step with the calendar visible. Screenshot.",
    "Same, Revenue $50K+ → Booking step. Screenshot.",
    "Same, Revenue Pre-revenue → Thank You step. Screenshot.",
    "Same, Revenue Under $10K → Thank You step. Screenshot.",
    "WF1 execution log shows BOTH form sources firing (one entry per form). Screenshot.",
    "Original landing (github.io) one submission: $10K-$50K still → qualified.html. Screenshot.",
    "Contact record from a funnel submission shows revenue/hours/owner saved. Screenshot.",
]
for i, tline in enumerate(tests, 1):
    story.append(P(f"<b>{i}.</b> {tline}", "cell"))
story.append(Spacer(1, 8))
story.append(boxed([
    P("<b>Rule of thumb:</b> a different email per test run (GHL updates the same contact otherwise), and "
      "always test redirects through the page where the form is embedded, never the standalone form URL.", "cell"),
]))

doc.build(story)
print("OK", OUT, os.path.getsize(OUT), "bytes")
