<template>
  <div class="layout">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="top-bar">
        <div class="container">
          <div class="top-bar-content">
            <div class="left">
              <span>欢迎来到 YPH 电商平台！</span>
            </div>
            <div class="right">
              <template v-if="isLogin">
                <span class="user-name">{{ username }}</span>
                <el-divider direction="vertical" />
                <a href="#" @click.prevent="handleLogout">退出</a>
              </template>
              <template v-else>
                <router-link to="/login">登录</router-link>
                <el-divider direction="vertical" />
                <router-link to="/register">注册</router-link>
              </template>
              <el-divider direction="vertical" />
              <router-link to="/user">个人中心</router-link>
              <el-divider direction="vertical" />
              <router-link to="/cart">
                <el-icon><ShoppingCart /></el-icon>
                购物车
                <el-badge v-if="cartCount > 0" :value="cartCount" class="cart-badge" />
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="header-main">
        <div class="container">
          <div class="header-content">
            <router-link to="/" class="logo">
              <h1>YPH</h1>
              <span>电商平台</span>
            </router-link>

            <div class="search-box">
              <el-input
                v-model="searchKeyword"
                placeholder="请输入商品名称"
                class="search-input"
                @keyup.enter="handleSearch"
              >
                <template #append>
                  <el-button type="primary" @click="handleSearch">
                    <el-icon><Search /></el-icon>
                    搜索
                  </el-button>
                </template>
              </el-input>
              <div class="hot-keywords">
                <span>热门搜索：</span>
                <a
                  v-for="keyword in hotKeywords"
                  :key="keyword"
                  href="#"
                  @click.prevent="searchKeyword = keyword; handleSearch()"
                >
                  {{ keyword }}
                </a>
              </div>
            </div>

            <div class="header-right">
              <el-button type="primary" plain @click="$router.push('/cart')">
                <el-icon><ShoppingCart /></el-icon>
                购物车
                <el-badge v-if="cartCount > 0" :value="cartCount" class="item" />
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <nav class="nav-bar">
        <div class="container">
          <div class="nav-content">
            <el-dropdown class="category-menu" trigger="hover" @command="handleCategoryClick">
              <div class="category-menu-trigger">
                <el-icon><Grid /></el-icon>
                全部商品分类
              </div>
              <template #dropdown>
                <el-dropdown-menu class="category-dropdown">
                  <el-dropdown-item
                    v-for="category in categories"
                    :key="category.id"
                    :command="category.id"
                  >
                    <el-icon v-if="category.icon"><Picture /></el-icon>
                    {{ category.name }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <div class="nav-links">
              <router-link to="/" :class="{ active: $route.path === '/' }">首页</router-link>
              <router-link to="/products" :class="{ active: $route.path === '/products' }">全部商品</router-link>
              <a href="#">限时秒杀</a>
              <a href="#">新品上市</a>
              <a href="#">品牌专区</a>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 底部 -->
    <footer class="footer">
      <div class="footer-main">
        <div class="container">
          <div class="footer-content">
            <div class="footer-section">
              <h3>购物指南</h3>
              <ul>
                <li><a href="#">购物流程</a></li>
                <li><a href="#">会员介绍</a></li>
                <li><a href="#">常见问题</a></li>
                <li><a href="#">联系客服</a></li>
              </ul>
            </div>
            <div class="footer-section">
              <h3>配送方式</h3>
              <ul>
                <li><a href="#">上门自提</a></li>
                <li><a href="#">物流配送</a></li>
                <li><a href="#">配送服务</a></li>
                <li><a href="#">运费说明</a></li>
              </ul>
            </div>
            <div class="footer-section">
              <h3>支付方式</h3>
              <ul>
                <li><a href="#">在线支付</a></li>
                <li><a href="#">货到付款</a></li>
                <li><a href="#">分期付款</a></li>
                <li><a href="#">发票说明</a></li>
              </ul>
            </div>
            <div class="footer-section">
              <h3>售后服务</h3>
              <ul>
                <li><a href="#">退换货政策</a></li>
                <li><a href="#">退换货流程</a></li>
                <li><a href="#">价格保护</a></li>
                <li><a href="#">退款说明</a></li>
              </ul>
            </div>
            <div class="footer-section">
              <h3>关于我们</h3>
              <ul>
                <li><a href="#">公司简介</a></li>
                <li><a href="#">联系我们</a></li>
                <li><a href="#">招聘信息</a></li>
                <li><a href="#">友情链接</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <div class="container">
          <p>Copyright © 2024 YPH 电商平台. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCategoryList } from '@/api/product'

const router = useRouter()

const isLogin = ref(false)
const username = ref('用户名')
const cartCount = ref(0)
const searchKeyword = ref('')
const categories = ref([])

