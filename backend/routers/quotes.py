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
from sqlalchemy import select

from database.connection import get_db
from database.models import Quote, Source, SearchLog
from database.schemas import QuoteSearchRequest, SearchResponse, QuoteOut, SourceOut
from nlp.normalizer import normalize_quote
from nlp.groq_client import extract_provenance
from scrapers import (
    search_wikiquote,
    search_wikipedia,
    search_news,
    search_web,
    search_quotable,
)

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


async def get_sources_for_quote(db: AsyncSession, quote_id: int) -> list[Source]:
    result = await db.execute(
        select(Source).where(Source.quote_id == quote_id)
    )
    return result.scalars().all()


def build_quote_out(quote: Quote, sources: list[Source]) -> QuoteOut:
    return QuoteOut(
        id=quote.id,
        input_text=quote.input_text,
        original_phrasing=quote.original_phrasing,
        speaker=quote.speaker,
        earliest_date=quote.earliest_date,
        confidence_score=quote.confidence_score,
        reasoning=quote.reasoning,
        is_resolved=quote.is_resolved,
        created_at=quote.created_at,
        sources=[SourceOut(
            id=s.id,
            platform=s.platform,
            title=s.title,
            url=s.url,
            snippet=s.snippet,
            mentioned_date=s.mentioned_date,
            speaker_mentioned=s.speaker_mentioned,
            relevance=s.relevance,
        ) for s in sources],
    )


@router.post("/search", response_model=SearchResponse)
async def search_quote(
    request: QuoteSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    start_ms = int(time.time() * 1000)
    normalized = normalize_quote(request.quote)

    # ── 1. Cache check ────────────────────────────────────────────────────────
    cached_result = await db.execute(
        select(Quote).where(Quote.normalized_text == normalized)
    )
    cached = cached_result.scalar_one_or_none()

    if cached and cached.is_resolved:
        sources = await get_sources_for_quote(db, cached.id)
        duration = int(time.time() * 1000) - start_ms

        log = SearchLog(input_text=request.quote, cache_hit=True,
                       sources_found=len(sources), duration_ms=duration)
        db.add(log)
        await db.commit()

        return SearchResponse(
            quote=build_quote_out(cached, sources),
            cache_hit=True,
            sources_found=len(sources),
            duration_ms=duration,
        )

    # ── 2. Run all scrapers in parallel ───────────────────────────────────────
    results = await asyncio.gather(
        search_quotable(request.quote),
        search_wikiquote(request.quote),
        search_wikipedia(request.quote),
        search_news(request.quote),
        search_web(request.quote),
        return_exceptions=True,
    )

    all_sources: list[dict] = []
    for batch in results:
        if isinstance(batch, Exception):
            continue
        all_sources.extend(batch)

    #if not all_sources:
    #    raise HTTPException(status_code=503, detail="All scrapers failed.")

    # If no scrapers found anything, let Groq use its own knowledge
    if not all_sources:
        all_sources = [{
            "platform": "llm_knowledge",
            "title": "LLM internal knowledge",
            "snippet": "No external sources found. Using LLM training knowledge only.",
            "url": None,
            "mentioned_date": None,
            "speaker_mentioned": None,
            "relevance": 0.5,
        }]

    # ── 3. LLM extraction via Groq ────────────────────────────────────────────
    provenance = await extract_provenance(request.quote, all_sources)

    # ── 4. Save to PostgreSQL ─────────────────────────────────────────────────
    quote = Quote(
        normalized_text=normalized,
        input_text=request.quote,
        original_phrasing=provenance.get("original_phrasing"),
        speaker=provenance.get("speaker"),
        earliest_date=provenance.get("earliest_date"),
        confidence_score=provenance.get("confidence"),
        reasoning=provenance.get("reasoning"),
        is_resolved=True,
    )
    db.add(quote)
    await db.flush()

    for s in all_sources:
        db.add(Source(
            quote_id=quote.id,
            platform=s.get("platform", "unknown"),
            title=s.get("title"),
            url=s.get("url"),
            snippet=s.get("snippet"),
            mentioned_date=s.get("mentioned_date"),
            speaker_mentioned=s.get("speaker_mentioned"),
            relevance=s.get("relevance"),
        ))

    await db.commit()

    sources = await get_sources_for_quote(db, quote.id)
    duration = int(time.time() * 1000) - start_ms

    log = SearchLog(input_text=request.quote, cache_hit=False,
                   sources_found=len(sources), duration_ms=duration)
    db.add(log)
    await db.commit()

    return SearchResponse(
        quote=build_quote_out(quote, sources),
        cache_hit=False,
        sources_found=len(sources),
        duration_ms=duration,
    )


@router.get("/recent")
async def get_recent_quotes(limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Quote)
        .where(Quote.is_resolved == True)
        .where(Quote.speaker != "Error")
        .where(Quote.confidence_score > 0)
        .order_by(Quote.created_at.desc())
        .limit(limit)
    )
    quotes = result.scalars().all()

    output = []
    for q in quotes:
        sources = await get_sources_for_quote(db, q.id)
        output.append(build_quote_out(q, sources))

    return {"quotes": output}
