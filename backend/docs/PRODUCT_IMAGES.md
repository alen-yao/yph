# 产品图片管理 - MinIO 集成方案

## 📋 概述

产品表已升级为支持多图展示，符合现代电商平台（淘宝、京东）的设计规范：

- **主图列表 (main_images)**: 用于商品列表和详情页轮播，第一张为封面图
- **详情图列表 (detail_images)**: 用于商品详情页按顺序展示
- **存储方式**: MinIO 对象存储，返回 URL 存入数据库

## 🎯 数据结构

### Product 模型字段

```python
class Product(models.Model):
    # ... 其他字段 ...
    
    # 主图列表（JSON数组）
    main_images = models.JSONField(
        default=list, 
        verbose_name='主图列表',
        help_text='商品主图URL列表，第一张为封面图'
    )
    # 示例: ["http://minio/bucket/img1.jpg", "http://minio/bucket/img2.jpg"]
    
    # 详情图列表（JSON数组）
    detail_images = models.JSONField(
        default=list, 
        verbose_name='详情图列表',
        help_text='商品详情页图片URL列表，按顺序展示'
    )
    # 示例: ["http://minio/bucket/detail1.jpg", "http://minio/bucket/detail2.jpg"]
```

### 辅助属性和方法

```python
# 只读属性
product.cover_image          # 封面图（第一张主图）
product.main_images_count    # 主图数量
product.detail_images_count  # 详情图数量

# 操作方法
product.add_main_image(url)       # 添加主图
product.add_detail_image(url)     # 添加详情图
product.set_main_images([urls])   # 批量设置主图（替换）
product.set_detail_images([urls]) # 批量设置详情图（替换）
product.remove_main_image(url)    # 删除主图
product.remove_detail_image(url)  # 删除详情图
```

## 📸 图片数量限制

| 类型 | 最大数量 | 推荐数量 | 说明 |
|------|---------|---------|------|
| 主图 | 10张 | 5-6张 | 用于列表封面和详情页轮播 |
| 详情图 | 20张 | 8-15张 | 用于详情页按顺序展示 |

## 🔄 完整流程示例

### 流程 1: 创建商品（推荐方式）

```python
# 步骤1: 上传主图
main_images = []
for image_file in main_image_files:
    url = minio_client.upload_file(image_file, folder='products/main')
    main_images.append(url)

# 步骤2: 上传详情图
detail_images = []
for image_file in detail_image_files:
    url = minio_client.upload_file(image_file, folder='products/detail')
    detail_images.append(url)

# 步骤3: 创建商品
product = Product.objects.create(
    name='iPhone 15 Pro Max',
    category=category,
    price=8999.00,
    main_images=main_images,      # ["url1", "url2", "url3"]
    detail_images=detail_images,  # ["url4", "url5", "url6"]
    # ... 其他字段 ...
)

# 封面图自动为第一张主图
print(product.cover_image)  # 输出: url1
```

### 流程 2: 更新商品图片

```python
from utils.minio_client import minio_client

# 方式A: 添加单张图片
new_url = minio_client.upload_file(image_file, folder='products/main')
product.add_main_image(new_url)

# 方式B: 批量替换图片
new_main_images = minio_client.upload_multiple_files(
    files=image_files,
    folder='products/main'
)
product.set_main_images(new_main_images)

# 方式C: 删除指定图片
product.remove_main_image('http://old-url.jpg')
```

## 🌐 API 使用

### 创建商品（POST /api/products/）

```json
{
  "name": "iPhone 15 Pro Max",
  "category": 1,
  "brand": 2,
  "price": "8999.00",
  "market_price": "9999.00",
  "stock": 100,
  "main_images": [
    "http://localhost:9000/yph-products/products/main/abc123.jpg",
    "http://localhost:9000/yph-products/products/main/def456.jpg",
    "http://localhost:9000/yph-products/products/main/ghi789.jpg"
  ],
  "detail_images": [
    "http://localhost:9000/yph-products/products/detail/aaa111.jpg",
    "http://localhost:9000/yph-products/products/detail/bbb222.jpg"
  ],
  "description": "最新款iPhone",
  "state": 1
}
```

### 商品列表响应（GET /api/products/）

