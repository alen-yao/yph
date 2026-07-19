"""系统模块URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'roles', UserRoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),
]
