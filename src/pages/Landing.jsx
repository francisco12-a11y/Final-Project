import { useEffect, useRef, useState } from 'react'
import Nav from '../components/Nav.jsx'
import Footer from '../components/Footer.jsx'
import Quiz from '../components/Quiz.jsx'
import Testimonials from '../components/Testimonials.jsx'
import TalentPool from '../components/TalentPool.jsx'
import GlobeDispatch from '../components/GlobeDispatch.jsx'

const HEROES = {
  dan: {
    h1: <>You're the bottleneck. Here's the <span className="accent">15 hours a week</span> to take back first</>,
    sub: "The test puts a number on the ops load pinning you down, then ranks exactly what to hand off first.",
  },
  vanessa: {
    h1: <>Burned by a VA? Audit what to hand off <span className="accent">before</span> you ever hire again</>,
    sub: "The test separates what to delegate from what to systemize, so your next hire starts clean and never needs babysitting.",
  },
  chris: {
    h1: <>If you took a week off, would the business stop? Find the <span className="accent">first process to cut loose</span></>,
    sub: "The test forces the first cut: which of the tasks running through your head gets documented once and handed off forever.",
  },
  sofia: {
    h1: <>You didn't leave your job to become your own assistant. Reclaim your <span className="accent">15 hours a week</span></>,
    sub: "The test puts a dollar figure on the $10/hour work crowding your calendar and shows what founder work it could fund.",
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

const GHL_FORM_BASE = 'https://api.leadconnectorhq.com/widget/form/RLyDEDAtpk2Voju4RLa0'

// Quiz answers ride to GoHighLevel as URL params on the form iframe.
// In the GHL form builder, set each field's URL parameter to the matching
// name below (q_email, q_crm, q_admin, q_support, q_hiring, q_who, q_total)
// so they pre-fill the custom fields from the GHL Build Spec (section 3).
function formUrl(result) {
  if (!result) return GHL_FORM_BASE
  const p = new URLSearchParams()
  result.hours.forEach((h) => p.set(h.id, String(h.h)))
  p.set('q_total', String(result.total))
  if (result.who) p.set('q_who', result.who)
  return `${GHL_FORM_BASE}?${p.toString()}`
}

export default function Landing() {
  const [hero, setHero] = useState(null)
  const [quizResult, setQuizResult] = useState(null)

  useEffect(() => {
    // Persona-matched heroes: ads link here with ?p=dan|vanessa|chris|sofia
    const p = new URLSearchParams(window.location.search).get('p')
    if (p && HEROES[p]) setHero(HEROES[p])
  }, [])

  // Routing lives in the GHL form (conditional On Submit redirect to
  // qualified.html / thank-you.html); the result pages break out of the
  // embed iframe themselves. No client-side submit listener here.

  // GHL form embed: built imperatively so React never touches the node
  // (form_embed.js relocates iframes; removing a relocated node crashes React)
  const formContainerRef = useRef(null)
  const formFrameRef = useRef(null)
  useEffect(() => {
    if (!formContainerRef.current) return
    const f = document.createElement('iframe')
    f.src = GHL_FORM_BASE
    f.style.cssText = 'width:100%;height:711px;border:none;border-radius:8px'
    f.id = 'inline-RLyDEDAtpk2Voju4RLa0'
    f.setAttribute('data-layout', "{'id':'INLINE'}")
    f.setAttribute('data-trigger-type', 'alwaysShow')
    f.setAttribute('data-trigger-value', '')
    f.setAttribute('data-activation-type', 'alwaysActivated')
    f.setAttribute('data-activation-value', '')
    f.setAttribute('data-deactivation-type', 'neverDeactivate')
    f.setAttribute('data-deactivation-value', '')
    f.setAttribute('data-form-name', 'FB-Qualifying')
    f.setAttribute('data-height', '711')
    f.setAttribute('data-layout-iframe-id', 'inline-RLyDEDAtpk2Voju4RLa0')
    f.setAttribute('data-form-id', 'RLyDEDAtpk2Voju4RLa0')
    f.setAttribute('data-cookie-consent', 'true')
    f.setAttribute('data-cookie-consent-provider', 'auto')
    f.title = 'FB-Qualifying'
    formContainerRef.current.appendChild(f)
    formFrameRef.current = f
    const s = document.createElement('script')
    s.src = 'https://link.msgsndr.com/js/form_embed.js'
    s.type = 'text/javascript'
    document.body.appendChild(s)
  }, [])

  // when the quiz completes, append its answers to the form URL (prefill)
  useEffect(() => {
    if (quizResult && formFrameRef.current) {
      formFrameRef.current.src = formUrl(quizResult)
    }
  }, [quizResult])

  return (
    <>
      <Nav cta="#get-audit" ctaLabel="Book a call" />

      {/* HERO */}
      <header className="hero">
        <div className="container hero-grid">
          <div>
            <span className="eyebrow">Free 2-minute test</span>
            <h1>
              {hero ? hero.h1 : <>You're the CEO and <span className="accent">your own assistant</span>. Hand off the assistant job.</>}
            </h1>
            <p className="hero-sub">
              {hero ? hero.sub
                : "Take the test and see how many hours a week you could get back from the assistant job, then get the Right Hand Starter Kit by email."}
            </p>
            <div className="hero-cta-row">
              <a className="btn btn-primary btn-lg" href="#quiz">Take the 2-minute quiz →</a>
            </div>
            <p className="hero-micro">Instant result · No email needed to see your number · Free kit delivered after</p>
            <div className="stat-chips">
              <span className="chip">10–15 hrs/week recoverable</span>
              <span className="chip">4.3x ROI on a Right Hand</span>
              <span className="chip">3 matches within 24 hours</span>
            </div>
          </div>
          <div>
            <AuditPreview />
            <div className="trust-row under-card">
              <span className="avatar-stack" aria-hidden="true">
                <img src="/Final-Project/site-assets/avatar-1.svg" alt="" />
                <img src="/Final-Project/site-assets/avatar-2.svg" alt="" />
                <img src="/Final-Project/site-assets/avatar-3.svg" alt="" />
                <span className="avatar-more">+</span>
              </span>
              <span className="stars">★★★★★</span>
              <span className="txt"><b>4.9</b> · Trusted by 100+ founders</span>
            </div>
          </div>
        </div>
      </header>

      {/* SOCIAL PROOF CAROUSEL */}
      <Testimonials />

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
          <span className="eyebrow">The kit</span>
          <h2 className="section-title">The test gives you the number. The kit gives you the systems.</h2>
          <p className="section-sub">Delivered by email the moment you opt in: four tools our operators start with, written to hand off on day one, plus a 30-day plan built from your test result.</p>
          <div className="steps-grid" id="inside">
            <div className="step-card">
              <div className="step-num">1</div>
              <h3>The 30-Day Handoff Plan</h3>
              <p>Week by week: what to hand off, when, and the words to use. Your Week 1 comes straight from your test result.</p>
            </div>
            <div className="step-card">
              <div className="step-num">2</div>
              <h3>The handoff script</h3>
              <p>The conversation that makes delegation stick: the outcome, one delegated decision, and the Friday question.</p>
            </div>
            <div className="step-card">
              <div className="step-num">3</div>
              <h3>Inbox and calendar systems</h3>
              <p>The rules our operators run in week one: response targets, meeting defaults, and the two blocks that never move.</p>
            </div>
            <div className="step-card">
              <div className="step-num">4</div>
              <h3>The weekly check-in agenda</h3>
              <p>Thirty minutes on decisions made, never tasks done. The meeting that replaces all the interruptions.</p>
            </div>
          </div>
          <div className="kit-preview">
            <img src="/Final-Project/site-assets/kit-cover.png" alt="The Right Hand Starter Kit — cover page" loading="lazy" />
            <div>
              <h3>What lands in your inbox</h3>
              <ul>
                <li>The 30-day handoff plan, with your Week 1 pre-filled from your test result</li>
                <li>The handoff script and the three rules that make it stick</li>
                <li>Inbox, calendar, follow-up, and check-in systems, written to run</li>
                <li>One page to bring to your Matching Call: your first job description</li>
              </ul>
              <a className="btn btn-primary kit-cta" href="#get-audit">Get the kit by email →</a>
            </div>
          </div>
        </div>
      </section>

      {/* WHO IT'S FOR */}
      <section className="section section-surface" id="personas">
        <div className="container">
          <span className="eyebrow">Who this is for</span>
          <h2 className="section-title">Built for founders who are the ceiling of their own company</h2>
          <div className="persona-grid">
            <div className="persona-card">
              <img className="portrait portrait-43" src="/Final-Project/site-assets/dan.jpg" alt="Founder buried in tabs at his desk, late at night" loading="lazy" />
              <span className="tag" style={{ marginTop: 14 }}>The Drowning Operator</span>
              <p className="q">"I didn't build a company to become its assistant."</p>
              <p className="angle">Revenue grew, ops grew with it, and you became the ceiling. The test shows you which hours to buy back first and what keeping them costs.</p>
            </div>
            <div className="persona-card">
              <img className="portrait portrait-43" src="/Final-Project/site-assets/vanessa.jpg" alt="Skeptical founder reviewing a stack of VA resumes" loading="lazy" />
              <span className="tag" style={{ marginTop: 14 }}>Burned by a VA</span>
              <p className="q">"I'm not paying someone to need managed."</p>
              <p className="angle">The first VA failed because nobody vetted or trained her. The test separates what to hand off from what to systemize, so your next hire starts clean.</p>
            </div>
            <div className="persona-card">
              <img className="portrait portrait-43" src="/Final-Project/site-assets/chris.jpg" alt="Founder surrounded by sticky notes and boxes" loading="lazy" />
              <span className="tag" style={{ marginTop: 14 }}>Chaos at Scale</span>
              <p className="q">"It's faster if I do it myself."</p>
              <p className="angle">Everything runs through you because no process exists outside your head. The test forces the first cut: what to document once and hand off forever.</p>
            </div>
            <div className="persona-card">
              <img className="portrait portrait-43" src="/Final-Project/site-assets/sofia.jpg" alt="Founder closing her laptop early, relieved" loading="lazy" />
              <span className="tag" style={{ marginTop: 14 }}>Solo Until Now</span>
              <p className="q">"I didn't leave my job to become my own assistant."</p>
              <p className="angle">You protected margin by doing everything. Now growth stalled and the calendar is full of $10/hour work. The test puts a dollar figure on that trade.</p>
            </div>
          </div>
        </div>
      </section>

      {/* WHAT HAPPENS NEXT */}
      <section className="section">
        <div className="container">
          <span className="eyebrow">After you opt in</span>
          <h2 className="section-title">The test is step one. Step two is a call.</h2>
          <p className="section-sub">After you grab the worksheet, we ask six quick questions. Your answers pick which of two paths you get.</p>
          <div className="paths-grid">
            <div className="path-card win">
              <h3><span className="path-pill green">Scaling now</span> Book a Matching Call</h3>
              <p>If the test finds 10+ recoverable hours and your answers say you're scaling (real revenue, real ops load, hiring on your plate), we invite you to book a <b>Matching Call</b> with us.</p>
              <ul>
                <li>Bring your kit; your Week 1 list is your first job description</li>
                <li>Meet 3+ hand-picked, AI-trained Right Hand candidates within 24 hours</li>
                <li>Backed by the Freedom 40 guarantee and lifetime replacement</li>
              </ul>
            </div>
            <div className="path-card">
              <h3><span className="path-pill gray">Early days</span> Keep the kit anyway</h3>
              <p>If the timing isn't right (pre-revenue, still validating, ops load too light), we tell you straight instead of pitching you.</p>
              <ul>
                <li>The kit is yours either way, no strings</li>
                <li>You'll get a short email series on delegation that pays off when you are ready</li>
                <li>One click to unsubscribe, zero hard feelings</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* THE PROGRAM */}
      <section className="section section-surface rh-section">
        <GlobeDispatch
          className="rh-bg"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', aspectRatio: 'auto' }}
          cities={24}
          tempo={0.075}
          lift={0.24}
          size={460}
          distance={14}
          offsetX={0.04}
          offsetY={-0.08}
          globe={{ spin: 12, tilt: -22, roll: 17 }}
          camera={{ yaw: -22, pitch: 2, roll: 12 }}
        />
        <div className="container">
          <span className="eyebrow">The next-step offer</span>
          <h2 className="section-title">What a Right Hand actually is</h2>
          <p className="section-sub">Freelance marketplaces hand you a list. We hand-pick full-time operators in Latin America, fluent in English, and train them 40+ hours on the AI stack before you ever meet them. Then we match them to your task list within 24 hours, with guarantees in writing.</p>
          <p className="rh-caption">
            Matched in Buenos Aires. Working US hours, in your tools. One hire covers the map.
          </p>
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
          <div style={{ marginTop: 44 }}>
            <img className="portrait portrait-219" src="/Final-Project/site-assets/va-bench.jpg" alt="A bench of Pareto Talent Right Hand operators at work" loading="lazy" />
          </div>
        </div>
      </section>

      {/* FOUNDERS */}
      <section className="section" id="founders">
        <div className="container">
          <div className="center">
            <span className="eyebrow">The founders</span>
            <h2 className="section-title">Kasim hired an assistant in 2018. That assistant became his CTO, then his business partner.</h2>
            <p className="section-sub">Ivan Bunin answered Kasim Aslam's assistant job ad. Pareto Talent is the company they built from it.</p>
          </div>
          <img
            className="founders-photo"
            src="/Final-Project/site-assets/founders.jpg"
            alt="Kasim Aslam and Ivan Bunin, founders of Pareto Talent"
            loading="lazy"
          />
          <div className="founders-note">
            <p>
              The agency was Solutions 8, a Google Ads shop with six employees when Ivan joined and 80
              when Kasim sold it for eight figures. Kasim never ran a Google Ads campaign himself; his
              hires ran the ads and the operations. Ivan ran the diligence on the sale, then co-founded
              Pareto with him.
            </p>
            <div className="founders-names">
              <span><b>Kasim Aslam</b> · Co-founder</span>
              <span><b>Ivan Bunin</b> · Co-founder</span>
            </div>
          </div>
        </div>
      </section>

      {/* THE TALENT POOL */}
      <TalentPool />

      {/* QUIZ */}
      <section className="section section-surface" id="quiz">
        <div className="container">
          <div className="center">
            <span className="eyebrow">The 2-minute test</span>
            <h2 className="section-title">Test how much time you can get back</h2>
            <p className="section-sub">Answer six questions about your week. You'll see your recoverable hours on the spot, and your answers pre-fill the form so the next step routes you honestly.</p>
          </div>
          <Quiz onDone={setQuizResult} />
        </div>
      </section>

      {/* FORM */}
      <section className="section" id="get-audit">
        <div className="container">
          <div className="center">
            <span className="eyebrow">Book a call</span>
            <h2 className="section-title">First, a quick check so the call is worth your time</h2>
            <p className="section-sub">Six questions qualify you: founders we can help get the calendar on the next screen, and the Right Hand Starter Kit lands in your inbox either way.</p>
          </div>
          <div className="form-box">
            {quizResult && (
              <div className="quiz-summary" id="quiz-summary">
                <span>Your test: <b>{quizResult.total} hours a week</b> recoverable</span>
                {quizResult.whoText && <span>· today: <b>{quizResult.whoText.toLowerCase()}</b></span>}
                <span>· your answers pass to GoHighLevel with this form</span>
              </div>
            )}
            {/* GHL FORM EMBED — FB-Qualifying. Mounted imperatively (React never
                reconciles this node: GHL's form_embed.js relocates iframes in the
                DOM and crashes React on re-render). Styled in the GHL builder. */}
            <div ref={formContainerRef} />
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
              <summary>Is the kit free?</summary>
              <p>Yes. It's a pack of systems and scripts: download it, use it, keep it. The only thing we ask is six quick questions so the next step we show you is the honest one.</p>
            </details>
            <details>
              <summary>Why do you ask qualifying questions for a free worksheet?</summary>
              <p>Because a Matching Call is a real program with real cost, and it only makes sense if you're scaling. Your answers route you: ready founders get invited to book a call, everyone else still gets the kit and the email series.</p>
            </details>
            <details>
              <summary>What exactly is a Right Hand?</summary>
              <p>A full-time, hand-picked and AI-trained operator who owns your ops (inbox, calendar, CRM, follow-ups, reporting) as a person, not a task list. We match 3+ candidates to your task list within 24 hours.</p>
            </details>
            <details>
              <summary>What if I've been burned by a VA before?</summary>
              <p>That's the most common story we hear. The difference is vetting and training: we hand-pick the top 1% and train them 40+ hours on the AI stack before you ever meet them, and the lifetime replacement guarantee means a bad match never sticks.</p>
            </details>
            <details>
              <summary>What if the test finds I'm not ready to delegate?</summary>
              <p>Then you learned that in two minutes instead of losing a year to it. Keep the kit, retake the test each quarter, and read the delegation email series. It'll be here when the timing is right.</p>
            </details>
          </div>
        </div>
      </section>

      <Footer label="FP | Francisco Buiras | Lead Magnet Landing Page" />
    </>
  )
}
