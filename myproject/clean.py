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
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# โฟลเดอร์ข้อมูล
output_folder = "data"
filename = os.path.join(output_folder, "scraped_news.csv")

# อ่านไฟล์ CSV ด้วย pandas
try:
    df = pd.read_csv(filename, encoding='utf-8')
except FileNotFoundError:
    print(f"ไม่พบไฟล์: {filename}")
    exit()

# รวมข้อความจากคอลัมน์ 'title' และ 'summary'
all_text = ' '.join(df['title'].astype(str)) + ' ' + ' '.join(df['summary'].astype(str))
all_text = all_text.lower()

# เตรียม stop words
stop_words = set(stopwords.words('english'))

# เตรียม lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    # ลบ non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    # ลบ stop words และ lemmatize
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

# คลีนข้อความทั้งหมด
cleaned_text = clean_text(all_text)

# สร้าง Word Cloud
wordcloud = WordCloud(width=800, height=400,
                      background_color='white',
                      stopwords=stop_words,
                      min_font_size=10).generate(cleaned_text)

# แสดงผล Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Scraped News")
plt.show()

# บันทึก Word Cloud เป็นรูปภาพ (ถ้าต้องการ)
#wordcloud.to_file(os.path.join(output_folder, "news_wordcloud.png"))
#print(f"Word Cloud ถูกบันทึกเป็น: {os.path.join(output_folder, 'news_wordcloud.png')}")