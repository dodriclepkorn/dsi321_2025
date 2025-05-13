import csv
import os
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ดาวน์โหลดทรัพยากร nltk (ทำครั้งแรกครั้งเดียว)
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    WordNetLemmatizer().lemmatize('running')
except LookupError:
    nltk.download('wordnet', quiet=True)
try:
    nltk.data.find('omw-1.4')
except LookupError:
    nltk.download('omw-1.4', quiet=True)

# โฟลเดอร์ข้อมูล
output_folder = "data"
filename = os.path.join(output_folder, "scraped_news.csv")
output_cleaned_filename = os.path.join(output_folder, "output_cleaned.csv")

# อ่านไฟล์ CSV ด้วย pandas
try:
    df = pd.read_csv(filename, encoding='utf-8')
    print(f"อ่านไฟล์ CSV สำเร็จ มีจำนวน rows: {len(df)}")
except FileNotFoundError:
    print(f"ไม่พบไฟล์: {filename}")
    exit()

# เตรียม stop words
stop_words = set(stopwords.words('english'))

# เตรียม lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if isinstance(text, str):
        # แปลงเป็น lowercase
        text = text.lower()
        # ลบตัวเลข
        text = re.sub(r'\d+', '', text)
        # ลบ non-alphabetic characters
        text = re.sub(r'[^a-z\s]', '', text)
        # แยกคำ
        words = text.split()
        # ลบ stop words, คำสั้น, lemmatize
        words = [
            lemmatizer.lemmatize(word)
            for word in words
            if word not in stop_words and len(word) >= 3
        ]
        return ' '.join(words)
    return ''

# Clean ทั้ง title และ summary
df['cleaned_title'] = df['title'].apply(clean_text)
df['cleaned_summary'] = df['summary'].apply(clean_text)

# บันทึกไฟล์ใหม่
try:
    df.to_csv(output_cleaned_filename, encoding='utf-8', index=False)
    print(f"ข้อมูลที่ clean แล้วถูกบันทึกในไฟล์: {output_cleaned_filename}")
except Exception as e:
    print(f"เกิดข้อผิดพลาดในการบันทึกไฟล์ CSV: {e}")

# รวมข้อความที่ clean แล้วทั้งหมดเพื่อทำ Word Cloud
all_cleaned_text = ' '.join(df['cleaned_title'].astype(str)) + ' ' + ' '.join(df['cleaned_summary'].astype(str))

# สร้าง Word Cloud
wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color='white',
    stopwords=stop_words,
    min_font_size=10
).generate(all_cleaned_text)

# แสดงผล Word Cloud
plt.figure(figsize=(14, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Cleaned Scraped News", fontsize=18)
plt.show()

# ถ้าต้องการบันทึกเป็นไฟล์รูปภาพ:
# wordcloud.to_file(os.path.join(output_folder, "news_wordcloud.png"))
