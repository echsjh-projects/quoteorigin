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
import re

settings = get_settings()

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

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def init_db():
    from database.models import Quote, Source, SearchLog  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created.")


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
