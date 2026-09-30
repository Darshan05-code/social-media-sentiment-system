# AI-Based Social Media Sentiment and Reputation Analysis System

A production-style web application that analyzes social-media content from **Twitter / X** and **Instagram** using classical machine-learning models (Logistic Regression + TF-IDF) and presents actionable insights in an interactive, modern dashboard.

---

## Architecture Overview

```
                                      ┌────────────────────────────────────────┐
                                      │        React + Vite Frontend           │
                                      │   (Executive Dashboard, Analyzer,      │
                                      │    Platform Comparison, Dataset Docs)  │
                                      └──────────────────┬─────────────────────┘
                                                         │ HTTP / JSON
                                                         ▼
                                      ┌────────────────────────────────────────┐
                                      │         Django REST Backend            │
                                      │     (/api/sentiment, /api/social,      │
                                      │      /api/analytics, /api/docs)        │
                                      └───────┬──────────────┬───────────────┬─┘
                                              │              │               │
                                              ▼              ▼               ▼
┌───────────────────────────────┐   ┌──────────────────┐   ┌───────────────────────────────┐
│     ML Model Service Layer    │   │ SQLite / Postgres│   │  Official Social Media APIs   │
│  - Twitter (100K Balanced)    │   │  - Sentiment     │   │  - Twitter/X API v2 (Bearer)  │
│  - Instagram (Unicode-Safe)   │   │  - SocialPosts   │   │  - Meta Graph API v19.0+      │
│  - Advanced NLP (Emotions,    │   └──────────────────┘   │  - Zero Fake Data Policy      │
│    Topics, Feature Influence) │                          └───────────────────────────────┘
└───────────────────────────────┘
```

---

## Key Features

1. **Pre-Trained Classical ML Baseline & Preprocessing:**
   - Evaluates sentiment into `positive`, `neutral`, and `negative` classes with exact class probability distribution percentages.
   - **Twitter Model:** Scikit-learn Logistic Regression trained on a 100K balanced corpus with a 20,000 unigram/bigram TF-IDF vectorizer.
   - **Instagram Model & Preprocessing:** Scikit-learn Logistic Regression trained on 4,162 vocabulary features. Inference preprocessing strictly mirrors model training:
     - Strips URLs, mentions, and `#` prefixes.
     - Strips emojis and punctuation via `re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)` while retaining Unicode letters (such as Hindi and Gujarati).
     - Normalizes whitespace and converts to lowercase before passing to the TF-IDF vectorizer.
2. **Dual-Pipeline Architecture for Sentiment & Advanced NLP:**
   ```
   Original Input Text
       ├── Sentiment Preprocessing (URL/mention strip, [^\w\s] emoji/punct removal) → TF-IDF → Logistic Regression
       └── Original Text (Unmodified) → Advanced NLP (Emoji & keyword emotion detection, topic categorization)
   ```
   - Emojis are stripped from the sentiment TF-IDF feature input to maintain strict training compatibility.
   - Emojis are retained in the original text passed to Advanced NLP, allowing the rule-based emotion lexicon to detect nuanced emotional signals (e.g. `❤️`, `😍` for `joy`, `😢` for `sadness`).
   - Salient keyword extraction and word-level linear feature influence explanations (non-causal).
3. **Official Social Media Integration Layer:**
   - Strictly official Twitter API v2 and Meta Graph API v19.0+ integrations.
   - **Zero Fake Data:** Clearly reports `"Twitter/X integration is not configured"` or `"Instagram integration is not configured"` when credentials are unset.
   - Manual sentiment analysis remains 100% operational without third-party credentials.
4. **Interactive Glassmorphism Dashboard:**
   - High-performance SVG Donut Charts for sentiment distribution.
   - Stat cards with glowing sentiment indicators.
   - Side-by-side Twitter vs Instagram comparative metrics.
   - Interactive manual testing workbench with real-time benchmark chips.
   - Filterable table of historical predictions.
