# YPH 电商系统 API 文档

## 项目概述

YPH 是一个基于 Python Django + DRF 的电商系统，结合了 Dailyfresh-B2C 的简洁架构和 ModulithShop 的完整业务功能。

## API 基础信息

- **基础 URL**: `http://localhost:8000/api/v1/`
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON

## 认证说明

大部分API需要在请求头中携带JWT token：

```
Authorization: Bearer <your_access_token>
```

## 主要模块

### 1. 用户模块 (/users/)

#### 用户注册
- **URL**: `/api/v1/users/users/register/`
- **Method**: POST
- **权限**: 公开
- **参数**:
  ```json
  {
    "mobile": "13800138000",
    "password": "password123",
    "password_confirm": "password123",
    "code": "123456"
  }
  ```

#### 用户登录
- **URL**: `/api/v1/users/login/`
- **Method**: POST
- **权限**: 公开
- **参数**:
  ```json
  {
    "username": "13800138000",
    "password": "password123"
  }
  ```
- **返回**:
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user_id": 1,
    "mobile": "13800138000",
    "nickname": "用户昵称"
  }
  ```

#### 获取用户信息
- **URL**: `/api/v1/users/users/profile/`
- **Method**: GET
- **权限**: 需要登录

#### 修改用户信息
- **URL**: `/api/v1/users/users/profile/`
- **Method**: PUT
- **权限**: 需要登录

#### 收货地址管理
- **列表**: GET `/api/v1/users/addresses/`
- **创建**: POST `/api/v1/users/addresses/`
- **更新**: PUT `/api/v1/users/addresses/{id}/`
- **删除**: DELETE `/api/v1/users/addresses/{id}/`
- **设为默认**: POST `/api/v1/users/addresses/{id}/set-default/`

#### 用户消息
- **列表**: GET `/api/v1/users/messages/`
- **标记已读**: POST `/api/v1/users/messages/{id}/mark-read/`
- **全部已读**: POST `/api/v1/users/messages/mark-all-read/`
- **未读数量**: GET `/api/v1/users/messages/unread-count/`

### 2. 商品模块 (/products/)

#### 商品分类
- **列表**: GET `/api/v1/products/categories/`
- **详情**: GET `/api/v1/products/categories/{id}/`

#### 商品品牌
- **列表**: GET `/api/v1/products/brands/`
- **详情**: GET `/api/v1/products/brands/{id}/`

#### 商品列表
- **URL**: GET `/api/v1/products/products/`
- **参数**:
  - `category`: 分类ID
  - `brand`: 品牌ID
  - `keyword`: 搜索关键词
  - `ordering`: 排序 (price, -price, sales_count, -created_time)
  - `page`: 页码
  - `page_size`: 每页数量

#### 商品详情
- **URL**: GET `/api/v1/products/products/{id}/`

#### 商品评论
- **URL**: GET `/api/v1/products/comments/?product_id={id}`

### 3. 交易模块 (/trade/)

#### 购物车
- **列表**: GET `/api/v1/trade/cart/`
- **添加**: POST `/api/v1/trade/cart/`
- **更新数量**: PUT `/api/v1/trade/cart/{id}/`
- **删除**: DELETE `/api/v1/trade/cart/{id}/`

#### 订单
- **列表**: GET `/api/v1/trade/orders/`
- **详情**: GET `/api/v1/trade/orders/{id}/`
- **创建**: POST `/api/v1/trade/orders/`
- **取消**: POST `/api/v1/trade/orders/{id}/cancel/`

### 4. 营销模块 (/marketing/)

- 优惠券管理
- 活动管理
- 秒杀活动
- 拼团活动

### 5. 支付模块 (/payment/)

- 微信支付
- 支付宝支付
- 余额支付

### 6. 店铺模块 (/shops/)

- 店铺信息
- 商品收藏
- 浏览历史
- 搜索历史

## 通用响应格式

### 成功响应
```json
{
  "count": 100,
  "next": "http://api.example.com/products/?page=2",
  "previous": null,
  "results": [...]
}
```

### 错误响应
```json
{
  "detail": "错误信息"
}
```

## 状态码说明

- `200 OK`: 请求成功
- `201 Created`: 创建成功
- `204 No Content`: 删除成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未认证
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器错误

## 在线文档

启动项目后访问：
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
