from django.urls import path
from .views import (
    SocialStatusView,
    FetchSocialPostsView,
    SocialPostListView,
    SocialPostDetailView
)

urlpatterns = [
    path('status/', SocialStatusView.as_view(), name='social_status'),
    path('fetch/', FetchSocialPostsView.as_view(), name='social_fetch'),
    path('posts/', SocialPostListView.as_view(), name='social_posts_list'),
    path('posts/<int:pk>/', SocialPostDetailView.as_view(), name='social_post_detail'),
]
