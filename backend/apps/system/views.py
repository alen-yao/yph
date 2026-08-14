"""系统模块视图"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import SystemConfig, Banner, UserRole, Region
from .serializers import (BannerSerializer, UserRoleSerializer, RegionSerializer,
                          RegionListSerializer, ImageUploadSerializer, MultipleImageUploadSerializer)
from utils.minio_client import minio_client


class UserRoleViewSet(viewsets.ModelViewSet):
    """用户角色管理视图集"""
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        """删除角色前检查是否有用户在使用"""
        instance = self.get_object()

        # 检查该角色下是否有用户
        user_count = instance.users.count()
        if user_count > 0:
            return Response(
                {'error': f'该角色下有 {user_count} 个用户，无法删除'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)


class RegionViewSet(viewsets.ModelViewSet):
    """地区管理视图集"""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """根据不同接口返回不同的查询集"""
        queryset = super().get_queryset()
        # 如果是H5前端调用（list接口），只返回启用的地区
        if self.action == 'list' and not self.request.user.is_staff:
            queryset = queryset.filter(status=True)
        return queryset

    def get_serializer_class(self):
        """根据不同action使用不同的序列化器"""
        if self.action == 'enabled_list':
            return RegionListSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def enabled_list(self, request):
        """获取所有启用的地区列表（简化版）"""
        regions = Region.objects.filter(status=True).order_by('sort_order', 'id')
        serializer = RegionListSerializer(regions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """切换地区启用状态"""
        region = self.get_object()
        region.status = not region.status
        region.save()
        return Response({
            'id': region.id,
            'status': region.status,
            'message': f'地区 {region.name} 已{"启用" if region.status else "禁用"}'
        })

    @action(detail=False, methods=['post'])
    def update_sort(self, request):
        """批量更新地区排序"""
        region_orders = request.data.get('regions', [])
        for item in region_orders:
            Region.objects.filter(id=item['id']).update(sort_order=item['sort_order'])
        return Response({'message': '排序更新成功'})


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """轮播图视图集"""
    queryset = Banner.objects.filter(is_show=True)
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]


@swagger_auto_schema(
    method='post',
    operation_description='上传单张图片到MinIO',
    request_body=ImageUploadSerializer,
    responses={
        200: openapi.Response(
            description='上传成功',
            examples={
                'application/json': {
                    'key': 'products/2026/08/abc123.jpg',
                    'url': 'http://localhost:9000/yph-products/products/2026/08/abc123.jpg',
                    'message': '图片上传成功'
                }
            }
        )
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_image(request):
    """上传单张图片"""
    serializer = ImageUploadSerializer(data=request.data)
    if serializer.is_valid():
        file = serializer.validated_data['file']
        folder = serializer.validated_data.get('folder', 'products')

        try:
            # 上传到MinIO，返回对象key
            object_key = minio_client.upload_file(file, folder=folder)
            # 生成完整URL供前端预览
            full_url = minio_client.get_image_url(object_key)
            return Response({
                'key': object_key,
                'url': full_url,
                'message': '图片上传成功'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description='批量上传图片到MinIO',
    request_body=MultipleImageUploadSerializer,
    responses={
        200: openapi.Response(
            description='上传成功',
            examples={
                'application/json': {
                    'keys': [
                        'products/2026/08/abc123.jpg',
                        'products/2026/08/def456.jpg'
                    ],
                    'urls': [
                        'http://localhost:9000/yph-products/products/2026/08/abc123.jpg',
                        'http://localhost:9000/yph-products/products/2026/08/def456.jpg'
                    ],
                    'message': '图片上传成功',
                    'count': 2
                }
            }
        )
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_multiple_images(request):
    """批量上传图片"""
    serializer = MultipleImageUploadSerializer(data=request.data)
    if serializer.is_valid():
        files = serializer.validated_data['files']
        folder = serializer.validated_data.get('folder', 'products')

        try:
            # 批量上传到MinIO，返回对象key列表
            object_keys = minio_client.upload_multiple_files(files, folder=folder)
            # 生成完整URL列表供前端预览
            full_urls = [minio_client.get_image_url(key) for key in object_keys]
            return Response({
                'keys': object_keys,
                'urls': full_urls,
                'message': '图片上传成功',
                'count': len(object_keys)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
