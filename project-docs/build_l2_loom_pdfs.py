#!/usr/bin/env python3
"""Builds two deliverables:
1. FP_FranciscoBuiras_L02_Research.pdf   (L2 - research doc)
2. FP_FranciscoBuiras_L15_LoomScript.pdf (L15 - 2-minute Loom script)
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
             spaceBefore=8, spaceAfter=3),
    "body": st("body"),
    "muted": st("muted", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": st("cell", fontSize=8.5, leading=11.5, textColor=BODY),
    "cellB": st("cellB", fontName="Lib-B", fontSize=8.5, leading=11.5,
                textColor=INK),
    "quote": st("quote", fontName="Lib-I", fontSize=9.5, leading=13.5,
                textColor=DEEP),
    "line": st("line", fontSize=10, leading=15, textColor=INK),
    "cue": st("cue", fontName="Lib-B", fontSize=8, leading=11, textColor=BRAND),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def header(c, doc_title, subtitle):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 26 * mm, PAGE_W, 26 * mm, stroke=0, fill=1)
    c.setFillColor(MINT)
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


def table(rows, widths):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TINT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BRAND),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


# ================================================================ L2 RESEARCH
def build_research():
    OUT = "/home/fran/Descargas/FP_FranciscoBuiras_L02_Research.pdf"
    story = []

    story.append(P("What the Second Brain holds (sources)", "h2"))
    story.append(P(
        "Every claim in this funnel traces to a note in the Second Brain "
        "(Obsidian vault, FP | Francisco Buiras | Second Brain). Sources ingested:", "body"))
    story.append(Spacer(1, 4))
    story.append(table([
        [P("<b>Source</b>", "cellB"), P("<b>What it contributed</b>", "cellB")],
        [P("The Hire book (7 steps + 7 principles)", "cell"),
         P("Hiring philosophy, filter-before-interview, the delegation ladder", "cell")],
        [P("Bootcamp BC7, days 1–9 (transcripts + notes)", "cell"),
         P("GHL mechanics, core skills, the delegation mastermind content", "cell")],
        [P("paretotalent.com + bootcamp site + wall of love", "cell"),
         P("Public stats (10–15 hrs/wk, 4.3x ROI, Freedom 40, 1-in-1,000, 93% at 12 months), client quotes, pricing", "cell")],
        [P("Hiring regions data", "cell"),
         P("Salary benchmarks across 6 regions", "cell")],
        [P("Competitor sites (Athena, Belay, Virtual Latinos, Wing)", "cell"),
         P("Live teardown of their lead magnets, Oct 2026", "cell")],
    ], [190, CONTENT_W - 190]))
    story.append(Spacer(1, 8))

    story.append(P("Competitor lead-magnet teardowns (verified live)", "h2"))
    story.append(Spacer(1, 2))
    story.append(P("1 · Athena — \u201CDelegation Assessment\u201D quiz", "h3"))
    story.append(P(
        "<b>Format:</b> 10-question quiz, gated at the end (email only). "
        "<b>Promise:</b> your named delegation level, your specific barrier, the next level. "
        "<b>For:</b> overwhelmed founders, including EA skeptics. "
        "<b>Qualify:</b> answers score into six levels (Beginner to Mastery); email requested last, so completion stays high. "
        "<b>After opt-in:</b> instant personalized diagnosis; the top three results all conclude \u201Cthe ceiling here is not your mindset, it is the match\u201D "
        "and bridge into their match signup. <b>Steal:</b> the diagnosis-to-match bridge — the quiz flatters you AND sells the hire.", "cell"))
    story.append(Spacer(1, 5))
    story.append(P("2 · Belay — \u201CFind your MVP\u201D guide", "h3"))
    story.append(P(
        "<b>Format:</b> gated PDF plus a large ungated resource library. "
        "<b>Promise:</b> proof of talent quality — \u201Conly 3% of applicants ever become BELAY contractors.\u201D "
        "<b>For:</b> leaders comparing providers. "
        "<b>Qualify:</b> highest-friction capture of the three — phone number with SMS consent; anyone surrendering a phone is far down the buying path. "
        "<b>After opt-in:</b> download plus SMS/email nurture. <b>Steal:</b> exclusivity stats as belief-building — Pareto's \u201C1 in 1,000\u201D beats their 3%.", "cell"))
    story.append(Spacer(1, 5))
    story.append(P("3 · Virtual Latinos — \u201CAre you doing too much?\u201D quiz + recruiter call", "h3"))
    story.append(P(
        "<b>Format:</b> site-wide quiz feeding a business survey, then a recruiter call; pricing public ($1.6–4.4k/mo). "
        "<b>For:</b> US businesses hiring LatAm talent, organized by vertical (Admin, Sales, Finance & HR, Legal...). "
        "<b>Qualify:</b> the verticals self-sort leads — a lawyer lands on the Legal Assistant page before any form. "
        "<b>After opt-in:</b> 3–4 candidates to interview, with vertical-matched testimonials (law firms quoting law firms). "
        "<b>Steal:</b> vertical proof converts — Pareto's wall is horizontal; vertical pages are the expansion move.", "cell"))
    story.append(Spacer(1, 5))
    story.append(P("Honorable mention · Wing — the demo as magnet", "h3"))
    story.append(P(
        "\u201CFree trial, no credit card\u201D for a managed service is a demo call in disguise. When the product is a matched human, "
        "the call IS the trial — Pareto's Matching Guarantee is the same move, better named.", "cell"))
    story.append(Spacer(1, 8))

    story.append(P("Synthesis — four patterns, and what they decided", "h2"))
    story.append(table([
        [P("<b>Pattern in the space</b>", "cellB"), P("<b>What it decided in our funnel</b>", "cellB")],
        [P("The quiz is the category's default magnet (Athena, VL)", "cell"),
         P("Our lead magnet is a scored test — but personalized (your hours, your money) instead of a generic level", "cell")],
        [P("Gate at the end, email only (Athena) beats form-first", "cell"),
         P("Result first, no email needed; the form comes after the visitor is invested", "cell")],
        [P("Every magnet doubles as a qualifier", "cell"),
         P("The test's answers ARE the qualification data — routing runs on them", "cell")],
        [P("Vertical proof converts (VL's legal vertical)", "cell"),
         P("Five ads, five causes of pain, each landing on its own hero — and the legal vertical flagged as the expansion move", "cell")],
    ], [235, CONTENT_W - 235]))
    story.append(Spacer(1, 8))

    story.append(P("The ICP (company-level filter)", "h2"))
    story.append(boxed([
        P("<b>US-based founder of a growing service business who is personally the operational bottleneck</b> "
          "— real revenue (this launch routes at $10k+/mo), 15+ hours a week of admin and ops on their own plate, "
          "and the hiring decision on their desk. They want a strategic full-time partner, not a task-list VA; they're "
          "open to AI; they value a long-term placement over cheap churn. <b>Disqualified honestly:</b> pre-revenue ideas, "
          "\u201C5 hours of data entry,\u201D offshore-bargain hunters.", "cell"),
    ]))
    story.append(Spacer(1, 8))

    story.append(P("Founder personas (by cause, in client words)", "h2"))
    personas = [
        ("Persona 1 · \u201CEveryone bills time except me\u201D — Agency Owner at Capacity",
         "Cause: client comms, account management and scheduling eat the calendar; the agency can't take client #12.",
         "\u201CI just can't even imagine not having my EA right now.\u201D (Joe Polish, Genius Network)",
         "Tried: another PM tool, a part-time freelancer, a junior AM in burnout. Trigger: dropped balls on a big account."),
        ("Persona 2 · \u201CThe deal dies in my inbox\u201D — Real Estate Operator",
         "Cause: transaction coordination and follow-up are time-critical; slow replies cost deals.",
         "\u201CMy executive assistant runs point on critical projects and keeps track of so many endless opportunities.\u201D (Andrew Myers)",
         "Tried: per-deal coordinators, ISA cold callers — task-shaped, none strategic. Trigger: a deal lost to slow follow-up."),
        ("Persona 3 · \u201CIf I don't post it, it doesn't exist\u201D — Creator with a Content Bottleneck",
         "Cause: publishing, DMs and launch ops pile on top of making content; the channel goes quiet every launch.",
         "\u201CI won't even tell her to do it, and she'll just go and figure out how to do it.\u201D (Elina Panteleyeva)",
         "Tried: editors and VAs needing frame-by-frame instructions. Trigger: a two-week silence on the channel."),
        ("Persona 4 · \u201CI bill $400 an hour and I'm chasing file names\u201D — Law Firm Owner ★ strongest math",
         "Cause: intake, case-status updates, filings — $300–500/hr time burned on $20/hr work.",
         "Hypothesis persona (flagged as such): \u201CEvery missed call is a case walking to another firm.\u201D "
         "Competitor proof: Virtual Latinos runs a whole Legal Assistant vertical with law-firm testimonials (Shankar & Associates PC, Planzer Law LLC).",
         "10 hrs/week back at a billed rate is $150–250k/yr against the program cost — no other persona's math comes close."),
    ]
    for title, cause, words, extra in personas:
        story.append(KeepTogether([
            P(f"<b>{title}</b>", "cellB"),
            P(cause, "cell"),
            P(words, "quote"),
            P(extra, "cell"),
            Spacer(1, 6),
        ]))
    story.append(boxed([
        P("<b>Overlay — \u201Cburned before\u201D (the cross-persona state):</b> \u201CI've had three different executive assistants before, "
          "and I thought it was me… I was burning through them.\u201D (Eric Ritter). The site says 60%+ of founders arrive here. "
          "Every asset speaks to it: the test names the failure, Freedom 40 is the antidote, 93% at 12 months is the proof.", "cell"),
    ], bg=TINT, border=HexColor("#BFE8D9")))
    story.append(Spacer(1, 8))

    story.append(P("Decision record — why this funnel looks like it does", "h2"))
    story.append(P(
        "Magnet: a scored test (pattern 1) that answers first and gates later (pattern 2), whose output — "
        "the recoverable-hours number and the Week 1 handoffs — is both the qualification data and the sales pitch "
        "(pattern 3). Delivery artifact: the Right Hand Starter Kit, the systems the competition never gives away. "
        "Ads: five causes of pain, each with a matching hero. Routing: revenue $10k+ AND 15+ hours AND founder, "
        "computed from the visitor's own answers — a magnet that disqualifies is on-brand.", "body"))

    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=32 * mm, bottomMargin=16 * mm,
        title="Research Doc — Pareto Final Project",
        author="Francisco Buiras",
        subject="Competitor teardowns, ICP, personas, and the research behind the lead magnet funnel",
        creator="FP | Francisco Buiras | Research Doc",
    )
    frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 32 * mm - 16 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                          onPage=lambda c, d: (header(c, "Research Doc", "FP | Francisco Buiras | Competitor teardowns · ICP · personas · decision record"),
                                                None))])
    doc.build(story)
    print("OK ->", OUT)


# ================================================================ LOOM SCRIPT
def build_loom():
    OUT = "/home/fran/Descargas/FP_FranciscoBuiras_L15_LoomScript.pdf"
    story = []

    story.append(P("Before you hit record (2 minutes of setup)", "h2"))
    story.append(P(
        "• Close every tab except: the landing page, the GHL pipeline tab, and the GHL workflows tab (all logged in)."
        "<br/>• Set the browser to 100% zoom, hide bookmarks bar."
        "<br/>• Have the test-result page ready in a second window if you want to jump fast."
        "<br/>• The script is ~300 words — it times out at 2:00 when read at a normal pace. Do not rush; cut ad-libs instead."
        "<br/>• Say the mouse moves out loud in your head, not on the recording. Silence while navigating is fine.", "body"))
    story.append(Spacer(1, 8))

    beats = [
        ("0:00 – 0:15", "HOOK", "(landing page, hero on screen)",
         "Founders don't have a people problem. They have a delegation problem — and it costs most of them fifteen hours a week. "
         "So for my final project I built the thing I wished existed: a test that finds those hours in two minutes, and the funnel that gets them back."),
        ("0:15 – 0:45", "THE MAGNET", "(scroll the landing: hero → problem → what's inside)",
         "The Founder Delegation Test. Eight questions about your actual week — no email to see your number. "
         "At the end you get your recoverable hours, what they're worth at founder rates, and your first two handoffs. "
         "The full systems pack — inbox, calendar, the handoff script, a 30-day plan — lands in your inbox right after."),
        ("0:45 – 1:10", "THE ROUTING", "(scroll to the form, then jump to the two landing pages)",
         "Then one short form decides what happens next — honestly. If you're doing ten thousand a month and drowning in fifteen hours of ops, "
         "you go straight to the calendar and book a Matching Call with Pareto. If it's not your time yet, you still keep everything, "
         "and the thank-you page tells you exactly when to come back. Same funnel, two honest paths."),
        ("1:10 – 1:35", "THE MACHINE", "(GHL pipeline tab, then workflows tab, then one email)",
         "Under the hood: a pipeline that tracks every founder from lead to match. Four workflows — the kit delivery, "
         "the qualified follow-up, a nurture sequence for the not-yet-ready, and booking reminders. "
         "Here's one firing in real time: contact created, tagged, opportunity moved, email out."),
        ("1:35 – 1:55", "THE PROOF IT'S ORGANIZED", "(Business Map in Notion, then the Second Brain)",
         "The whole journey is mapped — every step linked to its real asset. And every decision traces back to my Second Brain: "
         "competitor teardowns, the client's own words, the math behind each promise."),
        ("1:55 – 2:00", "CLOSE", "(back to the landing, CTA on screen)",
         "Take the test. Find your fifteen hours. Pareto has the Right Hand waiting."),
    ]
    for t, label, screen, words in beats:
        story.append(KeepTogether([
            boxed([
                P(f"<b>{t}</b> &nbsp;·&nbsp; {label}", "cellB"),
                P(f"<i>On screen: {screen}</i>", "muted"),
                Spacer(1, 3),
                P(f"\u201C{words}\u201D", "line"),
            ]),
            Spacer(1, 6),
        ]))

    story.append(P("Delivery notes", "h2"))
    story.append(P(
        "• The two page-jumps in the ROUTING beat are the ones to rehearse — do them slowly enough to follow."
        "<br/>• If the GHL form shows a styled dark form on screen, hover it for a second; it sells the 'matches the brand' point silently."
        "<br/>• Don't say 'um' battles with the timer — the CLOSE line can be cut to \u201CTake the test. Pareto has the Right Hand waiting.\u201D"
        "<br/>• Record at 2:05 max; Loom's trim handles the rest.", "body"))


    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=32 * mm, bottomMargin=16 * mm,
        title="Loom Script (2:00) — Pareto Final Project",
        author="Francisco Buiras",
        subject="Two-minute Loom walkthrough script for the lead magnet funnel",
        creator="FP | Francisco Buiras | Loom Script",
    )
    frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 32 * mm - 16 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                          onPage=lambda c, d: (header(c, "Loom Script · 2:00", "FP | Francisco Buiras | Landing → test → routing → the machine → close"),
                                                None))])
    doc.build(story)
    print("OK ->", OUT)


if __name__ == "__main__":
    build_research()
    build_loom()
