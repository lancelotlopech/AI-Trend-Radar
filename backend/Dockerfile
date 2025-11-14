FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 如需别的系统依赖，可以加在这一行后面
RUN apt-get update \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先拷贝依赖文件，利用 Docker 缓存
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝剩余代码
COPY . .

# Railway / Render 都会提供 PORT 环境变量，这里给个默认值
ENV PORT=8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
