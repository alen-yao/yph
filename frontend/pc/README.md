# YPH 电商平台 - PC 端

基于 Vue 3 + Vite + Element Plus 的现代化电商平台 PC 端项目。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 4
- **UI 组件库**: Element Plus
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP 客户端**: Axios
- **样式**: SCSS

## 项目结构

```
pc/
├── public/          # 静态资源
├── src/
│   ├── api/         # API 接口
│   ├── components/  # 公共组件
│   ├── router/      # 路由配置
│   ├── stores/      # 状态管理
│   ├── styles/      # 全局样式
│   ├── utils/       # 工具函数
│   ├── views/       # 页面组件
│   ├── App.vue      # 根组件
│   └── main.js      # 入口文件
├── Dockerfile       # Docker 配置
├── nginx.conf       # Nginx 配置
└── vite.config.js   # Vite 配置
```

## 功能特性

### 已实现页面

- **首页**: 轮播图、分类导航、热门推荐、新品上市、品牌推荐
- **商品列表**: 分类筛选、价格筛选、品牌筛选、排序功能
- **商品详情**: 图片展示、商品信息、规格参数、用户评价、相关推荐
- **购物车**: 商品管理、数量调整、价格计算、批量操作
- **个人中心**: 订单管理、收藏管理、地址管理、个人信息、修改密码
- **登录页**: 用户登录、记住密码

### UI 设计特点

- 主色调: #e93323（电商红）
- 响应式布局
- 卡片式设计
- 悬停动画效果
- 渐变按钮
- 统一圆角和间距

## 开发指南

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:8080

### 生产构建

```bash
npm run build
```

### 预览构建结果

```bash
npm run preview
```

## Docker 部署

### 构建镜像

```bash
docker build -t yph-pc:latest .
```

### 运行容器

```bash
docker run -d -p 8080:80 --name yph-pc yph-pc:latest
```

## 环境变量

开发环境默认 API 代理配置在 `vite.config.js` 中：

```js
proxy: {
  '/api': {
    target: 'http://backend:8000',
    changeOrigin: true
  }
}
```

## 浏览器兼容性

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 待开发功能

- [ ] 订单确认页
- [ ] 支付页面
- [ ] 订单列表和详情
- [ ] 收藏功能
- [ ] 地址管理完整功能
- [ ] 商品搜索功能
- [ ] 用户注册功能
- [ ] 找回密码功能

## License

Copyright © 2024 YPH 电商平台
