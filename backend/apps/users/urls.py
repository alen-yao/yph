"""
用户模块URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView, UserViewSet, UserLevelViewSet,
    DeliveryAddressViewSet, UserMessageViewSet,
    UserPointsHistoryViewSet, UserLoginHistoryViewSet,
    MultiLoginView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'levels', UserLevelViewSet, basename='user-level')
router.register(r'addresses', DeliveryAddressViewSet, basename='address')
router.register(r'messages', UserMessageViewSet, basename='message')
router.register(r'points-history', UserPointsHistoryViewSet, basename='points-history')
router.register(r'login-history', UserLoginHistoryViewSet, basename='login-history')
router.register(r'auth', MultiLoginView, basename='auth')

urlpatterns = [
    # JWT认证（旧接口，兼容性保留）
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 路由
    path('', include(router.urls)),
]

# 新的多登录接口：
# POST /api/users/auth/multi-login/  - 统一登录接口
# POST /api/users/auth/send-sms/     - 发送短信验证码
