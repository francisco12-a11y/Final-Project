export default function TalentPool() {
  return (
    <section className="section" id="talent-pool">
      <div className="container">
        <div className="center">
          <span className="eyebrow">The talent pool</span>
          <h2 className="section-title">One in a thousand makes it in</h2>
          <p className="section-sub">
            Every Right Hand comes from a pool with a 1-in-1,000 acceptance rate,
            trains 40+ hours on the AI stack before they ever meet you, and works
            your hours from Latin America. This is the team behind every match.
          </p>
        </div>
        <figure className="pool-photo">
          <img
            src="/Final-Project/site-assets/pareto-team.jpg"
            alt="The Pareto Talent team in Buenos Aires"
            loading="lazy"
          />
        </figure>
        <div className="pool-stats">
          <div className="pool-card">
            <span className="pool-num">1 in 1,000</span>
            <span className="pool-label">acceptance rate into the pool</span>
          </div>
          <div className="pool-card">
            <span className="pool-num">40+ hours</span>
            <span className="pool-label">AI-stack training before day one</span>
          </div>
          <div className="pool-card">
            <span className="pool-num">US hours</span>
            <span className="pool-label">full-time from Latin America</span>
          </div>
        </div>
      </div>
    </section>
  )
}
