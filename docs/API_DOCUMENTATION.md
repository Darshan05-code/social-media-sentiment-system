# API Documentation
## AI-Based Social Media Sentiment & Reputation Analysis System

Base URL: `http://127.0.0.1:8000/api`

Interactive Swagger UI: `http://127.0.0.1:8000/api/docs/`
OpenAPI 3.0 Schema: `http://127.0.0.1:8000/api/schema/`

---

### Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health/` | Service health status |
| `POST` | `/sentiment/predict/` | Unified sentiment prediction (Twitter / Instagram) |
| `POST` | `/sentiment/twitter/` | Twitter-specific sentiment prediction |
| `POST` | `/sentiment/instagram/` | Instagram-specific sentiment prediction (Unicode-safe) |
| `GET` | `/sentiment/` | Paginated list of recent sentiment analysis records |
| `GET` | `/sentiment/<id>/` | Detailed record by ID |
| `DELETE` | `/sentiment/<id>/` | Delete sentiment record by ID |
| `GET` | `/analytics/overview/` | Aggregate metrics, sentiment distribution, confidence |
| `GET` | `/analytics/comparison/` | Twitter vs Instagram comparative statistics |

---

### 1. Unified Sentiment Prediction
`POST /api/sentiment/predict/`

Analyzes sentiment for either Twitter or Instagram using pre-trained Logistic Regression and TF-IDF models, returning class probabilities and advanced NLP attributes.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Body
```json
{
  "platform": "instagram",
  "text": "I absolutely love this! 😍",
  "save_to_db": true,
  "run_advanced_nlp": true
}
```

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `platform` | `string` | **Yes** | Target platform (`"twitter"` or `"instagram"`). |
| `text` | `string` | **Yes** | Text to evaluate (1 to 5,000 characters). Cannot be empty or whitespace. |
| `save_to_db` | `boolean` | No | Whether to persist record into `SentimentAnalysis` table (default: `true`). |
| `run_advanced_nlp` | `boolean` | No | Whether to compute emotions, topics, and feature influence (default: `true`). |

#### Response (`200 OK`)
```json
{
  "platform": "instagram",
  "text": "I absolutely love this! 😍",
  "cleaned_text": "i absolutely love this",
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
    "emotion_scores": {
      "joy": 0.9381,
      "sadness": 0.0103,
      "anger": 0.0103,
      "fear": 0.0103,
      "surprise": 0.0103,
      "disgust": 0.0103,
      "neutral": 0.0103
    },
    "topics": ["Lifestyle & Community"],
    "keywords": [
      {"keyword": "love", "weight": 4.678},
      {"keyword": "absolutely", "weight": 1.0}
    ],
    "feature_importance": [
      {"token": "love", "influence": 3.15, "direction": "positive_contribution"},
      {"token": "love this", "influence": 0.3558, "direction": "positive_contribution"},
      {"token": "this", "influence": 0.1748, "direction": "positive_contribution"}
    ],
    "explanation_disclaimer": "Word influence indicates contribution to the linear model decision boundary. Not a causal explanation."
  },
  "analysis_id": 1
}
```

---

### 2. Twitter-Specific Prediction
`POST /api/sentiment/twitter/`

Uses the 100K balanced Twitter Logistic Regression model and TF-IDF vectorizer.

#### Request Body
```json
{
  "text": "Great work team! Really proud of our progress today. #win",
  "save_to_db": true
}
```

#### Response (`200 OK`)
```json
{
  "platform": "twitter",
  "text": "Great work team! Really proud of our progress today. #win",
  "cleaned_text": "great work team! really proud of our progress today. win",
  "sentiment": "positive",
  "confidence": 98.74,
  "probabilities": {
    "negative": 0.82,
    "neutral": 0.44,
    "positive": 98.74
  },
  "confidence_disclaimer": "Model probability/confidence, not guaranteed real-world truth.",
  "advanced_nlp": { ... },
  "analysis_id": 2
}
```

---

### 3. Instagram-Specific Prediction
`POST /api/sentiment/instagram/`

Processes text using the Unicode-safe Instagram Logistic Regression model. Multilingual Indic characters (Hindi, Gujarati, etc.) are preserved, while emojis and punctuation are stripped before TF-IDF feature extraction to strictly mirror model training.

