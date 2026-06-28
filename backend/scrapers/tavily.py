import httpx
from config import get_settings

settings = get_settings()

async def search_web(query: str) -> list[dict]:
    if not settings.tavily_api_key:
        return []

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": settings.tavily_api_key,
                "query": f"{query} quote origin",
                "max_results": 6,
                "search_depth": "basic",
            },
        )
        if resp.status_code != 200:
            return []

        results = resp.json().get("results", [])
        return [{
            "platform": "tavily",
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "mentioned_date": r.get("published_date"),
            "speaker_mentioned": None,
            "relevance": r.get("score", 0.7),
        } for r in results]
