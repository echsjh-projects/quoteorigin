"""
database/connection.py
----------------------
Sets up the async SQLAlchemy engine and session factory.

PostgreSQL primer:
  - engine    = the connection pool (one per app, reused across requests)
  - session   = a single unit of work (one per request, then closed)
  - AsyncSession is the async version — it uses `await` for all DB calls

Neon.tech SSL note:
  Neon requires SSL. The connection string from Neon already includes
  ?sslmode=require or ?ssl=require. asyncpg handles this automatically.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import get_settings

settings = get_settings()

# Create the async engine (connection pool)
# pool_pre_ping=True: test connections before use (important for Neon's idle timeout)
import re

db_url = settings.database_url
db_url = re.sub(r'[?&]sslmode=\w+', '', db_url)

engine = create_async_engine(
    db_url,
    echo=(settings.environment == "development"),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={"ssl": "require"},
)

# Session factory — call this to get a session object
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """All SQLAlchemy models inherit from this."""
    pass


async def init_db():
    """Create all tables. Run once on first deploy."""
    from database.models import Quote, Source, SearchLog  # noqa: F401 — needed for Base to see them
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created.")


async def get_db():
    """
    FastAPI dependency — injects a DB session into route handlers.
    Usage in a route:
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    The 'async with' ensures the session is always closed after the request.
    """
    async with AsyncSessionLocal() as session:
        yield session
