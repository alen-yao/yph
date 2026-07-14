"""支付模块数据模型 - 参照 modulithshop pay 模块"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentOrder(models.Model):
    """支付订单"""
    PAY_TYPE = (
        (1, '微信支付'),
        (2, '支付宝'),
        (3, '余额支付'),
    )

    PAY_STATE = (
        (0, '未支付'),
        (1, '支付成功'),
        (2, '支付失败'),
    )

    payment_no = models.CharField(max_length=50, unique=True, verbose_name='支付单号')
    order_id = models.IntegerField(verbose_name='订单ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    pay_type = models.SmallIntegerField(choices=PAY_TYPE, verbose_name='支付方式')
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    pay_state = models.SmallIntegerField(choices=PAY_STATE, default=0, verbose_name='支付状态')

    # 第三方支付信息
    trade_no = models.CharField(max_length=100, blank=True, verbose_name='第三方交易号')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'payment_order'
        verbose_name = '支付订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.payment_no


class PaymentConfig(models.Model):
    """支付配置"""
    config_name = models.CharField(max_length=50, verbose_name='配置名称')
    pay_type = models.SmallIntegerField(verbose_name='支付类型')
    app_id = models.CharField(max_length=100, blank=True, verbose_name='应用ID')
    mch_id = models.CharField(max_length=100, blank=True, verbose_name='商户号')
    api_key = models.CharField(max_length=200, blank=True, verbose_name='API密钥')
    notify_url = models.CharField(max_length=200, blank=True, verbose_name='回调地址')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')

    class Meta:
        db_table = 'payment_config'
        verbose_name = '支付配置'
        verbose_name_plural = verbose_name
