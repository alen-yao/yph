<template>
  <div>
    <el-card>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本设置" name="basic">
          <el-form ref="basicFormRef" :model="basicForm" label-width="150px" style="max-width: 800px">
            <el-divider content-position="left">
              <span style="font-weight: bold">网站信息</span>
            </el-divider>

            <el-form-item label="网站名称">
              <el-input v-model="basicForm.site_name" placeholder="请输入网站名称" />
            </el-form-item>

            <el-form-item label="网站Logo">
              <el-input v-model="basicForm.site_logo" placeholder="Logo URL">
                <template #append>
                  <el-button @click="previewImage(basicForm.site_logo)">预览</el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item label="网站关键词">
              <el-input v-model="basicForm.site_keywords" placeholder="请输入网站关键词，用逗号分隔" />
            </el-form-item>

            <el-form-item label="网站描述">
              <el-input
                v-model="basicForm.site_description"
                type="textarea"
                :rows="3"
                placeholder="请输入网站描述"
              />
            </el-form-item>

            <el-divider content-position="left">
              <span style="font-weight: bold">联系信息</span>
            </el-divider>

            <el-form-item label="客服电话">
              <el-input v-model="basicForm.service_phone" placeholder="400-xxx-xxxx" />
            </el-form-item>

            <el-form-item label="客服邮箱">
              <el-input v-model="basicForm.service_email" placeholder="service@example.com" />
            </el-form-item>

            <el-form-item label="公司地址">
              <el-input v-model="basicForm.company_address" placeholder="请输入公司地址" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
              <el-button @click="resetBasicSettings">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="交易设置" name="trade">
          <el-form ref="tradeFormRef" :model="tradeForm" label-width="150px" style="max-width: 800px">
            <el-divider content-position="left">
              <span style="font-weight: bold">订单设置</span>
            </el-divider>

            <el-form-item label="未支付订单自动取消">
              <el-input-number v-model="tradeForm.order_auto_cancel_time" :min="1" :step="1" />
              <span style="margin-left: 10px">分钟</span>
            </el-form-item>

            <el-form-item label="自动确认收货">
              <el-input-number v-model="tradeForm.order_auto_confirm_time" :min="1" :step="1" />
              <span style="margin-left: 10px">天</span>
            </el-form-item>

            <el-form-item label="售后期限">
              <el-input-number v-model="tradeForm.order_refund_time" :min="1" :step="1" />
              <span style="margin-left: 10px">天</span>
            </el-form-item>

            <el-divider content-position="left">
              <span style="font-weight: bold">物流设置</span>
            </el-divider>

            <el-form-item label="免运费金额">
              <el-input-number v-model="tradeForm.free_shipping_amount" :min="0" :precision="2" :step="10" />
              <span style="margin-left: 10px">元</span>
            </el-form-item>

            <el-form-item label="默认运费">
              <el-input-number v-model="tradeForm.default_shipping_fee" :min="0" :precision="2" :step="1" />
              <span style="margin-left: 10px">元</span>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveTradeSettings">保存设置</el-button>
              <el-button @click="resetTradeSettings">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="支付设置" name="payment">
          <el-alert
            title="支付配置"
            type="warning"
            :closable="false"
            style="margin-bottom: 20px"
          >
            配置微信支付、支付宝等支付方式的密钥和参数
          </el-alert>

          <el-form ref="paymentFormRef" :model="paymentForm" label-width="150px" style="max-width: 800px">
            <el-divider content-position="left">
              <span style="font-weight: bold">微信支付</span>
            </el-divider>

            <el-form-item label="微信支付">
              <el-switch v-model="paymentForm.wechat_enabled" active-text="启用" inactive-text="禁用" />
            </el-form-item>

            <el-form-item label="AppID" v-if="paymentForm.wechat_enabled">
              <el-input v-model="paymentForm.wechat_appid" placeholder="请输入AppID" />
            </el-form-item>

            <el-form-item label="商户号" v-if="paymentForm.wechat_enabled">
              <el-input v-model="paymentForm.wechat_mchid" placeholder="请输入商户号" />
            </el-form-item>

            <el-form-item label="API密钥" v-if="paymentForm.wechat_enabled">
              <el-input v-model="paymentForm.wechat_api_key" type="password" show-password placeholder="请输入API密钥" />
            </el-form-item>

            <el-divider content-position="left">
              <span style="font-weight: bold">支付宝</span>
            </el-divider>

            <el-form-item label="支付宝">
              <el-switch v-model="paymentForm.alipay_enabled" active-text="启用" inactive-text="禁用" />
            </el-form-item>

            <el-form-item label="AppID" v-if="paymentForm.alipay_enabled">
              <el-input v-model="paymentForm.alipay_appid" placeholder="请输入AppID" />
            </el-form-item>

            <el-form-item label="应用私钥" v-if="paymentForm.alipay_enabled">
              <el-input
                v-model="paymentForm.alipay_private_key"
                type="textarea"
                :rows="3"
                placeholder="请输入应用私钥"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="savePaymentSettings">保存设置</el-button>
              <el-button @click="resetPaymentSettings">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="短信设置" name="sms">
          <el-alert
            title="短信配置"
            type="info"
            :closable="false"
            style="margin-bottom: 20px"
          >
            配置短信服务商的API密钥，用于发送验证码、通知等
          </el-alert>

          <el-form ref="smsFormRef" :model="smsForm" label-width="150px" style="max-width: 800px">
            <el-form-item label="短信服务商">
              <el-select v-model="smsForm.provider" placeholder="请选择" style="width: 300px">
                <el-option label="阿里云" value="aliyun" />
                <el-option label="腾讯云" value="tencent" />
                <el-option label="华为云" value="huawei" />
              </el-select>
            </el-form-item>

            <el-form-item label="AccessKey ID">
              <el-input v-model="smsForm.access_key_id" placeholder="请输入AccessKey ID" style="width: 400px" />
            </el-form-item>

            <el-form-item label="AccessKey Secret">
              <el-input
                v-model="smsForm.access_key_secret"
                type="password"
                show-password
                placeholder="请输入AccessKey Secret"
                style="width: 400px"
              />
            </el-form-item>

            <el-form-item label="短信签名">
              <el-input v-model="smsForm.sign_name" placeholder="请输入短信签名" style="width: 300px" />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveSmsSettings">保存设置</el-button>
              <el-button @click="resetSmsSettings">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="产品分类" name="category">
          <div style="margin-bottom: 20px">
            <el-button type="primary" @click="handleAddCategory">添加分类</el-button>
          </div>

          <el-table :data="categories" border style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="分类名称" width="200" />
            <el-table-column prop="sort_order" label="排序" width="100" />
            <el-table-column label="是否显示" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_show ? 'success' : 'danger'">
                  {{ row.is_show ? '显示' : '隐藏' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_time" label="创建时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.created_time) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link @click="handleEditCategory(row)">编辑</el-button>
                <el-button type="danger" link @click="handleDeleteCategory(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="用户角色" name="role">
          <el-alert
            title="角色权限管理"
            type="info"
            :closable="false"
            style="margin-bottom: 20px"
          >
            配置不同角色的权限，管理员(is_staff=true)拥有所有权限，普通用户根据角色权限访问对应功能
          </el-alert>

          <div style="margin-bottom: 20px">
            <el-button type="primary" @click="handleAddRole">添加角色</el-button>
          </div>

          <el-table :data="roles" border style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="角色名称" width="150" />
            <el-table-column prop="description" label="角色描述" min-width="200" />
            <el-table-column label="权限模块" min-width="300">
              <template #default="{ row }">
                <el-tag
                  v-for="perm in availablePermissions.filter(p => row.permissions_data?.[p.key])"
                  :key="perm.key"
                  size="small"
                  style="margin-right: 5px; margin-bottom: 5px"
                >
                  {{ perm.label }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="用户数" width="100">
              <template #default="{ row }">
                <el-tag type="info">{{ row.user_count }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'danger'">
                  {{ row.is_active ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link @click="handleEditRole(row)">编辑</el-button>
                <el-button type="danger" link @click="handleDeleteRole(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 分类编辑对话框 -->
    <el-dialog v-model="categoryDialogVisible" :title="categoryForm.id ? '编辑分类' : '添加分类'" width="600px">
      <el-form ref="categoryFormRef" :model="categoryForm" :rules="categoryRules" label-width="120px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>

        <el-form-item label="父分类" prop="parent">
          <el-select v-model="categoryForm.parent" placeholder="请选择父分类（可选）" clearable style="width: 100%">
            <el-option
              v-for="cat in parentCategories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
              :disabled="cat.id === categoryForm.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="categoryForm.sort_order" :min="0" />
        </el-form-item>

        <el-form-item label="是否显示" prop="is_show">
          <el-switch v-model="categoryForm.is_show" />
        </el-form-item>

        <el-form-item label="分类图标" prop="icon">
          <el-input v-model="categoryForm.icon" placeholder="请输入图标URL（可选）" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="categoryDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="categorySaving" @click="handleSaveCategory">保存</el-button>
      </template>
    </el-dialog>

    <!-- 角色编辑对话框 -->
    <el-dialog v-model="roleDialogVisible" :title="roleForm.id ? '编辑角色' : '添加角色'" width="700px">
      <el-form ref="roleFormRef" :model="roleForm" :rules="roleRules" label-width="120px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>

        <el-form-item label="角色描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            :rows="2"
            placeholder="请输入角色描述"
          />
        </el-form-item>

        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="roleForm.is_active" />
        </el-form-item>

        <el-form-item label="权限配置">
          <el-card shadow="never" style="width: 100%">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center">
                <span>选择可访问的功能模块</span>
                <div>
                  <el-button size="small" @click="selectAllPermissions">全选</el-button>
                  <el-button size="small" @click="clearAllPermissions">清空</el-button>
                </div>
              </div>
            </template>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px">
              <el-checkbox
                v-for="perm in availablePermissions"
                :key="perm.key"
                v-model="roleForm.permissions[perm.key]"
                :label="perm.label"
                size="large"
              >
                <div style="display: flex; align-items: center; gap: 8px">
                  <el-icon><component :is="perm.icon" /></el-icon>
                  <span>{{ perm.label }}</span>
                </div>
              </el-checkbox>
            </div>
          </el-card>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="roleSaving" @click="handleSaveRole">保存</el-button>
      </template>
    </el-dialog>

    <!-- 图片预览对话框 -->
    <el-dialog v-model="imagePreviewVisible" title="图片预览" width="500px">
      <div style="text-align: center">
        <el-image :src="previewImageUrl" fit="contain" style="max-width: 100%; max-height: 400px" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCategoryList, createCategory, updateCategory, deleteCategory } from '@/api/product'
import { getRoleList, createRole, updateRole, deleteRole } from '@/api/system'

const activeTab = ref('basic')
const imagePreviewVisible = ref(false)
const previewImageUrl = ref('')

// 产品分类管理
const categories = ref([])
const categoryDialogVisible = ref(false)
const categorySaving = ref(false)
const categoryFormRef = ref()
const categoryForm = reactive({
  id: null,
  name: '',
  parent: null,
  sort_order: 0,
  is_show: true,
  icon: ''
})

const categoryRules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }]
}

// 父分类选项（排除当前分类）
const parentCategories = computed(() => {
  return categories.value.filter(cat => cat.id !== categoryForm.id)
})

// 用户角色管理
const roles = ref([])
const roleDialogVisible = ref(false)
const roleSaving = ref(false)
const roleFormRef = ref()
const roleForm = reactive({
  id: null,
  name: '',
  description: '',
  permissions: {},
  is_active: true
})

const roleRules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }]
}

