import { useState } from 'react'

// Quiz answers feed the GHL funnel: on completion, onDone() exposes the
// answers; Landing renders them above the form embed. When the real GHL form
// goes in, map URL params -> custom fields (e.g. ?q_email=6&q_crm=5&q_total=12)
// so workflows can tag and route on every answer.

const QUESTIONS = [
  {
    id: 'q_email',
    label: 'Email & scheduling',
    help: 'Triage, replies, booking meetings, chasing confirmations',
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
    help: 'Updating deals, chasing leads, customer check-ins',
    options: [
      { t: 'Under 2 hrs', h: 0 },
      { t: '2–4 hrs', h: 2 },
      { t: '5–8 hrs', h: 5 },
      { t: '9+ hrs', h: 7 },
    ],
  },
  {
    id: 'q_admin',
    label: 'Invoicing, data entry & reports',
    help: 'Billing, spreadsheets, copy-paste between tools',
    options: [
      { t: 'Under 2 hrs', h: 0 },
      { t: '2–4 hrs', h: 2 },
      { t: '5–8 hrs', h: 5 },
      { t: '9+ hrs', h: 7 },
    ],
  },
  {
    id: 'q_support',
    label: 'Customer support & order issues',
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
    label: 'Recruiting & team admin',
    help: 'Screening, onboarding, timesheets, payroll prep',
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
  if (total === 0) return 'Your week is already lean. The full audit will double-check the corners.'
  if (total <= 5) return 'That is a half-day a week back in founder hands.'
  if (total <= 10) return 'That is a full workday every week, given back to you.'
  return 'That is a full-time salary paid in your hours. Time to hire it back.'
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
          <h3 className="quiz-label">{QUESTIONS[step].label}</h3>
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
          <p className="quiz-math">
            At Pareto's $200/hr founder rate, that is about{' '}
            <b>${Math.round(total * 4.3 * 200).toLocaleString('en-US')}/month</b> of
            founder time stuck in an assistant job.
          </p>
          <a className="btn btn-primary" href="#get-audit">Get the full audit by email →</a>
          <p className="quiz-note">Two minutes, six questions, zero email required to see your number.</p>
        </div>
      )}
    </div>
  )
}
