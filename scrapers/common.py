import time
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

from config import HEADLESS, REQUEST_DELAY


def get_meta(page, prop):
    """Returns the content of <meta property="...">, or None if it does not exist."""
    tag = page.locator(f'meta[property="{prop}"]')
    if tag.count() == 0:
        return None
    return tag.first.get_attribute("content")


def build_news(title, content, link, published_at, source, category, image_url):
    """Creates an article in the common format."""
    return {
        "title": title.strip(),
        "content": content,
        "link": link,
        "published_at": datetime.fromisoformat(published_at) if published_at else None,
        "source": source,
        "category": category,
        "image_url": image_url,
        "scraped_at": datetime.now(timezone.utc),
    }


def scrape_site(source, collect_links, scrape_article, limit):
    """Opens a browser, collects links and scrapes each article."""
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        try:
            links = collect_links(page)
        except Exception as error:
            print(f"[{source}] Could not open list page: {error}")
            browser.close()
            return results

        print(f"[{source}] Found {len(links)} links, scraping the first {limit}.")

        for link in links[:limit]:
            try:
                news = scrape_article(page, link)
                if news:
                    results.append(news)
                    print(f"   ✓ {news['title'][:70]}")
                else:
                    print(f"   ✗ Title or content not found: {link}")
            except Exception as error:
                print(f"   ✗ Error: {link} -> {error}")

            time.sleep(REQUEST_DELAY)

        browser.close()

    return results