```json
{
  "results": [
    {
      "id": 1,
      "name": "iPhone 15 Pro Max",
      "category_name": "手机数码",
      "brand_name": "Apple",
      "cover_image": "http://localhost:9000/yph-products/products/main/abc123.jpg",
      "price": "8999.00",
      "market_price": "9999.00",
      "sales_count": 156,
      "rating_average": "4.85",
      "is_recommend": true,
      "is_new": true,
      "is_hot": true,
      "state": 1
    }
  ]
}
```

### 商品详情响应（GET /api/products/1/）

```json
{
  "id": 1,
  "name": "iPhone 15 Pro Max",
  "category_name": "手机数码",
  "brand_name": "Apple",
  "cover_image": "http://localhost:9000/yph-products/products/main/abc123.jpg",
  "main_images": [
    "http://localhost:9000/yph-products/products/main/abc123.jpg",
    "http://localhost:9000/yph-products/products/main/def456.jpg",
    "http://localhost:9000/yph-products/products/main/ghi789.jpg"
  ],
  "detail_images": [
    "http://localhost:9000/yph-products/products/detail/aaa111.jpg",
    "http://localhost:9000/yph-products/products/detail/bbb222.jpg"
  ],
  "main_images_count": 3,
  "detail_images_count": 2,
  "price": "8999.00",
  "market_price": "9999.00",
  "description": "最新款iPhone",
  "detail_html": "<p>富文本详情...</p>",
  "stock": 100,
  "sales_count": 156,
  "rating_average": "4.85"
}
```

## 💻 前端展示方案

### Vue 3 商品列表

```vue
<template>
  <div class="product-list">
    <div v-for="product in products" :key="product.id" class="product-card">
      <!-- 封面图 -->
      <img :src="product.cover_image" :alt="product.name" class="cover" />
      <div class="info">
        <h3>{{ product.name }}</h3>
        <p class="price">¥{{ product.price }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const products = ref([])

const fetchProducts = async () => {
  const { data } = await axios.get('/api/products/')
  products.value = data.results
}

fetchProducts()
</script>
```

### Vue 3 商品详情（主图轮播）

```vue
<template>
  <div class="product-detail">
    <!-- 主图轮播 -->
    <el-carousel height="400px">
      <el-carousel-item v-for="(img, index) in product.main_images" :key="index">
        <img :src="img" :alt="`${product.name}-${index + 1}`" />
      </el-carousel-item>
    </el-carousel>

    <!-- 商品信息 -->
    <div class="product-info">
      <h1>{{ product.name }}</h1>
      <p class="price">¥{{ product.price }}</p>
    </div>

    <!-- 详情图按顺序展示 -->
    <div class="detail-images">
      <h2>商品详情</h2>
      <img 
        v-for="(img, index) in product.detail_images" 
        :key="index"
        :src="img" 
        :alt="`详情-${index + 1}`"
        class="detail-img"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const product = ref({})

const fetchProductDetail = async () => {
  const { data } = await axios.get(`/api/products/${route.params.id}/`)
  product.value = data
}

onMounted(fetchProductDetail)
</script>

<style scoped>
.detail-images {
  margin-top: 40px;
}
.detail-img {
  width: 100%;
  margin-bottom: 10px;
}
</style>
```

### React 商品详情（主图轮播 + 详情图）

```jsx
import React, { useState, useEffect } from 'react';
import { Carousel, Image } from 'antd';
import axios from 'axios';

const ProductDetail = ({ productId }) => {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    axios.get(`/api/products/${productId}/`).then(res => {
      setProduct(res.data);
    });
  }, [productId]);

  if (!product) return <div>Loading...</div>;

  return (
    <div className="product-detail">
      {/* 主图轮播 */}
      <Carousel autoplay>
        {product.main_images.map((img, index) => (
          <div key={index}>
            <img src={img} alt={`${product.name}-${index + 1}`} />
          </div>
        ))}
      </Carousel>

      {/* 商品信息 */}
      <div className="product-info">
        <h1>{product.name}</h1>
        <p className="price">¥{product.price}</p>
      </div>

      {/* 详情图 */}
      <div className="detail-images">
        <h2>商品详情</h2>
        <Image.PreviewGroup>
          {product.detail_images.map((img, index) => (
            <Image key={index} src={img} alt={`详情-${index + 1}`} />
          ))}
        </Image.PreviewGroup>
      </div>
    </div>
  );
};

export default ProductDetail;
```

