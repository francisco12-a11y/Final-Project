import { useEffect, useState } from 'react'

// Real client quotes from Pareto's wall of love (Second Brain: 02-PEOPLE / icp-founder-personas).
const QUOTES = [
  {
    q: "I just can't even imagine not having my EA right now. I can't fathom a world where she's not a big part of it.",
    name: 'Joe Polish',
    role: 'Genius Network',
    initials: 'JP',
  },
  {
    q: "I've had three different executive assistants before, and I thought it was me… I was burning through them. They just weren't up to the task.",
    name: 'Eric Ritter',
    role: 'Matched to Agustina',
    initials: 'ER',
  },
  {
    q: 'My executive assistant runs point on critical projects and keeps track of so many endless opportunities.',
    name: 'Andrew Myers',
    role: 'Founder',
    initials: 'AM',
  },
  {
    q: "I won't even tell her to do it, and she'll just go and figure out how to do it.",
    name: 'Elina Panteleyeva',
    role: 'Founder',
    initials: 'EP',
  },
  {
    q: "A beast. She's on it. She's super efficient and a master task manager.",
    name: 'Marie Monet',
    role: 'Founder',
    initials: 'MM',
  },
  {
    q: 'Always punctual, reliable, and fully prepared… someone I can trust without hesitation.',
    name: 'Kevin Whatley',
    role: 'Founder',
    initials: 'KW',
  },
]

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
              <span className="tinit" aria-hidden="true">{q.initials}</span>
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
          Quotes from Pareto Talent's client wall of love · 93% of founders still with their Right Hand at 12 months
        </p>
      </div>
    </section>
  )
}
