<template>
  <div class="category-page">
    <!-- 顶部搜索栏 -->
    <div class="search-bar">
      <van-search
        v-model="searchValue"
        shape="round"
        placeholder="新鲜海南芒果"
        background="transparent"
        @search="onSearch"
      >
        <template #left-icon>
          <van-icon name="search" size="16" color="#999" />
        </template>
      </van-search>
      <div class="search-icons">
        <van-icon name="ellipsis" size="20" />
        <van-icon name="scan" size="20" />
      </div>
    </div>

    <!-- 横向省份导航（顶部滑动） -->
    <div class="province-tabs-wrapper">
      <div class="province-tabs">
        <div
          v-for="(province, index) in displayProvinces"
          :key="province.id"
          :class="['province-tab-item', { active: activeProvinceIndex === index }]"
          @click="onProvinceChange(index)"
        >
          <div class="province-icon">
            <span class="province-emoji">{{ province.emoji }}</span>
          </div>
          <div class="province-name">{{ province.name }}</div>
        </div>
      </div>
      <div class="more-province-btn" v-if="allProvinces.length > displayProvinces.length" @click="showAllProvinces">
        <div class="more-icon">
          <van-icon name="arrow-down" size="14" />
        </div>
        <div class="more-text">全部</div>
      </div>
    </div>

    <!-- 主体内容区域：左侧二级分类 + 右侧商品列表 -->
    <div class="category-main">
      <!-- 左侧二级分类 -->
      <div class="subcategory-sidebar">
        <div
          v-for="(sub, index) in currentSubcategories"
          :key="sub.id"
          :class="['subcategory-item', { active: activeSubIndex === index }]"
          @click="onSubCategoryChange(index)"
        >
          <div class="subcategory-text">{{ sub.name }}</div>
          <div v-if="activeSubIndex === index" class="subcategory-indicator"></div>
        </div>
        <!-- 如果没有二级分类，显示期待 -->
        <div v-if="currentSubcategories.length === 0" class="subcategory-placeholder">
          敬请期待
        </div>
      </div>

      <!-- 右侧商品列表 -->
      <div class="product-area">
        <div v-if="currentProducts.length > 0" class="product-grid">
          <div
            v-for="product in currentProducts"
            :key="product.id"
            class="product-card"
            @click="goToProduct(product.id)"
          >
            <van-image
              :src="product.image"
              fit="cover"
              class="product-image"
              lazy-load
            >
              <template #loading>
                <van-loading type="spinner" size="16" />
              </template>
            </van-image>
            <div class="product-info">
              <div class="product-name">{{ product.name }}</div>
              <div class="product-price">¥{{ product.price }}</div>
            </div>
            <div class="add-cart-btn">
              <van-icon name="plus" size="14" color="#fff" />
            </div>
          </div>
        </div>
        <van-empty v-else description="暂无商品" />
      </div>
    </div>

    <!-- 全部省份弹出层 -->
    <van-popup
      v-model:show="showProvincePopup"
      position="bottom"
      :style="{ height: '50%' }"
      round
    >
      <div class="province-popup">
        <div class="popup-header">
          <span class="popup-title">选择产地</span>
          <van-icon name="cross" size="20" @click="showProvincePopup = false" />
        </div>
        <div class="province-grid">
          <div
            v-for="(province, index) in allProvinces"
            :key="province.id"
            :class="['province-grid-item', { active: activeProvinceIndex === index }]"
            @click="selectProvince(index)"
          >
            <div class="province-grid-emoji">{{ province.emoji }}</div>
            <div class="province-grid-name">{{ province.name }}</div>
          </div>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { getCategoryList } from '@/api/product'

const router = useRouter()
const searchValue = ref('')
const activeProvinceIndex = ref(0)
const allCategories = ref([])
const showProvincePopup = ref(false)

// 所有省份（一级分类）- 模拟数据，实际应该从API获取
const allProvinces = ref([
  { id: 1, name: '云南', emoji: '🌄' },
  { id: 2, name: '新疆', emoji: '🏔️' },
  { id: 3, name: '山东', emoji: '🌊' },
  { id: 4, name: '四川', emoji: '🌶️' },
  { id: 5, name: '浙江', emoji: '🍃' },
  { id: 6, name: '江苏', emoji: '🏮' }
])

// 显示的省份（最多4个，不足补充"期待别的地区"）
const displayProvinces = computed(() => {
  const provinces = [...allProvinces.value.slice(0, 4)]

  // 如果不足4个，补充"期待别的地区"
  while (provinces.length < 4) {
    provinces.push({
      id: `placeholder-${provinces.length}`,
      name: '期待别的地区',
      emoji: '🌟',
      isPlaceholder: true
    })
  }

  return provinces
})

