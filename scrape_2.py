from prefect import flow, task
from playwright.sync_api import sync_playwright
from prefect.schedules import Interval
from datetime import timedelta
from pathlib import Path
import pandas as pd
from datetime import datetime
import time
import logging
from config_path import keywords

logger = logging.getLogger("scrape")
logger.setLevel('INFO')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

@task(name="Search News")
def search_news(keyword: str, max_pages: int = 1):  # ให้รัน 1 หน้า เพราะได้ข่าวใหม่โดยใช้ลิงก์แบบเรียงล่าสุดอยู่แล้ว
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&tbm=nws&tbs=sbd:1"
        page.goto(search_url)

        titles_links = []
        seen_titles = set()

        for page_num in range(1, max_pages + 1):
            logger.info(f"📄 กำลังประมวลผลหน้าที่ {page_num}")
            time.sleep(2)
            page.keyboard.press("End")
            time.sleep(2)

            titles = page.query_selector_all('div[role="heading"][aria-level="3"]')
            for title_el in titles:
                try:
                    title = title_el.text_content().strip()
                    a_tag = title_el.query_selector("xpath=ancestor::a")
                    link = a_tag.get_attribute("href") if a_tag else None

                    # 🟩 เพิ่มส่วนดึงวันที่
                    main_element = title_el.query_selector("xpath=..")
                    date_element = main_element.query_selector('[class="OSrXXb rbYSKb LfVVr"]')
                    date_text = None
                    if date_element:
                        date_text = date_element.text_content().strip()
                    else:
                        logger.error("ไม่มี Date")

                    if title and link and title not in seen_titles:
                        titles_links.append((title, link, date_text))  # 🟩 เพิ่ม date_text
                        seen_titles.add(title)
                except Exception as e:
                    logger.error(f"❌ Error ที่หน้า {page_num}: {e}")
                    continue

            next_button = page.query_selector('#pnnext')
            if next_button:
                next_button.click()
            else:
                break

        browser.close()
        return titles_links

@task(name="save to csv")
def save_to_csv(data, filename="new_scrape.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    logger.info(f"✅ ดึงข่าวรวมได้ทั้งหมด {len(df)} หัวข้อ และบันทึกใน {filename}")

@flow(name="incremental flow")
def news_scraper_flow():
    all_results = []

    for keyword in keywords:
        results = search_news(keyword)
        for title, link, date in results:  # 🟩 เพิ่ม date
            all_results.append({
                "Fetched Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Keyword": keyword,
                "Title": title,
                "Link": link,
                "Date": date  # 🟩 บันทึกวันที่ลง CSV
            })

    save_to_csv(all_results)

if __name__ == "__main__":
    news_scraper_flow.from_source(
        source=Path(__file__).parent,
        entrypoint="./scrape_2.py:news_scraper_flow",
    ).deploy(
        name="incremental flow",
        work_pool_name="scrape-news",
        schedule=Interval(
            timedelta(minutes=2),
            timezone="Asia/Bangkok"
        )
    )