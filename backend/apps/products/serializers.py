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
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'brand_name', 'main_image',
                  'price', 'market_price', 'sales_count', 'rating_average']


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """商品创建和更新序列化器"""

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'main_image', 'description',
                  'price', 'market_price', 'cost_price', 'stock', 'state',
                  'sort_order', 'is_recommend', 'is_new', 'is_hot']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('价格必须大于0')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('库存不能为负数')
        return value


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
