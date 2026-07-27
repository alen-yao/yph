# MinIO 对象存储集成文档

## 概述

本项目已集成 MinIO 对象存储服务，用于存储产品图片、用户头像、轮播图等文件。MinIO 是一个高性能的分布式对象存储服务，兼容 Amazon S3 API。

## 快速开始

### 1. 安装 MinIO

#### Docker 方式（推荐）

```bash
# 拉取 MinIO 镜像
docker pull minio/minio

# 运行 MinIO 容器
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  -v /data/minio:/data \
  minio/minio server /data --console-address ":9001"
```

#### 本地安装方式

**Windows:**
```bash
# 下载 minio.exe
wget https://dl.min.io/server/minio/release/windows-amd64/minio.exe

# 启动 MinIO
.\minio.exe server C:\data --console-address ":9001"
```

**Linux/macOS:**
```bash
# 下载
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio

# 启动
./minio server /data --console-address ":9001"
```

### 2. 访问 MinIO 控制台

启动后访问：http://localhost:9001

默认账号：
- 用户名: `minioadmin`
- 密码: `minioadmin`

### 3. 配置环境变量

在 `backend/.env` 文件中配置 MinIO 连接信息：

```bash
# MinIO Object Storage
MINIO_ENDPOINT=localhost:9000          # MinIO 服务地址
MINIO_ACCESS_KEY=minioadmin            # 访问密钥
MINIO_SECRET_KEY=minioadmin            # 密钥
MINIO_BUCKET_NAME=yph-products         # 存储桶名称
MINIO_SECURE=False                     # 是否使用 HTTPS
MINIO_PUBLIC_URL=http://localhost:9000 # 公开访问 URL
```

### 4. 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

MinIO Python 客户端 (`minio==7.2.7`) 已添加到 `requirements.txt`。

## API 接口

### 1. 上传单张图片

**接口:** `POST /api/system/upload/image/`

**权限:** 需要登录认证

**请求参数:**
- `file`: 图片文件（必填）
- `folder`: 存储文件夹（可选，默认: `products`）

**请求示例（curl）:**
```bash
curl -X POST http://localhost:8000/api/system/upload/image/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg" \
  -F "folder=products"
```

**响应示例:**
```json
{
  "url": "http://localhost:9000/yph-products/products/abc123def456.jpg",
  "message": "图片上传成功"
}
```

### 2. 批量上传图片

**接口:** `POST /api/system/upload/images/`

**权限:** 需要登录认证

**请求参数:**
- `files`: 图片文件列表（必填，最多10张）
- `folder`: 存储文件夹（可选，默认: `products`）

**请求示例（curl）:**
```bash
curl -X POST http://localhost:8000/api/system/upload/images/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.jpg" \
  -F "folder=products"
```

**响应示例:**
```json
{
  "urls": [
    "http://localhost:9000/yph-products/products/abc123.jpg",
    "http://localhost:9000/yph-products/products/def456.jpg"
  ],
  "message": "图片上传成功",
  "count": 2
}
```

## 前端集成示例

### Vue 3 + Element Plus

```vue
<template>
  <el-upload
    :action="uploadUrl"
    :headers="headers"
    :on-success="handleSuccess"
    :before-upload="beforeUpload"
    :limit="10"
    list-type="picture-card"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const uploadUrl = ref('http://localhost:8000/api/system/upload/image/')
const token = localStorage.getItem('access_token')

const headers = {
  Authorization: `Bearer ${token}`
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB!')
    return false
  }
  return true
}

const handleSuccess = (response) => {
  if (response.url) {
    ElMessage.success('上传成功!')
    console.log('图片URL:', response.url)
  }
}
</script>
```

### React + Ant Design

```jsx
import { Upload, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const ImageUpload = () => {
  const token = localStorage.getItem('access_token');

  const uploadProps = {
    action: 'http://localhost:8000/api/system/upload/image/',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    beforeUpload: (file) => {
      const isImage = file.type.startsWith('image/');
      const isLt10M = file.size / 1024 / 1024 < 10;

      if (!isImage) {
        message.error('只能上传图片文件!');
        return false;
      }
      if (!isLt10M) {
        message.error('图片大小不能超过 10MB!');
        return false;
      }
      return true;
    },
    onChange: (info) => {
      if (info.file.status === 'done') {
        message.success('上传成功!');
        console.log('图片URL:', info.file.response.url);
      } else if (info.file.status === 'error') {
        message.error('上传失败!');
      }
    },
  };

  return (
    <Upload {...uploadProps} listType="picture-card">
      <div>
        <PlusOutlined />
        <div style={{ marginTop: 8 }}>上传</div>
      </div>
    </Upload>
  );
};

export default ImageUpload;
```

