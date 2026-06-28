import { SearchBar } from "./components/SearchBar"
import { ResultCard } from "./components/ResultCard"
import { SourceList } from "./components/SourceList"
import { useSearch } from "./hooks/useSearch"

export default function App() {
  const { result, loading, error, search, reset } = useSearch()

  return (
    <div style={styles.page}>
      {/* Header */}
      <header style={styles.header}>
        <button onClick={reset} style={styles.logoBtn}>
          <h1 style={styles.logo}>QuoteOrigin</h1>
          <p style={styles.tagline}>Trace any quote to its earliest known source</p>
        </button>
      </header>

      {/* Main content */}
      <main style={styles.main}>
        <SearchBar onSearch={search} loading={loading} />

        {/* Loading state */}
        {loading && (
          <div style={styles.loading}>
            <div style={styles.spinner} />
            <p style={styles.loadingText}>
              Searching Wikiquote, news archives, and the web…<br />
              <span style={styles.loadingSubtext}>This takes 5–15 seconds</span>
            </p>
          </div>
        )}

        {/* Error state */}
        {error && !loading && (
          <div style={styles.error}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <>
            <ResultCard result={result} />
            <SourceList sources={result.quote.sources} />
            <div style={styles.newSearch}>
              <button onClick={reset} style={styles.newSearchBtn}>
                ← Search another quote
              </button>
            </div>
          </>
        )}

        {/* Empty state */}
        {!result && !loading && !error && (
          <div style={styles.examples}>
            <p style={styles.examplesLabel}>Try these examples:</p>
            <div style={styles.exampleList}>
              {EXAMPLES.map((ex) => (
                <button key={ex} style={styles.exampleBtn} onClick={() => search(ex)}>
                  "{ex}"
                </button>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer style={styles.footer}>
        Built with Groq · FastAPI · PostgreSQL · React
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

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f5f3ee",
    color: "#2c2c2c",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    borderBottom: "1px solid #d0c8b8",
    background: "#faf9f6",
    padding: "2rem 1rem 1.5rem",
    textAlign: "center",
  },
  logoBtn: {
    background: "none",
    border: "none",
    cursor: "pointer",
    padding: 0,
  },
  logo: {
    margin: 0,
    fontSize: "2.2rem",
    fontFamily: "Georgia, serif",
    fontWeight: 700,
    letterSpacing: "-0.02em",
    color: "#2c2c2c",
  },
  tagline: {
    margin: "0.3rem 0 0",
    fontSize: "0.95rem",
    color: "#777",
  },
  main: {
    flex: 1,
    maxWidth: "780px",
    width: "100%",
    margin: "0 auto",
    padding: "2.5rem 1rem 3rem",
  },
  loading: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "1rem",
    marginTop: "3rem",
  },
  spinner: {
    width: 36,
    height: 36,
    border: "3px solid #d0c8b8",
    borderTop: "3px solid #2c2c2c",
    borderRadius: "50%",
    animation: "spin 0.9s linear infinite",
  },
  loadingText: {
    textAlign: "center",
    color: "#555",
    lineHeight: 1.7,
    margin: 0,
  },
  loadingSubtext: {
    fontSize: "0.82rem",
    color: "#999",
  },
  error: {
    marginTop: "1.5rem",
    padding: "1rem 1.25rem",
    background: "#fdf0f0",
    border: "1px solid #f5c6c6",
    borderRadius: "8px",
    color: "#c0392b",
    maxWidth: "680px",
    margin: "1.5rem auto 0",
  },
  examples: {
    marginTop: "3rem",
    textAlign: "center",
  },
  examplesLabel: {
    fontSize: "0.85rem",
    color: "#888",
    marginBottom: "0.75rem",
    textTransform: "uppercase",
    letterSpacing: "0.06em",
    fontWeight: 600,
  },
  exampleList: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
    gap: "0.5rem",
  },
  exampleBtn: {
    background: "#faf9f6",
    border: "1px solid #d0c8b8",
    borderRadius: "999px",
    padding: "0.45rem 1rem",
    fontSize: "0.88rem",
    color: "#555",
    fontFamily: "Georgia, serif",
    fontStyle: "italic",
    cursor: "pointer",
    transition: "border-color 0.2s",
  },
  newSearch: {
    textAlign: "center",
    marginTop: "2.5rem",
  },
  newSearchBtn: {
    background: "none",
    border: "none",
    color: "#3366cc",
    fontSize: "0.9rem",
    cursor: "pointer",
    textDecoration: "underline",
  },
  footer: {
    borderTop: "1px solid #d0c8b8",
    padding: "1.25rem",
    textAlign: "center",
    fontSize: "0.78rem",
    color: "#aaa",
  },
}
