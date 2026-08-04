<template>
  <div class="home-page">
    <!-- 顶部导航栏 -->
    <div class="top-nav-bar">
      <van-icon name="wap-nav" size="20" class="nav-icon" />
      <van-search
        v-model="searchValue"
        shape="round"
        placeholder="搜索特产名称、产地"
        background="transparent"
        @search="onSearch"
      >
        <template #left-icon>
          <van-icon name="search" size="16" color="#999" />
        </template>
      </van-search>
      <div class="nav-right">
        <van-icon name="ellipsis" size="20" class="nav-icon" />
        <van-icon name="scan" size="20" class="nav-icon" />
      </div>
    </div>

    <!-- 占位元素，避免内容被固定搜索栏遮挡 -->
    <div class="search-bar-placeholder"></div>

    <!-- 轮播图 -->
    <van-swipe class="banner-swiper" :autoplay="3000" indicator-color="#FF6B35">
      <van-swipe-item v-for="banner in banners" :key="banner.id">
        <img :src="banner.image" class="banner-img" alt="轮播图" />
      </van-swipe-item>
    </van-swipe>

    <!-- 热门省份 - 省份分类导航 -->
    <div class="province-section">
      <div class="section-header">
        <div class="header-left">
          <div class="header-icon">🗺️</div>
          <span class="section-title">热门产地</span>
        </div>
        <van-button size="small" plain hairline @click="goToCategory">
          更多省份 <van-icon name="arrow" />
        </van-button>
      </div>

      <div class="province-grid">
        <div
          v-for="province in provinces.slice(0, 10)"
          :key="province.id"
          class="province-item"
          @click="onProvinceClick(province)"
        >
          <div class="province-icon">
            <div class="province-emoji">{{ province.emoji }}</div>
          </div>
          <div class="province-name">{{ province.name }}</div>
        </div>
      </div>
    </div>

    <!-- 特色专区 -->
    <div class="feature-zones">
      <!-- 云南特产专区 -->
      <div class="zone-card" v-for="zone in featureZones" :key="zone.id">
        <div class="zone-header">
          <div class="zone-title">
            <span class="zone-emoji">{{ zone.emoji }}</span>
            <span class="zone-name">{{ zone.title }}</span>
          </div>
          <van-button size="mini" plain hairline @click="goToZone(zone.id)">
            查看更多 <van-icon name="arrow" size="12" />
          </van-button>
        </div>

        <div class="zone-products">
          <div
            v-for="product in zone.products"
            :key="product.id"
            class="zone-product-card"
            @click="goToProduct(product.id)"
          >
            <van-image
              :src="product.image"
              fit="cover"
              class="zone-product-image"
              lazy-load
            >
              <template #loading>
                <van-loading type="spinner" size="16" />
              </template>
            </van-image>
            <div class="zone-product-info">
              <div class="zone-product-name">{{ product.name }}</div>
              <div class="zone-product-origin">
                <van-icon name="location-o" size="10" />
                {{ product.origin }}
              </div>
              <div class="zone-product-footer">
                <div class="zone-product-price">¥{{ product.price }}</div>
                <div class="zone-product-sales">{{ product.sales }}人购买</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 全部特产 - 瀑布流展示 -->
    <div class="all-products-section">
      <div class="section-divider">
        <span class="divider-text">精选特产</span>
      </div>

      <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <van-list
          v-model:loading="loading"
          :finished="finished"
          finished-text="没有更多了"
          @load="onLoad"
        >
          <div class="product-waterfall">
            <div
              v-for="product in productList"
              :key="product.id"
              class="product-card"
              @click="goToProduct(product.id)"
            >
              <div class="product-image-wrapper">
                <van-image
                  :src="product.main_image"
                  fit="cover"
                  class="product-image"
                  lazy-load
                >
                  <template #loading>
                    <van-loading type="spinner" size="20" />
                  </template>
                </van-image>
                <div class="product-badge" v-if="product.badge">
                  <van-tag plain type="danger" size="mini">{{ product.badge }}</van-tag>
                </div>
              </div>

              <div class="product-info">
                <div class="product-origin-tag">
                  <van-icon name="location-o" size="10" />
                  {{ product.origin }}
                </div>
                <div class="product-name">{{ product.name }}</div>
                <div class="product-desc" v-if="product.desc">{{ product.desc }}</div>
                <div class="product-footer">
                  <div class="product-price">
                    <span class="price-symbol">¥</span>
                    <span class="price-value">{{ product.price }}</span>
                    <span class="price-unit" v-if="product.unit">/{{ product.unit }}</span>
                  </div>
                  <div class="product-sales">{{ product.sales }}+人购买</div>
                </div>
              </div>
            </div>
          </div>
        </van-list>
      </van-pull-refresh>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()
const searchValue = ref('')
const refreshing = ref(false)
const loading = ref(false)
const finished = ref(false)

