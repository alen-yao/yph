<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">{{ stat.value }}</div>
            </div>
            <el-icon :size="48" :color="stat.color">
              <component :is="stat.icon" />
            </el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div>订单趋势</div>
          </template>
          <div ref="orderChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div>商品分类占比</div>
          </template>
          <div ref="categoryChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const stats = ref([
  { title: '订单总数', value: '1,234', icon: 'List', color: '#409eff' },
  { title: '商品总数', value: '567', icon: 'Goods', color: '#67c23a' },
  { title: '用户总数', value: '890', icon: 'User', color: '#e6a23c' },
  { title: '销售额', value: '¥12,345', icon: 'Money', color: '#f56c6c' }
])

const orderChartRef = ref()
const categoryChartRef = ref()

onMounted(() => {
  initOrderChart()
  initCategoryChart()
})

const initOrderChart = () => {
  const chart = echarts.init(orderChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: { type: 'value' },
    series: [{
      data: [120, 200, 150, 80, 70, 110, 130],
      type: 'line',
      smooth: true,
      itemStyle: { color: '#409eff' }
    }]
  })
}

const initCategoryChart = () => {
  const chart = echarts.init(categoryChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '60%',
      data: [
        { value: 335, name: '数码电器' },
        { value: 234, name: '服装服饰' },
        { value: 135, name: '食品生鲜' },
        { value: 154, name: '图书音像' }
      ]
    }]
  })
}
</script>

<style scoped>
.dashboard {
  height: 100%;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-title {
  color: #909399;
  font-size: 14px;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
</style>
