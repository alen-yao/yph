<template>
  <div>
    <el-card>
      <el-form :inline="true">
        <el-form-item label="订单号">
          <el-input v-model="query.search" placeholder="订单号/收货人/手机号" clearable />
        </el-form-item>
        <el-form-item label="订单状态">
          <el-select v-model="query.status" placeholder="全部" clearable style="width: 150px">
            <el-option label="待支付" :value="0" />
            <el-option label="已支付" :value="1" />
            <el-option label="已发货" :value="2" />
            <el-option label="已完成" :value="3" />
            <el-option label="已取消" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="order_sn" label="订单号" width="180" />
        <el-table-column prop="total_amount" label="订单金额" width="120">
          <template #default="{ row }">¥{{ row.total_amount }}</template>
        </el-table-column>
        <el-table-column prop="receiver_name" label="收货人" width="100" />
        <el-table-column prop="receiver_mobile" label="手机号" width="130" />
        <el-table-column label="订单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_time" label="下单时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">详情</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="query.page"
        v-model:page-size="query.page_size"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchData"
        @size-change="fetchData"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>

    <!-- 订单详情对话框 -->
    <el-dialog v-model="detailVisible" title="订单详情" width="800px">
      <el-descriptions :column="2" border v-if="currentOrder">
        <el-descriptions-item label="订单号">{{ currentOrder.order_sn }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusType(currentOrder.status)">
            {{ getStatusText(currentOrder.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="收货人">{{ currentOrder.receiver_name }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentOrder.receiver_mobile }}</el-descriptions-item>
        <el-descriptions-item label="收货地址" :span="2">
          {{ currentOrder.receiver_province }} {{ currentOrder.receiver_city }}
          {{ currentOrder.receiver_district }} {{ currentOrder.receiver_address }}
        </el-descriptions-item>
        <el-descriptions-item label="商品金额">¥{{ currentOrder.goods_amount }}</el-descriptions-item>
        <el-descriptions-item label="运费">¥{{ currentOrder.freight_amount }}</el-descriptions-item>
        <el-descriptions-item label="优惠金额">¥{{ currentOrder.discount_amount }}</el-descriptions-item>
        <el-descriptions-item label="实付金额">¥{{ currentOrder.total_amount }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.created_time }}</el-descriptions-item>
        <el-descriptions-item label="支付时间">{{ currentOrder.pay_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentOrder.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getOrderList, getOrderDetail, deleteOrder } from '@/api/order'

const tableData = ref([])
const total = ref(0)
const detailVisible = ref(false)
const currentOrder = ref(null)

const query = reactive({
  page: 1,
  page_size: 10,
  search: '',
  status: null
})

const fetchData = async () => {
  try {
    const res = await getOrderList(query)
    tableData.value = res.results || []
    total.value = res.count || 0
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  }
}

const handleReset = () => {
  query.search = ''
  query.status = null
  query.page = 1
  fetchData()
}

const handleView = async (row) => {
  try {
    currentOrder.value = await getOrderDetail(row.id)
    detailVisible.value = true
  } catch (error) {
    ElMessage.error('获取订单详情失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除订单"${row.order_sn}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteOrder(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getStatusText = (status) => {
  const statusMap = {
    0: '待支付',
    1: '已支付',
    2: '已发货',
    3: '已完成',
    4: '已取消'
  }
  return statusMap[status] || '未知'
}

const getStatusType = (status) => {
  const typeMap = {
    0: 'warning',
    1: 'primary',
    2: 'success',
    3: 'info',
    4: 'danger'
  }
  return typeMap[status] || 'info'
}

onMounted(() => {
  fetchData()
})
</script>
