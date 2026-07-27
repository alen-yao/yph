# 📦 MinIO + 产品多图集成完成

## ✅ 已完成的工作

### 1. MinIO 对象存储集成

- ✅ 安装 MinIO Python 客户端 (`minio==7.2.7`)
- ✅ 配置 MinIO 连接参数 ([settings.py](backend/yph/settings.py#L284-L290))
- ✅ 创建 MinIO 工具类 ([minio_client.py](backend/utils/minio_client.py))
- ✅ 实现图片上传 API
  - 单图上传: `POST /api/system/upload/image/`
  - 批量上传: `POST /api/system/upload/images/`
- ✅ 添加 Swagger API 文档

### 2. 产品模型升级

- ✅ 修改 Product 模型支持多图 ([models.py](backend/apps/products/models.py#L73-L76))
  - `main_images`: 主图列表（JSONField），第一张为封面
  - `detail_images`: 详情图列表（JSONField），按顺序展示
- ✅ 新增便捷属性和方法
  - `cover_image`: 封面图
  - `add_main_image()`, `set_main_images()` 等
- ✅ 更新序列化器 ([serializers.py](backend/apps/products/serializers.py))
- ✅ 创建数据库迁移文件 ([0001_initial.py](backend/apps/products/migrations/0001_initial.py))

### 3. 文档和示例

- ✅ MinIO 集成完整文档 ([MINIO_INTEGRATION.md](backend/docs/MINIO_INTEGRATION.md))
- ✅ 产品图片管理文档 ([PRODUCT_IMAGES.md](backend/docs/PRODUCT_IMAGES.md))
- ✅ MinIO 快速开始指南 ([README_MINIO.md](backend/README_MINIO.md))
- ✅ 产品模型升级说明 ([PRODUCT_MODEL_UPGRADE.md](backend/PRODUCT_MODEL_UPGRADE.md))
- ✅ 数据迁移脚本 ([migrate_product_images.py](backend/scripts/migrate_product_images.py))
- ✅ MinIO 测试脚本 ([test_minio.py](backend/test_minio.py))
- ✅ 前端上传组件示例 ([ProductImageUpload.vue](frontend/admin/src/examples/ProductImageUpload.vue))
- ✅ 前端详情页示例 ([ProductDetail.vue](frontend/h5/src/examples/ProductDetail.vue))

## 🎯 核心特性

### 图片存储结构

```json
{
  "main_images": [
    "http://minio/bucket/main1.jpg",  // 封面图
    "http://minio/bucket/main2.jpg",
    "http://minio/bucket/main3.jpg"
  ],
  "detail_images": [
    "http://minio/bucket/detail1.jpg",
    "http://minio/bucket/detail2.jpg"
  ]
}
```

### 限制

- 主图: 最多 **10张**，推荐 5-6张
- 详情图: 最多 **20张**，推荐 8-15张
- 文件大小: 单张 < **10MB**
- 支持格式: **JPEG, PNG, GIF, WebP**

## 🚀 快速开始

### 1. 启动 MinIO

```bash
docker run -d --name minio -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

访问控制台: http://localhost:9001 (minioadmin/minioadmin)

### 2. 后端配置

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（.env）
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=yph-products

# 运行迁移
python manage.py migrate

# 测试 MinIO 连接
python test_minio.py

# 创建示例数据
python scripts/migrate_product_images.py --sample
```

### 3. 前端使用

参考示例组件:
- 管理后台上传: [ProductImageUpload.vue](frontend/admin/src/examples/ProductImageUpload.vue)
- H5 详情页: [ProductDetail.vue](frontend/h5/src/examples/ProductDetail.vue)

## 📡 API 示例

### 上传图片

```bash
curl -X POST http://localhost:8000/api/system/upload/image/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@product.jpg"

# 响应
{
  "url": "http://localhost:9000/yph-products/products/abc123.jpg",
  "message": "图片上传成功"
}
```

### 创建商品

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro Max",
    "category": 1,
    "price": "8999.00",
    "market_price": "9999.00",
    "main_images": [
      "http://localhost:9000/yph-products/products/main/img1.jpg",
      "http://localhost:9000/yph-products/products/main/img2.jpg"
    ],
    "detail_images": [
      "http://localhost:9000/yph-products/products/detail/d1.jpg"
    ]
  }'
```

### 获取商品详情

```bash
curl http://localhost:8000/api/products/1/

# 响应
{
  "id": 1,
  "name": "iPhone 15 Pro Max",
  "cover_image": "http://localhost:9000/yph-products/products/main/img1.jpg",
  "main_images": ["...", "..."],
  "detail_images": ["..."],
  "main_images_count": 2,
  "detail_images_count": 1,
  "price": "8999.00"
}
```

## 📁 文件结构

```
backend/
├── apps/products/
│   ├── models.py              # ✅ 已更新（多图支持）
│   ├── serializers.py         # ✅ 已更新
│   └── migrations/
│       └── 0001_initial.py    # ✅ 新增
├── apps/system/
│   ├── views.py               # ✅ 新增上传接口
│   ├── serializers.py         # ✅ 新增上传验证器
│   └── urls.py                # ✅ 新增路由
├── utils/
│   └── minio_client.py        # ✅ 新增 MinIO 客户端
├── docs/
│   ├── MINIO_INTEGRATION.md   # ✅ MinIO 集成文档
│   └── PRODUCT_IMAGES.md      # ✅ 产品图片文档
├── scripts/
│   └── migrate_product_images.py  # ✅ 数据迁移脚本
├── test_minio.py              # ✅ MinIO 测试脚本
└── requirements.txt           # ✅ 已添加 minio==7.2.7

frontend/
├── admin/src/examples/
│   └── ProductImageUpload.vue # ✅ 管理后台上传组件
└── h5/src/examples/
    └── ProductDetail.vue      # ✅ H5 详情页组件
```

## 🔄 数据迁移

如果有旧数据需要迁移:

```bash
# 备份数据库
mysqldump -u root -p yph > backup.sql

# 运行迁移
python scripts/migrate_product_images.py --migrate
```

## ⚠️ 重要提示

### 前端需要适配

1. **商品列表页**
   - 旧: 使用 `product.main_image`
   - 新: 使用 `product.cover_image`

2. **商品详情页**
   - 新增主图轮播: `product.main_images` 数组
   - 新增详情图展示: `product.detail_images` 数组

### 图片上传流程

```
用户选择图片 → 上传到 MinIO API → 获得 URL → 保存到商品 main_images/detail_images
```

## 📚 详细文档

| 文档 | 说明 |
|------|------|
| [README_MINIO.md](backend/README_MINIO.md) | MinIO 快速开始 |
| [MINIO_INTEGRATION.md](backend/docs/MINIO_INTEGRATION.md) | MinIO 完整集成指南 |
| [PRODUCT_IMAGES.md](backend/docs/PRODUCT_IMAGES.md) | 产品图片管理详解 |
| [PRODUCT_MODEL_UPGRADE.md](backend/PRODUCT_MODEL_UPGRADE.md) | 产品模型升级说明 |

## 🆘 常见问题

**Q: MinIO 连接失败？**  
A: 检查 MinIO 是否启动 `docker ps | grep minio`

**Q: 图片无法访问？**  
A: 确认存储桶策略为公开读取（MinIO 客户端自动设置）

**Q: 旧数据会丢失吗？**  
A: 不会。运行迁移脚本自动转换为新格式

**Q: 必须使用 MinIO 吗？**  
A: 推荐使用。也可以使用其他对象存储（阿里云OSS、AWS S3）

## 🎉 现在可以做什么

1. ✅ 在管理后台上传产品主图和详情图
2. ✅ 商品列表显示封面图
3. ✅ 商品详情页显示主图轮播
4. ✅ 商品详情页按顺序展示详情图
5. ✅ 图片存储在 MinIO，支持高并发访问

---

**集成完成日期**: 2026-07-27  
**版本**: v1.0
