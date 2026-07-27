<template>
  <div class="product-detail" v-if="product">
    <!-- 主图轮播 -->
    <div class="main-images-carousel">
      <el-carousel :interval="3000" height="375px" indicator-position="inside">
        <el-carousel-item v-for="(image, index) in product.main_images" :key="index">
          <img :src="image" :alt="`${product.name}-${index + 1}`" class="carousel-image" />
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 商品信息 -->
    <div class="product-info">
      <h1 class="product-name">{{ product.name }}</h1>

      <!-- 标签 -->
      <div class="product-tags">
        <el-tag v-if="product.is_recommend" type="danger" size="small">推荐</el-tag>
        <el-tag v-if="product.is_new" type="success" size="small">新品</el-tag>
        <el-tag v-if="product.is_hot" type="warning" size="small">热销</el-tag>
      </div>

      <!-- 价格 -->
      <div class="price-section">
        <div class="current-price">
          <span class="price-label">价格</span>
          <span class="price-value">¥{{ product.price }}</span>
        </div>
        <div class="market-price" v-if="product.market_price > product.price">
          <span class="old-price">¥{{ product.market_price }}</span>
        </div>
      </div>

      <!-- 销量和评分 -->
      <div class="stats-section">
        <div class="stat-item">
          <span class="stat-label">销量</span>
          <span class="stat-value">{{ product.sales_count }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">评分</span>
          <el-rate
            v-model="ratingValue"
            disabled
            show-score
            text-color="#ff9900"
          />
        </div>
      </div>

      <!-- 简介 -->
      <div class="description" v-if="product.description">
        <p>{{ product.description }}</p>
      </div>
    </div>

    <!-- 商品详情 -->
    <div class="product-details">
      <div class="detail-header">
        <h2>商品详情</h2>
      </div>

      <!-- 详情图（按顺序展示） -->
      <div class="detail-images" v-if="product.detail_images?.length > 0">
        <img
          v-for="(image, index) in product.detail_images"
          :key="index"
          :src="image"
          :alt="`详情-${index + 1}`"
          class="detail-image"
        />
      </div>

      <!-- 富文本详情 -->
      <div class="detail-html" v-if="product.detail_html" v-html="product.detail_html"></div>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-actions">
      <el-button icon="Star" @click="handleFavorite">收藏</el-button>
      <el-button type="warning" icon="ShoppingCart" @click="handleAddToCart">
        加入购物车
      </el-button>
      <el-button type="danger" @click="handleBuyNow">立即购买</el-button>
    </div>
  </div>

  <div v-else class="loading">
    <el-skeleton :rows="10" animated />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const route = useRoute()
const product = ref(null)
const loading = ref(false)

// 评分值
const ratingValue = computed(() => {
  return product.value ? parseFloat(product.value.rating_average) : 5
})

// 加载商品详情
const loadProductDetail = async () => {
  try {
    loading.value = true
    const productId = route.params.id
    const { data } = await axios.get(`/api/products/${productId}/`)
    product.value = data

    // 统计浏览量
    await axios.post(`/api/products/${productId}/view/`)
  } catch (error) {
    console.error('加载商品详情失败:', error)
    ElMessage.error('加载失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 收藏
const handleFavorite = async () => {
  try {
    await axios.post(`/api/products/${product.value.id}/favorite/`)
    ElMessage.success('收藏成功')
    product.value.favorite_count++
  } catch (error) {
    ElMessage.error('收藏失败: ' + error.message)
  }
}

// 加入购物车
const handleAddToCart = async () => {
  try {
    await axios.post('/api/cart/add/', {
      product_id: product.value.id,
      quantity: 1
    })
    ElMessage.success('已加入购物车')
  } catch (error) {
    ElMessage.error('添加失败: ' + error.message)
  }
}

// 立即购买
const handleBuyNow = () => {
  // 跳转到订单确认页
  ElMessage.info('跳转到订单确认页')
}

onMounted(() => {
  loadProductDetail()
})
</script>

<style scoped>
.product-detail {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 60px;
}

/* 主图轮播 */
.main-images-carousel {
  background-color: #fff;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 商品信息 */
.product-info {
  background-color: #fff;
  padding: 15px;
  margin-top: 10px;
}

.product-name {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.product-tags {
  margin-bottom: 15px;
}

.product-tags .el-tag {
  margin-right: 8px;
}

/* 价格区域 */
.price-section {
  display: flex;
  align-items: baseline;
  margin-bottom: 15px;
}

.current-price {
  display: flex;
  align-items: baseline;
}

.price-label {
  font-size: 12px;
  color: #999;
  margin-right: 8px;
}

.price-value {
  font-size: 24px;
  color: #ff4500;
  font-weight: bold;
}

.market-price {
  margin-left: 15px;
}

.old-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

/* 统计信息 */
.stats-section {
  display: flex;
  gap: 30px;
  padding: 15px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.stat-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

/* 简介 */
.description {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

/* 商品详情 */
.product-details {
  background-color: #fff;
  margin-top: 10px;
  padding: 15px;
}

.detail-header {
  margin-bottom: 20px;
}

.detail-header h2 {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #ff4500;
}

/* 详情图 */
.detail-images {
  margin-top: 20px;
}

.detail-image {
  width: 100%;
  display: block;
  margin-bottom: 10px;
}

.detail-html {
  margin-top: 20px;
  line-height: 1.6;
}

.detail-html :deep(img) {
  width: 100%;
  display: block;
  margin-bottom: 10px;
}

/* 底部操作栏 */
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  padding: 10px;
  display: flex;
  gap: 10px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.bottom-actions .el-button {
  flex: 1;
}

/* 加载状态 */
.loading {
  padding: 20px;
  background-color: #fff;
}

/* 响应式 */
@media (min-width: 768px) {
  .product-detail {
    max-width: 750px;
    margin: 0 auto;
  }
}
</style>
