import csv
import os
import hashlib
import logging
from duckduckgo_search import DDGS

# ตั้งค่าระบบ logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

ddgs = DDGS()

# โฟลเดอร์ปลายทาง
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

filename = os.path.join(output_folder, "scraped_news.csv")
file_exists = os.path.isfile(filename)

# หัวข้อที่ใช้ค้นหา (เฉพาะเจาะจง)
suggested_topics = [
    "hempcrete in construction",
    "rammed earth wall technology",
    "geopolymer concrete applications",
    "bio-based insulation materials",
    "fungus-based building materials",
    "graphene-enhanced concrete",
    "3D printed earth homes",
    "mycelium bricks",
    "carbon-negative building blocks",

    "real estate using sustainable materials",
    "eco-friendly public infrastructure projects",
    "zero-energy buildings materials",
    "climate-resilient building materials",

    "thermal performance of eco materials",
    "green building code adoption",
    "circular construction policy",
    "low-carbon construction technologies",
    "building standards for bio-based materials",

    "BioMason bricks adoption",
    "startup using recycled plastic bricks",
    "BamCore bamboo structures",
    "construction companies using sustainable materials",
    "Earthship homes materials",

    "economic impact of sustainable building materials",
    "government subsidies for green construction",
    "community projects using local materials",
    "cost-effectiveness of alternative construction",

    "sustainable materials education in architecture",
    "training for green building technologies"
]

base_query = "news about "

# เก็บ hash ข่าวที่เคยบันทึกไว้
existing_hashes = set()

def make_entry_hash(title, summary):
    content = (title.strip() + summary.strip()).lower()
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# โหลด hash จากไฟล์ที่มีอยู่
if file_exists:
    logging.info(f"โหลดข้อมูลจากไฟล์ที่มีอยู่แล้ว: {filename}")
    with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            hash_val = make_entry_hash(row.get('title', ''), row.get('summary', ''))
            existing_hashes.add(hash_val)
    logging.info(f"พบข้อมูลที่มีอยู่แล้วจำนวน {len(existing_hashes)} รายการ")

# เปิดไฟล์เพื่อเพิ่มข่าว
with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'summary', 'source', 'date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not file_exists:
        logging.info("สร้างไฟล์ใหม่และเขียน header")
        writer.writeheader()

    # ดึงข่าวจาก query หลัก
    logging.info("เริ่มค้นหาข่าวหลัก...")
    main_query_results = ddgs.news(base_query + "alternative construction materials", max_results=100)
    count_main = 0
    for result in main_query_results:
        title = result.get('title', '').strip()
        summary = result.get('body', '').strip()
        hash_val = make_entry_hash(title, summary)

        if title and hash_val not in existing_hashes:
            writer.writerow({
                'title': title,
                'summary': summary,
                'source': result.get('source', ''),
                'date': result.get('date', '')
            })
            existing_hashes.add(hash_val)
            count_main += 1
    logging.info(f"เพิ่มข่าวจาก query หลัก: {count_main} รายการ")

    # ดึงข่าวจากแต่ละ topic
    for topic in suggested_topics:
        logging.info(f"กำลังค้นหา: {topic}")
        query = base_query + topic
        results = ddgs.news(query, max_results=100)
        count_topic = 0
        for result in results:
            title = result.get('title', '').strip()
            summary = result.get('body', '').strip()
            hash_val = make_entry_hash(title, summary)

            if title and hash_val not in existing_hashes:
                writer.writerow({
                    'title': title,
                    'summary': summary,
                    'source': result.get('source', ''),
                    'date': result.get('date', '')
                })
                existing_hashes.add(hash_val)
                count_topic += 1
        logging.info(f"เพิ่มข่าวจาก '{topic}': {count_topic} รายการ")

logging.info(f"ดึงข้อมูลข่าวเสร็จสิ้นและบันทึกในไฟล์: {filename}")
