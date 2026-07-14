"""商品模块视图"""
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Product, ProductCategory, ProductBrand,
                     ProductComment, ProductItem)
from .serializers import (ProductCategorySerializer, ProductBrandSerializer,
                          ProductListSerializer, ProductDetailSerializer,
                          ProductCreateUpdateSerializer,
                          ProductCommentSerializer, ProductItemSerializer)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """商品分类管理"""
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['sort_order', 'created_time']

    def get_permissions(self):
        # 读取操作允许所有人，写入操作需要管理员权限
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        # 普通用户只能看到显示的分类，管理员可以看到所有
        queryset = ProductCategory.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_show=True)
        return queryset


class ProductBrandViewSet(viewsets.ModelViewSet):
    """商品品牌管理"""
    queryset = ProductBrand.objects.all()
    serializer_class = ProductBrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['sort_order', 'created_time']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = ProductBrand.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_show=True)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    """商品管理"""
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'state']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'sales_count', 'rating_average', 'created_time']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = Product.objects.all()
        # 普通用户只能看到上架的商品
        if not self.request.user.is_staff:
            queryset = queryset.filter(state=1)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductListSerializer


class ProductCommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductCommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        queryset = ProductComment.objects.filter(is_show=True)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
