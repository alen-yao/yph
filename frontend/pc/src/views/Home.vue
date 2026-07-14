<template>
  <div class="home-page">
    <!-- 轮播图 -->
    <section class="banner-section">
      <div class="container">
        <el-carousel height="400px" indicator-position="none">
          <el-carousel-item v-for="banner in banners" :key="banner.id">
            <img :src="banner.image" :alt="banner.title" class="banner-img" />
          </el-carousel-item>
        </el-carousel>
      </div>
    </section>

    <!-- 分类快捷入口 -->
    <section class="category-section">
      <div class="container">
        <div class="category-grid">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-item"
            @click="goToCategory(category)"
          >
            <div class="category-icon">
              <img :src="category.icon" :alt="category.name" />
            </div>
            <div class="category-name">{{ category.name }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 热门商品 -->
    <section class="products-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">热门推荐</h2>
          <router-link to="/products" class="more-link">
            查看更多
            <el-icon><ArrowRight /></el-icon>
          </router-link>
        </div>
        <div class="product-grid">
          <div
            v-for="product in hotProducts"
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
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 新品上市 -->
    <section class="products-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">新品上市</h2>
          <router-link to="/products?filter=new" class="more-link">
            查看更多
            <el-icon><ArrowRight /></el-icon>
          </router-link>
        </div>
        <div class="product-grid">
          <div
            v-for="product in newProducts"
            :key="product.id"
            class="product-card"
            @click="goToProduct(product.id)"
          >
            <div class="product-image">
              <img :src="product.main_image" :alt="product.name" />
              <div class="product-tags">
                <span class="tag tag-new">新品</span>
              </div>
            </div>
            <div class="product-info">
              <div class="product-name ellipsis-2">{{ product.name }}</div>
              <div class="product-desc ellipsis">{{ product.description }}</div>
              <div class="product-footer">
                <div class="price price-large">{{ product.price }}</div>
                <div class="sales text-tertiary text-sm">已售 {{ product.sales }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 品牌推荐 -->
    <section class="brands-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">品牌推荐</h2>
        </div>
        <div class="brands-grid">
          <div v-for="brand in brands" :key="brand.id" class="brand-item">
            <img :src="brand.logo" :alt="brand.name" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const banners = ref([
  { id: 1, image: 'https://via.placeholder.com/1200x400/E93323/FFFFFF?text=YPH+Banner+1', title: 'Banner 1' },
  { id: 2, image: 'https://via.placeholder.com/1200x400/1890FF/FFFFFF?text=YPH+Banner+2', title: 'Banner 2' },
  { id: 3, image: 'https://via.placeholder.com/1200x400/FA8C16/FFFFFF?text=YPH+Banner+3', title: 'Banner 3' }
])

const categories = ref([
  { id: 1, name: '数码电器', icon: 'https://via.placeholder.com/80/1890FF/FFFFFF?text=数码' },
  { id: 2, name: '服装服饰', icon: 'https://via.placeholder.com/80/E93323/FFFFFF?text=服装' },
  { id: 3, name: '食品生鲜', icon: 'https://via.placeholder.com/80/13CE66/FFFFFF?text=食品' },
  { id: 4, name: '图书音像', icon: 'https://via.placeholder.com/80/FA8C16/FFFFFF?text=图书' },
  { id: 5, name: '家居家装', icon: 'https://via.placeholder.com/80/722ED1/FFFFFF?text=家居' },
  { id: 6, name: '美妆个护', icon: 'https://via.placeholder.com/80/EB2F96/FFFFFF?text=美妆' },
  { id: 7, name: '运动户外', icon: 'https://via.placeholder.com/80/52C41A/FFFFFF?text=运动' },
  { id: 8, name: '母婴玩具', icon: 'https://via.placeholder.com/80/FAAD14/FFFFFF?text=母婴' }
])

const hotProducts = ref([])
const newProducts = ref([])

const brands = ref([
  { id: 1, name: '品牌1', logo: 'https://via.placeholder.com/150x60/F5F5F5/999?text=Brand+1' },
  { id: 2, name: '品牌2', logo: 'https://via.placeholder.com/150x60/F5F5F5/999?text=Brand+2' },
  { id: 3, name: '品牌3', logo: 'https://via.placeholder.com/150x60/F5F5F5/999?text=Brand+3' },
  { id: 4, name: '品牌4', logo: 'https://via.placeholder.com/150x60/F5F5F5/999?text=Brand+4' },
  { id: 5, name: '品牌5', logo: 'https://via.placeholder.com/150x60/F5F5F5/999?text=Brand+5' },
  { id: 6, name: '品牌6', logo: 'https://via.placeholder.com/150x60/F5F5F5/999?text=Brand+6' }
])

const goToCategory = (category) => {
  router.push({
    path: '/products',
    query: { category: category.id }
  })
}

const goToProduct = (id) => {
  router.push(`/product/${id}`)
}

// 生成示例商品数据
const generateProducts = (count, isNew = false) => {
  const products = []
  for (let i = 1; i <= count; i++) {
    products.push({
      id: i,
      name: `YPH 精选优质商品 ${i} - 高品质正品保障`,
      description: '精选优质材料，匠心工艺制作',
      main_image: `https://via.placeholder.com/280x280/E8F4F8/${isNew ? '1890FF' : 'E93323'}?text=Product+${i}`,
      price: (Math.random() * 900 + 100).toFixed(2),
      sales: Math.floor(Math.random() * 10000),
      is_hot: !isNew && Math.random() > 0.5,
      is_new: isNew
    })
  }
  return products
}

onMounted(() => {
  hotProducts.value = generateProducts(8, false)
  newProducts.value = generateProducts(8, true)
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.home-page {
  .container {
    width: $container-width;
    margin: 0 auto;
    padding: 0 15px;
  }
}

// 轮播图
.banner-section {
  padding: 20px 0;

  .banner-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: $border-radius-lg;
  }

  :deep(.el-carousel__container) {
    border-radius: $border-radius-lg;
    overflow: hidden;
  }
}

// 分类区域
.category-section {
  padding: 30px 0;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 20px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: $box-shadow-base;

    .category-icon {
      transform: scale(1.1);
    }
  }

  .category-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    transition: transform 0.3s;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .category-name {
    font-size: $font-size-base;
    color: $text-color-primary;
    font-weight: 500;
  }
}

// 商品区域
.products-section {
  padding: 30px 0;

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 2px solid $theme-color;

    .section-title {
      font-size: $font-size-xxl;
      font-weight: 600;
      color: $text-color-primary;
      position: relative;
      padding-left: 12px;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 20px;
        background: $theme-color;
        border-radius: 2px;
      }
    }

    .more-link {
      display: flex;
      align-items: center;
      gap: 4px;
      color: $text-color-secondary;
      font-size: $font-size-sm;
      transition: color 0.3s;

      &:hover {
        color: $theme-color;
      }
    }
  }
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
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
    }
  }
}

// 品牌区域
.brands-section {
  padding: 30px 0;
  margin-bottom: 40px;

  .section-header {
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 2px solid $theme-color;

    .section-title {
      font-size: $font-size-xxl;
      font-weight: 600;
      color: $text-color-primary;
      position: relative;
      padding-left: 12px;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 20px;
        background: $theme-color;
        border-radius: 2px;
      }
    }
  }
}

.brands-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
}

.brand-item {
  background: $bg-color-white;
  border: 1px solid $border-color;
  border-radius: $border-radius-base;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    border-color: $theme-color;
    box-shadow: $box-shadow-sm;
  }

  img {
    max-width: 100%;
    height: auto;
    opacity: 0.8;
    transition: opacity 0.3s;
  }

  &:hover img {
    opacity: 1;
  }
}
</style>
