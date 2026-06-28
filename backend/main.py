"""
main.py
-------
FastAPI application entry point.
Render runs this file via: uvicorn main:app --host 0.0.0.0 --port $PORT
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from database.connection import init_db
from routers.quotes import router as quotes_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup and shutdown."""
    # Startup: create DB tables if they don't exist yet
    await init_db()
    yield
    # Shutdown: nothing to clean up (connection pool handles itself)


app = FastAPI(
    title="QuoteOrigin API",
    description="Trace the true origin and earliest source of any quote.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# This tells the backend to accept requests from your frontend domains.
# Without this, the browser will block requests from Vercel to Render.
allowed_origins = [
    "http://localhost:5173",       # Vite local dev
    "http://localhost:3000",       # fallback
    settings.frontend_url,        # your Vercel URL (from .env)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(quotes_router)


# ── Health check ─────────────────────────────────────────────────────────────
# Render pings /health to know the service is running
@app.get("/health")
async def health():
    return {"status": "ok", "service": "QuoteOrigin API"}


@app.get("/")
async def root():
    return {
        "message": "QuoteOrigin API",
        "docs": "/docs",
        "health": "/health",
    }
