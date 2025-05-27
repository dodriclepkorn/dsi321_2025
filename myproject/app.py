import os
import streamlit as st
import pandas as pd
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re, string
import pandera as pa
from pandera import Column, Check

# ดาวน์โหลด stopwords ครั้งแรก (จะไม่รันซ้ำถ้ามีแล้ว)
nltk.download('stopwords')

# อ่าน config จาก env
LAKEFS_ENDPOINT    = os.getenv("LAKEFS_ENDPOINT", "http://localhost:8001")
LAKEFS_ACCESS_KEY  = os.getenv("LAKEFS_ACCESS_KEY", "access_key")
LAKEFS_SECRET_KEY  = os.getenv("LAKEFS_SECRET_KEY", "secret_key")

st.title("📰 News Word Cloud Explorer")

def clean_text(text):
    text = re.sub(r'\|.*', '', text)
    text = re.sub(r'-.*', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    text = " ".join([w for w in text.split() if w not in stopwords.words('english')])
    return text

@st.cache_data(ttl=600)
def read_and_validate():
    repo    = "scrape-news"
    branch  = "main"
    s3path  = f"s3://{repo}/{branch}/scrape-news.parquet"
    storage_opts = {
        "key": LAKEFS_ACCESS_KEY,
        "secret": LAKEFS_SECRET_KEY,
        "client_kwargs": {"endpoint_url": LAKEFS_ENDPOINT}
    }

    df = pd.read_parquet(s3path, storage_options=storage_opts, engine="pyarrow")

    # แปลง timestamp
    df['fetched_at'] = pd.to_datetime(df['fetched_at'], errors='coerce')

    # แปลง categorical เป็น string แล้วเป็น int
    for col in ['year', 'month', 'day']:
        df[col] = df[col].astype(str).astype(int)

    # ตรวจ schema
    schema = pa.DataFrameSchema({
        "title"     : Column(pa.String),
        "link"      : Column(pa.String),
        "published" : Column(pa.String, nullable=True),
        "fetched_at": Column(pa.DateTime),
        "keyword"   : Column(pa.String),
        "year"      : Column(pa.Int, Check.ge(1970)),
        "month"     : Column(pa.Int, Check.in_range(1, 12)),
        "day"       : Column(pa.Int, Check.in_range(1, 31)),
    })

    return schema.validate(df, lazy=True)

def generate_wordcloud(df):
    df['cleaned'] = df['title'].dropna().astype(str).apply(clean_text)
    text = " ".join(df['cleaned'])
    wc = WordCloud(
        width=1000, height=600, background_color='white',
        max_words=200, colormap='viridis', collocations=False
    ).generate(text)
    return wc

try:
    df = read_and_validate()
    wc = generate_wordcloud(df)

    st.subheader("🔤 Word Cloud")
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    st.subheader("📄 Data Table")
    st.dataframe(df[['title', 'keyword', 'year', 'month', 'day']])

except Exception as e:
    st.error(f"❌ {e}")
