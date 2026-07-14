<template>
  <div class="product-list-page">
    <div class="container">
      <div class="page-content">
        <!-- 侧边栏筛选 -->
        <aside class="sidebar">
          <div class="filter-section">
            <h3 class="filter-title">商品分类</h3>
            <ul class="filter-list">
              <li
                v-for="category in categories"
                :key="category.id"
                :class="{ active: selectedCategory === category.id }"
                @click="selectCategory(category.id)"
              >
                {{ category.name }}
              </li>
            </ul>
          </div>

          <div class="filter-section">
            <h3 class="filter-title">价格区间</h3>
            <ul class="filter-list">
              <li
                v-for="range in priceRanges"
                :key="range.id"
                :class="{ active: selectedPriceRange === range.id }"
                @click="selectPriceRange(range.id)"
              >
                {{ range.label }}
              </li>
            </ul>
            <div class="custom-price">
              <el-input v-model="minPrice" placeholder="最低价" size="small" />
              <span>-</span>
              <el-input v-model="maxPrice" placeholder="最高价" size="small" />
              <el-button size="small" type="primary" @click="applyCustomPrice">确定</el-button>
            </div>
          </div>

          <div class="filter-section">
            <h3 class="filter-title">品牌</h3>
            <ul class="filter-list">
              <li
                v-for="brand in brands"
                :key="brand.id"
                :class="{ active: selectedBrand === brand.id }"
                @click="selectBrand(brand.id)"
              >
                {{ brand.name }}
              </li>
            </ul>
          </div>
        </aside>

        <!-- 商品列表主区域 -->
        <main class="main-area">
          <!-- 排序栏 -->
          <div class="sort-bar">
            <div class="result-count">
              共找到 <span class="count">{{ total }}</span> 件商品
            </div>
            <div class="sort-options">
              <span
                v-for="option in sortOptions"
                :key="option.value"
                :class="{ active: sortBy === option.value }"
                @click="changeSortBy(option.value)"
              >
                {{ option.label }}
                <el-icon v-if="option.sortable">
                  <component :is="getSortIcon(option.value)" />
                </el-icon>
              </span>
            </div>
          </div>

          <!-- 商品网格 -->
          <div v-loading="loading" class="product-grid">
            <div
              v-for="product in products"
              :key="product.id"
              class="product-card"
              @click="goToProduct(product.id)"
            >
              <div class="product-image">
                <img :src="product.main_image" :alt="product.name" />
                <div class="product-tags" v-if="product.is_hot || product.is_new">
                  <span v-if="product.is_hot" class="tag tag-hot">热销</span>
                  <span v-if="product.is_new" class="tag tag-new">新品</span>
                </div>
              </div>
              <div class="product-info">
                <div class="product-name ellipsis-2">{{ product.name }}</div>
                <div class="product-desc ellipsis">{{ product.description }}</div>
                <div class="product-footer">
                  <div class="price price-large">{{ product.price }}</div>
                  <div class="sales text-tertiary text-sm">已售 {{ product.sales }}</div>
                </div>
                <div class="product-actions">
                  <el-button size="small" @click.stop="addToCart(product)">加入购物车</el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              :page-sizes="[12, 24, 36, 48]"
              layout="total, sizes, prev, pager, next, jumper"
              @current-change="loadProducts"
              @size-change="loadProducts"
            />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const products = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)

const selectedCategory = ref(null)
const selectedPriceRange = ref(null)
const selectedBrand = ref(null)
const sortBy = ref('default')
const minPrice = ref('')
const maxPrice = ref('')

const categories = ref([
  { id: 'all', name: '全部分类' },
  { id: 1, name: '数码电器' },
  { id: 2, name: '服装服饰' },
  { id: 3, name: '食品生鲜' },
  { id: 4, name: '图书音像' },
  { id: 5, name: '家居家装' }
])

const priceRanges = ref([
  { id: 'all', label: '全部价格' },
  { id: 1, label: '0-100元' },
  { id: 2, label: '100-300元' },
  { id: 3, label: '300-500元' },
  { id: 4, label: '500-1000元' },
  { id: 5, label: '1000元以上' }
])

const brands = ref([
  { id: 'all', name: '全部品牌' },
  { id: 1, name: 'YPH官方' },
  { id: 2, name: '品牌A' },
  { id: 3, name: '品牌B' },
  { id: 4, name: '品牌C' }
])

const sortOptions = ref([
  { value: 'default', label: '默认排序', sortable: false },
  { value: 'sales', label: '销量', sortable: true },
  { value: 'price', label: '价格', sortable: true },
  { value: 'new', label: '上新时间', sortable: true }
])

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId === 'all' ? null : categoryId
  currentPage.value = 1
  loadProducts()
}

const selectPriceRange = (rangeId) => {
  selectedPriceRange.value = rangeId === 'all' ? null : rangeId
  currentPage.value = 1
  loadProducts()
}

