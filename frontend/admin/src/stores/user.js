import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))

  // 检查是否是超级管理员
  const isAdmin = computed(() => {
    return userInfo.value.is_staff === true || userInfo.value.is_superuser === true
  })

  // 获取用户权限
  const permissions = computed(() => {
    // 超级管理员拥有所有权限
    if (isAdmin.value) {
      return {
        dashboard: true,
        users: true,
        products: true,
        orders: true,
        marketing: true,
        settings: true
      }
    }
    // 普通用户根据角色获取权限
    return userInfo.value.role?.permissions_data || {}
  })

  // 检查是否有某个权限
  const hasPermission = (permission) => {
    if (!permission) return true // 没有权限要求的路由，所有人都可以访问
    if (isAdmin.value) return true // 管理员拥有所有权限
    return permissions.value[permission] === true
  }

  const login = async (username, password) => {
    try {
      const res = await apiLogin({ username, password })
      token.value = res.access
      userInfo.value = res
      localStorage.setItem('token', res.access)
      localStorage.setItem('userInfo', JSON.stringify(res))
      return true
    } catch (error) {
      return false
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = {}
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return {
    token,
    userInfo,
    isAdmin,
    permissions,
    hasPermission,
    login,
    logout
  }
})
