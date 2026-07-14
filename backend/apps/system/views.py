"""系统模块视图"""
from rest_framework import viewsets, permissions, serializers
from .models import SystemConfig, Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """轮播图视图集"""
    queryset = Banner.objects.filter(is_show=True)
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]
