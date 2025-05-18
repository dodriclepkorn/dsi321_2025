from prefect import flow, task, get_run_logger
import csv
import os
import hashlib
import datetime
from duckduckgo_search import DDGS

@task
def scrape_news():
    logger = get_run_logger()
    ddgs = DDGS()

    output_folder = "data"
    os.makedirs(output_folder, exist_ok=True)

    # เพิ่ม timestamp ต่อท้ายชื่อไฟล์ เช่น scraped_news_20250518_153000.csv
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_folder, f"scraped_news_{timestamp}.csv")
    file_exists = os.path.isfile(filename)

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

    existing_hashes = set()

    def load_existing_hashes():
        if file_exists:
            logger.info(f"โหลดข้อมูลจากไฟล์ที่มีอยู่แล้ว: {filename}")
            with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    hash_val = hashlib.md5((row.get('title', '').strip() + row.get('summary', '').strip()).lower().encode('utf-8')).hexdigest()
                    existing_hashes.add(hash_val)
            logger.info(f"พบข้อมูลที่มีอยู่แล้วจำนวน {len(existing_hashes)} รายการ")
        else:
            logger.info("ไม่พบไฟล์เก็บข่าวเดิม จะสร้างไฟล์ใหม่")

    load_existing_hashes()

    with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'summary', 'source', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            logger.info("สร้างไฟล์ใหม่และเขียน header")
            writer.writeheader()

        logger.info("เริ่มค้นหาข่าวหลัก...")
        main_results = ddgs.news(base_query + "alternative construction materials", max_results=100)
        count_main = 0
        for result in main_results:
            title = result.get('title', '').strip()
            summary = result.get('body', '').strip()
            hash_val = hashlib.md5((title + summary).lower().encode('utf-8')).hexdigest()
            if title and hash_val not in existing_hashes:
                writer.writerow({
                    'title': title,
                    'summary': summary,
                    'source': result.get('source', ''),
                    'date': result.get('date', '')
                })
                existing_hashes.add(hash_val)
                count_main += 1
        logger.info(f"เพิ่มข่าวจาก query หลัก: {count_main} รายการ")

        for topic in suggested_topics:
            logger.info(f"กำลังค้นหา: {topic}")
            query = base_query + topic
            results = ddgs.news(query, max_results=100)
            count_topic = 0
            for result in results:
                title = result.get('title', '').strip()
                summary = result.get('body', '').strip()
                hash_val = hashlib.md5((title + summary).lower().encode('utf-8')).hexdigest()
                if title and hash_val not in existing_hashes:
                    writer.writerow({
                        'title': title,
                        'summary': summary,
                        'source': result.get('source', ''),
                        'date': result.get('date', '')
                    })
                    existing_hashes.add(hash_val)
                    count_topic += 1
            logger.info(f"เพิ่มข่าวจาก '{topic}':
