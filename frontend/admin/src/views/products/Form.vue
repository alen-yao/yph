<template>
  <div>
    <el-page-header @back="handleBack" :content="isEdit ? '编辑商品' : '新增商品'" />

    <el-card style="margin-top: 20px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" maxlength="200" show-word-limit />
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

        <el-form-item label="商品品牌" prop="brand">
          <el-select v-model="form.brand" placeholder="请选择品牌" style="width: 100%">
            <el-option
              v-for="brand in brands"
              :key="brand.id"
              :label="brand.name"
              :value="brand.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="主图" prop="main_image">
          <el-input v-model="form.main_image" placeholder="请输入图片URL">
            <template #append>
              <el-button @click="handleImagePreview">预览</el-button>
            </template>
          </el-input>
          <div class="tip">示例：https://via.placeholder.com/300</div>
        </el-form-item>

        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入商品描述"
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

    <!-- 图片预览对话框 -->
    <el-dialog v-model="imagePreviewVisible" title="图片预览" width="500px">
      <div style="text-align: center">
        <el-image :src="form.main_image" fit="contain" style="max-width: 100%; max-height: 400px" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  getProductDetail,
  createProduct,
  updateProduct,
  getCategoryList,
  getBrandList
} from '@/api/product'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)
const imagePreviewVisible = ref(false)
const isEdit = ref(false)
const productId = ref(null)

const categories = ref([])
const brands = ref([])

const form = reactive({
  name: '',
  category: null,
  brand: null,
  main_image: '',
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
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  brand: [{ required: true, message: '请选择品牌', trigger: 'change' }],
  main_image: [{ required: true, message: '请输入主图URL', trigger: 'blur' }],
  price: [{ required: true, message: '请输入售价', trigger: 'blur' }]
}

const handleBack = () => {
  router.back()
}

const handleImagePreview = () => {
  if (form.main_image) {
    imagePreviewVisible.value = true
  } else {
    ElMessage.warning('请先输入图片URL')
  }
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true

  try {
    if (isEdit.value) {
      await updateProduct(productId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createProduct(form)
      ElMessage.success('创建成功')
    }
    router.push('/products')
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
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

const fetchBrands = async () => {
  try {
    const res = await getBrandList()
    brands.value = res.results || res
  } catch (error) {
    console.error('获取品牌失败', error)
  }
}

const fetchProductDetail = async (id) => {
  try {
    const res = await getProductDetail(id)
    Object.assign(form, res)
  } catch (error) {
    ElMessage.error('获取商品详情失败')
    router.back()
  }
}

onMounted(async () => {
  // 获取分类和品牌列表
  await Promise.all([fetchCategories(), fetchBrands()])

  // 如果是编辑模式，获取商品详情
  if (route.params.id) {
    isEdit.value = true
    productId.value = route.params.id
    await fetchProductDetail(productId.value)
  }
})
</script>

<style scoped>
.tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}
</style>
