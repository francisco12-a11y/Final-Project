# Pareto Talent Bootcamp — Final Project

**FP | Francisco Buiras | Final Project**
Lead magnet + funnel for Pareto Talent's Right Hand Program. Deadline: **October 7, 2026** (end of day).

- **Lead magnet:** interactive **Delegation Quiz** on the landing page (instant recoverable-hours result, answers feed GHL) + *The Founder Delegation Audit* PDF delivered by email
- **Funnel tool:** GoHighLevel (form with conditional redirects) + GitHub Pages (public pages)
- **Branding:** Pareto Talent real branding — emerald `#10B981`, Jakarta Sans

## Repo structure

React (Vite, multi-page) → GitHub Pages via Actions. Branding is Pareto Talent's real one: their live logo, their `:root` design tokens (`#050a0e` dark, emerald `#10b981`), Plus Jakarta Sans + DM Sans.

| Path | What it is |
|------|------------|
| `index.html` + `src/pages/Landing.jsx` | Lead magnet landing page (L7) with persona-matched heroes (`?p=dan\|vanessa\|chris\|sofia`) and the GHL form slot |
| `qualified.html` + `src/pages/Qualified.jsx` | Booking page for qualified founders (L9), real GHL calendar embed |
| `thank-you.html` + `src/pages/ThankYou.jsx` | Thank-you page + nurture entry for unqualified leads (L10) |
| `src/styles.css` | Pareto's real design tokens (edit the `:root` block to rebrand everything) |
| `public/` | Real Pareto logo + favicon, and the audit PDF served at `/lead-magnet/` |
| `lead-magnet/` | Audit PDF source copy — regenerate with `python3 project-docs/build_audit_pdf.py`, then copy into `public/lead-magnet/` |
| `project-docs/` | Strategy, research, SOP, Business Map, ClickUp structure, email + ad copy, Loom script, PDF build scripts |
| `.github/workflows/deploy.yml` | Builds and deploys to Pages on every push to main |

## Deliverable tracker

### Strategy & planning
- [ ] L1 · Second Brain — *Fran*
- [ ] L2 · Research doc — competitor lead magnets + ICP research
- [ ] L3 · Business Map
- [ ] L4 · ClickUp board — *Fran builds from our structure*
- [ ] L5 · SOP

### Lead magnet & funnel
- [ ] L6 · Lead magnet (live) — audit PDF in public Drive folder
- [ ] L7 · Landing page — this repo, GitHub Pages
- [ ] L8 · Qualifying form — GHL, embedded on landing page
- [ ] L9 · Booking page (qualified) — this repo + real GHL calendar embed
- [ ] L10 · Thank you page (not qualified) — this repo

### Automation & creative
- [ ] L11 · Pipeline screenshots folder — *Fran (GHL), Drive*
- [ ] L12 · Workflow screenshots folder — *Fran (GHL), Drive*
- [ ] L13 · Ads folder — 5 ads, persona-matched
- [ ] L14 · Imagery folder
- [ ] L15 · Loom presentation — *Fran records (2 min)*

### Homework, Days 1–9
- [ ] H1–H9 — *Fran collects the links from his homework submissions*

## Submission checklist (from the guidelines)

- Every link opens in an incognito window, no login walls, no shortened links
- Form tested twice: qualified → booking page, unqualified → thank-you page
- Lead magnet arrives by email after opt-in
- PDF named `FP_FranciscoBuiras_ParetoBootcamp.pdf`, written in Google Docs, exported to PDF
- Everything named `FP | Francisco Buiras | Item Name`
- Submitted at bootcamp.paretotalent.com/finalproject before EOD Oct 7
