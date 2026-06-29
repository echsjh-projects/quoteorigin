export function RecentSearches({ quotes, onSelect }) {
  if (!quotes || quotes.length === 0) return null

  return (
    <div className="recent-section">
      <div className="section-eyebrow">Recently traced</div>
      <div className="recent-grid">
        {quotes.map(q => (
          <button
            key={q.id}
            className="recent-item"
            onClick={() => onSelect(q.input_text)}
          >
            <div className="recent-item-left">
              <p className="recent-quote-text">
                "{q.input_text.length > 80 ? q.input_text.slice(0, 80) + "…" : q.input_text}"
              </p>
              {q.speaker && (
                <span className="recent-speaker">— {q.speaker}{q.earliest_date ? `, ${q.earliest_date}` : ""}</span>
              )}
            </div>
            <span className="recent-date">↗</span>
          </button>
        ))}
      </div>
    </div>
  )
}
