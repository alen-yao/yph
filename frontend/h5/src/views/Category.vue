<template>
  <div class="category">
    <van-search v-model="searchValue" placeholder="请输入搜索关键词" @search="handleSearch" />

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
  if (searchValue.value.trim()) {
    router.push({
      path: '/products',
      query: { keyword: searchValue.value }
    })
  }
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

<style scoped>
.category {
  height: 100vh;
  background: #fff;
}

.category-container {
  display: flex;
  height: calc(100vh - 54px);
}

.van-sidebar {
  width: 25%;
}

.category-content {
  flex: 1;
  overflow-y: auto;
  background: #f7f8fa;
}

.subcategory-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  padding: 15px;
}

.subcategory-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  font-size: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;

  &:active {
    transform: scale(0.95);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}
</style>
