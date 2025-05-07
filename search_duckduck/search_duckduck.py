import csv
from duckduckgo_search import DDGS
import os

ddgs = DDGS()

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

base_query = "news about "

filename = "alternative_construction_materials_news.csv"
file_exists = os.path.isfile(filename)
existing_titles = set()

if file_exists:
    with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if 'headline' in row and row['headline']:
                existing_titles.add(row['headline'])

with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['headline', 'summary', 'source', 'date', 'topic']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    # General query
    main_query_results = ddgs.news(base_query + "alternative construction materials", max_results=100)
    for result in main_query_results:
        headline = result.get('title')
        if headline and headline not in existing_titles:
            writer.writerow({
                'headline': headline,
                'summary': result.get('body', ''),  # fallback to empty string if no summary
                'source': result.get('source', ''),
                'date': result.get('date', ''),
                'topic': "General Alternative Construction Materials"
            })
            existing_titles.add(headline)

    # Specific topic queries
    for topic in suggested_topics:
        query = base_query + topic
        results = ddgs.news(query, max_results=100)
        for result in results:
            headline = result.get('title')
            if headline and headline not in existing_titles:
                writer.writerow({
                    'headline': headline,
                    'summary': result.get('body', ''),
                    'source': result.get('source', ''),
                    'date': result.get('date', ''),
                    'topic': topic
                })
                existing_titles.add(headline)

print(f" ดึงข้อมูลข่าวเสร็จสิ้นและบันทึกในไฟล์: {filename}")
