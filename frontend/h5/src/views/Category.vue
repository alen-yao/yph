<template>
  <div class="category">
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

    <!-- 占位元素 -->
    <div class="search-bar-placeholder"></div>

    <!-- 横向省份导航栏 -->
    <div class="province-nav">
      <div class="province-tabs">
        <div
          v-for="(province, index) in displayProvinces"
          :key="province.id"
          :class="['province-tab', { active: activeProvinceIndex === index }]"
          @click="onProvinceChange(index)"
        >
          <span class="province-emoji">{{ province.emoji }}</span>
          <span class="province-label">{{ province.name }}</span>
        </div>
      </div>
      <div class="more-btn" v-if="allProvinces.length > 4" @click="showAllProvinces">
        <van-icon name="apps-o" size="16" />
        <span>全部</span>
      </div>
    </div>

    <!-- 二级分类列表（竖向） -->
    <div class="subcategory-container">
      <div v-if="currentSubcategories.length > 0" class="subcategory-list">
        <div
          v-for="sub in currentSubcategories"
          :key="sub.id"
          class="subcategory-item"
          @click="handleSubCategoryClick(sub.id)"
        >
          <van-image
            :src="sub.icon || 'https://via.placeholder.com/100/F4A460/FFFFFF?text=' + sub.name"
            fit="cover"
            class="subcategory-image"
            lazy-load
          >
            <template #loading>
              <van-loading type="spinner" size="20" />
            </template>
          </van-image>
          <div class="subcategory-info">
            <div class="subcategory-name">{{ sub.name }}</div>
            <div class="subcategory-desc" v-if="sub.description">{{ sub.description }}</div>
          </div>
          <van-icon name="arrow" color="#ccc" />
        </div>
      </div>
      <van-empty v-else description="该地区暂无特产分类" />
    </div>

    <!-- 全部省份弹出层 -->
    <van-popup
      v-model:show="showProvincePopup"
      position="bottom"
      :style="{ height: '60%' }"
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

