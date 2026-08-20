<template>
  <div class="product-detail-page">
    <!-- 顶部导航 -->
    <van-nav-bar
      :title="product.name"
      left-arrow
      fixed
      placeholder
      @click-left="handleBack"
    >
      <template #right>
        <div class="nav-right-actions">
          <van-icon name="ellipsis" size="20" @click="onMore" />
          <van-icon name="video-o" size="20" class="home-icon" />
        </div>
      </template>
    </van-nav-bar>

    <!-- 商品图片轮播 -->
    <van-swipe class="product-swiper" :autoplay="3000" indicator-color="#e93323">
      <van-swipe-item v-for="(image, index) in product.main_images" :key="index">
        <van-image :src="getImageUrl(image)" fit="cover" class="swiper-image" @click="onPreviewImage(index)" />
      </van-swipe-item>
    </van-swipe>

    <!-- 价格和标题信息 -->
    <div class="product-header">
      <div class="price-section">
        <div class="price">¥{{ product.price }}</div>
        <div class="coupon-link" @click="onCoupon">查看优惠 ></div>
      </div>
      <div class="product-title">{{ product.name }}</div>
      <div class="share-btn" @click="onShare">
        <van-icon name="share-o" size="16" />
        分享
      </div>
    </div>

    <!-- 商品评价 -->
    <div class="review-section" v-if="product.reviews">
      <div class="review-title">商品评价</div>
      <div class="review-summary" v-if="product.reviewSummary">
        <span class="review-tag" v-for="tag in product.reviewSummary" :key="tag.name">
          {{ tag.name }}({{ tag.count }})
        </span>
      </div>
    </div>

    <!-- 店铺信息 -->
    <div class="shop-section" v-if="product.shop">
      <div class="shop-info">
        <div class="shop-logo">
          <img :src="product.shop.logo" alt="" />
        </div>
        <div class="shop-detail">
          <div class="shop-name">{{ product.shop.name }}</div>
          <div class="shop-badges">
            <span class="badge" v-for="badge in product.shop.badges" :key="badge">
              <van-icon name="success" size="12" /> {{ badge }}
            </span>
          </div>
        </div>
        <div class="shop-action" @click="visitShop">进店逛逛</div>
      </div>
    </div>

    <!-- 商品详情 -->
    <div class="detail-section">
      <div class="section-title">商品详情</div>
      <div class="detail-content">
        <div v-if="product.detail_html" v-html="product.detail_html"></div>
        <div v-if="product.detail_images && product.detail_images.length > 0" class="detail-images">
          <img
            v-for="(image, index) in product.detail_images"
            :key="index"
            :src="getImageUrl(image)"
            style="width: 100%; display: block; margin-bottom: 10px;"
          />
        </div>
        <div v-if="!product.detail_html && (!product.detail_images || product.detail_images.length === 0)" style="padding: 40px; text-align: center; color: #999;">
          暂无详情
        </div>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <van-goods-action class="goods-action" safe-area-inset-bottom>
      <van-goods-action-icon icon="chat-o" text="客服" @click="onContact" />
      <van-goods-action-icon icon="shop-o" text="店铺" @click="visitShop" />
      <van-goods-action-icon
        icon="cart-o"
        text="购物车"
        :badge="cartCount"
        @click="onCart"
      />
      <van-goods-action-button
        type="warning"
        text="加入购物车"
        @click="addToCart"
      />
      <van-goods-action-button
        type="danger"
        text="立即购买"
        @click="buyNow"
      />
    </van-goods-action>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast, showImagePreview } from 'vant'
import { getProductDetail } from '@/api/product'

const route = useRoute()
const router = useRouter()

const cartCount = ref(0)
const loading = ref(false)

const product = ref({
  id: '',
  name: '',
  price: 0,
  market_price: 0,
  description: '',
  detail_html: '',
  main_images: [],
  detail_images: [],
  region_name: '',
  category_name: '',
  sales_count: 0,
  stock: 0,
  reviews: false,
  reviewSummary: [],
  shop: null,
  images: []
})

// 处理图片URL
const getImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  return `http://localhost:9000/yph-products/${url}`
}

// 加载商品详情
const loadProductDetail = async () => {
  const productId = route.params.id
  if (!productId) {
    showToast('商品ID不存在')
    return
  }

  loading.value = true
  try {
    const res = await getProductDetail(productId)
    console.log('商品详情数据:', res)

    // 更新商品信息
    product.value = {
      ...res,
      images: res.main_images || []
    }
  } catch (error) {
    console.error('获取商品详情失败:', error)
    showToast('获取商品详情失败')
  } finally {
    loading.value = false
  }
}

// 返回按钮处理
const handleBack = () => {
  router.back()
}

const goHome = () => {
  router.push('/home')
}

const onMore = () => {
  showToast('更多选项')
}

const onShare = () => {
  showToast('分享功能')
}

const onCoupon = () => {
  showToast('查看优惠券')
}

const visitShop = () => {
  showToast('进入店铺')
}

const onPreviewImage = (index) => {
  const images = (product.value.main_images || []).map(img => getImageUrl(img))
  showImagePreview({
    images: images,
    startPosition: index
  })
}

