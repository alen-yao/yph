<template>
  <div class="cart">
    <van-nav-bar title="购物车" />

    <van-checkbox-group v-model="checkedGoods">
      <van-swipe-cell v-for="item in cartList" :key="item.id">
        <div class="cart-item">
          <van-checkbox :name="item.id" />
          <van-image :src="item.product_image" width="80" height="80" />
          <div class="item-info">
            <div class="item-name">{{ item.product_name }}</div>
            <div class="item-price">¥{{ item.price }}</div>
            <van-stepper v-model="item.quantity" min="1" />
          </div>
        </div>
        <template #right>
          <van-button square type="danger" text="删除" class="delete-button" @click="handleDelete(item.id)" />
        </template>
      </van-swipe-cell>
    </van-checkbox-group>

    <van-submit-bar
      :price="totalPrice"
      button-text="结算"
      @submit="onSubmit"
    >
      <van-checkbox v-model="checkedAll" @click="toggleCheckAll">全选</van-checkbox>
    </van-submit-bar>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { showToast } from 'vant'

const checkedGoods = ref([])
const checkedAll = ref(false)

const cartList = ref([
  {
    id: 1,
    product_name: '商品名称1',
    product_image: 'https://via.placeholder.com/80',
    price: 99.00,
    quantity: 1
  },
  {
    id: 2,
    product_name: '商品名称2',
    product_image: 'https://via.placeholder.com/80',
    price: 199.00,
    quantity: 2
  }
])

const totalPrice = computed(() => {
  return cartList.value
    .filter(item => checkedGoods.value.includes(item.id))
    .reduce((total, item) => total + item.price * item.quantity * 100, 0)
})

const toggleCheckAll = () => {
  checkedGoods.value = checkedAll.value ? [] : cartList.value.map(item => item.id)
}

const handleDelete = (id) => {
  cartList.value = cartList.value.filter(item => item.id !== id)
  showToast('删除成功')
}

const onSubmit = () => {
  if (checkedGoods.value.length === 0) {
    showToast('请选择商品')
    return
  }
  showToast('去结算')
}
</script>

<style scoped>
.cart {
  height: 100vh;
  background: #f7f8fa;
}

.cart-item {
  display: flex;
  gap: 10px;
  padding: 15px;
  background: #fff;
  align-items: center;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-name {
  font-size: 14px;
  color: #323233;
}

.item-price {
  color: #ff6b6b;
  font-size: 16px;
  font-weight: bold;
}

.delete-button {
  height: 100%;
}
</style>