### JavaScript Fetch API

```javascript
async function uploadImage(file, folder = 'products') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('folder', folder);

  const token = localStorage.getItem('access_token');

  try {
    const response = await fetch('http://localhost:8000/api/system/upload/image/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    const data = await response.json();
    
    if (response.ok) {
      console.log('上传成功:', data.url);
      return data.url;
    } else {
      console.error('上传失败:', data.error);
      throw new Error(data.error);
    }
  } catch (error) {
    console.error('上传错误:', error);
    throw error;
  }
}

// 使用示例
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', async (e) => {
  const file = e.target.files[0];
  if (file) {
    const imageUrl = await uploadImage(file);
    console.log('图片URL:', imageUrl);
  }
});
```

## 编程使用

在 Django 代码中直接使用 MinIO 客户端：

```python
from utils.minio_client import minio_client

# 上传文件
def upload_product_image(file):
    """上传产品图片"""
    url = minio_client.upload_file(file, folder='products')
    return url

# 批量上传
def upload_multiple_images(files):
    """批量上传图片"""
    urls = minio_client.upload_multiple_files(files, folder='products')
    return urls

# 删除文件
def delete_image(image_url):
    """删除图片"""
    success = minio_client.delete_file(image_url)
    return success

# 获取预签名URL（用于私有文件临时访问）
from datetime import timedelta
def get_temp_url(file_path):
    """获取临时访问URL"""
    url = minio_client.get_presigned_url(
        file_path, 
        expires=timedelta(hours=1)
    )
    return url
```

## 文件夹结构

推荐的文件存储结构：

```
yph-products/
├── products/          # 产品图片
│   ├── main/         # 产品主图
│   └── detail/       # 产品详情图
├── avatars/          # 用户头像
├── banners/          # 轮播图
├── brands/           # 品牌Logo
├── categories/       # 分类图标
└── reviews/          # 评价图片
```

## 限制说明

- **文件大小限制:** 10MB
- **支持格式:** JPEG, PNG, GIF, WebP
- **批量上传限制:** 一次最多上传 10 张图片
- **命名规则:** 自动生成 UUID 文件名，避免冲突

## 生产环境配置

### 1. 修改默认密钥

```bash
MINIO_ACCESS_KEY=your-secure-access-key
MINIO_SECRET_KEY=your-secure-secret-key
```

### 2. 启用 HTTPS

```bash
MINIO_SECURE=True
MINIO_PUBLIC_URL=https://your-domain.com
```

### 3. 使用反向代理（Nginx）

```nginx
server {
    listen 80;
    server_name minio.yourdomain.com;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 文件大小限制
        client_max_body_size 100M;
    }
}
```

### 4. Docker Compose 部署

```yaml
version: '3.8'

services:
  minio:
    image: minio/minio
    container_name: yph-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY}
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    restart: unless-stopped

volumes:
  minio_data:
```

## 常见问题

### 1. 连接失败

检查 MinIO 服务是否启动：
```bash
docker ps | grep minio
```

### 2. 存储桶不存在

客户端会自动创建存储桶，如果失败请手动在控制台创建。

### 3. 图片无法访问

确认存储桶策略设置为公开读取，或使用预签名URL。

### 4. 上传失败

检查文件大小和格式是否符合要求，查看后端日志获取详细错误信息。

## 监控与维护

### 查看存储使用情况

在 MinIO 控制台 (http://localhost:9001) 可以查看：
- 存储桶数量
- 对象数量
- 存储空间使用
- 上传下载流量

### 日志查看

```bash
# Docker 方式
docker logs minio

# 本地方式
查看 MinIO 启动终端输出
```

## 参考资料

- [MinIO 官方文档](https://min.io/docs/)
- [MinIO Python SDK](https://min.io/docs/minio/linux/developers/python/minio-py.html)
- [Django File Upload](https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/)
