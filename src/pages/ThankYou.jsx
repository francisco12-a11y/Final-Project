import Nav from '../components/Nav.jsx'
import Footer from '../components/Footer.jsx'

export default function ThankYou() {
  return (
    <>
      <Nav right={<a className="nav-cta" href="index.html">Back to the audit</a>} />

      <header className="status-hero">
        <div className="container">
          <div className="badge-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <rect x="3" y="5" width="18" height="14" rx="2" stroke="#10b981" strokeWidth="2" />
              <path d="M3.5 7l8.5 6 8.5-6" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <span className="eyebrow">Check your inbox</span>
          <h1>Your Founder Delegation Audit is on its way</h1>
          <p className="section-sub">It should land within a minute or two. If you don't see it, check promotions and spam — then drag it to your primary inbox so nothing gets lost.</p>
          <div className="hero-cta-row" style={{ justifyContent: 'center' }}>
            <a className="btn btn-primary" href="#while-you-wait">What to do while it arrives</a>
          </div>
        </div>
      </header>

      <section className="section section-surface" style={{ paddingTop: 64 }}>
        <div className="container">
          <span className="eyebrow">Straight talk</span>
          <h2 className="section-title" style={{ fontSize: 'clamp(24px, 3.4vw, 34px)' }}>Here's why there's no booking link for you yet</h2>
          <p className="section-sub" style={{ marginBottom: 0 }}>
            The Right Hand Program is built for founders who are already scaling — real revenue,
            real ops load, hiring on your plate. Based on your answers, that's not where you are
            today. We'd rather tell you that than put you on a call that wastes 20 minutes of your
            life. The audit doesn't care what stage you're at: run it now, and you'll know exactly
            what to hand off the moment growth makes it necessary.
          </p>
        </div>
      </section>

      <section className="section" id="while-you-wait">
        <div className="container">
          <h2 className="section-title center">While you wait for the email</h2>
          <div className="check-grid">
            <div className="check-card">
              <div className="ic">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M4 6h16M4 12h16M4 18h10" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" />
                </svg>
              </div>
              <h3>Run the audit this week</h3>
              <p>Block 20 minutes, list the week honestly, and score every task. The number at the end — your recoverable hours — is the one most founders screenshot.</p>
            </div>
            <div className="check-card">
              <div className="ic">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z" fill="#10b981" />
                </svg>
              </div>
              <h3>Use the handoff script on one task</h3>
              <p>You don't need to hire anyone to delegate better. Pick your highest-scoring task and run the script with a current teammate — outcome, not method.</p>
            </div>
            <div className="check-card">
              <div className="ic">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <rect x="3" y="5" width="18" height="14" rx="2" stroke="#10b981" strokeWidth="2" />
                  <path d="M3.5 7l8.5 6 8.5-6" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <h3>Watch for three short emails</h3>
              <p>Over the next week we'll send the delegation rules that separate founders who scale from founders who stall. Every one has a one-click unsubscribe.</p>
            </div>
          </div>
          <div className="callout center">
            When the audit finds 10+ recoverable hours and revenue clears $10k/month, <b>the Matching Call will be here waiting.</b> Most founders get there faster than they think.
          </div>
        </div>
      </section>

      <Footer label="FP | Francisco Buiras | Thank You Page (Not Qualified)" />
    </>
  )
}
