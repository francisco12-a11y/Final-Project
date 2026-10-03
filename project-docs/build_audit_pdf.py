#!/usr/bin/env python3
"""Build the Founder Delegation Audit lead-magnet PDF (L6).

FP | Francisco Buiras | Founder Delegation Audit
Branding: Pareto Talent — emerald #10B981, dark navy #0B1526, Liberation Sans.
Re-run after editing content: python3 project-docs/build_audit_pdf.py
"""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, KeepTogether,
)

# ---------------------------------------------------------------- constants
OUT = os.path.join(os.path.dirname(__file__), "..", "lead-magnet",
                   "FP_FranciscoBuiras_L06_FounderDelegationAudit.pdf")

BRAND = HexColor("#10B981")
BRAND_DARK = HexColor("#059669")
DEEP = HexColor("#065F46")
INK = HexColor("#0F172A")
BODY = HexColor("#334155")
MUTED = HexColor("#64748B")
LINE = HexColor("#E2E8F0")
SOFT = HexColor("#F5F9F7")
DARK = HexColor("#0B1526")
MINT = HexColor("#6EE7B7")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

LOGO = os.path.join(os.path.dirname(__file__), "..", "public",
                    "logo-pareto-talent.png")
TOTAL_PAGES = 4  # set by build() after the first pass

_FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Lib", f"{_FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lib-B", f"{_FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lib-I", f"{_FDIR}/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Lib-BI", f"{_FDIR}/LiberationSans-BoldItalic.ttf"))

# ---------------------------------------------------------------- styles
def st(name, **kw):
    base = dict(fontName="Lib", fontSize=10.5, leading=15.5, textColor=BODY)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "intro":    st("intro", fontSize=11, leading=17),
    "h2kick":   st("h2kick", fontName="Lib-B", fontSize=9, leading=12,
                   textColor=DEEP, spaceBefore=0, spaceAfter=2),
    "h2":       st("h2", fontName="Lib-B", fontSize=17, leading=21,
                   textColor=INK, spaceAfter=6),
    "h3":       st("h3", fontName="Lib-B", fontSize=12.5, leading=16,
                   textColor=INK, spaceBefore=10, spaceAfter=4),
    "body":     st("body"),
    "muted":    st("muted", fontSize=9.5, leading=13.5, textColor=MUTED),
    "cell":     st("cell", fontSize=9.5, leading=13),
    "cellB":    st("cellB", fontName="Lib-B", fontSize=9.5, leading=13,
                   textColor=INK),
    "cellMuted": st("cellMuted", fontSize=9.5, leading=13, textColor=MUTED),
    "quote":    st("quote", fontName="Lib-I", fontSize=10.5, leading=16.5,
                   textColor=INK),
    "stepT":    st("stepT", fontName="Lib-B", fontSize=11, leading=14,
                   textColor=INK),
    "stepB":    st("stepB", fontSize=9.5, leading=13.5, textColor=BODY),
    "chipTxt":  st("chipTxt", fontSize=9.5, leading=13, textColor=DEEP),
    "darkT":    st("darkT", fontName="Lib-B", fontSize=15, leading=20,
                   textColor=white),
    "darkB":    st("darkB", fontSize=10, leading=15, textColor=MINT),
    "fill":     st("fill", fontName="Lib-B", fontSize=12, leading=16,
                   textColor=DEEP),
}


def sparkle(c, cx, cy, r, color=BRAND):
    """Four-point star (Pareto spark)."""
    k = 0.18 * r
    p = c.beginPath()
    p.moveTo(cx, cy - r)
    p.curveTo(cx + k * .3, cy - k, cx + k, cy - k * .3, cx + r, cy)
    p.curveTo(cx + k, cy + k * .3, cx + k * .3, cy + k, cx, cy + r)
    p.curveTo(cx - k * .3, cy + k, cx - k, cy + k * .3, cx - r, cy)
    p.curveTo(cx - k, cy - k * .3, cx - k * .3, cy - k, cx, cy - r)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, stroke=0, fill=1)


# ---------------------------------------------------------------- decorations
HEADER_H = 88 * mm  # dark band on page 1


