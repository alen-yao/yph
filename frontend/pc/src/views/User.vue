<template>
  <div class="user-page">
    <div class="container">
      <div class="user-layout">
        <aside class="user-sidebar">
          <div class="user-info">
            <el-avatar :size="80" src="https://via.placeholder.com/80" />
            <div class="user-name">{{ userInfo.username }}</div>
          </div>
          <el-menu :default-active="activeMenu" @select="handleMenuSelect">
            <el-menu-item index="orders">
              <el-icon><List /></el-icon>
              <span>我的订单</span>
            </el-menu-item>
            <el-menu-item index="favorites">
              <el-icon><Star /></el-icon>
              <span>我的收藏</span>
            </el-menu-item>
            <el-menu-item index="addresses">
              <el-icon><Location /></el-icon>
              <span>收货地址</span>
            </el-menu-item>
            <el-menu-item index="profile">
              <el-icon><User /></el-icon>
              <span>个人信息</span>
            </el-menu-item>
            <el-menu-item index="password">
              <el-icon><Lock /></el-icon>
              <span>修改密码</span>
            </el-menu-item>
          </el-menu>
        </aside>

        <main class="user-main">
          <div v-if="activeMenu === 'orders'" class="section-content">
            <h2 class="section-title">我的订单</h2>
            <el-empty description="暂无订单" />
          </div>

          <div v-if="activeMenu === 'favorites'" class="section-content">
            <h2 class="section-title">我的收藏</h2>
            <el-empty description="暂无收藏" />
          </div>

          <div v-if="activeMenu === 'addresses'" class="section-content">
            <h2 class="section-title">收货地址</h2>
            <el-button type="primary" @click="addAddress">新增地址</el-button>
          </div>

          <div v-if="activeMenu === 'profile'" class="section-content">
            <h2 class="section-title">个人信息</h2>
            <el-form :model="userInfo" label-width="100px" style="max-width: 600px">
              <el-form-item label="用户名">
                <el-input v-model="userInfo.username" disabled />
              </el-form-item>
              <el-form-item label="昵称">
                <el-input v-model="userInfo.nickname" />
              </el-form-item>
              <el-form-item label="手机号">
                <el-input v-model="userInfo.mobile" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="userInfo.email" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveProfile">保存</el-button>
              </el-form-item>
            </el-form>
          </div>

          <div v-if="activeMenu === 'password'" class="section-content">
            <h2 class="section-title">修改密码</h2>
            <el-form :model="passwordForm" label-width="120px" style="max-width: 600px">
              <el-form-item label="原密码">
                <el-input v-model="passwordForm.oldPassword" type="password" show-password />
              </el-form-item>
              <el-form-item label="新密码">
                <el-input v-model="passwordForm.newPassword" type="password" show-password />
              </el-form-item>
              <el-form-item label="确认新密码">
                <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="changePassword">确认修改</el-button>
              </el-form-item>
            </el-form>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const activeMenu = ref('orders')
const userInfo = ref({
  username: 'user123',
  nickname: '用户昵称',
  mobile: '13800138000',
  email: 'user@example.com'
})

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const handleMenuSelect = (index) => {
  activeMenu.value = index
}

const addAddress = () => {
  ElMessage.info('新增地址功能')
}

const saveProfile = () => {
  ElMessage.success('保存成功')
}

const changePassword = () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  ElMessage.success('密码修改成功')
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.user-page {
  padding: 20px 0 60px;
  min-height: 70vh;
}

.user-layout {
  display: flex;
  gap: 20px;
}

.user-sidebar {
  width: 220px;
  flex-shrink: 0;

  .user-info {
    background: $bg-color-white;
    padding: 30px 20px;
    border-radius: $border-radius-lg;
    text-align: center;
    margin-bottom: 20px;

    .user-name {
      margin-top: 16px;
      font-size: $font-size-lg;
      font-weight: 500;
      color: $text-color-primary;
    }
  }

  .el-menu {
    background: $bg-color-white;
    border-radius: $border-radius-lg;
    border: none;
  }
}

.user-main {
  flex: 1;
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  padding: 30px;
  min-height: 500px;

  .section-title {
    font-size: $font-size-xl;
    font-weight: 600;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid $border-color-light;
  }
}
</style>
