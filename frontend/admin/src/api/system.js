import request from '@/utils/request'

// ==================== 地区管理 ====================

// 获取地区列表
export const getRegionList = (params) => {
  return request.get('/system/regions/', { params })
}

// 获取启用的地区列表
export const getEnabledRegions = () => {
  return request.get('/system/regions/enabled_list/')
}

// 获取地区详情
export const getRegionDetail = (id) => {
  return request.get(`/system/regions/${id}/`)
}

// 更新地区
export const updateRegion = (id, data) => {
  return request.put(`/system/regions/${id}/`, data)
}

// 批量更新地区排序
export const updateRegionSort = (data) => {
  return request.post('/system/regions/update_sort/', data)
}

// 切换地区启用状态
export const toggleRegionStatus = (id) => {
  return request.post(`/system/regions/${id}/toggle_status/`)
}

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
