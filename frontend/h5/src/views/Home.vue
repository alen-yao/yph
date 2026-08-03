<template>
  <div class="home-page">
    <!-- 顶部导航栏 -->
    <div class="top-nav-bar">
      <van-icon name="wap-nav" size="20" class="nav-icon" />
      <van-search
        v-model="searchValue"
        shape="round"
        placeholder="新鲜海南芒果"
        background="transparent"
        @click="onSearchClick"
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
    <van-swipe class="banner-swiper" :autoplay="3000" indicator-color="#e93323">
      <van-swipe-item v-for="banner in banners" :key="banner.id">
        <img :src="banner.image" class="banner-img" alt="轮播图" />
      </van-swipe-item>
    </van-swipe>

    <!-- 分类导航 -->
    <div class="category-section">
      <div class="category-grid">
        <div
          v-for="cat in categories.slice(0, 10)"
          :key="cat.id"
          class="category-item"
          @click="onCategoryClick(cat)"
        >
          <div class="category-icon">
            <van-image
              :src="cat.icon || 'https://via.placeholder.com/60'"
              round
              width="48"
              height="48"
              fit="cover"
            />
          </div>
          <div class="category-name">{{ cat.name }}</div>
        </div>
      </div>
    </div>

    <!-- 商品标签页 -->
    <van-tabs
      v-model:active="activeTab"
      sticky
      :offset-top="44"
      color="#e93323"
      title-active-color="#e93323"
      @change="onTabChange"
    >
      <van-tab title="推荐商品">
        <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
          <van-list
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="onLoad"
          >
            <div class="product-list">
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
                    <div class="price">{{ product.price }}</div>
                    <div class="sales text-tertiary text-sm">已售{{ product.sales || 0 }}</div>
                  </div>
                </div>
              </div>
            </div>
          </van-list>
        </van-pull-refresh>
      </van-tab>
      <van-tab title="新品上市">
        <div class="empty-tip">新品上市列表</div>
      </van-tab>
      <van-tab title="热销榜单">
        <div class="empty-tip">热销榜单列表</div>
      </van-tab>
    </van-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()
const searchValue = ref('')
const activeTab = ref(0)
const refreshing = ref(false)
const loading = ref(false)
const finished = ref(false)

const banners = ref([
  { id: 1, image: 'https://via.placeholder.com/375x180/E93323/FFFFFF?text=YPH+Banner+1' },
  { id: 2, image: 'https://via.placeholder.com/375x180/FF6700/FFFFFF?text=YPH+Banner+2' },
  { id: 3, image: 'https://via.placeholder.com/375x180/1890FF/FFFFFF?text=YPH+Banner+3' }
])

const categories = ref([
  { id: 1, name: '数码电器', icon: 'https://via.placeholder.com/60/1890FF/FFFFFF?text=数码' },
  { id: 2, name: '服装服饰', icon: 'https://via.placeholder.com/60/E93323/FFFFFF?text=服装' },
  { id: 3, name: '食品生鲜', icon: 'https://via.placeholder.com/60/13CE66/FFFFFF?text=食品' },
  { id: 4, name: '图书音像', icon: 'https://via.placeholder.com/60/FA8C16/FFFFFF?text=图书' },
  { id: 5, name: '家居家装', icon: 'https://via.placeholder.com/60/722ED1/FFFFFF?text=家居' },
  { id: 6, name: '美妆个护', icon: 'https://via.placeholder.com/60/EB2F96/FFFFFF?text=美妆' },
  { id: 7, name: '运动户外', icon: 'https://via.placeholder.com/60/52C41A/FFFFFF?text=运动' },
  { id: 8, name: '母婴玩具', icon: 'https://via.placeholder.com/60/FAAD14/FFFFFF?text=母婴' },
  { id: 9, name: '汽车用品', icon: 'https://via.placeholder.com/60/2F54EB/FFFFFF?text=汽车' },
  { id: 10, name: '更多分类', icon: 'https://via.placeholder.com/60/8C8C8C/FFFFFF?text=更多' }
])

const productList = ref([])

const onSearchClick = () => {
  router.push('/search')
}

const onCategoryClick = (category) => {
  showToast(`点击分类：${category.name}`)
  // TODO: 跳转到分类页面
}

const onTabChange = (index) => {
  console.log('切换标签页:', index)
  // TODO: 根据标签页加载不同数据
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

  setTimeout(() => {
    for (let i = 0; i < 10; i++) {
      const index = productList.value.length + 1
      productList.value.push({
        id: index,
        name: `YPH 精选商品 ${index} - 高品质正品保障`,
        main_image: `https://via.placeholder.com/200/E8F4F8/E93323?text=Product+${index}`,
        price: (Math.random() * 900 + 100).toFixed(2),
        sales: Math.floor(Math.random() * 10000),
        is_hot: Math.random() > 0.7,
        is_new: Math.random() > 0.8,
        tags: true
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

// 分类区域
.category-section {
  background: $bg-color-white;
  padding: 16px 0 20px;
  margin-bottom: 8px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px 8px;
  padding: 0 $spacing-base;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;

  &:active {
    opacity: 0.7;
  }

  .category-icon {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    overflow: hidden;
    background: #f5f5f5;
    box-shadow: none;
    transition: transform 0.2s;

    &:active {
      transform: scale(0.95);
    }

    :deep(.van-image__img) {
      border-radius: 50%;
    }
  }

  .category-name {
    font-size: 12px;
    color: #666;
    text-align: center;
    line-height: 1.2;
    max-width: 60px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

// 标签页
:deep(.van-tabs) {
  .van-tabs__wrap {
    background: $bg-color-white;
  }

  .van-tab {
    font-weight: 500;
  }
}

// 商品列表
.product-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  padding: 8px;
  background: $bg-color;
}

.product-card {
  background: $bg-color-white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: none;
  border: 1px solid #f0f0f0;
  transition: transform 0.2s, box-shadow 0.2s;

  &:active {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  .product-image {
    width: 100%;
    height: 180px;
    background: #fafafa;
  }

  .product-info {
    padding: 10px;
  }

  .product-name {
    font-size: 13px;
    color: $text-color-primary;
    line-height: 1.4;
    min-height: 36px;
    margin-bottom: 6px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .product-tags {
    display: flex;
    gap: 4px;
    margin-bottom: 6px;
    min-height: 18px;

    .tag {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 3px;
      color: #fff;
      font-weight: 500;

      &.tag-hot {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%);
      }

      &.tag-new {
        background: linear-gradient(135deg, #4CAF50 0%, #43A047 100%);
      }
    }
  }

  .product-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 4px;

    .price {
      color: #ff4757;
      font-size: 16px;
      font-weight: bold;

      &::before {
        content: '¥';
        font-size: 12px;
        margin-right: 1px;
      }
    }

    .sales {
      font-size: 11px;
      line-height: 1.5;
    }
  }
}

// 空状态提示
.empty-tip {
  padding: 60px 20px;
  text-align: center;
  color: $text-color-tertiary;
  font-size: $font-size-base;
}

// 下拉刷新样式优化
:deep(.van-pull-refresh) {
  min-height: calc(100vh - 44px - 180px - 100px);
}

:deep(.van-list__finished-text) {
  padding: 20px 0;
  color: $text-color-tertiary;
  font-size: $font-size-sm;
}
</style>
