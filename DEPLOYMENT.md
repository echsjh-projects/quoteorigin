# Deployment Guide: GitHub → Render (backend) + Vercel (frontend)

This guide walks you through deploying QuoteOrigin from scratch.
Total time: ~30 minutes.

---

## Step 1: Set Up PostgreSQL on Neon.tech (5 min)

1. Go to https://neon.tech and sign up (free, no credit card)
2. Click **New Project** → name it `quoteorigin`
3. Choose a region close to you
4. Click **Create Project**
5. On the dashboard, click **Connection string** → select **asyncpg** format
   It looks like: `postgresql+asyncpg://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`
6. **Copy this string** — you'll need it in Steps 3 and 4

---

## Step 2: Push to GitHub (5 min)

```bash
# In the quoteorigin/ root directory:
git init
git add .
git commit -m "Initial commit: QuoteOrigin full-stack app"

# Create a new repo on github.com (name it quoteorigin, keep it public for CV)
# Then:
git remote add origin https://github.com/YOUR_USERNAME/quoteorigin.git
git branch -M main
git push -u origin main
```

> **Important:** The `.gitignore` already excludes `.env` files.
> Never commit real API keys.

---

## Step 3: Deploy Backend to Render (10 min)

1. Go to https://render.com → sign up with GitHub
2. Click **New** → **Web Service**
3. Connect your GitHub repo → select `quoteorigin`
4. Fill in the settings:
   - **Name:** `quoteorigin-api`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r ../requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free

5. Click **Environment** tab → add these variables:

   | Key | Value |
   |-----|-------|
   | `GROQ_API_KEY` | your key from console.groq.com |
   | `DATABASE_URL` | your Neon connection string from Step 1 |
   | `NEWS_API_KEY` | your key from newsapi.org (optional) |
   | `BRAVE_API_KEY` | your key from api.search.brave.com (optional) |
   | `FRONTEND_URL` | leave blank for now, add after Step 4 |
   | `ENVIRONMENT` | `production` |

6. Click **Create Web Service** → wait 3–5 minutes for the first deploy
7. Your backend URL will be: `https://quoteorigin-api.onrender.com`
8. Test it: visit `https://quoteorigin-api.onrender.com/health` → should return `{"status":"ok"}`

> **Note on Render free tier:** The service "spins down" after 15 minutes of inactivity.
> The first request after sleep takes ~30 seconds. For a CV project this is fine —
> just mention it in your README as a known limitation.

---

## Step 4: Deploy Frontend to Vercel (5 min)

1. Go to https://vercel.com → sign up with GitHub
2. Click **New Project** → import your `quoteorigin` repo
3. Fill in:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)
4. Under **Environment Variables**, add:
   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | `https://quoteorigin-api.onrender.com` |
5. Click **Deploy** → wait ~1 minute
6. Your frontend URL will be: `https://quoteorigin.vercel.app`

---

## Step 5: Connect Frontend URL to Backend (2 min)

Now that you have your Vercel URL:

1. Go back to Render → your service → **Environment**
2. Add/update: `FRONTEND_URL` = `https://quoteorigin.vercel.app`
3. Click **Save Changes** → Render will redeploy automatically

This tells the backend's CORS policy to accept requests from your Vercel domain.

---

## Step 6: Test End-to-End

1. Visit your Vercel URL
2. Type: `Blood, sweat, and tears`
3. Click **Trace Origin**
4. You should see the result card with Churchill as the speaker

If something fails:
- Check Render logs: Render dashboard → your service → **Logs**
- Check browser console (F12) for CORS or network errors
- Verify all env vars are set correctly

---

## Updating the App

```bash
# Make your changes locally, then:
git add .
git commit -m "Your change description"
git push

# Render and Vercel both auto-deploy on push to main ✅
```

---

## Free Tier Limits Summary

| Service | Limit | Impact |
|---------|-------|--------|
| Render (free) | Spins down after 15min idle | First request is slow |
| Vercel (free) | 100GB bandwidth/month | More than enough |
| Neon (free) | 0.5GB storage, 1 project | Fine for CV |
| Groq (free) | 14,400 req/day | Very generous |
| NewsAPI (free) | 100 req/day | Cache helps a lot |
| Brave Search (free) | 2,000 req/month | Cache helps a lot |
