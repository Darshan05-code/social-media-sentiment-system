"""
Base abstraction for social media integration services.
Provides unified ingestion, sentiment analysis pipeline integration, and configuration checks.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging

from apps.sentiment.services import predict_sentiment
from apps.social_media.models import SocialPost

logger = logging.getLogger(__name__)


class BaseSocialMediaService(ABC):
    """Abstract base class for third-party social media integrations."""

    platform_name: str = 'base'

    @abstractmethod
    def is_configured(self) -> bool:
        """Returns True only if all required API keys/tokens are non-empty in settings."""
        pass

    @abstractmethod
    def get_configuration_status(self) -> Dict[str, Any]:
        """Returns diagnostic details regarding credential availability."""
        pass

    @abstractmethod
    def fetch_raw_posts(self, query: str = '', count: int = 10) -> Dict[str, Any]:
        """
        Fetches raw post/comment objects from the platform API.
        Must return a dict:
        {
            "success": bool,
            "error": Optional[str],
            "posts": List[Dict[str, Any]]  # Normalized post dicts
        }
        """
        pass

    def ingest_and_analyze(
        self,
        query: str = '',
        count: int = 10,
        save_to_db: bool = True
    ) -> Dict[str, Any]:
        """
        Orchestrates safe ingestion and analysis:
        1. Checks whether credentials exist.
        2. If not configured, gracefully returns without faking data.
        3. Invokes the official platform fetcher.
        4. Processes each post through the Phase 2 sentiment model.
        5. Persists both the SentimentAnalysis and SocialPost database models.
        """
        if not self.is_configured():
            status_info = self.get_configuration_status()
            return {
                "platform": self.platform_name,
                "configured": False,
                "status": "not_configured",
                "message": status_info.get("message", f"{self.platform_name.capitalize()} integration is not configured."),
                "required_env_vars": status_info.get("required_env_vars", []),
                "count": 0,
                "results": []
            }

        fetch_result = self.fetch_raw_posts(query=query, count=count)
        if not fetch_result.get("success", False):
            return {
                "platform": self.platform_name,
                "configured": True,
                "status": "api_error",
                "error": fetch_result.get("error", "Unknown API error"),
                "count": 0,
                "results": []
            }

        raw_posts = fetch_result.get("posts", [])
        if not raw_posts:
            return {
                "platform": self.platform_name,
                "configured": True,
                "status": "empty",
                "message": f"No {self.platform_name} posts found matching query '{query}'.",
                "count": 0,
                "results": []
            }

        processed_items = []
        for post in raw_posts:
            text = post.get('text', '').strip()
            if not text:
                continue

            try:
                # Process via Phase 2 ML Service Layer
                analysis_res = predict_sentiment(
                    platform=self.platform_name,
                    text=text,
                    save_to_db=save_to_db,
                    run_advanced_nlp=True
                )

                social_post_id = None
                if save_to_db:
                    # Update or create SocialPost record
                    sentiment_analysis_id = analysis_res.get('analysis_id')
                    social_record, _ = SocialPost.objects.update_or_create(
                        platform=self.platform_name,
                        external_id=str(post.get('external_id', '')),
                        defaults={
                            'username': post.get('username', '')[:150],
                            'author_display_name': post.get('author_display_name', '')[:200],
                            'text': text,
                            'likes_count': int(post.get('likes_count', 0)),
                            'comments_count': int(post.get('comments_count', 0)),
                            'shares_count': int(post.get('shares_count', 0)),
                            'sentiment': analysis_res.get('sentiment'),
                            'sentiment_score': analysis_res.get('confidence'),
                            'posted_at': post.get('posted_at'),
                            'raw_metadata': post.get('raw_metadata', {}),
                            'sentiment_analysis_id': sentiment_analysis_id,
                        }
                    )
                    social_post_id = social_record.id

                processed_items.append({
                    "social_post_id": social_post_id,
                    "external_id": post.get('external_id'),
                    "username": post.get('username'),
                    "text": text,
                    "likes_count": post.get('likes_count', 0),
                    "comments_count": post.get('comments_count', 0),
                    "shares_count": post.get('shares_count', 0),
                    "engagement_score": float(
                        post.get('likes_count', 0) +
                        (post.get('comments_count', 0) * 2) +
                        (post.get('shares_count', 0) * 3)
                    ),
                    "posted_at": post.get('posted_at'),
                    "sentiment": analysis_res.get('sentiment'),
                    "confidence": analysis_res.get('confidence'),
                    "probabilities": analysis_res.get('probabilities'),
                    "advanced_nlp": analysis_res.get('advanced_nlp'),
                })

            except Exception as proc_err:
                logger.error(f"Error processing social post: {proc_err}", exc_info=True)

        return {
            "platform": self.platform_name,
            "configured": True,
            "status": "success",
            "count": len(processed_items),
            "results": processed_items
        }
