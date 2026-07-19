from rest_framework import serializers
from .models import UserRole, Banner
import json


class UserRoleSerializer(serializers.ModelSerializer):
    """用户角色序列化器"""
    permissions_data = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = ['id', 'name', 'description', 'permissions', 'permissions_data',
                  'is_active', 'user_count', 'created_time', 'updated_time']
        read_only_fields = ['created_time', 'updated_time']

    def get_permissions_data(self, obj):
        """解析权限JSON为字典"""
        return obj.get_permissions()

    def get_user_count(self, obj):
        """获取该角色下的用户数量"""
        return obj.users.count()

    def validate_permissions(self, value):
        """验证permissions字段是否为有效JSON"""
        if isinstance(value, str):
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('权限配置必须是有效的JSON格式')
        return value

    def create(self, validated_data):
        """创建角色时处理permissions"""
        if 'permissions' in validated_data and isinstance(validated_data['permissions'], dict):
            validated_data['permissions'] = json.dumps(validated_data['permissions'], ensure_ascii=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """更新角色时处理permissions"""
        if 'permissions' in validated_data and isinstance(validated_data['permissions'], dict):
            validated_data['permissions'] = json.dumps(validated_data['permissions'], ensure_ascii=False)
        return super().update(instance, validated_data)


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
