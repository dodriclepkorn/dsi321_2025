import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import string
from nltk.corpus import stopwords
import nltk

st.title('Test')

nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'\|.*', '', text)  # remove everything after |
    text = re.sub(r'-.*', '', text)   # remove everything after -
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in stopwords.words('english')])
    return text

@st.cache_data(ttl=600)
def read_from_lakefs():
    repo_name = "scrape-news"
    branch_name = "main"
    path = "scrape-news.parquet"
    lakefs_s3_path = f"s3://{repo_name}/{branch_name}/{path}"
    storage_options = {
        "key": "access_key",
        "secret": "secret_key",
        "client_kwargs": {
            "endpoint_url": "http://localhost:8001"
        }
    }
    df = pd.read_parquet(
        lakefs_s3_path,
        storage_options=storage_options,
        engine='pyarrow',
    )
    return df

df = read_from_lakefs()
st.write(df)

def generate_wordcloud(df: pd.DataFrame) -> str:
    df['cleaned_title'] = df['title'].dropna().astype(str).apply(clean_text)
    # Generate word cloud text
    all_text = " ".join(df["cleaned_title"])

    wordcloud = WordCloud(
        width=1000,
        height=600,
        background_color='white',
        max_words=200,
        colormap='viridis',      # เปลี่ยนโทนสีได้ตามต้องการ เช่น 'plasma', 'inferno', 'cividis'
        collocations=False       # ปิดการรวมคำซ้ำ (เช่น "New York")
    ).generate(all_text)
    return wordcloud

wordcloud = generate_wordcloud(df=df)

# Streamlit display
st.title("Word Cloud of Construction Material Topics")

# Display WordCloud
fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Display the dataframe
st.subheader("Data Table")
st.write(df)