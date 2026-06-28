"""
scrapers/quotable.py
--------------------
Searches Quotable.io — a free, open-source quote API with 1,500+ curated,
attributed quotes. No API key required.
API docs: https://github.com/lukePeavey/quotable

This is the fastest source to check: if the quote exists here,
we get the speaker and tags immediately with high confidence.
"""

import httpx

BASE_URL = "https://api.quotable.kurokeita.dev"


async def search_quotable(query: str) -> list[dict]:
    """
    Search Quotable for matching quotes. Returns structured source dicts.
    """
    sources = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(f"{BASE_URL}/quotes", params={
                "query": query,
                "limit": 5,
            })

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = data.get("results", [])

            for q in results:
                author = q.get("author", {})
                author_name = author.get("name", "") if isinstance(author, dict) else str(author)
                sources.append({
                    "platform": "quotable",
                    "title": f"Quote by {author_name}",
                    "url": None,
                    "snippet": q.get("content", ""),
                    "mentioned_date": None,
                    "speaker_mentioned": author_name,
                    "relevance": 0.95,  # Curated + attributed = high confidence
                })
        except Exception:
            pass  # Quotable going down shouldn't break the whole search

    return sources
