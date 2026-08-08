# MinIO Bucket 公开访问设置指南

## 为什么要设置为公开？

设置bucket为公开访问后：
- ✅ 图片URL永不过期
- ✅ 无需生成临时签名URL
- ✅ 前端可直接访问图片
- ✅ 适合存储商品图片、头像等公开资源

## 方法1：使用Python脚本（最简单）

### 自动设置（推荐）

**首次运行项目时会自动设置**：

```bash
cd backend
python test_minio.py
```

该脚本会：
1. 检查bucket是否存在
2. 如果不存在，创建bucket并设置为公开
3. 如果已存在，也会设置为公开

### 手动强制设置

如果需要手动设置或重新设置：

```bash
cd backend
python set_minio_public.py
```

输出示例：
```
============================================================
设置 MinIO Bucket 为公开访问
============================================================

当前配置:
  Endpoint: localhost:9000
  Bucket: yph-products
  Public URL: http://localhost:9000

检查bucket是否存在...
✓ Bucket 'yph-products' 存在

设置bucket为公开读取...
✓ 成功设置bucket为公开访问!

公开策略已应用:
  - 任何人都可以通过URL直接访问bucket中的文件
  - 无需认证，URL永不过期
  - 适合存储商品图片等公开资源
```

## 方法2：通过MinIO Web控制台

### 步骤：

1. **打开MinIO控制台**
   ```
   浏览器访问：http://localhost:9001
   ```

2. **登录**
   ```
   用户名: minioadmin
   密码: minioadmin
   ```

3. **进入Buckets管理**
   - 点击左侧菜单 "Buckets"
   - 找到 `yph-products` bucket
   - 点击进入

4. **设置访问策略**
   - 点击 "Access Policy" 或 "Anonymous" 标签页
   - 选择 "Public" 或设置为 "Download"
   - 或者点击 "Add Access Rule"，设置：
     - Prefix: `*` （所有文件）
     - Access: `readonly` 或 `download`

5. **保存设置**
   - 点击 "Set" 或 "Save"

### 验证设置

在浏览器中直接访问图片URL（无需登录）：
```
http://localhost:9000/yph-products/products/2026/08/test.jpg
```

如果能直接看到图片，说明设置成功。

## 方法3：使用mc命令行工具

### 安装mc

**Windows:**
```bash
# 下载mc.exe
curl -O https://dl.min.io/client/mc/release/windows-amd64/mc.exe

# 或使用Chocolatey
choco install minio-client
```

**Linux/Mac:**
```bash
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-bin/mc

chmod +x $HOME/minio-bin/mc
export PATH=$PATH:$HOME/minio-bin/
```

### 配置mc

```bash
# 添加MinIO服务器
mc alias set local http://localhost:9000 minioadmin minioadmin

# 验证连接
mc admin info local
```

### 设置bucket为公开

```bash
# 设置为公开下载（只读）
mc anonymous set download local/yph-products

# 或设置为完全公开（读写，不推荐）
mc anonymous set public local/yph-products

# 查看当前策略
mc anonymous get local/yph-products
```

### 验证策略

```bash
# 查看bucket策略
mc anonymous get local/yph-products

# 输出应该显示：
# Access permission for `local/yph-products` is `download`
```

## 方法4：直接设置Bucket Policy（高级）

使用mc或API直接设置JSON策略：

### 创建策略文件 `public-policy.json`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": ["*"]
            },
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::yph-products/*"
            ]
        }
    ]
}
```

### 应用策略

```bash
mc anonymous set-json public-policy.json local/yph-products
```

## 验证bucket是否公开

### 方法1：上传测试文件

```bash
cd backend
python test_minio.py
```

脚本会上传测试图片并打印URL，在浏览器中访问该URL验证。

### 方法2：直接访问URL

如果已有文件，直接在浏览器中访问：
```
http://localhost:9000/yph-products/products/2026/08/abc123.jpg
```

- ✅ **成功**：直接显示图片，无需登录
- ❌ **失败**：提示 `AccessDenied` 或需要认证

### 方法3：使用curl测试

```bash
curl -I http://localhost:9000/yph-products/products/2026/08/test.jpg

# 成功输出：
# HTTP/1.1 200 OK
# Content-Type: image/jpeg
```

## 生产环境注意事项

### 1. 使用HTTPS

```bash
# .env配置
MINIO_SECURE=True
MINIO_PUBLIC_URL=https://minio.yourdomain.com
```

### 2. 修改默认凭证

```bash
# 不要在生产环境使用默认的 minioadmin/minioadmin
MINIO_ACCESS_KEY=your-secure-access-key
MINIO_SECRET_KEY=your-secure-secret-key-min-8-chars
```

### 3. 配置域名访问

如果使用自定义域名，需要配置反向代理（Nginx）：

```nginx
server {
    listen 443 ssl;
    server_name cdn.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. 配置CDN加速

建议在生产环境使用CDN：
- 阿里云OSS CDN
- 腾讯云COS CDN
- Cloudflare CDN

```bash
MINIO_PUBLIC_URL=https://cdn.yourdomain.com
```

## 故障排除

### 问题1：AccessDenied错误

**症状：** 访问图片URL时提示 `AccessDenied`

**解决：**
```bash
# 重新设置为公开
python set_minio_public.py

# 或使用mc
mc anonymous set download local/yph-products
```

### 问题2：连接MinIO失败

**症状：** 脚本报错 `MinIO 存储桶操作失败`

**解决：**
1. 检查MinIO是否运行：
   ```bash
   # 检查进程
   netstat -ano | findstr :9000
   
   # 或访问
   http://localhost:9001
   ```

2. 检查配置文件 `.env`：
   ```bash
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   ```

### 问题3：Bucket不存在

**症状：** 提示 bucket 不存在

**解决：**
```bash
# 运行测试脚本会自动创建bucket
python test_minio.py

# 或使用mc创建
mc mb local/yph-products
mc anonymous set download local/yph-products
```

### 问题4：URL无法访问

**症状：** 浏览器访问图片URL超时或连接失败

**解决：**
1. 检查防火墙是否开放9000端口
2. 检查 `MINIO_PUBLIC_URL` 配置是否正确
3. 确认MinIO监听的地址（不要只监听127.0.0.1）

## 最佳实践

### 开发环境
- ✅ 使用公开bucket
- ✅ HTTP连接（无需证书）
- ✅ 默认凭证即可
- ✅ 本地访问 `http://localhost:9000`

### 生产环境
- ✅ 使用公开bucket（商品图片等公开资源）
- ✅ HTTPS连接（必须）
- ✅ 强密码凭证
- ✅ 配置CDN加速
- ✅ 定期备份
- ⚠️ 敏感数据用私有bucket

## 相关文档

- [MinIO图片存储方案](./MINIO_IMAGE_STORAGE.md)
- [MinIO官方文档](https://min.io/docs/minio/linux/administration/identity-access-management/policy-based-access-control.html)