> **Note on Multilingual & Emoji Inference (Dual Pipeline):**
> The sentiment preprocessing pipeline strictly follows model training by applying `re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)`. This preserves Unicode language characters (including Hindi and Gujarati) while stripping emojis and punctuation before TF-IDF feature extraction. Simultaneously, the Advanced NLP layer receives the **original unmodified text**, allowing the emotion classifier to evaluate emojis (`❤️`, `😍`, etc.). If non-Romanized Indic words fall outside the pre-trained 4,162 TF-IDF vocabulary, the Logistic Regression baseline gracefully predicts according to the class prior intercept distribution (yielding `neutral` ~40.94%).

#### Request Body (Multilingual Example)
```json
{
  "text": "ખૂબ સરસ કામ! बहुत बढ़િયા काम ❤️👏",
  "save_to_db": true
}
```

#### Response (`200 OK`)
```json
{
  "platform": "instagram",
  "text": "ખૂબ સરસ કામ! बहुत बढ़િયા काम ❤️👏",
  "cleaned_text": "ખ બ સરસ बह त अच छ क म",
  "sentiment": "neutral",
  "confidence": 40.94,
  "probabilities": {
    "negative": 26.12,
    "neutral": 40.94,
    "positive": 32.94
  },
  "confidence_disclaimer": "Model probability/confidence, not guaranteed real-world truth.",
  "advanced_nlp": {
    "emotion": "joy",
    "topics": ["General Discussion"],
    "keywords": [{"keyword": "સરસ", "weight": 1.0}],
    ...
  },
  "analysis_id": 3
}
```

---

### 4. Error Responses

#### `400 Bad Request` — Validation Error
* **Empty text:**
  ```json
  {
    "error": "Validation failed",
    "details": {
      "text": ["Text cannot be empty."]
    }
  }
  ```
* **Invalid platform:**
  ```json
  {
    "error": "Validation failed",
    "details": {
      "platform": ["\"facebook\" is not a valid choice."]
    }
  }
  ```
* **Text too long (>5,000 characters):**
  ```json
  {
    "error": "Validation failed",
    "details": {
      "text": ["Text exceeds maximum allowed length of 5000 characters."]
    }
  }
  ```

#### `503 Service Unavailable` — Model Artifacts Missing
```json
{
  "error": "Sentiment model is unavailable."
}
```

---

### 5. Social Media Ingestion Endpoints

#### Check Integration Status
`GET /api/social/status/`

Returns the diagnostic status of official Twitter and Meta API credentials without throwing 500 errors.

**Response (`200 OK`):**
```json
{
  "twitter": {
    "platform": "twitter",
    "configured": false,
    "message": "Twitter/X integration is not configured. Set TWITTER_BEARER_TOKEN in environment to enable live fetching."
  },
  "instagram": {
    "platform": "instagram",
    "configured": false,
    "message": "Instagram integration is not configured. Set META_ACCESS_TOKEN and INSTAGRAM_BUSINESS_ACCOUNT_ID in environment to enable live fetching."
  }
}
```

#### Fetch Social Content
`POST /api/social/fetch/`

Ingests live posts or comments via official APIs and analyzes them through the ML sentiment service. Never uses web scraping or returns fake mock data.

**Request Body:**
```json
{
  "platform": "twitter",
  "query": "#AI",
  "max_results": 10
}
```

**Unconfigured Response (`200 OK`):**
```json
{
  "platform": "twitter",
  "configured": false,
  "status": "not_configured",
  "message": "Twitter/X integration is not configured. Set TWITTER_BEARER_TOKEN in environment to enable live fetching."
}
```

#### List Ingested Social Posts
`GET /api/social/posts/`

Retrieves previously ingested posts and comments with sentiment scores and composite engagement metrics.

---

### 6. Analytics Endpoints

#### Dashboard Overview
`GET /api/analytics/overview/`

Returns system-wide aggregated sentiment counts, percentages, and average confidence scores across all analyzed content.

#### Platform Comparison
`GET /api/analytics/comparison/`

Returns side-by-side sentiment distributions between Twitter and Instagram, along with academic methodology disclaimers regarding observational cross-platform comparisons.

