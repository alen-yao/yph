# MinIO 对象存储集成 - 快速开始

## 已完成的工作

✅ 安装 MinIO Python 客户端依赖  
✅ 配置 MinIO 连接参数  
✅ 创建 MinIO 客户端工具类  
✅ 实现图片上传 API 接口  
✅ 添加请求验证和错误处理  
✅ 集成 Swagger API 文档  

## 快速启动步骤

### 1️⃣ 启动 MinIO 服务

**Docker 方式（推荐）:**
```bash
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

访问 MinIO 控制台: http://localhost:9001  
默认账号: `minioadmin` / `minioadmin`

### 2️⃣ 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ 配置环境变量

复制 `.env.example` 到 `.env` 并配置 MinIO 参数（默认配置已可用）:

```bash
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=yph-products
MINIO_SECURE=False
MINIO_PUBLIC_URL=http://localhost:9000
```

### 4️⃣ 测试集成

```bash
cd backend
python test_minio.py
```

如果看到 "✓ MinIO 集成正常工作"，说明配置成功！

### 5️⃣ 启动 Django 服务

```bash
python manage.py runserver
```

## API 使用

### 上传单张图片

```bash
curl -X POST http://localhost:8000/api/system/upload/image/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@image.jpg" \
  -F "folder=products"
```

**响应:**
```json
{
  "url": "http://localhost:9000/yph-products/products/abc123.jpg",
  "message": "图片上传成功"
}
```

### 批量上传图片

```bash
curl -X POST http://localhost:8000/api/system/upload/images/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "folder=products"
```

**响应:**
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

## API 文档

启动服务后访问 Swagger 文档:
- http://localhost:8000/swagger/
- http://localhost:8000/redoc/

在 "system" 分组下可以找到图片上传接口。

## 文件结构

```
backend/
├── utils/
│   └── minio_client.py           # MinIO 客户端工具类
├── apps/
│   └── system/
│       ├── serializers.py        # 添加了图片上传序列化器
│       ├── views.py              # 添加了上传接口
│       └── urls.py               # 添加了上传路由
├── docs/
│   └── MINIO_INTEGRATION.md      # 详细集成文档
├── test_minio.py                 # 集成测试脚本
├── .env.example                  # 环境变量示例（已添加MinIO配置）
└── requirements.txt              # 已添加 minio==7.2.7
```

## 核心功能

### MinIO 客户端 (`utils/minio_client.py`)

- ✅ 单例模式，自动初始化
- ✅ 自动创建存储桶
- ✅ 自动设置公开访问策略
- ✅ 支持单文件上传
- ✅ 支持批量上传
- ✅ 支持文件删除
- ✅ 支持预签名URL（临时访问）

### API 接口

| 接口 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/system/upload/image/` | POST | 需登录 | 上传单张图片 |
| `/api/system/upload/images/` | POST | 需登录 | 批量上传图片 |

### 验证规则

- ✅ 文件大小限制: 10MB
- ✅ 格式限制: JPEG, PNG, GIF, WebP
- ✅ 批量上传限制: 最多10张
- ✅ 自动生成UUID文件名

## 在代码中使用

```python
from utils.minio_client import minio_client

# 上传文件
url = minio_client.upload_file(file_object, folder='products')

# 批量上传
urls = minio_client.upload_multiple_files(files, folder='banners')

# 删除文件
minio_client.delete_file(image_url)

# 获取临时访问URL
from datetime import timedelta
temp_url = minio_client.get_presigned_url(
    'products/abc123.jpg',
    expires=timedelta(hours=1)
)
```

## 推荐文件夹结构

```
yph-products/
├── products/       # 产品图片
├── avatars/        # 用户头像
├── banners/        # 轮播图
├── brands/         # 品牌Logo
├── categories/     # 分类图标
└── reviews/        # 评价图片
```

## 前端集成

详见 `backend/docs/MINIO_INTEGRATION.md` 文档，包含:
- Vue 3 + Element Plus 示例
- React + Ant Design 示例
- JavaScript Fetch API 示例

## 生产环境部署

1. **修改默认密钥** - 使用强密码
2. **启用 HTTPS** - 设置 `MINIO_SECURE=True`
3. **配置反向代理** - 使用 Nginx
4. **设置 CORS** - 配置跨域访问
5. **监控存储** - 定期检查存储使用情况

详细配置请查看完整文档: `backend/docs/MINIO_INTEGRATION.md`

## 常见问题

### MinIO 连接失败？

检查服务是否启动:
```bash
docker ps | grep minio
```

### 图片无法访问？

确认存储桶策略为公开读取，MinIO 客户端会自动设置。

### 需要帮助？

查看详细文档: `backend/docs/MINIO_INTEGRATION.md`

---

**🎉 现在你可以开始使用 MinIO 上传产品图片了！**
