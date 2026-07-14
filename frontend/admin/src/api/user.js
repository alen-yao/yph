import request from '@/utils/request'

// 登录
export const login = (data) => {
  return request.post('/users/login/', data)
}

// 获取用户信息
export const getUserInfo = () => {
  return request.get('/users/users/profile/')
}

// 获取用户列表
export const getUserList = (params) => {
  return request.get('/users/users/', { params })
}

// 获取用户详情
export const getUserDetail = (id) => {
  return request.get(`/users/users/${id}/`)
}

// 创建用户
export const createUser = (data) => {
  return request.post('/users/users/', data)
}

// 更新用户
export const updateUser = (id, data) => {
  return request.put(`/users/users/${id}/`, data)
}

// 删除用户
export const deleteUser = (id) => {
  return request.delete(`/users/users/${id}/`)
}
