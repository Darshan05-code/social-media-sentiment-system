"""
Serializers for the Sentiment Analysis API and request validation.
"""

from rest_framework import serializers
from .models import SentimentAnalysis


class SentimentPredictRequestSerializer(serializers.Serializer):
    """Serializer for the unified sentiment prediction endpoint."""
    platform = serializers.ChoiceField(
        choices=['twitter', 'instagram', 'x', 'ig'],
        default='twitter',
        help_text="Target model platform: 'twitter' or 'instagram'"
    )
    text = serializers.CharField(
        max_length=5000,
        required=True,
        help_text="Text content to analyze (1 to 5000 characters)"
    )
    save_to_db = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Whether to persist the prediction record to the database"
    )
    run_advanced_nlp = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Whether to compute emotions, topics, and feature influence"
    )

    def validate_text(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError("Text cannot be empty.")
        if len(stripped) > 5000:
            raise serializers.ValidationError("Text exceeds maximum allowed length of 5000 characters.")
        return stripped

    def validate_platform(self, value):
        normalized = value.strip().lower()
        if normalized in ('twitter', 'x'):
            return 'twitter'
        elif normalized in ('instagram', 'ig'):
            return 'instagram'
        raise serializers.ValidationError(f"Invalid platform '{value}'. Must be 'twitter' or 'instagram'.")


class PlatformPredictRequestSerializer(serializers.Serializer):
    """Serializer for platform-specific prediction endpoints (/twitter/ and /instagram/)."""
    text = serializers.CharField(
        max_length=5000,
        required=True,
        help_text="Text content to analyze (1 to 5000 characters)"
    )
    save_to_db = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Whether to persist the prediction record to the database"
    )
    run_advanced_nlp = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Whether to compute emotions, topics, and feature influence"
    )

    def validate_text(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError("Text cannot be empty.")
        if len(stripped) > 5000:
            raise serializers.ValidationError("Text exceeds maximum allowed length of 5000 characters.")
        return stripped


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for retrieving persisted SentimentAnalysis records."""
    probabilities = serializers.SerializerMethodField()

    class Meta:
        model = SentimentAnalysis
        fields = [
            'id',
            'platform',
            'original_text',
            'cleaned_text',
            'sentiment',
            'confidence',
            'probabilities',
            'emotion',
            'emotion_scores',
            'topics',
            'keywords',
            'feature_importance',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_probabilities(self, obj):
        return {
            'negative': round(float(obj.negative_probability), 2),
            'neutral': round(float(obj.neutral_probability), 2),
            'positive': round(float(obj.positive_probability), 2),
        }
