"""
Twitter / X official API v2 integration service.

Complies strictly with platform policies:
- Uses official Twitter API v2 endpoints only
- Never scrapes unauthorized HTML
- Gracefully handles missing credentials
- Sanitizes metadata to avoid storing private personal data
"""

import logging
from typing import Dict, List, Any
import requests
from django.conf import settings

from .base import BaseSocialMediaService

logger = logging.getLogger(__name__)


class TwitterService(BaseSocialMediaService):
    """Integration service for querying Twitter/X posts via official API v2."""

    platform_name: str = 'twitter'
    TWITTER_SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

    def is_configured(self) -> bool:
        """Checks whether official Twitter API credentials are present."""
        bearer_token = getattr(settings, 'TWITTER_BEARER_TOKEN', '')
        api_key = getattr(settings, 'TWITTER_API_KEY', '')
        api_secret = getattr(settings, 'TWITTER_API_SECRET', '')

        # Bearer token is standard for v2 Recent Search
        if bearer_token and bearer_token.strip():
            return True
        if api_key and api_key.strip() and api_secret and api_secret.strip():
            return True
        return False

    def get_configuration_status(self) -> Dict[str, Any]:
        """Provides status details regarding credentials."""
        configured = self.is_configured()
        return {
            "platform": "twitter",
            "configured": configured,
            "message": "Twitter/X integration is configured." if configured else "Twitter/X integration is not configured.",
            "required_env_vars": [
                "TWITTER_BEARER_TOKEN",
                "TWITTER_API_KEY",
                "TWITTER_API_SECRET"
            ],
            "note": "Twitter/X API v2 requires an active Developer Portal account and a valid Bearer Token."
        }

    def fetch_raw_posts(self, query: str = '', count: int = 10) -> Dict[str, Any]:
        """
        Fetches public tweets matching the query using Twitter API v2.
        Does not fake data if credentials are not configured or request fails.
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "Twitter/X integration is not configured.",
                "posts": []
            }

        search_query = (query or '').strip()
        if not search_query:
            search_query = "AI OR technology"

        # Twitter API v2 enforces count between 10 and 100
        limit = max(10, min(count, 100))

        bearer_token = getattr(settings, 'TWITTER_BEARER_TOKEN', '').strip()
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "AI-Sentiment-Reputation-Analyzer/1.0"
        }

        params = {
            "query": f"{search_query} -is:retweet lang:en",
            "max_results": limit,
            "tweet.fields": "created_at,public_metrics,lang",
            "expansions": "author_id",
            "user.fields": "username,name",
        }

        try:
            response = requests.get(
                self.TWITTER_SEARCH_URL,
                headers=headers,
                params=params,
                timeout=12
            )

            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}

                normalized_posts = []
                for tweet in tweets:
                    author_id = tweet.get("author_id")
                    author = users.get(author_id, {})
                    metrics = tweet.get("public_metrics", {})

                    normalized_posts.append({
                        "external_id": str(tweet.get("id")),
                        "text": tweet.get("text", ""),
                        "username": author.get("username", "")[:150],
                        "author_display_name": author.get("name", "")[:200],
                        "posted_at": tweet.get("created_at"),
                        "likes_count": metrics.get("like_count", 0),
                        "comments_count": metrics.get("reply_count", 0),
                        "shares_count": metrics.get("retweet_count", 0),
                        "raw_metadata": {
                            "lang": tweet.get("lang"),
                            "impression_count": metrics.get("impression_count", 0)
                        }
                    })

                return {
                    "success": True,
                    "error": None,
                    "posts": normalized_posts
                }

            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Twitter API authentication failed. Please verify TWITTER_BEARER_TOKEN.",
                    "posts": []
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "Twitter API access forbidden. Ensure your developer account has v2 search permissions.",
                    "posts": []
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "Twitter API rate limit reached. Please wait before retrying.",
                    "posts": []
                }
            else:
                return {
                    "success": False,
                    "error": f"Twitter API returned status {response.status_code}: {response.text[:200]}",
                    "posts": []
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Twitter API request timed out after 12 seconds.",
                "posts": []
            }
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Network error contacting Twitter API: {req_err}")
            return {
                "success": False,
                "error": f"Network error contacting Twitter API: {str(req_err)}",
                "posts": []
            }


# Global singleton instance
twitter_service = TwitterService()
