from django.urls import path
from .views import DashboardOverviewView, PlatformComparisonView

urlpatterns = [
    path('overview/', DashboardOverviewView.as_view(), name='analytics_overview'),
    path('comparison/', PlatformComparisonView.as_view(), name='analytics_comparison'),
]
