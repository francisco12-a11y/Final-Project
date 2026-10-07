#!/usr/bin/env python3
"""Build The Right Hand Starter Kit — the email-delivered lead magnet (L6).

FP | Francisco Buiras | Right Hand Starter Kit
Branding: Pareto Talent — real logo, emerald #10B981 on dark #0B1526, Liberation Sans.
Re-run after editing content: python3 project-docs/build_kit_pdf.py
"""
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, KeepTogether, NextPageTemplate,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "lead-magnet",
                   "FP_FranciscoBuiras_L06_RightHandStarterKit.pdf")
LOGO = os.path.join(os.path.dirname(__file__), "..", "public",
                    "logo-pareto-talent.png")
TOTAL_PAGES = 6  # set by build() after the first pass

BRAND = HexColor("#10B981")
DEEP = HexColor("#065F46")
INK = HexColor("#0F172A")
BODY = HexColor("#334155")
MUTED = HexColor("#64748B")
LINE = HexColor("#E2E8F0")
SOFT = HexColor("#F5F9F7")
TINT = HexColor("#EAF6F1")
TINT_LINE = HexColor("#BFE8D9")
DARK = HexColor("#0B1526")
MINT = HexColor("#6EE7B7")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

_FDIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Lib", f"{_FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lib-B", f"{_FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lib-I", f"{_FDIR}/LiberationSans-Italic.ttf"))


def flat_logo(path, bg_hex="#0B1526", scale=2):
    """Flatten the palettized brand PNG onto the band color.

    The raw asset is P-mode with a binary transparency mask; ReportLab embeds
    it as RGB + SMask, which some PDF viewers render as corrupted streaks.
    A plain RGB image with no transparency renders identically everywhere.
    """
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    bg = Image.new("RGB", im.size,
                   tuple(int(bg_hex[i:i + 2], 16) for i in (1, 3, 5)))
    bg.paste(im, (0, 0), im)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "_kit_logo_flat.png")
    bg.save(out)
    return out


LOGO_FLAT = flat_logo(LOGO)


def st(name, **kw):
    base = dict(fontName="Lib", fontSize=10.5, leading=15.5, textColor=BODY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "h2kick":  st("h2kick", fontName="Lib-B", fontSize=9, leading=12,
                  textColor=DEEP, spaceAfter=2),
    "h2":      st("h2", fontName="Lib-B", fontSize=16.5, leading=20,
                  textColor=INK, spaceAfter=6),
    "h3":      st("h3", fontName="Lib-B", fontSize=12, leading=16,
                  textColor=INK, spaceBefore=10, spaceAfter=4),
    "body":    st("body"),
    "muted":   st("muted", fontSize=9.5, leading=13.5, textColor=MUTED),
    "cell":    st("cell", fontSize=9.5, leading=13),
    "cellB":   st("cellB", fontName="Lib-B", fontSize=9.5, leading=13,
                  textColor=INK),
    "cellMuted": st("cellMuted", fontSize=9.5, leading=13, textColor=MUTED),
    "quote":   st("quote", fontName="Lib-I", fontSize=10.5, leading=16.5,
                  textColor=INK),
    "rule":    st("rule", fontSize=10, leading=15),
    "darkT":   st("darkT", fontName="Lib-B", fontSize=15, leading=20,
                  textColor=white),
    "darkB":   st("darkB", fontSize=10, leading=15, textColor=MINT),
    "fill":    st("fill", fontName="Lib-B", fontSize=11, leading=15,
                  textColor=DEEP),
}


def P(text, style="body"):
    return Paragraph(text, S[style])


def sparkle(c, cx, cy, r, color=BRAND):
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


HEADER_H = 88 * mm


def on_first_page(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - HEADER_H, PAGE_W + 2, HEADER_H, stroke=0, fill=1)
    c.setFillColor(BRAND)
    c.rect(0, PAGE_H - HEADER_H, PAGE_W + 2, 2.2, stroke=0, fill=1)
    c.setFillColor(HexColor("#10B981"))
    c.setFillAlpha(0.08)
    c.circle(PAGE_W - 30 * mm, PAGE_H - 18 * mm, 42 * mm, stroke=0, fill=1)
    c.setFillAlpha(1)

    c.drawImage(LOGO_FLAT, MARGIN, PAGE_H - 20 * mm,
                width=22 * mm, height=9 * mm)
    c.setFillColor(HexColor("#8FA3B8"))
    c.setFont("Lib-B", 9.5)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 18 * mm,
                      "FREE SYSTEMS PACK")

    c.setFillColor(white)
    c.setFont("Lib-B", 29)
    c.drawString(MARGIN, PAGE_H - 38 * mm, "The Right Hand Starter Kit")
    c.setFillColor(MINT)
    c.setFont("Lib-B", 14)
    c.drawString(MARGIN, PAGE_H - 47 * mm,
                 "The systems, scripts, 30-day plan, and real costs of your first hire")

    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 10.5)
    c.drawString(MARGIN, PAGE_H - 57 * mm,
                 "Most delegation fails at the handoff. This kit fixes the handoff:")
    c.drawString(MARGIN, PAGE_H - 62 * mm,
                 "what to give away, the words to use, and the systems that keep it running.")

    chips = ["4 SYSTEMS", "30-DAY PLAN", "YOUR WEEK 1"]
    x = MARGIN
    c.setFont("Lib-B", 8.5)
    for label in chips:
        w = c.stringWidth(label, "Lib-B", 8.5) + 9 * mm
        c.setStrokeColor(HexColor("#2A3B52"))
        c.setLineWidth(0.8)
        c.roundRect(x, PAGE_H - 73 * mm, w, 7.5 * mm, 3.75 * mm, stroke=1, fill=0)
        c.setFillColor(MINT)
        c.drawCentredString(x + w / 2, PAGE_H - 70.8 * mm, label)
        x += w + 4 * mm
    c.restoreState()
    _footer(c, doc)