## 📝 管理后台 - 图片上传示例

### Vue 3 + Element Plus 完整示例

```vue
<template>
  <el-form :model="productForm" label-width="120px">
    <el-form-item label="商品名称">
      <el-input v-model="productForm.name" />
    </el-form-item>

    <!-- 主图上传 -->
    <el-form-item label="主图">
      <div class="upload-tip">第一张为封面图，最多10张</div>
      <el-upload
        :action="uploadUrl"
        :headers="headers"
        :file-list="mainImageList"
        :on-success="handleMainImageSuccess"
        :on-remove="handleMainImageRemove"
        list-type="picture-card"
        :limit="10"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
    </el-form-item>

    <!-- 详情图上传 -->
    <el-form-item label="详情图">
      <div class="upload-tip">按顺序展示，最多20张</div>
      <el-upload
        :action="uploadUrl"
        :headers="headers"
        :file-list="detailImageList"
        :on-success="handleDetailImageSuccess"
        :on-remove="handleDetailImageRemove"
        list-type="picture-card"
        :limit="20"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submitProduct">提交</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const uploadUrl = ref('http://localhost:8000/api/system/upload/image/')
const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const productForm = ref({
  name: '',
  main_images: [],
  detail_images: [],
  price: 0,
  // ... 其他字段
})

const mainImageList = ref([])
const detailImageList = ref([])

// 主图上传成功
const handleMainImageSuccess = (response) => {
  productForm.value.main_images.push(response.url)
  mainImageList.value.push({ url: response.url })
  ElMessage.success('主图上传成功')
}

// 主图删除
const handleMainImageRemove = (file) => {
  const index = productForm.value.main_images.indexOf(file.url)
  if (index > -1) {
    productForm.value.main_images.splice(index, 1)
  }
}

// 详情图上传成功
const handleDetailImageSuccess = (response) => {
  productForm.value.detail_images.push(response.url)
  detailImageList.value.push({ url: response.url })
  ElMessage.success('详情图上传成功')
}

// 详情图删除
const handleDetailImageRemove = (file) => {
  const index = productForm.value.detail_images.indexOf(file.url)
  if (index > -1) {
    productForm.value.detail_images.splice(index, 1)
  }
}

// 提交商品
const submitProduct = async () => {
  try {
    await axios.post('/api/products/', productForm.value, { headers })
    ElMessage.success('商品创建成功')
  } catch (error) {
    ElMessage.error('创建失败: ' + error.message)
  }
}
</script>

<style scoped>
.upload-tip {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}
</style>
```

## 🔧 数据库迁移

```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 运行迁移
python manage.py migrate products

# 3. 验证
python manage.py shell
>>> from apps.products.models import Product
>>> Product.objects.create(
...     name='测试商品',
...     category_id=1,
...     price=99.00,
...     market_price=199.00,
...     main_images=['http://example.com/1.jpg', 'http://example.com/2.jpg'],
...     detail_images=['http://example.com/d1.jpg']
... )
```

## 📊 数据库表结构

```sql
CREATE TABLE `product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL COMMENT '商品名称',
  `main_images` json DEFAULT NULL COMMENT '主图列表',
  `detail_images` json DEFAULT NULL COMMENT '详情图列表',
  `description` longtext COMMENT '商品简介',
  `detail_html` longtext COMMENT '商品详情HTML',
  `price` decimal(10,2) NOT NULL COMMENT '销售价格',
  `market_price` decimal(10,2) NOT NULL COMMENT '市场价格',
  -- ... 其他字段
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## ⚠️ 注意事项

1. **图片顺序很重要**: 主图第一张为封面，详情图按顺序展示
2. **URL格式**: 确保URL完整且可访问
3. **图片优化**: 上传前建议压缩图片（推荐 < 500KB）
4. **删除处理**: 删除商品时记得清理 MinIO 中的图片
5. **迁移数据**: 旧数据需要手动迁移到新结构

## 🚀 最佳实践

1. **主图**: 5-6张，包含不同角度、细节特写
2. **详情图**: 8-15张，展示产品特性、参数、使用场景
3. **图片尺寸**: 主图建议 800x800，详情图建议宽度750-1000px
4. **命名规范**: 使用 UUID 避免文件名冲突
5. **CDN加速**: 生产环境建议配置 CDN

---

**文档更新时间**: 2026-07-27
