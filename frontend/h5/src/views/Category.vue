<template>
  <div class="category-page">
    <!-- 顶部搜索栏 -->
    <div class="search-bar">
      <van-search
        v-model="searchValue"
        shape="round"
        placeholder="搜索特产"
        background="transparent"
        @search="onSearch"
      >
        <template #left-icon>
          <van-icon name="search" size="16" color="#999" />
        </template>
      </van-search>
    </div>

    <!-- 地区选择器（横向） -->
    <RegionSelector
      v-model="currentRegion"
      @change="onRegionChange"
    />

    <!-- 主体内容区域：左侧分类 + 右侧商品列表 -->
    <div class="category-main">
      <!-- 左侧一级分类 -->
      <div class="category-sidebar">
        <div
          v-for="(category, index) in categories"
          :key="category.id"
          :class="['category-item', { active: activeCategoryIndex === index }]"
          @click="onCategoryChange(index)"
        >
          <div class="category-text">{{ category.name }}</div>
          <div v-if="activeCategoryIndex === index" class="category-indicator"></div>
        </div>
        <van-empty v-if="categories.length === 0" description="暂无分类" />
      </div>

      <!-- 右侧商品列表 -->
      <div class="product-area">
        <div v-if="products.length > 0" class="product-list">
          <div
            v-for="product in products"
            :key="product.id"
            class="product-item"
            @click="goToProduct(product.id)"
          >
            <van-image
              :src="getImageUrl(product.cover_image)"
              fit="cover"
              class="product-img"
            >
              <template #loading>
                <van-loading type="spinner" size="16" />
              </template>
              <template #error>
                <div class="img-error">
                  <van-icon name="photo-fail" size="24" />
                </div>
              </template>
            </van-image>
            <div class="product-content">
              <div class="product-title">{{ product.name }}</div>
              <div class="product-desc" v-if="product.description">
                {{ product.description }}
              </div>
              <div class="product-tags">
                <van-tag v-if="product.is_new" type="success" size="mini">新品</van-tag>
                <van-tag v-if="product.is_hot" type="danger" size="mini">热销</van-tag>
                <van-tag v-if="product.is_recommend" type="warning" size="mini">推荐</van-tag>
              </div>
              <div class="product-footer">
                <div class="product-price">
                  <span class="price-symbol">¥</span>
                  <span class="price-value">{{ product.price }}</span>
                  <span class="market-price" v-if="product.market_price > product.price">
                    ¥{{ product.market_price }}
                  </span>
                </div>
                <div class="product-sales">已售{{ product.sales_count }}</div>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="!loading && !currentRegion" class="empty-hint">
          <van-icon name="location-o" size="48" color="#ddd" />
          <p>请选择地区查看商品</p>
        </div>
        <div v-else-if="!loading && !currentCategory" class="empty-hint">
          <van-icon name="apps-o" size="48" color="#ddd" />
          <p>请选择分类查看商品</p>
        </div>
        <van-empty v-else-if="!loading" description="暂无商品" image="search" />
        <van-loading v-if="loading" type="spinner" vertical>
          加载中...
        </van-loading>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast } from 'vant'
import { getCategoryList, getProductList } from '@/api/product'
import RegionSelector from '@/components/RegionSelector.vue'

const router = useRouter()
const route = useRoute()
const searchValue = ref('')
const currentRegion = ref(null)
const categories = ref([])
const activeCategoryIndex = ref(0)
const products = ref([])
const loading = ref(false)

// 处理图片URL（与admin端保持一致）
const getImageUrl = (url) => {
  if (!url) return ''
  // 如果已经是完整URL，直接返回
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  // 否则拼接 MinIO 公开访问地址
  return `http://localhost:9000/yph-products/${url}`
}

// 当前选中的分类
const currentCategory = computed(() => {
  return categories.value[activeCategoryIndex.value] || null
})

// 从URL读取初始参数
const initFromUrl = () => {
  const { region, category } = route.query
  if (region) {
    // region参数将由RegionSelector组件处理
  }
  if (category) {
    const index = categories.value.findIndex(c => c.id === parseInt(category))
    if (index !== -1) {
      activeCategoryIndex.value = index
    }
  }
}

// 同步到URL
const syncToUrl = () => {
  const query = {}
  if (currentRegion.value) {
    query.region = currentRegion.value.code
  }
  if (currentCategory.value) {
    query.category = currentCategory.value.id
  }
  router.replace({ path: '/category', query })
}

// 获取分类列表
const fetchCategories = async () => {
  try {
    const res = await getCategoryList({ is_show: true })
    // 响应拦截器已经返回了 response.data，所以直接使用
    categories.value = res?.results || res || []
    console.log('分类数据:', categories.value)
    initFromUrl()
    // 如果地区已经选中，则加载商品
    if (currentRegion.value && currentCategory.value) {
      fetchProducts()
    }
  } catch (error) {
    console.error('获取分类失败:', error)
    showToast('获取分类失败')
  }
}