const selectBrand = (brandId) => {
  selectedBrand.value = brandId === 'all' ? null : brandId
  currentPage.value = 1
  loadProducts()
}

const changeSortBy = (value) => {
  if (sortBy.value === value) {
    // Toggle sort direction
    sortBy.value = value + '_desc'
  } else if (sortBy.value === value + '_desc') {
    sortBy.value = value
  } else {
    sortBy.value = value
  }
  loadProducts()
}

const getSortIcon = (value) => {
  if (sortBy.value === value + '_desc') {
    return ArrowDown
  } else if (sortBy.value === value) {
    return ArrowUp
  }
  return null
}

const applyCustomPrice = () => {
  if (minPrice.value || maxPrice.value) {
    currentPage.value = 1
    loadProducts()
  }
}

const loadProducts = () => {
  loading.value = true
  // 模拟 API 请求
  setTimeout(() => {
    const mockProducts = []
    for (let i = 1; i <= pageSize.value; i++) {
      const id = (currentPage.value - 1) * pageSize.value + i
      mockProducts.push({
        id,
        name: `YPH 精选商品 ${id} - 高品质正品保障`,
        description: '精选优质材料，匠心工艺制作',
        main_image: `https://via.placeholder.com/280x280/E8F4F8/E93323?text=Product+${id}`,
        price: (Math.random() * 900 + 100).toFixed(2),
        sales: Math.floor(Math.random() * 10000),
        is_hot: Math.random() > 0.7,
        is_new: Math.random() > 0.8
      })
    }
    products.value = mockProducts
    total.value = 120
    loading.value = false
  }, 500)
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

const addToCart = (product) => {
  ElMessage.success(`已将 ${product.name} 加入购物车`)
}

onMounted(() => {
  // 从路由参数获取筛选条件
  if (route.query.category) {
    selectedCategory.value = parseInt(route.query.category)
  }
  if (route.query.keyword) {
    // TODO: 处理搜索关键词
  }
  loadProducts()
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.product-list-page {
  padding: 20px 0 60px;
}

.page-content {
  display: flex;
  gap: 20px;
}

// 侧边栏
.sidebar {
  width: 220px;
  flex-shrink: 0;
}

.filter-section {
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  padding: 20px;
  margin-bottom: 20px;

  .filter-title {
    font-size: $font-size-base;
    font-weight: 600;
    color: $text-color-primary;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid $border-color-light;
  }

  .filter-list {
    li {
      padding: 8px 12px;
      font-size: $font-size-sm;
      color: $text-color-secondary;
      cursor: pointer;
      border-radius: $border-radius-base;
      transition: all 0.3s;

      &:hover {
        background: $bg-color-light;
        color: $theme-color;
      }

      &.active {
        background: $theme-color-light;
        color: $theme-color;
        font-weight: 500;
      }
    }
  }

  .custom-price {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 12px;

    .el-input {
      flex: 1;
    }

    span {
      color: $text-color-tertiary;
    }
  }
}

// 主区域
.main-area {
  flex: 1;
}

.sort-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: $bg-color-white;
  padding: 16px 20px;
  border-radius: $border-radius-lg;
  margin-bottom: 20px;

  .result-count {
    font-size: $font-size-sm;
    color: $text-color-secondary;

    .count {
      color: $theme-color;
      font-weight: 600;
      margin: 0 4px;
    }
  }

  .sort-options {
    display: flex;
    gap: 24px;

    span {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: $font-size-sm;
      color: $text-color-secondary;
      cursor: pointer;
      transition: color 0.3s;

      &:hover,
      &.active {
        color: $theme-color;
      }

      &.active {
        font-weight: 500;
      }
    }
  }
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  min-height: 400px;
}

.product-card {
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid transparent;

  &:hover {
    transform: translateY(-4px);
    box-shadow: $box-shadow-lg;
    border-color: $theme-color;

    .product-image img {
      transform: scale(1.05);
    }

    .product-actions {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .product-image {
    position: relative;
    width: 100%;
    padding-top: 100%;
    overflow: hidden;
    background: $bg-color-grey;

    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s;
    }

    .product-tags {
      position: absolute;
      top: 12px;
      left: 0;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
  }

  .product-info {
    padding: 16px;

    .product-name {
      font-size: $font-size-base;
      color: $text-color-primary;
      line-height: 1.5;
      min-height: 42px;
      margin-bottom: 8px;
    }

    .product-desc {
      font-size: $font-size-sm;
      color: $text-color-tertiary;
      margin-bottom: 12px;
    }

    .product-footer {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      margin-bottom: 12px;
    }

    .product-actions {
      opacity: 0;
      transform: translateY(10px);
      transition: all 0.3s;

      .el-button {
        width: 100%;
      }
    }
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}
</style>
