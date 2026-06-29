"""
database/crud.py
----------------
CRUD = Create, Read, Update, Delete
All database read/write logic lives here, keeping routes clean.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from database.models import Quote, Source, SearchLog
from nlp.normalizer import normalize_quote


async def get_quote_by_text(db: AsyncSession, raw_text: str) -> Quote | None:
    normalized = normalize_quote(raw_text)
    result = await db.execute(
        select(Quote).where(Quote.normalized_text == normalized)
    )
    return result.scalar_one_or_none()


async def save_quote(
    db: AsyncSession,
    input_text: str,
    provenance: dict,
    sources: list[dict],
) -> Quote:
    normalized = normalize_quote(input_text)

    quote = Quote(
        normalized_text=normalized,
        input_text=input_text,
        original_phrasing=provenance.get("original_phrasing"),
        speaker=provenance.get("speaker"),
        earliest_date=provenance.get("earliest_date"),
        confidence_score=provenance.get("confidence"),
        reasoning=provenance.get("reasoning"),
        is_resolved=True,
    )
    db.add(quote)
    await db.flush()

    for s in sources:
        source = Source(
            quote_id=quote.id,
            platform=s.get("platform", "unknown"),
            title=s.get("title"),
            url=s.get("url"),
            snippet=s.get("snippet"),
            mentioned_date=s.get("mentioned_date"),
            speaker_mentioned=s.get("speaker_mentioned"),
            relevance=s.get("relevance"),
        )
        db.add(source)

    await db.commit()

    # Re-fetch with sources using a fresh query
    result = await db.execute(
        select(Quote).where(Quote.id == quote.id)
    )
    quote = result.scalar_one()
    
    source_result = await db.execute(
        select(Source).where(Source.quote_id == quote.id)
    )
    quote.sources = source_result.scalars().all()
    
    return quote


async def log_search(
    db: AsyncSession,
    input_text: str,
    cache_hit: bool,
    sources_found: int,
    duration_ms: int,
):
    log = SearchLog(
        input_text=input_text,
        cache_hit=cache_hit,
        sources_found=sources_found,
        duration_ms=duration_ms,
    )
    db.add(log)
    await db.commit()
