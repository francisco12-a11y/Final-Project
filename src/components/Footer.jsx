export default function Footer({ label }) {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <span style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <img src="/Final-Project/logo-pareto-talent.png" alt="Pareto Talent" />
          <span>© 2026 · <a href="https://paretotalent.com" target="_blank" rel="noopener">paretotalent.com</a></span>
        </span>
        <span>{label}</span>
      </div>
    </footer>
  )
}
