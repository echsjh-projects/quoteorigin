import { useState, useEffect } from "react"
import { SearchBar } from "./components/SearchBar"
import { ResultCard } from "./components/ResultCard"
import { SourceList } from "./components/SourceList"
import { RecentSearches } from "./components/RecentSearches"
import { useSearch } from "./hooks/useSearch"
import { api } from "./api/client"
import "./App.css"

export default function App() {
  const { result, loading, error, search, reset } = useSearch()
  const [recent, setRecent] = useState([])

  useEffect(() => {
    api.getRecent(6).then(data => setRecent(data.quotes || [])).catch(() => {})
  }, [result])

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="header-title">
            <span className="header-eyebrow">NLP · Quote Provenance</span>
            <h1 className="header-h1">QuoteOrigin</h1>
          </div>
          <div className="header-meta">
            <span className="meta-pill">Groq LLaMA 3</span>
            <span className="meta-pill">Wikiquote</span>
            <span className="meta-pill">Tavily</span>
            <span className="meta-pill accent">Live</span>
          </div>
        </div>
      </header>

      <main className="main">
        {result && (
          <div className="back-row">
            <button className="btn ghost" onClick={reset}>← New search</button>
          </div>
        )}

        <SearchBar onSearch={search} loading={loading} />

        {loading && (
          <div className="loading-wrap">
            <div className="spinner" />
            <div className="loading-text">
              Searching Wikiquote · NewsAPI · Tavily · Groq…<br />
              First search may take up to 30 seconds
            </div>
          </div>
        )}

        {error && !loading && (
          <div className="error-box">
            ERROR › {error}
          </div>
        )}

        {result && !loading && (
          <>
            <ResultCard result={result} />
            <SourceList sources={result.quote.sources} />
          </>
        )}

        {!result && !loading && !error && (
          <>
            <div className="examples-section">
              <div className="examples-label">Try an example</div>
              <div className="examples-grid">
                {EXAMPLES.map(ex => (
                  <button key={ex} className="example-btn" onClick={() => search(ex)}>
                    "{ex}"
                  </button>
                ))}
              </div>
            </div>

            {recent.length > 0 && (
              <RecentSearches quotes={recent} onSelect={search} />
            )}
          </>
        )}
      </main>

      <footer className="footer">
        Built with FastAPI · Groq LLaMA 3 · PostgreSQL · React · Neon · Render · Vercel
      </footer>
    </div>
  )
}

const EXAMPLES = [
  "Blood, sweat, and tears",
  "The only thing we have to fear is fear itself",
  "Be the change you wish to see in the world",
  "Elementary, my dear Watson",
]
