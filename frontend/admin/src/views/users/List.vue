<template>
  <div>
    <el-card>
      <el-form :inline="true">
        <el-form-item label="关键词">
          <el-input v-model="query.search" placeholder="用户名/手机号/昵称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="handleCreate">新增用户</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="mobile" label="手机号" width="130" />
        <el-table-column prop="nickname" label="昵称" />
        <el-table-column prop="email" label="邮箱" show-overflow-tooltip />
        <el-table-column prop="user_points" label="积分" width="100" />
        <el-table-column prop="user_money" label="余额" width="120">
          <template #default="{ row }">¥{{ row.user_money }}</template>
        </el-table-column>
        <el-table-column prop="created_time" label="注册时间" width="180" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">详情</el-button>
            <el-button type="warning" link size="small" @click="handleEdit(row)">编辑</el-button>
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

    <!-- 用户详情对话框 -->
    <el-dialog v-model="detailVisible" title="用户详情" width="600px">
      <el-descriptions :column="2" border v-if="currentUser">
        <el-descriptions-item label="用户名">{{ currentUser.username }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentUser.mobile }}</el-descriptions-item>
        <el-descriptions-item label="昵称">{{ currentUser.nickname || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ currentUser.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="性别">
          {{ currentUser.gender === 1 ? '男' : currentUser.gender === 2 ? '女' : '保密' }}
        </el-descriptions-item>
        <el-descriptions-item label="生日">{{ currentUser.birthday || '-' }}</el-descriptions-item>
        <el-descriptions-item label="积分">{{ currentUser.user_points }}</el-descriptions-item>
        <el-descriptions-item label="余额">¥{{ currentUser.user_money }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentUser.is_active ? 'success' : 'danger'">
            {{ currentUser.is_active ? '正常' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ currentUser.created_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList, getUserDetail, deleteUser } from '@/api/user'

const router = useRouter()
const tableData = ref([])
const total = ref(0)
const detailVisible = ref(false)
const currentUser = ref(null)

const query = reactive({
  page: 1,
  page_size: 10,
  search: ''
})

const fetchData = async () => {
  try {
    const res = await getUserList(query)
    tableData.value = res.results || []
    total.value = res.count || 0
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  }
}

const handleReset = () => {
  query.search = ''
  query.page = 1
  fetchData()
}

const handleCreate = () => {
  router.push('/users/create')
}

const handleView = async (row) => {
  try {
    currentUser.value = await getUserDetail(row.id)
    detailVisible.value = true
  } catch (error) {
    ElMessage.error('获取用户详情失败')
  }
}

const handleEdit = (row) => {
  router.push(`/users/edit/${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除用户"${row.username}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchData()
})
</script>
