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
os.makedirs(output_folder, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี

filename = os.path.join(output_folder, "scraped_news.csv")
file_exists = os.path.isfile(filename)

# หัวข้อที่ใช้ค้นหา 
suggested_topics = [
    "bamboo construction methods",
    "recycled concrete aggregate uses",
    "3D printing construction technology",
    "sustainable timber framing",
    "eco-friendly insulation materials",
    "innovative bricklaying techniques",
    "government regulations for green building materials",
    "economic benefits of sustainable construction",
    "challenges in adopting hempcrete",
    "market analysis of recycled building materials",
    "case studies of bamboo houses",
    "research on mycelium based construction",
    "automation in concrete construction",
    "robotic bricklaying systems",
    "energy efficient building design",
    "zero waste construction practices",
    "carbon neutral building technologies",
    "local sourcing of building materials",
    "circular economy in construction",
    "collaborative housing projects with sustainable materials",
    "fungus based insulation",
    "sustainable pavement solutions",
    "alternative roofing materials",
    "bamboo scaffolding systems",
    "recycled glass in construction",
    "energy harvesting building materials",
    "cool roof technologies",
    "alternative binders for concrete",
    "geopolymer concrete applications",
    "3D printed affordable housing",
    "graphene enhanced construction materials",
    "BioMason brick production",
    "renewable energy integration in buildings",
    "zero waste building design",
    "earth friendly construction techniques",
    "carbon neutral construction projects",
    "hempcrete wall construction",
    "rammed earth building techniques",
    "reclaimed wood flooring options",
    "sustainable architectural design",
    "circular materials in building design",
    "innovative building facades",
    "alternative construction materials market trends",
    "alternative materials for road construction",
    "cost effectiveness of alternative building materials",
    "performance analysis of sustainable construction",
    "environmental impact of traditional building materials",
    "life cycle assessment of alternative materials",
    "consumer perception of green building",
    "education and training in sustainable construction",
    "investment opportunities in alternative construction",
    "future trends in building materials",
    "modular construction with sustainable materials",
    "prefabricated sustainable building components",
    "self-healing concrete with alternative additives",
    "air purification through building materials",
    "water harvesting through building design",
    "biomimicry in sustainable architecture",
    "smart and sustainable building technologies",
    "community-led sustainable building initiatives",
    "policy frameworks for promoting green construction",
    "standardization of alternative building materials",
    "certification programs for sustainable buildings",
    "the role of architects in promoting sustainable materials",
    "the role of engineers in sustainable construction",
    "innovative uses of natural fibers in building",
    "challenges and solutions for scaling up alternative materials",
    "the impact of climate change on building materials",
    "resilient building design with sustainable materials",
    "urban farming integrated with sustainable buildings",
    "the aesthetics of sustainable architecture",
    "preserving traditional building techniques with sustainable materials",
    "the role of 3D printing in material innovation for construction",
    "advancements in bio-based adhesives for building",
    "the use of robotics in sustainable construction",
    "blockchain technology for transparent material sourcing",
    "artificial intelligence for optimizing building material use",
    "the impact of building materials on occupant health",
    "designing for disassembly and material reuse",
    "the potential of algae-based building materials",
    "innovative sound insulation using sustainable materials",
    "sustainable solutions for historic building renovation",
    "the role of material banks in circular construction",
    "financing mechanisms for sustainable building projects",
    "insurance and liability considerations for alternative materials",
    "the role of universities in sustainable building research",
    "public awareness and adoption of sustainable building practices",
    "the impact of transportation on the carbon footprint of materials",
    "strategies for reducing waste in the construction industry",
    "the potential of bamboo as a structural material",
    "advancements in earth-based building technologies",
    "the use of straw bales in modern construction",
    "innovative applications of recycled plastic in building",
    "the role of fungi in creating new building materials",
    "sustainable solutions for building foundations",
    "the use of living materials in architecture",
    "advancements in transparent solar building materials",
    "the integration of green infrastructure with buildings"
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

    # ดึงข่าวจาก query หลัก (ยังคงค้นหาภาพรวม)
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

    # ดึงข่าวจากแต่ละ topic ที่เพิ่มความหลากหลายแล้ว
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