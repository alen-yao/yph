<template>
  <div class="category">
    <!-- 顶部导航栏 -->
    <div class="top-nav-bar">
      <van-icon name="wap-nav" size="20" class="nav-icon" />
      <van-search
        v-model="searchValue"
        shape="round"
        placeholder="新鲜海南芒果"
        background="transparent"
        @click="handleSearch"
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

    <div class="category-container">
      <van-sidebar v-model="activeKey">
        <van-sidebar-item v-for="(cat, index) in categories" :key="cat.id" :title="cat.name" />
      </van-sidebar>

      <div class="category-content">
        <div v-if="subcategories.length > 0" class="subcategory-list">
          <div
            v-for="sub in subcategories"
            :key="sub.id"
            class="subcategory-item"
            @click="handleSubCategoryClick(sub.id)"
          >
            <van-image
              v-if="sub.icon"
              :src="sub.icon"
              fit="cover"
              width="60"
              height="60"
            />
            <van-image
              v-else
              src="https://via.placeholder.com/60?text=No+Image"
              fit="cover"
              width="60"
              height="60"
            />
            <div>{{ sub.name }}</div>
          </div>
        </div>
        <van-empty v-else description="暂无子分类" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCategoryList } from '@/api/product'

const router = useRouter()
const searchValue = ref('')
const activeKey = ref(0)
const allCategories = ref([])

// 一级分类（无父分类的）
const categories = computed(() => {
  return allCategories.value.filter(cat => !cat.parent && cat.is_show)
})

// 当前选中分类的子分类
const subcategories = computed(() => {
  if (categories.value.length === 0) return []
  const currentCategory = categories.value[activeKey.value]
  if (!currentCategory) return []

  return allCategories.value.filter(cat => cat.parent === currentCategory.id && cat.is_show)
})

const fetchCategories = async () => {
  try {
    const res = await getCategoryList({ is_show: true })
    allCategories.value = res.results || res
  } catch (error) {
    console.error('获取分类失败', error)
  }
}

const handleSearch = () => {
  router.push('/search')
}

const handleSubCategoryClick = (categoryId) => {
  router.push({
    path: '/products',
    query: { category: categoryId }
  })
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

.category-container {
  display: flex;
  height: calc(100vh - 52px);
}

:deep(.van-sidebar) {
  width: 90px;
  background: #f5f5f5;

  .van-sidebar-item {
    padding: 20px 12px;
    font-size: 13px;
    color: #666;
    background: transparent;
    border-right: 3px solid transparent;

    &::before {
      display: none;
    }

    &--select {
      color: #333;
      background: #fff;
      font-weight: 500;
      border-right-color: #1a1a1a;

      &::before {
        display: none;
      }
    }
  }
}

.category-content {
  flex: 1;
  overflow-y: auto;
  background: #fff;
  padding: 16px 12px;
}

.subcategory-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.subcategory-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px 8px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: transform 0.2s;

  &:active {
    transform: scale(0.95);
  }

  :deep(.van-image) {
    border-radius: 50%;
    overflow: hidden;
    background: #f5f5f5;
  }
}
</style>
