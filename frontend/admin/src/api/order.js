import request from '@/utils/request'

// 获取订单列表
export const getOrderList = (params) => {
  return request.get('/trade/orders/', { params })
}

// 获取订单详情
export const getOrderDetail = (id) => {
  return request.get(`/trade/orders/${id}/`)
}

// 更新订单
export const updateOrder = (id, data) => {
  return request.put(`/trade/orders/${id}/`, data)
}

// 删除订单
export const deleteOrder = (id) => {
  return request.delete(`/trade/orders/${id}/`)
}

// 取消订单
export const cancelOrder = (id) => {
  return request.post(`/trade/orders/${id}/cancel/`)
}

// 确认收货
export const confirmReceipt = (id) => {
  return request.post(`/trade/orders/${id}/confirm-receipt/`)
}

// 获取订单状态统计
export const getOrderStatusCount = () => {
  return request.get('/trade/orders/status-count/')
}
