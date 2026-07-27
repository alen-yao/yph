# 📦 产品模型升级说明

## ✨ 核心改动

产品表已升级为支持**多主图 + 多详情图**的电商标准结构，图片存储在 MinIO 对象存储中。

### 旧结构 vs 新结构

| 字段 | 旧结构 | 新结构 | 说明 |
|------|--------|--------|------|
| 主图 | `main_image` (ImageField) | `main_images` (JSONField) | 支持多张主图，第一张为封面 |
| 图片列表 | `images` (TextField) | 已删除 | 拆分为主图和详情图 |
| 详情图 | ❌ 不存在 | `detail_images` (JSONField) | 新增详情图列表 |

### 数据格式

```python
# 旧格式
product.main_image = '/media/products/main/abc.jpg'  # 单张
product.images = '["img1.jpg", "img2.jpg"]'          # JSON字符串

# 新格式
product.main_images = [
    'http://localhost:9000/yph-products/products/main/abc123.jpg',
    'http://localhost:9000/yph-products/products/main/def456.jpg',
    'http://localhost:9000/yph-products/products/main/ghi789.jpg'
]  # MinIO URL 数组，第一张为封面

product.detail_images = [
    'http://localhost:9000/yph-products/products/detail/d1.jpg',
    'http://localhost:9000/yph-products/products/detail/d2.jpg'
]  # 详情页图片数组
```

## 🎯 新增功能

### 1. 便捷属性

```python
product.cover_image          # 封面图（第一张主图）
product.main_images_count    # 主图数量
product.detail_images_count  # 详情图数量
```

### 2. 操作方法

```python
# 添加图片
product.add_main_image(url)
product.add_detail_image(url)

# 批量设置（替换）
product.set_main_images([url1, url2, url3])
product.set_detail_images([url4, url5])

# 删除图片
product.remove_main_image(url)
product.remove_detail_image(url)
```

## 🚀 快速开始

### 1. 运行数据库迁移

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate products
```

### 2. 启动 MinIO

```bash
docker run -d --name minio -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

### 3. 创建测试商品

```bash
python scripts/migrate_product_images.py --sample
```

### 4. 测试 API

```bash
# 上传图片
curl -X POST http://localhost:8000/api/system/upload/image/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@product.jpg"

# 响应: {"url": "http://localhost:9000/yph-products/products/abc123.jpg"}

# 创建商品
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试商品",
    "category": 1,
    "price": "99.00",
    "market_price": "199.00",
    "main_images": ["http://localhost:9000/yph-products/products/abc123.jpg"],
    "detail_images": ["http://localhost:9000/yph-products/products/def456.jpg"]
  }'
```

## 📋 API 变更

### 商品列表 GET /api/products/

**旧响应:**
```json
{
  "id": 1,
  "main_image": "/media/products/main/abc.jpg"
}
```

**新响应:**
```json
{
  "id": 1,
  "cover_image": "http://localhost:9000/yph-products/products/main/abc.jpg",
  "is_recommend": true,
  "is_new": true,
  "is_hot": false
}
```

### 商品详情 GET /api/products/1/

**新增字段:**
```json
{
  "id": 1,
  "cover_image": "http://...",
  "main_images": ["url1", "url2", "url3"],
  "detail_images": ["url4", "url5"],
  "main_images_count": 3,
  "detail_images_count": 2
}
```

### 创建/更新商品 POST/PUT /api/products/

**新参数:**
```json
{
  "main_images": ["url1", "url2"],    // 主图数组（最多10张）
  "detail_images": ["url3", "url4"]   // 详情图数组（最多20张）
}
```

## 🔄 数据迁移

如果你有旧数据需要迁移:

```bash
# 备份数据库
mysqldump -u root -p yph > backup.sql

# 运行迁移脚本
python scripts/migrate_product_images.py --migrate

# 验证迁移结果
python manage.py shell
>>> from apps.products.models import Product
>>> p = Product.objects.first()
>>> print(p.main_images)
>>> print(p.cover_image)
```

## 📂 文件结构

```
backend/
├── apps/products/
│   ├── models.py                      # ✅ 已更新
│   ├── serializers.py                 # ✅ 已更新
│   ├── views.py                       # ✅ 无需修改
│   └── migrations/
│       └── 0001_initial.py            # ✅ 新增
├── docs/
│   ├── MINIO_INTEGRATION.md           # MinIO 集成文档
│   └── PRODUCT_IMAGES.md              # 产品图片管理文档
├── scripts/
│   └── migrate_product_images.py      # 数据迁移脚本
└── utils/
    └── minio_client.py                # MinIO 客户端工具
```

## ⚠️ 重要提示

### 1. 前端需要适配

**商品列表页:**
- 旧: 使用 `main_image`
- 新: 使用 `cover_image`

**商品详情页:**
- 新增主图轮播: `main_images` 数组
- 新增详情图展示: `detail_images` 数组

### 2. 图片上传流程

```
1. 上传图片到 MinIO → 获得 URL
2. 将 URL 添加到 main_images 或 detail_images 数组
3. 创建/更新商品
```

### 3. 向后兼容

旧的 `main_image` 和 `images` 字段已删除，**不兼容**。必须:
- 运行数据迁移脚本
- 更新前端代码

## 📚 参考文档

- [MinIO 集成文档](docs/MINIO_INTEGRATION.md) - MinIO 安装和使用
- [产品图片管理](docs/PRODUCT_IMAGES.md) - 完整的前后端示例
- [README_MINIO.md](README_MINIO.md) - MinIO 快速开始

## 🆘 常见问题

**Q: 旧数据会丢失吗？**  
A: 不会。运行迁移脚本会自动将旧数据转换为新格式。

**Q: 必须使用 MinIO 吗？**  
A: 是的。新结构存储 URL，推荐使用 MinIO。也可以使用其他对象存储（阿里云OSS、AWS S3）。

**Q: 图片限制是多少？**  
A: 主图最多10张，详情图最多20张，单张图片 < 10MB。

**Q: 如何批量上传？**  
A: 使用 `/api/system/upload/images/` 接口，一次最多上传10张。

---

**升级日期**: 2026-07-27  
**版本**: v2.0
