<template>
  <div class="region-selector">
    <!-- 顶部横向地区栏 -->
    <div class="region-tabs">
      <div class="tabs-container">
        <div
          v-for="region in displayRegions"
          :key="region.id"
          class="region-item"
          :class="{ active: currentRegion?.id === region.id }"
          @click="selectRegion(region)"
        >
          <img
            :src="getRegionIcon(region.code)"
            :alt="region.name"
            class="region-icon"
            :style="{ filter: region.status ? 'none' : 'grayscale(100%) opacity(0.5)' }"
          />
          <span class="region-name">{{ region.name }}</span>
        </div>
        <div class="region-item more" @click="showAllRegions">
          <van-icon name="apps-o" size="24" />
          <span class="region-name">全部</span>
        </div>
      </div>
    </div>

    <!-- 全部地区选择弹窗 -->
    <van-popup
      v-model:show="showPopup"
      position="bottom"
      :style="{ height: '70%' }"
      round
    >
      <div class="region-popup">
        <div class="popup-header">
          <span class="title">选择地区</span>
          <van-icon name="cross" @click="showPopup = false" />
        </div>
        <div class="popup-content">
          <div class="region-grid">
            <div
              v-for="region in allRegions"
              :key="region.id"
              class="grid-item"
              :class="{
                active: currentRegion?.id === region.id,
                disabled: !region.status
              }"
              @click="handleRegionSelect(region)"
            >
              <img
                :src="getRegionIcon(region.code)"
                :alt="region.name"
                class="grid-icon"
                :style="{ filter: region.status ? 'none' : 'grayscale(100%) opacity(0.5)' }"
              />
              <span class="grid-name">{{ region.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { showToast } from 'vant'
import { getEnabledRegions, getAllRegions } from '@/api/product'

const props = defineProps({
  modelValue: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const allRegions = ref([])
const enabledRegions = ref([])
const currentRegion = ref(props.modelValue)
const showPopup = ref(false)

// 顶部展示的前5个启用地区
const displayRegions = computed(() => {
  return enabledRegions.value.slice(0, 5)
})

// 获取地区图标路径
const getRegionIcon = (code) => {
  try {
    return new URL(`../assets/regions/${code}.png`, import.meta.url).href
  } catch (e) {
    console.error('Failed to load region icon:', code, e)
    return ''
  }
}

// 选择地区
const selectRegion = (region) => {
  if (!region.status) {
    showToast('该地区暂未开放')
    return
  }
  currentRegion.value = region
  emit('update:modelValue', region)
  emit('change', region)
}

// 显示全部地区弹窗
const showAllRegions = () => {
  showPopup.value = true
}

// 从弹窗中选择地区
const handleRegionSelect = (region) => {
  if (!region.status) {
    showToast('该地区暂未开放')
    return
  }
  selectRegion(region)
  showPopup.value = false
}

// 加载地区数据
const loadRegions = async () => {
  try {
    // 获取所有地区（含未启用，用于弹窗展示）
    const allRes = await getAllRegions()
    allRegions.value = allRes.data || []

    // 获取启用的地区（用于顶部展示）
    const enabledRes = await getEnabledRegions()
    enabledRegions.value = enabledRes.data || []

    // 如果没有当前选中地区，默认选中第一个启用的地区
    if (!currentRegion.value && enabledRegions.value.length > 0) {
      selectRegion(enabledRegions.value[0])
    }
  } catch (error) {
    console.error('加载地区数据失败:', error)
    showToast('加载地区数据失败')
  }
}

onMounted(() => {
  loadRegions()
})

// 暴露方法给父组件
defineExpose({
  loadRegions
})
</script>

<style lang="scss" scoped>
.region-selector {
  background: #fff;
}

.region-tabs {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.tabs-container {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;

  &::-webkit-scrollbar {
    display: none;
  }
}

.region-item {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.3s;

  &.active {
    .region-icon {
      border-color: #1a1a1a;
    }
    .region-name {
      color: #1a1a1a;
      font-weight: 600;
    }
  }

  &.more {
    .van-icon {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px solid #e5e5e5;
      border-radius: 50%;
    }
  }
}

.region-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.region-name {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  transition: all 0.3s;
}

.region-popup {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.popup-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;

  .title {
    font-size: 16px;
    font-weight: 600;
  }

  .van-icon {
    font-size: 20px;
    color: #999;
    cursor: pointer;
  }
}

.popup-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.region-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;

  &.active {
    background: #f7f8fa;

    .grid-icon {
      border-color: #1a1a1a;
    }
    .grid-name {
      color: #1a1a1a;
      font-weight: 600;
    }
  }

  &.disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }

  &:not(.disabled):active {
    background: #f7f8fa;
  }
}

.grid-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.grid-name {
  font-size: 13px;
  color: #666;
  text-align: center;
  word-break: break-all;
  transition: all 0.3s;
}
</style>
