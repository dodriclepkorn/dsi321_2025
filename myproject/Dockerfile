# Dockerfile
FROM python:3.10-slim

# ติดตั้งไลบรารีพื้นฐาน
RUN apt-get update && apt-get install -y build-essential

# ติดตั้ง Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์เข้า container
COPY . /app
WORKDIR /app

# ตั้ง default command (เมื่อ container รัน)
CMD ["prefect", "agent", "start", "-q", "default"]