def on_first_page(c, doc):
    c.saveState()
    # full-bleed dark band
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, stroke=0, fill=1)
    # soft emerald glow, low-saturation
    c.setFillColor(HexColor("#10B981"))
    c.setFillAlpha(0.08)
    c.circle(PAGE_W - 30 * mm, PAGE_H - 18 * mm, 42 * mm, stroke=0, fill=1)
    c.setFillAlpha(1)

    # real Pareto Talent logo (transparent PNG from paretotalent.com)
    c.drawImage(LOGO, MARGIN, PAGE_H - 20 * mm,
                width=22 * mm, height=9 * mm, mask="auto")
    c.setFillColor(HexColor("#8FA3B8"))
    c.setFont("Lib-B", 9.5)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 18 * mm,
                      "FREE FOUNDER WORKSHEET")

    c.setFillColor(white)
    c.setFont("Lib-B", 30)
    c.drawString(MARGIN, PAGE_H - 38 * mm, "The Founder Delegation Audit")
    c.setFillColor(MINT)
    c.setFont("Lib-B", 14.5)
    c.drawString(MARGIN, PAGE_H - 47 * mm,
                 "Find the 15 hours a week you're doing a $10/hour job")

    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 10.5)
    c.drawString(MARGIN, PAGE_H - 57 * mm,
                 "A 20-minute worksheet that ranks what to hand off first and scripts")
    c.drawString(MARGIN, PAGE_H - 62 * mm,
                 "the handoff conversation you've been avoiding.")

    # meta chips
    chips = ["20 MINUTES", "3 STEPS", "YOUR RECOVERABLE WEEK"]
    x = MARGIN
    c.setFont("Lib-B", 8.5)
    for label in chips:
        w = c.stringWidth(label, "Lib-B", 8.5) + 9 * mm
        c.setStrokeColor(HexColor("#2A3B52"))
        c.setLineWidth(0.8)
        c.roundRect(x, PAGE_H - 73 * mm, w, 7.5 * mm, 3.75 * mm,
                    stroke=1, fill=0)
        c.setFillColor(MINT)
        c.drawCentredString(x + w / 2, PAGE_H - 70.8 * mm, label)
        x += w + 4 * mm
    c.restoreState()
    _footer(c, doc)


def on_later_pages(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, stroke=0, fill=1)
    c.drawImage(LOGO, MARGIN, PAGE_H - 8.4 * mm,
                width=12 * mm, height=4.9 * mm, mask="auto")
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib-B", 8)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 7.8 * mm,
                      "THE FOUNDER DELEGATION AUDIT")
    c.restoreState()
    _footer(c, doc)


def _footer(c, doc):
    c.saveState()
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN, 13 * mm, PAGE_W - MARGIN, 13 * mm)
    c.setFillColor(MUTED)
    c.setFont("Lib", 8)
    c.drawString(MARGIN, 8.5 * mm,
                 "FP | Francisco Buiras | Founder Delegation Audit · "
                 "© 2026 Pareto Talent · paretotalent.com")
    c.drawRightString(PAGE_W - MARGIN, 8.5 * mm,
                      f"Page {c.getPageNumber()} of {TOTAL_PAGES}")
    c.restoreState()


# ---------------------------------------------------------------- helpers
def section_block(kicker, title, intro=None):
    out = [Paragraph(kicker, S["h2kick"]),
           Paragraph(title, S["h2"])]
    if intro:
        out.append(Paragraph(intro, S["body"]))
    return out


