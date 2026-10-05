export default function ImgPlaceholder({ label, hint, ratio = '16 / 9', wide = false }) {
  return (
    <figure
      className="img-placeholder"
      style={{ aspectRatio: ratio }}
      data-wide={wide || undefined}
    >
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <rect x="3" y="4" width="18" height="16" rx="2" stroke="#10b981" strokeWidth="1.6" />
        <circle cx="9" cy="10" r="1.8" fill="#10b981" />
        <path d="M4 18l5-5 3.5 3.5L16 13l4 5" stroke="#10b981" strokeWidth="1.6" strokeLinejoin="round" />
      </svg>
      <figcaption>
        <span className="ph-label">{label}</span>
        {hint && <span className="ph-hint">{hint}</span>}
      </figcaption>
    </figure>
  )
}
