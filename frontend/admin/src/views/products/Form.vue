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

        <el-form-item label="主图" prop="main_images">
          <div class="image-upload-container">
            <div class="image-list">
              <draggable
                v-model="form.main_images"
                item-key="index"
                class="image-draggable"
                handle=".image-item"
              >
                <template #item="{ element, index }">
                  <div class="image-item">
                    <el-image
                      :src="element"
                      fit="cover"
                      :preview-src-list="form.main_images"
                      :initial-index="index"
                    />
                    <div class="image-overlay">
                      <el-icon class="drag-handle"><Rank /></el-icon>
                      <el-icon class="delete-icon" @click="handleRemoveMainImage(index)"><Delete /></el-icon>
                    </div>
                    <div v-if="index === 0" class="cover-badge">封面</div>
                  </div>
                </template>
              </draggable>

              <div v-if="form.main_images.length < 5" class="image-upload" @click="handleAddMainImage">
                <el-icon><Plus /></el-icon>
                <div class="upload-text">添加主图</div>
              </div>
            </div>
            <div class="tip">
              最多上传5张，第一张为封面图，拖动可调整顺序
            </div>
          </div>
        </el-form-item>

        <el-form-item label="详情图" prop="detail_images">
          <div class="image-upload-container">
            <div class="image-list">
              <draggable
                v-model="form.detail_images"
                item-key="index"
                class="image-draggable"
                handle=".image-item"
              >
                <template #item="{ element, index }">
                  <div class="image-item">
                    <el-image
                      :src="element"
                      fit="cover"
                      :preview-src-list="form.detail_images"
                      :initial-index="index"
                    />
                    <div class="image-overlay">
                      <el-icon class="drag-handle"><Rank /></el-icon>
                      <el-icon class="delete-icon" @click="handleRemoveDetailImage(index)"><Delete /></el-icon>
                    </div>
                  </div>
                </template>
              </draggable>

              <div v-if="form.detail_images.length < 20" class="image-upload" @click="handleAddDetailImage">
                <el-icon><Plus /></el-icon>
                <div class="upload-text">添加详情图</div>
              </div>
            </div>
            <div class="tip">
              最多上传20张，拖动可调整顺序，详情页按顺序展示
            </div>
          </div>
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

    <!-- 图片URL输入对话框 -->
    <el-dialog v-model="imageInputVisible" :title="currentImageType === 'main' ? '添加主图' : '添加详情图'" width="500px">
      <el-input
        v-model="imageUrl"
        placeholder="请输入图片URL"
        clearable
      >
        <template #prepend>URL</template>
      </el-input>
      <div class="tip" style="margin-top: 10px">
        示例：https://via.placeholder.com/800x800
      </div>
      <div v-if="imageUrl" style="margin-top: 20px; text-align: center">
        <el-image :src="imageUrl" fit="contain" style="max-width: 100%; max-height: 300px" />
      </div>
      <template #footer>
        <el-button @click="imageInputVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmAddImage" :disabled="!imageUrl">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Delete, Rank } from '@element-plus/icons-vue'
import draggable from 'vuedraggable'
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
const imageInputVisible = ref(false)
const imageUrl = ref('')
const currentImageType = ref('main') // 'main' or 'detail'
const isEdit = ref(false)
const productId = ref(null)

const categories = ref([])
const brands = ref([])

const form = reactive({
  name: '',
  category: null,
  brand: null,
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
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  brand: [{ required: true, message: '请选择品牌', trigger: 'change' }],
  main_images: [
    { required: true, message: '请至少添加一张主图', trigger: 'change' },
    { type: 'array', min: 1, message: '请至少添加一张主图', trigger: 'change' }
  ],
  price: [{ required: true, message: '请输入售价', trigger: 'blur' }]
}

const handleBack = () => {
  router.back()
}

const handleAddMainImage = () => {
  if (form.main_images.length >= 5) {
    ElMessage.warning('主图最多5张')
    return
  }
  currentImageType.value = 'main'
  imageUrl.value = ''
  imageInputVisible.value = true
}

const handleAddDetailImage = () => {
  if (form.detail_images.length >= 20) {
    ElMessage.warning('详情图最多20张')
    return
  }
  currentImageType.value = 'detail'
  imageUrl.value = ''
  imageInputVisible.value = true
}

const handleConfirmAddImage = () => {
  if (!imageUrl.value) {
    ElMessage.warning('请输入图片URL')
    return
  }

  if (currentImageType.value === 'main') {
    form.main_images.push(imageUrl.value)
  } else {
    form.detail_images.push(imageUrl.value)
  }

  imageInputVisible.value = false
  imageUrl.value = ''
}

const handleRemoveMainImage = (index) => {
  form.main_images.splice(index, 1)
}

const handleRemoveDetailImage = (index) => {
  form.detail_images.splice(index, 1)
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
    // 确保图片字段是数组
    form.main_images = Array.isArray(res.main_images) ? res.main_images : []
    form.detail_images = Array.isArray(res.detail_images) ? res.detail_images : []
    // 其他字段
    form.name = res.name
    form.category = res.category
    form.brand = res.brand
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

.image-upload-container {
  width: 100%;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-draggable {
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
}

.image-item :deep(.el-image) {
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

.image-item:hover .image-overlay {
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

.image-upload {
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
}

.image-upload:hover {
  border-color: #409eff;
  color: #409eff;
}

.image-upload .el-icon {
  font-size: 28px;
  margin-bottom: 5px;
}

.upload-text {
  font-size: 12px;
  color: #999;
}
</style>
