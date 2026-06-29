"""
routers/quotes.py
-----------------
All /api/quotes endpoints live here.
The router is registered in main.py.
"""

import asyncio
import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database import crud
from database.schemas import QuoteSearchRequest, SearchResponse
from nlp.groq_client import extract_provenance
from scrapers import (
    search_wikiquote,
    search_wikipedia,
    search_news,
    search_web,
    search_quotable,
)

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


@router.post("/search", response_model=SearchResponse)
async def search_quote(
    request: QuoteSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Main endpoint: given a quote, find its earliest known source.

    Flow:
      1. Check DB cache — return immediately if already researched
      2. Fire all scrapers in parallel (asyncio.gather)
      3. Feed results to Groq LLM for NLP extraction
      4. Save everything to PostgreSQL
      5. Return structured response
    """
    start_ms = int(time.time() * 1000)

    # ── 1. Cache check ────────────────────────────────────────────────────────
    cached = await crud.get_quote_by_text(db, request.quote)
    if cached and cached.is_resolved:
        # Explicitly load sources async — never access relationships directly
        from sqlalchemy import select
        from database.models import Source
        source_result = await db.execute(
            select(Source).where(Source.quote_id == cached.id)
        )
        cached.sources = source_result.scalars().all()
        
        duration = int(time.time() * 1000) - start_ms
        await crud.log_search(db, request.quote, True, len(cached.sources), duration)
        return SearchResponse(
            quote=cached,
            cache_hit=True,
            sources_found=len(cached.sources),
            duration_ms=duration,
        )

    # ── 2. Run all scrapers in parallel ───────────────────────────────────────
    results = await asyncio.gather(
        search_quotable(request.quote),   # fastest — check curated DB first
        search_wikiquote(request.quote),
        search_wikipedia(request.quote),
        search_news(request.quote),
        search_web(request.quote),
        return_exceptions=True,           # don't let one scraper crash everything
    )

    # Flatten results, skip any scrapers that threw exceptions
    all_sources: list[dict] = []
    for batch in results:
        if isinstance(batch, Exception):
            continue  # log silently in production
        all_sources.extend(batch)

    if not all_sources:
        raise HTTPException(
            status_code=503,
            detail="All scrapers failed. Please check API keys and try again.",
        )

    # ── 3. LLM extraction via Groq ────────────────────────────────────────────
    provenance = await extract_provenance(request.quote, all_sources)

    # ── 4. Save to PostgreSQL ─────────────────────────────────────────────────
    quote = await crud.save_quote(db, request.quote, provenance, all_sources)

    # ── 5. Return response ────────────────────────────────────────────────────
    duration = int(time.time() * 1000) - start_ms
    await crud.log_search(db, request.quote, False, len(all_sources), duration)

    return SearchResponse(
        quote=quote,
        cache_hit=False,
        sources_found=len(all_sources),
        duration_ms=duration,
    )


@router.get("/recent")
async def get_recent_quotes(limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Return the most recently searched quotes (for the homepage)."""
    from sqlalchemy import select
    from database.models import Quote

    result = await db.execute(
        select(Quote)
        .where(Quote.is_resolved == True)
        .order_by(Quote.created_at.desc())
        .limit(limit)
    )
    quotes = result.scalars().all()
    return {"quotes": quotes}
