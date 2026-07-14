"""商品模块后台管理"""
from django.contrib import admin
from .models import (Product, ProductCategory, ProductBrand, ProductItem,
                     ProductSpec, ProductSpecValue, ProductComment, ProductTag)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'level', 'sort_order', 'is_show']
    list_filter = ['level', 'is_show']
    search_fields = ['name']


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sort_order', 'is_show']
    list_filter = ['is_show']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'brand', 'price', 'stock', 'sales_count', 'state']
    list_filter = ['state', 'category', 'brand']
    search_fields = ['name']


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'sku_code', 'price', 'stock', 'sales_count']
    search_fields = ['sku_code']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating', 'is_show', 'created_time']
    list_filter = ['rating', 'is_show']
