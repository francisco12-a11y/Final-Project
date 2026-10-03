import { useEffect, useState } from 'react'
import Nav from '../components/Nav.jsx'
import Footer from '../components/Footer.jsx'

const HEROES = {
  dan: {
    h1: <>You're the bottleneck. Here's the <span className="accent">15 hours a week</span> to take back first</>,
    sub: "The Founder Delegation Audit puts a number on the ops load pinning you down, then ranks exactly what to hand off first.",
  },
  vanessa: {
    h1: <>Burned by a VA? Audit what to hand off <span className="accent">before</span> you ever hire again</>,
    sub: "The Founder Delegation Audit separates what to delegate from what to systemize, so your next hire starts clean and never needs babysitting.",
  },
  chris: {
    h1: <>If you took a week off, would the business stop? Find the <span className="accent">first process to cut loose</span></>,
    sub: "The Founder Delegation Audit forces the first cut: which of the tasks running through your head gets documented once and handed off forever.",
  },
  sofia: {
    h1: <>You didn't leave your job to become your own assistant. Reclaim your <span className="accent">15 hours a week</span></>,
    sub: "The Founder Delegation Audit puts a dollar figure on the $10/hour work crowding your calendar and shows what founder work it could fund.",
  },
}

function AuditPreview() {
  return (
    <div className="audit-card" aria-hidden="true">
      <h3>Your delegation shortlist</h3>
      <div className="audit-row"><span className="audit-score hot">6</span><span>Inbox triage &amp; scheduling</span><span className="h">9 hrs/wk</span></div>
      <div className="audit-row"><span className="audit-score hot">6</span><span>CRM updates &amp; follow-ups</span><span className="h">4 hrs/wk</span></div>
      <div className="audit-row"><span className="audit-score hot">5</span><span>Invoicing &amp; data entry</span><span className="h">3 hrs/wk</span></div>
      <div className="audit-row"><span className="audit-score">3</span><span>Weekly report building</span><span className="h">systemize</span></div>
      <div className="audit-row"><span className="audit-score">0</span><span>Sales calls &amp; product</span><span className="h">keep</span></div>
      <div className="audit-total"><span>Your recoverable week</span><span className="n">16 hrs</span></div>
    </div>
  )
}

