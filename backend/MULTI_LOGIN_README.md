# YPH电商多登录系统使用文档

## 功能概述

本系统支持三种登录方式：
1. **账号密码登录**（PC端）
2. **手机验证码登录**（PC端、移动端）
3. **微信登录**（小程序、H5）

---

## 一、环境配置

### 1. 安装依赖包

```bash
cd backend
pip install -r requirements.txt

# 如果需要阿里云短信功能（生产环境）
pip install aliyun-python-sdk-core

# 如果需要微信登录
pip install requests
```

### 2. 数据库迁移

由于添加了微信登录字段，需要执行数据库迁移：

```bash
cd backend
python manage.py makemigrations users
python manage.py migrate
```

**迁移内容：**
- 添加 `wechat_openid` 字段（微信OpenID，唯一索引）
- 添加 `wechat_unionid` 字段（微信UnionID）

### 3. 环境变量配置

在 `.env` 文件或环境变量中配置以下参数：

#### 阿里云短信配置
```bash
# 阿里云短信配置
ALIYUN_SMS_ACCESS_KEY_ID=你的AccessKeyId
ALIYUN_SMS_ACCESS_KEY_SECRET=你的AccessKeySecret
ALIYUN_SMS_SIGN_NAME=YPH电商
ALIYUN_SMS_TEMPLATE_LOGIN=SMS_123456  # 登录验证码模板
ALIYUN_SMS_TEMPLATE_REGISTER=SMS_123457  # 注册验证码模板
ALIYUN_SMS_TEMPLATE_RESET=SMS_123458  # 重置密码模板
```

#### 微信配置
```bash
# 微信小程序配置
WECHAT_MINIPROGRAM_APP_ID=你的小程序AppId
WECHAT_MINIPROGRAM_APP_SECRET=你的小程序AppSecret

# 微信H5配置（公众号）
WECHAT_H5_APP_ID=你的公众号AppId
WECHAT_H5_APP_SECRET=你的公众号AppSecret
```

---

## 二、API接口说明

### 1. 统一登录接口

**接口地址：** `POST /api/users/auth/multi-login/`

**权限要求：** 无需认证（AllowAny）

#### 1.1 账号密码登录

```json
{
  "login_type": "password",
  "username": "13800138000",
  "password": "123456"
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user_id": 1,
    "mobile": "13800138000",
    "nickname": "张三",
    "avatar": "/media/users/avatars/xxx.jpg"
  }
}
```

#### 1.2 手机验证码登录

**步骤1：发送验证码**
```bash
POST /api/users/auth/send-sms/
```

```json
{
  "mobile": "13800138000",
  "code_type": "login"
}
```

**步骤2：验证码登录**
```json
{
  "login_type": "sms",
  "mobile": "13800138000",
  "code": "123456"
}
```

**特点：**
- 如果手机号不存在，自动注册新用户
- 验证码有效期：5分钟
- 发送频率限制：60秒

#### 1.3 微信登录

**场景1：已绑定用户直接登录**
```json
{
  "login_type": "wechat",
  "wechat_code": "wx_code_from_frontend",
  "app_type": "miniprogram"
}
```

**场景2：首次登录需绑定手机**

首次请求会返回：
```json
{
  "code": 1001,
  "message": "首次微信登录，请绑定手机号",
  "data": {
    "need_bind": true,
    "openid": "oxxxxxxxxxxxxxx"
  }
}
```

绑定手机号：
```json
{
  "login_type": "wechat",
  "wechat_code": "wx_code_from_frontend",
  "app_type": "miniprogram",
  "bind_mobile": "13800138000",
  "bind_code": "123456"
}
```

**app_type 选项：**
- `miniprogram` - 微信小程序
- `h5` - 微信公众号H5

---

### 2. 发送短信验证码接口

**接口地址：** `POST /api/users/auth/send-sms/`

**请求参数：**
```json
{
  "mobile": "13800138000",
  "code_type": "login"
}
```

**code_type 选项：**
- `login` - 登录验证码
- `register` - 注册验证码
- `reset` - 重置密码验证码

**响应示例：**
```json
{
  "code": 200,
  "message": "验证码已发送",
  "data": {
    "mobile": "13800138000",
    "expire_time": 300
  }
}
```

---

## 三、前端集成示例

### 3.1 小程序微信登录

