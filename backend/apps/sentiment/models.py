"""
Database models for storing sentiment analysis predictions and NLP metrics.
"""

from django.db import models


class SentimentAnalysis(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter / X'),
        ('instagram', 'Instagram'),
        ('manual', 'Manual Input'),
    ]

    SENTIMENT_CHOICES = [
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
        ('positive', 'Positive'),
    ]

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        default='manual',
        db_index=True,
        help_text="Platform source for the analyzed text"
    )
    original_text = models.TextField(
        help_text="Original raw text submitted for sentiment classification"
    )
    cleaned_text = models.TextField(
        blank=True,
        default='',
        help_text="Preprocessed text normalized for the respective model"
    )
    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        db_index=True,
        help_text="Predicted sentiment class (negative, neutral, positive)"
    )
    confidence = models.FloatField(
        help_text="Model prediction probability percentage for the winning class (0.0 to 100.0)"
    )
    negative_probability = models.FloatField(
        default=0.0,
        help_text="Model probability percentage for negative sentiment"
    )
    neutral_probability = models.FloatField(
        default=0.0,
        help_text="Model probability percentage for neutral sentiment"
    )
    positive_probability = models.FloatField(
        default=0.0,
        help_text="Model probability percentage for positive sentiment"
    )
    
    # Advanced NLP optional fields
    emotion = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Dominant emotion detected (e.g. joy, sadness, anger, fear, surprise, disgust, neutral)"
    )
    emotion_scores = models.JSONField(
        default=dict,
        blank=True,
        help_text="Dictionary of emotion confidence scores"
    )
    topics = models.JSONField(
        default=list,
        blank=True,
        help_text="List of extracted topic keywords or clusters"
    )
    keywords = models.JSONField(
        default=list,
        blank=True,
        help_text="List of salient extracted keywords and their TF-IDF scores"
    )
    feature_importance = models.JSONField(
        default=dict,
        blank=True,
        help_text="Word influence weights contributing to the linear model score (non-causal)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the analysis was performed"
    )

    class Meta:
        verbose_name = 'Sentiment Analysis'
        verbose_name_plural = 'Sentiment Analyses'
        ordering = ['-created_at']

    def __str__(self):
        snippet = self.original_text[:40].replace('\n', ' ')
        return f"[{self.platform.upper()}] {self.sentiment.upper()} ({self.confidence:.1f}%) - {snippet}"
