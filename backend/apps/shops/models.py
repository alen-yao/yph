"""店铺模块数据模型 - 参照 modulithshop shop 模块"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FavoritesItem(models.Model):
    """商品收藏"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    product_id = models.IntegerField(verbose_name='商品ID')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        db_table = 'favorites_item'
        verbose_name = '商品收藏'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'product_id']

    def __str__(self):
        return f'{self.user.username} - {self.product_id}'


class ProductBrowse(models.Model):
    """浏览历史"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='browse_history', verbose_name='用户')
    product_id = models.IntegerField(verbose_name='商品ID')
    browse_time = models.DateTimeField(auto_now=True, verbose_name='浏览时间')

    class Meta:
        db_table = 'product_browse'
        verbose_name = '浏览历史'
        verbose_name_plural = verbose_name
        ordering = ['-browse_time']

    def __str__(self):
        return f'{self.user.username} - {self.product_id}'


class SearchHistory(models.Model):
    """搜索历史"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history', verbose_name='用户')
    keyword = models.CharField(max_length=100, verbose_name='搜索关键词')
    search_time = models.DateTimeField(auto_now_add=True, verbose_name='搜索时间')

    class Meta:
        db_table = 'search_history'
        verbose_name = '搜索历史'
        verbose_name_plural = verbose_name
        ordering = ['-search_time']

    def __str__(self):
        return f'{self.user.username} - {self.keyword}'