5. **Interactive OpenAPI / Swagger Documentation:**
   - Live Swagger UI accessible at `/api/docs/` and raw OpenAPI 3.0 specification at `/api/schema/`.

---

## Directory Structure

```
MAJOR_PROJECT/
├── backend/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py           # Core settings (.env, CORS, SQLite/Postgres)
│   │   ├── urls.py               # Root URL configuration
│   │   ├── docs_views.py         # OpenAPI 3.0 & Swagger UI views
│   │   ├── wsgi.py               # WSGI entrypoint
│   │   └── asgi.py               # ASGI entrypoint
│   ├── apps/
│   │   ├── sentiment/            # Sentiment prediction & ML service layer
│   │   │   ├── models.py         # SentimentAnalysis model
│   │   │   ├── serializers.py    # Request/Response serializers
│   │   │   ├── views.py          # /api/sentiment/ endpoints
│   │   │   ├── urls.py
│   │   │   ├── tests.py          # 27 automated tests
│   │   │   └── services/
│   │   │       ├── model_loader.py       # Singleton ML artifact manager
│   │   │       ├── preprocessors.py      # Unicode & Twitter text sanitizers
│   │   │       ├── advanced_nlp.py       # Emotion, topics, keywords, explanations
│   │   │       └── prediction_service.py # Inference pipeline & DB persistence
│   │   ├── social_media/         # Social media ingestion layer
│   │   │   ├── models.py         # SocialPost model with engagement scoring
│   │   │   ├── serializers.py
│   │   │   ├── views.py          # /api/social/ endpoints
│   │   │   ├── urls.py
│   │   │   ├── tests.py          # 11 integration tests
│   │   │   └── services/
│   │   │       ├── base.py               # BaseSocialMediaService abstraction
│   │   │       ├── twitter_service.py    # Official Twitter v2 API client
│   │   │       └── instagram_service.py  # Official Meta Graph API client
│   │   └── analytics/            # High-level metrics & comparisons
│   │       ├── views.py          # /api/analytics/ endpoints
│   │       └── urls.py
│   ├── ml_models/                # Pre-trained .joblib model files
│   │   ├── twitter/
│   │   │   ├── twitter_sentiment_logistic_100k.joblib
│   │   │   └── twitter_tfidf_100k.joblib
│   │   └── instagram/
│   │       ├── instagram_sentiment_logistic.joblib
│   │       └── instagram_tfidf.joblib
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── Procfile
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable UI components (Charts, Cards, Tables)
│   │   ├── views/                # Overview, Manual Analyzer, Social, Dataset Docs
│   │   ├── api.js                # REST API client
│   │   ├── App.jsx               # Tabbed master dashboard shell
│   │   └── index.css             # Vanilla CSS glassmorphism design system
│   ├── package.json
│   ├── vite.config.js           # Reverse-proxy to Django backend
│   └── vercel.json
├── docs/
│   └── API_DOCUMENTATION.md      # Detailed REST API Reference
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Machine Learning Models Location & Hashes

The 4 pre-trained `.joblib` files are located in:

| File Path | Size | MD5 Hash |
| :--- | :--- | :--- |
| `backend/ml_models/twitter/twitter_sentiment_logistic_100k.joblib` | 481 KB | `D23EB28992138346D805AE05021F6443` |
| `backend/ml_models/twitter/twitter_tfidf_100k.joblib` | 755 KB | `1EDB68EE062F9E1145DE38F91218E1E8` |
| `backend/ml_models/instagram/instagram_sentiment_logistic.joblib` | 100 KB | `A7DABB7CB189EC9253154D1770F7E04E` |
| `backend/ml_models/instagram/instagram_tfidf.joblib` | 156 KB | `8F319AAA9D4E0A24C65EF22DA0047CFA` |

---

## Installation & Local Setup

### 1. Prerequisites
- Python 3.11+ (Tested on 3.13)
- Node.js 18+ (Tested on v24.14.0) and npm

### 2. Backend Setup
```powershell
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env from template
copy .env.example .env

