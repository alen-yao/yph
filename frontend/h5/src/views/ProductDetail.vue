<template>
  <div class="product-detail-page">
    <!-- 顶部导航 -->
    <van-nav-bar
      title="商品详情"
      left-arrow
      fixed
      placeholder
      @click-left="$router.back()"
    >
      <template #right>
        <van-icon name="share-o" size="18" @click="onShare" />
      </template>
    </van-nav-bar>

    <!-- 商品图片轮播 -->
    <van-swipe class="product-swiper" :autoplay="3000" indicator-color="#e93323">
      <van-swipe-item v-for="(image, index) in product.images" :key="index">
        <van-image :src="image" fit="cover" class="swiper-image" @click="onPreviewImage(index)" />
      </van-swipe-item>
    </van-swipe>

    <!-- 价格和标题信息 -->
    <div class="product-header">
      <div class="price-section">
        <div class="price">{{ product.price }}</div>
        <div class="market-price" v-if="product.market_price">
          ¥{{ product.market_price }}
        </div>
      </div>
      <div class="product-title">{{ product.name }}</div>
      <div class="product-subtitle" v-if="product.description">
        {{ product.description }}
      </div>
      <div class="product-tags">
        <span class="tag tag-hot" v-if="product.is_hot">热销</span>
        <span class="tag tag-new" v-if="product.is_new">新品</span>
        <span class="sales-info">已售 {{ product.sales || 0 }} 件</span>
      </div>
    </div>

    <!-- 促销活动 -->
    <div class="promotion-section" v-if="product.promotions && product.promotions.length">
      <van-cell
        v-for="promo in product.promotions"
        :key="promo.id"
        :title="promo.title"
        :label="promo.desc"
        is-link
      >
        <template #icon>
          <div class="promo-tag">{{ promo.tag }}</div>
        </template>
      </van-cell>
    </div>

    <!-- 商品参数 -->
    <van-cell-group class="param-section" title="商品参数">
      <van-cell title="品牌" :value="product.brand || '无'" />
      <van-cell title="分类" :value="product.category || '无'" />
      <van-cell title="库存" :value="product.stock ? `${product.stock} 件` : '无货'" />
      <van-cell title="发货" value="24小时内发货" />
    </van-cell-group>

    <!-- 商品详情 -->
    <div class="detail-section">
      <div class="section-title">商品详情</div>
      <div class="detail-content" v-html="product.detail_html"></div>
    </div>

    <!-- 底部操作栏 -->
    <van-goods-action class="goods-action" safe-area-inset-bottom>
      <van-goods-action-icon icon="chat-o" text="客服" @click="onContact" />
      <van-goods-action-icon
        icon="cart-o"
        text="购物车"
        :badge="cartCount"
        @click="onCart"
      />
      <van-goods-action-icon icon="star-o" text="收藏" @click="onCollect" />
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

const route = useRoute()
const router = useRouter()

const cartCount = ref(0)

