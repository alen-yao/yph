import request from '@/utils/request'

// ========== 营销活动 ==========
// 获取活动列表
export const getActivityList = (params) => {
  return request.get('/marketing/activities/', { params })
}

// 获取活动详情
export const getActivityDetail = (id) => {
  return request.get(`/marketing/activities/${id}/`)
}

// 创建活动
export const createActivity = (data) => {
  return request.post('/marketing/activities/', data)
}

// 更新活动
export const updateActivity = (id, data) => {
  return request.put(`/marketing/activities/${id}/`, data)
}

// 删除活动
export const deleteActivity = (id) => {
  return request.delete(`/marketing/activities/${id}/`)
}

// ========== 优惠券 ==========
// 获取优惠券列表
export const getCouponList = (params) => {
  return request.get('/marketing/coupons/', { params })
}

// 获取优惠券详情
export const getCouponDetail = (id) => {
  return request.get(`/marketing/coupons/${id}/`)
}

// 创建优惠券
export const createCoupon = (data) => {
  return request.post('/marketing/coupons/', data)
}

// 更新优惠券
export const updateCoupon = (id, data) => {
  return request.put(`/marketing/coupons/${id}/`, data)
}

// 删除优惠券
export const deleteCoupon = (id) => {
  return request.delete(`/marketing/coupons/${id}/`)
}
