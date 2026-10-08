#!/usr/bin/env python3
"""SOP PDF (L5) — Lead Magnet Launch Process.
Output: /home/fran/Descargas/FP_FranciscoBuiras_L05_SOP.pdf
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

OUT = "/home/fran/Descargas/FP_FranciscoBuiras_L05_SOP.pdf"

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
    "body": st("body"),
    "muted": st("muted", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": st("cell", fontSize=8.5, leading=11.5, textColor=BODY),
    "cellB": st("cellB", fontName="Lib-B", fontSize=8.5, leading=11.5,
                textColor=INK),
    "step": st("step", fontSize=9.5, leading=13.5),
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
                 "P A R E T O   T A L E N T   ·   S T A N D A R D   O P E R A T I N G   P R O C E D U R E")
    c.setFillColor(white)
    c.setFont("Lib-B", 16)
    c.drawString(MARGIN, PAGE_H - 17 * mm, "Lead Magnet Launch Process")
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 9)
    c.drawString(MARGIN, PAGE_H - 22.5 * mm,
                 "FP | Francisco Buiras | SOP · version 1.1 · owner: Growth · review after every launch")
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    c.setFillColor(MUTED); c.setFont("Lib", 7.5)
    c.drawString(MARGIN, 8 * mm,
                 "SOP-LM-01 · Follow top to bottom. Every phase has a gate; do not start the next phase before the gate passes.")
    c.drawRightString(PAGE_W - MARGIN, 8 * mm, f"Page {c.getPageNumber()}")
    c.restoreState()


def phase(kicker, title, goal, steps, gate):
    flows = [
        P(f"<b>{kicker}</b>", "h2kick"),
        Spacer(1, 1),
        P(title, "h2"),
        P(f"<b>Goal:</b> {goal}", "body"),
        Spacer(1, 3),
    ]
    rows = [[P(f"<b>{i + 1}</b>", "cellB"), P(s, "cell")]
            for i, s in enumerate(steps)]
    tw = Table(rows, colWidths=[16, CONTENT_W - 16 - 14])
    tw.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("TEXTCOLOR", (0, 0), (0, -1), BRAND),
        ("LEFTPADDING", (0, 0), (0, -1), 2),
    ]))
    flows.append(tw)
    flows.append(Spacer(1, 3))
    flows.append(boxed([P(f"<b>Gate — done when:</b> {gate}", "cell")],
                       bg=TINT, border=HexColor("#BFE8D9")))
    flows.append(Spacer(1, 10))
    return KeepTogether(flows)


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


story = []

story.append(P("1 · Purpose and scope", "h2"))
story.append(P(
    "This SOP launches a lead magnet that books Matching Calls with Pareto Talent. It covers the "
    "full path: strategy, magnet build, funnel, automation, launch materials, verification, and "
    "submission-ready documentation. Run it top to bottom; each phase ends with a gate that must "
    "pass before the next phase starts. Default duration is five working days working backwards "
    "from launch day."))
story.append(Spacer(1, 4))
story.append(table([
    [P("<b>Role</b>", "cellB"), P("<b>Owns</b>", "cellB")],
    [P("Operator (EA / Right Hand candidate)", "cell"),
     P("Phases 1–7 end to end, docs, verification, reporting", "cell")],
    [P("Marketing lead", "cell"),
     P("Approves offer, qualification criteria, and final submission", "cell")],
    [P("Build support (AI-assisted)", "cell"),
     P("Pages, magnet production, ad copy, imagery prompts, email drafts", "cell")],
], [170, CONTENT_W - 170]))
story.append(Spacer(1, 4))
story.append(table([
    [P("<b>Stack</b>", "cellB"), P("<b>Used for</b>", "cellB")],
    [P("ClickUp", "cell"), P("Milestones, tasks, owners, dates (Phase 0 board, built first)", "cell")],
    [P("GitHub Pages + React", "cell"), P("Public funnel pages, magnet hosting", "cell")],
    [P("GoHighLevel", "cell"), P("Form, pipeline, workflows, emails, calendar", "cell")],
    [P("Notion / diagram tool", "cell"), P("Business Map, research doc", "cell")],
    [P("Google Drive + Docs", "cell"), P("Assets, folders, final submission PDF", "cell")],
], [130, CONTENT_W - 130]))

story.append(Spacer(1, 10))
story.append(phase(
    "PHASE 1", "Strategy and research (day 1)",
    "Know exactly who the magnet is for and what it promises before anything is built.",
    ["Write the ICP in the client's own words, from Pareto's public pages and calls.",
     "Build 3–4 founder personas, each from a cause (growth, burned by a VA, no systems, margin protection), each with a quoted pain line.",
     "Study 3 competitor lead magnets: format, promise, audience, qualification, and what happens after opt-in.",
     "Choose the magnet format against the goal: interactive test for qualification data, template pack for usefulness, calculator for math.",
     "Write the qualification criteria as hard rules (this launch: revenue $10k+/mo AND 15+ ops hrs/wk AND owner).",
     "Title with MAGIC: Measurable, Actionable, Goal-driven, Interested audience, Credible. Score it against the Value Equation."],
    "Marketing lead approves the one-paragraph offer, the criteria, and the title."))

story.append(phase(
    "PHASE 2", "Magnet build (day 2)",
    "Ship the artifact and make it personal: the output must map to the visitor's answers.",
    ["Draft the content in one file (source of truth), then produce the branded PDF or app.",
     "Apply brand rules: real logo, exact palette and fonts from the company site, no invented claims.",
     "If the magnet has a test, wire every answer to a named field that the CRM can read.",
     "Make the result personal before asking for anything: hours, dollars, and their next step.",
     "Host the file publicly and keep one canonical link."],
    "The magnet opens incognito with no login, and the personalization demonstrably changes with different answers."))

story.append(phase(
    "PHASE 3", "Funnel build (day 2–3)",
    "One page in, two honest paths out, and a calendar at the end of the good path.",
    ["Landing page: headline states the problem in the client's words; CTA above the fold; one job per page.",
     "Embed the qualifying form with the questions that map 1:1 to the criteria.",
     "Set conditional redirects: qualified → booking page with calendar; everyone else → thank-you page. Never a dead end.",
     "Booking page carries the real calendar and one instruction: bring the magnet.",
     "Thank-you page delivers the magnet, explains why there is no call yet, and sets the nurture expectation.",
     "Name everything FP | First Last | Item Name from the first commit."],
    "Form tested twice in incognito — once as qualified, once as not — and both land on the right page."))

story.append(phase(
    "PHASE 4", "Automation (day 3–4)",
    "Six workflows, ten emails, one pipeline. Every lead is touched by a system, not a person.",
    ["Pipeline: New Lead, Qualified, Call Booked, Call Done, Won (Matched), Nurture. Tags: qualified, nurture, kit-sent, booked, no-show.",
     "Workflow 1 Opt-in: form submitted → opportunity created, qualification checked, kit delivered as attachment, tags set, operator notified.",
     "Workflow 2 Qualified follow-up: wait 1 day, check for booking, chase day 1 and day 3, and re-check before the last touch so fresh bookings are never chased.",
     "Workflow 3 Nurture: 3 teach-only emails (days 2, 5, 8). Never pitch this list.",
     "Workflow 4 Booking: confirmation immediately (calendar default off), reminder 24h before.",
     "Workflows 5 and 6 run off appointment status: Showed sends the next-steps email, No Show sends the rebook email with the calendar link.",
     "Mark every call Showed or No-show in the calendar the same hour; the status pair fires off that.",
     "Write every email to one job, under 180 words, with the magnet doing the persuading."],
    "Workflow 1 fires on a real submission: attachment received, tags set, opportunity created, notification sent. A no-show test produces the rebook email."))

story.append(phase(
    "PHASE 5", "Launch materials (day 4)",
    "Five ads that are five different arguments, not one argument five times.",
    ["One ad per persona, each with that persona's pain line and its own landing hero (ad-to-page match).",
     "Imagery system: same palette and tone across ads and page placeholders; prompts saved so visuals regenerate identically.",
     "Ads link to the landing with the persona parameter so the hero echoes the ad.",
     "Drive folders with exact naming, all set to Anyone with the link can view."],
    "Each of the five ads, read cold, could not be swapped with another."))

story.append(phase(
    "PHASE 6", "Verification (day 5, morning)",
    "Receipts, not claims. Every proof is a screenshot in the Drive folders.",
    ["Run the 7-step end-to-end test (form twice, kit received, pipeline stage, tags, booking emails, workflow histories).",
     "Open all index links incognito; fix any login wall or error the same hour.",
     "Screenshot workflows executing, pipeline stages, and both redirect paths.",
     "Re-check naming across tools, folders, and files against the convention."],
    "The verification folder contains a screenshot for every claim the walkthrough will make."))

story.append(phase(
    "PHASE 7", "Document and submit (day 5)",
    "The walkthrough is written evidence, assembled while the tests are fresh.",
    ["Write the walkthrough against the required parts; every claim is text plus a screenshot.",
     "Link index: every line, full URLs, dash for anything not built. Never fake a link.",
     "Assemble in Google Docs, export to PDF, name per convention, submit before the deadline.",
     "Log what worked and what slipped; update this SOP the same day."],
    "Submitted, and this SOP has one paragraph of retrospective added."))

story.append(Spacer(1, 4))
story.append(P("Non-negotiables (every launch)", "h2"))
story.append(boxed([
    P("• Every link opens incognito. One login wall or dead link kills the launch.", "cell"),
    P("• The form is tested as both people: the qualified founder and the early one.", "cell"),
    P("• The magnet arrives by email, as an attachment, within a minute.", "cell"),
    P("• Proof is a screenshot, not a sentence.", "cell"),
    P("• Nothing is named Copy, Untitled, or Workflow 3.", "cell"),
    P("• Gaps are marked as gaps. Never fake a link.", "cell"),
]))

story.append(Spacer(1, 4))
story.append(P("Default timeline (T = launch day)", "h2"))
story.append(table([
    [P("<b>When</b>", "cellB"), P("<b>Phase</b>", "cellB"), P("<b>Gate</b>", "cellB")],
    [P("T-5", "cell"), P("1 · Strategy and research", "cell"), P("Offer + criteria + title approved", "cell")],
    [P("T-4", "cell"), P("2 · Magnet build", "cell"), P("Magnet personal and public", "cell")],
    [P("T-3", "cell"), P("3 · Funnel build", "cell"), P("Both redirect paths tested", "cell")],
    [P("T-2", "cell"), P("4 · Automation", "cell"), P("Workflow 1 fires end to end", "cell")],
    [P("T-1", "cell"), P("5 · Launch materials", "cell"), P("Five ads, none swappable", "cell")],
    [P("T, morning", "cell"), P("6 · Verification", "cell"), P("Screenshots for every claim", "cell")],
    [P("T, by 6 pm", "cell"), P("7 · Document and submit", "cell"), P("Submitted + SOP updated", "cell")],
], [70, 220, CONTENT_W - 70 - 220]))


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=32 * mm, bottomMargin=16 * mm,
        title="SOP-LM-01 Lead Magnet Launch Process — Pareto Talent",
        author="Francisco Buiras",
        subject="Standard operating procedure for launching a Pareto Talent lead magnet",
        creator="FP | Francisco Buiras | SOP",
    )
    frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 32 * mm - 16 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    doc.build(story)
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
