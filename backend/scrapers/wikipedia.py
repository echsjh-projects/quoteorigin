"""
scrapers/wikipedia.py
---------------------
Searches Wikipedia for context about a quote's likely speaker.
Free MediaWiki API — no key required.
"""

import httpx
import re

BASE_URL = "https://en.wikipedia.org/w/api.php"


async def search_wikipedia(query: str) -> list[dict]:
    """
    Search Wikipedia and return relevant page extracts.
    Useful for confirming biographical details about speakers.
    """
    sources = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(BASE_URL, params={
            "action": "query",
            "list": "search",
            "srsearch": f'"{query}" quote',
            "format": "json",
            "srlimit": 3,
            "srprop": "snippet",
        })
        data = resp.json()
        results = data.get("query", {}).get("search", [])

        for result in results[:3]:
            title = result.get("title", "")
            raw_snippet = result.get("snippet", "")
            clean = re.sub(r"<[^>]+>", "", raw_snippet)

            sources.append({
                "platform": "wikipedia",
                "title": title,
                "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                "snippet": clean,
                "mentioned_date": None,
                "speaker_mentioned": None,
                "relevance": 0.6,
            })

    return sources
