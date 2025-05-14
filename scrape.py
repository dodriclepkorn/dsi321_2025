from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import time
import logging
from config_path import keywords

logger = logging.getLogger("scrape")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def search_news(keyword: str, max_pages: int = 5):
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

                    main_element = title_el.query_selector("xpath=..")
                    date_element = main_element.query_selector('[class="OSrXXb rbYSKb LfVVr"]')
                    date_text = None
                    if date_element:
                        date_text = date_element.text_content().strip()
                    else:
                        logger.warning("⚠️ ไม่มี Date")

                    if title and link and title not in seen_titles:
                        titles_links.append((title, link, date_text))
                        seen_titles.add(title)
                except Exception as e:
                    logger.error(f" Error ที่หน้า {page_num}: {e}")
                    continue

            next_button = page.query_selector('#pnnext')
            if next_button:
                try:
                    next_button.click(timeout=5000)
                    time.sleep(2)  # รอโหลดหน้าใหม่
                except Exception as e:
                    logger.warning(f" ไม่สามารถคลิกปุ่มถัดไปได้: {e}")
                    break
            else:
                break

        browser.close()
        return titles_links


def save_to_csv(data, filename="raw_scrape.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    logger.info(f" ดึงข่าวรวมได้ทั้งหมด {len(df)} หัวข้อ และบันทึกใน {filename}")


def news_scraper():
    all_results = []

    for keyword in keywords:
        logger.info(f"🔍 เริ่มค้นหาข่าวด้วยคีย์เวิร์ด: {keyword}")
        results = search_news(keyword)
        for title, link, date in results:
            all_results.append({
                "Fetched Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Keyword": keyword,
                "Title": title,
                "Link": link,
                "Date": date
            })

    save_to_csv(all_results)


if __name__ == "__main__":
    news_scraper()
