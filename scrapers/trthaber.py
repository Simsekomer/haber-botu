from config import TRT_TAGS
from scrapers.common import get_meta, build_news, scrape_site

SOURCE = "TRT Haber"
TAG_URL = "https://www.trthaber.com/etiket/{}/"


def collect_links(page):
    links = []
    for tag in TRT_TAGS:
        page.goto(TAG_URL.format(tag), wait_until="domcontentloaded", timeout=30000)
        links += page.eval_on_selector_all(
            "div.title a.site-url", "elements => elements.map(a => a.href)"
        )

    # Keep only written articles (skip /videolar/ and /foto-galeri/)
    links = [link for link in links if "/haber/" in link]
    return list(dict.fromkeys(links))


def scrape_article(page, link):
    page.goto(link, wait_until="domcontentloaded", timeout=30000)

    # The page may load more articles below, take only the first one
    box = page.locator(".news-content-container").first

    title = get_meta(page, "og:title")
    image_url = get_meta(page, "og:image")
    published_at = box.locator("input.page-date-published").get_attribute("value")
    category = box.locator("input.page-category-name").get_attribute("value")
    paragraphs = box.locator(".news-content p").all_inner_texts()

    content = "\n".join(p.strip() for p in paragraphs if p.strip())

    if not title or not content:
        return None

    return build_news(title, content, link, published_at, SOURCE, category, image_url)


def scrape(limit):
    return scrape_site(SOURCE, collect_links, scrape_article, limit)