// 获取商品列表
const fetchProducts = async () => {
  console.log('fetchProducts 调用', {
    currentRegion: currentRegion.value,
    currentCategory: currentCategory.value
  })

  if (!currentRegion.value || !currentCategory.value) {
    console.log('地区或分类为空，跳过加载商品')
    products.value = []
    return
  }

  loading.value = true
  try {
    const params = {
      region: currentRegion.value.id,
      category: currentCategory.value.id,
      state: 1
    }
    console.log('加载商品参数:', params)
    const res = await getProductList(params)
    // 响应拦截器已经返回了 response.data，所以直接使用
    products.value = res?.results || res || []
    console.log('商品数据:', products.value)
  } catch (error) {
    console.error('获取商品失败:', error)
    showToast('获取商品失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const onSearch = (value) => {
  if (value.trim()) {
    router.push({
      path: '/search',
      query: {
        keyword: value,
        region: currentRegion.value?.code
      }
    })
  }
}

// 地区变化
const onRegionChange = (region) => {
  console.log('地区变化:', region)
  currentRegion.value = region
  syncToUrl()
  fetchProducts()
}

// 分类变化
const onCategoryChange = (index) => {
  activeCategoryIndex.value = index
  syncToUrl()
  fetchProducts()
}

// 跳转到商品详情
const goToProduct = (productId) => {
  router.push(`/product/${productId}`)
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped lang="scss">
.category-page {
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  background: #f7f7f7;
  overflow: hidden;
}

// 顶部搜索栏（增大高度和字体）
.search-bar {
  flex-shrink: 0;
  background: #fff;
  padding: 8px 12px;
  border-bottom: 1px solid #f2f2f2;

  :deep(.van-search) {
    padding: 0;

    .van-search__content {
      height: 38px;
      padding: 0 12px;
      background: #f6f6f6;
      border-radius: 19px;
    }

    .van-field__left-icon {
      margin-right: 4px;
    }

    .van-field__control {
      font-size: 14px;
      color: #333;

      &::placeholder {
        color: #aaa;
      }
    }
  }
}

// 主体内容区域
.category-main {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
}

// 左侧分类（优化视觉效果）
.category-sidebar {
  width: 88px;
  flex: 0 0 88px;
  background: #f8f8f8;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }

  .category-item {
    position: relative;
    min-height: 48px;
    padding: 14px 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: #f8f8f8;
    color: #666;
    transition: background 0.2s, color 0.2s;

    .category-text {
      max-width: 100%;
      font-size: 13px;
      line-height: 1.35;
      font-weight: 400;
      word-break: break-all;
    }
    
    &:active {
      background: #f0f0f0;
    }

    &.active {
      background: #fff;
      color: #222;
      font-weight: 600;

      .category-text {
        color: #222;
        font-weight: 600;
      }

      .category-indicator {
        position: absolute;
        left: 0;
        top: 50%;
        width: 3px;
        height: 24px;
        transform: translateY(-50%);
        background: #e93323;
        border-radius: 0 3px 3px 0;
      }
    }
  }
}

// 右侧商品区域
.product-area {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  background: #fff;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }

  .product-list {
    padding: 0;
    width: 100%;
  }

  .product-item {
    display: flex;
    gap: 10px;
    padding: 10px 10px 10px 8px;
    min-height: 94px;
    border-bottom: 1px solid #f2f2f2;
    background: #fff;
    cursor: pointer;

    &:active {
      background: #fafafa;
    }

    .product-img {
      width: 76px;
      height: 76px;
      flex: 0 0 76px;
      border-radius: 4px;
      overflow: hidden;
      background: #f7f7f7;

      .img-error {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f5f5f5;
        color: #ccc;
      }
    }

    .product-content {
      min-width: 0;
      flex: 1;
      min-height: 76px;
      display: flex;
      flex-direction: column;
    }

    .product-title {
      margin: 0;
      color: #333;
      font-size: 13px;
      font-weight: 500;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .product-desc {
      margin-top: 3px;
      color: #999;
      font-size: 11px;
      line-height: 1.3;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .product-tags {
      display: flex;
      align-items: center;
      gap: 4px;
      min-height: 16px;
      margin-top: 4px;

      :deep(.van-tag) {
        padding: 1px 4px;
        font-size: 9px;
        line-height: 1.3;
        border-radius: 2px;
      }
    }

    .product-footer {
      margin-top: auto;
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 6px;
    }

    .product-price {
      display: flex;
      align-items: baseline;
      gap: 1px;
      min-width: 0;

      .price-symbol {
        color: #e93323;
        font-size: 11px;
        font-weight: 600;
      }

      .price-value {
        color: #e93323;
        font-size: 18px;
        line-height: 1;
        font-weight: 700;
      }

      .market-price {
        margin-left: 3px;
        color: #aaa;
        font-size: 10px;
        text-decoration: line-through;
      }
    }

    .product-sales {
      flex-shrink: 0;
      color: #aaa;
      font-size: 10px;
      line-height: 1.2;
    }
  }

  .van-loading {
    padding: 40px 0;
  }

  .empty-hint {
    min-height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    color: #999;

    p {
      margin-top: 12px;
      font-size: 13px;
    }
  }
}
</style>
