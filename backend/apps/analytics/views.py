"""
Views for dashboard aggregate metrics, sentiment distribution, and platform comparison.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from apps.sentiment.models import SentimentAnalysis
from apps.social_media.models import SocialPost


class DashboardOverviewView(APIView):
    """Returns high-level statistics across all analyzed posts and sentiment records."""
    def get(self, request):
        total_analyses = SentimentAnalysis.objects.count()
        positive_count = SentimentAnalysis.objects.filter(sentiment='positive').count()
        neutral_count = SentimentAnalysis.objects.filter(sentiment='neutral').count()
        negative_count = SentimentAnalysis.objects.filter(sentiment='negative').count()
        avg_confidence = SentimentAnalysis.objects.aggregate(avg=Avg('confidence'))['avg'] or 0.0

        return Response({
            "total_analyzed": total_analyses,
            "sentiment_counts": {
                "positive": positive_count,
                "neutral": neutral_count,
                "negative": negative_count,
            },
            "sentiment_percentages": {
                "positive": round((positive_count / total_analyses * 100), 2) if total_analyses > 0 else 0.0,
                "neutral": round((neutral_count / total_analyses * 100), 2) if total_analyses > 0 else 0.0,
                "negative": round((negative_count / total_analyses * 100), 2) if total_analyses > 0 else 0.0,
            },
            "average_confidence": round(avg_confidence, 2),
        }, status=status.HTTP_200_OK)


class PlatformComparisonView(APIView):
    """Compares sentiment distribution and metrics between Twitter/X and Instagram."""
    def get(self, request):
        platforms = ['twitter', 'instagram']
        comparison = {}

        for p in platforms:
            total = SentimentAnalysis.objects.filter(platform=p).count()
            pos = SentimentAnalysis.objects.filter(platform=p, sentiment='positive').count()
            neu = SentimentAnalysis.objects.filter(platform=p, sentiment='neutral').count()
            neg = SentimentAnalysis.objects.filter(platform=p, sentiment='negative').count()
            avg_conf = SentimentAnalysis.objects.filter(platform=p).aggregate(avg=Avg('confidence'))['avg'] or 0.0

            comparison[p] = {
                "total": total,
                "positive": pos,
                "neutral": neu,
                "negative": neg,
                "positive_pct": round((pos / total * 100), 2) if total > 0 else 0.0,
                "neutral_pct": round((neu / total * 100), 2) if total > 0 else 0.0,
                "negative_pct": round((neg / total * 100), 2) if total > 0 else 0.0,
                "average_confidence": round(avg_conf, 2),
            }

        return Response({
            "comparison": comparison,
            "methodology_note": "Differences reflect distinct dataset source domains, vocabularies, and platform-specific behaviors. Not a controlled causal experiment."
        }, status=status.HTTP_200_OK)
