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
              :src="product.cover_image"
              fit="cover"
              class="product-img"
              lazy-load
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
        <van-empty v-else-if="!loading" description="暂无商品" />
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
    categories.value = res.data?.results || res.data || []
    initFromUrl()
  } catch (error) {
    console.error('获取分类失败:', error)
    showToast('获取分类失败')
  }
}

// 获取商品列表
const fetchProducts = async () => {
  if (!currentRegion.value || !currentCategory.value) {
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
    const res = await getProductList(params)
    products.value = res.data?.results || res.data || []
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

// 监听地区和分类变化
watch([currentRegion, currentCategory], () => {
  fetchProducts()
})

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped lang="scss">
.category-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

// 顶部搜索栏
.search-bar {
  position: sticky;
  top: 0;
  z-index: 999;
  background: #fff;
  padding: 8px 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

  :deep(.van-search) {
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
}

// 主体内容区域
.category-main {
  flex: 1;
  display: flex;
  overflow: hidden;
  padding-bottom: 54px; // 底部TabBar高度
}

// 左侧分类
.category-sidebar {
  width: 90px;
  background: #f5f5f5;
  overflow-y: auto;
  flex-shrink: 0;

  .category-item {
    position: relative;
    padding: 20px 8px;
    text-align: center;
    cursor: pointer;
    background: #f5f5f5;
    transition: all 0.2s;

    &:active {
      background: #e8e8e8;
    }

    .category-text {
      font-size: 13px;
      color: #666;
      line-height: 1.4;
      word-break: break-all;
    }

    &.active {
      background: #fff;

      .category-text {
        color: #1a1a1a;
        font-weight: 600;
      }

      .category-indicator {
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 3px;
        height: 20px;
        background: #1a1a1a;
        border-radius: 0 2px 2px 0;
      }
    }
  }
}

// 右侧商品区域
.product-area {
  flex: 1;
  overflow-y: auto;
  background: #fff;
  position: relative;

  .product-list {
    padding: 0;
  }

  .product-item {
    display: flex;
    gap: 12px;
    padding: 12px;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
    transition: background 0.2s;

    &:active {
      background: #fafafa;
    }

    .product-img {
      width: 100px;
      height: 100px;
      border-radius: 8px;
      overflow: hidden;
      background: #fafafa;
      flex-shrink: 0;

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
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-width: 0;
    }

    .product-title {
      font-size: 14px;
      font-weight: 500;
      color: #333;
      line-height: 1.4;
      margin-bottom: 4px;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .product-desc {
      font-size: 12px;
      color: #999;
      margin-bottom: 4px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .product-tags {
      display: flex;
      gap: 4px;
      margin-bottom: 8px;
    }

    .product-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .product-price {
      display: flex;
      align-items: baseline;
      gap: 4px;

      .price-symbol {
        color: #ff6b35;
        font-size: 12px;
        font-weight: bold;
      }

      .price-value {
        color: #ff6b35;
        font-size: 18px;
        font-weight: bold;
      }

      .market-price {
        color: #999;
        font-size: 11px;
        text-decoration: line-through;
      }
    }

    .product-sales {
      font-size: 11px;
      color: #999;
    }
  }

  .van-loading {
    padding: 40px 0;
  }
}
</style>
