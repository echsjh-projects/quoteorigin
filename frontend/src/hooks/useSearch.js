import { useState, useCallback } from "react"
import { api } from "../api/client"

/**
 * useSearch hook
 * Encapsulates all search state so components stay clean.
 *
 * Returns: { result, loading, error, search, reset }
 */
export function useSearch() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const search = useCallback(async (quote) => {
    if (!quote.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await api.searchQuote(quote.trim())
      setResult(data)
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.")
    } finally {
      setLoading(false)
    }
  }, [])

  const reset = useCallback(() => {
    setResult(null)
    setError(null)
  }, [])

  return { result, loading, error, search, reset }
}
