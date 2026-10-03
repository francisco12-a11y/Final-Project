import { useEffect } from 'react'
import Nav from '../components/Nav.jsx'
import Footer from '../components/Footer.jsx'

export default function Qualified() {
  // Inject the GHL embed script (it auto-resizes the booking iframe).
  useEffect(() => {
    const s = document.createElement('script')
    s.src = 'https://link.msgsndr.com/js/form_embed.js'
    s.type = 'text/javascript'
    document.body.appendChild(s)
    return () => { document.body.removeChild(s) }
  }, [])

  return (
    <>
      <Nav right={<span className="chip">Matching Call · Step 2 of 2</span>} />

      <header className="status-hero">
        <div className="container">
          <div className="badge-icon">
            <svg width="34" height="34" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M20 6L9 17l-5-5" stroke="#10b981" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <span className="eyebrow">You qualified</span>
          <h1>Founders like you get those hours back.<br />Let's meet your Right Hand.</h1>
          <p className="section-sub">Based on your answers, you're exactly who we built the Right Hand Program for. Book your Matching Call below. It's 20 minutes, and it's the last step before you meet your candidates.</p>
        </div>
      </header>

      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="check-grid" style={{ marginTop: 0 }}>
            <div className="check-card">
              <div className="ic">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z" fill="#10b981" />
                </svg>
              </div>
              <h3>What happens on the call</h3>
              <p>We walk through your audit together, pressure-test your delegation shortlist, and map the first 30 days of handoffs.</p>
            </div>
            <div className="check-card">
              <div className="ic">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <circle cx="12" cy="12" r="9" stroke="#10b981" strokeWidth="2.5" />
                  <path d="M12 7v5l3.5 2" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" />
                </svg>
              </div>
              <h3>Within 24 hours after</h3>
              <p>You meet 3+ hand-picked, AI-trained Right Hand candidates matched to your audit. No contracts, no payment, unless you pick someone you're excited about.</p>
            </div>
            <div className="check-card">
              <div className="ic">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 2l2.4 7.2H22l-6 4.6 2.3 7.2-6.3-4.5-6.3 4.5L8 13.8l-6-4.6h7.6z" stroke="#10b981" strokeWidth="2" strokeLinejoin="round" />
                </svg>
              </div>
              <h3>Backed by the guarantees</h3>
              <p>Freedom 40: reclaim 40 hours in your first 30 days or the next month is free. Plus lifetime replacement, no waiting period.</p>
            </div>
          </div>

          <div className="callout">
            <b>Bring your completed Founder Delegation Audit to the call.</b> Your shortlist, every task you scored 4 to 6, is your first job description. Founders who bring it finished usually match within days. <em>(Check your inbox if you haven't filled it in yet.)</em>
          </div>
        </div>
      </section>

      <section className="section section-surface" style={{ paddingTop: 56 }}>
        <div className="container">
          <div className="calendar-wrap">
            <h2>Pick your Matching Call time</h2>
            <p className="cal-sub">20 minutes · video call · brings your audit, leaves with your first 30-day handoff plan</p>
            <div className="iframe-holder">
              {/* FP | Francisco Buiras | Booking Calendar (real GHL embed) */}
              <iframe src="https://api.leadconnectorhq.com/widget/booking/U022LAXFG51gcLgvcOCt" allow="payment" style={{ width: '100%', border: 'none', overflow: 'hidden' }} scrolling="no" id="U022LAXFG51gcLgvcOCt_1791031787734" title="Book your Matching Call"></iframe>
            </div>
          </div>
        </div>
      </section>

      <Footer label="FP | Francisco Buiras | Booking Page (Qualified)" />
    </>
  )
}
