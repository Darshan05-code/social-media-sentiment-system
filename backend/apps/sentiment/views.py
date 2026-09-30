"""
Views for sentiment prediction and analysis retrieval.

Connects incoming REST requests to the Phase 2 ML Service Layer,
handling input validation, HTTP status codes, and error formatting.
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import SentimentAnalysis
from .serializers import (
    SentimentAnalysisSerializer,
    SentimentPredictRequestSerializer,
    PlatformPredictRequestSerializer,
)
from .services import predict_sentiment, ModelUnavailableException

logger = logging.getLogger(__name__)


class SentimentAnalysisListView(APIView):
    """
    get:
    List recent sentiment analysis records with optional platform and sentiment filtering.
    Query parameters:
    - platform: filter by 'twitter', 'instagram', or 'manual'
    - sentiment: filter by 'positive', 'neutral', or 'negative'
    - limit: maximum number of records to return (default 50, max 200)
    """
    def get(self, request):
        platform = request.query_params.get('platform')
        sentiment = request.query_params.get('sentiment')
        try:
            limit = min(int(request.query_params.get('limit', 50)), 200)
        except (ValueError, TypeError):
            limit = 50

        queryset = SentimentAnalysis.objects.all()
        if platform:
            queryset = queryset.filter(platform=platform.strip().lower())
        if sentiment:
            queryset = queryset.filter(sentiment=sentiment.strip().lower())

        serializer = SentimentAnalysisSerializer(queryset[:limit], many=True)
        return Response({
            "count": len(serializer.data),
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class SentimentAnalysisDetailView(APIView):
    """
    get:
    Retrieve a single sentiment analysis record by ID.
    delete:
    Delete an existing sentiment analysis record by ID.
    """
    def get(self, request, pk):
        record = get_object_or_404(SentimentAnalysis, pk=pk)
        serializer = SentimentAnalysisSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        record = get_object_or_404(SentimentAnalysis, pk=pk)
        record.delete()
        return Response({"message": f"Record {pk} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class PredictUnifiedView(APIView):
    """
    post:
    Unified sentiment prediction endpoint.
    Accepts text and target platform ('twitter' or 'instagram').
    
    Example payload:
    ```json
    {
      "platform": "instagram",
      "text": "I absolutely love this! 😍",
      "save_to_db": true,
      "run_advanced_nlp": true
    }
    ```
    """
    def post(self, request):
        serializer = SentimentPredictRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        platform = data['platform']
        text = data['text']
        save_to_db = data.get('save_to_db', True)
        run_advanced_nlp = data.get('run_advanced_nlp', True)

        try:
            result = predict_sentiment(
                platform=platform,
                text=text,
                save_to_db=save_to_db,
                run_advanced_nlp=run_advanced_nlp
            )
            return Response(result, status=status.HTTP_200_OK)
        except ModelUnavailableException as exc:
            logger.error(f"Sentiment model unavailable: {exc}")
            return Response({
                "error": "Sentiment model is unavailable.",
                "details": str(exc)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ValueError as exc:
            return Response({
                "error": str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.error(f"Prediction failed unexpectedly: {exc}", exc_info=True)
            return Response({
                "error": "An unexpected error occurred during prediction. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PredictTwitterView(APIView):
    """
    post:
    Twitter/X-specific sentiment prediction endpoint.
    Processes text using the 100K-trained Twitter Logistic Regression and TF-IDF pipeline.
    
    Example payload:
    ```json
    {
      "text": "Great morning everyone! Exciting news coming up."
    }
    ```
    """
    def post(self, request):
        serializer = PlatformPredictRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        text = data['text']
        save_to_db = data.get('save_to_db', True)
        run_advanced_nlp = data.get('run_advanced_nlp', True)

        try:
            result = predict_sentiment(
                platform='twitter',
                text=text,
                save_to_db=save_to_db,
                run_advanced_nlp=run_advanced_nlp
            )
            return Response(result, status=status.HTTP_200_OK)
        except ModelUnavailableException as exc:
            logger.error(f"Twitter model unavailable: {exc}")
            return Response({
                "error": "Sentiment model is unavailable."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ValueError as exc:
            return Response({
                "error": str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.error(f"Twitter prediction failed: {exc}", exc_info=True)
            return Response({
                "error": "An error occurred while evaluating Twitter sentiment."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PredictInstagramView(APIView):
    """
    post:
    Instagram-specific sentiment prediction endpoint.
    Processes text using the Unicode-safe Instagram Logistic Regression and TF-IDF pipeline.
    Preserves emojis, Hindi, Gujarati, and other non-ASCII multilingual scripts.
    
    Example payload:
    ```json
    {
      "text": "I absolutely love this! 😍"
    }
    ```
    """
    def post(self, request):
        serializer = PlatformPredictRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        text = data['text']
        save_to_db = data.get('save_to_db', True)
        run_advanced_nlp = data.get('run_advanced_nlp', True)

        try:
            result = predict_sentiment(
                platform='instagram',
                text=text,
                save_to_db=save_to_db,
                run_advanced_nlp=run_advanced_nlp
            )
            return Response(result, status=status.HTTP_200_OK)
        except ModelUnavailableException as exc:
            logger.error(f"Instagram model unavailable: {exc}")
            return Response({
                "error": "Sentiment model is unavailable."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ValueError as exc:
            return Response({
                "error": str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.error(f"Instagram prediction failed: {exc}", exc_info=True)
            return Response({
                "error": "An error occurred while evaluating Instagram sentiment."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
