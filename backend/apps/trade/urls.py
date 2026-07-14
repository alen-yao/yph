"""交易模块URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet, OrderReturnViewSet, OrderReturnReasonViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'returns', OrderReturnViewSet, basename='return')
router.register(r'return-reasons', OrderReturnReasonViewSet, basename='return-reason')

urlpatterns = [
    path('', include(router.urls)),
]
