"""商品模块URL配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductCategoryViewSet, ProductBrandViewSet,
                   ProductViewSet, ProductCommentViewSet)

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet, basename='category')
router.register(r'brands', ProductBrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'comments', ProductCommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
