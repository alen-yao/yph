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
            <img
              v-if="province.code !== 'more'"
              :src="getRegionIcon(province.code)"
              :alt="province.name"
              class="province-img"
            />
            <van-icon v-else name="apps-o" size="28" />
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
            <img
              :src="zone.icon"
              :alt="zone.title"
              class="zone-icon"
            />
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
                  :src="product.cover_image || product.main_images?.[0]"
                  fit="cover"
                  class="product-image"
                  lazy-load
                >
                  <template #loading>
                    <van-loading type="spinner" size="20" />
                  </template>
                </van-image>
                <div class="product-badge" v-if="product.is_new">
                  <van-tag plain type="danger" size="mini">新品</van-tag>
                </div>
                <div class="product-badge" v-else-if="product.is_hot">
                  <van-tag plain type="danger" size="mini">热销</van-tag>
                </div>
              </div>

              <div class="product-info">
                <div class="product-origin-tag">
                  <van-icon name="location-o" size="10" />
                  {{ product.region?.name || '产地直供' }}
                </div>
                <div class="product-name">{{ product.name }}</div>
                <div class="product-desc" v-if="product.description">{{ product.description }}</div>
                <div class="product-footer">
                  <div class="product-price">
                    <span class="price-symbol">¥</span>
                    <span class="price-value">{{ product.price }}</span>
                  </div>
                  <div class="add-to-cart" @click.stop="goToProduct(product.id)">
                    <van-icon name="shopping-cart-o" size="14" color="#fff" />
                  </div>
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
import { getBannerList, getEnabledRegions, getProductList } from '@/api/product'

const router = useRouter()
const searchValue = ref('')
const refreshing = ref(false)
const loading = ref(false)
const finished = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)

// 轮播图
const banners = ref([])

// 热门省份
const provinces = ref([])

// 特色专区
const featureZones = ref([])

// 全部特产列表
const productList = ref([])

const onSearch = (value) => {
  if (value.trim()) {
    showToast(`搜索: ${value}`)
    // TODO: 执行搜索逻辑
  }
}

const goToCategory = () => {
  // 跳转到分类页面，默认显示第一个省份的第一个二级分类
  router.push('/category')
}

const onProvinceClick = (province) => {
  if (province.code === 'more') {
    // 点击"更多"跳转到分类页面
    router.push('/category')
  } else {
    // 跳转到该省份的商品列表
    router.push({
      path: '/category',
      query: { region: province.code }
    })
  }
}

const goToZone = (zoneId) => {
  // 根据专区ID查找对应的地区
  const zone = featureZones.value.find(z => z.id === zoneId)
  if (zone) {
    // 跳转到该地区的分类页面
    const region = provinces.value.find(p => p.id === zoneId)
    if (region) {
      router.push({
        path: '/category',
        query: { region: region.code }
      })
    }
  }
}

const onRefresh = async () => {
  refreshing.value = true
  productList.value = []
  finished.value = false
  currentPage.value = 1

  await onLoad()
  refreshing.value = false
}

const onLoad = async () => {
  if (refreshing.value) return

  loading.value = true

  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      state: 1 // 只获取上架的商品
    }
    const res = await getProductList(params)
    const newProducts = res.data?.results || []

    // 追加商品到列表
    productList.value = [...productList.value, ...newProducts]

    // 判断是否还有更多数据
    if (!res.data?.next || newProducts.length < pageSize.value) {
      finished.value = true
    } else {
      currentPage.value++
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
    showToast('获取商品列表失败')
    finished.value = true
  } finally {
    loading.value = false
  }
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

// 获取轮播图数据
const fetchBanners = async () => {
  try {
    const res = await getBannerList()
    banners.value = res.data || []
  } catch (error) {
    console.error('获取轮播图失败:', error)
  }
}

// 获取省份图标
const getRegionIcon = (code) => {
  try {
    return new URL(`../assets/regions/${code}.png`, import.meta.url).href
  } catch (e) {
    console.error('Failed to load region icon:', code, e)
    return ''
  }
}

// 获取省份数据
const fetchProvinces = async () => {
  try {
    const res = await getEnabledRegions()
    let regions = res.data || []

    // 添加"更多"按钮
    if (regions.length > 0) {
      provinces.value = [
        ...regions.slice(0, 9),
        { id: 'more', name: '更多', code: 'more' }
      ]
    }

    // 获取前2个省份的特色商品，用于特色专区展示
    await fetchFeatureZones(regions.slice(0, 2))
  } catch (error) {
    console.error('获取省份列表失败:', error)
  }
}

// 获取特色专区数据
const fetchFeatureZones = async (regions) => {
  try {
    const zones = []
    for (const region of regions) {
      // 获取该地区的推荐商品（前3个）
      const res = await getProductList({
        region: region.id,
        is_recommend: true,
        state: 1,
        page_size: 3
      })
      const products = res.data?.results || []

      if (products.length > 0) {
        zones.push({
          id: region.id,
          title: `${region.name}特产`,
          icon: getRegionIcon(region.code),
          products: products.map(p => ({
            id: p.id,
            name: p.name,
            origin: region.name,
            image: p.cover_image || p.main_images?.[0] || '',
            price: p.price,
            sales: p.sales_count
          }))
        })
      }
    }
    featureZones.value = zones
  } catch (error) {
    console.error('获取特色专区数据失败:', error)
  }
}

onMounted(() => {
  fetchBanners()
  fetchProvinces()
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

  .province-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
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
    gap: 8px;

    .zone-icon {
      width: 24px;
      height: 24px;
      object-fit: cover;
      border-radius: 50%;
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
    align-items: center;
    justify-content: space-between;
    margin-top: 8px;
  }

  .product-price {
    color: #FF6B35;
    font-weight: bold;
    flex: 1;

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

  .add-to-cart {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3);
    cursor: pointer;
    transition: transform 0.2s;
    flex-shrink: 0;

    &:active {
      transform: scale(0.9);
    }
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
