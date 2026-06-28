/**
 * ResultCard
 * Shows the main provenance result: speaker, date, original phrasing, confidence.
 */
export function ResultCard({ result }) {
  const { quote, cache_hit, sources_found, duration_ms } = result
  const confidencePct = quote.confidence_score
    ? Math.round(quote.confidence_score * 100)
    : null

  return (
    <div style={styles.card}>
      {/* Header */}
      <div style={styles.header}>
        <span style={styles.badge}>Origin Found</span>
        {cache_hit && <span style={styles.cacheBadge}>⚡ Cached</span>}
      </div>

      {/* Original phrasing */}
      <blockquote style={styles.blockquote}>
        "{quote.original_phrasing || quote.input_text}"
      </blockquote>

      {/* Attribution row */}
      <div style={styles.attribution}>
        {quote.speaker && (
          <div style={styles.attributionItem}>
            <span style={styles.label}>Speaker / Author</span>
            <span style={styles.value}>{quote.speaker}</span>
          </div>
        )}
        {quote.earliest_date && (
          <div style={styles.attributionItem}>
            <span style={styles.label}>Earliest Known Date</span>
            <span style={styles.value}>{quote.earliest_date}</span>
          </div>
        )}
        {confidencePct !== null && (
          <div style={styles.attributionItem}>
            <span style={styles.label}>Confidence</span>
            <ConfidenceBar pct={confidencePct} />
          </div>
        )}
      </div>

      {/* Reasoning */}
      {quote.reasoning && (
        <div style={styles.reasoning}>
          <span style={styles.label}>Analysis</span>
          <p style={styles.reasoningText}>{quote.reasoning}</p>
        </div>
      )}

      {/* Meta */}
      <div style={styles.meta}>
        {sources_found} sources consulted
        {duration_ms && ` · ${(duration_ms / 1000).toFixed(1)}s`}
      </div>
    </div>
  )
}

function ConfidenceBar({ pct }) {
  const color = pct >= 75 ? "#2d6a4f" : pct >= 45 ? "#b5651d" : "#c0392b"
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
      <div style={{ width: 120, height: 8, background: "#e8e4dc", borderRadius: 4, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 4 }} />
      </div>
      <span style={{ fontSize: "0.9rem", fontWeight: 600, color }}>{pct}%</span>
    </div>
  )
}

const styles = {
  card: {
    background: "#faf9f6",
    border: "1px solid #d0c8b8",
    borderRadius: "12px",
    padding: "2rem",
    maxWidth: "680px",
    margin: "2rem auto 0",
    boxShadow: "0 2px 12px rgba(0,0,0,0.07)",
  },
  header: {
    display: "flex",
    gap: "0.5rem",
    marginBottom: "1.25rem",
  },
  badge: {
    background: "#2c2c2c",
    color: "#fff",
    fontSize: "0.75rem",
    fontWeight: 700,
    padding: "0.2rem 0.65rem",
    borderRadius: "999px",
    letterSpacing: "0.05em",
    textTransform: "uppercase",
  },
  cacheBadge: {
    background: "#e8f4ea",
    color: "#2d6a4f",
    fontSize: "0.75rem",
    fontWeight: 700,
    padding: "0.2rem 0.65rem",
    borderRadius: "999px",
  },
  blockquote: {
    fontFamily: "Georgia, serif",
    fontSize: "1.25rem",
    fontStyle: "italic",
    color: "#2c2c2c",
    margin: "0 0 1.5rem",
    paddingLeft: "1rem",
    borderLeft: "3px solid #d0c8b8",
    lineHeight: 1.6,
  },
  attribution: {
    display: "flex",
    flexDirection: "column",
    gap: "0.9rem",
    marginBottom: "1.5rem",
  },
  attributionItem: {
    display: "flex",
    flexDirection: "column",
    gap: "0.2rem",
  },
  label: {
    fontSize: "0.72rem",
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#888",
  },
  value: {
    fontSize: "1.05rem",
    fontWeight: 600,
    color: "#2c2c2c",
  },
  reasoning: {
    borderTop: "1px solid #e8e4dc",
    paddingTop: "1rem",
    marginBottom: "1rem",
  },
  reasoningText: {
    margin: "0.4rem 0 0",
    fontSize: "0.92rem",
    color: "#555",
    lineHeight: 1.6,
  },
  meta: {
    fontSize: "0.78rem",
    color: "#aaa",
    borderTop: "1px solid #e8e4dc",
    paddingTop: "0.75rem",
    marginTop: "0.5rem",
  },
}
