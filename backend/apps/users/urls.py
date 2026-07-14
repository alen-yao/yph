"""
用户模块URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView, UserViewSet, UserLevelViewSet,
    DeliveryAddressViewSet, UserMessageViewSet,
    UserPointsHistoryViewSet, UserLoginHistoryViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'levels', UserLevelViewSet, basename='user-level')
router.register(r'addresses', DeliveryAddressViewSet, basename='address')
router.register(r'messages', UserMessageViewSet, basename='message')
router.register(r'points-history', UserPointsHistoryViewSet, basename='points-history')
router.register(r'login-history', UserLoginHistoryViewSet, basename='login-history')

urlpatterns = [
    # JWT认证
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 路由
    path('', include(router.urls)),
]
