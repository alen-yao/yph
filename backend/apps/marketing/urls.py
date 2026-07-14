"""营销模块URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, CouponViewSet, UserCouponViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'user-coupons', UserCouponViewSet, basename='user-coupon')

urlpatterns = [
    path('', include(router.urls)),
]
