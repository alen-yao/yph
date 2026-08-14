import request from '@/utils/request'

// 获取启用的地区列表
export const getEnabledRegions = () => {
  return request.get('/system/regions/enabled_list/')
}

// 获取所有地区列表（含未启用）
export const getAllRegions = () => {
  return request.get('/system/regions/')
}

// 获取商品列表
export const getProductList = (params) => {
  return request.get('/products/products/', { params })
}

// 获取商品详情
export const getProductDetail = (id) => {
  return request.get(`/products/products/${id}/`)
}

// 获取商品分类
export const getCategoryList = (params) => {
  return request.get('/products/categories/', { params })
}

// 获取品牌列表
export const getBrandList = () => {
  return request.get('/products/brands/')
}
