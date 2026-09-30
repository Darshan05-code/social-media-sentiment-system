"""
Serializers for SocialPost model and fetch requests.
"""

from rest_framework import serializers
from .models import SocialPost


class SocialPostSerializer(serializers.ModelSerializer):
    """Serializer for persisted social media posts."""
    class Meta:
        model = SocialPost
        fields = [
            'id',
            'platform',
            'external_id',
            'username',
            'author_display_name',
            'text',
            'likes_count',
            'comments_count',
            'shares_count',
            'engagement_score',
            'sentiment',
            'sentiment_score',
            'posted_at',
            'created_at',
            'raw_metadata',
            'sentiment_analysis_id',
        ]
        read_only_fields = ['id', 'engagement_score', 'created_at']


class SocialFetchRequestSerializer(serializers.Serializer):
    """Serializer for requesting social post ingestion from official APIs."""
    platform = serializers.ChoiceField(
        choices=['twitter', 'instagram'],
        help_text="Target social media platform"
    )
    query = serializers.CharField(
        max_length=200,
        required=False,
        default='',
        allow_blank=True,
        help_text="Keyword query for Twitter search (optional for Instagram)"
    )
    count = serializers.IntegerField(
        min_value=1,
        max_value=100,
        default=10,
        help_text="Number of posts to fetch (1 to 100)"
    )
    save_to_db = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Whether to save retrieved posts and sentiment predictions into the database"
    )
