<template>
  <div class="product-image-upload">
    <el-form :model="form" label-width="120px">
      <!-- 商品基本信息 -->
      <el-form-item label="商品名称" required>
        <el-input v-model="form.name" placeholder="请输入商品名称" />
      </el-form-item>

      <!-- 主图上传 -->
      <el-form-item label="商品主图" required>
        <div class="upload-description">
          <el-alert
            title="第一张图片将作为封面图在列表页展示，建议上传5-6张不同角度的图片"
            type="info"
            :closable="false"
            show-icon
          />
        </div>
        <el-upload
          :action="uploadUrl"
          :headers="uploadHeaders"
          :file-list="mainImageFileList"
          :on-success="handleMainImageSuccess"
          :on-remove="handleMainImageRemove"
          :before-upload="beforeImageUpload"
          list-type="picture-card"
          :limit="10"
          accept="image/*"
        >
          <el-icon><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">
              最多上传10张，单张不超过10MB，支持 JPG/PNG/GIF/WebP 格式
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 详情图上传 -->
      <el-form-item label="详情图">
        <div class="upload-description">
          <el-alert
            title="详情图将在商品详情页按顺序展示，展示产品特性、参数、使用场景等"
            type="info"
            :closable="false"
            show-icon
          />
        </div>
        <el-upload
          :action="uploadUrl"
          :headers="uploadHeaders"
          :file-list="detailImageFileList"
          :on-success="handleDetailImageSuccess"
          :on-remove="handleDetailImageRemove"
          :before-upload="beforeImageUpload"
          list-type="picture-card"
          :limit="20"
          accept="image/*"
        >
          <el-icon><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">
              最多上传20张，单张不超过10MB
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <!-- 价格信息 -->
      <el-form-item label="销售价格" required>
        <el-input-number v-model="form.price" :min="0" :precision="2" />
      </el-form-item>

      <el-form-item label="市场价格">
        <el-input-number v-model="form.market_price" :min="0" :precision="2" />
      </el-form-item>

      <!-- 提交按钮 -->
      <el-form-item>
        <el-button type="primary" @click="submitProduct" :loading="submitting">
          {{ productId ? '更新商品' : '创建商品' }}
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 预览对话框 -->
    <el-dialog v-model="previewVisible" title="图片预览" width="600px">
      <img :src="previewImageUrl" style="width: 100%" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'

// Props
const props = defineProps({
  productId: {
    type: Number,
    default: null
  }
})

// Emit
const emit = defineEmits(['success'])

// 上传配置
const uploadUrl = ref(import.meta.env.VITE_API_BASE_URL + '/api/system/upload/image/')
const token = localStorage.getItem('access_token')
const uploadHeaders = computed(() => ({
  'Authorization': `Bearer ${token}`
}))

// 表单数据
const form = reactive({
  name: '',
  category: null,
  brand: null,
  main_images: [],
  detail_images: [],
  price: 0,
  market_price: 0,
  stock: 0,
  description: '',
  state: 1
})

// 文件列表
const mainImageFileList = ref([])
const detailImageFileList = ref([])

// 预览
const previewVisible = ref(false)
const previewImageUrl = ref('')

// 提交状态
const submitting = ref(false)

// 上传前验证
const beforeImageUpload = (file) => {
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

// 主图上传成功
const handleMainImageSuccess = (response, file) => {
  if (response.url) {
    form.main_images.push(response.url)
    mainImageFileList.value.push({
      name: file.name,
      url: response.url
    })
    ElMessage.success('主图上传成功')
  } else {
    ElMessage.error('上传失败: ' + (response.error || '未知错误'))
  }
}

// 主图删除
const handleMainImageRemove = (file) => {
  const index = form.main_images.indexOf(file.url)
  if (index > -1) {
    form.main_images.splice(index, 1)
    ElMessage.success('已删除')
  }
}

// 详情图上传成功
const handleDetailImageSuccess = (response, file) => {
  if (response.url) {
    form.detail_images.push(response.url)
    detailImageFileList.value.push({
      name: file.name,
      url: response.url
    })
    ElMessage.success('详情图上传成功')
  } else {
    ElMessage.error('上传失败: ' + (response.error || '未知错误'))
  }
}

// 详情图删除
const handleDetailImageRemove = (file) => {
  const index = form.detail_images.indexOf(file.url)
  if (index > -1) {
    form.detail_images.splice(index, 1)
    ElMessage.success('已删除')
  }
}

// 提交商品
const submitProduct = async () => {
  // 验证
  if (!form.name) {
    ElMessage.error('请输入商品名称')
    return
  }
  if (form.main_images.length === 0) {
    ElMessage.error('请至少上传一张主图')
    return
  }
  if (!form.price || form.price <= 0) {
    ElMessage.error('请输入正确的销售价格')
    return
  }

  try {
    submitting.value = true

    const url = props.productId
      ? `/api/products/${props.productId}/`
      : '/api/products/'

    const method = props.productId ? 'put' : 'post'

    const response = await axios[method](url, form, {
      headers: uploadHeaders.value
    })

    ElMessage.success(props.productId ? '商品更新成功' : '商品创建成功')
    emit('success', response.data)

    if (!props.productId) {
      resetForm()
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    name: '',
    category: null,
    brand: null,
    main_images: [],
    detail_images: [],
    price: 0,
    market_price: 0,
    stock: 0,
    description: '',
    state: 1
  })
  mainImageFileList.value = []
  detailImageFileList.value = []
}

// 加载商品数据（编辑模式）
const loadProduct = async (id) => {
  try {
    const { data } = await axios.get(`/api/products/${id}/`, {
      headers: uploadHeaders.value
    })

    Object.assign(form, {
      name: data.name,
      category: data.category,
      brand: data.brand,
      main_images: data.main_images || [],
      detail_images: data.detail_images || [],
      price: parseFloat(data.price),
      market_price: parseFloat(data.market_price),
      stock: data.stock,
      description: data.description,
      state: data.state
    })

    // 设置文件列表
    mainImageFileList.value = data.main_images.map((url, index) => ({
      name: `main_image_${index + 1}`,
      url
    }))
    detailImageFileList.value = data.detail_images.map((url, index) => ({
      name: `detail_image_${index + 1}`,
      url
    }))
  } catch (error) {
    ElMessage.error('加载商品数据失败: ' + error.message)
  }
}

// 暴露方法给父组件
defineExpose({
  loadProduct,
  resetForm
})
</script>

<style scoped>
.product-image-upload {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.upload-description {
  margin-bottom: 15px;
}

.el-upload__tip {
  color: #999;
  font-size: 12px;
  margin-top: 8px;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 148px;
  height: 148px;
}

:deep(.el-upload--picture-card) {
  width: 148px;
  height: 148px;
}
</style>
