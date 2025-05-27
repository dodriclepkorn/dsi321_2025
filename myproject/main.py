import feedparser
import pandas as pd
import lakefs                          # ← เพิ่มการ import lakefs
from datetime import datetime
from prefect import task, flow
from lakefs.client import Client
import requests

from config_path import keywords       # import keywords จากไฟล์ config_path.py

@task
def scrape_and_save(keyword: str) -> pd.DataFrame:
    rss_url = (
        f"https://news.google.com/rss/search?"
        f"q={keyword.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    )
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(rss_url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Fetch failed for `{keyword}`: {e}")
        return pd.DataFrame()

    feed = feedparser.parse(resp.content)
    if feed.bozo:
        print(f"⚠️ Parsing issue with `{keyword}`")
        return pd.DataFrame()

    fetched_time = datetime.now().isoformat()
    rows = []
    for e in feed.entries:
        pub = getattr(e, "published", None)
        try:
            dt = datetime.strptime(pub, '%a, %d %b %Y %H:%M:%S GMT') if pub else datetime.now()
        except Exception:
            dt = datetime.now()
        rows.append({
            "title": e.title,
            "link": e.link,
            "published": pub,
            "fetched_at": fetched_time,
            "keyword": keyword,
            "year": dt.year,
            "month": dt.month,
            "day": dt.day,
        })
    return pd.DataFrame(rows)

@task
def load_to_lakefs(df: pd.DataFrame):
    repo   = "scrape-news"
    branch = "main"
    path   = "scrape-news.parquet"
    s3path = f"s3://{repo}/{branch}/{path}"

    # สร้าง client lakeFS
    client = Client(
        host="http://localhost:8001",
        username="access_key",
        password="secret_key",
        verify_ssl=False,
    )
    # สร้าง repository ถ้ายังไม่มี
    lakefs.repository(repo, client=client).create(
        storage_namespace=f"local://{repo}", exist_ok=True
    )

    # เขียน DataFrame ลง Parquet บน lakeFS (S3)
    storage_opts = {
        "key": "access_key",
        "secret": "secret_key",
        "client_kwargs": {"endpoint_url": "http://localhost:8001"},
    }
    df.to_parquet(
        s3path,
        storage_options=storage_opts,
        partition_cols=["year", "month", "day"],
        engine="pyarrow",
    )
    print("✅ Data written to lakeFS")

@flow
def scrape_news_flow():
    all_dfs = []
    for kw in keywords:
        df = scrape_and_save(kw)
        if not df.empty:
            all_dfs.append(df)
    if all_dfs:
        final = pd.concat(all_dfs, ignore_index=True)
        load_to_lakefs(final)
        print(f"✅ ดึงข่าวสำเร็จทั้งหมด {len(final)} รายการ")
    else:
        print("❌ ไม่พบข่าวใหม่ในคำค้นหาใดๆ")

if __name__ == "__main__":
    # สั่ง Prefect สร้าง deployment และตั้ง schedule ทุกนาที
    scrape_news_flow.serve(
        name="scrape-news-deployment",
        cron="* * * * *",
    )
