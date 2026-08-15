#!/bin/bash

# ============================================
# 数据库迁移脚本 - 使用 docker-compose 执行
# ============================================

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# MySQL 配置（从 docker-compose.yml 读取）
MYSQL_CONTAINER="yph-mysql"
MYSQL_DATABASE="${MYSQL_DATABASE:-yph}"
MYSQL_USER="${MYSQL_USER:-yph}"
MYSQL_PASSWORD="${MYSQL_PASSWORD:-yph123456}"
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD:-yph2024!}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  YPH 数据库迁移工具${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 docker-compose 是否运行
echo -e "${YELLOW}→ 检查 MySQL 容器状态...${NC}"
if ! docker ps | grep -q "$MYSQL_CONTAINER"; then
    echo -e "${RED}✗ MySQL 容器未运行，正在启动...${NC}"
    docker-compose up -d mysql
    echo -e "${YELLOW}→ 等待 MySQL 启动（最多 30 秒）...${NC}"
    sleep 10
else
    echo -e "${GREEN}✓ MySQL 容器正在运行${NC}"
fi

# 等待 MySQL 就绪
echo -e "${YELLOW}→ 等待 MySQL 就绪...${NC}"
for i in {1..30}; do
    if docker exec $MYSQL_CONTAINER mysqladmin ping -h localhost -u root -p"$MYSQL_ROOT_PASSWORD" &> /dev/null; then
        echo -e "${GREEN}✓ MySQL 已就绪${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}✗ MySQL 启动超时${NC}"
        exit 1
    fi
    echo -n "."
    sleep 1
done
echo ""

# 备份当前数据库（可选）
echo -e "${YELLOW}→ 是否需要备份数据库？ (y/n)${NC}"
read -r backup_choice
if [[ "$backup_choice" == "y" || "$backup_choice" == "Y" ]]; then
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    echo -e "${YELLOW}→ 正在备份到 $BACKUP_FILE ...${NC}"
    docker exec $MYSQL_CONTAINER mysqldump \
        -u root -p"$MYSQL_ROOT_PASSWORD" \
        --databases "$MYSQL_DATABASE" \
        --single-transaction \
        --quick \
        --lock-tables=false \
        > "$BACKUP_FILE"
    echo -e "${GREEN}✓ 备份完成: $BACKUP_FILE${NC}"
fi

# 复制 SQL 文件到容器
echo -e "${YELLOW}→ 复制迁移脚本到容器...${NC}"
docker cp backend/database_migration.sql $MYSQL_CONTAINER:/tmp/
docker cp backend/post_migration.sql $MYSQL_CONTAINER:/tmp/
echo -e "${GREEN}✓ 文件复制完成${NC}"

# 执行主迁移脚本
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  执行主迁移脚本${NC}"
echo -e "${GREEN}========================================${NC}"
docker exec -i $MYSQL_CONTAINER mysql \
    -u root -p"$MYSQL_ROOT_PASSWORD" \
    "$MYSQL_DATABASE" \
    < backend/database_migration.sql

echo -e "${GREEN}✓ 主迁移脚本执行完成${NC}"
echo ""

# 检查现有商品数据
echo -e "${YELLOW}→ 检查现有商品数据...${NC}"
PRODUCT_COUNT=$(docker exec $MYSQL_CONTAINER mysql \
    -u root -p"$MYSQL_ROOT_PASSWORD" \
    -N -B "$MYSQL_DATABASE" \
    -e "SELECT COUNT(*) FROM product;" 2>/dev/null || echo "0")

echo -e "${GREEN}✓ 发现 $PRODUCT_COUNT 个商品${NC}"

if [ "$PRODUCT_COUNT" -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}  处理现有商品数据${NC}"
    echo -e "${YELLOW}========================================${NC}"

    # 检查有多少商品没有地区
    NO_REGION_COUNT=$(docker exec $MYSQL_CONTAINER mysql \
        -u root -p"$MYSQL_ROOT_PASSWORD" \
        -N -B "$MYSQL_DATABASE" \
        -e "SELECT COUNT(*) FROM product WHERE region_id IS NULL;")

    echo -e "${YELLOW}发现 $NO_REGION_COUNT 个商品没有设置地区${NC}"

    if [ "$NO_REGION_COUNT" -gt 0 ]; then
        echo -e "${YELLOW}请选择处理方式:${NC}"
        echo "  1) 批量设置为北京市 (region_id=1)"
        echo "  2) 跳过，稍后手动在 Django Admin 中设置"
        read -p "请输入选项 (1/2): " region_choice

        if [ "$region_choice" == "1" ]; then
            docker exec $MYSQL_CONTAINER mysql \
                -u root -p"$MYSQL_ROOT_PASSWORD" \
                "$MYSQL_DATABASE" \
                -e "UPDATE product SET region_id = 1 WHERE region_id IS NULL;"
            echo -e "${GREEN}✓ 已设置默认地区为北京市${NC}"
        else
            echo -e "${YELLOW}⚠ 跳过设置，请稍后手动处理${NC}"
        fi
    fi
fi

# 询问是否将 region_id 改为 NOT NULL
if [ "$PRODUCT_COUNT" -gt 0 ]; then
    echo ""
    NULL_COUNT=$(docker exec $MYSQL_CONTAINER mysql \
        -u root -p"$MYSQL_ROOT_PASSWORD" \
        -N -B "$MYSQL_DATABASE" \
        -e "SELECT COUNT(*) FROM product WHERE region_id IS NULL;")

    if [ "$NULL_COUNT" -eq 0 ]; then
        echo -e "${YELLOW}→ 是否将 region_id 字段改为必填 (NOT NULL)? (y/n)${NC}"
        read -r notnull_choice
        if [[ "$notnull_choice" == "y" || "$notnull_choice" == "Y" ]]; then
            docker exec $MYSQL_CONTAINER mysql \
                -u root -p"$MYSQL_ROOT_PASSWORD" \
                "$MYSQL_DATABASE" \
                -e "ALTER TABLE product MODIFY COLUMN region_id bigint NOT NULL COMMENT '所属地区';"
            echo -e "${GREEN}✓ region_id 字段已改为必填${NC}"
        fi
    else
        echo -e "${RED}⚠ 还有 $NULL_COUNT 个商品没有地区，无法设置为必填${NC}"
    fi
fi

# 启用地区
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  地区管理${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}→ 是否需要启用地区？ (y/n)${NC}"
read -r enable_choice

if [[ "$enable_choice" == "y" || "$enable_choice" == "Y" ]]; then
    echo ""
    echo "请选择启用方式:"
    echo "  1) 启用所有地区"
    echo "  2) 启用指定地区 (如: 110000,310000,440000)"
    echo "  3) 跳过，稍后在 Django Admin 中设置"
    read -p "请输入选项 (1/2/3): " enable_option

    case $enable_option in
        1)
            docker exec $MYSQL_CONTAINER mysql \
                -u root -p"$MYSQL_ROOT_PASSWORD" \
                "$MYSQL_DATABASE" \
                -e "UPDATE region SET status = 1;"
            echo -e "${GREEN}✓ 已启用所有地区${NC}"
            ;;
        2)
            echo -n "请输入地区代码（逗号分隔，如: 110000,310000,440000）: "
            read -r region_codes
            docker exec $MYSQL_CONTAINER mysql \
                -u root -p"$MYSQL_ROOT_PASSWORD" \
                "$MYSQL_DATABASE" \
                -e "UPDATE region SET status = 1 WHERE code IN ('${region_codes//,/\',\'}');"
            echo -e "${GREEN}✓ 已启用指定地区${NC}"
            ;;
        3)
            echo -e "${YELLOW}⚠ 跳过启用，请稍后在 Django Admin 中设置${NC}"
            ;;
    esac
