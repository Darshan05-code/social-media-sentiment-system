"""
Social media integrations package exposing service abstractions for Twitter/X and Instagram/Meta.
"""

from .base import BaseSocialMediaService
from .twitter_service import TwitterService, twitter_service
from .instagram_service import InstagramService, instagram_service

def get_social_service(platform: str) -> BaseSocialMediaService:
    """Factory helper to obtain the appropriate platform integration service."""
    normalized = (platform or '').strip().lower()
    if normalized in ('twitter', 'x'):
        return twitter_service
    elif normalized in ('instagram', 'ig'):
        return instagram_service
    else:
        raise ValueError(f"Unsupported social media platform: '{platform}'. Must be 'twitter' or 'instagram'.")

__all__ = [
    'BaseSocialMediaService',
    'TwitterService',
    'twitter_service',
    'InstagramService',
    'instagram_service',
    'get_social_service',
]
