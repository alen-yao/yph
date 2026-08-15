<template>
  <div class="region-list">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>地区管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleEnableAll">
              启用所有地区
            </el-button>
            <el-button @click="loadRegions">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="regionList"
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" />

        <el-table-column label="地区图标" width="100">
          <template #default="{ row }">
            <el-image
              :src="getRegionIcon(row.code)"
              fit="cover"
              style="width: 50px; height: 50px; border-radius: 50%"
              :style="{ filter: row.status ? 'none' : 'grayscale(100%) opacity(0.5)' }"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>

        <el-table-column prop="name" label="地区名称" width="150" />

        <el-table-column prop="code" label="地区代码" width="120" />

        <el-table-column prop="sort_order" label="排序" width="120" sortable="custom">
          <template #default="{ row }">
            <el-input-number
              v-model="row.sort_order"
              :min="0"
              :max="999"
              size="small"
              @change="handleSortUpdate(row)"
            />
          </template>
        </el-table-column>

        <el-table-column label="商品数量" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.products_count || 0 }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              :loading="row.switching"
              @change="handleStatusToggle(row)"
            />
          </template>
        </el-table-column>

        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_time) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" fixed="right" width="150">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              link
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              :type="row.status ? 'danger' : 'success'"
              size="small"
              link
              @click="handleStatusToggle(row)"
            >
              {{ row.status ? '禁用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-text class="text-info">
          共 {{ total }} 个地区，已启用 {{ enabledCount }} 个
        </el-text>
      </div>
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑地区"
      width="500px"
    >
      <el-form
        v-if="currentRegion"
        :model="currentRegion"
        label-width="100px"
      >
        <el-form-item label="地区名称">
          <el-input v-model="currentRegion.name" disabled />
        </el-form-item>
        <el-form-item label="地区代码">
          <el-input v-model="currentRegion.code" disabled />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number
            v-model="currentRegion.sort_order"
            :min="0"
            :max="999"
          />
        </el-form-item>
        <el-form-item label="启用状态">
          <el-switch v-model="currentRegion.status" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Picture } from '@element-plus/icons-vue'
import { getRegionList, updateRegion, toggleRegionStatus } from '@/api/system'

const loading = ref(false)
const regionList = ref([])
const dialogVisible = ref(false)
const currentRegion = ref(null)

const total = computed(() => regionList.value.length)
const enabledCount = computed(() => regionList.value.filter(r => r.status).length)

// 获取地区图标
const getRegionIcon = (code) => {
  // 这里返回后端的图标路径，实际应该从后端返回完整URL
  return `/static/regions/${code}.png`
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 加载地区列表
const loadRegions = async () => {
  loading.value = true
  try {
    const res = await getRegionList()
    console.log('API 返回数据:', res)

    // axios 拦截器已经返回 response.data，所以这里的 res 就是后端返回的数据
    if (Array.isArray(res)) {
      // 直接返回数组
      regionList.value = res
    } else if (res.results && Array.isArray(res.results)) {
      // DRF 分页格式: { count, results }
      regionList.value = res.results
    } else {
      console.error('未知的数据格式:', res)
      regionList.value = []
    }

    console.log('处理后的地区列表:', regionList.value)
  } catch (error) {
    console.error('加载地区列表失败:', error)
    ElMessage.error('加载地区列表失败')
  } finally {
    loading.value = false
  }
}

// 排序变化
const handleSortChange = ({ order, prop }) => {
  if (prop === 'sort_order') {
    regionList.value.sort((a, b) => {
      return order === 'ascending'
        ? a.sort_order - b.sort_order
        : b.sort_order - a.sort_order
    })
  }
}

// 更新排序
const handleSortUpdate = async (row) => {
  try {
    await updateRegion(row.id, { sort_order: row.sort_order })
    ElMessage.success('排序更新成功')
    loadRegions()
  } catch (error) {
    console.error('更新排序失败:', error)
    ElMessage.error('更新排序失败')
  }
}

// 切换启用状态
const handleStatusToggle = async (row) => {
  const action = row.status ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(
      `确定要${action}「${row.name}」吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    row.switching = true
    await toggleRegionStatus(row.id)
    ElMessage.success(`${action}成功`)
    loadRegions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('切换状态失败:', error)
      ElMessage.error(`${action}失败`)
      row.status = !row.status // 恢复原状态
    }
  } finally {
    row.switching = false
  }
}

// 编辑
const handleEdit = (row) => {
  currentRegion.value = { ...row }
  dialogVisible.value = true
}

// 保存编辑
const handleSave = async () => {
  try {
    await updateRegion(currentRegion.value.id, {
      sort_order: currentRegion.value.sort_order,
      status: currentRegion.value.status
    })
    ElMessage.success('保存成功')
    dialogVisible.value = false
    loadRegions()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

// 启用所有地区
const handleEnableAll = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要启用所有地区吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true
    // 批量更新
    const promises = regionList.value
      .filter(r => !r.status)
      .map(r => toggleRegionStatus(r.id))

    await Promise.all(promises)
    ElMessage.success('已启用所有地区')
    loadRegions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('启用失败:', error)
      ElMessage.error('批量启用失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRegions()
})
</script>

<style lang="scss" scoped>
.region-list {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }

  .image-slot {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background: #f5f7fa;
    color: #909399;
    font-size: 20px;
  }

  .text-info {
    color: #909399;
    font-size: 14px;
  }
}
</style>