def on_later_pages(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, PAGE_H - 12 * mm, PAGE_W + 2, 12 * mm, stroke=0, fill=1)
    c.setFillColor(BRAND)
    c.rect(0, PAGE_H - 12 * mm, PAGE_W + 2, 2.2, stroke=0, fill=1)
    c.drawImage(LOGO_FLAT, MARGIN, PAGE_H - 8.4 * mm,
                width=12 * mm, height=4.9 * mm)
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib-B", 8)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 7.8 * mm,
                      "THE RIGHT HAND STARTER KIT")
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
                 "FP | Francisco Buiras | Right Hand Starter Kit · "
                 "© 2026 Pareto Talent · paretotalent.com")
    c.drawRightString(PAGE_W - MARGIN, 8.5 * mm,
                      f"Page {c.getPageNumber()} of {TOTAL_PAGES}")
    c.restoreState()


def boxed(flows, bg=SOFT, border=LINE, pad=12, accent=None):
    t = Table([[flows]], colWidths=[CONTENT_W])
    style = [
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad - 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 2),
    ]
    if accent:
        style.append(("LINEBEFORE", (0, 0), (0, -1), 2.5, accent))
    t.setStyle(TableStyle(style))
    return t


def filled_line(label, width_pts):
    t = Table([[Paragraph(label, S["fill"]), ""]],
              colWidths=[width_pts - 90, 90], rowHeights=[9 * mm])
    t.setStyle(TableStyle([
        ("LINEBELOW", (1, 0), (1, 0), 0.9, HexColor("#9FB3C8")),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def system_card(num, title, intro, rules):
    flows = [
        Paragraph(f"<b>SYSTEM {num}</b>", S["h2kick"]),
        Spacer(1, 2),
        Paragraph(title, S["h2"]),
        Paragraph(intro, S["body"]),
        Spacer(1, 4),
    ]
    for r in rules:
        flows.append(Paragraph(f"• {r}", S["rule"]))
    return flows


def plan_table():
    header = [P("<b>WEEK</b>", "cellMuted"), P("<b>HAND OFF</b>", "cellMuted"),
              P("<b>THE OWNER RUNS</b>", "cellMuted")]
    rows = [
        [P("<b>Week 1</b>", "cellB"),
         P("Inbox and calendar, your two biggest daily drains", "cell"),
         P("Your inbox rules and meeting defaults (Systems 1 and 2)", "cell")],
        [P("<b>Week 2</b>", "cellB"),
         P("CRM updates and lead/customer follow-ups", "cell"),
         P("The follow-up cadence you documented in week 1", "cell")],
        [P("<b>Week 3</b>", "cellB"),
         P("Invoicing, data entry, and the weekly report", "cell"),
         P("A one-page runbook per task: steps, tools, deadlines", "cell")],
        [P("<b>Week 4</b>", "cellB"),
         P("The rest of your test result, one task at a time", "cell"),
         P("The retro: what worked, what you take back, what scales", "cell")],
    ]
    t = Table([header] + rows, colWidths=[52, 231, 220], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TINT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BRAND),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def make_doc(path):
    doc = BaseDocTemplate(
        os.path.abspath(path), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 4 * mm, bottomMargin=18 * mm,
        title="The Right Hand Starter Kit · Pareto Talent",
        author="Francisco Buiras",
        subject="The systems, scripts, and 30-day plan to hand off the assistant job",
        creator="FP | Francisco Buiras | Right Hand Starter Kit",
    )
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 22 * mm - 18 * mm,
                  id="main")
    doc.addPageTemplates([
        PageTemplate(id="first", frames=[frame], onPage=on_first_page),
        PageTemplate(id="later", frames=[frame], onPage=on_later_pages),
    ])
    return doc


def make_story():
    story = [NextPageTemplate("later")]

    # ---- intro, clears the cover band
    story.append(Spacer(1, HEADER_H - 14 * mm))
    story.append(P(
        "Hiring fails at the handoff, not the search. Hand a person a job title "
        "and you get questions for a month. Hand them a system and they run. "
        "This kit is the system side: four tools our operators start with, a 30-day "
        "plan that sequences your first handoffs, what the hire should cost, the job "
        "posting to run, and how to treat the person in their first 90 days. Your "
        "test result told you how many hours are on the table. This kit is how you "
        "collect them."))
    story.append(Spacer(1, 12))

    # ---- Week 1
    week1 = [
        P("<b>YOUR WEEK 1</b>", "h2kick"),
        Spacer(1, 2),
        P("Start with the two biggest numbers from your test", "h2"),
        P("Open your test result. Take the two categories with the most hours; "
          "for most founders that is email and scheduling, then CRM and "
          "follow-ups. Write them here. These two handoffs are your entire "
          "week 1. Nothing else moves until these two run without you.", "body"),
        Spacer(1, 6),
        filled_line("<b>Handoff 1 (biggest number):</b>", CONTENT_W),
        Spacer(1, 3),
        filled_line("<b>Handoff 2:</b>", CONTENT_W),
        Spacer(1, 3),
        filled_line("<b>Recoverable hours from my test:</b>", CONTENT_W),
        Spacer(1, 8),
        P("Run the handoff script below with each one, then hold the line for "
          "seven days. The fastest way to fail is handing off five things at "
          "once and checking on all of them daily.", "muted"),
    ]
    story.append(KeepTogether(week1))
    story.append(Spacer(1, 14))

    # ---- The script
    script = [
        P("<b>THE HANDOFF SCRIPT</b>", "h2kick"),
        Spacer(1, 2),
        P("The conversation that makes it stick", "h2"),
        P("Use these words with your Right Hand, a VA, or anyone on your team:", "body"),
        Spacer(1, 6),
        boxed([
            P("\u201CI've mapped my week and this task, <b>[TASK]</b>, is now "
              "yours. Here's what 'done' looks like: <b>[OUTCOME, NOT METHOD]</b>. "
              "You own it end to end. The decision I'm handing you: "
              "<b>[E.G. REFUNDS UNDER $100]</b>. Friday, bring me one question: "
              "what did you decide?\u201D", "quote"),
        ], bg=TINT, border=TINT_LINE, accent=BRAND),
        Spacer(1, 8),
        P("<b>Three rules that make it permanent</b>", "h3"),
        P("• Hand off the <b>outcome</b>, not the method. If you script their steps, "
          "you've built a $10/hour puppet, and you're still the operator.", "body"),
        P("• Hand over one <b>decision authority</b> with every task. That is what "
          "makes it permanent.", "body"),
        P("• Check weekly on <b>decisions made</b>, never on tasks done.", "body"),
    ]
    story.append(KeepTogether(script))
    story.append(Spacer(1, 14))

    # ---- Systems
    story += [
        P("<b>THE FOUR SYSTEMS</b>", "h2kick"),
        Spacer(1, 2),
        P("Hand these over whole. They are written to be run, not adapted.", "h2"),
    ]
    story.append(Spacer(1, 6))
    story.append(KeepTogether(system_card(
        "1", "Inbox: the zero rules",
        "The founder sees decisions. The owner sees traffic. These rules split the two:",
        ["Two response targets: anything needing your decision, same day; "
         "everything else, 24 hours.",
         "Triage three times a day, never continuously. Notifications off.",
         "A living 'waiting on' list. Nothing sits unanswered without an owner and a date.",
         "You get copied only on decisions, never on discussions.",
         "Friday wipe: inbox at zero or every open thread has a next step and an owner."])))
    story.append(Spacer(1, 10))
    story.append(KeepTogether(system_card(
        "2", "Calendar: the defense rules",
        "Your calendar fills by default. These defaults fill it on purpose instead:",
        ["Meetings are 25 or 50 minutes by default. The old 30 and 60 were never chosen.",
         "Two no-meeting blocks a week, 3 hours each, marked as busy. They move for nothing.",
         "No agenda in the invite, no meeting. The owner can demand one on your behalf.",
         "15-minute buffers after anything decision-heavy.",
         "Once a month the owner brings you meetings to kill. Killing them is praise-worthy."])))
    story.append(Spacer(1, 10))
    story.append(KeepTogether(system_card(
        "3", "Follow-ups: the cadence",
        "Deals and customers rot in 'I should check in'. A cadence means nobody has to remember:",
        ["Every promise gets a date the moment it is made, logged where the owner lives.",
         "Leads: day 1, day 3, day 7, then a break-up email. Most deals die in silence, not in 'no'.",
         "Customers: a check-in at day 30 and day 90 that the owner drafts and you approve.",
         "One line per touch, logged. If it only happened in your head, it didn't happen."])))
    story.append(Spacer(1, 10))
    story.append(KeepTogether(system_card(
        "4", "The weekly check-in: 30 minutes, decisions only",
        "The meeting that replaces all the interruptions:",
        ["Fixed agenda: this week's numbers, decisions needed, blockers, one improvement.",
         "The owner brings decisions, not updates. Your job is to choose, not to catch up.",
         "Every decision gets an owner and a date before the meeting ends.",
         "Tasks never appear on this agenda. Tasks live in the systems above."])))
    story.append(Spacer(1, 14))

    # ---- 30 day plan
    plan = [
        P("<b>THE 30-DAY PLAN</b>", "h2kick"),
        Spacer(1, 2),
        P("One layer at a time", "h2"),
        P("Each week adds one layer. A layer only starts once the one before it "
          "runs for seven days without your help.", "body"),
        Spacer(1, 8),
        plan_table(),
    ]
    story.append(KeepTogether(plan))
    story.append(Spacer(1, 12))
    story.append(boxed([
        P("<b>What this is worth</b>", "cellB"),
        Spacer(1, 3),
        P("Founders who run this plan typically collect 10–15 hours a week by day "
          "30. Pareto prices a founder's hour at $200 when it goes to sales, "
          "product, and growth. Ten hours a week is about $8,600 a month of CEO "
          "work back on the calendar.", "cell"),
    ], accent=BRAND))
    story.append(Spacer(1, 14))

    # ---- closing
    closing = Table([[
        [Spacer(1, 4),
         P("Systems make delegation work. A person makes it scale.", "darkT"),
         Spacer(1, 6),
         P("This kit removes the excuse of 'nobody can do it like me'. What it "
           "can't do is be there at 8am Monday, running your inbox, your calendar, "
           "and your follow-ups so well that you forget they exist. That job is a "
           "Right Hand: hand-picked, AI-trained, matched to your task list within "
           "24 hours, backed by Freedom 40 (reclaim 40 hours in your first 30 "
           "days or the next month is free) and lifetime replacement.", "darkB"),
         Spacer(1, 10),
         P("<b>Book your Matching Call at paretotalent.com and bring this kit. "
           "Your Week 1 list is your first job description.</b>", "darkB")]]],
        colWidths=[CONTENT_W])
    closing.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 18),
        ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))
    story.append(Spacer(1, 10))

    # ---- What to budget
    budget = [
        P("<b>WHAT TO BUDGET</b>", "h2kick"),
        Spacer(1, 2),
        P("What a DIY hire costs by region", "h2"),
        P("Salary moves by region. These are the working norms the hiring world "
          "runs on, from the hiring-regions chapter of The Hire book:", "body"),
        Spacer(1, 6),
    ]
    rows = [
        [P("<b>Region</b>", "cellB"), P("<b>The norm</b>", "cellB")],
        [P("<b>Latin America</b>", "cellB"),
         P("From about $1,000/month full-time, working your time zone. Strong "
           "loyalty. Argentina adds a 13th salary (Aguinaldo), split between "
           "July and December.", "cell")],
        [P("<b>Southeast Asia</b>", "cellB"),
         P("The classic outsourcing hub; availability tightening. Budget a "
           "13th-month salary at year end.", "cell")],
        [P("<b>South Asia</b>", "cellB"),
         P("Scrappy problem-solvers who thrive with structure. Set explicit "
           "deadlines and build in buffers.", "cell")],
        [P("<b>Eastern Europe</b>", "cellB"),
         P("Higher salaries, less arbitrage, deep ownership. Direct feedback "
           "lands better than flattery.", "cell")],
    ]
    t = Table([rows[0]] + rows[1:], colWidths=[100, CONTENT_W - 100])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TINT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BRAND),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    budget.append(t)
    budget.append(Spacer(1, 6))
    budget.append(boxed([
        P("<b>Wherever they're from:</b> 20 days of paid time off is the norm. "
          "Pay on time or early through Wise, Payoneer, or PayPal, and cover the "
          "transfer fees. Late payment is the fastest way to lose a great hire.", "cell"),
    ], accent=BRAND))
    budget.append(Spacer(1, 8))
    budget.append(boxed([
        P("<b>Or skip the DIY route:</b> a fully-trained Right Hand from Pareto "
          "runs $3,000 a month on the annual plan plus a one-time $3,000 "
          "placement fee, and there is no contract until you hire. The fee "
          "covers 40+ hours of AI-stack training, the tool subscriptions, and "
          "the match. Check it against your own test: at $200 an hour, every 15 "
          "hours a week you get back is about $13,000 a month of founder work. "
          "The founder whose test said 37 hours is looking at $31,820.", "cell"),
    ], accent=BRAND))
    story.append(KeepTogether(budget))
    story.append(Spacer(1, 10))

    # ---- Job posting template
    posting = [
        P("<b>THE JOB POSTING TEMPLATE</b>", "h2kick"),
        Spacer(1, 2),
        P("Your Week 1 list, postable", "h2"),
        P("Your shortlist is your first job description. To post it anywhere, "
          "use this skeleton; it is built to filter while it attracts:", "body"),
        Spacer(1, 4),
        P("• <b>Title:</b> “WANTED! The World's Most [Adjective] Remote [Right "
          "Hand]” (sets the bar and self-selects).", "body"),
        P("• <b>First line, every posting:</b> “When you apply, make sure the "
          "subject line is: 'I actually read the instructions.'” Wrong subject "
          "line, auto-archived.", "body"),
        P("• <b>Include:</b> who you are (personality-forward), five "
          "responsibilities written as end results, the exact salary (never a "
          "range), and the traits of people who thrive in the role.", "body"),
        P("• <b>Always state the uncomfortable parts:</b> quiet workspace, "
          "reliable internet, a 60-day trial period. The right people nod. The "
          "wrong ones filter themselves.", "body"),
        P("• <b>Auto-reject:</b> didn't follow the instructions, sloppy "
          "formatting, sarcastic answers. Archive, never delete.", "body"),
    ]
    story.append(KeepTogether(posting))
    story.append(Spacer(1, 10))

    # ---- Go deeper: The Hire book
    deeper = [
        P("<b>GO DEEPER</b>", "h2kick"),
        Spacer(1, 2),
        P("Where this kit comes from", "h2"),
        P("The hiring system in these pages is from <b>The Hire: How to "
          "Attract, Hire, and Manage the Best Remote Talent in the World</b> by "
          "Kasim Aslam and Ivan Bunin, the team behind Pareto Talent. The "
          "book's site gives the templates away for free: the job posting, the "
          "trial-project offer, the contractor agreement, the rejection letter, "
          "and the one-page cheat sheet. Grab them at "
          "<link href=\"https://thehirebook.com/\" color=\"#10b981\"><b>thehirebook.com</b></link>.", "body"),
    ]
    story.append(KeepTogether(deeper))
    story.append(Spacer(1, 10))

    # ---- First 90 days (kicker + heading + lede kept together: an orphaned
    # kicker at a page bottom reads as a rendering bug)
    ninety = [
        KeepTogether([
            P("<b>THE FIRST 90 DAYS</b>", "h2kick"),
            Spacer(1, 2),
            P("Keep the person you hired", "h2"),
            P("Onboarding is a launch sequence: habits, expectations, and momentum "
              "are set here.", "body"),
        ]),
        Spacer(1, 4),
        P("• <b>Paper them up.</b> A simple contractor agreement, walked through "
          "section by section in a call. Transparency builds trust.", "body"),
        P("• <b>Set the pace.</b> Assign slightly more work than fits an 8-hour "
          "day, say so out loud, and hand over your real backlog, never "
          "busywork.", "body"),
        P("• <b>Pay on time or early</b> through Wise, Payoneer, or PayPal, and "
          "cover the transfer fees.", "body"),
        P("• <b>Daily short check-ins</b> until confidence is established, then "
          "two weekly meetings.", "body"),
        P("• <b>Celebrate the 60-day trial loudly.</b> It is nerve-wracking by "
          "design; passing it deserves a moment.", "body"),
    ]
    story.extend(ninety)

    # ---- The 2-6-2 rule
    twosixtwo = [
        P("<b>THE 2-6-2 RULE</b>", "h2kick"),
        Spacer(1, 2),
        P("How the assistant job becomes a Right Hand", "h2"),
        P("Kasim Aslam's standard: hand your assistant ten tasks. Two they "
          "will do worse than you. Six they will do just as well. Two they "
          "will do better than you ever did. Management orthodoxy says fix the "
          "bottom two. That is backwards: remove the bottom two and make the "
          "top two their whole job.", "body"),
        Spacer(1, 4),
        P("His proof: one executive assistant became his social director, "
          "another his automation director, and a third, Ivan Bunin, became "
          "his CTO, then his business partner.", "body"),
        Spacer(1, 4),
        P("That trajectory is the idea behind a Right Hand: someone AI-trained "
          "who starts on your Week 1 list and grows into the work only they "
          "can do.", "body"),
    ]
    story.append(KeepTogether(twosixtwo))
    story.append(Spacer(1, 10))

    recap = [
        P("<b>BEFORE YOU GO</b>", "h2kick"),
        Spacer(1, 2),
        P("The three moves, in order", "h2"),
        P("• <b>Fill in page 1.</b> Your two Week 1 handoffs and your recoverable "
          "hours, written down while the test result is fresh.", "body"),
        P("• <b>Run the script on handoff one this week.</b> Outcome, not method. "
          "One decision handed over with it.", "body"),
        P("• <b>When the test finds 10+ hours, book the Matching Call</b> and "
          "bring this kit. Your Week 1 list is the interview.", "body"),
    ]
    story.append(KeepTogether(recap))
    story.append(Spacer(1, 14))
    story.append(closing)
    return story


def build():
    global TOTAL_PAGES
    tmp = os.path.abspath(OUT) + ".tmp.pdf"
    make_doc(tmp).build(make_story())
    import pymupdf
    TOTAL_PAGES = len(pymupdf.open(tmp))
    os.remove(tmp)
    make_doc(OUT).build(make_story())
    print(f"OK -> {os.path.abspath(OUT)} ({TOTAL_PAGES} pages)")


if __name__ == "__main__":
    build()
