import csv

def find_duplicate_news(file1_path, file2_path):
    """
    ตรวจสอบข่าวที่ซ้ำกันระหว่างสองไฟล์ CSV โดยพิจารณาจาก 'title' และ 'link'

    Args:
        file1_path (str): พาธไปยังไฟล์ CSV แรก
        file2_path (str): พาธไปยังไฟล์ CSV ที่สอง

    Returns:
        list: รายการของข่าวที่ซ้ำกัน (ในรูปแบบ Dictionary)
    """
    duplicate_news = []
    data1 = set()
    data2 = set()

    # อ่านข้อมูลจากไฟล์แรก
    try:
        with open(file1_path, 'r', newline='', encoding='utf-8') as csvfile1:
            reader1 = csv.DictReader(csvfile1)
            for row in reader1:
                if 'title' in row and 'link' in row:
                    data1.add((row['title'].strip(), row['link'].strip()))
    except FileNotFoundError:
        print(f"ไม่พบไฟล์: {file1_path}")
        return duplicate_news

    # อ่านข้อมูลจากไฟล์ที่สอง
    try:
        with open(file2_path, 'r', newline='', encoding='utf-8') as csvfile2:
            reader2 = csv.DictReader(csvfile2)
            for row in reader2:
                if 'title' in row and 'link' in row:
                    data2.add((row['title'].strip(), row['link'].strip()))
    except FileNotFoundError:
        print(f"ไม่พบไฟล์: {file2_path}")
        return duplicate_news

    # หาข้อมูลที่ซ้ำกัน
    for title_link in data1:
        if title_link in data2:
            duplicate_news.append({'title': title_link[0], 'link': title_link[1], 'source_file': file1_path})
    for title_link in data2:
        if title_link in data1 and {'title': title_link[0], 'link': title_link[1], 'source_file': file2_path} not in duplicate_news:
            duplicate_news.append({'title': title_link[0], 'link': title_link[1], 'source_file': file2_path})

    return duplicate_news

if __name__ == "__main__":
    file1 = "newsapi_alternative_construction.csv"
    file2 = "alternative_construction_materials_news.csv"
    duplicates = find_duplicate_news(file1, file2)

    if duplicates:
        print("พบข่าวที่ซ้ำกันระหว่างสองไฟล์:")
        for news in duplicates:
            print(f"  Title: {news['title']}")
            print(f"  Link: {news['link']}")
            print(f"  พบในไฟล์: {news['source_file']}")
            print("-" * 30)
    else:
        print("ไม่พบข่าวที่ซ้ำกันระหว่างสองไฟล์")