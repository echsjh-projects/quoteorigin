"""
scrapers/brave_search.py
------------------------
Uses the Brave Search API for general web results.
Free tier: 2,000 requests/month.
Sign up at: https://api.search.brave.com/

Brave is a good alternative to Google Custom Search (which has a very
small free tier) and returns clean, unbiased results.
"""

import httpx
from config import get_settings

settings = get_settings()
BASE_URL = "https://api.search.brave.com/res/v1/web/search"


async def search_web(query: str) -> list[dict]:
    """
    Search the web via Brave Search API.
    Returns empty list if no API key is configured.
    """
    if not settings.brave_api_key:
        return []

    sources = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            BASE_URL,
            params={
                "q": f'"{query}" quote origin',
                "count": 8,
                "search_lang": "en",
            },
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": settings.brave_api_key,
            },
        )

        if resp.status_code != 200:
            return []

        data = resp.json()
        results = data.get("web", {}).get("results", [])

        for result in results[:6]:
            sources.append({
                "platform": "brave_search",
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("description", ""),
                "mentioned_date": result.get("page_age", None),
                "speaker_mentioned": None,
                "relevance": 0.75,
            })

    return sources
