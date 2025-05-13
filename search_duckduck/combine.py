import csv

# ไฟล์ input และ output
file1 = "newsapi_alternative_construction.csv"
file2 = "alternative_construction_materials_news.csv"
data_file = "combined_cleaned_data.csv"
not_relevant_file = "filtered_out_unrelated_news.csv"

# หัวคอลัมน์
fieldnames = ['headline', 'summary', 'source', 'date', 'topic']

# รวม keyword ที่ตัดให้สั้นลง สำหรับเช็คความเกี่ยวข้อง
relevant_keywords = [
    "LCA",
    "Earth blocks",
    "Bamboo",
    "Recycled",
    "Insulation",
    "Agri waste",
    "Bio-based",
    "3D printing",
    "Energy-efficient",
    "Standards",
    "Regulations",
    "Adoption",
    "Economic impact",
    "Awareness",
    "Production",
    "Enhanced",
    "Tech",
    "Local resources",
    "Circular economy",
    "Collaboration",
    "Fungus-based",
    "Sustain",
    "Paver blocks",
    "Alt. materials",
    "Bamboo build",
    "Recycled concrete",
    "Energy materials",
    "Cool roofing",
    "Concrete alt.",
    "Geopolymer",
    "3D homes",
    "Graphene",
    "BioMason",
    "Renewable",
    "Zero waste",
    "Earth-friendly",
    "Carbon neutral",
    "Hempcrete",
    "Rammed earth",
    "Reclaimed wood",
    "Sustainable",
    "Arch. materials",
    "Circular materials",
    "Innovative build"
]

# ฟังก์ชันตรวจสอบว่าข่าวเกี่ยวข้องหรือไม่
def is_relevant(text):
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in relevant_keywords)

# ใช้ set เพื่อตรวจสอบ headline ซ้ำ
seen_headlines = set()

# เปิดไฟล์สำหรับเขียนข่าวที่เกี่ยวข้อง
with open(data_file, mode='w', newline='', encoding='utf-8') as outfile, \
     open(not_relevant_file, mode='w', newline='', encoding='utf-8') as notfile:

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    not_writer = csv.DictWriter(notfile, fieldnames=fieldnames)

    writer.writeheader()
    not_writer.writeheader()

    for filename in [file1, file2]:
        with open(filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                headline = row.get('headline', '').strip()
                summary = row.get('summary', '').strip()
                combined_text = f"{headline} {summary}"

                if headline and headline not in seen_headlines:
                    entry = {
                        'headline': headline,
                        'summary': summary,
                        'source': row.get('source', '').strip(),
                        'date': row.get('date', '').strip(),
                        'topic': row.get('topic', '').strip()
                    }

                    if is_relevant(combined_text):
                        writer.writerow(entry)
                    else:
                        not_writer.writerow(entry)

                    seen_headlines.add(headline)

print(f"รวมและคลีนข้อมูลเรียบร้อย -> ไฟล์ที่เกี่ยวข้อง: {data_file}, ไฟล์ที่ไม่เกี่ยวข้อง: {not_relevant_file}")
