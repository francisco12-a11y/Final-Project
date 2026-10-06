#!/usr/bin/env python3
"""GHL Build Spec PDF — everything Fran needs to build the funnel in GoHighLevel.
Output: /home/fran/Descargas/Pareto_FinalProject_GHL_BuildSpec.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Table, TableStyle,
                                KeepTogether)

OUT = "/home/fran/Descargas/Pareto_FinalProject_GHL_BuildSpec.pdf"

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


def st(name, **kw):
    base = dict(fontName="Lib", fontSize=9.5, leading=13.5, textColor=BODY)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "h2kick": st("h2kick", fontName="Lib-B", fontSize=8, leading=11,
                 textColor=DEEP, spaceAfter=2),
    "h2": st("h2", fontName="Lib-B", fontSize=13.5, leading=17, textColor=INK,
             spaceAfter=5),
    "h3": st("h3", fontName="Lib-B", fontSize=10.5, leading=14, textColor=INK,
             spaceBefore=8, spaceAfter=3),
    "body": st("body"),
    "muted": st("muted", fontSize=8.5, leading=12, textColor=MUTED),
    "cell": st("cell", fontSize=8.5, leading=11.5, textColor=BODY),
    "cellB": st("cellB", fontName="Lib-B", fontSize=8.5, leading=11.5,
                textColor=INK),
    "mail": st("mail", fontSize=9, leading=13, textColor=BODY),
    "mailI": st("mailI", fontName="Lib-I", fontSize=9, leading=13,
                textColor=BODY),
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
    c.drawString(MARGIN, PAGE_H - 17 * mm, "GoHighLevel Build Spec")
    c.setFillColor(HexColor("#9FB3C8"))
    c.setFont("Lib", 9)
    c.drawString(MARGIN, PAGE_H - 22.5 * mm,
                 "FP | Francisco Buiras | Pipeline, form, workflows, and all 9 emails · build exactly this, in this order")
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    c.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
    c.setFillColor(MUTED); c.setFont("Lib", 7.5)
    c.drawString(MARGIN, 8 * mm,
                 "Working spec for Francisco Buiras — build in GHL, then screenshot everything for L11 and L12.")
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


def table(rows, widths, header=True):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), TINT),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, BRAND),
        ]
    style.append(("LINEBELOW", (0, 1), (-1, -1), 0.4, LINE))
    t.setStyle(TableStyle(style))
    return t


def email_card(subject, body, meta):
    flows = [
        P(f"<b>Subject:</b> {subject}", "cellB"),
        P(meta, "muted"),
        Spacer(1, 4),
        P(body.replace("\n\n", "<br/><br/>").replace("\n", "<br/>"), "mail"),
    ]
    return KeepTogether([boxed(flows, bg=SOFT, border=LINE), Spacer(1, 4)])


def workflow(title, steps, note=None):
    flows = [Paragraph(title, S["h2"]), Spacer(1, 2)]
    rows = [[P(f"<b>{i + 1}</b>", "cellB"), P(step, "cell")]
            for i, step in enumerate(steps)]
    tw = table(rows, [18, CONTENT_W - 18 - 12], header=False)
    tw.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (0, -1), BRAND),
        ("LEFTPADDING", (0, 0), (0, -1), 2),
    ]))
    flows.append(tw)
    if note:
        flows.append(Spacer(1, 3))
        flows.append(P(note, "muted"))
    return KeepTogether(flows)


story = []

# ---------------------------------------------------------------- 1 naming
story.append(P("1 · Naming (the judges check this)", "h2"))
story.append(P(
    "Every item you create in GHL gets the exact prefix <b>FP | Francisco Buiras | </b>. "
    "So: <b>FP | Francisco Buiras | Qualifying Form</b>, <b>FP | Francisco Buiras | Lead Magnet Pipeline</b>, "
    "<b>FP | Francisco Buiras | Opt-in Workflow</b>, and so on for the 4 workflows and every email. "
    "Nothing named Copy, Untitled, or Workflow 3 anywhere."))

# ---------------------------------------------------------------- 2 pipeline
story.append(P("2 · The pipeline (one pipeline, six stages)", "h2"))
story.append(P("Pipeline name: <b>FP | Francisco Buiras | Lead Magnet Pipeline</b>. "
               "Every form submission creates or updates an opportunity in it.", "body"))
story.append(Spacer(1, 4))
story.append(table([
    [P("<b>Stage</b>", "cellB"), P("<b>Who lands there</b>", "cellB"), P("<b>What moves them out</b>", "cellB")],
    [P("1 · New Lead", "cell"), P("Anyone who submits the qualifying form", "cell"),
     P("Workflow tags qualified or nurture within seconds", "cell")],
    [P("2 · Qualified", "cell"), P("Passed the screen: revenue $10k+/mo, 15+ hrs/wk ops, owner", "cell"),
     P("Books a call (appointment created)", "cell")],
    [P("3 · Call Booked", "cell"), P("Appointment on the Pareto calendar", "cell"),
     P("Call happens (no-show gets a rebook email, see workflow 4 note)", "cell")],
    [P("4 · Call Done", "cell"), P("Matching Call completed, candidates being matched", "cell"),
     P("Founder picks a candidate", "cell")],
    [P("5 · Won (Matched)", "cell"), P("Founder picked a Right Hand", "cell"),
     P("End of the line, celebrate", "cell")],
    [P("6 · Nurture (Not Qualified)", "cell"), P("Failed the screen; gets the kit + 3 nurture emails", "cell"),
     P("Retakes the test and qualifies later", "cell")],
], [80, 215, CONTENT_W - 80 - 215]))
story.append(Spacer(1, 4))
story.append(P("Tags to create: <b>qualified</b>, <b>nurture</b>, <b>kit-sent</b>, <b>booked</b>. "
               "Tags are what the workflows key off.", "body"))

# ---------------------------------------------------------------- 3 fields
story.append(P("3 · Custom fields (quiz answers + qualification)", "h2"))
story.append(P(
    "Create these six custom fields exactly. When you build the form and send ZCode the embed code, "
    "the quiz answers auto-fill them from the URL, so a founder never answers the same question twice.", "body"))
story.append(Spacer(1, 4))
story.append(table([
    [P("<b>Field name</b>", "cellB"), P("<b>Type</b>", "cellB"), P("<b>Filled by</b>", "cellB"), P("<b>Used for</b>", "cellB")],
    [P("quiz_hours_email", "cell"), P("Numeric", "cell"), P("Quiz, URL param q_email", "cell"), P("Week 1 personalization, tagging", "cell")],
    [P("quiz_hours_crm", "cell"), P("Numeric", "cell"), P("Quiz, URL param q_crm", "cell"), P("Same", "cell")],
    [P("quiz_hours_admin", "cell"), P("Numeric", "cell"), P("Quiz, URL param q_admin", "cell"), P("Same", "cell")],
    [P("quiz_hours_support", "cell"), P("Numeric", "cell"), P("Quiz, URL param q_support", "cell"), P("Same", "cell")],
    [P("quiz_hours_hiring", "cell"), P("Numeric", "cell"), P("Quiz, URL param q_hiring", "cell"), P("Same", "cell")],
    [P("quiz_who_runs", "cell"), P("Text", "cell"), P("Quiz, URL param q_who", "cell"), P("Persona tag, email personalization", "cell")],
], [110, 50, 130, CONTENT_W - 110 - 50 - 130]))
story.append(Spacer(1, 4))
story.append(P(
    "Fallback if URL pre-population fights you: skip the six fields, the form asks its own questions "
    "(section 4), and the funnel still routes correctly. The quiz answers also live in a summary strip "
    "on the page above the form, so the founder sees them either way.", "body"))

# ---------------------------------------------------------------- 4 form
story.append(P("4 · The qualifying form", "h2"))
story.append(P("Form name: <b>FP | Francisco Buiras | Qualifying Form</b>. Six questions, one screen. "
               "Questions 1 to 3 are the qualification screen (each maps to a criterion from the strategy).", "body"))
story.append(Spacer(1, 4))
story.append(table([
    [P("<b>#</b>", "cellB"), P("<b>Question</b>", "cellB"), P("<b>Options</b>", "cellB"), P("<b>Qualifies when</b>", "cellB")],
    [P("1", "cell"), P("What's your monthly revenue today?", "cell"),
     P("Idea / pre-revenue · Under $10k · $10k–$50k · $50k+", "cell"), P("$10k or more", "cell")],
    [P("2", "cell"), P("How many hours a week does the assistant job take (inbox, calendar, CRM, follow-ups)?", "cell"),
     P("Under 5 · 5–14 · 15+", "cell"), P("15 or more", "cell")],
    [P("3", "cell"), P("Are you the owner or co-founder, and the hiring decision-maker?", "cell"),
     P("Yes · Not yet / other", "cell"), P("Yes", "cell")],
    [P("4", "cell"), P("Do you run paid ads or serve active clients?", "cell"),
     P("Yes · Not yet", "cell"), P("Bonus signal, not required", "cell")],
    [P("5", "cell"), P("Who runs those tasks today?", "cell"),
     P("Me during work hours · Me nights and weekends · Partly delegated · An assistant who needs managing", "cell"),
     P("Context only", "cell")],
    [P("6", "cell"), P("Where should we send the Starter Kit?", "cell"),
     P("Email field (contact field, required)", "cell"), P("Always", "cell")],
], [14, 185, 185, CONTENT_W - 14 - 185 - 185]))
story.append(Spacer(1, 4))
story.append(boxed([
    P("<b>On Submit — updated Oct 6 (routing moved to the landing page)</b>", "cellB"),
    Spacer(1, 3),
    P("Choose <b>Show a message</b> (text: “Taking you to your next step\u2026”). Do NOT set a redirect here: "
      "the landing page itself listens for the form's submission and routes it \u2014 the visitor's test answers "
      "(revenue, hours, owner) decide between qualified.html and thank-you.html. Keeping the redirect off avoids "
      "the two hops fighting each other.", "cell"),
    Spacer(1, 3),
    P("Optional prefill: in each field's settings, add URL parameters q_email, q_crm, q_admin, q_support, "
      "q_hiring, q_who, q_total \u2014 the quiz answers arrive in the iframe URL and pre-fill the form.", "cell"),
]))
story.append(Spacer(1, 4))
story.append(Spacer(1, 4))
story.append(boxed([
    P("<b>Styling the form to match the site (do this in the form builder)</b>", "cellB"),
    Spacer(1, 3),
    P("The form is a cross-origin iframe, so it must be styled inside GHL (Style panel of the form builder). "
      "Enter these values and it becomes indistinguishable from the landing page:", "cell"),
    Spacer(1, 3),
    P("\u2022 Form background: #0B1119 (or transparent if the option exists)", "cell"),
    P("\u2022 Question / label text: #F0F4F8", "cell"),
    P("\u2022 Help text: #94A3B8", "cell"),
    P("\u2022 Input background: #0F1923 \u2014 input border: #2A3B52 \u2014 input text: #F0F4F8", "cell"),
    P("\u2022 Button background: #10B981 \u2014 button text: #050A0E \u2014 button radius: 12px", "cell"),
    P("\u2022 Button label: Continue. Font: DM Sans (falls back fine to default sans).", "cell"),
    P("\u2022 If your builder shows a Custom CSS box, paste:\u00A0"
      "input,select{background:#0F1923!important;color:#F0F4F8!important;border:1px solid #2A3B52!important;border-radius:8px!important}"
      " label{color:#F0F4F8!important} button{background:#10B981!important;color:#050A0E!important;border-radius:12px!important}", "cell"),
]))
story.append(Spacer(1, 4))
story.append(P(
    "When the form works, send ZCode the embed code and the quiz answers start auto-filling fields 5's "
    "sibling custom fields (section 3). Paste the embed into the marked slot on the landing page and "
    "ZCode pushes it same day.", "body"))

# ---------------------------------------------------------------- WF1
story.append(P("5 · Workflow 1 — Opt-in (deliver, tag, opportunity, notify)", "h2"))
story.append(workflow(
    "<b>FP | Francisco Buiras | Opt-in Workflow</b>",
    ["Trigger: <b>Form Submitted</b> (your qualifying form)",
     "Action: <b>Create/Edit Opportunity</b> in Lead Magnet Pipeline, stage New Lead, status Open, value $3,000 (one month)",
     "Action: <b>If/Else</b> — contact matches the qualified rule (revenue $10k+, hours 15+, owner yes)",
     "Branch QUALIFIED → <b>Add Tag</b> qualified",
     "Branch QUALIFIED → <b>Send Email</b> E1 below (attach the kit PDF to the email)",
     "Branch QUALIFIED → <b>Notify</b> you (email + app notification): 'New qualified founder: {{contact.first_name}}, {{contact.email}}'",
     "Branch NURTURE → <b>Add Tag</b> nurture",
     "Branch NURTURE → <b>Send Email</b> E1 below (same kit, same email works for both)",
     "Branch NURTURE → Move opportunity to stage Nurture (Not Qualified)",
     "Action (both branches): <b>Add Tag</b> kit-sent"]))
story.append(Spacer(1, 4))
story.append(email_card(
    "E1 · Your Right Hand Starter Kit (inside: your Week 1)",
    "{{contact.first_name}}, your kit is attached.\n\n"
    "Four systems, one script, and a 30-day plan. Everything in it is written to hand off on day one, not to teach you theory.\n\n"
    "Start here: page one asks for your two biggest handoffs. Write them in, run the script right below them, and hold the line for seven days. Most founders start with email and scheduling.\n\n"
    "One rule while you read: hand off outcomes, never methods. That's the difference between an operator and an assistant with extra steps.\n\n"
    "Already scaling and want it done for you? Book a Matching Call and bring the kit: [book link]\n\n"
    "— Pareto Talent",
    "Send immediately in workflow 1, both branches · attach FP_FranciscoBuiras_L06_RightHandStarterKit.pdf"))

# ---------------------------------------------------------------- WF2
story.append(P("6 · Workflow 2 — Qualified follow-up (2 emails, only if they didn't book)", "h2"))
story.append(workflow(
    "<b>FP | Francisco Buiras | Qualified Follow-up</b>",
    ["Trigger: <b>Tag Added</b> = qualified",
     "Action: <b>Wait</b> 1 day",
     "Action: <b>If/Else</b> — does the contact have a calendar appointment booked?",
     "Branch NO BOOKING → <b>Send Email</b> E2",
     "Branch NO BOOKING → <b>Wait</b> 2 days → <b>Send Email</b> E3 → End",
     "Branch BOOKED → End (workflow 4 takes over)"],
    "Timing per the rubric: qualified leads who didn't book get exactly 2 touches, day 1 and day 3 after opting in."))
story.append(Spacer(1, 4))
story.append(email_card(
    "E2 · You qualified. This is what the call is for",
    "{{contact.first_name}}, your answers put you in the group this program was built for: real revenue, real ops load, and hiring on your plate.\n\n"
    "The Matching Call is 20 minutes. We walk through your kit, pressure-test your Week 1 handoffs, and map your first month. Within 24 hours you meet 3+ hand-picked, AI-trained Right Hand candidates.\n\n"
    "No contracts and no payment unless you pick someone you're excited about.\n\n"
    "Bring the kit with Week 1 filled in. Founders who arrive with it running usually match in days.\n\n"
    "[Book your Matching Call]\n\n— Pareto Talent",
    "Send day 1 after opt-in, qualified only"))
story.append(email_card(
    "E3 · If you've been burned by a VA before, read this one",
    "{{contact.first_name}}, most founders who book with us swore off hiring first. The story is usually the same: they hired cheap, wrote no systems, and spent three months managing instead of saving.\n\n"
    "The fix is boring: vetting, training, and a written system. We hand-pick the top 1% and train them 40+ hours on the AI stack before you ever meet them. Your kit is the system they start from. Your Week 1 is their first job description.\n\n"
    "And if it still goes sideways: Freedom 40 says reclaim 40 hours in your first 30 days or the next month is free, and replacement is lifetime, no waiting period.\n\n"
    "The call is 20 minutes. Worst case, you leave with your first month planned.\n\n"
    "[Book your Matching Call]\n\n— Pareto Talent",
    "Send day 3 after opt-in, qualified only, still no booking"))

# ---------------------------------------------------------------- WF3
story.append(P("7 · Workflow 3 — Nurture (3 emails, not qualified)", "h2"))
story.append(workflow(
    "<b>FP | Francisco Buiras | Unqualified Nurture</b>",
    ["Trigger: <b>Tag Added</b> = nurture",
     "Action: <b>Wait</b> 2 days → <b>Send Email</b> E4",
     "Action: <b>Wait</b> 3 days → <b>Send Email</b> E5",
     "Action: <b>Wait</b> 3 days → <b>Send Email</b> E6 → End"],
    "Day 2, 5, and 8 after opting in. Every email teaches something from the kit and none of them pitches."))
story.append(Spacer(1, 4))
story.append(email_card(
    "E4 · The two-handoff week (from the kit)",
    "{{contact.first_name}}, a quick lesson from the Starter Kit, no pitch:\n\n"
    "Delegation fails when founders hand off five things at once and check on all of them daily. It works when they hand off two things and check weekly.\n\n"
    "This week: pick your two biggest tasks (for most founders, email and scheduling). Run the handoff script on each. Check on decisions made, never on tasks done. That's it.\n\n"
    "That's week one of the plan. The kit has the other three weeks: [kit link]\n\n— Pareto Talent",
    "Send day 2, nurture only"))
story.append(email_card(
    "E5 · Why your last hire needed managing",
    "{{contact.first_name}}, if your last VA needed managing, the handoff probably looked like this: a task title, a quick walkthrough, and hope.\n\n"
    "What works instead is written in the kit: hand off the outcome, not the method. Hand over one decision with the task (refunds under $100, reschedules inside a week). Then ask one question on Friday: what did you decide?\n\n"
    "A person who makes decisions is an operator. A person who waits for instructions is a $10/hour puppet, and you built it.\n\n"
    "The script is on page one: [kit link]\n\n— Pareto Talent",
    "Send day 5, nurture only"))
story.append(email_card(
    "E6 · The math from your test, in months",
    "{{contact.first_name}}, the number from your test is workdays a month. At the $200 an hour a founder's time earns when it goes to growth, the assistant job quietly bills you thousands a month.\n\n"
    "Two questions decide when this becomes a hire: are you still at 15+ hours a week on ops, and did revenue clear $10k a month? When both are true, book the Matching Call and bring your kit. Until then, run the systems and retake the test each quarter.\n\n"
    "[Retake the test] · [Book a call]\n\n— Pareto Talent",
    "Send day 8, nurture only · optionally merge {{custom_values.quiz_hours_email}} style fields if mapped"))

# ---------------------------------------------------------------- WF4
story.append(P("8 · Workflow 4 — Booking (confirmation + reminder)", "h2"))
story.append(workflow(
    "<b>FP | Francisco Buiras | Booking Workflow</b>",
    ["Trigger: <b>Customer Booked Appointment</b>  + filters: <b>Calendar is [your Matching Call calendar]</b> and <b>Appointment Status is Confirmed</b>",
     "Action: <b>Add Tag</b> booked · move opportunity to stage Call Booked",
     "Action: <b>Send Email</b> E7 immediately (turn OFF the calendar's default confirmation so it doesn't double-send)",
     "Action: <b>Wait</b> → step type 'event/appointment', until 1 day before the appointment",
     "Action: <b>Send Email</b> E8",
     "Optional: a second wait until 1 hour before, SMS reminder if you have numbers"],
    "If someone no-shows: manually re-add them to stage Qualified and workflow 2 logic re-engages them. Mention it in the walkthrough as handled."))
story.append(Spacer(1, 4))
story.append(email_card(
    "E7 · Your Matching Call is booked",
    "{{contact.first_name}}, you're on the calendar: {{appointment.start_time}}.\n\n"
    "The call is 20 minutes, video. We walk your kit page by page, pressure-test your Week 1, and map your first month with a Right Hand.\n\n"
    "Bring two things: your test result and your kit with Week 1 filled in. That list is your first job description.\n\n"
    "Need a different time? Reschedule here: {{appointment.reschedule_link}}\n\n— Pareto Talent",
    "Send immediately after booking · if GHL's merge field names differ, pick them from the email builder's tag icon"))
story.append(email_card(
    "E8 · Tomorrow: the 20 minutes that buy your hours back",
    "{{contact.first_name}}, your Matching Call is tomorrow at {{appointment.start_time}}.\n\n"
    "Everything you need is already in your kit. Before the call, write your two Week 1 handoffs on page one. Founders who arrive with it filled in meet candidates in days, not weeks.\n\n"
    "On the call we plan your first month. Within 24 hours after, you meet 3+ hand-picked, AI-trained Right Hand candidates.\n\n"
    "See you tomorrow.\n\n[Reschedule]\n\n— Pareto Talent",
    "Send 24 hours before the appointment (event-based wait)"))

# ---------------------------------------------------------------- WF5
story.append(P("9 · Workflow 5 — Post-call (status + thank-you)", "h2"))
story.append(workflow(
    "<b>FP | Francisco Buiras | Post-call Thank-you</b>",
    ["Trigger: <b>Customer Booked Appointment</b>  + filters: <b>Calendar is [your Matching Call calendar]</b> and <b>Appointment Status is Confirmed</b>",
     "Action: <b>Wait</b> → step type 'event/appointment', until 2 hours AFTER the appointment",
     "Action: <b>Update Opportunity</b> → move to stage <b>Call Done</b>",
     "Action: <b>Send Email</b> E9 (the thank-you below)"],
    "For testing, set the wait to 5 minutes instead of 2 hours, book a slot, and watch the stage + email fire. "
    "No-show branch (optional): an If/Else on appointment status = no-show can send a quick rebook email instead."))

story.append(Spacer(1, 4))
story.append(email_card(
    "E9 · Thanks for joining — here's what happens now",
    "{{contact.first_name}}, thanks for joining today's call.\n\n"
    "You showed up with the kit filled in, we pressure-tested your Week 1 handoffs, and your shortlist is now with the matching team.\n\n"
    "What happens next: within 24 hours you meet 3+ hand-picked, AI-trained Right Hand candidates matched to your task list. "
    "No contracts and no payment unless you pick someone you want to work with.\n\n"
    "One ask while you wait: reply to this email with anything you didn't get to say on the call. "
    "The matching team reads every reply, and the small details are what make the match.\n\n"
    "Talk soon.\n\n— Pareto Talent",
    "Send 2 hours after the appointment · opportunity moves to Call Done at the same time"))

# ---------------------------------------------------------------- tests
story.append(P("10 · The end-to-end test (screenshot everything for L11 and L12)", "h2"))
story.append(P(
    "Run this once everything is built. Every step gets a screenshot into the two Drive folders: "
    "<b>FP_FranciscoBuiras_L11_Pipeline</b> and <b>FP_FranciscoBuiras_L12_Workflows</b>.", "body"))
story.append(Spacer(1, 4))
tests = [
    "Incognito, open the landing, complete the test, submit the form as QUALIFIED (revenue $10k–$50k, hours 15+, owner yes). Confirm redirect to qualified.html. Screenshot.",
    "Same, submit as NOT QUALIFIED (revenue under $10k). Confirm redirect to thank-you.html. Screenshot.",
    "Check the qualified inbox: kit email (E1) arrived with the PDF attached. Screenshot.",
    "Check the pipeline: opportunity created, correct stage. Screenshot.",
    "Check tags on the contact: qualified + kit-sent (or nurture + kit-sent). Screenshot.",
    "Book a call on the calendar. Confirm E7 arrives immediately and E8 arrives 24h before. Screenshot both.",
    "Screenshot each workflow's execution history showing steps fired in order (this is the 'tested end to end' proof for Part 7).",
    "Post-call check: book a test slot with the wait shortened to 5 minutes, confirm the stage moves to Call Done and E9 arrives.",
]
rows = [[P(f"<b>{i + 1}</b>", "cellB"), P(t, "cell")] for i, t in enumerate(tests)]
tw = table(rows, [18, CONTENT_W - 18 - 12], header=False)
tw.setStyle(TableStyle([
    ("TEXTCOLOR", (0, 0), (0, -1), BRAND),
    ("LEFTPADDING", (0, 0), (0, -1), 2),
]))
story.append(tw)
story.append(Spacer(1, 6))
story.append(boxed([
    P("<b>Build order (fastest path)</b>", "cellB"),
    Spacer(1, 3),
    P("Pipeline and tags first (5 min) → form with redirects (20 min) → test the two redirects → "
      "workflow 1 + E1 (20 min) → workflows 2, 3, 4 with E2–E8 (40 min) → the 7-step test above → "
      "screenshots to Drive. When the form embed works, send it to ZCode to wire the quiz answers in.", "cell"),
]))


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=32 * mm, bottomMargin=16 * mm,
        title="GHL Build Spec — Pareto Final Project",
        author="Francisco Buiras",
        subject="Pipeline, form, workflows, and emails to build the Pareto lead magnet funnel in GoHighLevel",
        creator="ZCode",
    )
    frame = Frame(MARGIN, 16 * mm, CONTENT_W, PAGE_H - 32 * mm - 16 * mm, id="m")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    doc.build(story)
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
