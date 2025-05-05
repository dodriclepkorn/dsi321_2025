import csv
from duckduckgo_search import DDGS
import os

# สร้างอินสแตนซ์ของ DDGS
ddgs = DDGS()

# หัวข้อข่าวที่คุณแนะนำมา (ภาษาอังกฤษ)
suggested_topics = [
    "Life Cycle Assessment of Alternative Construction Materials",
    "Physical and Mechanical Properties of Compressed Earth Blocks",
    "Potential of Bamboo as a Structural Construction Material",
    "Applications of Concrete Mixed with Recycled Materials",
    "Thermal Insulation from Natural Materials",
    "Construction Materials from Agricultural Waste",
    "Bio-based Construction Materials",
    "3D Printing with Alternative Construction Materials",
    "Energy-Efficient Buildings with Alternative Construction Materials",
    "Standards and Regulations for Alternative Construction Materials",
    "Adoption of Alternative Construction Materials",
    "Economic Impact of Alternative Construction Materials",
    "Promoting Sustainable Alternative Construction Materials",
    "Consumer Awareness of Alternative Construction Materials",
    "Production of Alternative Construction Materials in Thailand",
    "Alternative Construction Materials with Enhanced Properties",
    "Improving Alternative Construction Materials with New Technologies",
    "Alternative Construction Materials from Local Resources",
    "Integrating Alternative Construction Materials into Circular Economy",
    "Collaboration for Development of Alternative Construction Materials"
]

# คีย์เวิร์ดหลัก
base_query = "news about "

# สร้างชื่อไฟล์ CSV
filename = "alternative_construction_materials_news.csv"
file_exists = os.path.isfile(filename)
existing_links = set()

# อ่านลิงก์ที่มีอยู่แล้วจากไฟล์ (ถ้ามี)
if file_exists:
    with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if 'link' in row and row['link']:
                existing_links.add(row['link'])

with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'link', 'source', 'date', 'topic']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    # ค้นหาข่าวสำหรับคีย์เวิร์ดหลัก (ถ้าต้องการเก็บไว้)
    main_query_results = ddgs.news(base_query + "alternative construction materials", max_results=100) # ปรับ max_results ได้ตามต้องการ
    for result in main_query_results:
        link = result.get('url')
        if link and link not in existing_links:
            writer.writerow({
                'title': result.get('title'),
                'link': link,
                'source': result.get('source'),
                'date': result.get('date'),
                'topic': "General Alternative Construction Materials"
            })
            existing_links.add(link)

    # ค้นหาข่าวสำหรับแต่ละหัวข้อที่แนะนำมา
    for topic in suggested_topics:
        query = base_query + topic
        results = ddgs.news(query, max_results=100) # ปรับ max_results ได้ตามต้องการ
        for result in results:
            link = result.get('url')
            if link and link not in existing_links:
                writer.writerow({
                    'title': result.get('title'),
                    'link': link,
                    'source': result.get('source'),
                    'date': result.get('date'),
                    'topic': topic
                })
                existing_links.add(link)

print(f"✅ ดึงข้อมูลข่าวเสร็จสิ้นและบันทึก (ไม่รวมข้อมูลซ้ำ) ในไฟล์: {filename}")