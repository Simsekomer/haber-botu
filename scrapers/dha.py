import json
import re

from config import DHA_TAGS
from scrapers.common import get_meta, build_news, scrape_site

SOURCE = "DHA"
SITE_URL = "https://www.dha.com.tr/"
TAG_URL = "https://www.dha.com.tr/haberleri/{}"

# Article links end with a dash and at least 6 digits, e.g. "-2959670"
ARTICLE_LINK_PATTERN = re.compile(r"-\d{6,}$")


def collect_links(page):
    links = []
    for tag in DHA_TAGS:
        page.goto(TAG_URL.format(tag), wait_until="domcontentloaded", timeout=30000)
        links += page.eval_on_selector_all("a", "elements => elements.map(a => a.href)")

    links = [
        link for link in links
        if link.startswith(SITE_URL) and ARTICLE_LINK_PATTERN.search(link)
    ]
    return list(dict.fromkeys(links))


def read_json_ld(page):
    """Returns the JSON-LD block that contains the article body."""
    blocks = page.locator('script[type="application/ld+json"]').all_text_contents()

    for block in blocks:
        try:
            data = json.loads(block, strict=False)
        except json.JSONDecodeError:
            continue

        candidates = data if isinstance(data, list) else data.get("@graph", [data])

        for candidate in candidates:
            if isinstance(candidate, dict) and candidate.get("articleBody"):
                return candidate

    return {}


def scrape_article(page, link):
    page.goto(link, wait_until="domcontentloaded", timeout=30000)

    info = read_json_ld(page)

    title = get_meta(page, "og:title")
    image_url = get_meta(page, "og:image")
    published_at = info.get("datePublished")
    content = info.get("articleBody")

    # Fall back to the page text if JSON-LD has no article body
    if not content:
        content = page.locator(".nd-content-column").first.inner_text()

    content = content.strip() if content else ""

    # https://www.dha.com.tr/dunya/... -> "dunya"
    category = link.replace(SITE_URL, "").split("/")[0]

    if not title or not content:
        return None

    return build_news(title, content, link, published_at, SOURCE, category, image_url)


def scrape(limit):
    return scrape_site(SOURCE, collect_links, scrape_article, limit)