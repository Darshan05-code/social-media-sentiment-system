"""
Meta / Instagram official Graph API integration service.

Complies strictly with platform policies:
- Uses official Meta Graph API v19.0+ endpoints only
- Never uses unauthorized scraping or third-party web scrapers
- Gracefully handles missing credentials or expired user tokens
- Sanitizes comments to avoid storing sensitive user data
"""

import logging
from typing import Dict, List, Any
import requests
from django.conf import settings

from .base import BaseSocialMediaService

logger = logging.getLogger(__name__)


class InstagramService(BaseSocialMediaService):
    """Integration service for querying Instagram media and comments via Meta Graph API."""

    platform_name: str = 'instagram'
    GRAPH_API_VERSION = "v19.0"

    def is_configured(self) -> bool:
        """Checks whether official Meta/Instagram credentials are configured in settings."""
        access_token = getattr(settings, 'META_ACCESS_TOKEN', '')
        account_id = getattr(settings, 'INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
        return bool(access_token and access_token.strip() and account_id and account_id.strip())

    def get_configuration_status(self) -> Dict[str, Any]:
        """Provides status details regarding credentials."""
        configured = self.is_configured()
        return {
            "platform": "instagram",
            "configured": configured,
            "message": "Instagram integration is configured." if configured else "Instagram integration is not configured.",
            "required_env_vars": [
                "META_ACCESS_TOKEN",
                "INSTAGRAM_BUSINESS_ACCOUNT_ID",
                "INSTAGRAM_APP_ID",
                "INSTAGRAM_APP_SECRET"
            ],
            "note": "Meta Graph API requires a Meta for Developers App with instagram_basic and instagram_manage_comments permissions."
        }

    def fetch_raw_posts(self, query: str = '', count: int = 10) -> Dict[str, Any]:
        """
        Fetches media objects and public comments from the configured Instagram Business Account.
        Does not fake data if credentials are not configured or request fails.
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "Instagram integration is not configured.",
                "posts": []
            }

        access_token = getattr(settings, 'META_ACCESS_TOKEN', '').strip()
        account_id = getattr(settings, 'INSTAGRAM_BUSINESS_ACCOUNT_ID', '').strip()
        limit = max(1, min(count, 50))

        url = f"https://graph.facebook.com/{self.GRAPH_API_VERSION}/{account_id}/media"
        params = {
            "fields": "id,caption,media_type,timestamp,like_count,comments_count,comments{id,text,timestamp}",
            "limit": limit,
            "access_token": access_token
        }

        try:
            response = requests.get(url, params=params, timeout=12)

            if response.status_code == 200:
                data = response.json()
                media_list = data.get("data", [])

                normalized_posts = []
                for media in media_list:
                    caption = media.get("caption", "")
                    if caption:
                        normalized_posts.append({
                            "external_id": str(media.get("id")),
                            "text": caption,
                            "username": "",  # Privacy: username omitted unless specifically granted
                            "author_display_name": "",
                            "posted_at": media.get("timestamp"),
                            "likes_count": int(media.get("like_count", 0)),
                            "comments_count": int(media.get("comments_count", 0)),
                            "shares_count": 0,
                            "raw_metadata": {
                                "media_type": media.get("media_type")
                            }
                        })

                    # Also extract top comments on the media item if available
                    comments_data = media.get("comments", {}).get("data", [])
                    for comment in comments_data:
                        c_text = comment.get("text", "")
                        if c_text:
                            normalized_posts.append({
                                "external_id": f"comment_{comment.get('id')}",
                                "text": c_text,
                                "username": "",
                                "author_display_name": "",
                                "posted_at": comment.get("timestamp"),
                                "likes_count": 0,
                                "comments_count": 0,
                                "shares_count": 0,
                                "raw_metadata": {
                                    "parent_media_id": media.get("id")
                                }
                            })

                return {
                    "success": True,
                    "error": None,
                    "posts": normalized_posts
                }

            elif response.status_code in (400, 401):
                err_msg = response.json().get('error', {}).get('message', 'Invalid access token.')
                return {
                    "success": False,
                    "error": f"Meta Graph API authentication failed: {err_msg}",
                    "posts": []
                }
            elif response.status_code == 403:
                return {
                    "success": False,
                    "error": "Meta Graph API permission denied. Ensure token has instagram_basic permissions.",
                    "posts": []
                }
            else:
                return {
                    "success": False,
                    "error": f"Meta Graph API returned status {response.status_code}: {response.text[:200]}",
                    "posts": []
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Instagram API request timed out after 12 seconds.",
                "posts": []
            }
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Network error contacting Meta Graph API: {req_err}")
            return {
                "success": False,
                "error": f"Network error contacting Instagram/Meta API: {str(req_err)}",
                "posts": []
            }


# Global singleton instance
instagram_service = InstagramService()
