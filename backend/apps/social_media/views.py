"""
Views for social media post retrieval, credential status, and platform ingestion.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import SocialPost
from .serializers import SocialPostSerializer, SocialFetchRequestSerializer
from .services import twitter_service, instagram_service, get_social_service


class SocialStatusView(APIView):
    """
    get:
    Check configuration and credential status for Twitter/X and Instagram/Meta integrations.
    Returns clear messages if credentials are missing without exposing secret tokens.
    """
    def get(self, request):
        return Response({
            "twitter": twitter_service.get_configuration_status(),
            "instagram": instagram_service.get_configuration_status(),
            "note": "Manual sentiment prediction works without social media API credentials."
        }, status=status.HTTP_200_OK)


class FetchSocialPostsView(APIView):
    """
    post:
    Trigger content retrieval from official Twitter/X or Meta/Instagram APIs.
    
    If credentials are missing, returns status 'not_configured' with a clear message:
    - 'Twitter/X integration is not configured.'
    - 'Instagram integration is not configured.'
    
    NEVER generates fake social media data.
    """
    def post(self, request):
        serializer = SocialFetchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        platform = serializer.validated_data['platform']
        query = serializer.validated_data.get('query', '')
        count = serializer.validated_data.get('count', 10)
        save_to_db = serializer.validated_data.get('save_to_db', True)

        try:
            service = get_social_service(platform)
            result = service.ingest_and_analyze(
                query=query,
                count=count,
                save_to_db=save_to_db
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response({
                "error": f"Failed to execute {platform} fetch: {str(exc)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SocialPostListView(APIView):
    """
    get:
    List social media posts with optional platform and sentiment filtering.
    """
    def get(self, request):
        platform = request.query_params.get('platform')
        sentiment = request.query_params.get('sentiment')
        try:
            limit = min(int(request.query_params.get('limit', 50)), 200)
        except (ValueError, TypeError):
            limit = 50

        queryset = SocialPost.objects.all()
        if platform:
            queryset = queryset.filter(platform=platform.strip().lower())
        if sentiment:
            queryset = queryset.filter(sentiment=sentiment.strip().lower())

        serializer = SocialPostSerializer(queryset[:limit], many=True)
        return Response({
            "count": len(serializer.data),
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class SocialPostDetailView(APIView):
    """
    get:
    Retrieve single post details by database ID.
    delete:
    Remove a post record.
    """
    def get(self, request, pk):
        post = get_object_or_404(SocialPost, pk=pk)
        serializer = SocialPostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = get_object_or_404(SocialPost, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
