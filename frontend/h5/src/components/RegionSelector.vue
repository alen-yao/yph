<template>
  <div class="region-selector">
    <!-- 顶部横向地区栏 -->
    <div class="region-tabs">
      <div class="tabs-container" ref="tabsContainerRef">
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
          <van-icon name="apps-o" />
          <span class="region-name">全部</span>
        </div>
      </div>
    </div>

    <!-- 全部地区选择弹窗 -->
    <van-popup
      v-model:show="showPopup"
      position="top"
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
import { ref, computed, onMounted, nextTick } from 'vue'
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
const tabsContainerRef = ref(null)

// 顶部展示所有启用地区（可左右滑动）
const displayRegions = computed(() => {
  return enabledRegions.value
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
  console.log('RegionSelector - selectRegion 调用:', region)
  if (!region.status) {
    showToast('该地区暂未开放')
    return
  }
  currentRegion.value = region
  console.log('RegionSelector - emit change:', region)
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
  // 滚动到选中的地区
  scrollToRegion(region)
}

// 滚动到选中的地区
const scrollToRegion = async (region) => {
  await nextTick()
  if (!tabsContainerRef.value) return

  const index = enabledRegions.value.findIndex(r => r.id === region.id)
  if (index === -1) return

  const container = tabsContainerRef.value
  const regionItems = container.querySelectorAll('.region-item:not(.more)')

  if (regionItems[index]) {
    const item = regionItems[index]
    const containerWidth = container.offsetWidth
    const itemLeft = item.offsetLeft
    const itemWidth = item.offsetWidth

    // 计算滚动位置，使选中的地区居中显示
    const scrollLeft = itemLeft - (containerWidth / 2) + (itemWidth / 2)

    container.scrollTo({
      left: scrollLeft,
      behavior: 'smooth'
    })
  }
}

// 加载地区数据
const loadRegions = async () => {
  try {
    // 获取所有地区（含未启用，用于弹窗展示）
    const allRes = await getAllRegions()
    // 响应拦截器已经返回了 response.data，所以直接使用
    allRegions.value = allRes || []
    console.log('RegionSelector - 所有地区:', allRegions.value)

    // 获取启用的地区（用于顶部展示）
    const enabledRes = await getEnabledRegions()
    // 响应拦截器已经返回了 response.data，所以直接使用
    enabledRegions.value = enabledRes || []
    console.log('RegionSelector - 启用的地区:', enabledRegions.value)

    // 如果没有当前选中地区，默认选中第一个启用的地区
    if (!currentRegion.value && enabledRegions.value.length > 0) {
      console.log('RegionSelector - 自动选中第一个地区')
      selectRegion(enabledRegions.value[0])
    } else {
      console.log('RegionSelector - 已有选中地区或没有可用地区', {
        currentRegion: currentRegion.value,
        enabledRegionsLength: enabledRegions.value.length
      })
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
  flex-shrink: 0;
  background: #fff;
  border-bottom: 1px solid #f2f2f2;
}

.region-tabs {
  padding: 10px 12px 8px;
  background: #fff;
}

.tabs-container {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 0 2px 1px;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}

.region-item {
  flex: 0 0 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: #666;
  cursor: pointer;

  &.active {
    .region-icon {
      border-color: #e93323;
    }
    .region-name {
      color: #e93323;
      font-weight: 600;
    }
  }

  &.more {
    flex: 0 0 50px;

    .van-icon {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid #e5e5e5;
      border-radius: 50%;
      background: #fafafa;
      font-size: 18px;
      color: #666;
    }

    .region-name {
      max-width: 50px;
      font-size: 11px;
    }
  }
}

.region-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  background: #f7f7f7;
}

.region-name {
  max-width: 60px;
  font-size: 11px;
  line-height: 1.2;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 400;
}

.region-popup {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.popup-header {
  padding: 14px 16px;
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
  padding: 14px;
}

.region-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 10px 6px;
  border-radius: 8px;

  &.active {
    background: #fff4f2;

    .grid-icon {
      border-color: #e93323;
    }
    .grid-name {
      color: #e93323;
      font-weight: 600;
    }
  }

  &.disabled {
    cursor: not-allowed;
    opacity: 0.55;
  }

  &:not(.disabled):active {
    background: #f7f7f7;
  }
}

.grid-icon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
}

.grid-name {
  font-size: 12px;
  color: #666;
  text-align: center;
  line-height: 1.3;
  word-break: break-all;
}
</style>
