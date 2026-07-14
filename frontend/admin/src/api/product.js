import request from '@/utils/request'

// 获取商品列表
export const getProductList = (params) => {
  return request.get('/products/products/', { params })
}

// 获取商品详情
export const getProductDetail = (id) => {
  return request.get(`/products/products/${id}/`)
}

// 创建商品
export const createProduct = (data) => {
  return request.post('/products/products/', data)
}

// 更新商品
export const updateProduct = (id, data) => {
  return request.put(`/products/products/${id}/`, data)
}

// 删除商品
export const deleteProduct = (id) => {
  return request.delete(`/products/products/${id}/`)
}

// 获取商品分类
export const getCategoryList = () => {
  return request.get('/products/categories/')
}

// 获取品牌列表
export const getBrandList = () => {
  return request.get('/products/brands/')
}
