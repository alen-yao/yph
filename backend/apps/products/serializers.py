"""商品模块序列化器"""
from rest_framework import serializers
from .models import (Product, ProductCategory, ProductItem,
                     ProductSpec, ProductSpecValue, ProductComment, ProductTag)
from utils.minio_client import minio_client


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    region_code = serializers.CharField(source='region.code', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    cover_image = serializers.SerializerMethodField(help_text='封面图URL（第一张主图）')
    main_images = serializers.SerializerMethodField(help_text='主图URL列表')

    class Meta:
        model = Product
        fields = ['id', 'name', 'region_name', 'region_code', 'category_name',
                  'cover_image', 'main_images', 'price', 'market_price', 'sales_count',
                  'rating_average', 'is_recommend', 'is_new', 'is_hot', 'state']

    def get_cover_image(self, obj):
        """获取封面图完整URL"""
        if obj.main_images and len(obj.main_images) > 0:
            return minio_client.get_image_url(obj.main_images[0])
        return None

    def get_main_images(self, obj):
        """获取主图URL列表"""
        if obj.main_images:
            return [minio_client.get_image_url(key) for key in obj.main_images]
        return []


class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    region_code = serializers.CharField(source='region.code', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    cover_image = serializers.SerializerMethodField(help_text='封面图URL（第一张主图）')
    main_images = serializers.SerializerMethodField(help_text='主图URL列表')
    detail_images = serializers.SerializerMethodField(help_text='详情图URL列表')
    main_images_count = serializers.ReadOnlyField(help_text='主图数量')
    detail_images_count = serializers.ReadOnlyField(help_text='详情图数量')

    class Meta:
        model = Product
        fields = '__all__'

    def get_cover_image(self, obj):
        """获取封面图完整URL"""
        if obj.main_images and len(obj.main_images) > 0:
            return minio_client.get_image_url(obj.main_images[0])
        return None

    def get_main_images(self, obj):
        """获取主图URL列表"""
        if obj.main_images:
            return [minio_client.get_image_url(key) for key in obj.main_images]
        return []

    def get_detail_images(self, obj):
        """获取详情图URL列表"""
        if obj.detail_images:
            return [minio_client.get_image_url(key) for key in obj.detail_images]
        return []


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """商品创建和更新序列化器"""
    main_images = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        allow_empty=False,
        help_text='主图对象key列表，第一张为封面图（如：products/2026/08/abc123.jpg）'
    )
    detail_images = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        default=list,
        help_text='详情图对象key列表'
    )

    class Meta:
        model = Product
        fields = ['name', 'region', 'category', 'main_images', 'detail_images',
                  'description', 'detail_html', 'price', 'market_price',
                  'cost_price', 'stock', 'state', 'sort_order',
                  'is_recommend', 'is_new', 'is_hot']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('价格必须大于0')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('库存不能为负数')
        return value

    def validate_main_images(self, value):
        if not value:
            raise serializers.ValidationError('请至少添加一张主图')
        if len(value) > 5:
            raise serializers.ValidationError('主图最多5张')
        return value

    def validate_detail_images(self, value):
        if value and len(value) > 20:
            raise serializers.ValidationError('详情图最多20张')
        return value or []

    def create(self, validated_data):
        # 确保图片字段是列表类型
        if 'main_images' not in validated_data:
            validated_data['main_images'] = []
        if 'detail_images' not in validated_data:
            validated_data['detail_images'] = []
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 确保图片字段是列表类型
        if 'main_images' in validated_data and validated_data['main_images'] is None:
            validated_data['main_images'] = []
        if 'detail_images' in validated_data and validated_data['detail_images'] is None:
            validated_data['detail_images'] = []
        return super().update(instance, validated_data)


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = '__all__'


class ProductCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.nickname', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)

    class Meta:
        model = ProductComment
        fields = '__all__'
