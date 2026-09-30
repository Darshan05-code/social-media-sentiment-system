"""
Root URL configuration for AI-Based Social Media Sentiment and Reputation Analysis System.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from .docs_views import OpenAPISchemaView, SwaggerUIDocView

def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "AI-Based Social Media Sentiment & Reputation Analysis API",
        "version": "1.0.0"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='api_health'),
    path('api/schema/', OpenAPISchemaView.as_view(), name='api_schema'),
    path('api/docs/', SwaggerUIDocView.as_view(), name='api_docs'),
    path('api/sentiment/', include('apps.sentiment.urls')),
    path('api/social/', include('apps.social_media.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]
