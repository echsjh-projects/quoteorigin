"""
scrapers/newsapi.py
-------------------
Searches NewsAPI.org for news articles mentioning the quote.
Free tier: 100 requests/day, articles from last 30 days only.
Sign up at: https://newsapi.org/register

Note: For historical quotes, NewsAPI is less useful (30-day limit).
It's most useful for recently viral quotes or misattributions in the news.
"""

import httpx
from config import get_settings

settings = get_settings()
BASE_URL = "https://newsapi.org/v2/everything"


async def search_news(query: str) -> list[dict]:
    """
    Search NewsAPI for articles mentioning the quote.
    Returns empty list if no API key is configured.
    """
    if not settings.news_api_key:
        return []

    sources = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(BASE_URL, params={
            "q": f'"{query}"',          # exact phrase search
            "apiKey": settings.news_api_key,
            "pageSize": 5,
            "sortBy": "publishedAt",
            "language": "en",
        })

        if resp.status_code != 200:
            return []

        data = resp.json()
        articles = data.get("articles", [])

        for article in articles[:5]:
            sources.append({
                "platform": "newsapi",
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "snippet": article.get("description", "") or article.get("content", "")[:300],
                "mentioned_date": article.get("publishedAt", "")[:10],  # YYYY-MM-DD
                "speaker_mentioned": article.get("source", {}).get("name"),
                "relevance": 0.7,
            })

    return sources
