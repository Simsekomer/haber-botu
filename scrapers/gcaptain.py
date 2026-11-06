import re

from scrapers.common import get_meta, build_news, scrape_site

SOURCE = "gCaptain"
HOME_URL = "https://gcaptain.com/"

# gcaptain.com/at-least-four-words-separated-by-dashes/
ARTICLE_LINK_PATTERN = re.compile(r"^https://gcaptain\.com/[a-z0-9]+(-[a-z0-9]+){3,}/$")


def collect_links(page):
    page.goto(HOME_URL, wait_until="domcontentloaded", timeout=30000)

    links = page.eval_on_selector_all("a", "elements => elements.map(a => a.href)")
    links = [link for link in links if ARTICLE_LINK_PATTERN.match(link)]
    return list(dict.fromkeys(links))


def scrape_article(page, link):
    page.goto(link, wait_until="domcontentloaded", timeout=30000)

    title = get_meta(page, "og:title")
    image_url = get_meta(page, "og:image")
    published_at = get_meta(page, "article:published_time")
    paragraphs = page.locator(".body > p").all_inner_texts()

    # Skip empty lines, very short lines like "(Bloomberg) —" and copyright lines
    paragraphs = [
        p.strip() for p in paragraphs
        if len(p.strip()) > 20 and not p.strip().startswith("©")
    ]

    content = "\n".join(paragraphs)

    if not title or not content:
        return None

    return build_news(title, content, link, published_at, SOURCE, None, image_url)


def scrape(limit):
    return scrape_site(SOURCE, collect_links, scrape_article, limit)