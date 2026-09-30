"""
Interactive Swagger UI and OpenAPI 3.0 specification views for the API.
"""

from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "AI-Based Social Media Sentiment & Reputation Analysis API",
        "version": "1.0.0",
        "description": "Production REST API for analyzing sentiment on Twitter/X and Instagram using pre-trained Logistic Regression and TF-IDF models with advanced NLP emotion detection and keyword extraction.",
        "contact": {
            "name": "Major Academic Project Research Team"
        }
    },
    "servers": [
        {
            "url": "http://127.0.0.1:8000",
            "description": "Local Development Server"
        }
    ],
    "paths": {
        "/api/health/": {
            "get": {
                "summary": "System Health Check",
                "description": "Returns operational status of the API services.",
                "responses": {
                    "200": {
                        "description": "API is operational",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "healthy",
                                    "service": "AI-Based Social Media Sentiment & Reputation Analysis API",
                                    "version": "1.0.0"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/sentiment/predict/": {
            "post": {
                "summary": "Unified Sentiment Prediction",
                "description": "Classifies sentiment for a given text snippet for either Twitter or Instagram using pre-trained Logistic Regression models.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["platform", "text"],
                                "properties": {
                                    "platform": {
                                        "type": "string",
                                        "enum": ["twitter", "instagram"],
                                        "example": "instagram"
                                    },
                                    "text": {
                                        "type": "string",
                                        "example": "I absolutely love this! 😍"
                                    },
                                    "save_to_db": {
                                        "type": "boolean",
                                        "default": True
                                    },
                                    "run_advanced_nlp": {
                                        "type": "boolean",
                                        "default": True
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Prediction evaluated successfully",
                        "content": {
                            "application/json": {
                                "example": {
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
                                        "keywords": [{"keyword": "love", "weight": 4.678}],
                                        "feature_importance": [
                                            {"token": "love", "influence": 3.15, "direction": "positive_contribution"}
                                        ],
                                        "explanation_disclaimer": "Word influence indicates contribution to the linear model decision boundary. Not a causal explanation."
                                    },
                                    "analysis_id": 12
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Validation error (empty text, invalid platform, or length > 5000 chars)"
                    },
                    "503": {
                        "description": "Model files missing or unavailable"
                    }
                }
            }
        },
        "/api/sentiment/twitter/": {
            "post": {
                "summary": "Twitter/X Sentiment Prediction",
                "description": "Classifies sentiment using the 100K-trained Twitter Logistic Regression model and TF-IDF vectorizer.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["text"],
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "example": "Great team accomplishment today! Really proud of our progress. #win"
                                    },
                                    "save_to_db": {
                                        "type": "boolean",
                                        "default": True
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Sentiment evaluated successfully"},
                    "400": {"description": "Empty text or text too long"},
                    "503": {"description": "Model unavailable"}
                }
            }
        },
        "/api/sentiment/instagram/": {
            "post": {
                "summary": "Instagram Sentiment Prediction",
                "description": "Classifies sentiment using the Unicode-safe Instagram Logistic Regression model (preserving emojis, Hindi, Gujarati).",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["text"],
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "example": "I absolutely love this! 😍"
                                    },
                                    "save_to_db": {
                                        "type": "boolean",
                                        "default": True
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Sentiment evaluated successfully"},
                    "400": {"description": "Empty text or text too long"},
                    "503": {"description": "Model unavailable"}
                }
            }
        },
        "/api/sentiment/": {
            "get": {
                "summary": "List Recent Sentiment Analyses",
                "description": "Returns a paginated list of historical sentiment records.",
                "parameters": [
                    {"name": "platform", "in": "query", "schema": {"type": "string"}},
                    {"name": "sentiment", "in": "query", "schema": {"type": "string"}},
                    {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 50}}
                ],
                "responses": {
                    "200": {"description": "List of analysis records"}
                }
            }
        },
        "/api/social/status/": {
            "get": {
                "summary": "Social Media Credential & Service Status",
                "description": "Checks whether Twitter/X and Instagram/Meta credentials are configured, returning clear status messages without leaking secrets.",
                "responses": {
                    "200": {
                        "description": "Integration status object",
                        "content": {
                            "application/json": {
                                "example": {
                                    "twitter": {
                                        "platform": "twitter",
                                        "configured": False,
                                        "message": "Twitter/X integration is not configured."
                                    },
                                    "instagram": {
                                        "platform": "instagram",
                                        "configured": False,
                                        "message": "Instagram integration is not configured."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/social/fetch/": {
            "post": {
                "summary": "Fetch and Ingest Social Media Content",
                "description": "Calls official platform APIs to retrieve permitted public posts/comments, runs them through the sentiment model, and stores results.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["platform"],
                                "properties": {
                                    "platform": {"type": "string", "enum": ["twitter", "instagram"]},
                                    "query": {"type": "string", "example": "artificial intelligence"},
                                    "count": {"type": "integer", "default": 10}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Ingestion results or clear unconfigured status"}
                }
            }
        },
        "/api/analytics/overview/": {
            "get": {
                "summary": "Dashboard Aggregate Overview",
                "description": "Returns aggregate totals, positive/neutral/negative counts and percentages, and average confidence.",
                "responses": {
                    "200": {"description": "Aggregate statistics object"}
                }
            }
        },
        "/api/analytics/comparison/": {
            "get": {
                "summary": "Platform Comparative Metrics",
                "description": "Compares Twitter vs Instagram sentiment distribution side-by-side with non-causal methodology notes.",
                "responses": {
                    "200": {"description": "Platform comparison object"}
                }
            }
        }
    }
}


class OpenAPISchemaView(APIView):
    """Returns OpenAPI 3.0 specification in JSON format."""
    permission_classes = [AllowAny]

    def get(self, request):
        return JsonResponse(OPENAPI_SPEC, safe=False)


class SwaggerUIDocView(APIView):
    """Renders interactive Swagger UI using the OpenAPI 3.0 schema."""
    permission_classes = [AllowAny]

    def get(self, request):
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>API Documentation - Sentiment & Reputation Analysis</title>
  <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@5/favicon-32x32.png" sizes="32x32" />
  <style>
    body { margin: 0; padding: 0; background: #0f172a; color: #f8fafc; font-family: sans-serif; }
    .topbar { display: none; }
    .swagger-ui { filter: invert(88%) hue-rotate(180deg); }
    .swagger-ui .highlight-code { filter: invert(100%) hue-rotate(180deg); }
    .header-bar {
      padding: 18px 24px;
      background: #1e293b;
      border-bottom: 1px solid #334155;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .header-title { font-size: 1.15rem; font-weight: 700; color: #38bdf8; }
    .badge { background: #3b82f6; color: white; padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
  </style>
</head>
<body>
  <div class="header-bar">
    <div class="header-title">AI-Based Social Media Sentiment & Reputation Analysis API</div>
    <div class="badge">OpenAPI 3.0 Interactive Docs</div>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "/api/schema/",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
"""
        return HttpResponse(html_content, content_type="text/html")
