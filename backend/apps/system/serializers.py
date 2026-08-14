from rest_framework import serializers
from .models import UserRole, Banner, Region
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


class RegionSerializer(serializers.ModelSerializer):
    """地区序列化器"""
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ['id', 'code', 'name', 'icon', 'sort_order', 'status',
                  'products_count', 'created_time', 'updated_time']
        read_only_fields = ['created_time', 'updated_time']

    def get_products_count(self, obj):
        """获取该地区下的商品数量"""
        return obj.products.filter(state=1).count()


class RegionListSerializer(serializers.ModelSerializer):
    """地区列表序列化器（简化版，用于下拉选择等）"""
    class Meta:
        model = Region
        fields = ['id', 'code', 'name', 'icon', 'status']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class ImageUploadSerializer(serializers.Serializer):
    """图片上传序列化器"""
    file = serializers.ImageField(required=True, help_text='图片文件')
    folder = serializers.CharField(
        required=False,
        default='products',
        help_text='存储文件夹，如：products, banners, avatars'
    )

    def validate_file(self, value):
        """验证文件"""
        # 限制文件大小为10MB
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('图片大小不能超过10MB')

        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError('只支持 JPEG, PNG, GIF, WebP 格式的图片')

        return value


class MultipleImageUploadSerializer(serializers.Serializer):
    """批量图片上传序列化器"""
    files = serializers.ListField(
        child=serializers.ImageField(),
        required=True,
        help_text='图片文件列表'
    )
    folder = serializers.CharField(
        required=False,
        default='products',
        help_text='存储文件夹'
    )

    def validate_files(self, value):
        """验证文件列表"""
        if len(value) > 10:
            raise serializers.ValidationError('一次最多上传10张图片')

        for file in value:
            if file.size > 10 * 1024 * 1024:
                raise serializers.ValidationError(f'图片 {file.name} 大小超过10MB')

            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if file.content_type not in allowed_types:
                raise serializers.ValidationError(f'图片 {file.name} 格式不支持')

        return value
