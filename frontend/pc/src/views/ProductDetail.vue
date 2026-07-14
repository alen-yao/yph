<template>
  <div class="product-detail-page">
    <div class="container">
      <div class="product-main">
        <!-- 商品图片 -->
        <div class="product-gallery">
          <div class="main-image">
            <img :src="currentImage" alt="商品图片" @click="previewImage" />
          </div>
          <div class="thumbnail-list">
            <div
              v-for="(image, index) in product.images"
              :key="index"
              :class="['thumbnail-item', { active: currentImageIndex === index }]"
              @click="selectImage(index)"
            >
              <img :src="image" alt="缩略图" />
            </div>
          </div>
        </div>

        <!-- 商品信息 -->
        <div class="product-info-panel">
          <h1 class="product-title">{{ product.name }}</h1>
          <div class="product-subtitle">{{ product.description }}</div>

          <div class="price-section">
            <div class="price-row">
              <span class="label">售价：</span>
              <div class="price price-large">{{ product.price }}</div>
              <div class="market-price" v-if="product.market_price">
                市场价：¥{{ product.market_price }}
              </div>
            </div>
            <div class="sales-info">
              <span>累计评价：<em>{{ product.reviews || 0 }}</em></span>
              <span>累计销量：<em>{{ product.sales || 0 }}</em></span>
            </div>
          </div>

          <div class="promotion-section" v-if="product.promotions">
            <div class="promo-item" v-for="promo in product.promotions" :key="promo.id">
              <span class="promo-tag">{{ promo.tag }}</span>
              <span class="promo-desc">{{ promo.desc }}</span>
            </div>
          </div>

          <div class="param-section">
            <div class="param-item">
              <span class="label">品牌：</span>
              <span class="value">{{ product.brand || 'YPH官方' }}</span>
            </div>
            <div class="param-item">
              <span class="label">分类：</span>
              <span class="value">{{ product.category || '数码电器' }}</span>
            </div>
            <div class="param-item">
              <span class="label">库存：</span>
              <span class="value">{{ product.stock || 999 }} 件</span>
            </div>
          </div>

          <div class="quantity-section">
            <span class="label">数量：</span>
            <el-input-number
              v-model="quantity"
              :min="1"
              :max="product.stock || 999"
              size="large"
            />
          </div>

          <div class="action-buttons">
            <el-button type="primary" size="large" @click="buyNow">
              <el-icon><ShoppingCart /></el-icon>
              立即购买
            </el-button>
            <el-button size="large" @click="addToCart">加入购物车</el-button>
            <el-button size="large" icon="Star" @click="addToFavorite">收藏</el-button>
          </div>
        </div>
      </div>

      <!-- 商品详情标签页 -->
      <div class="product-detail-tabs">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="商品详情" name="detail">
            <div class="detail-content" v-html="product.detail_html"></div>
          </el-tab-pane>
          <el-tab-pane label="规格参数" name="params">
            <div class="params-table">
              <table>
                <tr v-for="param in product.params" :key="param.name">
                  <td class="param-name">{{ param.name }}</td>
                  <td class="param-value">{{ param.value }}</td>
                </tr>
              </table>
            </div>
          </el-tab-pane>
          <el-tab-pane label="用户评价" name="reviews">
            <div class="reviews-section">
              <p class="empty-text">暂无评价</p>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 推荐商品 -->
      <div class="recommend-section">
        <h2 class="section-title">相关推荐</h2>
        <div class="product-grid">
          <div
            v-for="item in recommendProducts"
            :key="item.id"
            class="product-card"
            @click="goToProduct(item.id)"
          >
            <div class="product-image">
              <img :src="item.main_image" :alt="item.name" />
            </div>
            <div class="product-info">
              <div class="product-name ellipsis-2">{{ item.name }}</div>
              <div class="price">{{ item.price }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const activeTab = ref('detail')
const quantity = ref(1)
const currentImageIndex = ref(0)

const product = ref({
  id: 1,
  name: 'YPH 精选优质商品 - 高品质正品保障 全国联保',
  description: '精选优质材料，匠心工艺，为您提供卓越的使用体验',
  price: 299.00,
  market_price: 599.00,
  brand: 'YPH官方',
  category: '数码电器',
  stock: 999,
  sales: 12580,
  reviews: 8650,
  promotions: [
    { id: 1, tag: '促销', desc: '满299减30，满599减80' },
    { id: 2, tag: '优惠', desc: '新人专享立减50元' }
  ],
  images: [
    'https://via.placeholder.com/600x600/E8F4F8/E93323?text=YPH+Product+1',
    'https://via.placeholder.com/600x600/FFF7E6/FA8C16?text=YPH+Product+2',
    'https://via.placeholder.com/600x600/E6F7FF/1890FF?text=YPH+Product+3',
    'https://via.placeholder.com/600x600/F0F5FF/597EF7?text=YPH+Product+4'
  ],
  detail_html: `
    <div style="padding: 20px; line-height: 1.8;">
      <h2 style="margin-bottom: 20px; color: #e93323;">产品特点</h2>
      <p>1. 高品质材料，精工细作</p>
      <p>2. 人性化设计，使用便捷</p>
      <p>3. 专业品质保证，售后无忧</p>
      <br/>
      <img src="https://via.placeholder.com/800x400/E8F4F8/E93323?text=Product+Detail+1" style="width: 100%; margin: 20px 0;" />
      <h2 style="margin: 30px 0 20px; color: #e93323;">产品优势</h2>
      <p>• 优质材料，经久耐用</p>
      <p>• 先进工艺，品质卓越</p>
      <p>• 贴心服务，售后无忧</p>
      <br/>
      <img src="https://via.placeholder.com/800x400/E8F4F8/1890FF?text=Product+Detail+2" style="width: 100%; margin: 20px 0;" />
    </div>
  `,
  params: [
    { name: '商品名称', value: 'YPH精选商品' },
    { name: '商品编号', value: 'YPH2024001' },
    { name: '品牌', value: 'YPH官方' },
    { name: '产地', value: '中国' },
    { name: '保修期', value: '12个月' }
  ]
})

const recommendProducts = ref([])

const currentImage = computed(() => {
  return product.value.images[currentImageIndex.value]
})

const selectImage = (index) => {
  currentImageIndex.value = index
}

const previewImage = () => {
  // TODO: 实现图片预览
  ElMessage.info('图片预览功能')
}

const buyNow = () => {
  ElMessage.success('立即购买')
  // TODO: 跳转到订单确认页
}

const addToCart = () => {
  ElMessage.success(`已将 ${quantity.value} 件商品加入购物车`)
}

const addToFavorite = () => {
  ElMessage.success('已收藏')
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  const productId = route.params.id
  console.log('加载商品详情:', productId)

  // 生成推荐商品
  recommendProducts.value = Array.from({ length: 5 }, (_, i) => ({
    id: i + 100,
    name: `YPH 推荐商品 ${i + 1}`,
    main_image: `https://via.placeholder.com/200x200/E8F4F8/999?text=Recommend+${i + 1}`,
    price: (Math.random() * 500 + 100).toFixed(2)
  }))
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.product-detail-page {
  padding: 20px 0 60px;
}

.product-main {
  display: flex;
  gap: 30px;
  background: $bg-color-white;
  padding: 30px;
  border-radius: $border-radius-lg;
  margin-bottom: 20px;
}

// 商品图片
.product-gallery {
  width: 450px;
  flex-shrink: 0;

  .main-image {
    width: 100%;
    height: 450px;
    border: 1px solid $border-color;
    border-radius: $border-radius-base;
    overflow: hidden;
    margin-bottom: 12px;
    cursor: zoom-in;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .thumbnail-list {
    display: flex;
    gap: 8px;

    .thumbnail-item {
      width: 80px;
      height: 80px;
      border: 2px solid transparent;
      border-radius: $border-radius-base;
      overflow: hidden;
      cursor: pointer;
      transition: border-color 0.3s;

      &:hover,
      &.active {
        border-color: $theme-color;
      }

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }
  }
}

// 商品信息
.product-info-panel {
  flex: 1;

  .product-title {
    font-size: 20px;
    font-weight: 600;
    color: $text-color-primary;
    line-height: 1.5;
    margin-bottom: 12px;
  }

  .product-subtitle {
    font-size: $font-size-sm;
    color: $text-color-secondary;
    line-height: 1.5;
    margin-bottom: 24px;
  }

  .price-section {
    background: $bg-color-light;
    padding: 20px;
    border-radius: $border-radius-base;
    margin-bottom: 20px;

    .price-row {
      display: flex;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 12px;

      .label {
        color: $text-color-secondary;
      }

      .market-price {
        font-size: $font-size-sm;
        color: $text-color-tertiary;
        text-decoration: line-through;
      }
    }

    .sales-info {
      display: flex;
      gap: 24px;
      font-size: $font-size-sm;
      color: $text-color-secondary;

      em {
        color: $theme-color;
        font-style: normal;
        font-weight: 600;
        margin: 0 4px;
      }
    }
  }

  .promotion-section {
    margin-bottom: 20px;

    .promo-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 8px 0;
      font-size: $font-size-sm;

      .promo-tag {
        display: inline-block;
        padding: 2px 8px;
        background: $theme-color-light;
        color: $theme-color;
        border-radius: $border-radius-sm;
        font-weight: 500;
      }

      .promo-desc {
        color: $text-color-secondary;
      }
    }
  }

  .param-section {
    margin-bottom: 24px;
    padding: 16px 0;
    border-top: 1px solid $border-color-light;
    border-bottom: 1px solid $border-color-light;

    .param-item {
      display: flex;
      padding: 8px 0;
      font-size: $font-size-sm;

      .label {
        width: 80px;
        color: $text-color-tertiary;
      }

      .value {
        color: $text-color-secondary;
      }
    }
  }

  .quantity-section {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;

    .label {
      font-size: $font-size-base;
      color: $text-color-secondary;
    }
  }

  .action-buttons {
    display: flex;
    gap: 12px;

    .el-button {
      flex: 1;
    }
  }
}

// 详情标签页
.product-detail-tabs {
  background: $bg-color-white;
  padding: 30px;
  border-radius: $border-radius-lg;
  margin-bottom: 20px;

  .detail-content {
    :deep(img) {
      max-width: 100%;
      height: auto;
    }

    :deep(h2) {
      font-size: $font-size-xl;
      margin: 20px 0;
    }
  }

  .params-table {
    table {
      width: 100%;
      border-collapse: collapse;

      tr {
        border-bottom: 1px solid $border-color-light;

        &:last-child {
          border-bottom: none;
        }
      }

      td {
        padding: 16px 20px;
        font-size: $font-size-base;

        &.param-name {
          width: 200px;
          background: $bg-color-light;
          color: $text-color-secondary;
        }

        &.param-value {
          color: $text-color-primary;
        }
      }
    }
  }

  .reviews-section {
    padding: 40px 0;
    text-align: center;

    .empty-text {
      color: $text-color-tertiary;
    }
  }
}

// 推荐商品
.recommend-section {
  background: $bg-color-white;
  padding: 30px;
  border-radius: $border-radius-lg;

  .section-title {
    font-size: $font-size-xl;
    font-weight: 600;
    margin-bottom: 20px;
    padding-left: 12px;
    border-left: 4px solid $theme-color;
  }

  .product-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
  }

  .product-card {
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-4px);
    }

    .product-image {
      width: 100%;
      padding-top: 100%;
      position: relative;
      overflow: hidden;
      border-radius: $border-radius-base;
      background: $bg-color-grey;
      margin-bottom: 12px;

      img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .product-info {
      .product-name {
        font-size: $font-size-sm;
        color: $text-color-primary;
        line-height: 1.4;
        margin-bottom: 8px;
        min-height: 40px;
      }

      .price {
        font-size: $font-size-lg;
      }
    }
  }
}
</style>