// 可用的权限模块
const availablePermissions = [
  { key: 'dashboard', label: '仪表盘', icon: 'Odometer' },
  { key: 'users', label: '用户管理', icon: 'User' },
  { key: 'products', label: '商品管理', icon: 'Goods' },
  { key: 'orders', label: '订单管理', icon: 'Document' },
  { key: 'marketing', label: '营销管理', icon: 'TrendCharts' },
  { key: 'settings', label: '系统设置', icon: 'Setting' }
]

// 基本设置
const basicFormRef = ref()
const basicForm = reactive({
  site_name: 'YPH电商平台',
  site_logo: 'https://via.placeholder.com/200x80?text=LOGO',
  site_keywords: '电商,购物,商城',
  site_description: 'YPH电商平台 - 您的在线购物首选',
  service_phone: '400-xxx-xxxx',
  service_email: 'service@yph.com',
  company_address: '北京市朝阳区xxx大厦'
})

// 交易设置
const tradeFormRef = ref()
const tradeForm = reactive({
  order_auto_cancel_time: 30,
  order_auto_confirm_time: 7,
  order_refund_time: 7,
  free_shipping_amount: 99,
  default_shipping_fee: 10
})

// 支付设置
const paymentFormRef = ref()
const paymentForm = reactive({
  wechat_enabled: false,
  wechat_appid: '',
  wechat_mchid: '',
  wechat_api_key: '',
  alipay_enabled: false,
  alipay_appid: '',
  alipay_private_key: ''
})

