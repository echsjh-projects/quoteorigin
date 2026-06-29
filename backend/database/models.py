"""
database/models.py
------------------
SQLAlchemy ORM models = Python classes that map to PostgreSQL tables.

Each class attribute with Column(...) becomes a column in the table.
SQLAlchemy translates Python operations into SQL automatically.

Example:
  Python:  await db.execute(select(Quote).where(Quote.id == 1))
  SQL:     SELECT * FROM quotes WHERE id = 1;
"""

from sqlalchemy import (
    Column, Integer, String, Text, Float,
    DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.connection import Base


def utcnow():
    return datetime.now(timezone.utc)


class Quote(Base):
    """
    Stores a unique quote and its resolved provenance.
    One Quote has many Sources (the web pages where it was found).
    """
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    # The input text, normalized (lowercased, punctuation stripped) for deduplication
    normalized_text = Column(Text, unique=True, nullable=False, index=True)
    # The raw text the user typed
    input_text = Column(Text, nullable=False)
    # Best guess at original phrasing from LLM analysis
    original_phrasing = Column(Text, nullable=True)
    speaker = Column(String(512), nullable=True)
    # Earliest date found — stored as a string because it may be just "1940" or "circa 1850"
    earliest_date = Column(String(100), nullable=True)
    # 0.0–1.0: how confident is the LLM in this attribution?
    confidence_score = Column(Float, nullable=True)
    # LLM's explanation of why it reached this conclusion
    reasoning = Column(Text, nullable=True)
    # Has this quote been fully researched, or just cached partial?
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationship: access quote.sources to get all Source rows for this quote
    #sources = relationship("Source", back_populates="quote", cascade="all, delete-orphan")
    #sources = relationship("Source", back_populates="quote", cascade="all, delete-orphan", lazy="raise")

class Source(Base):
    """
    A single web source where a quote (or variant of it) was found.
    Many Sources belong to one Quote.
    """
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    # Foreign key links this row to a row in the quotes table
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False, index=True)
    url = Column(Text, nullable=True)
    platform = Column(String(50), nullable=False)  # "wikiquote", "newsapi", "brave", etc.
    title = Column(Text, nullable=True)
    snippet = Column(Text, nullable=True)
    # Date this source was published / the quote was mentioned (may be null if unknown)
    mentioned_date = Column(String(100), nullable=True)
    speaker_mentioned = Column(String(512), nullable=True)
    # Relevance score from the scraper or LLM (0–1)
    relevance = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)

    #quote = relationship("Quote", back_populates="sources")


class SearchLog(Base):
    """
    Logs every search request. Useful for analytics and debugging.
    Does NOT store the full result — just the fact that a search happened.
    """
    __tablename__ = "search_logs"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    # Did we serve this from cache, or did we do a fresh search?
    cache_hit = Column(Boolean, default=False)
    # How many sources did we find?
    sources_found = Column(Integer, default=0)
    # How long did the full search take in milliseconds?
    duration_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)
