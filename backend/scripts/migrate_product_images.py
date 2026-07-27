#!/usr/bin/env python
"""
迁移脚本：将旧的产品图片字段转换为新的 main_images 和 detail_images 结构

使用方法:
    python scripts/migrate_product_images.py
"""
import os
import sys
import django
import json

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yph.settings')
django.setup()

from apps.products.models import Product


def migrate_old_images():
    """
    迁移旧的图片数据到新结构

    假设旧数据库中有：
    - main_image (ImageField): 单张主图
    - images (TextField): JSON字符串，存储多张图片
    """
    print("=" * 60)
    print("开始迁移产品图片数据")
    print("=" * 60)

    products = Product.objects.all()
    total = products.count()

    if total == 0:
        print("\n未找到需要迁移的商品数据")
        return

    print(f"\n找到 {total} 个商品需要迁移\n")

    success_count = 0
    error_count = 0

    for index, product in enumerate(products, 1):
        try:
            print(f"[{index}/{total}] 迁移商品: {product.name} (ID: {product.id})")

            # 初始化新字段
            new_main_images = []
            new_detail_images = []

            # 迁移 main_image (如果存在旧字段)
            if hasattr(product, 'main_image') and product.main_image:
                # 假设旧的 ImageField 已经是 URL 或本地路径
                old_url = product.main_image.url if hasattr(product.main_image, 'url') else str(product.main_image)
                new_main_images.append(old_url)
                print(f"  - 迁移主图: {old_url}")

            # 迁移 images (如果存在旧字段)
            if hasattr(product, 'images') and product.images:
                try:
                    # 尝试解析 JSON
                    old_images = json.loads(product.images) if isinstance(product.images, str) else product.images

                    if isinstance(old_images, list):
                        # 假设前3张为主图，其余为详情图
                        for img_url in old_images[:3]:
                            if img_url not in new_main_images:
                                new_main_images.append(img_url)

                        for img_url in old_images[3:]:
                            new_detail_images.append(img_url)

                        print(f"  - 迁移 {len(old_images)} 张图片")
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"  ⚠ 警告: 解析旧图片数据失败: {e}")

            # 确保至少有一张主图（使用占位符）
            if not new_main_images:
                new_main_images = []
                print(f"  ⚠ 警告: 商品没有主图")

            # 更新商品
            product.main_images = new_main_images
            product.detail_images = new_detail_images
            product.save(update_fields=['main_images', 'detail_images'])

            print(f"  ✓ 成功: 主图 {len(new_main_images)} 张, 详情图 {len(new_detail_images)} 张")
            success_count += 1

        except Exception as e:
            print(f"  ✗ 错误: {e}")
            error_count += 1

    # 统计结果
    print("\n" + "=" * 60)
    print("迁移完成!")
    print("=" * 60)
    print(f"总计: {total} 个商品")
    print(f"成功: {success_count} 个")
    print(f"失败: {error_count} 个")
    print("=" * 60)


def create_sample_products():
    """创建示例商品数据（用于测试）"""
    print("\n创建示例商品数据...")

    try:
        from apps.products.models import ProductCategory, ProductBrand

        # 创建分类
        category, _ = ProductCategory.objects.get_or_create(
            name='测试分类',
            defaults={'sort_order': 1, 'is_show': True}
        )

        # 创建品牌
        brand, _ = ProductBrand.objects.get_or_create(
            name='测试品牌',
            defaults={'sort_order': 1, 'is_show': True}
        )

        # 创建示例商品
        product = Product.objects.create(
            name='示例商品 - iPhone 15',
            category=category,
            brand=brand,
            price=8999.00,
            market_price=9999.00,
            stock=100,
            main_images=[
                'http://localhost:9000/yph-products/products/main/sample1.jpg',
                'http://localhost:9000/yph-products/products/main/sample2.jpg',
                'http://localhost:9000/yph-products/products/main/sample3.jpg',
            ],
            detail_images=[
                'http://localhost:9000/yph-products/products/detail/d1.jpg',
                'http://localhost:9000/yph-products/products/detail/d2.jpg',
                'http://localhost:9000/yph-products/products/detail/d3.jpg',
            ],
            description='这是一个示例商品，展示多图片结构',
            state=1,
        )

        print(f"✓ 创建示例商品成功: {product.name} (ID: {product.id})")
        print(f"  - 封面图: {product.cover_image}")
        print(f"  - 主图数量: {product.main_images_count}")
        print(f"  - 详情图数量: {product.detail_images_count}")

    except Exception as e:
        print(f"✗ 创建示例商品失败: {e}")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='产品图片数据迁移脚本')
    parser.add_argument('--migrate', action='store_true', help='执行迁移')
    parser.add_argument('--sample', action='store_true', help='创建示例数据')

    args = parser.parse_args()

    if args.sample:
        create_sample_products()
    elif args.migrate:
        migrate_old_images()
    else:
        print("使用方法:")
        print("  python scripts/migrate_product_images.py --migrate  # 迁移旧数据")
        print("  python scripts/migrate_product_images.py --sample   # 创建示例数据")


if __name__ == '__main__':
    main()
