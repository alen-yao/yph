from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='品牌名称')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='products/brands/', verbose_name='品牌Logo')),
                ('description', models.TextField(blank=True, verbose_name='品牌描述')),
                ('sort_order', models.IntegerField(default=0, verbose_name='排序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '商品品牌',
                'verbose_name_plural': '商品品牌',
                'db_table': 'product_brand',
                'ordering': ['sort_order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='分类名称')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='products/categories/', verbose_name='分类图标')),
                ('sort_order', models.IntegerField(default=0, verbose_name='排序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'db_table': 'product_category',
                'ordering': ['sort_order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='商品名称')),
                ('main_images', models.JSONField(default=list, help_text='商品主图URL列表，第一张为封面图，用于列表展示和详情页轮播', verbose_name='主图列表')),
                ('detail_images', models.JSONField(default=list, help_text='商品详情页图片URL列表，按顺序展示', verbose_name='详情图列表')),
                ('description', models.TextField(blank=True, verbose_name='商品简介')),
                ('detail_html', models.TextField(blank=True, help_text='富文本编辑器内容，可选', verbose_name='商品详情HTML')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='销售价格')),
                ('market_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='市场价格')),
                ('cost_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='成本价')),
                ('stock', models.IntegerField(default=0, verbose_name='总库存')),
                ('sales_count', models.IntegerField(default=0, verbose_name='销量')),
                ('view_count', models.IntegerField(default=0, verbose_name='浏览量')),
                ('favorite_count', models.IntegerField(default=0, verbose_name='收藏量')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
                ('rating_average', models.DecimalField(decimal_places=2, default=5.0, max_digits=3, verbose_name='平均评分')),
                ('state', models.SmallIntegerField(choices=[(0, '下架'), (1, '上架')], default=1, verbose_name='商品状态')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='是否推荐')),
                ('is_new', models.BooleanField(default=False, verbose_name='是否新品')),
                ('is_hot', models.BooleanField(default=False, verbose_name='是否热销')),
                ('sort_order', models.IntegerField(default=0, verbose_name='排序')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.productbrand', verbose_name='品牌')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productcategory', verbose_name='商品分类')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='system.region', verbose_name='所属地区')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'db_table': 'product',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='规格名称')),
                ('sort_order', models.IntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '商品规格',
                'verbose_name_plural': '商品规格',
                'db_table': 'product_spec',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='标签名称')),
                ('color', models.CharField(default='#FF0000', max_length=20, verbose_name='标签颜色')),
                ('sort_order', models.IntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '商品标签',
                'verbose_name_plural': '商品标签',
                'db_table': 'product_tag',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='ProductSpecValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, verbose_name='规格值')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/specs/', verbose_name='规格图片')),
                ('sort_order', models.IntegerField(default=0, verbose_name='排序')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='products.productspec', verbose_name='所属规格')),
            ],
            options={
                'verbose_name': '商品规格值',
                'verbose_name_plural': '商品规格值',
                'db_table': 'product_spec_value',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_code', models.CharField(max_length=50, unique=True, verbose_name='SKU编码')),
                ('spec_values', models.TextField(verbose_name='规格值(JSON)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/items/', verbose_name='SKU图片')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('cost_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='成本价')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sales_count', models.IntegerField(default=0, verbose_name='销量')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='products.product', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
                'db_table': 'product_item',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(verbose_name='订单ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('images', models.TextField(blank=True, verbose_name='评论图片(JSON)')),
                ('rating', models.SmallIntegerField(default=5, verbose_name='评分(1-5)')),
                ('comment_level', models.SmallIntegerField(choices=[(1, '差评'), (2, '中评'), (3, '好评')], default=3, verbose_name='评价等级')),
                ('reply_content', models.TextField(blank=True, verbose_name='商家回复')),
                ('reply_time', models.DateTimeField(blank=True, null=True, verbose_name='回复时间')),
                ('helpful_count', models.IntegerField(default=0, verbose_name='有用数')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.product', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_comments', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '商品评论',
                'verbose_name_plural': '商品评论',
                'db_table': 'product_comment',
                'ordering': ['-created_time'],
            },
        ),
    ]