```javascript
// 1. 获取微信授权code
wx.login({
  success: (res) => {
    const wxCode = res.code;
    
    // 2. 调用后端登录接口
    wx.request({
      url: 'https://your-api.com/api/users/auth/multi-login/',
      method: 'POST',
      data: {
        login_type: 'wechat',
        wechat_code: wxCode,
        app_type: 'miniprogram'
      },
      success: (response) => {
        if (response.data.code === 200) {
          // 登录成功，保存token
          const token = response.data.data.access;
          wx.setStorageSync('token', token);
        } else if (response.data.code === 1001) {
          // 需要绑定手机号
          // 跳转到绑定手机页面
          wx.navigateTo({
            url: '/pages/bind-phone/index?openid=' + response.data.data.openid
          });
        }
      }
    });
  }
});
```

### 3.2 手机验证码登录

```javascript
// 1. 发送验证码
sendSMS() {
  wx.request({
    url: 'https://your-api.com/api/users/auth/send-sms/',
    method: 'POST',
    data: {
      mobile: this.data.mobile,
      code_type: 'login'
    },
    success: (res) => {
      if (res.data.code === 200) {
        wx.showToast({ title: '验证码已发送' });
        // 开始倒计时
        this.startCountdown();
      }
    }
  });
}

// 2. 验证码登录
login() {
  wx.request({
    url: 'https://your-api.com/api/users/auth/multi-login/',
    method: 'POST',
    data: {
      login_type: 'sms',
      mobile: this.data.mobile,
      code: this.data.code
    },
    success: (res) => {
      if (res.data.code === 200) {
        wx.setStorageSync('token', res.data.data.access);
        wx.showToast({ title: '登录成功' });
      }
    }
  });
}
```

---

## 四、开发环境说明

### 开发模式（DEBUG=True）

在开发环境下，短信验证码不会真正发送，而是在控制台打印：

```
========== 短信验证码 ==========
手机号: 13800138000
验证码: 123456
类型: login
有效期: 5分钟
================================
```

这样可以方便测试，无需消耗短信额度。

### 生产模式（DEBUG=False）

在生产环境下，系统会调用阿里云短信SDK真正发送短信。

---

## 五、数据库字段说明

User模型新增字段：

| 字段名 | 类型 | 说明 | 索引 |
|--------|------|------|------|
| wechat_openid | CharField(100) | 微信OpenID | unique=True |
| wechat_unionid | CharField(100) | 微信UnionID | 无 |

---

## 六、常见问题

### Q1: 微信登录失败，返回"微信登录失败，请重试"

**可能原因：**
1. `wechat_code` 已过期（有效期5分钟）
2. 微信配置（APP_ID、APP_SECRET）不正确
3. 网络问题导致无法访问微信API

**解决方案：**
- 检查settings.py中的微信配置
- 确保code是最新获取的
- 查看日志文件了解详细错误

### Q2: 短信验证码收不到

**可能原因：**
1. 开发环境下不会真正发送短信（查看控制台）
2. 阿里云短信配置不正确
3. 手机号被拉黑或停机

**解决方案：**
- 检查DEBUG模式
- 验证阿里云AccessKey是否正确
- 查看阿里云短信发送记录

### Q3: 验证码总是提示"错误或已过期"

**可能原因：**
1. Redis配置不正确，验证码未成功保存
2. 验证码已使用或过期（5分钟）
3. 手机号输入不一致

**解决方案：**
- 检查Redis连接是否正常
- 确保5分钟内使用验证码
- 确保发送和验证使用相同手机号

---

## 七、安全建议

1. **生产环境必须设置 DEBUG=False**
2. **定期更换 SECRET_KEY**
3. **使用HTTPS协议**
4. **限制短信发送频率（已实现60秒限制）**
5. **监控异常登录行为**
6. **定期更新依赖包版本**

---

## 八、后续优化建议

1. ✅ 添加登录历史记录（已有UserLoginHistory模型）
2. ⏳ 实现图形验证码防刷
3. ⏳ 添加登录失败次数限制
4. ⏳ 支持更多第三方登录（支付宝、QQ等）
5. ⏳ 实现账号绑定/解绑功能
6. ⏳ 添加登录日志审计

---

## 九、技术支持

如有问题，请查看：
- 项目日志：`backend/logs/yph.log`
- Django文档：https://docs.djangoproject.com/
- DRF文档：https://www.django-rest-framework.org/
