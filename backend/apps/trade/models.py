"""交易模块数据模型 - 参照 modulithshop trade 模块"""
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Cart(models.Model):
    """购物车 - 对应 UserCart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', verbose_name='用户')
    product_id = models.IntegerField(verbose_name='商品ID')
    product_item_id = models.IntegerField(verbose_name='商品SKU ID')
    product_name = models.CharField(max_length=200, verbose_name='商品名称')
    product_image = models.CharField(max_length=500, blank=True, verbose_name='商品图片')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    is_checked = models.BooleanField(default=True, verbose_name='是否选中')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def subtotal(self):
        """小计"""
        return self.price * self.quantity


class Order(models.Model):
    """订单 - 对应 OrderBase"""
    ORDER_STATUS = (
        (0, '待支付'),
        (1, '待发货'),
        (2, '待收货'),
        (3, '已完成'),
        (4, '已取消'),
        (5, '退款中'),
        (6, '已退款'),
    )

    PAY_TYPE = (
        (1, '微信支付'),
        (2, '支付宝'),
        (3, '余额支付'),
        (4, '货到付款'),
    )

    order_no = models.CharField(max_length=50, unique=True, verbose_name='订单号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')

    # 金额
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总金额')
    freight_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='运费')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='优惠金额')
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实付金额')

    # 状态
    status = models.SmallIntegerField(choices=ORDER_STATUS, default=0, verbose_name='订单状态')
    pay_type = models.SmallIntegerField(choices=PAY_TYPE, null=True, blank=True, verbose_name='支付方式')

    # 收货信息
    consignee = models.CharField(max_length=50, verbose_name='收货人')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    province = models.CharField(max_length=50, verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    district = models.CharField(max_length=50, verbose_name='区/县')
    address = models.CharField(max_length=200, verbose_name='详细地址')

    # 备注和时间
    user_remark = models.TextField(blank=True, verbose_name='买家备注')
    admin_remark = models.TextField(blank=True, verbose_name='管理员备注')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    ship_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    cancel_time = models.DateTimeField(null=True, blank=True, verbose_name='取消时间')

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    """订单商品 - 对应 OrderItem"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product_id = models.IntegerField(verbose_name='商品ID')
    product_name = models.CharField(max_length=200, verbose_name='商品名称')
    product_image = models.CharField(max_length=500, verbose_name='商品图片')
    product_item_id = models.IntegerField(verbose_name='SKU ID')
    sku_name = models.CharField(max_length=200, verbose_name='SKU名称')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    quantity = models.IntegerField(verbose_name='数量')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')

    # 售后
    is_comment = models.BooleanField(default=False, verbose_name='是否已评价')
    is_return = models.BooleanField(default=False, verbose_name='是否退货')

    class Meta:
        db_table = 'order_item'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name


class OrderLogistics(models.Model):
    """订单物流 - 对应 OrderLogistics"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='logistics', verbose_name='订单')
    express_company = models.CharField(max_length=50, blank=True, verbose_name='物流公司')
    express_no = models.CharField(max_length=50, blank=True, verbose_name='物流单号')
    express_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    logistics_info = models.TextField(blank=True, verbose_name='物流信息(JSON)')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order_logistics'
        verbose_name = '订单物流'
        verbose_name_plural = verbose_name


class OrderReturn(models.Model):
    """退货/退款 - 对应 OrderReturn"""
    RETURN_TYPE = (
        (1, '仅退款'),
        (2, '退货退款'),
    )

    RETURN_STATUS = (
        (0, '待审核'),
        (1, '审核通过'),
        (2, '审核拒绝'),
        (3, '退货中'),
        (4, '已完成'),
    )

    return_no = models.CharField(max_length=50, unique=True, verbose_name='退款单号')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns', verbose_name='订单')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, verbose_name='订单商品')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    return_type = models.SmallIntegerField(choices=RETURN_TYPE, verbose_name='退款类型')
    return_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='退款金额')
    return_reason = models.CharField(max_length=200, verbose_name='退款原因')
    return_description = models.TextField(blank=True, verbose_name='退款说明')
    return_images = models.TextField(blank=True, verbose_name='凭证图片(JSON)')

    status = models.SmallIntegerField(choices=RETURN_STATUS, default=0, verbose_name='状态')
    admin_remark = models.TextField(blank=True, verbose_name='管理员备注')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'order_return'
        verbose_name = '退货退款'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


class OrderReturnReason(models.Model):
    """退货原因 - 对应 OrderReturnReason"""
    reason = models.CharField(max_length=100, verbose_name='退货原因')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        db_table = 'order_return_reason'
        verbose_name = '退货原因'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.reason
