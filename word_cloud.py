import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# โหลดไฟล์ cleaned_data.csv ที่ได้ทำการ clean แล้ว
df = pd.read_csv("cleaned_data.csv")

# กรองเฉพาะแถวที่ในคอลัมน์ Date มีคำว่า "ชั่วโมงที่ผ่านมา" หรือ "วันที่ผ่านมา"
filtered_df = df[df['Date'].str.contains(r'(ชั่วโมงที่ผ่านมา|วันที่ผ่านมา)', na=False)]

# print("จำนวนแถวที่ตรงกับเงื่อนไข:", filtered_df.shape[0])
# print("ตัวอย่างข้อมูลที่กรองได้:")
# print(filtered_df[['Date', 'Title']].head(1000))

# รวมข้อความทั้งหมดในคอลัมน์ Title_no_stopwords (หรือชื่อคอลัมน์ที่คุณใช้จริง)
text = " ".join(filtered_df['Title'])

# สร้าง Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

# แสดงผล Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()