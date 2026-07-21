# 多阶段构建 - Stage 1: 基础镜像
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 多阶段构建 - Stage 2: 依赖安装
FROM base as dependencies

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 多阶段构建 - Stage 3: 最终镜像
FROM base as final

# 复制已安装的依赖
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# 创建非 root 用户
RUN useradd -m -u 1000 django && \
    mkdir -p /app/media /app/static /app/logs && \
    chown -R django:django /app

# 复制项目代码
COPY --chown=django:django . .

# 切换到非 root 用户
USER django

# 收集静态文件（在运行时执行）
# RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 确保 entrypoint.sh 有执行权限（已在 COPY . . 时复制）
RUN chmod +x /app/entrypoint.sh

# 健康检查端点（需要在 Django 中添加）
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/health/ || exit 1

# 启动命令
ENTRYPOINT ["/app/entrypoint.sh"]
