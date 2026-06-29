import { useState } from "react"

export function SearchBar({ onSearch, loading }) {
  const [value, setValue] = useState("")

  function handleSubmit(e) {
    e.preventDefault()
    if (value.trim()) onSearch(value)
  }

  return (
    <form onSubmit={handleSubmit}>
      <label className="search-label">Enter a quote</label>
      <textarea
        className="search-textarea"
        value={value}
        onChange={e => setValue(e.target.value)}
        placeholder={`e.g. "Blood, sweat, and tears"`}
        rows={3}
        disabled={loading}
        onKeyDown={e => {
          if ((e.ctrlKey || e.metaKey) && e.key === "Enter") handleSubmit(e)
        }}
      />
      <div className="search-row">
        <span className="search-hint">Ctrl+Enter to search</span>
        <button
          type="submit"
          className="btn"
          disabled={loading || !value.trim()}
        >
          {loading ? "Researching…" : "Trace Origin →"}
        </button>
      </div>
    </form>
  )
}
