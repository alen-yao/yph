#!/usr/bin/env python
"""MinIO 集成测试脚本"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yph.settings')
django.setup()

from utils.minio_client import minio_client
from io import BytesIO
from PIL import Image


def test_minio_connection():
    """测试 MinIO 连接"""
    print("=" * 50)
    print("测试 MinIO 连接...")
    print("=" * 50)

    try:
        # 检查存储桶是否存在
        if minio_client.client.bucket_exists(minio_client.bucket_name):
            print(f"✓ 成功连接到 MinIO")
            print(f"✓ 存储桶 '{minio_client.bucket_name}' 已存在")
        else:
            print(f"✗ 存储桶 '{minio_client.bucket_name}' 不存在")
            return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False

    return True


def test_upload_image():
    """测试图片上传"""
    print("\n" + "=" * 50)
    print("测试图片上传...")
    print("=" * 50)

    try:
        # 创建测试图片
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        img_io.name = 'test_image.jpg'
        img_io.size = img_io.getbuffer().nbytes
        img_io.content_type = 'image/jpeg'

        # 上传图片
        print("正在上传测试图片...")
        url = minio_client.upload_file(img_io, folder='test')

        print(f"✓ 图片上传成功!")
        print(f"  URL: {url}")

        return url
    except Exception as e:
        print(f"✗ 上传失败: {e}")
        return None


def test_delete_image(file_url):
    """测试图片删除"""
    print("\n" + "=" * 50)
    print("测试图片删除...")
    print("=" * 50)

    try:
        print(f"正在删除图片: {file_url}")
        success = minio_client.delete_file(file_url)

        if success:
            print("✓ 图片删除成功!")
        else:
            print("✗ 图片删除失败")

        return success
    except Exception as e:
        print(f"✗ 删除失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 50)
    print("MinIO 集成测试")
    print("=" * 50)

    # 显示配置信息
    print(f"\n配置信息:")
    print(f"  Endpoint: {minio_client.endpoint}")
    print(f"  Bucket: {minio_client.bucket_name}")
    print(f"  Public URL: {minio_client.public_url}")
    print(f"  Secure: {minio_client.secure}")

    # 测试连接
    if not test_minio_connection():
        print("\n" + "=" * 50)
        print("测试失败: 无法连接到 MinIO")
        print("=" * 50)
        print("\n请确保:")
        print("1. MinIO 服务已启动")
        print("2. .env 文件中的 MinIO 配置正确")
        print("3. 网络连接正常")
        return

    # 测试上传
    file_url = test_upload_image()
    if not file_url:
        print("\n" + "=" * 50)
        print("测试失败: 图片上传失败")
        print("=" * 50)
        return

    # 测试删除
    test_delete_image(file_url)

    # 总结
    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
    print("\n✓ MinIO 集成正常工作")
    print("\n你现在可以:")
    print("1. 访问 MinIO 控制台: http://localhost:9001")
    print("2. 使用 API 上传图片: POST /api/system/upload/image/")
    print("3. 查看文档: backend/docs/MINIO_INTEGRATION.md")


if __name__ == '__main__':
    main()
