<template>
  <div class="app-container">
    <router-view class="main-content" />
    <van-tabbar v-if="showTabbar" v-model="active" route>
      <van-tabbar-item to="/home" icon="wap-home-o">首页</van-tabbar-item>
      <van-tabbar-item to="/category" icon="apps-o">分类</van-tabbar-item>
      <van-tabbar-item to="/cart" icon="shopping-cart-o">购物车</van-tabbar-item>
      <van-tabbar-item to="/user" icon="user-o">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = ref(0)

const tabMap = {
  '/home': 0,
  '/category': 1,
  '/cart': 2,
  '/user': 3
}

// 需要显示底部导航栏的路由
const tabbarRoutes = ['/home', '/category', '/cart', '/user']

// 根据当前路由判断是否显示底部导航栏
const showTabbar = computed(() => {
  return tabbarRoutes.includes(route.path)
})

watch(() => route.path, (path) => {
  active.value = tabMap[path] || 0
}, { immediate: true })
</script>

<style scoped>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  overflow-y: auto;
}
</style>
