import { useState } from "react"

const PLATFORM_CONFIG = {
  wikiquote:    { label: "Wikiquote",    color: "#4a7fc1", bg: "#1a2535" },
  wikipedia:    { label: "Wikipedia",    color: "#4a7fc1", bg: "#1a2535" },
  newsapi:      { label: "News",         color: "#c14a4a", bg: "#2a1a1a" },
  brave_search: { label: "Web",          color: "#c18a4a", bg: "#2a2015" },
  tavily:       { label: "Tavily",       color: "#c18a4a", bg: "#2a2015" },
  quotable:     { label: "Quotable",     color: "#4ac18a", bg: "#152a20" },
  llm_knowledge:{ label: "LLM",         color: "#888",    bg: "#222"    },
  unknown:      { label: "Web",          color: "#888",    bg: "#222"    },
}

export function SourceList({ sources }) {
  const [open, setOpen] = useState(false)
  if (!sources || sources.length === 0) return null

  return (
    <div className="sources-section">
      <div className="sources-header">
        <span>Sources ({sources.length})</span>
        <button className="sources-toggle" onClick={() => setOpen(o => !o)}>
          {open ? "Hide ↑" : "Show ↓"}
        </button>
      </div>

      {open && (
        <div className="sources-list">
          {sources.map(s => <SourceItem key={s.id} source={s} />)}
        </div>
      )}
    </div>
  )
}

function SourceItem({ source }) {
  const cfg = PLATFORM_CONFIG[source.platform] || PLATFORM_CONFIG.unknown

  return (
    <div className="source-item">
      <div className="source-item-header">
        <span
          className="platform-tag"
          style={{ color: cfg.color, borderColor: cfg.color, background: cfg.bg }}
        >
          {cfg.label}
        </span>
        {source.mentioned_date && <span className="source-date">{source.mentioned_date}</span>}
        {source.speaker_mentioned && <span className="source-speaker">— {source.speaker_mentioned}</span>}
      </div>
      {source.title && <p className="source-title">{source.title}</p>}
      {source.snippet && <p className="source-snippet">{source.snippet}</p>}
      {source.url && (
        <a href={source.url} target="_blank" rel="noopener noreferrer" className="source-link">
          View source ↗
        </a>
      )}
    </div>
  )
}
