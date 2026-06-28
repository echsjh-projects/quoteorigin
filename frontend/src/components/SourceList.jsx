const PLATFORM_LABELS = {
  wikiquote: "Wikiquote",
  wikipedia: "Wikipedia",
  newsapi: "News",
  brave_search: "Web Search",
  quotable: "Quotable.io",
  unknown: "Web",
}

const PLATFORM_COLORS = {
  wikiquote: "#3366cc",
  wikipedia: "#3366cc",
  newsapi: "#c0392b",
  brave_search: "#e07b39",
  quotable: "#2d6a4f",
  unknown: "#666",
}

/**
 * SourceList
 * Shows all the raw sources gathered during research.
 */
export function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Sources Consulted ({sources.length})</h3>
      <div style={styles.list}>
        {sources.map((source) => (
          <SourceItem key={source.id} source={source} />
        ))}
      </div>
    </div>
  )
}

function SourceItem({ source }) {
  const label = PLATFORM_LABELS[source.platform] || source.platform
  const color = PLATFORM_COLORS[source.platform] || "#666"

  return (
    <div style={styles.item}>
      <div style={styles.itemHeader}>
        <span style={{ ...styles.platformTag, background: color }}>{label}</span>
        {source.mentioned_date && (
          <span style={styles.date}>{source.mentioned_date}</span>
        )}
        {source.speaker_mentioned && (
          <span style={styles.speaker}>by {source.speaker_mentioned}</span>
        )}
      </div>
      {source.title && <p style={styles.title}>{source.title}</p>}
      {source.snippet && <p style={styles.snippet}>{source.snippet}</p>}
      {source.url && (
        <a href={source.url} target="_blank" rel="noopener noreferrer" style={styles.link}>
          View source ↗
        </a>
      )}
    </div>
  )
}

const styles = {
  container: {
    maxWidth: "680px",
    margin: "2rem auto 0",
  },
  heading: {
    fontSize: "0.85rem",
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: "0.08em",
    color: "#888",
    marginBottom: "0.75rem",
  },
  list: {
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem",
  },
  item: {
    background: "#faf9f6",
    border: "1px solid #e8e4dc",
    borderRadius: "8px",
    padding: "1rem",
  },
  itemHeader: {
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
    flexWrap: "wrap",
    marginBottom: "0.4rem",
  },
  platformTag: {
    color: "#fff",
    fontSize: "0.7rem",
    fontWeight: 700,
    padding: "0.15rem 0.5rem",
    borderRadius: "999px",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  },
  date: {
    fontSize: "0.78rem",
    color: "#888",
  },
  speaker: {
    fontSize: "0.78rem",
    color: "#666",
    fontStyle: "italic",
  },
  title: {
    margin: "0 0 0.3rem",
    fontSize: "0.9rem",
    fontWeight: 600,
    color: "#2c2c2c",
  },
  snippet: {
    margin: "0 0 0.5rem",
    fontSize: "0.85rem",
    color: "#555",
    lineHeight: 1.5,
    display: "-webkit-box",
    WebkitLineClamp: 3,
    WebkitBoxOrient: "vertical",
    overflow: "hidden",
  },
  link: {
    fontSize: "0.78rem",
    color: "#3366cc",
    textDecoration: "none",
  },
}
