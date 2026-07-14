<template>
  <div>
    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="营销活动" name="activity">
        <el-card>
          <el-form :inline="true">
            <el-form-item label="活动名称">
              <el-input v-model="activityQuery.search" placeholder="请输入活动名称" clearable />
            </el-form-item>
            <el-form-item label="活动类型">
              <el-select v-model="activityQuery.activity_type" placeholder="全部" clearable style="width: 150px">
                <el-option label="优惠券" :value="1" />
                <el-option label="秒杀" :value="2" />
                <el-option label="拼团" :value="3" />
                <el-option label="砍价" :value="4" />
                <el-option label="满减" :value="5" />
              </el-select>
            </el-form-item>
            <el-form-item label="活动状态">
              <el-select v-model="activityQuery.activity_state" placeholder="全部" clearable style="width: 150px">
                <el-option label="未开始" :value="0" />
                <el-option label="进行中" :value="1" />
                <el-option label="已结束" :value="2" />
                <el-option label="已取消" :value="3" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="fetchActivityData">查询</el-button>
              <el-button @click="handleActivityReset">重置</el-button>
              <el-button type="success" @click="handleCreateActivity">新增活动</el-button>
            </el-form-item>
          </el-form>

          <el-table :data="activityData" border stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="activity_name" label="活动名称" show-overflow-tooltip />
            <el-table-column prop="activity_type_display" label="活动类型" width="100" />
            <el-table-column label="活动状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getActivityStateType(row.activity_state)">
                  {{ row.activity_state_display }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="start_time" label="开始时间" width="180" />
            <el-table-column prop="end_time" label="结束时间" width="180" />
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_enable ? 'success' : 'danger'">
                  {{ row.is_enable ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditActivity(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteActivity(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination
            v-model:current-page="activityQuery.page"
            v-model:page-size="activityQuery.page_size"
            :total="activityTotal"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="fetchActivityData"
            @size-change="fetchActivityData"
            style="margin-top: 20px; justify-content: flex-end"
          />
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="优惠券管理" name="coupon">
        <el-card>
          <el-form :inline="true">
            <el-form-item label="优惠券名称">
              <el-input v-model="couponQuery.search" placeholder="请输入优惠券名称" clearable />
            </el-form-item>
            <el-form-item label="优惠券类型">
              <el-select v-model="couponQuery.coupon_type" placeholder="全部" clearable style="width: 150px">
                <el-option label="满减券" :value="1" />
                <el-option label="折扣券" :value="2" />
                <el-option label="兑换券" :value="3" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="fetchCouponData">查询</el-button>
              <el-button @click="handleCouponReset">重置</el-button>
              <el-button type="success" @click="handleCreateCoupon">新增优惠券</el-button>
            </el-form-item>
          </el-form>

          <el-table :data="couponData" border stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="coupon_name" label="优惠券名称" show-overflow-tooltip />
            <el-table-column prop="coupon_type_display" label="类型" width="100" />
            <el-table-column prop="activity_name" label="所属活动" width="150" show-overflow-tooltip />
            <el-table-column prop="coupon_price" label="优惠金额" width="100">
              <template #default="{ row }">¥{{ row.coupon_price }}</template>
            </el-table-column>
            <el-table-column prop="min_amount" label="最低消费" width="100">
              <template #default="{ row }">¥{{ row.min_amount }}</template>
            </el-table-column>
            <el-table-column label="数量" width="150">
              <template #default="{ row }">
                {{ row.received_quantity }} / {{ row.total_quantity }}
              </template>
            </el-table-column>
            <el-table-column prop="valid_days" label="有效天数" width="100" />
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_enable ? 'success' : 'danger'">
                  {{ row.is_enable ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleEditCoupon(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click="handleDeleteCoupon(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination
            v-model:current-page="couponQuery.page"
            v-model:page-size="couponQuery.page_size"
            :total="couponTotal"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="fetchCouponData"
            @size-change="fetchCouponData"
            style="margin-top: 20px; justify-content: flex-end"
          />
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getActivityList, deleteActivity,
  getCouponList, deleteCoupon
} from '@/api/marketing'

const router = useRouter()
const activeTab = ref('activity')

// 活动数据
const activityData = ref([])
const activityTotal = ref(0)
const activityQuery = reactive({
  page: 1,
  page_size: 10,
  search: '',
  activity_type: null,
  activity_state: null
})

// 优惠券数据
const couponData = ref([])
const couponTotal = ref(0)
const couponQuery = reactive({
  page: 1,
  page_size: 10,
  search: '',
  coupon_type: null
})

// 获取活动列表
const fetchActivityData = async () => {
  try {
    const res = await getActivityList(activityQuery)
    activityData.value = res.results || []
    activityTotal.value = res.count || 0
  } catch (error) {
    ElMessage.error('获取活动列表失败')
  }
}

// 获取优惠券列表
const fetchCouponData = async () => {
  try {
    const res = await getCouponList(couponQuery)
    couponData.value = res.results || []
    couponTotal.value = res.count || 0
  } catch (error) {
    ElMessage.error('获取优惠券列表失败')
  }
}

const handleTabClick = (tab) => {
  if (tab.props.name === 'activity') {
    fetchActivityData()
  } else if (tab.props.name === 'coupon') {
    fetchCouponData()
  }
}

// 活动相关操作
const handleActivityReset = () => {
  activityQuery.search = ''
  activityQuery.activity_type = null
  activityQuery.activity_state = null
  activityQuery.page = 1
  fetchActivityData()
}

const handleCreateActivity = () => {
  router.push('/marketing/activity/create')
}

const handleEditActivity = (row) => {
  router.push(`/marketing/activity/edit/${row.id}`)
}

const handleDeleteActivity = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除活动"${row.activity_name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteActivity(row.id)
    ElMessage.success('删除成功')
    fetchActivityData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 优惠券相关操作
const handleCouponReset = () => {
  couponQuery.search = ''
  couponQuery.coupon_type = null
  couponQuery.page = 1
  fetchCouponData()
}

const handleCreateCoupon = () => {
  router.push('/marketing/coupon/create')
}

const handleEditCoupon = (row) => {
  router.push(`/marketing/coupon/edit/${row.id}`)
}

const handleDeleteCoupon = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除优惠券"${row.coupon_name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteCoupon(row.id)
    ElMessage.success('删除成功')
    fetchCouponData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getActivityStateType = (state) => {
  const typeMap = {
    0: 'info',
    1: 'success',
    2: 'warning',
    3: 'danger'
  }
  return typeMap[state] || 'info'
}

onMounted(() => {
  fetchActivityData()
})
</script>
