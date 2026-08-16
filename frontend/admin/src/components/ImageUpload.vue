<template>
  <div class="image-upload">
    <draggable
      v-model="imageList"
      item-key="uid"
      class="image-list"
      handle=".image-item"
      @end="handleDragEnd"
    >
      <template #item="{ element, index }">
        <div class="image-item">
          <el-image
            :src="getImageUrl(element.url)"
            fit="cover"
            :preview-src-list="previewList"
            :initial-index="index"
          />
          <div class="image-overlay">
            <el-icon class="drag-handle"><Rank /></el-icon>
            <el-icon class="delete-icon" @click="handleRemove(index)"><Delete /></el-icon>
          </div>
          <div v-if="index === 0 && showCoverBadge" class="cover-badge">封面</div>
        </div>
      </template>
    </draggable>

    <el-upload
      v-if="imageList.length < limit"
      class="image-uploader"
      :action="uploadUrl"
      :headers="uploadHeaders"
      :data="uploadData"
      :show-file-list="false"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      accept="image/*"
    >
      <div class="upload-trigger">
        <el-icon><Plus /></el-icon>
        <div class="upload-text">{{ uploadText }}</div>
      </div>
    </el-upload>

    <div v-if="tip" class="tip">{{ tip }}</div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Delete, Rank } from '@element-plus/icons-vue'
import draggable from 'vuedraggable'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  limit: {
    type: Number,
    default: 5
  },
  uploadText: {
    type: String,
    default: '上传图片'
  },
  tip: {
    type: String,
    default: ''
  },
  showCoverBadge: {
    type: Boolean,
    default: false
  },
  folder: {
    type: String,
    default: 'products'
  }
})

const emit = defineEmits(['update:modelValue'])

const userStore = useUserStore()
const imageList = ref([])
const isInternalUpdate = ref(false) // 防止循环更新的标志

// 上传接口配置
const uploadUrl = '/api/v1/system/upload/image/'
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))
const uploadData = computed(() => ({
  folder: props.folder
}))

// 监听 modelValue 变化
watch(() => props.modelValue, (newVal) => {
  if (isInternalUpdate.value) {
    isInternalUpdate.value = false
    return
  }

  const newUrls = newVal || []
  const currentUrls = imageList.value.map(item => item.url)

  // 只有当数据真的不同时才更新
  if (JSON.stringify(newUrls) !== JSON.stringify(currentUrls)) {
    imageList.value = newUrls.map((url, index) => ({
      uid: `img_${index}_${url.substring(url.length - 10)}`, // 使用稳定的 uid
      url
    }))
  }
}, { immediate: true })

// 监听 imageList 变化，同步到父组件
watch(imageList, (newVal) => {
  isInternalUpdate.value = true
  emit('update:modelValue', newVal.map(item => item.url))
}, { deep: true })

// 获取完整图片URL
const getImageUrl = (key) => {
  if (!key) return ''
  // 如果已经是完整URL，直接返回
  if (key.startsWith('http://') || key.startsWith('https://')) {
    return key
  }
  // 否则拼接 MinIO 公开访问地址
  return `http://localhost:9000/yph-products/${key}`
}

// 预览列表
const previewList = computed(() => {
  return imageList.value.map(item => getImageUrl(item.url))
})

// 上传前校验
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB!')
    return false
  }
  return true
}

// 上传成功
const handleSuccess = (response) => {
  if (response.key) {
    const key = response.key
    imageList.value.push({
      uid: `img_${imageList.value.length}_${key.substring(key.length - 10)}`,
      url: key  // 保存 MinIO key
    })
    ElMessage.success('上传成功')
  } else {
    ElMessage.error('上传失败：' + (response.error || '未知错误'))
  }
}

// 上传失败
const handleError = (error) => {
  console.error('上传失败:', error)
  ElMessage.error('上传失败，请重试')
}

// 删除图片
const handleRemove = (index) => {
  imageList.value.splice(index, 1)
}

// 拖拽结束
const handleDragEnd = () => {
  // 拖拽会自动更新 imageList，watch 会同步到父组件
}
</script>

<style lang="scss" scoped>
.image-upload {
  .image-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .image-item {
    position: relative;
    width: 120px;
    height: 120px;
    border: 1px solid #dcdfe6;
    border-radius: 6px;
    overflow: hidden;
    cursor: move;

    :deep(.el-image) {
      width: 100%;
      height: 100%;
    }

    .image-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
      opacity: 0;
      transition: opacity 0.3s;
    }

    &:hover .image-overlay {
      opacity: 1;
    }

    .drag-handle,
    .delete-icon {
      font-size: 20px;
      color: white;
      cursor: pointer;
    }

    .delete-icon:hover {
      color: #f56c6c;
    }

    .cover-badge {
      position: absolute;
      top: 5px;
      left: 5px;
      background: #409eff;
      color: white;
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 3px;
    }
  }

  .image-uploader {
    display: inline-block;

    .upload-trigger {
      width: 120px;
      height: 120px;
      border: 1px dashed #dcdfe6;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        border-color: #409eff;
        color: #409eff;
      }

      .el-icon {
        font-size: 28px;
        margin-bottom: 5px;
      }

      .upload-text {
        font-size: 12px;
        color: #999;
      }
    }
  }

  .tip {
    font-size: 12px;
    color: #999;
    margin-top: 5px;
  }
}
</style>
