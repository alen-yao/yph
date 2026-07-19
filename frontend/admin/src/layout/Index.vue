<template>
  <el-container class="layout-container">
    <el-aside :width="isCollapse ? '64px' : '266px'" class="layout-aside">
      <div class="logo">
        <h2 v-if="!isCollapse">YPH管理系统</h2>
        <h2 v-else class="logo-small">YPH</h2>
      </div>
      <el-menu
        :default-active="currentRoute"
        :collapse="isCollapse"
        router
        background-color="#282c34"
        text-color="rgba(255,255,255,0.8)"
        active-text-color="#fff"
      >
        <el-menu-item
          v-for="route in menuRoutes"
          :key="route.path"
          :index="route.path"
        >
          <el-icon><component :is="route.meta.icon" /></el-icon>
          <template #title>
            <span>{{ route.meta.title }}</span>
          </template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="layout-header">
        <div class="header-left">
          <el-icon class="collapse-icon" @click="toggleCollapse">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ userInfo.nickname || userInfo.username || '管理员' }}
              <el-icon class="arrow-down"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="layout-main">
        <router-view />
      </el-main>

      <el-footer class="layout-footer">
        <div class="footer-content">
          Copyright © 2024 YPH电商平台. All rights reserved.
        </div>
      </el-footer>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapse = ref(false)
const currentRoute = computed(() => route.path)
const userInfo = computed(() => userStore.userInfo)

// 基于权限过滤菜单
const menuRoutes = computed(() => {
  const allRoutes = router.options.routes
    .find(r => r.path === '/')
    ?.children.filter(r => r.meta?.title && !r.meta?.hidden) || []

  // 根据用户权限过滤菜单
  return allRoutes.filter(route => {
    const permission = route.meta?.permission
    return userStore.hasPermission(permission)
  })
})

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('退出成功')
  router.push('/login')
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.layout-container {
  height: 100vh;
}

.layout-aside {
  background-color: $base-menu-background;
  transition: $base-transition;
  overflow-x: hidden;

  :deep(.el-menu) {
    border-right: none;
  }

  :deep(.el-menu-item) {
    height: $base-menu-item-height;
    line-height: $base-menu-item-height;

    &.is-active {
      background-color: $base-menu-background-active !important;
    }

    &:hover {
      background-color: rgba(24, 144, 255, 0.1) !important;
    }
  }
}

.logo {
  height: $base-logo-height;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: $base-transition;

  h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 2px;

    &.logo-small {
      font-size: 18px;
    }
  }
}

.layout-header {
  height: $base-header-height;
  background: $base-color-white;
  border-bottom: 1px solid $base-border-color-lighter;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 $base-padding;
  box-shadow: $base-box-shadow;
  position: relative;
  z-index: 10;

  .header-left {
    display: flex;
    align-items: center;

    .collapse-icon {
      font-size: 20px;
      cursor: pointer;
      color: $base-color-text-regular;
      transition: $base-transition;

      &:hover {
        color: $base-color-primary;
      }
    }
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 20px;
  }
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: $base-border-radius;
  transition: $base-transition;
  color: $base-color-text-regular;
  font-size: $base-font-size-default;

  &:hover {
    background-color: rgba(24, 144, 255, 0.1);
    color: $base-color-primary;
  }

  .arrow-down {
    font-size: 12px;
  }
}

.layout-main {
  background: $base-color-background;
  padding: $base-padding;
  overflow-y: auto;

  :deep(> *) {
    animation: fadeIn 0.3s ease-in-out;
  }
}

.layout-footer {
  height: 55px;
  background: $base-color-white;
  border-top: 1px solid $base-border-color-lighter;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;

  .footer-content {
    color: $base-color-text-secondary;
    font-size: $base-font-size-small;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
