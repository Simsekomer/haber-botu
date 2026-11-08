import time
from datetime import datetime
import os
import schedule

from config import NEWS_LIMIT, RUN_INTERVAL_MINUTES
from scrapers import trthaber, denizhaber, dha, gcaptain
from filters import is_relevant
from db import save_news

SCRAPERS = [trthaber, denizhaber, dha, gcaptain]

# Sources whose articles must pass the keyword filter
FILTERED_SCRAPERS = [dha]


def run():
    all_news = []

    for scraper in SCRAPERS:
        try:
            results = scraper.scrape(NEWS_LIMIT)
        except Exception as error:
            print(f"[{scraper.SOURCE}] Failed: {error}")
            continue

        for news in results:
            if scraper in FILTERED_SCRAPERS and not is_relevant(news):
                print(f"   ⊘ Not relevant, skipped: {news['title'][:70]}")
                continue
            all_news.append(news)

    new_count = 0
    for news in all_news:
        if save_news(news):
            new_count += 1

    print(f"\nScraped {len(all_news)} articles, {new_count} of them are new.")


def run_safely():
    """Runs the bot without stopping the scheduler if an error occurs."""
    print(f"\n===== Bot running: {datetime.now():%d.%m.%Y %H:%M} =====")
    try:
        run()
    except Exception as error:
        print(f"Unexpected error: {error}")
    print(f"Next run in {RUN_INTERVAL_MINUTES} minutes. Press Ctrl + C to stop.")


if __name__ == "__main__":
    if os.getenv("RUN_ONCE") == "true":
        run()
    else:
        run_safely()
        schedule.every(RUN_INTERVAL_MINUTES).minutes.do(run_safely)
        while True:
            schedule.run_pending()
            time.sleep(30)