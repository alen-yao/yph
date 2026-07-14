<template>
  <div>
    <el-page-header @back="handleBack" :content="isEdit ? '编辑优惠券' : '新增优惠券'" />

    <el-card style="margin-top: 20px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="所属活动" prop="activity">
          <el-select v-model="form.activity" placeholder="请选择活动" style="width: 100%" filterable>
            <el-option
              v-for="activity in activities"
              :key="activity.id"
              :label="activity.activity_name"
              :value="activity.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="优惠券名称" prop="coupon_name">
          <el-input v-model="form.coupon_name" placeholder="请输入优惠券名称" maxlength="100" show-word-limit />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="优惠券类型" prop="coupon_type">
              <el-select v-model="form.coupon_type" placeholder="请选择" style="width: 100%">
                <el-option label="满减券" :value="1" />
                <el-option label="折扣券" :value="2" />
                <el-option label="兑换券" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="优惠金额" prop="coupon_price">
              <el-input-number v-model="form.coupon_price" :min="0.01" :precision="2" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="最低消费" prop="min_amount">
              <el-input-number v-model="form.min_amount" :min="0" :precision="2" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="有效天数" prop="valid_days">
              <el-input-number v-model="form.valid_days" :min="1" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="总量" prop="total_quantity">
              <el-input-number v-model="form.total_quantity" :min="1" :step="10" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="限领数量" prop="per_user_limit">
              <el-input-number v-model="form.per_user_limit" :min="1" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

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
import {
  getCouponDetail, createCoupon, updateCoupon,
  getActivityList
} from '@/api/marketing'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)
const isEdit = ref(false)
const couponId = ref(null)
const activities = ref([])

const form = reactive({
  activity: null,
  coupon_name: '',
  coupon_type: null,
  coupon_price: 0,
  min_amount: 0,
  total_quantity: 100,
  per_user_limit: 1,
  valid_days: 7,
  is_enable: true
})

const rules = {
  activity: [{ required: true, message: '请选择所属活动', trigger: 'change' }],
  coupon_name: [{ required: true, message: '请输入优惠券名称', trigger: 'blur' }],
  coupon_type: [{ required: true, message: '请选择优惠券类型', trigger: 'change' }],
  coupon_price: [{ required: true, message: '请输入优惠金额', trigger: 'blur' }],
  total_quantity: [{ required: true, message: '请输入总量', trigger: 'blur' }],
  valid_days: [{ required: true, message: '请输入有效天数', trigger: 'blur' }]
}

const handleBack = () => {
  router.back()
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    if (isEdit.value) {
      await updateCoupon(couponId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createCoupon(form)
      ElMessage.success('创建成功')
    }
    router.push('/marketing')
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

const fetchActivities = async () => {
  try {
    const res = await getActivityList({ page_size: 100 })
    activities.value = res.results || []
  } catch (error) {
    console.error('获取活动列表失败', error)
  }
}

const fetchCouponDetail = async (id) => {
  try {
    const res = await getCouponDetail(id)
    Object.assign(form, res)
  } catch (error) {
    ElMessage.error('获取优惠券详情失败')
    router.back()
  }
}

onMounted(async () => {
  await fetchActivities()

  if (route.params.id) {
    isEdit.value = true
    couponId.value = route.params.id
    await fetchCouponDetail(couponId.value)
  }
})
</script>
