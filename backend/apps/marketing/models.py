"""营销模块数据模型 - 参照 modulithshop marketing 模块"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ActivityBase(models.Model):
    """活动基础表 - 对应 ActivityBase"""
    ACTIVITY_TYPE = (
        (1, '优惠券'),
        (2, '秒杀'),
        (3, '拼团'),
        (4, '砍价'),
        (5, '满减'),
    )

    ACTIVITY_STATE = (
        (0, '未开始'),
        (1, '进行中'),
        (2, '已结束'),
        (3, '已取消'),
    )

    activity_name = models.CharField(max_length=100, verbose_name='活动名称')
    activity_type = models.SmallIntegerField(choices=ACTIVITY_TYPE, verbose_name='活动类型')
    activity_state = models.SmallIntegerField(choices=ACTIVITY_STATE, default=0, verbose_name='活动状态')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    activity_desc = models.TextField(blank=True, verbose_name='活动描述')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'activity_base'
        verbose_name = '营销活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity_name


class Coupon(models.Model):
    """优惠券"""
    COUPON_TYPE = ((1, '满减券'), (2, '折扣券'), (3, '兑换券'))

    activity = models.ForeignKey(ActivityBase, on_delete=models.CASCADE, related_name='coupons', verbose_name='所属活动')
    coupon_name = models.CharField(max_length=100, verbose_name='优惠券名称')
    coupon_type = models.SmallIntegerField(choices=COUPON_TYPE, verbose_name='类型')
    coupon_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='优惠金额')
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='最低消费')
    total_quantity = models.IntegerField(verbose_name='总量')
    received_quantity = models.IntegerField(default=0, verbose_name='已领取')
    per_user_limit = models.IntegerField(default=1, verbose_name='限领')
    valid_days = models.IntegerField(verbose_name='有效天数')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        db_table = 'coupon'
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name


class UserCoupon(models.Model):
    """用户优惠券"""
    COUPON_STATE = ((0, '未使用'), (1, '已使用'), (2, '已过期'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons', verbose_name='用户')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, verbose_name='优惠券')
    coupon_state = models.SmallIntegerField(choices=COUPON_STATE, default=0, verbose_name='状态')
    order_id = models.IntegerField(null=True, blank=True, verbose_name='订单ID')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    received_time = models.DateTimeField(auto_now_add=True, verbose_name='领取时间')

    class Meta:
        db_table = 'user_coupon'
        verbose_name = '用户优惠券'
        verbose_name_plural = verbose_name
