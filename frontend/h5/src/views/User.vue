<template>
  <div class="user">
    <div class="user-header">
      <van-image round width="60" height="60" :src="userInfo.avatar || 'https://via.placeholder.com/60'" />
      <div class="user-info">
        <div class="user-name">{{ userInfo.nickname || '未登录' }}</div>
        <div class="user-level">普通会员</div>
      </div>
    </div>

    <van-grid :column-num="4" :border="false">
      <van-grid-item icon="balance-o" text="余额" :badge="userInfo.user_money || '0'" />
      <van-grid-item icon="gold-coin-o" text="积分" :badge="userInfo.user_points || '0'" />
      <van-grid-item icon="gift-o" text="优惠券" badge="3" />
      <van-grid-item icon="star-o" text="收藏" />
    </van-grid>

    <van-cell-group title="我的订单" style="margin-top: 10px">
      <van-grid :column-num="5" :border="false">
        <van-grid-item icon="pending-payment" text="待付款" />
        <van-grid-item icon="tosend" text="待发货" />
        <van-grid-item icon="logistics" text="待收货" />
        <van-grid-item icon="comment-o" text="待评价" />
        <van-grid-item icon="after-sale" text="退换/售后" />
      </van-grid>
    </van-cell-group>

    <van-cell-group style="margin-top: 10px">
      <van-cell title="收货地址" is-link to="/address" />
      <van-cell title="我的足迹" is-link />
      <van-cell title="设置" is-link />
    </van-cell-group>

    <div style="padding: 16px">
      <van-button type="danger" block @click="handleLogout">退出登录</van-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { showToast } from 'vant'

const userInfo = ref({
  nickname: 'YPH用户',
  avatar: '',
  user_money: 1000,
  user_points: 500
})

const handleLogout = () => {
  showToast('退出登录')
}
</script>

<style scoped>
.user {
  min-height: 100vh;
  background: #f7f8fa;
}

.user-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.user-level {
  font-size: 12px;
  opacity: 0.8;
}
</style>
