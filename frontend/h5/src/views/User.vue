<template>
  <div class="user-page">
    <!-- 顶部导航栏 -->
    <div class="top-nav-bar">
      <van-icon name="wap-nav" size="20" class="nav-icon" />
      <div class="nav-title">个人中心</div>
      <div class="nav-right">
        <van-icon name="ellipsis" size="20" class="nav-icon" />
        <van-icon name="scan" size="20" class="nav-icon" />
      </div>
    </div>

    <!-- 绿色渐变头部 -->
    <div class="user-header">
      <!-- 头像区域 -->
      <div class="avatar-section">
        <div class="avatar-wrapper">
          <van-image
            round
            width="60"
            height="60"
            :src="userInfo.avatar || 'https://via.placeholder.com/60/4CAF50/FFFFFF?text=VIP'"
          />
          <div class="vip-badge">VIP</div>
        </div>
        <div class="avatar-info">
          <div class="avatar-text">点击显示微信头像</div>
          <div class="member-badge">成长值</div>
        </div>
        <div class="share-btn">
          <van-icon name="qr" size="16" />
          <span>晒码赢福利</span>
        </div>
      </div>

      <!-- 数据统计 -->
      <div class="stats-section">
        <div class="stat-item" @click="handleStatClick('balance')">
          <div class="stat-value">{{ userInfo.balance || '0.00' }}</div>
          <div class="stat-label">余额</div>
        </div>
        <div class="stat-item" @click="handleStatClick('points')">
          <div class="stat-value">{{ userInfo.points || '0' }}</div>
          <div class="stat-label">积分</div>
        </div>
        <div class="stat-item" @click="handleStatClick('cards')">
          <div class="stat-value">{{ userInfo.cards || '0' }}</div>
          <div class="stat-label">卡</div>
        </div>
        <div class="stat-item" @click="handleStatClick('coupons')">
          <div class="stat-value">{{ userInfo.coupons || '0' }}</div>
          <div class="stat-label">优惠券/积分</div>
        </div>
        <div class="stat-item" @click="handleStatClick('wallet')">
          <van-icon name="balance-o" size="20" class="stat-icon" />
          <div class="stat-label">钱包</div>
        </div>
      </div>
    </div>

    <!-- VIP会员卡片 -->
    <div class="vip-card">
      <div class="vip-info">
        <van-icon name="vip-card" size="18" color="#D4A574" />
        <span class="vip-text">本来生活VIP会员，享6大会员专享权益</span>
      </div>
      <van-button size="small" round color="#4CAF50">立即开通</van-button>
    </div>

    <!-- 广告横幅 -->
    <div class="banner-ad">
      <van-image
        width="100%"
        height="120"
        fit="cover"
        src="https://via.placeholder.com/750x240/2E7D32/FFFFFF?text=农家旅游券·充值入口"
      >
        <template #loading>
          <van-loading type="spinner" size="20" />
        </template>
      </van-image>
      <van-button size="small" round class="banner-btn">点击领券</van-button>
    </div>

    <!-- 我的订单 -->
    <div class="order-section">
      <div class="section-header">
        <span class="section-title">我的订单</span>
        <van-button size="small" plain hairline @click="goToAllOrders">
          查看全部订单
          <van-icon name="arrow" />
        </van-button>
      </div>

      <div class="order-types">
        <div class="order-type-item" @click="handleOrderClick('待付款')">
          <van-icon name="pending-payment" size="24" color="#FF9800" />
          <span class="order-type-text">待付款</span>
        </div>
        <div class="order-type-item" @click="handleOrderClick('待发货')">
          <van-icon name="tosend" size="24" color="#2196F3" />
          <span class="order-type-text">待发货</span>
        </div>
        <div class="order-type-item" @click="handleOrderClick('待收货')">
          <van-icon name="logistics" size="24" color="#4CAF50" />
          <span class="order-type-text">待收货</span>
        </div>
        <div class="order-type-item" @click="handleOrderClick('待评价')">
          <van-icon name="comment-o" size="24" color="#F44336" />
          <span class="order-type-text">待评价</span>
        </div>
        <div class="order-type-item" @click="handleOrderClick('直复购/清单')">
          <van-icon name="replay" size="24" color="#9C27B0" />
          <span class="order-type-text">直复购/清单</span>
        </div>
      </div>
    </div>

    <!-- 功能列表 -->
    <van-cell-group class="function-list">
      <van-cell
        title="我的拼单"
        icon="friends-o"
        is-link
        @click="handleFunctionClick('拼单')"
      />
      <van-cell
        title="订水卡"
        icon="card"
        is-link
        @click="handleFunctionClick('订水卡')"
      />
    </van-cell-group>

    <!-- 快捷入口 -->
    <div class="quick-actions">
      <div class="quick-action-item" @click="handleQuickAction('购物车')">
        <van-icon name="shopping-cart-o" size="22" />
        <span>购物车</span>
        <van-badge :content="cartCount" v-if="cartCount > 0" />
      </div>
      <div class="quick-action-item" @click="handleQuickAction('收货地址')">
        <van-icon name="location-o" size="22" />
        <span>收货地址</span>
      </div>
      <div class="quick-action-item" @click="handleQuickAction('客服聊天')">
        <van-icon name="chat-o" size="22" />
        <span>客服聊天</span>
      </div>
      <div class="quick-action-item" @click="handleQuickAction('联系商家电话')">
        <van-icon name="phone-o" size="22" />
        <span>联系商家电话</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()

