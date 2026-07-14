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
      </el-tabs>
    </el-card>

    <!-- 图片预览对话框 -->
    <el-dialog v-model="imagePreviewVisible" title="图片预览" width="500px">
      <div style="text-align: center">
        <el-image :src="previewImageUrl" fit="contain" style="max-width: 100%; max-height: 400px" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('basic')
const imagePreviewVisible = ref(false)
const previewImageUrl = ref('')

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
</script>

<style scoped>
.el-divider {
  margin: 30px 0 20px;
}
</style>
