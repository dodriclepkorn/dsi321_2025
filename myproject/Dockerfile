FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    gcc \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

# ลองติดตั้ง prefect ตรง ๆ ก่อน แล้วติดตั้ง dependencies อื่น ๆ
RUN pip install prefect==2.13.0 duckduckgo_search typing_extensions

# แสดงเวอร์ชัน prefect เพื่อยืนยันการติดตั้ง
RUN prefect version

# ติดตั้ง dependencies อื่น ๆ ถ้ามีใน requirements.txt (ยกเว้น prefect)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data

CMD ["prefect", "deployment", "run", "scrape_news"]
