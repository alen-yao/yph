<template>
  <div class="login-container">
    <div class="login-content">
      <div class="login-left">
        <div class="logo-section">
          <h1 class="system-title">YPH 电商管理系统</h1>
          <p class="system-desc">全场景智能电商解决方案</p>
        </div>
      </div>
      <div class="login-right">
        <div class="login-box">
          <div class="login-header">
            <h2>欢迎登录</h2>
            <p>Welcome to YPH Admin</p>
          </div>
          <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin">
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                size="large"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                size="large"
                show-password
                @keyup.enter="handleLogin"
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                style="width: 100%"
                @click="handleLogin"
              >
                <span v-if="!loading">登 录</span>
                <span v-else>登录中...</span>
              </el-button>
            </el-form-item>
          </el-form>
          <div class="login-footer">
            <p>默认账号：admin / 密码：admin123</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: 'admin',
  password: 'admin123'
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    const success = await userStore.login(form.username, form.password)
    if (success) {
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error('用户名或密码错误')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    border-radius: 50%;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 50%;
    height: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.08) 0%, transparent 70%);
    border-radius: 50%;
  }
}

.login-content {
  display: flex;
  width: 1000px;
  height: 600px;
  background: $base-color-white;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #1890ff 0%, #0050b3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  position: relative;

  .logo-section {
    text-align: center;
    color: $base-color-white;

    .system-title {
      font-size: 36px;
      font-weight: 600;
      margin-bottom: 20px;
      letter-spacing: 2px;
    }

    .system-desc {
      font-size: 16px;
      opacity: 0.9;
      letter-spacing: 1px;
    }
  }
}

.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: $base-color-white;
}

.login-box {
  width: 100%;
  max-width: 380px;

  .login-header {
    text-align: center;
    margin-bottom: 40px;

    h2 {
      font-size: 28px;
      font-weight: 600;
      color: $base-color-text-primary;
      margin-bottom: 10px;
    }

    p {
      font-size: 14px;
      color: $base-color-text-secondary;
    }
  }

  :deep(.el-form-item) {
    margin-bottom: 24px;

    .el-input__wrapper {
      padding: 12px 15px;
      box-shadow: 0 0 0 1px $base-border-color-light inset;
      transition: $base-transition;

      &:hover {
        box-shadow: 0 0 0 1px $base-color-primary inset;
      }
    }

    .el-input__inner {
      font-size: 15px;
    }
  }

  :deep(.el-button--primary) {
    height: 48px;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 2px;
    border-radius: $base-border-radius;
  }

  .login-footer {
    margin-top: 30px;
    text-align: center;

    p {
      font-size: 13px;
      color: $base-color-text-secondary;
      background: $base-background-color-base;
      padding: 12px;
      border-radius: $base-border-radius;
    }
  }
}

@media (max-width: 768px) {
  .login-content {
    width: 90%;
    height: auto;
    flex-direction: column;
  }

  .login-left {
    padding: 40px 20px;

    .system-title {
      font-size: 24px;
    }

    .system-desc {
      font-size: 14px;
    }
  }

  .login-right {
    padding: 40px 20px;
  }
}
</style>
