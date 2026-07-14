"""
商品模块数据模型
参照 ModulithShop pt (Product) 模块功能
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductCategory(models.Model):
    """
    商品分类
    对应 modulithshop 的 ProductCategory
    """
    name = models.CharField(max_length=100, verbose_name='分类名称')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='children', verbose_name='父分类')
    level = models.SmallIntegerField(default=1, verbose_name='分类层级')
    icon = models.ImageField(upload_to='products/categories/', null=True, blank=True, verbose_name='分类图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'product_category'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    """
    商品品牌
    对应 modulithshop 的 ProductBrand
    """
    name = models.CharField(max_length=100, verbose_name='品牌名称')
    logo = models.ImageField(upload_to='products/brands/', null=True, blank=True, verbose_name='品牌Logo')
    description = models.TextField(blank=True, verbose_name='品牌描述')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'product_brand'
        verbose_name = '商品品牌'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    商品基础信息
    对应 modulithshop 的 ProductBase
    """
    PRODUCT_STATE = (
        (0, '下架'),
        (1, '上架'),
    )

    name = models.CharField(max_length=200, verbose_name='商品名称')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 related_name='products', verbose_name='商品分类')
    brand = models.ForeignKey(ProductBrand, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='products', verbose_name='品牌')

    # 商品图片
    main_image = models.ImageField(upload_to='products/main/', verbose_name='主图')
    images = models.TextField(blank=True, verbose_name='商品图片列表(JSON)')

    # 商品详情
    description = models.TextField(blank=True, verbose_name='商品简介')
    detail_html = models.TextField(blank=True, verbose_name='商品详情HTML')

    # 价格和库存
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='销售价格')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价格')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='成本价')
    stock = models.IntegerField(default=0, verbose_name='总库存')

    # 销量和评分
    sales_count = models.IntegerField(default=0, verbose_name='销量')
    view_count = models.IntegerField(default=0, verbose_name='浏览量')
    favorite_count = models.IntegerField(default=0, verbose_name='收藏量')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=5.0, verbose_name='平均评分')

    # 状态
    state = models.SmallIntegerField(choices=PRODUCT_STATE, default=1, verbose_name='商品状态')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')

    # 排序和时间
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'product'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name


class ProductSpec(models.Model):
    """
    商品规格
    对应 modulithshop 的 ProductSpec
    """
    name = models.CharField(max_length=50, verbose_name='规格名称')
    sort_order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'product_spec'
        verbose_name = '商品规格'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class ProductSpecValue(models.Model):
    """
    商品规格值
    对应 modulithshop 的 ProductSpecItem
    """
    spec = models.ForeignKey(ProductSpec, on_delete=models.CASCADE,
                            related_name='values', verbose_name='所属规格')
    value = models.CharField(max_length=50, verbose_name='规格值')
    image = models.ImageField(upload_to='products/specs/', null=True, blank=True, verbose_name='规格图片')
    sort_order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'product_spec_value'
        verbose_name = '商品规格值'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.spec.name}:{self.value}'


class ProductItem(models.Model):
    """
    商品SKU
    对应 modulithshop 的 ProductItem
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                               related_name='items', verbose_name='商品')
    sku_code = models.CharField(max_length=50, unique=True, verbose_name='SKU编码')
    spec_values = models.TextField(verbose_name='规格值(JSON)')  # 存储规格值ID列表
    image = models.ImageField(upload_to='products/items/', null=True, blank=True, verbose_name='SKU图片')

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='成本价')
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales_count = models.IntegerField(default=0, verbose_name='销量')

    is_enable = models.BooleanField(default=True, verbose_name='是否启用')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'product_item'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f'{self.product.name} - {self.sku_code}'


class ProductComment(models.Model):
    """
    商品评论
    对应 modulithshop 的 ProductComment
    """
    COMMENT_LEVEL = (
        (1, '差评'),
        (2, '中评'),
        (3, '好评'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='商品')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name='product_comments', verbose_name='用户')
    order_id = models.IntegerField(verbose_name='订单ID')

    content = models.TextField(verbose_name='评论内容')
    images = models.TextField(blank=True, verbose_name='评论图片(JSON)')
    rating = models.SmallIntegerField(default=5, verbose_name='评分(1-5)')
    comment_level = models.SmallIntegerField(choices=COMMENT_LEVEL, default=3, verbose_name='评价等级')

    # 商家回复
    reply_content = models.TextField(blank=True, verbose_name='商家回复')
    reply_time = models.DateTimeField(null=True, blank=True, verbose_name='回复时间')

    # 统计
    helpful_count = models.IntegerField(default=0, verbose_name='有用数')

    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        db_table = 'product_comment'
        verbose_name = '商品评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class ProductTag(models.Model):
    """
    商品标签
    对应 modulithshop 的 ProductTag
    """
    name = models.CharField(max_length=50, verbose_name='标签名称')
    color = models.CharField(max_length=20, default='#FF0000', verbose_name='标签颜色')
    sort_order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'product_tag'
        verbose_name = '商品标签'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.name