// 轮播图
const banners = ref([
  { id: 1, image: 'https://via.placeholder.com/750x360/FF6B35/FFFFFF?text=全国特产·优选好货' },
  { id: 2, image: 'https://via.placeholder.com/750x360/4ECDC4/FFFFFF?text=地道风味·源产地直供' },
  { id: 3, image: 'https://via.placeholder.com/750x360/95E1D3/FFFFFF?text=新鲜到家·品质保障' }
])

// 热门省份
const provinces = ref([
  { id: 1, name: '云南', emoji: '🌄' },
  { id: 2, name: '新疆', emoji: '🏔️' },
  { id: 3, name: '山东', emoji: '🌊' },
  { id: 4, name: '四川', emoji: '🌶️' },
  { id: 5, name: '浙江', emoji: '🍃' },
  { id: 6, name: '江苏', emoji: '🏮' },
  { id: 7, name: '广东', emoji: '🌴' },
  { id: 8, name: '福建', emoji: '🍊' },
  { id: 9, name: '海南', emoji: '🥥' },
  { id: 10, name: '更多', emoji: '📍' }
])

// 特色专区
const featureZones = ref([
  {
    id: 1,
    title: '云南特产',
    emoji: '🌄',
    products: [
      {
        id: 101,
        name: '云南小粒咖啡',
        origin: '云南普洱',
        image: 'https://via.placeholder.com/160/8B4513/FFFFFF?text=咖啡',
        price: '58.00',
        sales: 1200
      },
      {
        id: 102,
        name: '文山三七粉',
        origin: '云南文山',
        image: 'https://via.placeholder.com/160/228B22/FFFFFF?text=三七',
        price: '128.00',
        sales: 856
      },
      {
        id: 103,
        name: '宣威火腿',
        origin: '云南宣威',
        image: 'https://via.placeholder.com/160/DC143C/FFFFFF?text=火腿',
        price: '168.00',
        sales: 645
      }
    ]
  },
  {
    id: 2,
    title: '新疆特产',
    emoji: '🏔️',
    products: [
      {
        id: 201,
        name: '若羌红枣',
        origin: '新疆若羌',
        image: 'https://via.placeholder.com/160/CD5C5C/FFFFFF?text=红枣',
        price: '45.00',
        sales: 2100
      },
      {
        id: 202,
        name: '阿克苏苹果',
        origin: '新疆阿克苏',
        image: 'https://via.placeholder.com/160/FF6347/FFFFFF?text=苹果',
        price: '39.90',
        sales: 1580
      },
      {
        id: 203,
        name: '和田大枣',
        origin: '新疆和田',
        image: 'https://via.placeholder.com/160/8B0000/FFFFFF?text=大枣',
        price: '52.00',
        sales: 980
      }
    ]
  }
])

// 全部特产列表
const productList = ref([])

const onSearch = (value) => {
  if (value.trim()) {
    showToast(`搜索: ${value}`)
    // TODO: 执行搜索逻辑
  }
}

const goToCategory = () => {
  router.push('/category')
}

const onProvinceClick = (province) => {
  showToast(`查看${province.name}特产`)
  // TODO: 跳转到该省份的特产列表
}

const goToZone = (zoneId) => {
  showToast(`查看专区`)
  // TODO: 跳转到专区页面
}

const onRefresh = () => {
  refreshing.value = true
  productList.value = []
  finished.value = false

  setTimeout(() => {
    onLoad()
    refreshing.value = false
  }, 1000)
}

