<template>
  <div>
    <el-page-header @back="handleBack" :content="isEdit ? '编辑用户' : '新增用户'" />

    <el-card style="margin-top: 20px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" :disabled="isEdit" />
        </el-form-item>

        <el-form-item label="手机号" prop="mobile">
          <el-input v-model="form.mobile" placeholder="请输入手机号" maxlength="11" />
        </el-form-item>

        <el-form-item label="密码" v-if="!isEdit" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>

        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入昵称" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="form.gender" style="width: 100%">
                <el-option label="保密" :value="0" />
                <el-option label="男" :value="1" />
                <el-option label="女" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="生日" prop="birthday">
              <el-date-picker
                v-model="form.birthday"
                type="date"
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="积分" prop="user_points">
              <el-input-number v-model="form.user_points" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="余额" prop="user_money">
              <el-input-number v-model="form.user_money" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" active-text="正常" inactive-text="禁用" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交</el-button>
          <el-button @click="handleBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getUserDetail, createUser, updateUser } from '@/api/user'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)
const isEdit = ref(false)
const userId = ref(null)

const form = reactive({
  username: '',
  mobile: '',
  password: '',
  nickname: '',
  email: '',
  gender: 0,
  birthday: null,
  user_points: 0,
  user_money: 0,
  is_active: true
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  mobile: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  email: [
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ]
}

const handleBack = () => {
  router.back()
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    const data = { ...form }
    // 编辑时不发送密码字段
    if (isEdit.value) {
      delete data.password
      await updateUser(userId.value, data)
      ElMessage.success('更新成功')
    } else {
      await createUser(data)
      ElMessage.success('创建成功')
    }
    router.push('/users')
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

const fetchUserDetail = async (id) => {
  try {
    const res = await getUserDetail(id)
    Object.assign(form, res)
  } catch (error) {
    ElMessage.error('获取用户详情失败')
    router.back()
  }
}

onMounted(async () => {
  if (route.params.id) {
    isEdit.value = true
    userId.value = route.params.id
    await fetchUserDetail(userId.value)
  }
})
</script>
