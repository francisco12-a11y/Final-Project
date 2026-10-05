#!/usr/bin/env python3
"""Fran's working guide: division of labor + submission rules.
Output: /home/fran/Descargas/Pareto_FinalProject_Guide_WhoDoesWhat.pdf
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

OUT = "/home/fran/Descargas/Pareto_FinalProject_Guide_WhoDoesWhat.pdf"

BRAND = HexColor("#10B981"); DEEP = HexColor("#065F46"); INK = HexColor("#0F172A")
BODY = HexColor("#334155"); MUTED = HexColor("#64748B"); LINE = HexColor("#E2E8F0")
SOFT = HexColor("#F5F9F7"); DARK = HexColor("#0B1526"); MINT = HexColor("#6EE7B7")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

_FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Lib", f"{_FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lib-B", f"{_FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lib-I", f"{_FDIR}/LiberationSans-Italic.ttf"))


def st(name, **kw):
    base = dict(fontName="Lib", fontSize=10, leading=14.5, textColor=BODY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "h1": st("h1", fontName="Lib-B", fontSize=19, leading=23, textColor=INK),
    "h2": st("h2", fontName="Lib-B", fontSize=13, leading=17, textColor=INK,
             spaceBefore=12, spaceAfter=5),
    "kick": st("kick", fontName="Lib-B", fontSize=8.5, leading=11,
               textColor=DEEP, spaceAfter=2),
    "body": st("body"),
    "muted": st("muted", fontSize=9, leading=12.5, textColor=MUTED),
    "item": st("item", fontSize=9.5, leading=13.5),
    "cell": st("cell", fontSize=8.5, leading=11.5, textColor=BODY),
    "cellB": st("cellB", fontName="Lib-B", fontSize=8.5, leading=11.5,
                textColor=INK),
    "boxB": st("boxB", fontName="Lib-B", fontSize=10.5, leading=14,
               textColor=INK),
    "box": st("box", fontSize=9.5, leading=13.5),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def checklist(items, accent=BRAND):
    rows = [[P("■", "cellB"), it] for it in items]
    t = Table(rows, colWidths=[14, CONTENT_W - 44 - 14])
    t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (0, -1), accent),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
    ]))
    return t


def on_page(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 34 * mm, PAGE_W, 34 * mm, stroke=0, fill=1)
    c.setFillColor(MINT)
    c.setFont("Lib-B", 8.5)
    c.drawString(MARGIN, PAGE_H - 12 * mm, "P A R E T O   T A L E N T   ·   B O O T C A M P   F I N A L   P R O J E C T")
    c.setFillColor(white)
    c.setFont("Lib-B", 20)
    c.drawString(MARGIN, PAGE_H - 21 * mm, "Who Does What — Working Guide")
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 10)
    c.drawString(MARGIN, PAGE_H - 27.5 * mm,
                 "FP | Francisco Buiras | The Founder Delegation Audit funnel · deadline Wednesday, October 7, 2026 (end of day)")
    # footer
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(MARGIN, 13 * mm, PAGE_W - MARGIN, 13 * mm)
    c.setFillColor(MUTED); c.setFont("Lib", 8)
    c.drawString(MARGIN, 8.5 * mm, "Working guide for Francisco Buiras — not part of the submission PDF.")
    c.drawRightString(PAGE_W - MARGIN, 8.5 * mm, f"Page {c.getPageNumber()} of 2")
    c.restoreState()


def boxed(flows, bg=SOFT, border=LINE):
    t = Table([[flows]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def link_table():
    rows = [
        [P("<b>LINK</b>", "cellB"), P("<b>ITEM</b>", "cellB"), P("<b>WHO</b>", "cellB")],
        [P("L1", "cell"), P("Second Brain", "cell"), P("Fran")],
        [P("L2", "cell"), P("Research doc (competitors + ICP)", "cell"), P("ZCode drafts → Fran hosts in Drive")],
        [P("L3", "cell"), P("Business Map", "cell"), P("ZCode drafts → Fran hosts")],
        [P("L4", "cell"), P("ClickUp board", "cell"), P("ZCode structure → Fran builds in ClickUp")],
        [P("L5", "cell"), P("SOP", "cell"), P("ZCode drafts → Fran hosts")],
        [P("L6", "cell"), P("Lead magnet live (Starter Kit PDF)", "cell"), P("ZCode PDF → Fran uploads to Drive (public)")],
        [P("L7", "cell"), P("Landing page", "cell"), P("ZCode (React, GitHub Pages)")],
        [P("L8", "cell"), P("Qualifying form", "cell"), P("Fran builds in GHL + sets redirects")],
        [P("L9", "cell"), P("Booking page (qualified)", "cell"), P("ZCode page + Fran's GHL calendar")],
        [P("L10", "cell"), P("Thank-you page (not qualified)", "cell"), P("ZCode")],
        [P("L11", "cell"), P("Pipeline screenshots folder", "cell"), P("Fran: GHL screenshots → public Drive folder")],
        [P("L12", "cell"), P("Workflow screenshots folder", "cell"), P("Fran: GHL screenshots → public Drive folder")],
        [P("L13", "cell"), P("Ads folder (5 ads)", "cell"), P("ZCode copy/design → Fran exports to Drive")],
        [P("L14", "cell"), P("Imagery folder", "cell"), P("ZCode prompts → Fran generates → Drive")],
        [P("L15", "cell"), P("Loom presentation (2 min)", "cell"), P("Fran records from ZCode's script")],
        [P("H1–H9", "cell"), P("Homework, Days 1–9", "cell"), P("Fran: paste your existing homework links")],
    ]
    t = Table(rows, colWidths=[42, 250, CONTENT_W - 42 - 250], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#EAF6F1")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BRAND),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    return t


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=40 * mm, bottomMargin=18 * mm,
        title="Pareto Final Project — Who Does What (Working Guide)",
        author="Francisco Buiras",
        subject="Division of labor and submission rules for the Pareto Talent bootcamp final project",
        creator="ZCode",
    )
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 40 * mm - 18 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])

    story = []

    story.append(P("The one-paragraph project", "h2"))
    story.append(P(
        "Pareto Talent needs more qualified founders booking Matching Calls. "
        "We build a lead magnet founders actually want — <b>The Founder Delegation "
        "Audit</b> — plus the funnel around it: landing page, qualifying form with "
        "two paths (qualified → booking page with the Pareto calendar; everyone "
        "else → thank-you page + nurture), and the automation behind it. Everything "
        "is built with Pareto's real branding (their logo, fonts, palette) and in "
        "Pareto's voice; we simulate running this campaign as a Pareto team member."))
    story.append(Spacer(1, 6))
    story.append(boxed([
        P("Non-negotiables", "boxB"),
        Spacer(1, 3),
        P("• <b>Every link must open incognito</b> — no logins, no shorteners. One broken link disqualifies the whole project.", "box"),
        P("• Submission is <b>ONE PDF</b>, written in Google Docs and exported, named <b>FP_FranciscoBuiras_ParetoBootcamp.pdf</b>.", "box"),
        P("• Sections in order: Cover, Link Index (L1–L15, H1–H9, dash if not built), Project Walkthrough (9 Parts).", "box"),
        P("• Everything named <b>FP | Francisco Buiras | Item Name</b> (tools) and <b>FP_FranciscoBuiras_L##_ItemName</b> (files/folders).", "box"),
        P("• Submit at bootcamp.paretotalent.com/finalproject <b>before end of day, October 7</b>.", "box"),
    ]))
    story.append(Spacer(1, 4))

    story.append(P("What ZCode builds (no accounts needed)", "h2"))
    story.append(checklist([
        P("<b>Site</b> — React app on GitHub Pages: landing (index), booking page for qualified (qualified.html, with your GHL calendar embed), thank-you page for unqualified. Pareto's real logo, fonts and palette. CTA above the fold, persona-matched heroes for the ads (?p=...).", "item"),
        P("<b>Lead magnet</b> — the Right Hand Starter Kit as a branded PDF (the 2-minute test on the landing personalizes it), hosted on the site and ready to attach in GHL.", "item"),
        P("<b>All email copy</b> — 1 delivery, 2 qualified follow-ups, 3 nurture, booking confirmation + reminder. Signed as the Pareto team.", "item"),
        P("<b>Ad copy ×5</b> — one per persona/angle, each with a matching landing hero.", "item"),
        P("<b>Imagery prompts</b> — on-brand prompt pack for you to generate.", "item"),
        P("<b>Docs</b> — research doc, Business Map, ClickUp board structure, SOP text, walkthrough draft for the submission PDF, Loom script.", "item"),
        P("<b>Repo + deploys</b> — github.com/francisco12-a11y/Final-Project, auto-deploys on every push.", "item"),
    ]))
    story.append(Spacer(1, 4))

    story.append(P("What only Fran can do (accounts + face)", "h2"))
    story.append(checklist([
        P("<b>GHL form (L8):</b> build the qualifying form, paste the embed into the landing slot ZCode leaves ready, set conditional redirects (qualified → …/qualified.html, unqualified → …/thank-you.html), and run both tests.", "item"),
        P("<b>GHL pipeline + 4 workflows (L11, L12):</b> opt-in (deliver + tag + opportunity + notify), qualified follow-up (2 emails), unqualified nurture (3 emails), booking (confirmation + reminder). Screenshot everything into the two Drive folders.", "item"),
        P("<b>Drive:</b> create the folders with exact FP naming, upload the kit PDF + ads + imagery + screenshots, set all to 'Anyone with the link can view'.", "item"),
        P("<b>ClickUp (L4):</b> build the board from ZCode's milestone structure.", "item"),
        P("<b>Second Brain (L1):</b> drop the Pareto frameworks/sources in (ZCode gives the structure).", "item"),
        P("<b>Loom (L15):</b> record the 2-minute walkthrough from ZCode's script.", "item"),
        P("<b>H1–H9:</b> collect your Day 1–9 homework links.", "item"),
        P("<b>Submit:</b> paste the walkthrough into Google Docs, insert every full URL, export the PDF, submit before Oct 7 EOD.", "item"),
    ]))
    story.append(Spacer(1, 4))

    story.append(P("Every link, and whose hands it needs", "h2"))
    story.append(link_table())
    story.append(Spacer(1, 4))

    story.append(P("The 5-minute check before you hit submit", "h2"))
    story.append(P(
        "1. Open every link incognito — if anything asks to log in, fix the sharing. "
        "2. Test the form twice: once as qualified (must land on the booking page), "
        "once as unqualified (must land on the thank-you page). "
        "3. Opt in with your own email and confirm the kit PDF arrives. "
        "4. Check every label L1–L15 and H1–H9 exists in the index (dash if not built). "
        "5. File name exactly FP_FranciscoBuiras_ParetoBootcamp.pdf, exported from Google Docs."))
    story.append(Spacer(1, 6))
    story.append(P(
        "Suggested order this week: <b>today</b> ZCode finishes the React site + audit PDF; "
        "<b>next</b> Fran builds the GHL form + workflows from ZCode's spec and tests the chain; "
        "<b>then</b> ads/imagery/emails go in; <b>last day</b> is Loom + Drive links + the submission PDF. "
        "Scoring: 20–25 = certificate + talent pool interview. Anything extra (test receipts, "
        "persona-matched ads, the audit-as-sales-tool bridge) lifts the category it belongs to.", "body"))

    doc.build(story)
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
