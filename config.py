# Tag pages to scrape on TRT Haber and DHA
TRT_TAGS = ["gemi"]
DHA_TAGS = ["gemi"]

# Maximum number of articles to scrape per site in one run
NEWS_LIMIT = 10

# Seconds to wait between requests (to avoid overloading the sites)
REQUEST_DELAY = 1.5

# True: browser runs in the background, False: browser window is visible
HEADLESS = True

# How often the bot runs, in minutes (300 = 5 hours)
RUN_INTERVAL_MINUTES = 300

# Articles from general news sites are saved only if they contain one of these words
# (must be lowercase)
KEYWORDS = [
    "gemi", "tanker", "liman", "tersane", "denizcilik", "deniz ticaret",
    "armatör", "kaptan", "mürettebat", "konteyner", "feribot", "vapur",
    "navlun", "boğaz", "donanma", "denizaltı", "fırkateyn",
    "emisyon", "karbon", "lng", "lpg",
]