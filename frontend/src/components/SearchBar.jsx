import { useState } from "react"

/**
 * SearchBar
 * Props:
 *   onSearch(quote: string) — called when user submits
 *   loading: bool — disables input while searching
 */
export function SearchBar({ onSearch, loading }) {
  const [value, setValue] = useState("")

  function handleSubmit(e) {
    e.preventDefault()
    if (value.trim()) onSearch(value)
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <textarea
        style={styles.textarea}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={`Paste a quote here…\ne.g. "Blood, sweat, and tears"`}
        rows={3}
        disabled={loading}
        onKeyDown={(e) => {
          // Ctrl+Enter or Cmd+Enter to submit
          if ((e.ctrlKey || e.metaKey) && e.key === "Enter") handleSubmit(e)
        }}
      />
      <button type="submit" style={styles.button} disabled={loading || !value.trim()}>
        {loading ? "Researching…" : "Trace Origin →"}
      </button>
      <p style={styles.hint}>Press Ctrl+Enter to search</p>
    </form>
  )
}

const styles = {
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "0.75rem",
    width: "100%",
    maxWidth: "680px",
    margin: "0 auto",
  },
  textarea: {
    width: "100%",
    padding: "1rem",
    fontSize: "1.1rem",
    fontFamily: "Georgia, serif",
    border: "2px solid #d0c8b8",
    borderRadius: "8px",
    background: "#faf9f6",
    color: "#2c2c2c",
    resize: "vertical",
    lineHeight: 1.5,
    boxSizing: "border-box",
  },
  button: {
    alignSelf: "flex-end",
    padding: "0.75rem 2rem",
    fontSize: "1rem",
    fontWeight: "600",
    background: "#2c2c2c",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    transition: "background 0.2s",
  },
  hint: {
    margin: 0,
    fontSize: "0.78rem",
    color: "#888",
    textAlign: "right",
  },
}
