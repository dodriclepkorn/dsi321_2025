from prefect import flow, task, get_run_logger
import requests
import feedparser
import csv
import os
from datetime import datetime

KEYWORDS = [
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
    "sustainable construction"
]

DATA_DIR = "news_data"
CSV_FILE = os.path.join(DATA_DIR, "news_data.csv")


@task
def create_data_folder_and_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "link", "published", "scraped_at", "keyword"])
    return CSV_FILE


@task
def load_existing_links(csv_path: str):
    existing_links = set()
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_links.add(row["link"])
    except FileNotFoundError:
        pass
    return existing_links


@task
def scrape_and_save(csv_path: str, keyword: str, existing_links: set):
    log = get_run_logger()

    query = keyword.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
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
        log.error(f"❌ Failed to fetch `{keyword}`: {e}")
        return 0

    feed = feedparser.parse(resp.content)

    if feed.bozo:
        log.warning(f"⚠️ Parsing issue (bozo=True) for `{keyword}`")
    
    entries = feed.entries
    log.info(f"🔎 Found {len(entries)} entries for `{keyword}`")

    new_count = 0
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for e in entries:
            if e.link not in existing_links:
                writer.writerow([
                    e.title,
                    e.link,
                    e.get("published", ""),
                    datetime.now().isoformat(),
                    keyword
                ])
                existing_links.add(e.link)
                new_count += 1

    log.info(f"✅ Added {new_count} new items for `{keyword}`")
    return new_count


@flow(name="scrape-news-flow")
def main():
    csv_path = create_data_folder_and_csv()
    existing_links = load_existing_links(csv_path)
    total_new = 0
    for kw in KEYWORDS:
        new_items = scrape_and_save(csv_path, kw, existing_links)
        total_new += new_items
    print(f"\n✅ Total new articles: {total_new}")


if __name__ == "__main__":
    main()
