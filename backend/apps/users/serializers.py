"""
用户模块序列化器
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from utils.sms import SMSService, WeChatService
from .models import User, UserLevel, DeliveryAddress, UserMessage, UserPointsHistory, UserLoginHistory

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6, max_length=20)
    password_confirm = serializers.CharField(write_only=True, min_length=6, max_length=20)
    code = serializers.CharField(write_only=True, min_length=4, max_length=6)

    class Meta:
        model = User
        fields = ['mobile', 'password', 'password_confirm', 'code']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('两次密码不一致')
        # TODO: 验证短信验证码
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data.pop('code')
        user = User.objects.create_user(
            username=validated_data['mobile'],
            mobile=validated_data['mobile'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义JWT token序列化器 - 账号密码登录"""

    def validate(self, attrs):
        data = super().validate(attrs)
        # 添加用户额外信息
        data['user_id'] = self.user.id
        data['mobile'] = self.user.mobile
        data['nickname'] = self.user.nickname or self.user.username
        data['avatar'] = self.user.avatar.url if self.user.avatar else ''
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser

        # 添加角色信息
        if self.user.role:
            data['role'] = {
                'id': self.user.role.id,
                'name': self.user.role.name,
                'description': self.user.role.description,
                'permissions_data': self.user.role.get_permissions()
            }
        else:
            data['role'] = None

        return data


class MultiLoginSerializer(serializers.Serializer):
    """
    统一登录序列化器 - 支持多种登录方式

    登录方式：
    1. password - 账号密码登录（PC端）
    2. sms - 手机验证码登录（PC端、移动端）
    3. wechat - 微信登录（小程序、H5）
    """
    login_type = serializers.ChoiceField(
        choices=['password', 'sms', 'wechat'],
        required=True,
        help_text='登录类型: password-密码登录, sms-验证码登录, wechat-微信登录'
    )

    # 密码登录字段
    username = serializers.CharField(required=False, help_text='用户名/手机号')
    password = serializers.CharField(required=False, write_only=True, help_text='密码')

    # 验证码登录字段
    mobile = serializers.CharField(required=False, help_text='手机号')
    code = serializers.CharField(required=False, help_text='验证码')

    # 微信登录字段
    wechat_code = serializers.CharField(required=False, help_text='微信授权code')
    app_type = serializers.ChoiceField(
        choices=['miniprogram', 'h5'],
        required=False,
        default='miniprogram',
        help_text='应用类型: miniprogram-小程序, h5-公众号'
    )

    # 微信登录时的可选信息（用于首次绑定）
    bind_mobile = serializers.CharField(required=False, help_text='绑定手机号（微信登录时可选）')
    bind_code = serializers.CharField(required=False, help_text='手机验证码（绑定手机时必填）')

    def validate(self, attrs):
        login_type = attrs.get('login_type')

        # 根据登录类型验证必填字段
        if login_type == 'password':
            if not attrs.get('username') or not attrs.get('password'):
                raise serializers.ValidationError('账号密码登录需要提供username和password')
            user = self._validate_password_login(attrs)

        elif login_type == 'sms':
            if not attrs.get('mobile') or not attrs.get('code'):
                raise serializers.ValidationError('验证码登录需要提供mobile和code')
            user = self._validate_sms_login(attrs)

        elif login_type == 'wechat':
            if not attrs.get('wechat_code'):
                raise serializers.ValidationError('微信登录需要提供wechat_code')
            user = self._validate_wechat_login(attrs)

        else:
            raise serializers.ValidationError('不支持的登录类型')

        if not user:
            raise serializers.ValidationError('登录失败')

        if not user.is_active:
            raise serializers.ValidationError('账号已被禁用')

        # 生成token
        refresh = RefreshToken.for_user(user)

        attrs['user'] = user
        attrs['token_data'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'mobile': user.mobile,
            'nickname': user.nickname or user.username,
            'avatar': user.avatar.url if user.avatar else '',
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'role': {
                'id': user.role.id,
                'name': user.role.name,
                'description': user.role.description,
                'permissions_data': user.role.get_permissions()
            } if user.role else None
        }

        return attrs

    def _validate_password_login(self, attrs):
        """验证账号密码登录"""
        from django.contrib.auth import authenticate

        username = attrs.get('username')
        password = attrs.get('password')

        # 尝试用户名登录
        user = authenticate(username=username, password=password)

        # 如果失败，尝试手机号登录
        if not user:
            try:
                user_obj = User.objects.get(mobile=username)
                if user_obj.check_password(password):
                    user = user_obj
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError('用户名或密码错误')

        return user

    def _validate_sms_login(self, attrs):
        """验证短信验证码登录"""
        mobile = attrs.get('mobile')
        code = attrs.get('code')

        # 验证验证码
        if not SMSService.verify_code(mobile, code, 'login'):
            raise serializers.ValidationError('验证码错误或已过期')

        # 查找或创建用户
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 自动注册
            user = User.objects.create_user(
                username=mobile,
                mobile=mobile,
                password=User.objects.make_random_password()  # 随机密码
            )

        return user

    def _validate_wechat_login(self, attrs):
        """验证微信登录"""
        wechat_code = attrs.get('wechat_code')
        app_type = attrs.get('app_type', 'miniprogram')

        # 获取微信openid
        wechat_data = WeChatService.get_openid_by_code(wechat_code, app_type)

        if not wechat_data or not wechat_data.get('openid'):
            raise serializers.ValidationError('微信登录失败，请重试')

        openid = wechat_data.get('openid')
        unionid = wechat_data.get('unionid')

        # 查找已绑定的用户
        try:
            user = User.objects.get(wechat_openid=openid)
            # 更新unionid（如果有）
            if unionid and not user.wechat_unionid:
                user.wechat_unionid = unionid
                user.save()
            return user

        except User.DoesNotExist:
            # 检查是否需要绑定手机号
            bind_mobile = attrs.get('bind_mobile')
            bind_code = attrs.get('bind_code')

            if bind_mobile and bind_code:
                # 验证手机验证码
                if not SMSService.verify_code(bind_mobile, bind_code, 'login'):
                    raise serializers.ValidationError('手机验证码错误或已过期')

                # 查找或创建用户
                try:
                    user = User.objects.get(mobile=bind_mobile)
                    # 绑定微信
                    user.wechat_openid = openid
                    if unionid:
                        user.wechat_unionid = unionid
                    user.save()
                except User.DoesNotExist:
                    # 创建新用户
                    user = User.objects.create_user(
                        username=bind_mobile,
                        mobile=bind_mobile,
                        password=User.objects.make_random_password(),
                        wechat_openid=openid,
                        wechat_unionid=unionid
                    )

                return user
            else:
                # 需要绑定手机号
                raise serializers.ValidationError({
                    'need_bind': True,
                    'openid': openid,
                    'message': '首次微信登录，请绑定手机号'
                })