// 模拟二级分类数据（带商品） - 实际应该从API获取
const mockSubcategories = {
  1: [ // 云南
    {
      id: 101,
      name: '鲜菇水果',
      products: [
        { id: 10101, name: '云南小粒咖啡', price: '58.00', image: 'https://via.placeholder.com/200/8B4513/FFFFFF?text=咖啡' },
        { id: 10102, name: '野生松茸', price: '128.00', image: 'https://via.placeholder.com/200/CD853F/FFFFFF?text=松茸' },
        { id: 10103, name: '石榴', price: '39.90', image: 'https://via.placeholder.com/200/DC143C/FFFFFF?text=石榴' },
        { id: 10104, name: '红心火龙果', price: '45.00', image: 'https://via.placeholder.com/200/FF69B4/FFFFFF?text=火龙果' }
      ]
    },
    {
      id: 102,
      name: '综合',
      products: [
        { id: 10201, name: '普洱茶饼', price: '88.00', image: 'https://via.placeholder.com/200/556B2F/FFFFFF?text=普洱' },
        { id: 10202, name: '宣威火腿', price: '168.00', image: 'https://via.placeholder.com/200/8B4513/FFFFFF?text=火腿' }
      ]
    },
    {
      id: 103,
      name: '调料',
      products: [
        { id: 10301, name: '云南辣椒', price: '25.00', image: 'https://via.placeholder.com/200/FF0000/FFFFFF?text=辣椒' }
      ]
    },
    { id: 104, name: '价格区', products: [] },
    { id: 105, name: '上新', products: [] }
  ],
  2: [ // 新疆
    {
      id: 201,
      name: '鲜菇水果',
      products: [
        { id: 20101, name: '阿克苏苹果', price: '39.90', image: 'https://via.placeholder.com/200/FF6347/FFFFFF?text=苹果' },
        { id: 20102, name: '库尔勒香梨', price: '45.00', image: 'https://via.placeholder.com/200/FFD700/FFFFFF?text=香梨' },
        { id: 20103, name: '吐鲁番葡萄', price: '52.00', image: 'https://via.placeholder.com/200/9370DB/FFFFFF?text=葡萄' }
      ]
    },
    {
      id: 202,
      name: '综合',
      products: [
        { id: 20201, name: '和田大枣', price: '58.00', image: 'https://via.placeholder.com/200/8B0000/FFFFFF?text=大枣' },
        { id: 20202, name: '新疆核桃', price: '68.00', image: 'https://via.placeholder.com/200/A0522D/FFFFFF?text=核桃' }
      ]
    },
    { id: 203, name: '进口水果', products: [] },
    { id: 204, name: '瓜/蔬/菇/菌', products: [] }
  ],
  3: [ // 山东
    {
      id: 301,
      name: '鲜菇水果',
      products: [
        { id: 30101, name: '烟台苹果', price: '35.00', image: 'https://via.placeholder.com/200/FF4500/FFFFFF?text=苹果' },
        { id: 30102, name: '莱阳梨', price: '28.00', image: 'https://via.placeholder.com/200/F0E68C/FFFFFF?text=梨' }
      ]
    },
    {
      id: 302,
      name: '综合',
      products: [
        { id: 30201, name: '章丘大葱', price: '18.00', image: 'https://via.placeholder.com/200/32CD32/FFFFFF?text=大葱' }
      ]
    }
  ],
  4: [ // 四川
    {
      id: 401,
      name: '调料',
      products: [
        { id: 40101, name: '四川花椒', price: '25.00', image: 'https://via.placeholder.com/200/B22222/FFFFFF?text=花椒' },
        { id: 40102, name: '郫县豆瓣', price: '32.00', image: 'https://via.placeholder.com/200/8B4513/FFFFFF?text=豆瓣' }
      ]
    },
    {
      id: 402,
      name: '鲜菇水果',
      products: [
        { id: 40201, name: '蒲江猕猴桃', price: '42.00', image: 'https://via.placeholder.com/200/9ACD32/FFFFFF?text=猕猴桃' }
      ]
    }
  ],
  5: [ // 浙江
    {
      id: 501,
      name: '综合',
      products: [
        { id: 50101, name: '西湖龙井', price: '128.00', image: 'https://via.placeholder.com/200/556B2F/FFFFFF?text=龙井' }
      ]
    }
  ],
  6: [ // 江苏
    {
      id: 601,
      name: '鲜菇水果',
      products: [
        { id: 60101, name: '阳澄湖大闸蟹', price: '188.00', image: 'https://via.placeholder.com/200/FF8C00/FFFFFF?text=大闸蟹' }
      ]
    },
    {
      id: 602,
      name: '综合',
      products: [
        { id: 60201, name: '碧螺春', price: '98.00', image: 'https://via.placeholder.com/200/228B22/FFFFFF?text=碧螺春' }
      ]
    }
  ]
}

// 当前选中省份的二级分类
const currentSubcategories = computed(() => {
  const currentProvince = displayProvinces.value[activeProvinceIndex.value]
  if (!currentProvince || currentProvince.isPlaceholder) {
    return []
  }
  return mockSubcategories[currentProvince.id] || []
})

