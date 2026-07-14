import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'))

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

  return { token, userInfo, login, logout }
})
