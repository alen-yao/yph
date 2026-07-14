"""交易模块后台管理"""
from django.contrib import admin
from .models import Cart, Order, OrderItem, OrderLogistics, OrderReturn, OrderReturnReason


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_name', 'price', 'quantity', 'is_checked', 'created_time']
    list_filter = ['is_checked', 'created_time']
    search_fields = ['user__username', 'product_name']
    raw_id_fields = ['user']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product_name', 'sku_name', 'price', 'quantity', 'total_amount']
    readonly_fields = ['total_amount']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'user', 'order_amount', 'pay_amount',
                    'status', 'pay_type', 'created_time', 'pay_time']
    list_filter = ['status', 'pay_type', 'created_time', 'pay_time']
    search_fields = ['order_no', 'user__username', 'mobile', 'consignee']
    raw_id_fields = ['user']
    readonly_fields = ['order_no', 'created_time', 'pay_time', 'ship_time', 'finish_time', 'cancel_time']
    inlines = [OrderItemInline]

    fieldsets = (
        ('订单信息', {
            'fields': ('order_no', 'user', 'status', 'pay_type')
        }),
        ('金额信息', {
            'fields': ('order_amount', 'freight_amount', 'discount_amount', 'pay_amount')
        }),
        ('收货信息', {
            'fields': ('consignee', 'mobile', 'province', 'city', 'district', 'address')
        }),
        ('备注', {
            'fields': ('user_remark', 'admin_remark')
        }),
        ('时间信息', {
            'fields': ('created_time', 'pay_time', 'ship_time', 'finish_time', 'cancel_time')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_name', 'quantity', 'price', 'total_amount']
    search_fields = ['product_name', 'order__order_no']
    raw_id_fields = ['order']


@admin.register(OrderLogistics)
class OrderLogisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'express_company', 'express_no', 'express_time']
    search_fields = ['express_no', 'order__order_no']
    raw_id_fields = ['order']


@admin.register(OrderReturn)
class OrderReturnAdmin(admin.ModelAdmin):
    list_display = ['id', 'return_no', 'order', 'user', 'return_type',
                    'return_amount', 'status', 'created_time']
    list_filter = ['return_type', 'status', 'created_time']
    search_fields = ['return_no', 'order__order_no', 'user__username']
    raw_id_fields = ['order', 'order_item', 'user']


@admin.register(OrderReturnReason)
class OrderReturnReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'reason', 'sort_order', 'is_enable']
    list_filter = ['is_enable']
    list_editable = ['sort_order', 'is_enable']
