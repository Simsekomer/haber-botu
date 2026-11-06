from config import KEYWORDS


def turkish_lower(text):
    """Lowercases text correctly for Turkish (İ -> i, I -> ı)."""
    return text.replace("İ", "i").replace("I", "ı").lower()


def is_relevant(news):
    """Checks whether the title or content contains any of the keywords."""
    text = turkish_lower(news["title"] + " " + news["content"])
    return any(keyword in text for keyword in KEYWORDS)