// 短信设置
const smsFormRef = ref()
const smsForm = reactive({
  provider: 'aliyun',
  access_key_id: '',
  access_key_secret: '',
  sign_name: ''
})

const previewImage = (url) => {
  if (url) {
    previewImageUrl.value = url
    imagePreviewVisible.value = true
  } else {
    ElMessage.warning('请先输入图片URL')
  }
}

const saveBasicSettings = () => {
  ElMessage.success('基本设置保存成功（演示）')
  console.log('基本设置:', basicForm)
}

const resetBasicSettings = () => {
  ElMessage.info('已重置基本设置')
}

const saveTradeSettings = () => {
  ElMessage.success('交易设置保存成功（演示）')
  console.log('交易设置:', tradeForm)
}

const resetTradeSettings = () => {
  ElMessage.info('已重置交易设置')
}

const savePaymentSettings = () => {
  ElMessage.success('支付设置保存成功（演示）')
  console.log('支付设置:', paymentForm)
}

const resetPaymentSettings = () => {
  ElMessage.info('已重置支付设置')
}

const saveSmsSettings = () => {
  ElMessage.success('短信设置保存成功（演示）')
  console.log('短信设置:', smsForm)
}

const resetSmsSettings = () => {
  ElMessage.info('已重置短信设置')
}