const onContact = () => {
  showToast('联系客服')
}

const onCart = () => {
  router.push('/cart')
}

const onCollect = () => {
  showToast('已收藏')
}

const addToCart = () => {
  cartCount.value++
  showToast('已加入购物车')
}

const buyNow = () => {
  showToast('立即购买')
  // TODO: 跳转到订单确认页
}

onMounted(() => {
  loadProductDetail()
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.product-detail-page {
  min-height: 100vh;
  background: $bg-color;
}

// 顶部导航
:deep(.van-nav-bar) {
  background: $bg-color-white;
  border-bottom: 1px solid #f0f0f0;

  .van-nav-bar__title {
    font-size: $font-size-base;
    font-weight: 400;
    color: $text-color-primary;
  }

  .van-nav-bar__arrow,
  .van-icon {
    color: $text-color-primary;
  }
}

.nav-right-actions {
  display: flex;
  align-items: center;
  gap: 16px;

  .van-icon {
    cursor: pointer;
    transition: opacity 0.2s;

    &:active {
      opacity: 0.7;
    }
  }

  .home-icon {
    font-size: 20px;
  }
}

// 商品轮播
.product-swiper {
  height: 375px;
  background: $bg-color-white;

  .swiper-image {
    width: 100%;
    height: 100%;
  }
}

// 商品头部信息
.product-header {
  background: $bg-color-white;
  padding: $spacing-lg;
  margin-bottom: $spacing-base;
  position: relative;

  .price-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-base;

    .price {
      color: $text-color-primary;
      font-size: 32px;
      font-weight: 600;
    }

    .coupon-link {
      color: $theme-color;
      font-size: $font-size-sm;
      cursor: pointer;

      &:active {
        opacity: 0.7;
      }
    }
  }

  .product-title {
    font-size: $font-size-base;
    font-weight: 400;
    color: $text-color-primary;
    line-height: 1.5;
    margin-bottom: 40px;
  }

  .share-btn {
    position: absolute;
    bottom: $spacing-lg;
    right: $spacing-lg;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 12px;
    background: $bg-color;
    border-radius: 20px;
    font-size: $font-size-sm;
    color: $text-color-secondary;
    cursor: pointer;

    &:active {
      opacity: 0.7;
    }
  }
}

// 商品评价区域
.review-section {
  background: $bg-color-white;
  padding: $spacing-lg;
  margin-bottom: $spacing-base;

  .review-title {
    font-size: $font-size-base;
    font-weight: 500;
    color: $text-color-primary;
    margin-bottom: $spacing-base;
  }

  .review-summary {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-sm;

    .review-tag {
      padding: 4px 12px;
      background: $bg-color;
      color: $text-color-secondary;
      font-size: $font-size-sm;
      border-radius: 4px;
    }
  }
}

// 店铺信息区域
.shop-section {
  background: $bg-color-white;
  padding: $spacing-lg;
  margin-bottom: $spacing-base;

  .shop-info {
    display: flex;
    align-items: center;
    gap: $spacing-base;

    .shop-logo {
      width: 48px;
      height: 48px;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .shop-detail {
      flex: 1;

      .shop-name {
        font-size: $font-size-base;
        font-weight: 500;
        color: $text-color-primary;
        margin-bottom: 4px;
      }

      .shop-badges {
        display: flex;
        gap: $spacing-sm;
        flex-wrap: wrap;

        .badge {
          display: flex;
          align-items: center;
          gap: 2px;
          font-size: $font-size-xs;
          color: $text-color-tertiary;

          :deep(.van-icon) {
            color: #52c41a;
          }
        }
      }
    }

    .shop-action {
      padding: 6px 16px;
      border: 1px solid $theme-color;
      border-radius: 20px;
      color: $theme-color;
      font-size: $font-size-sm;
      cursor: pointer;
      flex-shrink: 0;

      &:active {
        opacity: 0.7;
      }
    }
  }
}

// 详情区域
.detail-section {
  background: $bg-color-white;
  padding: $spacing-lg 0;

  .section-title {
    padding: 0 $spacing-lg;
    font-size: $font-size-base;
    font-weight: 600;
    color: $text-color-primary;
    margin-bottom: $spacing-base;
  }

  .detail-content {
    :deep(img) {
      display: block;
      width: 100%;
      height: auto;
    }

    :deep(h3) {
      font-size: $font-size-lg;
      margin: 15px 0;
    }

    :deep(p) {
      margin: 8px 0;
      line-height: 1.8;
    }
  }
}

// 底部操作栏
.goods-action {
  :deep(.van-goods-action-icon) {
    .van-icon {
      font-size: 20px;
    }

    .van-goods-action-icon__text {
      font-size: $font-size-xs;
    }
  }

  :deep(.van-goods-action-button) {
    &.van-goods-action-button--warning {
      background: linear-gradient(135deg, #faad14 0%, #fa8c16 100%);
    }

    &.van-goods-action-button--danger {
      background: linear-gradient(135deg, $theme-color 0%, $theme-color-hover 100%);
    }
  }
}
</style>
