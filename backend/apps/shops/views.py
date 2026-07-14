"""店铺模块视图"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FavoritesItem, ProductBrowse, SearchHistory
from rest_framework import serializers


class FavoritesItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritesItem
        fields = '__all__'


class ProductBrowseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrowse
        fields = '__all__'


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'


class FavoritesViewSet(viewsets.ModelViewSet):
    """商品收藏视图集"""
    serializer_class = FavoritesItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoritesItem.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle_favorite(self, request):
        """收藏/取消收藏"""
        product_id = request.data.get('product_id')
        favorite = FavoritesItem.objects.filter(user=request.user, product_id=product_id).first()

        if favorite:
            favorite.delete()
            return Response({'message': '已取消收藏', 'is_favorite': False})
        else:
            FavoritesItem.objects.create(user=request.user, product_id=product_id)
            return Response({'message': '收藏成功', 'is_favorite': True})


class BrowseHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """浏览历史视图集"""
    serializer_class = ProductBrowseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProductBrowse.objects.filter(user=self.request.user)


class SearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """搜索历史视图集"""
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)[:20]

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_history(self, request):
        """清空搜索历史"""
        SearchHistory.objects.filter(user=request.user).delete()
        return Response({'message': '已清空搜索历史'})
