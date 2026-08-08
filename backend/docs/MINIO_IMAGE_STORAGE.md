# MinIO 图片存储方案

## 问题说明

原来的实现中，商品图片直接存储MinIO的临时分享URL（通过`presigned_get_object`生成），这些URL会在12小时后过期，导致图片无法访问。

## 解决方案

### 核心思路

1. **存储对象Key而非完整URL**：数据库中只保存MinIO的对象路径（如：`products/2026/08/abc123.jpg`）
2. **动态生成访问URL**：通过统一的`get_image_url()`方法在需要时生成完整URL
3. **公开Bucket策略**：设置bucket为公开读取，确保URL永不过期

### 优势

- ✅ URL永不过期（公开bucket）
- ✅ MinIO地址变更时无需修改数据库
- ✅ 可灵活切换为临时URL（如果需要私有bucket）
- ✅ 存储空间更小（只存key不存完整URL）

## 实现细节

### 1. MinIO客户端工具（`utils/minio_client.py`）

#### 上传文件
```python
# 上传文件，返回对象key
object_key = minio_client.upload_file(file_obj, folder='products')
# 返回值示例：products/2026/08/abc123def456.jpg
```

#### 生成访问URL
```python
# 根据对象key生成完整URL
full_url = minio_client.get_image_url(object_key)
# 返回值示例：http://localhost:9000/yph-products/products/2026/08/abc123def456.jpg
```

#### 文件组织结构
上传的文件自动按年月组织：
```
bucket/
  └── products/
      └── 2026/
          └── 08/
              ├── abc123def456.jpg
              ├── def789ghi012.jpg
              └── ...
```

### 2. 数据库存储

#### Product模型（`apps/products/models.py`）
```python
class Product(models.Model):
    # 存储对象key列表，而非完整URL
    main_images = models.JSONField(default=list)  # ['products/2026/08/abc.jpg', ...]
    detail_images = models.JSONField(default=list)  # ['products/2026/08/def.jpg', ...]
```

### 3. API序列化器

#### 输入（创建/更新商品）
```python
# POST /api/products/
{
    "name": "测试商品",
    "main_images": [
        "products/2026/08/abc123.jpg",  // 对象key
        "products/2026/08/def456.jpg"
    ],
    "detail_images": [
        "products/2026/08/ghi789.jpg"
    ],
    ...
}
```

#### 输出（查询商品）
序列化器自动将对象key转换为完整URL：
```python
# GET /api/products/1/
{
    "id": 1,
    "name": "测试商品",
    "cover_image": "http://localhost:9000/yph-products/products/2026/08/abc123.jpg",
    "main_images": [
        "http://localhost:9000/yph-products/products/2026/08/abc123.jpg",
        "http://localhost:9000/yph-products/products/2026/08/def456.jpg"
    ],
    "detail_images": [
        "http://localhost:9000/yph-products/products/2026/08/ghi789.jpg"
    ],
    ...
}
```

### 4. 上传接口

#### 单张图片上传
```bash
POST /api/system/upload/image/

# 请求
FormData: {
    file: <图片文件>,
    folder: "products"  # 可选，默认为products
}

# 响应
{
    "key": "products/2026/08/abc123def456.jpg",  // 对象key，保存到数据库
    "url": "http://localhost:9000/yph-products/products/2026/08/abc123def456.jpg",  // 完整URL，供前端预览
    "message": "图片上传成功"
}
```

#### 批量图片上传
```bash
POST /api/system/upload/images/

# 请求
FormData: {
    files: [<图片文件1>, <图片文件2>, ...],
    folder: "products"
}

# 响应
{
    "keys": [
        "products/2026/08/abc123.jpg",
        "products/2026/08/def456.jpg"
    ],
    "urls": [
        "http://localhost:9000/yph-products/products/2026/08/abc123.jpg",
        "http://localhost:9000/yph-products/products/2026/08/def456.jpg"
    ],
    "message": "图片上传成功",
    "count": 2
}
```

## 前端使用流程