def filled_line(label, width_pts):
    t = Table(
        [[Paragraph(label, S["fill"]), ""]],
        colWidths=[width_pts - 90, 90], rowHeights=[9 * mm])
    t.setStyle(TableStyle([
        ("LINEBELOW", (1, 0), (1, 0), 0.9, HexColor("#9FB3C8")),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def boxed(body_flowables, bg=SOFT, border=LINE, pad=12):
    t = Table([[body_flowables]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad - 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 2),
    ]))
    return t


def P(text, style="body"):
    return Paragraph(text, S[style])


# ---------------------------------------------------------------- content
def task_log_table():
    header = [P("<b>#</b>", "cellMuted"), P("<b>TASK</b>", "cellMuted"),
              P("<b>HOURS/WK</b>", "cellMuted"),
              P("<b>TIMES/WK</b>", "cellMuted")]
    rows = [header]
    for i in range(1, 13):
        rows.append([P(str(i), "cellMuted"), "", "", ""])
    t = Table(rows, colWidths=[30, 285, 94, 94],
              rowHeights=[8 * mm] + [9.2 * mm] * 12)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#EAF6F1")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BRAND),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, LINE),
        ("LINEAFTER", (1, 0), (1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def question_table(title, question, options):
    data = [[P(f"<b>{title}</b>", "cellB"), "", P("<b>POINTS</b>", "cellMuted")]]
    data.append([P(question, "cellMuted"), "", ""])
    for letter, desc, pts in options:
        data.append([P(f"<b>{letter}</b>", "cellB"), P(desc, "cell"),
                     P(f"<b>{pts}</b>", "cellB")])
    t = Table(data, colWidths=[34, 369, 100])
    t.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)),
        ("SPAN", (0, 1), (1, 1)),
        ("BACKGROUND", (0, 0), (-1, 1), HexColor("#EAF6F1")),
        ("LINEBELOW", (0, 1), (-1, 1), 0.6, LINE),
        ("LINEBELOW", (0, 2), (-1, -2), 0.4, LINE),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def rank_table():
    header = [P("<b>TASK</b>", "cellMuted"), P("<b>SCORE</b>", "cellMuted"),
              P("<b>HOURS/WEEK</b>", "cellMuted"),
              P("<b>WHO COULD OWN IT</b>", "cellMuted")]
    owners = ["Right Hand", "Right Hand", "Right Hand",
              "Later / systemize", "Keep (founder work)", "", ""]
    rows = [header]
    for owner in owners:
        rows.append(["", "", "", P(owner, "cellMuted") if owner else ""])
    t = Table(rows, colWidths=[219, 70, 94, 120],
              rowHeights=[8 * mm] + [8.6 * mm] * 7)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#EAF6F1")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BRAND),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, LINE),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def steps_row():
    cells = [
        [P("<b>1 · LOG</b>", "stepT"),
         P("List every recurring task you did this week. Recurring only; "
           "one-off fires don't count.", "stepB")],
        [P("<b>2 · SCORE</b>", "stepT"),
         P("Rate each task on two questions: what it costs to hire out, "
           "and whether it truly needs you.", "stepB")],
        [P("<b>3 · RANK &amp; HAND OFF</b>", "stepT"),
         P("Sort by score, total the hours, and run the handoff script "
           "on your top task.", "stepB")],
    ]
    t = Table([cells], colWidths=[CONTENT_W / 3.0] * 3)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEAFTER", (0, 0), (1, 0), 0.6, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("LEFTPADDING", (1, 0), (-1, -1), 10),
    ]))
    return t


def closing_band():
    inner = [
        Spacer(1, 4),
        P("You found the hours. Now put a person on them.", "darkT"),
        Spacer(1, 6),
        P("If your audit found 10+ recoverable hours, the next problem is "
          "finding the person who takes those tasks. Pareto Talent does that "
          "part: hand-picked, AI-trained Right Hand candidates matched to "
          "your audit within 24 hours, backed by the Freedom 40 guarantee "
          "(reclaim 40 hours in your first 30 days or the next month is "
          "free) and lifetime replacement.", "darkB"),
        Spacer(1, 10),
        P("<b>Book your Matching Call at paretotalent.com and bring this "
          "audit. Your shortlist is your first job description.</b>", "darkB"),
    ]
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))
    return t


def make_doc(path):
    doc = BaseDocTemplate(
        os.path.abspath(path), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 4 * mm, bottomMargin=18 * mm,
        title="The Founder Delegation Audit — Pareto Talent",
        author="Francisco Buiras",
        subject="Free founder worksheet: rank what to delegate first and "
                "recover 10-15 hours a week",
        creator="FP | Francisco Buiras | Founder Delegation Audit",
    )
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 22 * mm - 18 * mm,
                  id="main")
    doc.addPageTemplates([
        PageTemplate(id="first", frames=[frame], onPage=on_first_page),
        PageTemplate(id="later", frames=[frame], onPage=on_later_pages),
    ])
    return doc


