<template>
  <div>
    <el-page-header @back="handleBack" :content="isEdit ? '编辑商品' : '新增商品'" />

    <el-card style="margin-top: 20px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" maxlength="200" show-word-limit />
        </el-form-item>

        <el-form-item label="所属地区" prop="region">
          <el-select v-model="form.region" placeholder="请选择地区" style="width: 100%">
            <el-option
              v-for="region in regions"
              :key="region.id"
              :label="region.name"
              :value="region.id"
              :disabled="!region.status"
            >
              <div style="display: flex; align-items: center; gap: 8px">
                <el-image
                  :src="`http://localhost/static/regions/${region.code}.png`"
                  fit="cover"
                  style="width: 20px; height: 20px; border-radius: 50%"
                  :style="{ filter: region.status ? 'none' : 'grayscale(100%) opacity(0.5)' }"
                >
                  <template #error>
                    <div style="width: 20px; height: 20px"></div>
                  </template>
                </el-image>
                <span>{{ region.name }}</span>
                <span v-if="!region.status" style="color: #ccc; margin-left: 10px">(未启用)</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="商品分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="主图" prop="main_images">
          <ImageUpload
            v-model="form.main_images"
            :limit="5"
            upload-text="上传主图"
            tip="最多上传5张，第一张为封面图，拖动可调整顺序"
            :show-cover-badge="true"
            folder="products"
          />
        </el-form-item>

        <el-form-item label="详情图" prop="detail_images">
          <ImageUpload
            v-model="form.detail_images"
            :limit="20"
            upload-text="上传详情图"
            tip="最多上传20张，拖动可调整顺序，详情页按顺序展示"
            folder="products"
          />
        </el-form-item>

        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入商品描述（可选）"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="售价" prop="price">
              <el-input-number v-model="form.price" :min="0.01" :precision="2" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="市场价" prop="market_price">
              <el-input-number v-model="form.market_price" :min="0" :precision="2" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="成本价" prop="cost_price">
              <el-input-number v-model="form.cost_price" :min="0" :precision="2" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="库存" prop="stock">
              <el-input-number v-model="form.stock" :min="0" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="排序" prop="sort_order">
              <el-input-number v-model="form.sort_order" :min="0" :step="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="状态" prop="state">
              <el-select v-model="form.state" style="width: 100%">
                <el-option label="下架" :value="0" />
                <el-option label="上架" :value="1" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="商品标签">
          <el-checkbox v-model="form.is_recommend">推荐</el-checkbox>
          <el-checkbox v-model="form.is_new">新品</el-checkbox>
          <el-checkbox v-model="form.is_hot">热销</el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交</el-button>
          <el-button @click="handleBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import ImageUpload from '@/components/ImageUpload.vue'
import {
  getProductDetail,
  createProduct,
  updateProduct,
  getCategoryList
} from '@/api/product'
import { getRegionList } from '@/api/system'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)
const isEdit = ref(false)
const productId = ref(null)

const categories = ref([])
const regions = ref([])

const form = reactive({
  name: '',
  region: null,
  category: null,
  main_images: [],
  detail_images: [],
  description: '',
  price: 0,
  market_price: 0,
  cost_price: 0,
  stock: 0,
  state: 1,
  sort_order: 0,
  is_recommend: false,
  is_new: false,
  is_hot: false
})

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  region: [{ required: true, message: '请选择所属地区', trigger: 'change' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  main_images: [
    { required: true, message: '请至少添加一张主图', trigger: 'change' },
    { type: 'array', min: 1, message: '请至少添加一张主图', trigger: 'change' }
  ],
  price: [{ required: true, message: '请输入售价', trigger: 'blur' }]
}

const handleBack = () => {
  router.back()
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    const submitData = {
      ...form,
      // 确保空数组也发送
      main_images: form.main_images.length > 0 ? form.main_images : [],
      detail_images: form.detail_images.length > 0 ? form.detail_images : []
    }

    if (isEdit.value) {
      await updateProduct(productId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      await createProduct(submitData)
      ElMessage.success('创建成功')
    }
    router.push('/products')
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

const fetchRegions = async () => {
  try {
    const res = await getRegionList()
    // axios 拦截器已经返回 response.data
    if (Array.isArray(res)) {
      regions.value = res
    } else if (res.results && Array.isArray(res.results)) {
      regions.value = res.results
    } else {
      regions.value = []
    }
  } catch (error) {
    console.error('获取地区失败', error)
  }
}

const fetchCategories = async () => {
  try {
    const res = await getCategoryList()
    categories.value = res.results || res
  } catch (error) {
    console.error('获取分类失败', error)
  }
}


// 从 URL 提取 MinIO key
const extractKeyFromUrl = (url) => {
  if (!url) return ''
  // 如果已经是 key（不是完整URL），直接返回
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    return url
  }
  // 从完整URL中提取 key: http://localhost:9000/yph-products/products/2026/08/xxx.jpg
  // 提取 products/2026/08/xxx.jpg 部分
  const match = url.match(/\/yph-products\/(.+)$/)
  return match ? match[1] : url
}

const fetchProductDetail = async (id) => {
  try {
    const res = await getProductDetail(id)
    // 后端返回的是完整URL，需要转换回 key 用于编辑
    form.main_images = Array.isArray(res.main_images)
      ? res.main_images.map(extractKeyFromUrl)
      : []
    form.detail_images = Array.isArray(res.detail_images)
      ? res.detail_images.map(extractKeyFromUrl)
      : []
    // 其他字段
    form.name = res.name
    form.region = res.region
    form.category = res.category
    form.description = res.description || ''
    form.price = res.price
    form.market_price = res.market_price
    form.cost_price = res.cost_price
    form.stock = res.stock
    form.state = res.state
    form.sort_order = res.sort_order
    form.is_recommend = res.is_recommend
    form.is_new = res.is_new
    form.is_hot = res.is_hot
  } catch (error) {
    ElMessage.error('获取商品详情失败')
    router.back()
  }
}

onMounted(async () => {
  // 获取地区和分类列表
  await Promise.all([fetchRegions(), fetchCategories()])

  // 如果是编辑模式，获取商品详情
  if (route.params.id) {
    isEdit.value = true
    productId.value = route.params.id
    await fetchProductDetail(productId.value)
  }
})
</script>

<style scoped>
/* 样式已移至 ImageUpload 组件 */
</style>