### 1. 上传图片
```javascript
// 上传商品主图
const formData = new FormData();
formData.append('file', imageFile);
formData.append('folder', 'products');

const response = await fetch('/api/system/upload/image/', {
    method: 'POST',
    body: formData,
    headers: {
        'Authorization': `Bearer ${token}`
    }
});

const data = await response.json();
// data.key: "products/2026/08/abc123.jpg" - 保存到状态
// data.url: "http://..." - 用于预览
```

### 2. 创建商品
```javascript
// 将收集到的keys提交给后端
const productData = {
    name: "商品名称",
    main_images: [
        "products/2026/08/abc123.jpg",  // 使用上传返回的key
        "products/2026/08/def456.jpg"
    ],
    detail_images: [
        "products/2026/08/ghi789.jpg"
    ],
    ...
};

await fetch('/api/products/', {
    method: 'POST',
    body: JSON.stringify(productData),
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    }
});
```

### 3. 显示商品图片
```javascript
// 从API获取商品详情
const response = await fetch('/api/products/1/');
const product = await response.json();

// 直接使用返回的URL
<img src={product.cover_image} />  // 已经是完整URL

product.main_images.forEach(url => {
    // 渲染图片轮播
    <img src={url} />  // 已经是完整URL
});
```

## MinIO配置

### 开发环境配置（.env）
```bash
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=yph-products
MINIO_SECURE=False
MINIO_PUBLIC_URL=http://localhost:9000
```

### Bucket策略（公开读取）

**重要：** Bucket必须设置为公开读取，否则URL会过期！

#### 自动设置（推荐）

项目首次运行时会自动设置bucket为公开：
```bash
cd backend
python test_minio.py
```

#### 手动设置

如需手动设置或重新设置：
```bash
cd backend
python set_minio_public.py
```

#### 策略详情

公开策略JSON：
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::yph-products/*"]
        }
    ]
}
```

这样任何人都可以通过URL直接访问图片，无需认证，URL永不过期。

**详细设置方法请参考：** [MINIO_SETUP.md](./MINIO_SETUP.md)

## 测试

运行测试脚本：
```bash
cd backend
python test_minio.py
```

测试脚本会：
1. 检查MinIO连接
2. 上传测试图片（返回对象key）
3. 生成访问URL
4. 删除测试图片

## 生产环境注意事项

1. **使用CDN**：建议在MinIO前面加CDN加速访问
2. **HTTPS**：生产环境设置 `MINIO_SECURE=True`
3. **域名**：配置 `MINIO_PUBLIC_URL` 为实际域名
4. **安全凭证**：修改默认的ACCESS_KEY和SECRET_KEY

### 生产环境配置示例
```bash
MINIO_ENDPOINT=minio.yourdomain.com:443
MINIO_ACCESS_KEY=<your-access-key>
MINIO_SECRET_KEY=<your-secret-key>
MINIO_BUCKET_NAME=yph-products
MINIO_SECURE=True
MINIO_PUBLIC_URL=https://cdn.yourdomain.com
```

## 数据迁移

如果已有数据使用了完整URL，需要进行迁移：

```python
# 迁移脚本示例
from apps.products.models import Product

for product in Product.objects.all():
    # 提取对象key
    main_images = []
    for url in product.main_images:
        if url.startswith('http'):
            # 从URL中提取key：http://localhost:9000/yph-products/products/abc.jpg -> products/abc.jpg
            key = url.split('/yph-products/')[-1]
            main_images.append(key)
        else:
            main_images.append(url)  # 已经是key
    
    product.main_images = main_images
    product.save(update_fields=['main_images'])
```

## 常见问题

### Q: 为什么不直接存完整URL？
A: 存URL的问题：
- 如果MinIO地址变更（如换域名、加CDN），所有数据都要更新
- 占用更多存储空间
- 不够灵活（无法根据环境切换URL）

### Q: 如何实现私有图片？
A: 修改bucket策略为私有，然后在`get_image_url()`中调用`get_presigned_url()`生成临时URL：
```python
def get_image_url(self, image_key, private=False):
    if private:
        return self.get_presigned_url(image_key, expires=timedelta(hours=12))
    return f"{self.public_url}/{self.bucket_name}/{image_key}"
```

### Q: 图片URL过期怎么办？
A: 使用公开bucket策略后，URL永不过期。如果必须使用私有bucket，建议设置较长的过期时间（如7天），并在序列化时动态生成新URL。