export default function Landing() {
  const [hero, setHero] = useState(null)

  useEffect(() => {
    // Persona-matched heroes: ads link here with ?p=dan|vanessa|chris|sofia
    const p = new URLSearchParams(window.location.search).get('p')
    if (p && HEROES[p]) setHero(HEROES[p])
  }, [])

  return (
    <>
      <Nav />

      {/* HERO */}
      <header className="hero">
        <div className="container hero-grid">
          <div>
            <div className="trust-row">
              <span className="stars">★★★★★</span>
              <span className="txt"><b>4.9</b> · Trusted by 100+ founders</span>
            </div>
            <span className="eyebrow">Free 20-minute worksheet</span>
            <h1>
              {hero ? hero.h1 : <>Find the <span className="accent">15 hours a week</span> you're doing a $10/hour job</>}
            </h1>
            <p className="hero-sub">
              {hero ? hero.sub
                : "The Founder Delegation Audit scores every task on your plate, ranks what to hand off first, and hands you the script for the handoff conversation you've been avoiding."}
            </p>
            <div className="hero-cta-row">
              <a className="btn btn-primary btn-lg" href="#get-audit">Get the Free Audit →</a>
            </div>
            <p className="hero-micro">Instant email delivery · No credit card · 20 minutes to finish</p>
            <div className="stat-chips">
              <span className="chip">10–15 hrs/week recoverable</span>
              <span className="chip">4.3x ROI on a Right Hand</span>
              <span className="chip">3 matches within 24 hours</span>
            </div>
          </div>
          <AuditPreview />
        </div>
      </header>

      {/* PROBLEM */}
      <section className="section section-surface">
        <div className="container">
          <span className="eyebrow">The bottleneck</span>
          <h2 className="section-title">You don't have a people problem.<br />You have a delegation problem.</h2>
          <p className="section-sub">The founders we match said these three things before they found us. Sound familiar?</p>
          <div className="pain-grid">
            <div className="pain-card">
              <p className="q">"I'm doing $10/hour work in a $100/hour job. I'm the bottleneck of my own company."</p>
              <p className="who">The Drowning Operator</p>
            </div>
            <div className="pain-card">
              <p className="q">"I spent more time training my VA than I got back. Never again… unless someone else did the vetting."</p>
              <p className="who">The Burned-by-a-VA Founder</p>
            </div>
            <div className="pain-card">
              <p className="q">"Everything lives in my head and my DMs. If I take a week off, the business stops."</p>
              <p className="who">The Chaos-at-Scale Founder</p>
            </div>
          </div>
        </div>
      </section>

      {/* WHAT'S INSIDE */}
      <section className="section" id="how">
        <div className="container">
          <span className="eyebrow">The audit</span>
          <h2 className="section-title">Three steps and 20 minutes to your recoverable week</h2>
          <p className="section-sub">Do it honestly. The math is uncomfortable on purpose.</p>
          <div className="steps-grid">
            <div className="step-card">
              <div className="step-num">1</div>
              <h3>Log</h3>
              <p>List every recurring task you did this week. We give you the usual suspects: inbox, calendar, CRM, invoicing, follow-ups, reports, data entry.</p>
            </div>
            <div className="step-card">
              <div className="step-num">2</div>
              <h3>Score</h3>
              <p>Rate each task on two questions: what would it cost to hire someone to do it, and does it need <em>you</em> or does it need <em>doing</em>?</p>
            </div>
            <div className="step-card">
              <div className="step-num">3</div>
              <h3>Rank &amp; hand off</h3>
              <p>Get your ranked delegation shortlist, your recoverable-hours number, and the script for your first handoff conversation.</p>
            </div>
          </div>
          <div className="deliverables" id="inside">
            <h3>What you walk away with</h3>
            <ul>
              <li><b>Your Delegation Shortlist</b>: every task scored 4–6, ranked and ready to hand off</li>
              <li><b>Your recoverable week</b>: the exact hours you're losing to assistant-level work and what they're worth per year</li>
              <li><b>The first handoff script</b>: the conversation that makes delegation stick (outcome, not method, plus the decision you delegate with it)</li>
              <li><b>Your first job description</b>: if the audit finds 10+ hours, your shortlist is the spec for hiring a Right Hand</li>
            </ul>
          </div>
        </div>
      </section>

      {/* WHO IT'S FOR */}
      <section className="section section-surface">
        <div className="container">
          <span className="eyebrow">Who this is for</span>
          <h2 className="section-title">Built for founders who are the ceiling of their own company</h2>
          <div className="persona-grid">
            <div className="persona-card">
              <span className="tag">The Drowning Operator</span>
              <p className="q">"I didn't build a company to become its assistant."</p>
              <p className="angle">Revenue grew, ops grew with it, and you became the ceiling. The audit shows you which hours to buy back first and what keeping them costs.</p>
            </div>
            <div className="persona-card">
              <span className="tag">Burned by a VA</span>
              <p className="q">"I'm not paying someone to need managed."</p>
              <p className="angle">The first VA failed because nobody vetted or trained her. The audit separates what to hand off from what to systemize, so your next hire starts clean.</p>
            </div>
            <div className="persona-card">
              <span className="tag">Chaos at Scale</span>
              <p className="q">"It's faster if I do it myself."</p>
              <p className="angle">Everything runs through you because no process exists outside your head. The audit's scoring forces the first cut: what to document once and hand off forever.</p>
            </div>
            <div className="persona-card">
              <span className="tag">Solo Until Now</span>
              <p className="q">"I didn't leave my job to become my own assistant."</p>
              <p className="angle">You protected margin by doing everything. Now growth stalled and the calendar is full of $10/hour work. The audit puts a dollar figure on that trade.</p>
            </div>
          </div>
        </div>
      </section>

      {/* WHAT HAPPENS NEXT */}
      <section className="section">
        <div className="container">
          <span className="eyebrow">After you opt in</span>
          <h2 className="section-title">The audit is step one. Here's step two.</h2>
          <p className="section-sub">After you grab the worksheet, we ask six quick questions. Your answers pick which of two paths you get.</p>
          <div className="paths-grid">
            <div className="path-card win">
              <h3><span className="path-pill green">Scaling now</span> Book a Matching Call</h3>
              <p>If the audit finds 10+ recoverable hours and your answers say you're scaling (real revenue, real ops load, hiring on your plate), we invite you to book a <b>Matching Call</b> with us.</p>
              <ul>
                <li>Bring your completed audit; your shortlist is your first job description</li>
                <li>Meet 3+ hand-picked, AI-trained Right Hand candidates within 24 hours</li>
                <li>Backed by the Freedom 40 guarantee and lifetime replacement</li>
              </ul>
            </div>
            <div className="path-card">
              <h3><span className="path-pill gray">Early days</span> Keep the audit anyway</h3>
              <p>If the timing isn't right (pre-revenue, still validating, ops load too light), we tell you straight instead of pitching you.</p>
              <ul>
                <li>The audit is yours either way, no strings</li>
                <li>You'll get a short email series on delegation that pays off when you are ready</li>
                <li>One click to unsubscribe, zero hard feelings</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* THE PROGRAM */}
      <section className="section section-surface">
        <div className="container">
          <span className="eyebrow">The next-step offer</span>
          <h2 className="section-title">What a Right Hand actually is</h2>
          <p className="section-sub">Freelance marketplaces hand you a list. We hand-pick full-time operators in Latin America, fluent in English, and train them 40+ hours on the AI stack before you ever meet them. Then we match them to your audit within 24 hours, with guarantees in writing.</p>
          <div className="guarantee-grid">
            <div className="guarantee-card">
              <h3>Freedom 40</h3>
              <p>Follow the onboarding plan, and if you don't reclaim 40 hours in your first 30 days, the next month is on us.</p>
            </div>
            <div className="guarantee-card">
              <h3>Matching Guarantee</h3>
              <p>3+ hand-picked candidates within 24 hours. No contracts, no payment, unless you pick someone you're excited about.</p>
            </div>
            <div className="guarantee-card">
              <h3>Lifetime Replacement</h3>
              <p>If your Right Hand ever stops performing, you get a free replacement with no waiting period, for as long as you work together.</p>
            </div>
          </div>
        </div>
      </section>

      {/* FORM */}
      <section className="section" id="get-audit">
        <div className="container">
          <div className="center">
            <span className="eyebrow">Get the audit</span>
            <h2 className="section-title">Find your 15 hours</h2>
            <p className="section-sub">Answer the questions below and the Founder Delegation Audit lands in your inbox instantly.</p>
          </div>
          <div className="form-box">
            {/* ============================================================
                GHL FORM EMBED — paste the GoHighLevel qualifying form embed
                code on the next line, replacing the placeholder div below.
                Form must redirect on submit:
                  qualified   ->  https://francisco12-a11y.github.io/pareto-final-project/qualified.html
                  unqualified ->  https://francisco12-a11y.github.io/pareto-final-project/thank-you.html
                ============================================================ */}
            <div id="ghl-form-slot" className="form-slot-note">
              [ GHL qualifying form embeds here: pending form build in GoHighLevel ]
            </div>
            {/* ==================== end GHL form embed ==================== */}
            <p className="form-trust">We ask a few qualifying questions so we don't waste your time on a pitch that isn't for you. Your answers are never sold or shared.</p>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="section section-surface" id="faq">
        <div className="container">
          <h2 className="section-title center">Questions founders ask</h2>
          <div className="faq">
            <details>
              <summary>Is the audit free?</summary>
              <p>Yes. It's a worksheet: download it, fill it in, keep it. The only thing we ask is six quick questions so the next step we show you is the honest one.</p>
            </details>
            <details>
              <summary>Why do you ask qualifying questions for a free worksheet?</summary>
              <p>Because a Matching Call is a real program with real cost, and it only makes sense if you're scaling. Your answers route you: ready founders get invited to book a call, everyone else still gets the audit and the email series.</p>
            </details>
            <details>
              <summary>What exactly is a Right Hand?</summary>
              <p>A full-time, hand-picked and AI-trained operator who owns your ops (inbox, calendar, CRM, follow-ups, reporting) as a person, not a task list. We match 3+ candidates to your audit within 24 hours.</p>
            </details>
            <details>
              <summary>What if I've been burned by a VA before?</summary>
              <p>That's the most common story we hear. The difference is vetting and training: we hand-pick the top 1% and train them 40+ hours on the AI stack before you ever meet them, and the lifetime replacement guarantee means a bad match never sticks.</p>
            </details>
            <details>
              <summary>What if the audit finds I'm not ready to delegate?</summary>
              <p>Then you learned that in 20 minutes instead of losing a year to it. Keep the worksheet, run it again each quarter, and read the delegation email series. It'll be here when the timing is right.</p>
            </details>
          </div>
        </div>
      </section>

      <Footer label="FP | Francisco Buiras | Lead Magnet Landing Page" />
    </>
  )
}