const hotKeywords = ref(['手机', '笔记本', '耳机', '数码相机', '智能手表'])

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      path: '/products',
      query: { keyword: searchKeyword.value }
    })
  } else {
    ElMessage.warning('请输入搜索关键词')
  }
}

const handleLogout = () => {
  localStorage.removeItem('token')
  isLogin.value = false
  ElMessage.success('退出成功')
  router.push('/')
}

const handleCategoryClick = (categoryId) => {
  router.push({
    path: '/products',
    query: { category: categoryId }
  })
}

const fetchCategories = async () => {
  try {
    const res = await getCategoryList({ is_show: true })
    categories.value = res.results || res
  } catch (error) {
    console.error('获取分类失败', error)
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

// 顶部栏
.top-bar {
  background: $bg-color-grey;
  border-bottom: 1px solid $border-color-light;
  font-size: $font-size-xs;
  color: $text-color-secondary;

  .top-bar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 30px;

    .left,
    .right {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    a {
      &:hover {
        color: $theme-color;
      }
    }

    .user-name {
      color: $theme-color;
    }

    .el-divider {
      margin: 0;
    }

    .cart-badge {
      margin-left: 4px;
    }
  }
}

// 主导航区域
.header-main {
  background: $bg-color-white;
  padding: 20px 0;

  .header-content {
    display: flex;
    align-items: center;
    gap: 40px;
  }

  .logo {
    display: flex;
    align-items: baseline;
    gap: 8px;
    text-decoration: none;

    h1 {
      font-size: 36px;
      font-weight: 700;
      color: $theme-color;
      letter-spacing: 2px;
    }

    span {
      font-size: $font-size-sm;
      color: $text-color-secondary;
    }

    &:hover h1 {
      color: $theme-color-hover;
    }
  }

  .search-box {
    flex: 1;

    .search-input {
      :deep(.el-input__wrapper) {
        border-radius: 4px 0 0 4px;
      }

      :deep(.el-input-group__append) {
        background: $theme-color;
        border-color: $theme-color;
        border-radius: 0 4px 4px 0;
        padding: 0 20px;

        .el-button {
          background: transparent;
          border: none;
          color: $text-color-white;
          font-weight: 500;

          &:hover {
            background: transparent;
            opacity: 0.9;
          }
        }
      }
    }

    .hot-keywords {
      margin-top: 8px;
      font-size: $font-size-xs;
      color: $text-color-tertiary;

      a {
        margin-left: 12px;
        color: $text-color-secondary;

        &:hover {
          color: $theme-color;
        }
      }
    }
  }

  .header-right {
    .el-button {
      height: 40px;
      padding: 0 20px;
    }
  }
}

// 导航栏
.nav-bar {
  background: $theme-color;
  height: $nav-height;

  .nav-content {
    display: flex;
    align-items: center;
    height: 100%;
  }

  .category-menu {
    height: 100%;

    .category-menu-trigger {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 0 20px;
      height: 100%;
      background: $theme-color-dark;
      color: $text-color-white;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.3s;

      &:hover {
        background: darken($theme-color-dark, 5%);
      }
    }
  }

  :deep(.category-dropdown) {
    min-width: 200px;
    max-height: 400px;
    overflow-y: auto;

    .el-dropdown-menu__item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;

      &:hover {
        background: $bg-color;
        color: $theme-color;
      }
    }
  }

  .nav-links {
    display: flex;
    align-items: center;
    height: 100%;
    margin-left: 40px;
    gap: 40px;

    a {
      color: $text-color-white;
      font-size: $font-size-base;
      height: 100%;
      display: flex;
      align-items: center;
      position: relative;
      transition: opacity 0.3s;

      &:hover,
      &.active {
        opacity: 1;

        &::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          height: 3px;
          background: $text-color-white;
        }
      }

      &:not(.active) {
        opacity: 0.9;
      }
    }
  }
}

// 主内容
.main-content {
  flex: 1;
  background: $bg-color;
}

// 底部
.footer {
  background: $bg-color-grey;
  margin-top: 60px;

  .footer-main {
    padding: 40px 0;
    border-bottom: 1px solid $border-color;
  }

  .footer-content {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 40px;
  }

  .footer-section {
    h3 {
      font-size: $font-size-base;
      font-weight: 600;
      margin-bottom: 16px;
      color: $text-color-primary;
    }

    ul {
      li {
        margin-bottom: 8px;

        a {
          font-size: $font-size-sm;
          color: $text-color-secondary;
          transition: color 0.3s;

          &:hover {
            color: $theme-color;
          }
        }
      }
    }
  }

  .footer-bottom {
    padding: 20px 0;
    text-align: center;
    font-size: $font-size-xs;
    color: $text-color-tertiary;
  }
}
</style>