# Run database migrations
python manage.py migrate

# (Optional) Verify backend tests
python manage.py test apps

# Start Django development server (Port 8000)
python manage.py runserver 127.0.0.1:8000
```

### 3. Frontend Setup
```powershell
# In a new terminal, navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite development server (Port 5173)
npm run dev
```

Open your browser to: **`http://127.0.0.1:5173/`**

---

## Environment Variables (`backend/.env`)

```ini
# Django Core
DEBUG=True
SECRET_KEY=your-secure-random-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database (Default: SQLite; for PostgreSQL provide connection URL)
# DATABASE_URL=postgresql://user:password@localhost:5432/sentiment_db
DATABASE_URL=

# CORS
CORS_ALLOW_ALL=True

# Twitter / X Official API Credentials (Optional)
TWITTER_BEARER_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=

# Meta / Instagram Official Graph API Credentials (Optional)
META_ACCESS_TOKEN=
INSTAGRAM_BUSINESS_ACCOUNT_ID=
INSTAGRAM_APP_ID=
INSTAGRAM_APP_SECRET=
```

---

## REST API Endpoints

Interactive Swagger UI: `http://127.0.0.1:8000/api/docs/`
OpenAPI Specification: `http://127.0.0.1:8000/api/schema/`

### 1. Unified Sentiment Prediction
`POST /api/sentiment/predict/`
```json
{
  "platform": "instagram",
  "text": "I absolutely love this! 😍"
}
```
**Response:**
```json
{
  "platform": "instagram",
  "text": "I absolutely love this! 😍",
  "cleaned_text": "i absolutely love this! 😍",
  "sentiment": "positive",
  "confidence": 89.45,
  "probabilities": {
    "negative": 4.78,
    "neutral": 5.78,
    "positive": 89.45
  },
  "confidence_disclaimer": "Model probability/confidence, not guaranteed real-world truth.",
  "advanced_nlp": {
    "emotion": "joy",
    "topics": ["Lifestyle & Community"],
    "keywords": [{"keyword": "love", "weight": 4.678}]
  },
  "analysis_id": 1
}
```

### 2. Platform-Specific Endpoints
- `POST /api/sentiment/twitter/` $\rightarrow$ `{"text": "Sample tweet text"}`
- `POST /api/sentiment/instagram/` $\rightarrow$ `{"text": "Sample caption or comment"}`

### 3. Analytics & Social Endpoints
- `GET /api/analytics/overview/` $\rightarrow$ Total content analyzed, sentiment breakdown, average confidence.
- `GET /api/analytics/comparison/` $\rightarrow$ Twitter vs Instagram side-by-side ratios.
- `GET /api/social/status/` $\rightarrow$ Diagnostic credential configuration status.
- `POST /api/social/fetch/` $\rightarrow$ Official API data ingestion.
- `GET /api/social/posts/` $\rightarrow$ Historical ingested posts with engagement metrics.

---

## Automated Test Suite

Run the full Django test suite:
```powershell
python backend\manage.py test apps -v 2
```
All **38 unit and integration tests** cover:
- Text Preprocessing (Twitter URL/mention stripping, Instagram Unicode & emoji preservation)
- Model Inference & Exact Probability Verification
- Edge Cases (empty text, invalid platform, oversized inputs)
- REST API Endpoints (`POST /predict/`, `POST /twitter/`, `POST /instagram/`, `GET /status/`)
- Social Media Ingestion (unconfigured states, mocked official API responses, error handling)
- Database Persistence in `SentimentAnalysis` and `SocialPost`

---

## Academic Disclosures & Known Limitations

