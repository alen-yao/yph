#!/bin/bash
# 快速添加字段脚本

set -e

echo "=========================================="
echo "快速添加数据库字段"
echo "=========================================="
echo ""

# 读取表名
read -p "请输入表名（如 user, product）: " table_name
if [ -z "$table_name" ]; then
    echo "❌ 表名不能为空"
    exit 1
fi

# 读取字段名
read -p "请输入字段名（如 avatar_url）: " field_name
if [ -z "$field_name" ]; then
    echo "❌ 字段名不能为空"
    exit 1
fi

# 读取字段类型
echo "选择字段类型:"
echo "  1) VARCHAR(50)"
echo "  2) VARCHAR(255)"
echo "  3) INT"
echo "  4) DECIMAL(10,2)"
echo "  5) TEXT"
echo "  6) DATETIME"
echo "  7) TINYINT (0/1, 用于布尔值)"
echo "  8) 自定义"
read -p "请选择 (1-8): " type_choice

case $type_choice in
    1) field_type="VARCHAR(50)" ;;
    2) field_type="VARCHAR(255)" ;;
    3) field_type="INT" ;;
    4) field_type="DECIMAL(10,2)" ;;
    5) field_type="TEXT" ;;
    6) field_type="DATETIME" ;;
    7) field_type="TINYINT(1)" ;;
    8)
        read -p "请输入自定义类型（如 VARCHAR(100)）: " field_type
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

# 读取默认值
read -p "请输入默认值（直接回车表示 NULL）: " default_value
if [ -z "$default_value" ]; then
    default_clause="DEFAULT NULL"
else
    if [ "$field_type" == "TEXT" ] || [[ $field_type == VARCHAR* ]]; then
        default_clause="DEFAULT '$default_value'"
    else
        default_clause="DEFAULT $default_value"
    fi
fi

# 读取注释
read -p "请输入字段说明（COMMENT）: " comment

# 生成 SQL
sql="ALTER TABLE \`$table_name\` ADD COLUMN \`$field_name\` $field_type $default_clause"
if [ ! -z "$comment" ]; then
    sql="$sql COMMENT '$comment'"
fi
sql="$sql;"

echo ""
echo "=========================================="
echo "将执行以下 SQL:"
echo "=========================================="
echo "$sql"
echo ""
read -p "确认执行？(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "已取消"
    exit 0
fi

# 执行 SQL
echo "执行 SQL..."
docker-compose exec mysql mysql -u yph -pyph123456 -D yph -e "$sql"

if [ $? -eq 0 ]; then
    echo "✅ 字段添加成功！"

    # 保存 SQL 到文件
    date_str=$(date +%Y%m%d)
    filename="sql/migrations/${date_str}_add_${table_name}_${field_name}.sql"
    echo "-- 添加 $table_name 表的 $field_name 字段" > "$filename"
    echo "-- 日期: $(date +%Y-%m-%d)" >> "$filename"
    echo "" >> "$filename"
    echo "$sql" >> "$filename"
    echo "📝 SQL 已保存到: $filename"

    echo ""
    echo "下一步:"
    echo "1. 在 models.py 中添加对应的字段定义"
    echo "2. 重启后端: docker-compose restart backend"
else
    echo "❌ 执行失败"
    exit 1
fi
