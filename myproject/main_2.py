import feedparser
import csv
from datetime import datetime
import os
from prefect import task, flow
import pandas as pd
from prefect.schedules import Interval
from pathlib import Path
from datetime import timedelta

# คำค้นหาหลายคำที่เกี่ยวกับ alternative construction materials
search_keywords = [
    "construction materials",
    "building materials",
    "building supplies",
    "construction market",
    "construction news",
    "construction chemicals",
    "material shortage",
    "price increase construction",
    "supply chain construction",
    "green building materials",
    "sustainable construction",
]

@task
def create_data_folder_and_csv(csv_path: str):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(csv_path)
    if not file_exists:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "link", "published", "fetched_at", "keyword"])
    return file_exists

@task
def load_existing_links(csv_path: str):
    existing_links = set()
    if os.path.isfile(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames and "link" in reader.fieldnames:
                for row in reader:
                    existing_links.add(row["link"])
    return existing_links

# @task
# def scrape_and_save(csv_path: str, keyword: str, existing_links: set):
#     new_entries = 0
#     rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}"
#     feed = feedparser.parse(rss_url)

#     with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         for entry in feed.entries:
#             if entry.link not in existing_links:
#                 writer.writerow([
#                     entry.title,
#                     entry.link,
#                     entry.published,
#                     datetime.now().isoformat(),
#                     keyword
#                 ])
#                 existing_links.add(entry.link)
#                 new_entries += 1
#     return new_entries

@task
def read_from_lakefs() -> pd.DataFrame:
    repo_name = "scrape-news"
    branch_name = "main"
    path = "scrape-news.parquet"
    lakefs_s3_path = f"s3://{repo_name}/{branch_name}/{path}"
    storage_options = {
        "key": "access_key",
        "secret": "secret_key",
        "client_kwargs": {
            "endpoint_url": "http://lakefsdb:8000"
        }
    }
    df = pd.read_parquet(
        lakefs_s3_path,
        storage_options=storage_options,
        engine='pyarrow',
    )
    return df

@task
def load_to_lakefs_incremental(df: pd.DataFrame):
    repo_name = "scrape-news"
    branch_name = "main"
    path = "scrape-news.parquet"
    lakefs_s3_path = f"s3://{repo_name}/{branch_name}/{path}"
    storage_options = {
        "key": "access_key",
        "secret": "secret_key",
        "client_kwargs": {
            "endpoint_url": "http://lakefsdb:8000"
        }
    }
    df.to_parquet(
        lakefs_s3_path,
        storage_options=storage_options,
        partition_cols=['year', 'month', 'day'],
        engine='pyarrow',
    )

@task
def scrape_and_save(keyword: str) -> pd.DataFrame:
    rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}"
    feed = feedparser.parse(rss_url)

    data = []
    for entry in feed.entries:
        published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S GMT')
        data.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "year": published_date.year,
            "month": published_date.month,
            "day": published_date.day
        })

    if feed.entries:
        fallback_date = published_date
    else:
        fallback_date = datetime.now()

    # Manually append dummy data
    # data.append({
    #     "title": "news news news news news news news news",
    #     "link": "http://news newsnews newsnews news.com",
    #     "published": fallback_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    #     "year": fallback_date.year,
    #     "month": fallback_date.month,
    #     "day": fallback_date.day
    # })
    df = pd.DataFrame(data)
    return df

    # with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #         if entry.link not in existing_links:
    #             writer.writerow([
    #                 entry.,
    #                 entry.link,
    #                 entry.published,
    #                 datetime.now().isoformat(),
    #                 keyword
    #             ])
    #             existing_links.add(entry.link)
    #             new_entries += 1
    return new_entries

@flow
def scrape_news_flow_2():
    # csv_path = os.path.join("data", "scrap_data.csv")
    # create_data_folder_and_csv(csv_path)
    # existing_links = load_existing_links(csv_path)

    # total_new_entries = 0
    all_df = []
    for keyword in search_keywords:
        df = scrape_and_save(keyword)
        all_df.append(df)
        break  # ← Remove or keep depending on whether you want to process only the first keyword

    # Combine all scraped results
    df_all = pd.concat(all_df, ignore_index=True)


    df_lakefs = read_from_lakefs()

    df_lakefs["uid"] = df_lakefs["link"].astype(str) + df_lakefs["title"].astype(str)
    df_all["uid"] = df_all["link"].astype(str) + df_all["title"].astype(str)

    # Filter only new entries
    new_df = df_all[~df_all["uid"].isin(df_lakefs["uid"])]
    new_df.drop(columns=["uid"], inplace=True, errors="ignore")
    if len(new_df) > 0:
        # Step 4: Load only new data to lakeFS
        load_to_lakefs_incremental(df=new_df)
    else:
        return

    # print(f"✅ ดึงข่าวใหม่ {total_new_entries} รายการจาก {len(search_keywords)} คำค้นและบันทึกลง scrap_data.csv แล้ว")

if __name__ == "__main__":
    # scrape_news_flow_2()
    scrape_news_flow_2.from_source(
        source=Path(__file__).parent,
        entrypoint="./main_2.py:scrape_news_flow_2",
    ).deploy(
        name="scrape-news",
        work_pool_name="scrape-news",
        schedule=Interval(
            timedelta(minutes=15),
            timezone="Asia/Bangkok"
        )
    )