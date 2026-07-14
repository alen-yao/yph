<template>
  <div>
    <el-page-header @back="handleBack" :content="isEdit ? '编辑活动' : '新增活动'" />

    <el-card style="margin-top: 20px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="活动名称" prop="activity_name">
          <el-input v-model="form.activity_name" placeholder="请输入活动名称" maxlength="100" show-word-limit />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="活动类型" prop="activity_type">
              <el-select v-model="form.activity_type" placeholder="请选择" style="width: 100%">
                <el-option label="优惠券" :value="1" />
                <el-option label="秒杀" :value="2" />
                <el-option label="拼团" :value="3" />
                <el-option label="砍价" :value="4" />
                <el-option label="满减" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="活动状态" prop="activity_state">
              <el-select v-model="form.activity_state" placeholder="请选择" style="width: 100%">
                <el-option label="未开始" :value="0" />
                <el-option label="进行中" :value="1" />
                <el-option label="已结束" :value="2" />
                <el-option label="已取消" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始时间" prop="start_time">
              <el-date-picker
                v-model="form.start_time"
                type="datetime"
                placeholder="选择开始时间"
                format="YYYY-MM-DD HH:mm:ss"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间" prop="end_time">
              <el-date-picker
                v-model="form.end_time"
                type="datetime"
                placeholder="选择结束时间"
                format="YYYY-MM-DD HH:mm:ss"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="活动描述" prop="activity_desc">
          <el-input
            v-model="form.activity_desc"
            type="textarea"
            :rows="4"
            placeholder="请输入活动描述"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="是否启用" prop="is_enable">
          <el-switch v-model="form.is_enable" active-text="启用" inactive-text="禁用" />
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
import { getActivityDetail, createActivity, updateActivity } from '@/api/marketing'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)
const isEdit = ref(false)
const activityId = ref(null)

const form = reactive({
  activity_name: '',
  activity_type: null,
  activity_state: 0,
  start_time: null,
  end_time: null,
  activity_desc: '',
  is_enable: true
})

const rules = {
  activity_name: [{ required: true, message: '请输入活动名称', trigger: 'blur' }],
  activity_type: [{ required: true, message: '请选择活动类型', trigger: 'change' }],
  activity_state: [{ required: true, message: '请选择活动状态', trigger: 'change' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }]
}

const handleBack = () => {
  router.back()
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    if (isEdit.value) {
      await updateActivity(activityId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createActivity(form)
      ElMessage.success('创建成功')
    }
    router.push('/marketing')
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

const fetchActivityDetail = async (id) => {
  try {
    const res = await getActivityDetail(id)
    Object.assign(form, res)
  } catch (error) {
    ElMessage.error('获取活动详情失败')
    router.back()
  }
}

onMounted(async () => {
  if (route.params.id) {
    isEdit.value = true
    activityId.value = route.params.id
    await fetchActivityDetail(activityId.value)
  }
})
</script>
