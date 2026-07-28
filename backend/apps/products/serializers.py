"""商品模块序列化器"""
from rest_framework import serializers
from .models import (Product, ProductCategory, ProductBrand, ProductItem,
                     ProductSpec, ProductSpecValue, ProductComment, ProductTag)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    cover_image = serializers.ReadOnlyField(help_text='封面图（第一张主图）')

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'brand_name', 'cover_image', 'main_images',
                  'price', 'market_price', 'sales_count', 'rating_average',
                  'is_recommend', 'is_new', 'is_hot', 'state']


class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    cover_image = serializers.ReadOnlyField(help_text='封面图（第一张主图）')
    main_images_count = serializers.ReadOnlyField(help_text='主图数量')
    detail_images_count = serializers.ReadOnlyField(help_text='详情图数量')

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """商品创建和更新序列化器"""
    main_images = serializers.ListField(
        child=serializers.URLField(),
        required=True,
        allow_empty=False,
        help_text='主图URL列表，第一张为封面图'
    )
    detail_images = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        allow_empty=True,
        default=list,
        help_text='详情图URL列表'
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'main_images', 'detail_images',
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
