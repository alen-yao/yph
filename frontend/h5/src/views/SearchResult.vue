<template>
  <div class="search-result-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      fixed
      placeholder
      left-arrow
      @click-left="onBack"
    >
      <template #title>
        <van-search
          v-model="searchValue"
          shape="round"
          placeholder="请输入搜索关键词"
          show-action
          autofocus
          @search="onSearch"
        >
          <template #action>
            <div @click="onSearch" class="search-action">搜索</div>
          </template>
        </van-search>
      </template>
      <template #right>
        <van-icon name="wap-home-o" size="20" @click="goHome" />
      </template>
    </van-nav-bar>

    <!-- 搜索结果列表 -->
    <div class="search-content">
      <!-- 搜索历史 -->
      <div v-if="!hasSearched && searchHistory.length > 0" class="search-history">
        <div class="history-header">
          <span class="title">搜索历史</span>
          <van-icon name="delete-o" size="16" @click="clearHistory" />
        </div>
        <div class="history-tags">
          <van-tag
            v-for="(item, index) in searchHistory"
            :key="index"
            round
            size="medium"
            @click="onHistoryClick(item)"
          >
            {{ item }}
          </van-tag>
        </div>
      </div>

      <!-- 热门搜索 -->
      <div v-if="!hasSearched" class="hot-search">
        <div class="section-title">热门搜索</div>
        <div class="hot-tags">
          <van-tag
            v-for="(item, index) in hotSearchList"
            :key="index"
            round
            type="danger"
            size="medium"
            @click="onHotClick(item)"
          >
            {{ item }}
          </van-tag>
        </div>
      </div>

      <!-- 搜索结果 -->
      <div v-if="hasSearched">
        <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="onLoad"
          >
            <!-- 结果统计 -->
            <div class="result-info" v-if="productList.length > 0">
              找到 <span class="count">{{ totalCount }}</span> 个相关商品
            </div>

            <!-- 商品列表 -->
            <div class="product-list" v-if="productList.length > 0">
              <div
                v-for="product in productList"
                :key="product.id"
                class="product-card"
                @click="goToProduct(product.id)"
              >
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
                <div class="product-info">
                  <div class="product-name ellipsis-2">{{ product.name }}</div>
                  <div class="product-tags" v-if="product.tags">
                    <span class="tag tag-hot" v-if="product.is_hot">热销</span>
                    <span class="tag tag-new" v-if="product.is_new">新品</span>
                  </div>
                  <div class="product-footer">
                    <div class="price">¥{{ product.price }}</div>
                    <div class="add-to-cart" @click.stop="goToProduct(product.id)">
                      <van-icon name="shopping-cart-o" size="16" color="#fff" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 空状态 -->
            <van-empty
              v-if="hasSearched && !loading && productList.length === 0"
              image="search"
              description="没有找到相关商品"
            />
          </van-list>
        </van-pull-refresh>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()
const searchValue = ref('')
const hasSearched = ref(false)
const refreshing = ref(false)
const loading = ref(false)
const finished = ref(false)
const totalCount = ref(0)

const searchHistory = ref(['手机', '笔记本', '数码相机'])
const hotSearchList = ref([
  'iPhone 15',
  '华为手机',
  '笔记本电脑',
  '机械键盘',
  '蓝牙耳机',
  '智能手表',
  '相机',
  '平板电脑'
])

const productList = ref([])

const onBack = () => {
  router.back()
}

const goHome = () => {
  router.push('/home')
}

const onSearch = () => {
  if (!searchValue.value.trim()) {
    showToast('请输入搜索关键词')
    return
  }

  hasSearched.value = true
  productList.value = []
  finished.value = false

  // 添加到搜索历史
  if (!searchHistory.value.includes(searchValue.value)) {
    searchHistory.value.unshift(searchValue.value)
    if (searchHistory.value.length > 10) {
      searchHistory.value.pop()
    }
  }

  // 触发加载
  onLoad()
}

const onHistoryClick = (keyword) => {
  searchValue.value = keyword
  onSearch()
}

const onHotClick = (keyword) => {
  searchValue.value = keyword
  onSearch()
}

