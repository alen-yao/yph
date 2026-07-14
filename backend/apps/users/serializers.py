"""
用户模块序列化器
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
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
    """自定义JWT token序列化器"""

    def validate(self, attrs):
        data = super().validate(attrs)
        # 添加用户额外信息
        data['user_id'] = self.user.id
        data['mobile'] = self.user.mobile
        data['nickname'] = self.user.nickname or self.user.username
        data['avatar'] = self.user.avatar.url if self.user.avatar else ''
        return data


class UserSerializer(serializers.ModelSerializer):
    """用户基本信息序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'nickname', 'avatar', 'gender',
                  'birthday', 'user_level_id', 'user_points', 'user_money',
                  'email', 'created_time']
        read_only_fields = ['id', 'username', 'mobile', 'user_points',
                            'user_money', 'created_time']


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详细信息序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'nickname', 'avatar', 'gender',
                  'birthday', 'user_level_id', 'user_points', 'user_money',
                  'user_invite_code', 'email', 'is_active', 'created_time']
        read_only_fields = ['id', 'username', 'mobile', 'user_points',
                            'user_money', 'user_invite_code', 'created_time']


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
