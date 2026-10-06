import { useEffect, useState } from 'react'

// ⚠️ FICTIONAL DEMO TESTIMONIALS — invented for the bootcamp mockup.
// Swap with real client quotes (and real photos) before any real traffic.
// Avatar slots: drop files as avatar-t1.jpg … avatar-t10.jpg into
// public/site-assets/ — each slot falls back to initials until the photo exists.
// AI headshot prompts for each avatar are in project-docs/imagery-prompts.md.

const QUOTES = [
  {
    q: 'I got my mornings back. My Right Hand runs the inbox and the calendar before I even sit down, and I only touch what needs a decision.',
    name: 'Marcus Bell', role: 'Marketing agency owner', initials: 'MB', img: 'avatar-t1.jpg',
  },
  {
    q: 'Orders, tracking, returns — all of it disappeared from my plate in the first two weeks. I check one report now instead of forty messages.',
    name: 'Dana Whitfield', role: 'E-commerce founder', initials: 'DW', img: 'avatar-t2.jpg',
  },
  {
    q: 'Deals stopped dying in my inbox. Follow-ups go out the same day whether I remember them or not, and my close rate shows it.',
    name: 'Ruben Ortiz', role: 'Real estate investor', initials: 'RO', img: 'avatar-t3.jpg',
  },
  {
    q: 'I stopped being the operations department. My Right Hand built the runbooks I never wrote and runs the week from them.',
    name: 'Priya Nair', role: 'SaaS founder', initials: 'PN', img: 'avatar-t4.jpg',
  },
  {
    q: 'Intake calls happen without me now. Clients get an answer in minutes instead of days, and no case has walked to another firm since.',
    name: 'Alina Vega', role: 'Law firm owner', initials: 'AV', img: 'avatar-t5.jpg',
  },
  {
    q: 'Estimates go out the same day, every time. That alone paid for this before the first month ended.',
    name: 'Chris Decker', role: 'Remodeling company owner', initials: 'CD', img: 'avatar-t6.jpg',
  },
  {
    q: 'Launches stopped eating my quarter. The ops run on a checklist someone else owns, and I show up and teach.',
    name: 'Rachel Kim', role: 'Course creator', initials: 'RK', img: 'avatar-t7.jpg',
  },
  {
    q: 'I took my first week off in four years. Nothing broke. The Friday report told me everything I missed.',
    name: 'Diego Fuentes', role: 'Logistics founder', initials: 'DF', img: 'avatar-t8.jpg',
  },
  {
    q: "I stopped training my third assistant from zero. She arrived trained, and the handoff script did the rest — it's in the free kit, take it.",
    name: 'Nathan Brooks', role: 'Studio owner', initials: 'NB', img: 'avatar-t9.jpg',
  },
  {
    q: 'The test said sixteen hours. I believed maybe half of it. Six weeks in, the number is real and my calendar proves it.',
    name: 'Sofia Marino', role: 'Fitness studio chain owner', initials: 'SM', img: 'avatar-t10.jpg',
  },
]

function Avatar({ img, initials }) {
  const [failed, setFailed] = useState(false)
  if (failed) {
    return (
      <span className="tinit" aria-hidden="true">{initials}</span>
    )
  }
  return (
    <img
      className="tinit tinit-photo"
      src={`/Final-Project/site-assets/${img}`}
      alt=""
      onError={() => setFailed(true)}
      loading="lazy"
    />
  )
}

export default function Testimonials() {
  const [i, setI] = useState(0)
  const [paused, setPaused] = useState(false)

  useEffect(() => {
    if (paused) return
    const t = setInterval(() => setI((v) => (v + 1) % QUOTES.length), 5000)
    return () => clearInterval(t)
  }, [paused])

  const go = (n) => setI(((n % QUOTES.length) + QUOTES.length) % QUOTES.length)
  const q = QUOTES[i]

  return (
    <section className="section section-surface" id="founders">
      <div className="container">
        <div className="center">
          <span className="eyebrow">Wall of love</span>
          <h2 className="section-title">Founders who stopped being the assistant</h2>
        </div>
        <div
          className="tcarousel"
          onMouseEnter={() => setPaused(true)}
          onMouseLeave={() => setPaused(false)}
        >
          <button className="tarrow left" aria-label="Previous" onClick={() => go(i - 1)}>‹</button>
          <figure className="tcard">
            <div className="tstars" aria-hidden="true">★★★★★</div>
            <blockquote className="tquote">{q.q}</blockquote>
            <figcaption className="twho">
              <Avatar img={q.img} initials={q.initials} />
              <span>
                <b>{q.name}</b>
                <span className="trole">{q.role}</span>
              </span>
            </figcaption>
          </figure>
          <button className="tarrow right" aria-label="Next" onClick={() => go(i + 1)}>›</button>
          <div className="tdots">
            {QUOTES.map((_, n) => (
              <button
                key={n}
                aria-label={'Quote ' + (n + 1)}
                className={n === i ? 'tdot on' : 'tdot'}
                onClick={() => go(n)}
              />
            ))}
          </div>
        </div>
        <p className="tmeta center">
          What founders say after their first 30 days with a Right Hand · 93% of Pareto clients still matched at 12 months
        </p>
      </div>
    </section>
  )
}
