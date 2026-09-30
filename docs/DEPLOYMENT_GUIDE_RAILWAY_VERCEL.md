# Production Deployment Guide
## Vercel (Frontend) + Railway (Django Backend & PostgreSQL)

This guide provides step-by-step instructions to deploy the **AI-Based Social Media Sentiment and Reputation Analysis System** to production using:
- **Frontend:** React + Vite on **Vercel**
- **Backend:** Django 6 REST Framework + Classical ML models on **Railway**
- **Database:** Managed **PostgreSQL** on **Railway**

---

## 1. Architecture Overview

```
┌───────────────────────────────────────┐
│     Vercel Static Hosting             │
│  - React + Vite SPA                   │
│  - Root directory: frontend           │
│  - Env: VITE_API_BASE_URL             │
└──────────────────┬────────────────────┘
                   │ HTTPS API Requests (/api/*)
                   ▼
┌───────────────────────────────────────┐         ┌───────────────────────────────────────┐
│     Railway Web Service               │         │     Railway PostgreSQL Service        │
│  - Gunicorn + Django 6 REST API       │◄───────►│  - Managed PostgreSQL 16              │
│  - Pre-trained ML Models (4 .joblib)  │         │  - Provided via ${DATABASE_URL}       │
│  - Root directory: backend            │         └───────────────────────────────────────┘
│  - WhiteNoise Static Files Serving    │
└──────────────────┬────────────────────┘
                   │ HTTPS Ingestion (Optional)
                   ▼
┌───────────────────────────────────────┐
│     Official Social Media APIs        │
│  - Twitter/X API v2 (Bearer)          │
│  - Meta Graph API v19.0+              │
└───────────────────────────────────────┘
```

---

