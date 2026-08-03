<template>
  <div class="cart-page">
    <!-- 顶部导航栏 -->
    <div class="top-nav-bar">
      <van-icon name="wap-home-o" size="20" class="nav-icon" @click="goHome" />
      <div class="nav-title">购物车</div>
      <div class="nav-right">
        <van-icon name="ellipsis" size="20" class="nav-icon" />
        <van-icon name="scan" size="20" class="nav-icon" />
      </div>
    </div>

    <!-- 购物车内容 -->
    <div class="cart-content" v-if="cartList.length > 0">
      <!-- 店铺分组 -->
      <div v-for="shop in shopGroups" :key="shop.id" class="shop-group">
        <!-- 店铺头部 -->
        <div class="shop-header">
          <van-checkbox
            v-model="shop.checked"
            @change="onShopCheckChange(shop)"
            icon-size="18px"
          />
          <van-icon name="shop-o" size="16" color="#666" style="margin-left: 8px" />
          <span class="shop-name">{{ shop.name }}</span>
          <van-button
            plain
            hairline
            size="mini"
            class="edit-btn"
            @click="toggleEdit"
          >
            编辑
          </van-button>
        </div>

        <!-- 商品列表 -->
        <div class="product-list">
          <van-swipe-cell
            v-for="item in shop.items"
            :key="item.id"
            :disabled="!isEditing"
          >
            <div class="cart-item">
              <van-checkbox
                v-model="item.checked"
                @change="onItemCheckChange"
                icon-size="18px"
              />
              <van-image
                :src="item.product_image"
                width="90"
                height="90"
                fit="cover"
                class="product-image"
                lazy-load
              >
                <template #loading>
                  <van-loading type="spinner" size="20" />
                </template>
              </van-image>

              <div class="item-info">
                <div class="item-name">{{ item.product_name }}</div>
                <div class="item-badge" v-if="item.badge">
                  <van-tag plain type="success" size="mini">{{ item.badge }}</van-tag>
                </div>
                <div class="item-footer">
                  <div class="item-price">
                    <span class="price-symbol">¥</span>
                    <span class="price-value">{{ item.price }}</span>
                  </div>
                  <van-stepper
                    v-model="item.quantity"
                    min="1"
                    theme="round"
                    button-size="22"
                    input-width="32px"
                  />
                </div>
              </div>
            </div>

            <template #right v-if="isEditing">
              <van-button
                square
                type="danger"
                text="删除"
                class="delete-button"
                @click="handleDelete(shop.id, item.id)"
              />
            </template>
          </van-swipe-cell>
        </div>
      </div>

      <!-- 底部占位，避免被结算栏遮挡 -->
      <div class="bottom-placeholder"></div>
    </div>

    <!-- 空状态 -->
    <van-empty
      v-else
      description="购物车空空如也"
      :image="require('@/assets/empty-cart.png') || 'https://via.placeholder.com/200/F5F5F5/999999?text=Empty+Cart'"
    >
      <van-button round type="primary" @click="goShopping">去逛逛</van-button>
    </van-empty>

    <!-- 底部结算栏 -->
    <van-submit-bar
      v-if="cartList.length > 0"
      :price="totalPrice"
      :disabled="checkedCount === 0"
      button-text="去结算"
      class="submit-bar"
      @submit="onSubmit"
    >
      <template #default>
        <van-checkbox
          v-model="checkedAll"
          @click="toggleCheckAll"
          icon-size="18px"
        >
          全选
        </van-checkbox>
      </template>
      <template #tip>
        <div class="submit-tip">
          <span>不含运费</span>
          <span style="margin-left: 8px">合计：<span class="total-text">¥{{ (totalPrice / 100).toFixed(2) }}</span></span>
          <van-button
            size="mini"
            plain
            hairline
            style="margin-left: 8px"
            @click="showCoupon"
          >
            优惠明细 <van-icon name="arrow-up" />
          </van-button>
        </div>
      </template>
    </van-submit-bar>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()

const isEditing = ref(false)
const checkedAll = ref(false)

// 店铺分组数据
const shopGroups = ref([
  {
    id: 1,
    name: '本来生活VIP官方店',
    checked: false,
    items: [
      {
        id: 1,
        product_name: '梅子良物·奉化水蜜桃精品12个装(单果150-200g)（云仓）',
        product_image: 'https://via.placeholder.com/180/FFE0E6/FF69B4?text=水蜜桃',
        price: 88.00,
        quantity: 1,
        checked: false,
        badge: '放心购'
      }
    ]
  }
])

// 扁平化所有商品
const cartList = computed(() => {
  return shopGroups.value.flatMap(shop => shop.items)
})

