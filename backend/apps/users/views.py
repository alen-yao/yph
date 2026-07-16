"""
用户模块视图
参照 ModulithShop account 模块的 Controller
"""
from rest_framework import viewsets, status, permissions, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from utils.sms import SMSService
from .models import User, UserLevel, DeliveryAddress, UserMessage, UserPointsHistory, UserLoginHistory
from .serializers import (
    UserRegisterSerializer, CustomTokenObtainPairSerializer,
    UserSerializer, UserDetailSerializer, UserLevelSerializer,
    DeliveryAddressSerializer, UserMessageSerializer,
    UserPointsHistorySerializer, UserLoginHistorySerializer,
    MultiLoginSerializer, SendSMSSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    用户登录 - 账号密码登录（兼容旧接口）
    对应 modulithshop 的 LoginController
    """
    serializer_class = CustomTokenObtainPairSerializer


class MultiLoginView(viewsets.GenericViewSet):
    """
    统一登录视图 - 支持多种登录方式

    支持的登录方式：
    1. password - 账号密码登录（PC端）
    2. sms - 手机验证码登录（PC端、移动端）
    3. wechat - 微信登录（小程序、H5）
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MultiLoginSerializer

    @action(detail=False, methods=['post'], url_path='multi-login')
    def multi_login(self, request):
        """
        统一登录接口

        请求示例：
        1. 密码登录：
        {
            "login_type": "password",
            "username": "13800138000",
            "password": "123456"
        }

        2. 验证码登录：
        {
            "login_type": "sms",
            "mobile": "13800138000",
            "code": "123456"
        }

        3. 微信登录（首次需绑定手机）：
        {
            "login_type": "wechat",
            "wechat_code": "wx_code_from_frontend",
            "app_type": "miniprogram",
            "bind_mobile": "13800138000",  // 首次登录必填
            "bind_code": "123456"           // 首次登录必填
        }
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            token_data = serializer.validated_data.get('token_data')

            return Response({
                'code': 200,
                'message': '登录成功',
                'data': token_data
            }, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            # 处理微信首次登录需要绑定手机的情况
            if isinstance(e.detail, dict) and e.detail.get('need_bind'):
                return Response({
                    'code': 1001,
                    'message': e.detail.get('message', '需要绑定手机号'),
                    'data': {
                        'need_bind': True,
                        'openid': e.detail.get('openid')
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                'code': 400,
                'message': str(e.detail) if isinstance(e.detail, str) else '登录失败',
                'data': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='send-sms')
    def send_sms(self, request):
        """
        发送短信验证码

        请求示例：
        {
            "mobile": "13800138000",
            "code_type": "login"  // login-登录, register-注册, reset-重置密码
        }
        """
        serializer = SendSMSSerializer(data=request.data)

        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            code_type = serializer.validated_data.get('code_type', 'login')

            success, message, code = SMSService.send_code(mobile, code_type)

            if success:
                return Response({
                    'code': 200,
                    'message': message,
                    'data': {
                        'mobile': mobile,
                        'expire_time': 300  # 5分钟
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'code': 400,
                    'message': message
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'code': 400,
            'message': '参数错误',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集
    对应 modulithshop 的 UserController
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'mobile', 'nickname', 'email']
    ordering_fields = ['id', 'created_time', 'user_points', 'user_money']

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve', 'update', 'partial_update']:
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """用户注册"""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '注册成功',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put'], url_path='profile')
    def profile(self, request):
        """获取/更新用户信息"""
        if request.method == 'GET':
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserDetailSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """修改密码"""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'error': '请提供旧密码和新密码'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(old_password):
            return Response({'error': '旧密码错误'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()
        return Response({'message': '密码修改成功'})


class UserLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户等级视图集
    对应 modulithshop 的 UserLevelController
    """
    queryset = UserLevel.objects.all()
    serializer_class = UserLevelSerializer
    permission_classes = [permissions.AllowAny]


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    """
    收货地址视图集
    对应 modulithshop 的 UserDeliveryAddressController
    """
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='set-default')
    def set_default(self, request, pk=None):
        """设置默认地址"""
        address = self.get_object()
        DeliveryAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
        address.is_default = True
        address.save()
        return Response({'message': '设置成功'})


class UserMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户消息视图集
    对应 modulithshop 的 UserMessageController
    """
    serializer_class = UserMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        """标记为已读"""
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'message': '已标记为已读'})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        """全部标记为已读"""
        UserMessage.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': '已全部标记为已读'})

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        """未读消息数量"""
        count = UserMessage.objects.filter(user=request.user, is_read=False).count()
        return Response({'count': count})


class UserPointsHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """积分历史视图集"""
    serializer_class = UserPointsHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPointsHistory.objects.filter(user=self.request.user)


class UserLoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    登录历史视图集
    对应 modulithshop 的 UserLoginHistoryController
    """
    serializer_class = UserLoginHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserLoginHistory.objects.filter(user=self.request.user)