fi

# 显示迁移结果
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  迁移结果${NC}"
echo -e "${GREEN}========================================${NC}"

# 地区统计
docker exec $MYSQL_CONTAINER mysql \
    -u root -p"$MYSQL_ROOT_PASSWORD" \
    -t "$MYSQL_DATABASE" \
    -e "SELECT
        COUNT(*) AS total_regions,
        SUM(status) AS enabled_regions
    FROM region;"

# 启用的地区列表
echo ""
echo -e "${GREEN}已启用的地区:${NC}"
docker exec $MYSQL_CONTAINER mysql \
    -u root -p"$MYSQL_ROOT_PASSWORD" \
    -t "$MYSQL_DATABASE" \
    -e "SELECT id, code, name, sort_order
    FROM region
    WHERE status = 1
    ORDER BY sort_order
    LIMIT 10;"

# 每个地区的商品数量
echo ""
echo -e "${GREEN}各地区商品数量:${NC}"
docker exec $MYSQL_CONTAINER mysql \
    -u root -p"$MYSQL_ROOT_PASSWORD" \
    -t "$MYSQL_DATABASE" \
    -e "SELECT
        r.name AS region_name,
        COUNT(p.id) AS product_count
    FROM region r
    LEFT JOIN product p ON r.id = p.region_id
    GROUP BY r.id, r.name
    ORDER BY r.sort_order
    LIMIT 10;"

# 清理临时文件
docker exec $MYSQL_CONTAINER rm -f /tmp/database_migration.sql /tmp/post_migration.sql

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  迁移完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}下一步操作:${NC}"
echo "  1. 将 34 个省的图标放到: frontend/h5/src/assets/regions/"
echo "  2. 启动后端服务: docker-compose up -d backend"
echo "  3. 访问 Django Admin 管理地区和商品"
echo ""
