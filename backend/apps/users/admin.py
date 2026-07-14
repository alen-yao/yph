"""
用户模块后台管理
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserLevel, DeliveryAddress, UserMessage, UserPointsHistory, UserLoginHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'mobile', 'nickname', 'user_level_id',
                    'user_points', 'user_money', 'is_active', 'created_time']
    list_filter = ['is_active', 'user_level_id', 'created_time']
    search_fields = ['username', 'mobile', 'nickname']
    readonly_fields = ['created_time', 'updated_time']

    fieldsets = (
        ('基本信息', {'fields': ('username', 'password', 'mobile', 'email')}),
        ('个人信息', {'fields': ('nickname', 'avatar', 'gender', 'birthday')}),
        ('会员信息', {'fields': ('user_level_id', 'user_points', 'user_money')}),
        ('推广信息', {'fields': ('user_parent_id', 'user_invite_code')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('时间', {'fields': ('created_time', 'updated_time', 'last_login')}),
    )


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'level_name', 'level_discount', 'min_points', 'max_points',
                    'is_default', 'sort_order']
    list_filter = ['is_default']
    search_fields = ['level_name']


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'consignee', 'mobile', 'province', 'city',
                    'district', 'is_default', 'created_time']
    list_filter = ['is_default', 'province', 'city']
    search_fields = ['consignee', 'mobile', 'address']
    raw_id_fields = ['user']


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message_type', 'title', 'is_read', 'created_time']
    list_filter = ['message_type', 'is_read', 'created_time']
    search_fields = ['title', 'content']
    raw_id_fields = ['user']


@admin.register(UserPointsHistory)
class UserPointsHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'points', 'points_type', 'description', 'created_time']
    list_filter = ['points_type', 'created_time']
    search_fields = ['description']
    raw_id_fields = ['user']


@admin.register(UserLoginHistory)
class UserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'login_ip', 'login_device', 'login_time']
    list_filter = ['login_time']
    search_fields = ['login_ip']
    raw_id_fields = ['user']
