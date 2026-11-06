import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
news_collection = db["news"]

# The same link cannot be saved twice
news_collection.create_index("link", unique=True)


def save_news(news):
    """Saves an article. Returns True if saved, False if it already exists."""
    try:
        news_collection.insert_one(news)
        return True
    except errors.DuplicateKeyError:
        return False