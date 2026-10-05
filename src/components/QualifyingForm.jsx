import { useState } from 'react'

// The landing uses this native styled form instead of the GHL-hosted iframe
// (cross-origin iframes can't be themed from our CSS). Submissions POST to a
// GoHighLevel Inbound Webhook so contacts, tags, and workflows still fire.
//
// FRAN: create a workflow with trigger "Inbound Webhook", copy its URL, and
// paste it below. Map the JSON keys to contact fields in that workflow's
// "Webhook Received" step. Until then the form validates and routes but the
// lead is not stored in GHL.

const GHL_WEBHOOK_URL = ''

const QUALIFIED_VALUE = (v) =>
  (v.revenue === '10-50' || v.revenue === '50+') &&
  v.hours === '15+' &&
  v.owner === 'yes'

export default function QualifyingForm({ quizResult }) {
  const [sending, setSending] = useState(false)

  function submit(e) {
    e.preventDefault()
    const data = new FormData(e.target)
    const v = {
      full_name: (data.get('full_name') || '').trim(),
      email: (data.get('email') || '').trim(),
      phone: (data.get('phone') || '').trim(),
      revenue: data.get('revenue') || '',
      hours: data.get('hours') || '',
      owner: data.get('owner') || '',
    }
    if (!v.full_name || !v.email || !v.revenue || !v.hours || !v.owner) return
    setSending(true)

    const payload = {
      ...v,
      ...Object.fromEntries((quizResult?.hours || []).map((h) => [h.id, h.h])),
      q_total: quizResult ? quizResult.total : null,
      q_who: quizResult ? quizResult.who : null,
    }
    const go = () => {
      window.location.href = QUALIFIED_VALUE(v) ? 'qualified.html' : 'thank-you.html'
    }
    if (GHL_WEBHOOK_URL) {
      fetch(GHL_WEBHOOK_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify(payload),
      })
        .catch(() => {})
        .finally(() => setTimeout(go, 500))
    } else {
      console.warn('GHL_WEBHOOK_URL not set — lead not stored yet, routing only.')
      setTimeout(go, 500)
    }
  }

  return (
    <form className="qform" onSubmit={submit}>
      <div className="qform-row">
        <label>
          Full name *
          <input name="full_name" type="text" required placeholder="Your name" />
        </label>
        <label>
          Email *
          <input name="email" type="email" required placeholder="you@company.com" />
        </label>
      </div>
      <label>
        Phone *
        <input name="phone" type="tel" required placeholder="+1 (555) 000-0000" />
      </label>
      <label>
        What's your monthly revenue today? *
        <select name="revenue" required defaultValue="">
          <option value="" disabled>Choose one</option>
          <option value="idea">Idea / pre-revenue</option>
          <option value="under-10">Under $10k/month</option>
          <option value="10-50">$10k–$50k/month</option>
          <option value="50+">$50k+/month</option>
        </select>
      </label>
      <label>
        How many hours a week does the assistant job take (inbox, calendar, CRM, follow-ups)? *
        <select name="hours" required defaultValue="">
          <option value="" disabled>Choose one</option>
          <option value="under-5">Under 5 hours</option>
          <option value="5-14">5–14 hours</option>
          <option value="15+">15 hours or more</option>
        </select>
      </label>
      <label>
        Are you the founder or co-founder, and the hiring decision-maker? *
        <select name="owner" required defaultValue="">
          <option value="" disabled>Choose one</option>
          <option value="yes">Yes</option>
          <option value="not-yet">Not yet / someone else decides</option>
        </select>
      </label>
      <button className="btn btn-primary qform-submit" type="submit" disabled={sending}>
        {sending ? 'Sending…' : 'Continue →'}
      </button>
    </form>
  )
}