const userInfo = ref({
  nickname: 'YPH用户',
  avatar: '',
  balance: '0.00',
  points: 0,
  cards: 0,
  coupons: 0
})

const cartCount = ref(0)

const onBack = () => {
  router.back()
}

const handleStatClick = (type) => {
  showToast(`查看${type}`)
}

const goToAllOrders = () => {
  showToast('查看全部订单')
}

const handleOrderClick = (type) => {
  showToast(`查看${type}订单`)
}

const handleFunctionClick = (name) => {
  showToast(`进入${name}`)
}

const handleQuickAction = (action) => {
  if (action === '购物车') {
    router.push('/cart')
  } else if (action === '收货地址') {
    router.push('/address')
  } else {
    showToast(action)
  }
}
</script>

<style lang="scss" scoped>
.user-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 60px;
}

// 顶部导航栏
.top-nav-bar {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background: #fff;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .nav-icon {
    color: #333;
    cursor: pointer;

    &:active {
      opacity: 0.6;
    }
  }

  .nav-title {
    flex: 1;
    text-align: center;
    font-size: 17px;
    font-weight: 500;
    color: #333;
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}

// 绿色渐变头部
.user-header {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  padding: 0 16px 20px;
  color: #fff;
}

// 头像区域
.avatar-section {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 20px;
}

.avatar-wrapper {
  position: relative;

  .vip-badge {
    position: absolute;
    bottom: -2px;
    left: -2px;
    background: #D4A574;
    color: #fff;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 8px;
    font-weight: bold;
  }
}

.avatar-info {
  flex: 1;

  .avatar-text {
    font-size: 15px;
    margin-bottom: 4px;
  }

  .member-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.3);
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
  }
}

.share-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  padding: 6px 10px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;

  span {
    white-space: nowrap;
  }
}

// 数据统计
.stats-section {
  display: flex;
  justify-content: space-around;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 16px 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;

  &:active {
    opacity: 0.7;
  }

  .stat-value {
    font-size: 16px;
    font-weight: bold;
  }

  .stat-label {
    font-size: 12px;
    opacity: 0.9;
  }

  .stat-icon {
    margin-bottom: 2px;
  }
}

// VIP会员卡片
.vip-card {
  margin: 12px 16px;
  background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.vip-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;

  .vip-text {
    font-size: 13px;
    color: #5D4037;
  }
}

// 广告横幅
.banner-ad {
  margin: 12px 16px;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  .banner-btn {
    position: absolute;
    bottom: 12px;
    right: 12px;
    background: #FF5722;
    color: #fff;
    border: none;
    padding: 6px 16px;
  }
}

// 我的订单
.order-section {
  margin: 12px 16px;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;

  .section-title {
    font-size: 15px;
    font-weight: 600;
    color: #333;
  }
}

.order-types {
  display: flex;
  justify-content: space-around;
}

.order-type-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;

  &:active {
    opacity: 0.7;
  }

  .order-type-text {
    font-size: 12px;
    color: #666;
  }
}

// 功能列表
.function-list {
  margin: 12px 16px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  :deep(.van-cell) {
    font-size: 14px;
  }
}

// 快捷入口
.quick-actions {
  position: fixed;
  bottom: 60px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  background: #fff;
  padding: 12px 16px;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}

.quick-action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #666;
  cursor: pointer;
  position: relative;

  &:active {
    opacity: 0.7;
  }

  span {
    text-align: center;
  }

  :deep(.van-badge) {
    position: absolute;
    top: -4px;
    right: -8px;
  }
}
</style>
