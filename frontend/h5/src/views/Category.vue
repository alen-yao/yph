<template>
  <div class="category">
    <van-search v-model="searchValue" placeholder="请输入搜索关键词" />

    <div class="category-container">
      <van-sidebar v-model="activeKey">
        <van-sidebar-item v-for="cat in categories" :key="cat.id" :title="cat.name" />
      </van-sidebar>

      <div class="category-content">
        <div class="subcategory-list">
          <div v-for="sub in subcategories" :key="sub.id" class="subcategory-item">
            <van-image :src="sub.icon || 'https://via.placeholder.com/80'" />
            <div>{{ sub.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchValue = ref('')
const activeKey = ref(0)

const categories = ref([
  { id: 1, name: '数码电器' },
  { id: 2, name: '服装服饰' },
  { id: 3, name: '食品生鲜' },
  { id: 4, name: '图书音像' },
  { id: 5, name: '家居家装' }
])

const subcategories = ref([
  { id: 1, name: '手机', icon: '' },
  { id: 2, name: '电脑', icon: '' },
  { id: 3, name: '数码配件', icon: '' },
  { id: 4, name: '智能设备', icon: '' }
])
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
}
</style>
