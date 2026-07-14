<template>
  <div class="cart-page">
    <div class="container">
      <h2 class="page-title">购物车</h2>

      <div v-if="cartItems.length > 0" class="cart-content">
        <el-table :data="cartItems" border style="width: 100%">
          <el-table-column type="selection" width="55" />
          <el-table-column label="商品信息" min-width="400">
            <template #default="{ row }">
              <div class="product-info">
                <img :src="row.image" alt="" class="product-image" />
                <div class="product-text">
                  <div class="product-name">{{ row.name }}</div>
                  <div class="product-spec">{{ row.spec }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="price" label="单价" width="150" align="center">
            <template #default="{ row }">
              <div class="price">{{ row.price }}</div>
            </template>
          </el-table-column>
          <el-table-column label="数量" width="180" align="center">
            <template #default="{ row }">
              <el-input-number v-model="row.quantity" :min="1" :max="99" size="small" />
            </template>
          </el-table-column>
          <el-table-column label="小计" width="150" align="center">
            <template #default="{ row }">
              <div class="price">{{ (row.price * row.quantity).toFixed(2) }}</div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" align="center">
            <template #default="{ row }">
              <el-button type="danger" link @click="removeItem(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="cart-footer">
          <div class="footer-left">
            <el-checkbox v-model="selectAll" @change="handleSelectAll">全选</el-checkbox>
            <el-button link @click="clearCart">清空购物车</el-button>
          </div>
          <div class="footer-right">
            <div class="total-info">
              <span>已选商品 <em>{{ selectedCount }}</em> 件</span>
              <span class="total-price">
                合计：<span class="price price-large">{{ totalPrice }}</span>
              </span>
            </div>
            <el-button type="primary" size="large" @click="checkout">结算</el-button>
          </div>
        </div>
      </div>

      <el-empty v-else description="购物车是空的" :image-size="200">
        <el-button type="primary" @click="$router.push('/products')">去逛逛</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const selectAll = ref(false)
const cartItems = ref([
  {
    id: 1,
    name: 'YPH 精选商品 1 - 高品质正品保障',
    spec: '颜色：红色 规格：标准版',
    image: 'https://via.placeholder.com/80x80/E8F4F8/E93323?text=1',
    price: 299.00,
    quantity: 1,
    selected: false
  },
  {
    id: 2,
    name: 'YPH 精选商品 2 - 高品质正品保障',
    spec: '颜色：蓝色 规格：豪华版',
    image: 'https://via.placeholder.com/80x80/E8F4F8/1890FF?text=2',
    price: 499.00,
    quantity: 2,
    selected: false
  }
])

const selectedCount = computed(() => {
  return cartItems.value.filter(item => item.selected).reduce((sum, item) => sum + item.quantity, 0)
})

const totalPrice = computed(() => {
  return cartItems.value
    .filter(item => item.selected)
    .reduce((sum, item) => sum + item.price * item.quantity, 0)
    .toFixed(2)
})

const handleSelectAll = () => {
  cartItems.value.forEach(item => {
    item.selected = selectAll.value
  })
}

const removeItem = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const index = cartItems.value.indexOf(row)
    if (index > -1) {
      cartItems.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  } catch {}
}

const clearCart = async () => {
  try {
    await ElMessageBox.confirm('确定要清空购物车吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    cartItems.value = []
    ElMessage.success('购物车已清空')
  } catch {}
}

const checkout = () => {
  if (selectedCount.value === 0) {
    ElMessage.warning('请选择要结算的商品')
    return
  }
  ElMessage.success('前往结算')
  // TODO: 跳转到订单确认页
}
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';

.cart-page {
  padding: 20px 0 60px;
  min-height: 70vh;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid $theme-color;
}

.cart-content {
  background: $bg-color-white;
  border-radius: $border-radius-lg;
  padding: 20px;
}

.product-info {
  display: flex;
  gap: 12px;

  .product-image {
    width: 80px;
    height: 80px;
    border-radius: $border-radius-base;
    object-fit: cover;
  }

  .product-text {
    flex: 1;

    .product-name {
      font-size: $font-size-base;
      color: $text-color-primary;
      margin-bottom: 8px;
      line-height: 1.5;
    }

    .product-spec {
      font-size: $font-size-sm;
      color: $text-color-tertiary;
    }
  }
}

.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 20px;
  background: $bg-color-light;
  border-radius: $border-radius-base;

  .footer-left {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .footer-right {
    display: flex;
    align-items: center;
    gap: 24px;

    .total-info {
      display: flex;
      align-items: baseline;
      gap: 24px;
      font-size: $font-size-base;

      em {
        color: $theme-color;
        font-style: normal;
        font-weight: 600;
      }

      .total-price {
        font-size: $font-size-lg;

        .price {
          font-size: 28px;
        }
      }
    }
  }
}
</style>