const product = ref({
  id: 1,
  name: 'YPH 精选优质商品 - 高品质正品保障 全国联保',
  price: 299.00,
  market_price: 599.00,
  description: '精选优质材料，匠心工艺，为您提供卓越的使用体验',
  brand: 'YPH官方',
  category: '数码电器',
  stock: 999,
  sales: 12580,
  is_hot: true,
  is_new: false,
  promotions: [
    { id: 1, tag: '促销', title: '限时优惠', desc: '满299减30，满599减80' },
    { id: 2, tag: '优惠', title: '新人专享', desc: '新用户立减50元' }
  ],
  detail_html: `
    <div style="padding: 15px; line-height: 1.8; color: #333;">
      <h3 style="margin-bottom: 15px; color: #e93323;">产品特点</h3>
      <p>1. 高品质材料，精工细作</p>
      <p>2. 人性化设计，使用便捷</p>
      <p>3. 专业品质保证，售后无忧</p>
      <br/>
      <img src="https://via.placeholder.com/375x300/E8F4F8/E93323?text=Product+Detail+1" style="width: 100%; margin: 10px 0;" />
      <h3 style="margin: 20px 0 15px; color: #e93323;">规格参数</h3>
      <p>• 产品尺寸：标准尺寸</p>
      <p>• 产品重量：轻便便携</p>
      <p>• 包装清单：主机 x1，配件 x1，说明书 x1</p>
      <br/>
      <img src="https://via.placeholder.com/375x300/E8F4F8/1890FF?text=Product+Detail+2" style="width: 100%; margin: 10px 0;" />
      <h3 style="margin: 20px 0 15px; color: #e93323;">温馨提示</h3>
      <p>• 请仔细阅读产品说明书</p>
      <p>• 如有质量问题，7天无理由退换</p>
      <p>• 全国联保，终身维护</p>
    </div>
  `,
  images: [
    'https://via.placeholder.com/375x375/E8F4F8/E93323?text=YPH+Product+1',
    'https://via.placeholder.com/375x375/FFF7E6/FA8C16?text=YPH+Product+2',
    'https://via.placeholder.com/375x375/E6F7FF/1890FF?text=YPH+Product+3',
    'https://via.placeholder.com/375x375/F0F5FF/597EF7?text=YPH+Product+4'
  ]
})

const onShare = () => {
  showToast('分享功能')
}

const onPreviewImage = (index) => {
  showImagePreview({
    images: product.value.images,
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
  const productId = route.params.id
  console.log('加载商品详情:', productId)
  // TODO: 从 API 加载商品详情
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.product-detail-page {
  min-height: 100vh;
  background: $bg-color;
  padding-bottom: 50px;
}

// 顶部导航
:deep(.van-nav-bar) {
  background: linear-gradient(135deg, $theme-color 0%, $theme-color-hover 100%);

  .van-nav-bar__title,
  .van-nav-bar__arrow,
  .van-icon {
    color: $text-color-white;
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

  .price-section {
    display: flex;
    align-items: baseline;
    gap: $spacing-sm;
    margin-bottom: $spacing-base;

    .price {
      color: $theme-color;
      font-size: 28px;
      font-weight: 700;

      &::before {
        content: '¥';
        font-size: 18px;
        margin-right: 2px;
      }
    }

    .market-price {
      color: $text-color-tertiary;
      font-size: $font-size-sm;
      text-decoration: line-through;
    }
  }

  .product-title {
    font-size: $font-size-lg;
    font-weight: 600;
    color: $text-color-primary;
    line-height: 1.5;
    margin-bottom: $spacing-sm;
  }

  .product-subtitle {
    font-size: $font-size-sm;
    color: $text-color-secondary;
    line-height: 1.5;
    margin-bottom: $spacing-base;
  }

  .product-tags {
    display: flex;
    align-items: center;
    gap: $spacing-sm;

    .sales-info {
      color: $text-color-tertiary;
      font-size: $font-size-sm;
      margin-left: auto;
    }
  }
}

// 促销活动区域
.promotion-section {
  margin-bottom: $spacing-base;

  :deep(.van-cell) {
    padding-left: $spacing-lg;
    padding-right: $spacing-lg;

    .promo-tag {
      display: inline-block;
      padding: 2px 6px;
      background: $theme-color-light;
      color: $theme-color;
      font-size: $font-size-xs;
      border-radius: $border-radius-sm;
      margin-right: $spacing-sm;
      font-weight: 500;
    }

    .van-cell__title {
      color: $text-color-primary;
      font-weight: 500;
    }

    .van-cell__label {
      color: $text-color-secondary;
    }
  }
}

// 参数区域
.param-section {
  margin-bottom: $spacing-base;

  :deep(.van-cell) {
    padding-left: $spacing-lg;
    padding-right: $spacing-lg;
  }

  :deep(.van-cell-group__title) {
    padding-left: $spacing-lg;
    padding-right: $spacing-lg;
    font-size: $font-size-base;
    font-weight: 600;
    color: $text-color-primary;
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
