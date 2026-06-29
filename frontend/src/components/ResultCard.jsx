import { useState } from "react"

export function ResultCard({ result }) {
  const { quote, cache_hit, sources_found, duration_ms } = result
  const [copied, setCopied] = useState(false)

  const pct = quote.confidence_score ? Math.round(quote.confidence_score * 100) : null
  const barColor = pct >= 75 ? "#d4a843" : pct >= 45 ? "#b8922e" : "#8a4040"

  function handleShare() {
    const text = `"${quote.original_phrasing || quote.input_text}" — ${quote.speaker || "Unknown"} (${quote.earliest_date || "date unknown"})\n\nFound via QuoteOrigin`
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <div className="result-card">
      <div className="result-header">
        <div className="result-header-left">
          <span className="result-eyebrow">Origin found</span>
          {cache_hit && <span className="cache-tag">⚡ cached</span>}
        </div>
        <button className="btn secondary" onClick={handleShare} style={{ padding: "5px 14px" }}>
          {copied ? <span className="share-toast">Copied ✓</span> : "Share"}
        </button>
      </div>

      <div className="result-body">
        <blockquote className="result-quote">
          "{quote.original_phrasing || quote.input_text}"
        </blockquote>

        <div className="stat-row">
          {quote.speaker && (
            <div className="stat">
              <div className="stat-label">Speaker / Author</div>
              <div className="stat-val">{quote.speaker}</div>
            </div>
          )}
          {quote.earliest_date && (
            <div className="stat">
              <div className="stat-label">Earliest known date</div>
              <div className="stat-val">{quote.earliest_date}</div>
            </div>
          )}
          {pct !== null && (
            <div className="stat">
              <div className="stat-label">Confidence</div>
              <div className="confidence-row">
                <div className="confidence-bar-track">
                  <div
                    className="confidence-bar-fill"
                    style={{ width: `${pct}%`, background: barColor }}
                  />
                </div>
                <span className="confidence-pct">{pct}%</span>
              </div>
            </div>
          )}
        </div>

        {quote.reasoning && (
          <div className="analysis-section">
            <div className="analysis-label">Analysis</div>
            <p className="analysis-text">{quote.reasoning}</p>
          </div>
        )}
      </div>

      <div className="result-meta">
        <span>{sources_found} sources consulted{duration_ms ? ` · ${(duration_ms / 1000).toFixed(1)}s` : ""}</span>
      </div>
    </div>
  )
}
