import os

BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    "8321125645:AAFCoHwRm2gzgIVzB-C_qKXXV7eCLzXvPBE"
)

ADMIN_ID = 5062529401

MOD_GROUP = "@ueiwiwieieissiedjdjxjzzt"
NEWS_CHANNEL = "@joonix_news"
REVIEWS_CHANNEL = "@JoonixGold_otvizi"

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com")

DEFAULT_RATE = float(os.getenv("RATE", 0.67))
REVIEW_CASHBACK = int(os.getenv("REVIEW_CASHBACK", 3))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./database.db"
)
