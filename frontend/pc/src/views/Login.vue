<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <div class="login-header">
          <h1>YPH 电商平台</h1>
          <p>欢迎登录</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" class="login-form">
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          <el-form-item>
            <el-checkbox v-model="form.remember">记住密码</el-checkbox>
            <a href="#" class="forgot-password">忘记密码？</a>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-button"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
          <div class="register-link">
            还没有账号？<a href="#" @click.prevent="goToRegister">立即注册</a>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: 'demo',
  password: '123456',
  remember: false
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    // 模拟登录
    setTimeout(() => {
      localStorage.setItem('token', 'mock-token')
      ElMessage.success('登录成功')
      router.push('/')
    }, 1000)
  } finally {
    loading.value = false
  }
}

const goToRegister = () => {
  ElMessage.info('注册功能开发中')
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e93323 0%, #d12920 100%);
}

.login-container {
  width: 100%;
  max-width: 450px;
  padding: 20px;
}

.login-box {
  background: $bg-color-white;
  border-radius: $border-radius-xl;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 50px 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  h1 {
    font-size: 32px;
    font-weight: 700;
    color: $theme-color;
    margin-bottom: 12px;
  }

  p {
    font-size: $font-size-base;
    color: $text-color-secondary;
  }
}

.login-form {
  .el-form-item {
    margin-bottom: 24px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .forgot-password {
    float: right;
    color: $theme-color;
    font-size: $font-size-sm;

    &:hover {
      text-decoration: underline;
    }
  }

  .login-button {
    width: 100%;
    height: 48px;
    font-size: $font-size-lg;
    font-weight: 500;
  }

  .register-link {
    text-align: center;
    font-size: $font-size-sm;
    color: $text-color-secondary;

    a {
      color: $theme-color;
      margin-left: 4px;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>
