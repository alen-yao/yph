<template>
  <div class="page-container">
    <el-card shadow="hover">
      <el-form :inline="true" class="search-form">
        <el-form-item label="商品名称">
          <el-input
            v-model="query.keyword"
            placeholder="请输入商品名称"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData" icon="Search">查询</el-button>
          <el-button @click="handleReset" icon="Refresh">重置</el-button>
          <el-button type="success" @click="handleCreate" icon="Plus">新增商品</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column label="商品图片" width="100" align="center">
          <template #default="{ row }">
            <el-image
              :src="row.main_image"
              fit="cover"
              :preview-src-list="[row.main_image]"
              style="width: 60px; height: 60px; border-radius: 4px"
            />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="category_name" label="分类" width="120" align="center" />
        <el-table-column prop="price" label="价格" width="100" align="center">
          <template #default="{ row }">
            <span style="color: #ff6700; font-weight: 500">¥{{ row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="sales_count" label="销量" width="100" align="center" />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)" icon="Edit">
              编辑
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)" icon="Delete">
              删除
            </el-button>
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
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProductList, deleteProduct } from '@/api/product'

const router = useRouter()

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const query = reactive({
  keyword: '',
  page: 1,
  page_size: 10
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getProductList(query)
    tableData.value = res.results || []
    total.value = res.count || 0
  } catch (error) {
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  query.keyword = ''
  query.page = 1
  fetchData()
}

const handleCreate = () => {
  router.push('/products/create')
}

const handleEdit = (row) => {
  router.push(`/products/edit/${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除商品"${row.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteProduct(row.id)
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

<style lang="scss" scoped>
.page-container {
  .search-form {
    margin-bottom: 0;
  }

  :deep(.el-card__body) {
    padding-bottom: 0;
  }
}
</style>