def make_story():
    story = []
    from reportlab.platypus import NextPageTemplate
    story.append(NextPageTemplate("later"))

    # ---- clear the page-1 dark band, then intro + how it works
    story.append(Spacer(1, HEADER_H - 14 * mm))
    story.append(P(
        "You became a founder to do founder work. Somewhere along the way, "
        "your week filled up with inbox triage, scheduling, CRM updates and "
        "follow-ups — $10/hour work inside a $100/hour brain. This audit "
        "makes the trade visible: what each task costs you and what to hand "
        "off first. Do it honestly. The math is uncomfortable "
        "on purpose."))
    story.append(Spacer(1, 10))
    story.append(steps_row())
    story.append(Spacer(1, 16))

    # ---- STEP 1
    story += section_block("STEP 1", "The Task Log",
                           "List every task you did more than once this week. "
                           "Not sure what counts? The usual suspects: email "
                           "triage · calendar management · CRM updates · "
                           "invoicing · following up with leads or customers · "
                           "social posting · data entry · research · meeting "
                           "notes · order processing · recruiting admin · "
                           "travel booking · report building.")
    story.append(Spacer(1, 8))
    story.append(task_log_table())
    story.append(Spacer(1, 14))

    # ---- STEP 2
    story += section_block(
        "STEP 2", "Score every task (two questions each)")
    story.append(Spacer(1, 6))
    story.append(question_table(
        "Q1 — Hire-out cost", "What would it cost to hire someone to do this?",
        [("A", "Under $15/hour — data entry, scheduling, inbox triage", "3"),
         ("B", "$15–50/hour — follow-ups, CRM updates, reporting", "2"),
         ("C", "$50+/hour — strategy, sales, product", "0")]))
    story.append(Spacer(1, 8))
    story.append(question_table(
        "Q2 — You vs. anyone",
        "Does this task need <i>you</i>, or does it need <i>doing</i>?",
        [("A", "Anyone trained could do it", "3"),
         ("B", "Needs judgment, but not my judgment", "2"),
         ("C", "Genuinely needs me — vision, key relationships", "0")]))
    story.append(Spacer(1, 10))
    story.append(boxed([
        P("<b>Delegation Score = Q1 + Q2.</b> Maximum 6 points per task. "
          "Write each score in the margin next to your task log.", "body"),
        Spacer(1, 4),
        P("If you scored C on Q2 but A on Q1, that's a <b>systemize-first</b> "
          "task — write the process down once, then hand it off.", "muted"),
    ]))
    story.append(Spacer(1, 14))

    # ---- STEP 3
    story += section_block(
        "STEP 3", "Rank and recover",
        "Sort your tasks by Delegation Score, highest first. Everything "
        "scoring <b>4–6</b> goes on your Delegation Shortlist. Add up the "
        "hours; that's your recoverable week.")
    story.append(Spacer(1, 8))
    story.append(rank_table())
    story.append(Spacer(1, 10))
    story.append(filled_line("<b>Your recoverable hours per week:</b>",
                             CONTENT_W))
    story.append(Spacer(1, 12))
    story.append(boxed([
        P("<b>What those hours are worth</b>", "cellB"),
        Spacer(1, 3),
        P("Recoverable hours × 50 weeks × your effective hourly rate "
          "(last year's profit ÷ hours worked). Founders who run this audit "
          "typically find <b>10–15 hours a week</b>, over 600 hours a year "
          "of founder-level work stuck in assistant-level tasks.", "cell"),
    ]))
    story.append(Spacer(1, 14))

    # ---- The handoff script
    script_flow = [
        P("<b>YOUR FIRST HANDOFF CONVERSATION</b>", "h2kick"),
        Spacer(1, 2),
        P("The script nobody gives you", "h2"),
        P("Most delegation fails at the handoff. Use this when you're "
          "ready, with a Right Hand or with your current team:",
          "body"),
        Spacer(1, 6),
        boxed([
            P("\u201CI've audited my week and this task — <b>[TASK]</b> — is "
              "now yours. Here's what 'done' looks like: <b>[OUTCOME, NOT "
              "METHOD]</b>. You own it end to end. The decision I'm "
              "delegating to you: <b>[E.G. REFUNDS UNDER $100]</b>. Check in "
              "with me Friday with one question: what did you decide?\u201D",
              "quote"),
        ], bg=HexColor("#EAF6F1"), border=HexColor("#BFE8D9")),
        Spacer(1, 8),
        P("<b>The three rules that make it stick</b>", "h3"),
        P("• Hand off the <b>outcome</b>, not the method. If you script "
          "their steps, you've built a $10/hour puppet, and you're still "
          "the operator.", "body"),
        P("• Delegate one <b>decision authority</b> with every task. That's "
          "what makes it permanent.", "body"),
        P("• Check in weekly on <b>decisions made</b>, never on tasks done.",
          "body"),
    ]
    story.append(KeepTogether(script_flow))
    story.append(Spacer(1, 14))
    story.append(closing_band())
    return story


def build():
    global TOTAL_PAGES
    # pass 1: build to a temp file to count pages
    tmp = os.path.abspath(OUT) + ".tmp.pdf"
    make_doc(tmp).build(make_story())
    import pymupdf
    TOTAL_PAGES = len(pymupdf.open(tmp))
    os.remove(tmp)
    # pass 2: final build with the correct "Page X of N"
    make_doc(OUT).build(make_story())
    print(f"OK -> {os.path.abspath(OUT)} ({TOTAL_PAGES} pages)")


if __name__ == "__main__":
    build()
