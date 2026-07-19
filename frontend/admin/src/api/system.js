import request from '@/utils/request'

// ==================== 用户角色管理 ====================

// 获取角色列表
export const getRoleList = (params) => {
  return request.get('/system/roles/', { params })
}

// 获取角色详情
export const getRoleDetail = (id) => {
  return request.get(`/system/roles/${id}/`)
}

// 创建角色
export const createRole = (data) => {
  return request.post('/system/roles/', data)
}

// 更新角色
export const updateRole = (id, data) => {
  return request.put(`/system/roles/${id}/`, data)
}

// 删除角色
export const deleteRole = (id) => {
  return request.delete(`/system/roles/${id}/`)
}