// 已选商品数量
const checkedCount = computed(() => {
  return cartList.value.filter(item => item.checked).length
})

// 总价（单位：分）
const totalPrice = computed(() => {
  return cartList.value
    .filter(item => item.checked)
    .reduce((total, item) => total + item.price * item.quantity * 100, 0)
})

// 监听商品选中状态，更新店铺选中状态
watch(
  () => cartList.value.map(item => item.checked),
  () => {
    shopGroups.value.forEach(shop => {
      shop.checked = shop.items.every(item => item.checked)
    })
    checkedAll.value = cartList.value.length > 0 && cartList.value.every(item => item.checked)
  },
  { deep: true }
)

const goHome = () => {
  router.push('/home')
}

const toggleEdit = () => {
  isEditing.value = !isEditing.value
}

// 店铺全选/取消
const onShopCheckChange = (shop) => {
  shop.items.forEach(item => {
    item.checked = shop.checked
  })
}

// 商品选中变化
const onItemCheckChange = () => {
  // 由 watch 自动更新店铺和全选状态
}

// 全选/取消全选
const toggleCheckAll = () => {
  const newChecked = !checkedAll.value
  shopGroups.value.forEach(shop => {
    shop.checked = newChecked
    shop.items.forEach(item => {
      item.checked = newChecked
    })
  })
}

// 删除商品
const handleDelete = (shopId, itemId) => {
  const shop = shopGroups.value.find(s => s.id === shopId)
  if (shop) {
    shop.items = shop.items.filter(item => item.id !== itemId)
    if (shop.items.length === 0) {
      shopGroups.value = shopGroups.value.filter(s => s.id !== shopId)
    }
    showToast('删除成功')
  }
}

// 去结算
const onSubmit = () => {
  if (checkedCount.value === 0) {
    showToast('请选择商品')
    return
  }
  showToast(`结算${checkedCount.value}件商品`)
  // router.push('/checkout')
}

// 查看优惠明细
const showCoupon = () => {
  showToast('优惠明细')
}

// 去购物
const goShopping = () => {
  router.push('/home')
}
</script>

<style lang="scss" scoped>
.cart-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 50px;
}

// 顶部导航栏
.top-nav-bar {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background: #fff;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .nav-icon {
    color: #333;
    cursor: pointer;

    &:active {
      opacity: 0.6;
    }
  }

  .nav-title {
    flex: 1;
    text-align: center;
    font-size: 17px;
    font-weight: 500;
    color: #333;
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}

// 购物车内容
.cart-content {
  padding-bottom: 100px;
}

// 店铺分组
.shop-group {
  margin-bottom: 12px;
  background: #fff;
}

// 店铺头部
.shop-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f5f5f5;

  .shop-name {
    flex: 1;
    font-size: 14px;
    color: #333;
    margin-left: 6px;
    font-weight: 500;
  }

  .edit-btn {
    font-size: 13px;
    padding: 4px 12px;
  }
}

// 商品列表
.product-list {
  .cart-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
    background: #fff;
    border-bottom: 1px solid #f5f5f5;

    .product-image {
      border-radius: 8px;
      overflow: hidden;
      background: #f5f5f5;
    }

    .item-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: 90px;
    }

    .item-name {
      font-size: 14px;
      color: #333;
      line-height: 1.5;
      margin-bottom: 4px;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .item-badge {
      margin-bottom: auto;
    }

    .item-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 8px;
    }

    .item-price {
      color: #ff4757;
      font-weight: bold;

      .price-symbol {
        font-size: 12px;
      }

      .price-value {
        font-size: 18px;
      }
    }
  }

  .delete-button {
    height: 100%;
  }
}

// 底部占位
.bottom-placeholder {
  height: 20px;
}

// 结算栏
.submit-bar {
  :deep(.van-submit-bar__bar) {
    padding: 8px 16px;
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.08);
  }

  :deep(.van-submit-bar__text) {
    flex: 1;
  }

  :deep(.van-submit-bar__button) {
    background: linear-gradient(135deg, #e93323 0%, #d32f2f 100%);
    border-radius: 20px;
    padding: 0 28px;
    font-weight: 500;
  }

  .submit-tip {
    display: flex;
    align-items: center;
    font-size: 12px;
    color: #999;
    margin-top: 4px;

    .total-text {
      color: #ff4757;
      font-weight: bold;
    }
  }
}

// 空状态
:deep(.van-empty) {
  padding: 80px 0;

  .van-empty__description {
    margin-top: 16px;
    font-size: 14px;
    color: #999;
  }

  .van-button {
    margin-top: 20px;
    padding: 0 40px;
  }
}
</style>
