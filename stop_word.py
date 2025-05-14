import pandas as pd
import re
from nltk.corpus import stopwords
import nltk

# โหลด stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# เพิ่ม custom stopwords
custom_stopwords = {
    # ข่าวและสื่อ
    "news", "update", "latest", "breaking", "read", "watch", "live", "video",
    "media", "outlet", "journal", "articles", "headline", "source", "coverage", "information",
    "say", "says", "said", "report", "reports", "reported",
    "announced", "introduced", "launch", "revealed", "expects",
    "statements", "highlighted", "unveiled", "discussed", "talk", "asks", "request",
    "today", "week", "now",
    "company", "group", "corporation", "organization", "firm", "business",
    "ltd", "inc", "co", "plc", "association", "partner", "entity", "owner",
    "market", "investment", "opportunity", "cost", "revenue",
    "u.s", "china", "europe", "asia", "india", "africa", "japan", "korea",
    "middle", "east", "north", "america", "latin",
    "province", "city", "region", "district", "country",
    "is", "will", "with", "for", "by", "on", "at", "in", "to",
    "and", "or", "that", "as", "during", "through", "along",
    "from", "above", "around", "of", "between", "under", "over",
    "products", "services", "materials", "solutions", "technologies", "construction", "building",
    "supply", "demand", "development", "design",
    "engineering", "value", "growth", "trend", "innovation", "technology",
    "cement", "industry", "s", "weak", "strat",
    "smm", "made", "engineering", "sale", "travis", "perkins", "finding",
    "material", "insights", "german", "researchers", "prices", "start",
    "driven", "forecast", "analysis", "launched", "study", "data", "reporting",
    "usd", "billion", "million", "cagr", "year", "years", "2030", "2035", "2025", "2031"
}
stop_words.update(custom_stopwords)

# โหลดไฟล์
df = pd.read_csv("raw_scrape.csv")

# ฟังก์ชันล้างข้อความ
def clean_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r"[\"“”‘’'’:,®%&]", "", text)  # ลบเครื่องหมายพิเศษ
    text = re.sub(r"\b\d+\b", "", text)          # ลบตัวเลขล้วน
    text = re.sub(r"[^a-z\s\-]", "", text)       # ลบทุกอย่างที่ไม่ใช่ a-z, space, hyphen
    text = re.sub(r"\s+", " ", text).strip()     # ลบช่องว่างซ้ำ
    return text

# ฟังก์ชันลบ stopwords
def remove_stopwords(text):
    if pd.isnull(text):
        return ""
    words = text.split()
    filtered = [word for word in words if word not in stop_words]
    return " ".join(filtered)

# รวมกระบวนการ clean และ remove stopwords
df["Title"] = df["Title"].astype(str).apply(clean_text).apply(remove_stopwords)

# บันทึกไฟล์
df.to_csv("cleaned_data.csv", index=False, encoding="utf-8-sig")

print("✅ เสร็จแล้ว บันทึกไฟล์เป็น cleaned_data.csv")
import pandas as pd
import re
from nltk.corpus import stopwords
import nltk

# โหลด stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# เพิ่ม custom stopwords
custom_stopwords = {
    # ข่าวและสื่อ
    "news", "update", "latest", "breaking", "read", "watch", "live", "video",
    "media", "outlet", "journal", "articles", "headline", "source", "coverage", "information",
    "say", "says", "said", "report", "reports", "reported",
    "announced", "introduced", "launch", "revealed", "expects",
    "statements", "highlighted", "unveiled", "discussed", "talk", "asks", "request",
    "today", "week", "now",
    "company", "group", "corporation", "organization", "firm", "business",
    "ltd", "inc", "co", "plc", "association", "partner", "entity", "owner",
    "market", "investment", "opportunity", "revenue",
    "u.s", "china", "europe", "asia", "india", "africa", "japan", "korea",
    "middle", "east", "north", "america", "latin",
    "province", "city", "region", "district", "country",
    "is", "will", "with", "for", "by", "on", "at", "in", "to",
    "and", "or", "that", "as", "during", "through", "along",
    "from", "above", "around", "of", "between", "under", "over",
    "products", "services", "materials", "solutions", "technologies", "construction", "building",
    "supply", "demand", "development", "design",
    "engineering", "value", "growth", "trend", "innovation", "technology",
    "cement", "industry", "s", "weak", "strat",
    "smm", "made", "engineering", "sale", "travis", "perkins", "finding",
    "material", "insights", "german", "researchers", "prices", "start",
    "driven", "forecast", "analysis", "launched", "study", "data", "reporting",
    "usd", "billion", "million", "cagr", "year", "years", "2030", "2035", "2025", "2031",
    "announce", "maintain", "announces", 
}
stop_words.update(custom_stopwords)

# โหลดไฟล์
df = pd.read_csv("raw_scrape.csv")

# ฟังก์ชันล้างข้อความ
def clean_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r"[\"“”‘’'’:,®%&]", "", text)  # ลบเครื่องหมายพิเศษ
    text = re.sub(r"\b\d+\b", "", text)          # ลบตัวเลขล้วน
    text = re.sub(r"[^a-z\s\-]", "", text)       # ลบทุกอย่างที่ไม่ใช่ a-z, space, hyphen
    text = re.sub(r"\s+", " ", text).strip()     # ลบช่องว่างซ้ำ
    return text

# ฟังก์ชันลบ stopwords
def remove_stopwords(text):
    if pd.isnull(text):
        return ""
    words = text.split()
    filtered = [word for word in words if word not in stop_words]
    return " ".join(filtered)

# รวมกระบวนการ clean และ remove stopwords
df["Title"] = df["Title"].astype(str).apply(clean_text).apply(remove_stopwords)

# บันทึกไฟล์
df.to_csv("cleaned_data.csv", index=False, encoding="utf-8-sig")

print("✅ เสร็จแล้ว บันทึกไฟล์เป็น cleaned_data.csv")