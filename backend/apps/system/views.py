"""系统模块视图"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import SystemConfig, Banner, UserRole
from .serializers import (BannerSerializer, UserRoleSerializer,
                          ImageUploadSerializer, MultipleImageUploadSerializer)
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
                    'url': 'http://localhost:9000/yph-products/products/abc123.jpg',
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
            # 上传到MinIO
            file_url = minio_client.upload_file(file, folder=folder)
            return Response({
                'url': file_url,
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
                    'urls': [
                        'http://localhost:9000/yph-products/products/abc123.jpg',
                        'http://localhost:9000/yph-products/products/def456.jpg'
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
            # 批量上传到MinIO
            file_urls = minio_client.upload_multiple_files(files, folder=folder)
            return Response({
                'urls': file_urls,
                'message': '图片上传成功',
                'count': len(file_urls)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