const onLoad = () => {
  if (refreshing.value) return

  loading.value = true

  const origins = ['云南昆明', '新疆和田', '山东烟台', '四川成都', '浙江杭州', '江苏苏州', '广东广州', '福建福州', '海南三亚']
  const specialties = [
    { name: '野生菌礼盒', badge: '新鲜直供' },
    { name: '手工核桃糕', badge: '传统工艺' },
    { name: '山地蜂蜜', badge: '农家自采' },
    { name: '茶叶礼盒', badge: '明前春茶' },
    { name: '阳澄湖大闸蟹', badge: '产地直发' },
    { name: '烟台苹果', badge: '脆甜多汁' },
    { name: '海南芒果', badge: '热带水果' },
    { name: '松茸干货', badge: '野生精选' }
  ]

  setTimeout(() => {
    for (let i = 0; i < 10; i++) {
      const index = productList.value.length
      const specialty = specialties[index % specialties.length]
      const origin = origins[index % origins.length]

      productList.value.push({
        id: 1000 + index,
        name: specialty.name,
        desc: '原产地直供，新鲜品质保障',
        origin: origin,
        main_image: `https://via.placeholder.com/200/F4A460/FFFFFF?text=${specialty.name}`,
        price: (Math.random() * 150 + 20).toFixed(2),
        unit: index % 3 === 0 ? '500g' : index % 3 === 1 ? '盒' : '份',
        sales: Math.floor(Math.random() * 5000 + 100),
        badge: Math.random() > 0.6 ? specialty.badge : null
      })
    }
    loading.value = false

    if (productList.value.length >= 40) {
      finished.value = true
    }
  }, 800)
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

onMounted(() => {
  // 初始加载第一页数据会自动触发
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.home-page {
  min-height: 100vh;
  background: $bg-color;
  padding-bottom: 50px;
}

// 顶部导航栏
.top-nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background: #fff;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .nav-icon {
    color: #333;
    flex-shrink: 0;
  }

  :deep(.van-search) {
    flex: 1;
    padding: 0;

    .van-search__content {
      background: #f5f5f5;
      border-radius: 20px;
      padding-left: 12px;
      padding-right: 12px;
    }

    .van-field__control {
      font-size: 14px;

      &::placeholder {
        color: #999;
      }
    }
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
  }
}

// 搜索栏占位
.search-bar-placeholder {
  height: 52px;
}

// 轮播图
.banner-swiper {
  height: 180px;
  background: $bg-color-white;

  .banner-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

// 省份分类区域
.province-section {
  background: $bg-color-white;
  padding: 16px;
  margin-bottom: 8px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;

  .header-left {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .header-icon {
    font-size: 18px;
  }

  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
  }
}

.province-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px 8px;
}

.province-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;

  &:active {
    opacity: 0.7;
  }

  .province-icon {
    width: 54px;
    height: 54px;
    border-radius: 50%;
    background: linear-gradient(135deg, #FFF5E6 0%, #FFE8CC 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s;
    box-shadow: 0 2px 8px rgba(255, 107, 53, 0.15);

    &:active {
      transform: scale(0.95);
    }
  }

  .province-emoji {
    font-size: 28px;
  }

  .province-name {
    font-size: 12px;
    color: #666;
    text-align: center;
    line-height: 1.2;
  }
}

// 特色专区
.feature-zones {
  background: $bg-color;
  padding: 8px 0;
}

.zone-card {
  background: $bg-color-white;
  margin-bottom: 8px;
  padding: 16px;

  .zone-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
  }

  .zone-title {
    display: flex;
    align-items: center;
    gap: 6px;

    .zone-emoji {
      font-size: 20px;
    }

    .zone-name {
      font-size: 16px;
      font-weight: 600;
      color: #333;
    }
  }

  .zone-products {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 4px;

    &::-webkit-scrollbar {
      display: none;
    }
  }

  .zone-product-card {
    flex-shrink: 0;
    width: 120px;
    background: #fff;
    cursor: pointer;

    &:active {
      opacity: 0.8;
    }
  }

  .zone-product-image {
    width: 120px;
    height: 120px;
    background: #f5f5f5;
    border-radius: 8px;
    overflow: hidden;
  }

  .zone-product-info {
    padding-top: 8px;
  }

  .zone-product-name {
    font-size: 13px;
    color: #333;
    margin-bottom: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .zone-product-origin {
    display: flex;
    align-items: center;
    gap: 2px;
    font-size: 11px;
    color: #999;
    margin-bottom: 6px;
  }

  .zone-product-footer {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  .zone-product-price {
    color: #FF6B35;
    font-size: 15px;
    font-weight: bold;
  }

  .zone-product-sales {
    font-size: 10px;
    color: #999;
  }
}

// 全部特产区域
.all-products-section {
  background: $bg-color;
  padding: 8px 0 16px;
}

.section-divider {
  text-align: center;
  padding: 16px 0;
  position: relative;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 30%;
    height: 1px;
    background: linear-gradient(to right, transparent, #ddd, transparent);
  }

  &::before {
    left: 0;
  }

  &::after {
    right: 0;
  }

  .divider-text {
    font-size: 14px;
    color: #999;
    background: $bg-color;
    padding: 0 12px;
  }
}

// 瀑布流商品列表
.product-waterfall {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  padding: 0 8px;
}

.product-card {
  background: $bg-color-white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;

  &:active {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .product-image-wrapper {
    position: relative;
  }

  .product-image {
    width: 100%;
    height: 180px;
    background: #fafafa;
  }

  .product-badge {
    position: absolute;
    top: 8px;
    left: 8px;
  }

  .product-info {
    padding: 10px;
  }

  .product-origin-tag {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    background: #FFF5E6;
    color: #FF6B35;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 3px;
    margin-bottom: 6px;
  }

  .product-name {
    font-size: 14px;
    color: #333;
    font-weight: 500;
    line-height: 1.4;
    margin-bottom: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .product-desc {
    font-size: 11px;
    color: #999;
    line-height: 1.4;
    margin-bottom: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .product-footer {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  .product-price {
    color: #FF6B35;
    font-weight: bold;

    .price-symbol {
      font-size: 12px;
    }

    .price-value {
      font-size: 18px;
    }

    .price-unit {
      font-size: 11px;
      color: #999;
      font-weight: normal;
      margin-left: 2px;
    }
  }

  .product-sales {
    font-size: 11px;
    color: #999;
  }
}

// 下拉刷新样式优化
:deep(.van-pull-refresh) {
  min-height: 200px;
}

:deep(.van-list__finished-text) {
  padding: 20px 0;
  color: $text-color-tertiary;
  font-size: $font-size-sm;
}
</style>
