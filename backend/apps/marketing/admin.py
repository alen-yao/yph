"""营销模块后台管理"""
from django.contrib import admin
from .models import ActivityBase, Coupon, UserCoupon


@admin.register(ActivityBase)
class ActivityBaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'activity_name', 'activity_type', 'activity_state',
                    'start_time', 'end_time', 'is_enable']
    list_filter = ['activity_type', 'activity_state', 'is_enable']
    search_fields = ['activity_name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'coupon_name', 'coupon_type', 'coupon_price',
                    'total_quantity', 'received_quantity', 'is_enable']
    list_filter = ['coupon_type', 'is_enable']
    search_fields = ['coupon_name']


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'coupon', 'coupon_state', 'received_time']
    list_filter = ['coupon_state']
    search_fields = ['user__username']
    raw_id_fields = ['user', 'coupon']