const fetchCategories = async () => {
  try {
    const res = await getCategoryList({ is_show: true })
    allCategories.value = res.results || res
    // TODO: 将API数据映射到allProvinces和mockSubcategories
  } catch (error) {
    console.error('获取分类失败', error)
  }
}

const activeSubIndex = ref(0)

// 当前选中二级分类的商品
const currentProducts = computed(() => {
  if (currentSubcategories.value.length === 0) return []
  const currentSub = currentSubcategories.value[activeSubIndex.value]
  if (!currentSub || !currentSub.products) return []
  return currentSub.products
})

const onSearch = (value) => {
  if (value.trim()) {
    showToast(`搜索: ${value}`)
    // TODO: 执行搜索逻辑
  }
}

const onProvinceChange = (index) => {
  const province = displayProvinces.value[index]
  if (province.isPlaceholder) {
    showToast('敬请期待更多产地')
    return
  }
  activeProvinceIndex.value = index
  activeSubIndex.value = 0 // 切换省份时重置二级分类索引
}

const onSubCategoryChange = (index) => {
  activeSubIndex.value = index
}

const showAllProvinces = () => {
  showProvincePopup.value = true
}

const selectProvince = (index) => {
  activeProvinceIndex.value = index
  activeSubIndex.value = 0
  showProvincePopup.value = false
}

const goToProduct = (productId) => {
  router.push(`/product/${productId}`)
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

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
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

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

  .search-icons {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #333;
  }
}

// 横向省份导航
.province-tabs-wrapper {
  position: sticky;
  top: 54px;
  z-index: 98;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;

  .province-tabs {
    flex: 1;
    display: flex;
    gap: 12px;
    padding: 0 12px;
    overflow-x: auto;

    &::-webkit-scrollbar {
      display: none;
    }
  }

  .province-tab-item {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    cursor: pointer;
    transition: transform 0.2s;

    &:active {
      transform: scale(0.95);
    }

    .province-icon {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: #f5f5f5;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s;

      .province-emoji {
        font-size: 26px;
      }
    }

    .province-name {
      font-size: 12px;
      color: #666;
      white-space: nowrap;
    }

    &.active {
      .province-icon {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);

        .province-emoji {
          transform: scale(1.1);
        }
      }

      .province-name {
        color: #4CAF50;
        font-weight: 600;
      }
    }
  }

  .more-province-btn {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 0 12px;
    cursor: pointer;
    color: #999;

    &:active {
      opacity: 0.6;
    }

    .more-icon {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: #f5f5f5;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .more-text {
      font-size: 12px;
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

// 左侧二级分类
.subcategory-sidebar {
  width: 90px;
  background: #f5f5f5;
  overflow-y: auto;
  flex-shrink: 0;

  .subcategory-item {
    position: relative;
    padding: 16px 8px;
    text-align: center;
    cursor: pointer;
    background: #f5f5f5;
    transition: all 0.2s;

    &:active {
      background: #e8e8e8;
    }

    .subcategory-text {
      font-size: 13px;
      color: #666;
      line-height: 1.4;
    }

    &.active {
      background: #fff;

      .subcategory-text {
        color: #333;
        font-weight: 600;
      }

      .subcategory-indicator {
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 3px;
        height: 20px;
        background: #4CAF50;
        border-radius: 0 2px 2px 0;
      }
    }
  }

  .subcategory-placeholder {
    padding: 40px 8px;
    text-align: center;
    font-size: 12px;
    color: #999;
  }
}

// 右侧商品区域
.product-area {
  flex: 1;
  overflow-y: auto;
  background: #fff;
  padding: 12px;

  .product-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .product-card {
    position: relative;
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s;

    &:active {
      transform: scale(0.98);
    }

    .product-image {
      width: 100%;
      height: 160px;
      background: #fafafa;
    }

    .product-info {
      padding: 8px;
    }

    .product-name {
      font-size: 13px;
      color: #333;
      line-height: 1.4;
      margin-bottom: 6px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .product-price {
      color: #FF6B35;
      font-size: 16px;
      font-weight: bold;

      &::before {
        content: '¥';
        font-size: 12px;
      }
    }

    .add-cart-btn {
      position: absolute;
      bottom: 8px;
      right: 8px;
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

// 全部省份弹出层
.province-popup {
  padding: 16px;

  .popup-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 16px;
    border-bottom: 1px solid #f0f0f0;
    margin-bottom: 16px;

    .popup-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
    }
  }

  .province-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    padding-bottom: 16px;
  }

  .province-grid-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 16px 8px;
    border-radius: 12px;
    background: #f5f5f5;
    cursor: pointer;
    transition: all 0.3s;

    &.active {
      background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
      color: #fff;

      .province-grid-name {
        color: #fff;
        font-weight: 600;
      }
    }

    &:active {
      transform: scale(0.95);
    }

    .province-grid-emoji {
      font-size: 36px;
    }

    .province-grid-name {
      font-size: 12px;
      color: #333;
      margin-top: 4px;
    }
  }
}
</style>
