import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layout/TabBar.vue'),
      redirect: '/home',
      children: [
        {
          path: '/home',
          name: 'Home',
          component: () => import('@/views/Home.vue'),
          meta: { title: '首页', keepAlive: true }
        },
        {
          path: '/category',
          name: 'Category',
          component: () => import('@/views/Category.vue'),
          meta: { title: '分类', keepAlive: true }
        },
        {
          path: '/cart',
          name: 'Cart',
          component: () => import('@/views/Cart.vue'),
          meta: { title: '购物车' }
        },
        {
          path: '/user',
          name: 'User',
          component: () => import('@/views/User.vue'),
          meta: { title: '我的' }
        }
      ]
    },
    {
      path: '/product/:id',
      name: 'ProductDetail',
      component: () => import('@/views/ProductDetail.vue'),
      meta: { title: '商品详情' }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { title: '登录' }
    }
  ]
})

export default router
