"""系统模块数据模型"""
from django.db import models
import json


class UserRole(models.Model):
    """
    用户角色/类别
    用于管理后台的权限控制
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.CharField(max_length=200, blank=True, verbose_name='角色描述')
    permissions = models.TextField(default='{}', verbose_name='权限配置(JSON)')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_role'
        verbose_name = '用户角色'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_permissions(self):
        """获取权限配置"""
        try:
            return json.loads(self.permissions)
        except:
            return {}

    def set_permissions(self, permissions_dict):
        """设置权限配置"""
        self.permissions = json.dumps(permissions_dict, ensure_ascii=False)


class SystemConfig(models.Model):
    """系统配置"""
    CONFIG_TYPE = (
        (1, '基础配置'),
        (2, '上传配置'),
        (3, '短信配置'),
        (4, '支付配置'),
    )

    config_key = models.CharField(max_length=50, unique=True, verbose_name='配置键')
    config_value = models.TextField(verbose_name='配置值')
    config_type = models.SmallIntegerField(choices=CONFIG_TYPE, default=1, verbose_name='配置类型')
    config_desc = models.CharField(max_length=200, blank=True, verbose_name='配置说明')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'system_config'
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.config_key


class Banner(models.Model):
    """轮播图"""
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banners/', verbose_name='图片')
    link_type = models.SmallIntegerField(default=1, verbose_name='链接类型')
    link_url = models.CharField(max_length=200, blank=True, verbose_name='链接地址')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.title