class SendSMSSerializer(serializers.Serializer):
    """发送短信验证码序列化器"""
    mobile = serializers.CharField(max_length=11, min_length=11, help_text='手机号')
    code_type = serializers.ChoiceField(
        choices=['login', 'register', 'reset'],
        default='login',
        help_text='验证码类型: login-登录, register-注册, reset-重置密码'
    )

    def validate_mobile(self, value):
        """验证手机号格式"""
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value


class UserSerializer(serializers.ModelSerializer):
    """用户基本信息序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'nickname', 'avatar', 'gender',
                  'birthday', 'user_level_id', 'user_points', 'user_money',
                  'email', 'is_active', 'created_time']
        read_only_fields = ['id', 'username', 'mobile', 'user_points',
                            'user_money', 'created_time']


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详细信息序列化器"""
    password = serializers.CharField(write_only=True, required=False, min_length=6, max_length=20, allow_blank=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    role_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'nickname', 'avatar', 'gender',
                  'birthday', 'user_level_id', 'user_points', 'user_money',
                  'user_invite_code', 'email', 'is_active', 'is_staff', 'is_superuser',
                  'role', 'role_name', 'role_data', 'password', 'created_time']
        read_only_fields = ['id', 'user_invite_code', 'created_time']
        extra_kwargs = {
            'username': {'required': False}  # 编辑时不需要，新增时会自动设置
        }

    def get_role_data(self, obj):
        """获取角色详细信息"""
        if obj.role:
            return {
                'id': obj.role.id,
                'name': obj.role.name,
                'description': obj.role.description,
                'permissions_data': obj.role.get_permissions()
            }
        return None

    def validate(self, attrs):
        """验证数据"""
        # 新增时密码必填
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': '新增用户时密码不能为空'})
        return attrs

    def create(self, validated_data):
        """创建用户时处理密码"""
        password = validated_data.pop('password')
        # 如果没有提供 username，使用 mobile 作为 username
        if 'username' not in validated_data or not validated_data.get('username'):
            validated_data['username'] = validated_data['mobile']
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user

    def update(self, instance, validated_data):
        """更新用户时处理密码"""
        password = validated_data.pop('password', None)
        validated_data.pop('username', None)  # 编辑时不允许修改用户名
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserLevelSerializer(serializers.ModelSerializer):
    """用户等级序列化器"""

    class Meta:
        model = UserLevel
        fields = '__all__'


class DeliveryAddressSerializer(serializers.ModelSerializer):
    """收货地址序列化器"""

    class Meta:
        model = DeliveryAddress
        fields = ['id', 'consignee', 'mobile', 'province', 'city', 'district',
                  'address', 'zipcode', 'is_default', 'created_time']
        read_only_fields = ['id', 'created_time']

    def create(self, validated_data):
        user = self.context['request'].user
        # 如果设置为默认地址，取消其他默认地址
        if validated_data.get('is_default'):
            DeliveryAddress.objects.filter(user=user, is_default=True).update(is_default=False)
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('is_default'):
            DeliveryAddress.objects.filter(user=instance.user, is_default=True).update(is_default=False)
        return super().update(instance, validated_data)


class UserMessageSerializer(serializers.ModelSerializer):
    """用户消息序列化器"""

    class Meta:
        model = UserMessage
        fields = ['id', 'message_type', 'title', 'content', 'is_read', 'created_time']
        read_only_fields = ['id', 'created_time']


class UserPointsHistorySerializer(serializers.ModelSerializer):
    """积分历史序列化器"""

    class Meta:
        model = UserPointsHistory
        fields = ['id', 'points', 'points_type', 'description', 'created_time']
        read_only_fields = ['id', 'created_time']


class UserLoginHistorySerializer(serializers.ModelSerializer):
    """登录历史序列化器"""

    class Meta:
        model = UserLoginHistory
        fields = ['id', 'login_ip', 'login_device', 'login_os', 'login_browser', 'login_time']
        read_only_fields = ['id']