// 模拟二级分类数据 - 实际应该从API获取
const mockSubcategories = {
  1: [ // 云南
    { id: 101, name: '普洱茶', description: '云南特色茶叶', icon: 'https://via.placeholder.com/100/8B4513/FFFFFF?text=普洱茶' },
    { id: 102, name: '文山三七', description: '名贵药材', icon: 'https://via.placeholder.com/100/228B22/FFFFFF?text=三七' },
    { id: 103, name: '宣威火腿', description: '传统腌制肉品', icon: 'https://via.placeholder.com/100/DC143C/FFFFFF?text=火腿' },
    { id: 104, name: '野生菌', description: '山珍美味', icon: 'https://via.placeholder.com/100/CD853F/FFFFFF?text=野生菌' }
  ],
  2: [ // 新疆
    { id: 201, name: '和田大枣', description: '优质红枣', icon: 'https://via.placeholder.com/100/8B0000/FFFFFF?text=大枣' },
    { id: 202, name: '阿克苏苹果', description: '冰糖心苹果', icon: 'https://via.placeholder.com/100/FF6347/FFFFFF?text=苹果' },
    { id: 203, name: '吐鲁番葡萄', description: '无核白葡萄', icon: 'https://via.placeholder.com/100/9370DB/FFFFFF?text=葡萄' },
    { id: 204, name: '库尔勒香梨', description: '香甜多汁', icon: 'https://via.placeholder.com/100/FFD700/FFFFFF?text=香梨' }
  ],
  3: [ // 山东
    { id: 301, name: '烟台苹果', description: '红富士苹果', icon: 'https://via.placeholder.com/100/FF4500/FFFFFF?text=苹果' },
    { id: 302, name: '章丘大葱', description: '高品质大葱', icon: 'https://via.placeholder.com/100/32CD32/FFFFFF?text=大葱' },
    { id: 303, name: '莱阳梨', description: '清甜爽口', icon: 'https://via.placeholder.com/100/F0E68C/FFFFFF?text=梨' }
  ],
  4: [ // 四川
    { id: 401, name: '四川花椒', description: '麻辣调料', icon: 'https://via.placeholder.com/100/B22222/FFFFFF?text=花椒' },
    { id: 402, name: '郫县豆瓣', description: '传统调味品', icon: 'https://via.placeholder.com/100/8B4513/FFFFFF?text=豆瓣' },
    { id: 403, name: '蒲江猕猴桃', description: '绿色水果', icon: 'https://via.placeholder.com/100/9ACD32/FFFFFF?text=猕猴桃' }
  ],
  5: [ // 浙江
    { id: 501, name: '西湖龙井', description: '名茶之首', icon: 'https://via.placeholder.com/100/556B2F/FFFFFF?text=龙井' },
    { id: 502, name: '杭州丝绸', description: '传统工艺品', icon: 'https://via.placeholder.com/100/FFB6C1/FFFFFF?text=丝绸' }
  ],
  6: [ // 江苏
    { id: 601, name: '阳澄湖大闸蟹', description: '鲜美海鲜', icon: 'https://via.placeholder.com/100/FF8C00/FFFFFF?text=大闸蟹' },
    { id: 602, name: '碧螺春', description: '苏州名茶', icon: 'https://via.placeholder.com/100/228B22/FFFFFF?text=碧螺春' }
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
}

const showAllProvinces = () => {
  showProvincePopup.value = true
}

const selectProvince = (index) => {
  activeProvinceIndex.value = index
  showProvincePopup.value = false
}

const handleSubCategoryClick = (categoryId) => {
  showToast(`查看商品分类: ${categoryId}`)
  // TODO: 跳转到商品列表页
  // router.push({
  //   path: '/products',
  //   query: { category: categoryId }
  // })
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.category {
  height: 100vh;
  background: #fff;
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

// 横向省份导航栏
.province-nav {
  display: flex;
  align-items: center;
  background: #fff;
  padding: 12px 8px;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 52px;
  z-index: 99;

  .province-tabs {
    flex: 1;
    display: flex;
    gap: 8px;
    overflow-x: auto;

    &::-webkit-scrollbar {
      display: none;
    }
  }

  .province-tab {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px 16px;
    border-radius: 12px;
    background: #f5f5f5;
    cursor: pointer;
    transition: all 0.3s;

    &.active {
      background: linear-gradient(135deg, #FF6B35 0%, #FF8C5A 100%);
      color: #fff;
      box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);

      .province-emoji {
        transform: scale(1.1);
      }

      .province-label {
        font-weight: 600;
      }
    }

    &:active {
      transform: scale(0.95);
    }

    .province-emoji {
      font-size: 22px;
      transition: transform 0.3s;
    }

    .province-label {
      font-size: 12px;
      color: #333;
      white-space: nowrap;
    }

    &.active .province-label {
      color: #fff;
    }
  }

  .more-btn {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 8px 12px;
    color: #666;
    cursor: pointer;

    &:active {
      opacity: 0.6;
    }

    span {
      font-size: 11px;
    }
  }
}

// 二级分类容器
.subcategory-container {
  flex: 1;
  overflow-y: auto;
  background: #f5f5f5;
  padding: 8px 0;
  min-height: calc(100vh - 52px - 90px - 54px); // 减去顶部栏、省份栏、底部TabBar
}

.subcategory-list {
  background: #fff;
  margin: 0 8px;
  border-radius: 12px;
  overflow: hidden;
}

.subcategory-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: background 0.2s;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background: #fafafa;
  }

  .subcategory-image {
    width: 70px;
    height: 70px;
    border-radius: 8px;
    overflow: hidden;
    background: #f5f5f5;
    flex-shrink: 0;
  }

  .subcategory-info {
    flex: 1;
    min-width: 0;
  }

  .subcategory-name {
    font-size: 15px;
    font-weight: 500;
    color: #333;
    margin-bottom: 4px;
  }

  .subcategory-desc {
    font-size: 12px;
    color: #999;
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
    padding: 12px;
    border-radius: 12px;
    background: #f5f5f5;
    cursor: pointer;
    transition: all 0.3s;

    &.active {
      background: linear-gradient(135deg, #FF6B35 0%, #FF8C5A 100%);
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
      font-size: 32px;
    }

    .province-grid-name {
      font-size: 13px;
      color: #333;
    }
  }
}
</style>
