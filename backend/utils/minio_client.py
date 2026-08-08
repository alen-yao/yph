"""MinIO 对象存储客户端工具类"""
import os
import uuid
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MinioClient:
    """MinIO 客户端封装类"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.endpoint = settings.MINIO['ENDPOINT']
        self.access_key = settings.MINIO['ACCESS_KEY']
        self.secret_key = settings.MINIO['SECRET_KEY']
        self.bucket_name = settings.MINIO['BUCKET_NAME']
        self.secure = settings.MINIO['SECURE']
        self.public_url = settings.MINIO['PUBLIC_URL']

        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )

        self._ensure_bucket_exists()
        self._initialized = True

    def _ensure_bucket_exists(self):
        """确保存储桶存在，不存在则创建"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"创建存储桶: {self.bucket_name}")
            else:
                logger.info(f"存储桶已存在: {self.bucket_name}")

            # 设置存储桶为公开读取
            self._set_public_policy()
        except S3Error as e:
            logger.error(f"MinIO 存储桶操作失败: {e}")
            raise

    def _set_public_policy(self):
        """设置存储桶为公开读取"""
        try:
            import json
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"]
                    }
                ]
            }
            self.client.set_bucket_policy(self.bucket_name, json.dumps(policy))
            logger.info(f"设置存储桶 {self.bucket_name} 为公开读取")
        except S3Error as e:
            logger.error(f"设置bucket策略失败: {e}")
            raise

    def set_bucket_public(self):
        """手动设置bucket为公开（外部调用）"""
        self._set_public_policy()
        return True

    def upload_file(self, file_obj, file_path=None, folder='products', content_type=None):
        """
        上传文件到MinIO

        Args:
            file_obj: 文件对象（Django UploadedFile）
            file_path: 文件路径，不提供则自动生成
            folder: 文件夹名称
            content_type: 文件类型

        Returns:
            str: 文件的对象key（路径）
        """
        try:
            # 生成文件路径
            if not file_path:
                ext = os.path.splitext(file_obj.name)[1]
                # 按日期组织文件：products/2026/08/abc123.jpg
                from datetime import datetime
                now = datetime.now()
                file_path = f"{folder}/{now.year}/{now.month:02d}/{uuid.uuid4().hex}{ext}"

            # 获取文件内容类型
            if not content_type:
                content_type = file_obj.content_type or 'application/octet-stream'

            # 上传文件
            file_obj.seek(0)
            self.client.put_object(
                self.bucket_name,
                file_path,
                file_obj,
                length=file_obj.size,
                content_type=content_type
            )

            logger.info(f"文件上传成功: {file_path}")
            # 返回对象key，而不是完整URL
            return file_path

        except S3Error as e:
            logger.error(f"MinIO 文件上传失败: {e}")
            raise Exception(f"文件上传失败: {str(e)}")

    def upload_multiple_files(self, files, folder='products'):
        """
        批量上传文件

        Args:
            files: 文件对象列表
            folder: 存储文件夹

        Returns:
            list: 文件对象key列表
        """
        keys = []
        for file_obj in files:
            object_key = self.upload_file(file_obj, folder=folder)
            keys.append(object_key)
        return keys

    def get_image_url(self, image_key):
        """
        根据对象key生成完整访问URL

        Args:
            image_key: MinIO对象key（如：products/2026/08/abc123.jpg）

        Returns:
            str: 完整的访问URL
        """
        if not image_key:
            return None

        # 如果已经是完整URL，直接返回（兼容旧数据）
        if image_key.startswith('http://') or image_key.startswith('https://'):
            return image_key

        # 构建完整URL
        return f"{self.public_url}/{self.bucket_name}/{image_key}"

    def delete_file(self, file_path):
        """
        删除文件

        Args:
            file_path: 文件路径或完整URL

        Returns:
            bool: 是否删除成功
        """
        try:
            # 如果是完整URL，提取文件路径
            if file_path.startswith('http'):
                file_path = file_path.split(f"{self.bucket_name}/")[-1]

            self.client.remove_object(self.bucket_name, file_path)
            logger.info(f"文件删除成功: {file_path}")
            return True
        except S3Error as e:
            logger.error(f"MinIO 文件删除失败: {e}")
            return False

    def get_presigned_url(self, file_path, expires=timedelta(hours=1)):
        """
        获取预签名URL（用于临时访问私有文件）

        Args:
            file_path: 文件路径
            expires: 过期时间

        Returns:
            str: 预签名URL
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_name,
                file_path,
                expires=expires
            )
            return url
        except S3Error as e:
            logger.error(f"获取预签名URL失败: {e}")
            raise


# 创建全局单例
minio_client = MinioClient()
