from scrapers.common import get_meta, build_news, scrape_site

SOURCE = "Deniz Haber"
HOME_URL = "https://www.denizhaber.net/"


def collect_links(page):
    page.goto(HOME_URL, wait_until="domcontentloaded", timeout=30000)

    links = page.eval_on_selector_all(
        'a[href*="-haber-"]', "elements => elements.map(a => a.href)"
    )
    links = [link for link in links if link.startswith(HOME_URL)]
    return list(dict.fromkeys(links))


def scrape_article(page, link):
    page.goto(link, wait_until="domcontentloaded", timeout=30000)

    title = get_meta(page, "og:title")
    image_url = get_meta(page, "og:image")

    date_tag = page.locator('[itemprop="datePublished"]')
    published_at = date_tag.first.get_attribute("content") if date_tag.count() else None

    paragraphs = page.locator(".text_content p").all_inner_texts()
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Remove the agency signature at the end (short and all uppercase)
    if paragraphs and paragraphs[-1].isupper() and len(paragraphs[-1]) < 40:
        paragraphs = paragraphs[:-1]

    content = "\n".join(paragraphs)

    if not title or not content:
        return None

    return build_news(title, content, link, published_at, SOURCE, None, image_url)


def scrape(limit):
    return scrape_site(SOURCE, collect_links, scrape_article, limit)