const clearHistory = () => {
  searchHistory.value = []
  showToast('已清空搜索历史')
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
  if (refreshing.value || !hasSearched.value) return

  loading.value = true

  // 模拟API请求
  setTimeout(() => {
    for (let i = 0; i < 10; i++) {
      const index = productList.value.length + 1
      productList.value.push({
        id: index,
        name: `${searchValue.value} - 相关商品 ${index}`,
        main_image: `https://via.placeholder.com/200/E8F4F8/E93323?text=Product+${index}`,
        price: (Math.random() * 900 + 100).toFixed(2),
        sales: Math.floor(Math.random() * 10000),
        is_hot: Math.random() > 0.7,
        is_new: Math.random() > 0.8,
        tags: true
      })
    }

    totalCount.value = productList.value.length + Math.floor(Math.random() * 50)
    loading.value = false

    if (productList.value.length >= 30) {
      finished.value = true
    }
  }, 800)
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.search-result-page {
  min-height: 100vh;
  background: $bg-color;
}

// 导航栏样式
:deep(.van-nav-bar) {
  background: linear-gradient(135deg, $theme-color 0%, $theme-color-hover 100%);

  .van-nav-bar__arrow,
  .van-icon {
    color: $text-color-white;
    cursor: pointer;
  }

  .van-nav-bar__title {
    max-width: 70%;
  }

  .van-search {
    padding: 0;

    .van-search__content {
      background: rgba(255, 255, 255, 0.95);
      border-radius: $border-radius-round;
      padding-left: 12px;
    }

    .van-field__body {
      input {
        font-size: $font-size-sm;
      }
    }
  }

  .search-action {
    color: $theme-color;
    font-size: $font-size-base;
    font-weight: 500;
    cursor: pointer;
    padding: 0 8px;
  }
}

// 搜索内容区域
.search-content {
  padding: $spacing-base;
}

// 搜索历史
.search-history {
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-base;

  .history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-base;

    .title {
      font-size: $font-size-base;
      font-weight: 600;
      color: $text-color-primary;
    }

    .van-icon {
      color: $text-color-tertiary;
      cursor: pointer;
    }
  }

  .history-tags {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-sm;

    :deep(.van-tag) {
      background: $bg-color-grey;
      color: $text-color-secondary;
      border: none;
      cursor: pointer;
      padding: 6px 12px;

      &:active {
        background: $bg-color;
      }
    }
  }
}

// 热门搜索
.hot-search {
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  padding: $spacing-lg;
  margin-bottom: $spacing-base;

  .section-title {
    font-size: $font-size-base;
    font-weight: 600;
    color: $text-color-primary;
    margin-bottom: $spacing-base;
  }

  .hot-tags {
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-sm;

    :deep(.van-tag) {
      cursor: pointer;
      padding: 6px 12px;

      &:active {
        opacity: 0.8;
      }
    }
  }
}

// 结果统计
.result-info {
  padding: $spacing-base 0;
  font-size: $font-size-sm;
  color: $text-color-secondary;

  .count {
    color: $theme-color;
    font-weight: 600;
  }
}

// 商品列表
.product-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-base;
}

.product-card {
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  overflow: hidden;
  box-shadow: $box-shadow-sm;
  transition: transform 0.2s, box-shadow 0.2s;

  &:active {
    transform: translateY(-2px);
    box-shadow: $box-shadow-base;
  }

  .product-image {
    width: 100%;
    height: 180px;
    background: $bg-color-grey;
  }

  .product-info {
    padding: $spacing-base;
  }

  .product-name {
    font-size: $font-size-base;
    color: $text-color-primary;
    line-height: 1.4;
    min-height: 40px;
    margin-bottom: $spacing-sm;
  }

  .product-tags {
    display: flex;
    gap: $spacing-xs;
    margin-bottom: $spacing-sm;
  }

  .product-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: $spacing-sm;

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

      &:active {
        transform: scale(0.9);
      }
    }
  }
}

// 下拉刷新优化
:deep(.van-pull-refresh) {
  min-height: calc(100vh - 100px);
}

:deep(.van-list__finished-text) {
  padding: 20px 0;
  color: $text-color-tertiary;
  font-size: $font-size-sm;
}
</style>