// 分类管理方法
const fetchCategories = async () => {
  try {
    const res = await getCategoryList()
    categories.value = res.results || res
  } catch (error) {
    ElMessage.error('获取分类列表失败')
  }
}

const handleAddCategory = () => {
  Object.assign(categoryForm, {
    id: null,
    name: '',
    parent: null,
    sort_order: 0,
    is_show: true,
    icon: ''
  })
  categoryDialogVisible.value = true
}

const handleEditCategory = (row) => {
  Object.assign(categoryForm, {
    id: row.id,
    name: row.name,
    parent: row.parent,
    sort_order: row.sort_order,
    is_show: row.is_show,
    icon: row.icon || ''
  })
  categoryDialogVisible.value = true
}

const handleSaveCategory = async () => {
  await categoryFormRef.value.validate()
  categorySaving.value = true

  try {
    const data = {
      name: categoryForm.name,
      parent: categoryForm.parent || null,
      sort_order: categoryForm.sort_order,
      is_show: categoryForm.is_show,
      icon: categoryForm.icon || null,
      level: categoryForm.parent ? 2 : 1
    }

    if (categoryForm.id) {
      await updateCategory(categoryForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await createCategory(data)
      ElMessage.success('添加成功')
    }

    categoryDialogVisible.value = false
    await fetchCategories()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || error.message || '操作失败')
  } finally {
    categorySaving.value = false
  }
}

const handleDeleteCategory = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除分类"${row.name}"吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteCategory(row.id)
    ElMessage.success('删除成功')
    await fetchCategories()
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    ElMessage.error(error.response?.data?.error || error.message || '删除失败')
  }
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  return new Date(dateTime).toLocaleString('zh-CN')
}

// 角色管理方法
const fetchRoles = async () => {
  try {
    const res = await getRoleList()
    roles.value = res.results || res
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  }
}

const handleAddRole = () => {
  Object.assign(roleForm, {
    id: null,
    name: '',
    description: '',
    permissions: {},
    is_active: true
  })
  // 默认全部勾选
  availablePermissions.forEach(p => {
    roleForm.permissions[p.key] = true
  })
  roleDialogVisible.value = true
}

const handleEditRole = (row) => {
  Object.assign(roleForm, {
    id: row.id,
    name: row.name,
    description: row.description,
    permissions: row.permissions_data || {},
    is_active: row.is_active
  })
  roleDialogVisible.value = true
}

const handleSaveRole = async () => {
  await roleFormRef.value.validate()
  roleSaving.value = true

  try {
    const data = {
      name: roleForm.name,
      description: roleForm.description,
      permissions: roleForm.permissions,
      is_active: roleForm.is_active
    }

    if (roleForm.id) {
      await updateRole(roleForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await createRole(data)
      ElMessage.success('添加成功')
    }

    roleDialogVisible.value = false
    await fetchRoles()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || error.message || '操作失败')
  } finally {
    roleSaving.value = false
  }
}

const handleDeleteRole = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除角色"${row.name}"吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteRole(row.id)
    ElMessage.success('删除成功')
    await fetchRoles()
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    ElMessage.error(error.response?.data?.error || error.message || '删除失败')
  }
}

const selectAllPermissions = () => {
  availablePermissions.forEach(p => {
    roleForm.permissions[p.key] = true
  })
}

const clearAllPermissions = () => {
  availablePermissions.forEach(p => {
    roleForm.permissions[p.key] = false
  })
}

onMounted(() => {
  fetchCategories()
  fetchRoles()
})
</script>

<style scoped>
.el-divider {
  margin: 30px 0 20px;
}
</style>
