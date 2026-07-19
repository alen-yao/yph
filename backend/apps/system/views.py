"""系统模块视图"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import SystemConfig, Banner, UserRole
from .serializers import BannerSerializer, UserRoleSerializer


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
