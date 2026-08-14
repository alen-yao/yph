from django.contrib import admin
from .models import Region, UserRole, SystemConfig, Banner


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'icon', 'sort_order', 'status', 'created_time']
    list_filter = ['status', 'created_time']
    search_fields = ['name', 'code']
    list_editable = ['sort_order', 'status']
    ordering = ['sort_order', 'id']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_active', 'created_time']
    list_filter = ['is_active', 'created_time']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'config_key', 'config_type', 'is_enable', 'updated_time']
    list_filter = ['config_type', 'is_enable']
    search_fields = ['config_key', 'config_value', 'config_desc']
    list_editable = ['is_enable']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'sort_order', 'is_show', 'created_time']
    list_filter = ['is_show', 'created_time']
    search_fields = ['title']
    list_editable = ['sort_order', 'is_show']
    ordering = ['sort_order', '-created_time']
