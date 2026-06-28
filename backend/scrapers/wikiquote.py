"""
scrapers/wikiquote.py
---------------------
Searches Wikiquote using the free MediaWiki API (no API key required).
Wikiquote is one of the best sources for attributed quotes with context.
"""

import httpx
import re

BASE_URL = "https://en.wikiquote.org/w/api.php"


async def search_wikiquote(query: str) -> list[dict]:
    """
    Search Wikiquote for pages matching the query, then fetch snippets.
    Returns a list of source dicts.
    """
    sources = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Step 1: full-text search
        search_resp = await client.get(BASE_URL, params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 5,
            "srprop": "snippet|titlesnippet",
        })
        search_data = search_resp.json()
        results = search_data.get("query", {}).get("search", [])

        for result in results[:4]:
            title = result.get("title", "")
            raw_snippet = result.get("snippet", "")
            # Strip HTML tags from snippet
            clean_snippet = re.sub(r"<[^>]+>", "", raw_snippet)

            sources.append({
                "platform": "wikiquote",
                "title": title,
                "url": f"https://en.wikiquote.org/wiki/{title.replace(' ', '_')}",
                "snippet": clean_snippet,
                "mentioned_date": None,
                "speaker_mentioned": title,  # Wikiquote pages are named after the speaker
                "relevance": 0.9,
            })

    return sources
