#!/usr/bin/env python
"""设置MinIO bucket为公开访问"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yph.settings')
django.setup()

from utils.minio_client import minio_client


def main():
    print("=" * 60)
    print("设置 MinIO Bucket 为公开访问")
    print("=" * 60)

    print(f"\n当前配置:")
    print(f"  Endpoint: {minio_client.endpoint}")
    print(f"  Bucket: {minio_client.bucket_name}")
    print(f"  Public URL: {minio_client.public_url}")

    # 检查bucket是否存在
    print(f"\n检查bucket是否存在...")
    if not minio_client.client.bucket_exists(minio_client.bucket_name):
        print(f"✗ Bucket '{minio_client.bucket_name}' 不存在")
        print(f"  请先创建bucket或运行 python test_minio.py")
        return

    print(f"✓ Bucket '{minio_client.bucket_name}' 存在")

    # 设置为公开
    print(f"\n设置bucket为公开读取...")
    try:
        minio_client.set_bucket_public()
        print(f"✓ 成功设置bucket为公开访问!")

        print(f"\n公开策略已应用:")
        print(f"  - 任何人都可以通过URL直接访问bucket中的文件")
        print(f"  - 无需认证，URL永不过期")
        print(f"  - 适合存储商品图片等公开资源")

        print(f"\n测试URL（如果文件存在）:")
        print(f"  {minio_client.public_url}/{minio_client.bucket_name}/products/test.jpg")

        print(f"\n" + "=" * 60)
        print("设置完成!")
        print("=" * 60)

    except Exception as e:
        print(f"✗ 设置失败: {e}")
        print(f"\n可能的原因:")
        print(f"  1. MinIO服务未启动")
        print(f"  2. 访问凭证不正确")
        print(f"  3. 网络连接问题")
        return


if __name__ == '__main__':
    main()