## 2. Prerequisites
1. A [GitHub](https://github.com/) account.
2. A [Railway](https://railway.com/) account.
3. A [Vercel](https://vercel.com/) account.

---

## 3. Step 1: Push Codebase to GitHub

1. Initialize Git in the project root:
   ```bash
   git init
   ```
2. Verify untracked files are protected by `.gitignore`:
   ```bash
   git status
   ```
   *(Ensure `.env` and `db.sqlite3` are NOT staged).*
3. Stage and commit:
   ```bash
   git add .
   git commit -m "feat: complete social media sentiment analysis system ready for production"
   ```
4. Create a repository on GitHub (e.g. `social-media-sentiment-system`) and push:
   ```bash
   git remote add origin https://github.com/<your-username>/social-media-sentiment-system.git
   git branch -M main
   git push -u origin main
   ```

---

## 4. Step 2: Deploy Database & Backend on Railway

### A. Create Project & PostgreSQL Database
1. Go to [Railway Dashboard](https://railway.com/dashboard) and click **"New Project"**.
2. Select **"Provision PostgreSQL"**.
3. Railway will provision a managed PostgreSQL instance.
4. Click on the PostgreSQL card, go to the **"Variables"** tab, and observe that `DATABASE_URL` is automatically generated.

### B. Deploy Django Backend Service
1. In the same Railway project, click **"+ New"** $\rightarrow$ **"GitHub Repo"** (create Railway service from GitHub repository).
2. Select your repository: `social-media-sentiment-system`.
3. Click on the newly created service card and navigate to **"Settings"**:
   - **Service Name:** `sentiment-backend` (or your choice).
   - **Root Directory:** Set to `/backend` (required for monorepo configuration so Railway operates within the Django project).
   - **Build:** Use default **Railpack / automatic build** detection (do not depend on or require `railway.json`).
   - **Pre-deploy Command:** Under the **Deploy** section, set:
     ```bash
     python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:** Under the **Deploy** section, set:
     ```bash
     gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
     ```
     *(Uses Railway's dynamically injected `$PORT`. Migrations are executed in the separate Pre-deploy step, NOT as part of the Gunicorn start command)*.
   - **Public Networking:** Click **"Generate Domain"** under Networking to receive a public URL (e.g., `https://sentiment-backend.up.railway.app`).
4. Navigate to the **"Variables"** tab and add the required environment variables:

| Variable Name | Value / Recommended Format | Notes |
| :--- | :--- | :--- |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Use Railway's reference variable to connect to the PostgreSQL service. |
| `DEBUG` | `False` | Disables debug mode for security. |
| `SECRET_KEY` | *(Generate a 50+ char random string)* | E.g., `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `ALLOWED_HOSTS` | `.railway.app,localhost,127.0.0.1` | **Django Syntax:** Use leading dot (`.railway.app`) or exact Railway domain. Do NOT use `*.railway.app`. |
| `CORS_ALLOW_ALL` | `False` | Enforces origin whitelist in production. |
| `CORS_ALLOWED_ORIGINS` | `https://<your-vercel-app>.vercel.app` | Set to your Vercel frontend URL once created. |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app,https://*.railway.app` | Allows cross-origin REST requests from Vercel to Railway. |

### C. Build & Start Commands (Railway Service Settings)
The deployment relies entirely on Railway's standard dashboard service settings (without depending on `railway.json`):
- **Build Detection:** Railpack / automatic build detection analyzes `requirements.txt` and prepares the Python environment.
- **Pre-deploy Command:** `python manage.py migrate && python manage.py collectstatic --noinput` automatically runs database migrations and collects static assets prior to launching the container.
- **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120` starts Gunicorn with 3 workers bound to `$PORT`. Note that migrations run exclusively in the pre-deploy phase and are NOT part of the Gunicorn start command.

Once deployment finishes, open `https://<your-backend>.up.railway.app/api/health/` in your browser. You should see:
```json
{
  "status": "healthy",
  "service": "AI-Based Social Media Sentiment & Reputation Analysis API",
  "version": "1.0.0"
}
```

---

## 5. Step 3: Deploy Frontend on Vercel

1. Log in to [Vercel Dashboard](https://vercel.com/) and click **"Add New..."** $\rightarrow$ **"Project"**.
2. Select your GitHub repository: `social-media-sentiment-system`.
3. In the project configuration modal:
   - **Framework Preset:** `Vite`
   - **Root Directory:** Click **Edit** and select `frontend`.
   - **Build Command:** `npm run build` (default).
   - **Output Directory:** `dist` (default).
4. Expand **"Environment Variables"** and add:

| Variable Name | Value | Description |
| :--- | :--- | :--- |
| `VITE_API_BASE_URL` | `https://<your-backend>.up.railway.app/api` | Absolute URL to the Railway Django backend API. |

5. Click **"Deploy"**.
6. Vercel will build the frontend bundle. When complete, you will receive a production URL (e.g., `https://social-sentiment-analyzer.vercel.app`).

### D. Link Frontend Domain in Railway CORS
Copy your Vercel domain (e.g. `https://social-sentiment-analyzer.vercel.app`), go back to your Railway `sentiment-backend` service $\rightarrow$ **Variables**, and update:
```ini
CORS_ALLOWED_ORIGINS=https://social-sentiment-analyzer.vercel.app
```
Railway will automatically redeploy the backend with the updated CORS rule in ~15 seconds.

---

## 6. Required Environment Variables Reference

| Variable | Purpose | Where It Belongs | Example Format |
| :--- | :--- | :---: | :--- |
| `DEBUG` | Django debug toggle (must be False in prod) | Railway Backend | `False` |
| `SECRET_KEY` | Django cryptographic signing key | Railway Backend | `prod-sec-k9$2mP#8vL1...` |
| `ALLOWED_HOSTS` | Whitelisted HTTP Host headers | Railway Backend | `sentiment-backend.up.railway.app,.railway.app` |
| `DATABASE_URL` | PostgreSQL connection string | Railway Backend | `postgresql://user:pass@host:5432/railway` or `${{Postgres.DATABASE_URL}}` |
| `CORS_ALLOW_ALL` | Disables open wildcard CORS | Railway Backend | `False` |
| `CORS_ALLOWED_ORIGINS` | Whitelists frontend URL for browser fetch | Railway Backend | `https://social-sentiment.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | Whitelists cross-origin requests | Railway Backend | `https://*.vercel.app,https://*.railway.app` |
| `VITE_API_BASE_URL` | Points frontend API client to Railway backend | Vercel Frontend | `https://sentiment-backend.up.railway.app/api` |
| `TWITTER_BEARER_TOKEN` | (Optional) Twitter API v2 live search | Railway Backend | `AAAAAAAAAAAAAAAAAAAAA...` |
| `META_ACCESS_TOKEN` | (Optional) Meta Graph API live media/comments | Railway Backend | `EAABwz...` |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | (Optional) Instagram professional ID | Railway Backend | `17841400000000000` |

---

## 7. Post-Deployment Verification Checklist

1. **Backend Health Check:**
   `curl https://<your-railway-app>.up.railway.app/api/health/`
   Returns HTTP 200 with status `"healthy"`.
2. **OpenAPI Interactive Documentation:**
   Open `https://<your-railway-app>.up.railway.app/api/docs/` in browser to verify Swagger UI renders static CSS/JS cleanly via WhiteNoise.
3. **Frontend Connection Check:**
   Open your Vercel URL `https://<your-vercel-app>.vercel.app`.
   Verify the header displays **"Backend API Connected"** with a green indicator.
4. **Manual Sentiment Prediction Workbench:**
   Submit `"I absolutely love this! 😍"` under Instagram.
   Verify that:
   - Sentiment is `positive` (~89.45% confidence)
   - Probabilities display negative: 4.78%, neutral: 5.78%, positive: 89.45%
   - Emotion badge shows `joy`
5. **Database Persistence:**
   Refresh the Overview Dashboard tab and verify the new prediction is recorded in the recent analyses table.
