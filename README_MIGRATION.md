# 数据库迁移指南 - Docker Compose 命令行

## 快速执行步骤

### 1️⃣ 启动 MySQL 容器

```bash
docker-compose up -d mysql
```

等待 MySQL 启动（约10秒）

---

### 2️⃣ 执行主迁移脚本

```bash
docker-compose exec -T mysql mysql -u root -pyph2024! yph < backend/database_migration.sql
```

✅ 执行结果：
- 创建 `region` 表
- 插入 34 个省份数据
- 修改 `product_category` 表（删除 parent_id、level）
- 修改 `product` 表（添加 region_id）

---

### 3️⃣ 查看迁移结果

```bash
# 查看地区表
docker-compose exec mysql mysql -u root -pyph2024! yph -e "SELECT id, code, name, status FROM region LIMIT 10;"

# 查看商品表结构
docker-compose exec mysql mysql -u root -pyph2024! yph -e "SHOW COLUMNS FROM product WHERE Field = 'region_id';"

# 检查有多少商品
docker-compose exec mysql mysql -u root -pyph2024! yph -e "SELECT COUNT(*) AS total FROM product;"
```

---

### 4️⃣ 为现有商品设置地区（如果有商品数据）

#### 方案A：批量设置为北京（region_id=1）

```bash
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE product SET region_id = 1 WHERE region_id IS NULL;"
```

#### 方案B：查看并手动设置

```bash
# 查看没有地区的商品数量
docker-compose exec mysql mysql -u root -pyph2024! yph -e "SELECT COUNT(*) FROM product WHERE region_id IS NULL;"

# 稍后在 Django Admin 中手动设置
```

---

### 5️⃣ 将 region_id 改为必填（确保所有商品都有地区后）

```bash
# 先确认没有 NULL 值
docker-compose exec mysql mysql -u root -pyph2024! yph -e "SELECT COUNT(*) FROM product WHERE region_id IS NULL;"

# 如果结果是 0，执行以下命令
docker-compose exec mysql mysql -u root -pyph2024! yph -e "ALTER TABLE product MODIFY COLUMN region_id bigint NOT NULL COMMENT '所属地区';"
```

---

### 6️⃣ 启用地区

#### 方案A：启用所有地区

```bash
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET status = 1;"
```

#### 方案B：启用指定地区（如：北京、上海、广东、四川）

```bash
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET status = 1 WHERE code IN ('110000', '310000', '440000', '510000');"
```

#### 方案C：逐个启用

```bash
# 北京
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET status = 1 WHERE code = '110000';"

# 上海
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET status = 1 WHERE code = '310000';"

# 广东
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET status = 1 WHERE code = '440000';"
```

---

### 7️⃣ 验证迁移结果

```bash
# 地区统计
docker-compose exec mysql mysql -u root -pyph2024! yph -e "
SELECT 
    COUNT(*) AS total_regions,
    SUM(status) AS enabled_regions 
FROM region;"

# 查看启用的地区列表
docker-compose exec mysql mysql -u root -pyph2024! yph -e "
SELECT id, code, name, sort_order, status 
FROM region 
WHERE status = 1 
ORDER BY sort_order;"

# 各地区商品数量
docker-compose exec mysql mysql -u root -pyph2024! yph -e "
SELECT 
    r.name AS region_name,
    COUNT(p.id) AS product_count
FROM region r
LEFT JOIN product p ON r.id = p.region_id
GROUP BY r.id, r.name
ORDER BY r.sort_order
LIMIT 10;"
```

---

## 🔧 常用维护命令

### 备份数据库

```bash
docker-compose exec mysql mysqldump -u root -pyph2024! --databases yph > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 调整地区排序

```bash
# 把四川排到第一位
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET sort_order = 0 WHERE code = '510000';"
```

### 查看所有地区

```bash
docker-compose exec mysql mysql -u root -pyph2024! yph -e "SELECT * FROM region ORDER BY sort_order;"
```

### 禁用某个地区

```bash
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET status = 0 WHERE code = '710000';"
```

---

## 📝 一键执行（完整流程）

如果你的商品表是空的，可以一次性执行：

```bash
# 1. 启动 MySQL
docker-compose up -d mysql && sleep 10

# 2. 执行迁移
docker-compose exec -T mysql mysql -u root -pyph2024! yph < backend/database_migration.sql

# 3. 启用所有地区
docker-compose exec mysql mysql -u root -pyph2024! yph -e "UPDATE region SET status = 1;"

# 4. 查看结果
docker-compose exec mysql mysql -u root -pyph2024! yph -e "SELECT COUNT(*) AS total, SUM(status) AS enabled FROM region;"
```

---

## ⚠️ 注意事项

1. **密码修改**：如果你的 MySQL root 密码不是 `yph2024!`，请替换命令中的密码
2. **数据库名**：如果数据库名不是 `yph`，请替换命令中的数据库名
3. **备份数据**：执行迁移前建议先备份
4. **检查结果**：每步执行后检查输出，确认无误再继续

---

## 🚀 执行后的操作

1. **放置图标**：将 34 个省的图标放到 `frontend/h5/src/assets/regions/` 目录
   - 命名格式：`110000.png`, `120000.png`, ..., `820000.png`

2. **重启后端服务**：
   ```bash
   docker-compose restart backend
   ```

3. **访问 Django Admin**：
   ```
   http://localhost:8000/admin/
   ```

4. **添加测试数据**：
   - 在 Django Admin 中添加分类
   - 添加商品时选择地区和分类
