import { useState } from 'react'

// Quiz answers feed the GHL funnel: on completion, onDone() exposes the
// answers; Landing renders them above the form embed. When the real GHL form
// goes in, map URL params -> custom fields (e.g. ?q_email=6&q_crm=5&q_total=12)
// so workflows can tag and route on every answer.

const QUESTIONS = [
  {
    id: 'q_email',
    label: 'Email & scheduling',
    q: 'How many hours a week do you spend on email and scheduling?',
    help: 'Reading, replying, booking meetings, chasing confirmations',
    options: [
      { t: 'Under 2 hrs', h: 0 },
      { t: '3–5 hrs', h: 3 },
      { t: '6–10 hrs', h: 6 },
      { t: '11+ hrs', h: 9 },
    ],
  },
  {
    id: 'q_crm',
    label: 'CRM & follow-ups',
    q: 'How many hours a week do you spend on your CRM and follow-ups?',
    help: 'Updating deals, chasing leads, checking in with customers',
    options: [
      { t: 'Under 2 hrs', h: 0 },
      { t: '2–4 hrs', h: 2 },
      { t: '5–8 hrs', h: 5 },
      { t: '9+ hrs', h: 7 },
    ],
  },
  {
    id: 'q_admin',
    label: 'Admin & reports',
    q: 'How much time goes to invoices, data entry and reports?',
    help: 'Billing, spreadsheets, copy-pasting between tools',
    options: [
      { t: 'Under 2 hrs', h: 0 },
      { t: '2–4 hrs', h: 2 },
      { t: '5–8 hrs', h: 5 },
      { t: '9+ hrs', h: 7 },
    ],
  },
  {
    id: 'q_support',
    label: 'Customer support',
    q: 'How much time do you lose to customer support every week?',
    help: 'Tickets, refunds, tracking numbers, "quick questions"',
    options: [
      { t: 'Under 2 hrs', h: 0 },
      { t: '3–5 hrs', h: 3 },
      { t: '6–10 hrs', h: 6 },
      { t: '11+ hrs', h: 8 },
    ],
  },
  {
    id: 'q_hiring',
    label: 'Hiring & team admin',
    q: 'How many hours a week go to hiring and team admin?',
    help: 'Screening candidates, onboarding, timesheets, payroll prep',
    options: [
      { t: 'Under 2 hrs', h: 0 },
      { t: '2–4 hrs', h: 2 },
      { t: '5–8 hrs', h: 5 },
      { t: '9+ hrs', h: 6 },
    ],
  },
  {
    id: 'q_who',
    label: 'Who runs these tasks today?',
    q: 'Who does these tasks today?',
    help: 'Be honest, this routes your next step',
    options: [
      { t: 'Me, during work hours', ghl: 'me-work-hours' },
      { t: 'Me, at night and on weekends', ghl: 'me-nights-weekends' },
      { t: 'Partly delegated, partly me', ghl: 'partly-delegated' },
      { t: 'An assistant who needs managing', ghl: 'assistant-needs-managing' },
    ],
  },
]

function tierLine(total) {
  if (total === 0) return 'Your week is already lean. The kit\'s systems will keep it that way.'
  if (total <= 5) return 'That is a half-day every week back in your hands.'
  if (total <= 10) return 'That is a full workday every week, spent on assistant work.'
  return 'That is a whole extra workweek every month, done by you.'
}

export default function Quiz({ onDone }) {
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState({})
  const done = step >= QUESTIONS.length

  function pick(qIndex, optIndex) {
    const q = QUESTIONS[qIndex]
    const next = { ...answers, [q.id]: optIndex }
    setAnswers(next)
    if (qIndex + 1 >= QUESTIONS.length) {
      const total = QUESTIONS.reduce((sum, question) => {
        const a = next[question.id]
        return sum + (a === undefined ? 0 : (question.options[a].h ?? 0))
      }, 0)
      const whoOpt = next.q_who !== undefined ? QUESTIONS[5].options[next.q_who] : null
      onDone({
        total,
        hours: QUESTIONS.slice(0, 5).map((question) => ({
          id: question.id,
          label: question.label,
          h: next[question.id] !== undefined ? question.options[next[question.id]].h : 0,
        })),
        who: whoOpt ? whoOpt.ghl : null,
        whoText: whoOpt ? whoOpt.t : null,
        ts: new Date().toISOString(),
      })
    }
    setStep(qIndex + 1)
  }

  const progress = Math.min(step, QUESTIONS.length)
  const total = QUESTIONS.reduce((sum, question) => {
    const a = answers[question.id]
    return sum + (a === undefined ? 0 : (question.options[a].h ?? 0))
  }, 0)

  return (
    <div className="quiz">
      <div className="quiz-progress" aria-hidden="true">
        <span style={{ width: `${(progress / QUESTIONS.length) * 100}%` }} />
      </div>

      {!done ? (
        <div className="quiz-q" key={step}>
          <p className="quiz-step">Question {progress + 1} of {QUESTIONS.length}</p>
          <h3 className="quiz-label">{QUESTIONS[step].q}</h3>
          <p className="quiz-help">{QUESTIONS[step].help}</p>
          <div className="quiz-options">
            {QUESTIONS[step].options.map((opt, i) => (
              <button
                key={opt.t}
                type="button"
                className={answers[QUESTIONS[step].id] === i ? 'quiz-opt picked' : 'quiz-opt'}
                onClick={() => pick(step, i)}
              >
                {opt.t}
              </button>
            ))}
          </div>
          {step > 0 && (
            <button type="button" className="quiz-back" onClick={() => setStep(step - 1)}>← Back</button>
          )}
        </div>
      ) : (
        <div className="quiz-result">
          <p className="quiz-step">Your test result</p>
          <div className="quiz-number">
            <span className="n">{total}</span>
            <span className="u">hours a week<br />can come back to you</span>
          </div>
          <p className="quiz-tier">{tierLine(total)}</p>
          <ul className="quiz-breakdown">
            {QUESTIONS.slice(0, 5).map((question) => {
              const a = answers[question.id]
              const h = a === undefined ? 0 : question.options[a].h
              return (
                <li key={question.id}>
                  <span>{question.label}</span>
                  <b>{h} hrs</b>
                </li>
              )
            })}
          </ul>
          {total > 0 && (
            <>
              <p className="quiz-math">
                That is about <b>{Math.max(1, Math.round((total * 4.3) / 8))} full workdays</b> every month spent on assistant work.
              </p>
              <p className="quiz-math">
                Pareto prices a founder's hour at $200 when it goes to sales, product, and growth.
                At {total} hours a week, that is <b>about ${Math.round(total * 4.3 * 200).toLocaleString('en-US')} a month</b> of CEO work that never happens.
              </p>
              <p className="quiz-week1">
                Your Week 1 in the kit starts with{' '}
                <b>
                  {QUESTIONS.slice(0, 5)
                    .map((question) => ({
                      label: question.label,
                      h: answers[question.id] !== undefined ? question.options[answers[question.id]].h : 0,
                    }))
                    .filter((x) => x.h > 0)
                    .sort((a, b) => b.h - a.h)
                    .slice(0, 2)
                    .map((x) => x.label)
                    .join(' and ')}
                </b>. The kit, delivered by email, plans the rest of the month.
              </p>
            </>
          )}
          <a className="btn btn-primary" href="#get-audit">Book a call →</a>
          <p className="quiz-note">Booking starts with a short check so the call is worth your time. The kit arrives by email either way.</p>
        </div>
      )}
    </div>
  )
}
