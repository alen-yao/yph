"""
用户模块数据模型
参照 ModulithShop account 模块功能
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    用户模型 - 扩展Django内置用户模型
    对应 modulithshop 的 UserInfo
    """
    GENDER_CHOICES = (
        (0, '保密'),
        (1, '男'),
        (2, '女'),
    )

    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name='头像')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')

    # 第三方登录
    wechat_openid = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='微信OpenID')
    wechat_unionid = models.CharField(max_length=100, null=True, blank=True, verbose_name='微信UnionID')

    # 会员相关
    user_level_id = models.IntegerField(default=1, verbose_name='会员等级ID')
    user_points = models.IntegerField(default=0, verbose_name='积分')
    user_money = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='余额')

    # 推广相关
    user_parent_id = models.IntegerField(default=0, verbose_name='推荐人ID')
    user_invite_code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='邀请码')

    # 状态
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    # 时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


class UserLevel(models.Model):
    """
    用户等级
    对应 modulithshop 的 UserLevel
    """
    level_name = models.CharField(max_length=50, verbose_name='等级名称')
    level_discount = models.DecimalField(max_digits=3, decimal_places=2, default=1.00, verbose_name='折扣率')
    min_points = models.IntegerField(default=0, verbose_name='所需最低积分')
    max_points = models.IntegerField(default=0, verbose_name='所需最高积分')
    level_icon = models.ImageField(upload_to='users/levels/', null=True, blank=True, verbose_name='等级图标')
    is_default = models.BooleanField(default=False, verbose_name='是否默认等级')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'user_level'
        verbose_name = '用户等级'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.level_name


class DeliveryAddress(models.Model):
    """
    收货地址
    对应 modulithshop 的 UserDeliveryAddress
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    consignee = models.CharField(max_length=50, verbose_name='收货人')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    province = models.CharField(max_length=50, verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    district = models.CharField(max_length=50, verbose_name='区/县')
    address = models.CharField(max_length=200, verbose_name='详细地址')
    zipcode = models.CharField(max_length=10, blank=True, verbose_name='邮编')
    is_default = models.BooleanField(default=False, verbose_name='是否默认地址')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'delivery_address'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-id']

    def __str__(self):
        return f'{self.consignee} - {self.mobile}'


class UserMessage(models.Model):
    """
    用户消息
    对应 modulithshop 的 UserMessage
    """
    MESSAGE_TYPE = (
        (1, '系统消息'),
        (2, '订单消息'),
        (3, '活动消息'),
        (4, '物流消息'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='用户')
    message_type = models.SmallIntegerField(choices=MESSAGE_TYPE, default=1, verbose_name='消息类型')
    title = models.CharField(max_length=100, verbose_name='消息标题')
    content = models.TextField(verbose_name='消息内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'user_message'
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title


class UserPointsHistory(models.Model):
    """
    积分历史
    """
    POINTS_TYPE = (
        (1, '订单获得'),
        (2, '签到获得'),
        (3, '消费扣除'),
        (4, '后台调整'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_history', verbose_name='用户')
    points = models.IntegerField(verbose_name='积分变动')
    points_type = models.SmallIntegerField(choices=POINTS_TYPE, verbose_name='积分类型')
    description = models.CharField(max_length=200, verbose_name='说明')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'user_points_history'
        verbose_name = '积分历史'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.user.username} - {self.points}'


class UserLoginHistory(models.Model):
    """
    登录历史
    对应 modulithshop 的 UserLoginHistory
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history', verbose_name='用户')
    login_ip = models.GenericIPAddressField(verbose_name='登录IP')
    login_device = models.CharField(max_length=50, blank=True, verbose_name='登录设备')
    login_os = models.CharField(max_length=50, blank=True, verbose_name='操作系统')
    login_browser = models.CharField(max_length=50, blank=True, verbose_name='浏览器')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    class Meta:
        db_table = 'user_login_history'
        verbose_name = '登录历史'
        verbose_name_plural = verbose_name
        ordering = ['-login_time']

    def __str__(self):
        return f'{self.user.username} - {self.login_time}'
