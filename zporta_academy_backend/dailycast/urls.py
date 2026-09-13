"""
URL configuration for DailyCast & Podcasts API.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from dailycast.views_api import DailyPodcastViewSet

router = DefaultRouter()
router.register(r'podcasts', DailyPodcastViewSet, basename='podcast')

urlpatterns = [
    path('', include(router.urls)),
]
