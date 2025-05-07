import csv

# ชื่อไฟล์ที่ต้องรวม
file1 = "newsapi_alternative_construction.csv"
file2 = "alternative_construction_materials_news.csv"
data_file = "combined_cleaned_alternative_construction_news.csv"

# ใช้ set เพื่อตรวจสอบ headline ซ้ำ
seen_headlines = set()

# คอลัมน์ที่ต้องการ
fieldnames = ['headline', 'summary', 'source', 'date', 'topic']

with open(data_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # รวมข้อมูลจากแต่ละไฟล์
    for filename in [file1, file2]:
        with open(filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                headline = row.get('headline', '').strip()
                if headline and headline not in seen_headlines:
                    writer.writerow({
                        'headline': headline,
                        'summary': row.get('summary', '').strip(),
                        'source': row.get('source', '').strip(),
                        'date': row.get('date', '').strip(),
                        'topic': row.get('topic', '').strip()
                    })
                    seen_headlines.add(headline)

print(f" รวมและคลีนข้อมูลเสร็จสิ้น -> บันทึกในไฟล์: combined_cleaned_alternative_construction_news.csv")
