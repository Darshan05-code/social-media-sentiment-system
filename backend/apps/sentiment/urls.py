from django.urls import path
from .views import (
    SentimentAnalysisListView,
    SentimentAnalysisDetailView,
    PredictUnifiedView,
    PredictTwitterView,
    PredictInstagramView,
)

urlpatterns = [
    path('', SentimentAnalysisListView.as_view(), name='sentiment_list'),
    path('<int:pk>/', SentimentAnalysisDetailView.as_view(), name='sentiment_detail'),
    path('predict/', PredictUnifiedView.as_view(), name='sentiment_predict_unified'),
    path('twitter/', PredictTwitterView.as_view(), name='sentiment_predict_twitter'),
    path('instagram/', PredictInstagramView.as_view(), name='sentiment_predict_instagram'),
]