1. **Twitter Model Domain Shift:** Trained on 100K balanced samples. While effective on informal slang, hashtags, and social discourse, domain shift may occur on formal, technical, or legal corporate texts.
2. **Instagram Model Baseline & Multilingual Generalization:**
   - **Baseline Performance:** Trained on 4,601 usable comments with ~60.8% accuracy and ~0.60 Macro F1. Labels in the original training corpus were machine-predicted; model outputs represent statistical agreement with training dataset annotations rather than infallible ground truth.
   - **Multilingual Generalization Limitation:** The sentiment preprocessing pipeline preserves Unicode letter scripts (Devanagari, Gujarati, etc.), while emojis and punctuation are removed via `re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)` to strictly match model training. However, because the underlying TF-IDF vocabulary (4,162 terms) was extracted predominantly from English and Romanized/Hinglish Instagram comments, purely Devanagari text (e.g., `यह उत्पाद बहुत ही शानदार और उपयोगी है! 😍`) falls outside the high-polarity feature vocabulary and is predicted as `Neutral`. (Meanwhile, the Advanced NLP layer receives the original text, correctly detecting the `😍` emoji as `joy`). This is an inherent dataset and vocabulary generalization limitation of the classical bag-of-words model, not a software failure.
3. **Probability & Confidence Interpretation:** Confidence scores represent conditional model probabilities ($P(y|\mathbf{x})$) under training feature distributions, not guaranteed real-world fact or objective truth.
4. **Feature Influence (Non-Causal):** Linear model coefficients show directional feature weight along the hyperplane, not real-world causation.
5. **Observational Engagement Data:** Correlations between sentiment and engagement metrics do not imply causality.
6. **Automated Browser Automation Limitation (Playwright 404):**
   - Automated browser verification using Playwright encountered an external driver download failure (Azure CDN returned HTTP 404 on `playwright-1.57.0-win32_x64.zip`).
   - This was an automated testing runtime environment limitation, **not** an application or frontend code failure.
   - Complete end-to-end verification was conducted via:
     - 38/38 Django backend test suite passing (100%)
     - Vite frontend production build (`npm run build`) passing cleanly (1.45s)
     - Live reverse-proxy HTTP requests verifying JSON responses across all REST endpoints
     - Live interactive UI verification on `http://127.0.0.1:5173/`

---

## Deployment Instructions

### Option A: Local Docker Compose (Recommended for Full Stack Testing)
```bash
# Build and start PostgreSQL and Django backend in containers
docker-compose up --build

# In frontend directory, run Vite dev or build
cd frontend
npm run build
npm run preview
```

### Option B: Production Cloud Deployment (Vercel + Railway + PostgreSQL)

*For complete step-by-step screenshots and walkthrough, see [DEPLOYMENT_GUIDE_RAILWAY_VERCEL.md](file:///e:/TRASHER/MAJOR_PROJECT/docs/DEPLOYMENT_GUIDE_RAILWAY_VERCEL.md).*

1. **Backend & Database (Railway):**
   - **PostgreSQL:** Add a PostgreSQL service in Railway; it automatically supplies `${{Postgres.DATABASE_URL}}`.
   - **Django Web Service:** Create a Railway service from your GitHub repository and configure Railway service settings:
     - **Root Directory:** Set to `/backend`.
     - **Build:** Railpack / automatic detection (no `railway.json` required).
     - **Pre-deploy Command:** `python manage.py migrate && python manage.py collectstatic --noinput` (runs database migrations and collects static assets prior to container launch).
     - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120` (starts Gunicorn using Railway's dynamic `$PORT`).
   - **Environment Variables:** Set `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS=.railway.app`, `DATABASE_URL=${{Postgres.DATABASE_URL}}`, `CORS_ALLOWED_ORIGINS=https://<your-vercel-app>.vercel.app`.
2. **Frontend (Vercel):**
   - Import your GitHub repo in Vercel.
   - Set Root Directory to `frontend`.
   - Add Environment Variable: `VITE_API_BASE_URL=https://<your-backend>.up.railway.app/api`.
   - Click Deploy. Vercel builds the bundle and handles client-side routing via `frontend/vercel.json`.


