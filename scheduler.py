import schedule
import time
from scraper import scrape_data
from datetime import datetime

# ✅ Global logs list
logs = []

def job():
    try:
        logs.append("🔄 Scraping started...")

        df = scrape_data()

        logs.append(f"✅ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Scraped {len(df)} records")

    except Exception as e:
        logs.append(f"❌ Error: {e}")

def start_scheduler():
    logs.append("🚀 Scheduler started successfully!")

    # Schedule scraper every 1 minute
    schedule.every(1).minutes.do(job)

    # Run immediately once (IMPORTANT FIX)
    job()

    while True:
        schedule.run_pending()
        time.sleep(1)