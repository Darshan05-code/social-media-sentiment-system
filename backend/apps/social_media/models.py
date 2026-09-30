"""
Database models for storing ingested social media posts, comments, and engagement metrics.
"""

from django.db import models


class SocialPost(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter / X'),
        ('instagram', 'Instagram'),
    ]

    SENTIMENT_CHOICES = [
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
        ('positive', 'Positive'),
    ]

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        db_index=True,
        help_text="Originating platform (Twitter/X or Instagram)"
    )
    external_id = models.CharField(
        max_length=128,
        db_index=True,
        help_text="External platform ID (tweet ID, IG media ID, IG comment ID)"
    )
    username = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Platform username / handle where permitted"
    )
    author_display_name = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text="Display name where permitted"
    )
    text = models.TextField(
        help_text="Body content of the post, tweet, or comment"
    )
    likes_count = models.IntegerField(
        default=0,
        help_text="Number of likes / favorites"
    )
    comments_count = models.IntegerField(
        default=0,
        help_text="Number of replies / comments"
    )
    shares_count = models.IntegerField(
        default=0,
        help_text="Number of retweets / reposts / shares"
    )
    engagement_score = models.FloatField(
        default=0.0,
        help_text="Calculated engagement metric: likes + comments*2 + shares*3"
    )
    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        blank=True,
        null=True,
        db_index=True,
        help_text="Evaluated sentiment class"
    )
    sentiment_score = models.FloatField(
        blank=True,
        null=True,
        help_text="Confidence percentage (0.0 to 100.0) from the sentiment model"
    )
    posted_at = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        help_text="Original timestamp published on the platform"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when ingested into the local system"
    )
    raw_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Permitted platform metadata (non-sensitive)"
    )
    sentiment_analysis = models.ForeignKey(
        'sentiment.SentimentAnalysis',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='social_posts',
        help_text="Linked detailed sentiment prediction record"
    )

    class Meta:
        verbose_name = 'Social Post'
        verbose_name_plural = 'Social Posts'
        ordering = ['-posted_at', '-created_at']
        unique_together = ('platform', 'external_id')

    def save(self, *args, **kwargs):
        # Calculate composite engagement metric
        self.engagement_score = float(self.likes_count + (self.comments_count * 2) + (self.shares_count * 3))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.platform.upper()}] @{self.username or 'anon'}: {self.text[:30]}"
