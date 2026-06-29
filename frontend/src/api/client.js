/**
 * api/client.js
 * -------------
 * All fetch calls to the backend live here.
 *
 * VITE_API_URL is set to "" in local dev (the Vite proxy handles /api → localhost:8000)
 * and to your Render URL in production (set in Vercel dashboard).
 */

const BASE_URL = import.meta.env.VITE_API_URL || ""

async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || "Request failed")
  }

  return res.json()
}

export const api = {
  /** Search for quote provenance */
  searchQuote: async (quote) => {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 30000)
    try {
      return await request("/api/quotes/search", {
        method: "POST",
        body: JSON.stringify({ quote }),
        signal: controller.signal,
      })
    } catch (err) {
      if (err.name === "AbortError") {
        throw new Error("Search timed out — the result may still be processing. Try searching again in a few seconds.")
      }
      throw err
    } finally {
      clearTimeout(timeout)
    }
  },

  /** Get recently searched quotes for the homepage */
  getRecent: (limit = 8) =>
    request(`/api/quotes/recent?limit=${limit}`),

  /** Health check */
  health: () => request("/health"),
}
