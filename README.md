# QuoteOrigin 🔍

> **Find the earliest known source, original phrasing, and true speaker of any quote.**

QuoteOrigin is a full-stack NLP application that traces the provenance of quotes across news, web, Wikipedia, Wikiquote, and Reddit. It uses Groq (LLaMA 3) for intelligent extraction and PostgreSQL for caching results.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 + FastAPI |
| LLM | Groq API (LLaMA 3.3 70B) — free tier |
| NLP | sentence-transformers (semantic similarity) |
| Database | PostgreSQL (Neon.tech — free tier) |
| ORM | SQLAlchemy 2.0 (async) |
| Frontend | React 18 + Vite |
| Backend Hosting | Render (free tier) |
| Frontend Hosting | Vercel (free tier) |

---

## Project Structure

```
quoteorigin/
├── backend/               # FastAPI Python app (deployed to Render)
│   ├── main.py
│   ├── config.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── crud.py
│   ├── nlp/
│   │   ├── groq_client.py
│   │   └── normalizer.py
│   ├── scrapers/
│   │   ├── wikiquote.py
│   │   ├── wikipedia.py
│   │   ├── newsapi.py
│   │   ├── brave_search.py
│   │   └── quotable.py
│   └── routers/
│       └── quotes.py
├── frontend/              # React app (deployed to Vercel)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── api/
│   └── package.json
├── .env.example
├── requirements.txt
├── render.yaml            # Render deployment config
└── README.md
```

---

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL (or a free Neon.tech account)

### 1. Clone & configure

```bash
git clone https://github.com/YOUR_USERNAME/quoteorigin.git
cd quoteorigin
cp .env.example .env
# Fill in your keys in .env
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# Create DB tables
python -c "from database.connection import init_db; import asyncio; asyncio.run(init_db())"

# Start dev server
uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev     # starts at http://localhost:5173
```

---

## Deployment

### Backend → Render
1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service → connect your repo
3. Set root directory: `backend`
4. Add all environment variables from `.env`
5. Render auto-detects `render.yaml` for settings

### Frontend → Vercel
1. Go to [vercel.com](https://vercel.com) → New Project → import your GitHub repo
2. Set root directory: `frontend`
3. Add env var: `VITE_API_URL=https://your-render-app.onrender.com`
4. Deploy

### Database → Neon.tech
1. Create free account at [neon.tech](https://neon.tech)
2. Create a new project → copy the connection string
3. Paste into `DATABASE_URL` in your `.env` and Render env vars

---

## Free API Keys Needed

| Service | Get Key At | Free Limit |
|---|---|---|
| Groq | console.groq.com | 14,400 req/day |
| NewsAPI | newsapi.org | 100 req/day |
| Brave Search | api.search.brave.com | 2,000 req/month |
| Neon (Postgres) | neon.tech | 1 project free |

Wikiquote, Wikipedia, Quotable.io — **no key needed**.

---

## Architecture Notes

- Social platform APIs (X/Twitter, TikTok, Instagram) now require paid access. QuoteOrigin is architected with a pluggable scraper interface so these can be added when available.
- Results are cached in PostgreSQL so the same quote is only looked up once.
- Groq's LLaMA 3.3 70B model performs the final attribution reasoning across all gathered sources.
