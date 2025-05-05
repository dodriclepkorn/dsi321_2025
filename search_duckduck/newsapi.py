import requests
import json
import csv
from datetime import datetime
import os

# แทนที่ด้วย API Key ของคุณ
API_KEY = "a6d999e2c59444828740a414495a33ad"
BASE_URL = "https://newsapi.org/v2/everything"  # หรือใช้ Endpoint อื่นๆ เช่น /v2/top-headlines

# หัวข้อข่าวที่ต้องการค้นหา
topics = [
    "alternative construction materials",
    "bamboo building",
    "recycled concrete",
    # เพิ่มหัวข้ออื่นๆ ได้ตามต้องการ
]

filename = "newsapi_alternative_construction.csv"
headers = ['title', 'url', 'source_name', 'publishedAt', 'description', 'topic']
existing_links = set()

# ตรวจสอบไฟล์ CSV ที่มีอยู่เพื่อหลีกเลี่ยงการบันทึกซ้ำ
try:
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'url' in row:
                existing_links.add(row['url'])
except FileNotFoundError:
    pass

with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    if not existing_links:
        writer.writeheader()

    for topic in topics:
        params = {
            'q': topic,
            'apiKey': API_KEY,
            'pageSize': 100,  # จำนวนผลลัพธ์ต่อหน้า (สูงสุด 100)
            'sortBy': 'relevancy', # หรือ 'publishedAt'
            'language': 'en'      # หรือภาษาอื่นๆ ที่รองรับ
            # เพิ่ม parameters อื่นๆ ได้ตามต้องการ เช่น 'from', 'to', 'sources', 'domains'
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'ok' and 'articles' in data:
                for article in data['articles']:
                    title = article.get('title')
                    url = article.get('url')
                    source_name = article.get('source', {}).get('name')
                    publishedAt_str = article.get('publishedAt')
                    description = article.get('description')
                    publishedAt = None
                    if publishedAt_str:
                        publishedAt = datetime.fromisoformat(publishedAt_str.replace('Z', '+00:00'))

                    if url and url not in existing_links:
                        writer.writerow({
                            'title': title,
                            'url': url,
                            'source_name': source_name,
                            'publishedAt': publishedAt.strftime('%Y-%m-%d %H:%M:%S') if publishedAt else None,
                            'description': description,
                            'topic': topic
                        })
                        existing_links.add(url)
            else:
                print(f"ไม่พบผลลัพธ์สำหรับหัวข้อ: {topic} - {data.get('message')}")

        except requests.exceptions.RequestException as e:
            print(f"เกิดข้อผิดพลาดในการร้องขอสำหรับหัวข้อ '{topic}': {e}")
        except json.JSONDecodeError as e:
            print(f"เกิดข้อผิดพลาดในการถอดรหัส JSON สำหรับหัวข้อ '{topic}': {e}")

print(f"✅ ดึงข้อมูลข่าวจาก NewsAPI.org เสร็จสิ้นและบันทึกในไฟล์: {filename}")