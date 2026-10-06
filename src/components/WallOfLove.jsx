import { useEffect, useState } from 'react'

// FABRICATED PLACEHOLDER QUOTES — invented for the demo funnel. Before this
// page runs real traffic or ads, swap these for real client quotes (Pareto's
// own wall-of-love is the source to mine) and delete this comment.
const QUOTES = [
  {
    q: 'I got my first free Saturday in two years. The weekly check-in alone killed about forty interruptions a week.',
    name: 'Martín D.',
    role: 'E-commerce founder, 12-person team',
  },
  {
    q: 'My inbox went from 200 unread to under 20 in nine days. I stopped being the mailroom of my own company.',
    name: 'Priya S.',
    role: 'Marketing agency owner',
  },
  {
    q: 'She rebuilt my calendar in week one. Sales calls live on Tuesdays and Thursdays now, and nothing moves them.',
    name: 'Tomás R.',
    role: 'B2B SaaS founder',
  },
  {
    q: "I didn't believe the 24-hour matching. Three candidates landed the next morning and one was a fit by Friday.",
    name: 'Daniel K.',
    role: 'Real estate investor',
  },
  {
    q: 'Six months of my own delegating never stuck. The handoff script stuck in one week.',
    name: 'Rachel M.',
    role: 'Business coach',
  },
  {
    q: "My first hire didn't work out. The replacement landed in four days with no waiting period. That guarantee is the whole product for me.",
    name: 'Ahmed B.',
    role: 'Dental clinic owner',
  },
  {
    q: "Four weeks in, invoicing, CRM updates and follow-ups are off my plate. That's 17 hours a week I got back.",
    name: 'Sofía G.',
    role: 'DTC brand founder',
  },
  {
    q: 'Our Right Hand runs the AI stack better than I do, and I built the stack. I stopped chasing the team in week one.',
    name: 'James W.',
    role: 'Agency owner, 25 people',
  },
  {
    q: 'The test said 15 hours. We got 12 back in month one and that was enough to end my night shifts.',
    name: 'Lucía F.',
    role: 'Consulting firm partner',
  },
  {
    q: 'The candidate ran my week from day three because someone wrote the process down. Onboarding took one call.',
    name: 'Nitin P.',
    role: 'Logistics startup founder',
  },
]

function initials(name) {
  return name.split(/\s+/).map((w) => w[0]).join('').replace('.', '').slice(0, 2).toUpperCase()
}

export default function WallOfLove() {
  const [i, setI] = useState(0)
  const [paused, setPaused] = useState(false)

  useEffect(() => {
    if (paused) return undefined
    const t = setInterval(() => setI((v) => (v + 1) % QUOTES.length), 6000)
    return () => clearInterval(t)
  }, [paused])

  const go = (d) => setI((v) => (v + d + QUOTES.length) % QUOTES.length)
  const quote = QUOTES[i]

  return (
    <div>
      <div
        className="quote-viewport"
        onMouseEnter={() => setPaused(true)}
        onMouseLeave={() => setPaused(false)}
      >
        <div className="quote-track" style={{ transform: `translateX(-${i * 100}%)` }}>
          {QUOTES.map((item) => (
            <div className="quote-slide" key={item.name}>
              <figure className="quote-card">
                <div className="quote-stars" aria-hidden="true">★★★★★</div>
                <blockquote className="quote-text">“{item.q}”</blockquote>
                <figcaption className="quote-person">
                  <span className="quote-avatar" aria-hidden="true">{initials(item.name)}</span>
                  <span>
                    <span className="n">{item.name}</span>
                    <br />
                    <span className="r">{item.role}</span>
                  </span>
                </figcaption>
              </figure>
            </div>
          ))}
        </div>
      </div>
      <div className="quote-nav">
        <button type="button" className="quote-arrow" aria-label="Previous story" onClick={() => go(-1)}>‹</button>
        <div className="quote-dots">
          {QUOTES.map((item, n) => (
            <button
              type="button"
              key={item.name}
              className={n === i ? 'quote-dot on' : 'quote-dot'}
              aria-label={`Go to story ${n + 1} of ${QUOTES.length}`}
              onClick={() => setI(n)}
            />
          ))}
        </div>
        <button type="button" className="quote-arrow" aria-label="Next story" onClick={() => go(1)}>›</button>
      </div>
      <p className="quote-count" aria-live="polite">
        {i + 1} / {QUOTES.length} · {quote.name}
      </p>
    </div>
  )
}
