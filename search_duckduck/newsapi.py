import requests
import json
import csv
from datetime import datetime
import os

API_KEY = "a6d999e2c59444828740a414495a33ad"
BASE_URL = "https://newsapi.org/v2/everything"

topics = [
    "alternative construction materials",
    "bamboo building",
    "recycled concrete",
    "Recycled materials",
    "Energy-efficient Materials",
    "Cool roofing materials",
    "Concrete Alternatives",
    "Geopolymer concrete",
    "3D-printed homes",
    "Graphene-enhanced materials",
    "BioMason bricks",
]

filename = "newsapi_alternative_construction.csv"
headers = ['headline', 'summary', 'source', 'date', 'topic']
existing_titles = set()

# ตรวจสอบไฟล์ CSV ที่มีอยู่เพื่อหลีกเลี่ยงการบันทึกซ้ำ
try:
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'headline' in row:
                existing_titles.add(row['headline'])
except FileNotFoundError:
    pass

with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    if not existing_titles:
        writer.writeheader()

    for topic in topics:
        params = {
            'q': topic,
            'apiKey': API_KEY,
            'pageSize': 100,
            'sortBy': 'relevancy',
            'language': 'en'
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'ok' and 'articles' in data:
                for article in data['articles']:
                    headline = article.get('title')
                    summary = article.get('description', '')
                    source = article.get('source', {}).get('name', '')
                    publishedAt_str = article.get('publishedAt')
                    date = None

                    if publishedAt_str:
                        date = datetime.fromisoformat(publishedAt_str.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')

                    if headline and headline not in existing_titles:
                        writer.writerow({
                            'headline': headline,
                            'summary': summary,
                            'source': source,
                            'date': date,
                            'topic': topic
                        })
                        existing_titles.add(headline)
            else:
                print(f"ไม่พบผลลัพธ์สำหรับหัวข้อ: {topic} - {data.get('message')}")

        except requests.exceptions.RequestException as e:
            print(f"เกิดข้อผิดพลาดในการร้องขอสำหรับหัวข้อ '{topic}': {e}")
        except json.JSONDecodeError as e:
            print(f"เกิดข้อผิดพลาดในการถอดรหัส JSON สำหรับหัวข้อ '{topic}': {e}")

print(f" ดึงข้อมูลข่าวจาก NewsAPI.org เสร็จสิ้นและบันทึกในไฟล์: {filename}")
