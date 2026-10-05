export default function Nav({ cta = '#get-audit', ctaLabel = 'Get the Free Audit', right = null }) {
  return (
    <nav className="nav">
      <div className="nav-inner">
        <a href="index.html" className="nav-logo" aria-label="Pareto Talent">
          <img src="/Final-Project/logo-pareto-talent.png" alt="Pareto Talent" />
        </a>
        <div className="nav-links">
          <a className="nav-link" href="index.html#how">How it works</a>
          <a className="nav-link" href="index.html#inside">What's inside</a>
          <a className="nav-link" href="index.html#faq">FAQ</a>
          {right || <a className="nav-cta" href={cta}>{ctaLabel}</a>}
        </div>
      </div>
    </nav>
  )
}
