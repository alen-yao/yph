"""店铺模块URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FavoritesViewSet, BrowseHistoryViewSet, SearchHistoryViewSet

router = DefaultRouter()
router.register(r'favorites', FavoritesViewSet, basename='favorites')
router.register(r'browse-history', BrowseHistoryViewSet, basename='browse-history')
router.register(r'search-history', SearchHistoryViewSet, basename='search-history')

urlpatterns = [
    path('', include(router.urls)),
]
