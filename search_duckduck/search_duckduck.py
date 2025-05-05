import csv
from duckduckgo_search import DDGS

# สร้างอินสแตนซ์ของ DDGS
ddgs = DDGS()

# ค้นหาข่าวด้วยคีย์เวิร์ดที่กำหนด
query = "alternative construction materials"
results = ddgs.news(query, max_results=20)

# สร้างไฟล์ CSV เพื่อบันทึกผลลัพธ์
filename = "alternative_construction_materials_news.csv"

with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'link', 'source', 'date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for result in results:
        writer.writerow({
            'title': result.get('title'),
            'link': result.get('url'),
            'source': result.get('source'),
            'date': result.get('date')
        })

print(f"✅ ดึงข้อมูลข่าวเสร็จสิ้นและบันทึกในไฟล์: {filename}")
