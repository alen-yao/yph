import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: () => import('@/layout/Index.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: '/dashboard',
          name: 'Dashboard',
          component: () => import('@/views/Dashboard.vue'),
          meta: { title: '数据概览', icon: 'DataLine', permission: 'dashboard' }
        },
        {
          path: '/products',
          name: 'Products',
          component: () => import('@/views/products/List.vue'),
          meta: { title: '商品管理', icon: 'Goods', permission: 'products' }
        },
        {
          path: '/products/create',
          name: 'ProductCreate',
          component: () => import('@/views/products/Form.vue'),
          meta: { title: '新增商品', hidden: true }
        },
        {
          path: '/products/edit/:id',
          name: 'ProductEdit',
          component: () => import('@/views/products/Form.vue'),
          meta: { title: '编辑商品', hidden: true }
        },
        {
          path: '/orders',
          name: 'Orders',
          component: () => import('@/views/orders/List.vue'),
          meta: { title: '订单管理', icon: 'List', permission: 'orders' }
        },
        {
          path: '/users',
          name: 'Users',
          component: () => import('@/views/users/List.vue'),
          meta: { title: '用户管理', icon: 'User', permission: 'users' }
        },
        {
          path: '/users/create',
          name: 'UserCreate',
          component: () => import('@/views/users/Form.vue'),
          meta: { title: '新增用户', hidden: true }
        },
        {
          path: '/users/edit/:id',
          name: 'UserEdit',
          component: () => import('@/views/users/Form.vue'),
          meta: { title: '编辑用户', hidden: true }
        },
        {
          path: '/marketing',
          name: 'Marketing',
          component: () => import('@/views/marketing/List.vue'),
          meta: { title: '营销活动', icon: 'Present', permission: 'marketing' }
        },
        {
          path: '/marketing/activity/create',
          name: 'ActivityCreate',
          component: () => import('@/views/marketing/ActivityForm.vue'),
          meta: { title: '新增活动', hidden: true }
        },
        {
          path: '/marketing/activity/edit/:id',
          name: 'ActivityEdit',
          component: () => import('@/views/marketing/ActivityForm.vue'),
          meta: { title: '编辑活动', hidden: true }
        },
        {
          path: '/marketing/coupon/create',
          name: 'CouponCreate',
          component: () => import('@/views/marketing/CouponForm.vue'),
          meta: { title: '新增优惠券', hidden: true }
        },
        {
          path: '/marketing/coupon/edit/:id',
          name: 'CouponEdit',
          component: () => import('@/views/marketing/CouponForm.vue'),
          meta: { title: '编辑优惠券', hidden: true }
        },
        {
          path: '/settings',
          name: 'Settings',
          component: () => import('@/views/settings/Index.vue'),
          meta: { title: '系统设置', icon: 'Setting', permission: 'settings' }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 检查登录状态
  if (to.meta.requiresAuth !== false && !userStore.token) {
    next('/login')
    return
  }

  // 已登录用户访问登录页，重定向到首页
  if (to.path === '/login' && userStore.token) {
    next('/')
    return
  }

  // 检查权限
  const permission = to.meta?.permission
  if (permission && !userStore.hasPermission(permission)) {
    // 没有权限，重定向到首页或显示403
    next('/dashboard')
    return
  }

  next()
})

export default router
