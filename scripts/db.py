import os
from datetime import datetime
from pymongo import MongoClient

# Read connection string from environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect once, reuse everywhere
client = MongoClient(MONGODB_URI)
db = client["leetcode_daily"]

# Collections
problems_cache = db["problems_cache"]
daily_history = db["daily_history"]


# -------------------------
# Save all problems to cache
# -------------------------
def save_problems_cache(problems_list):
    """
    Replace the entire problems_cache with new data.
    """
    problems_cache.delete_many({})
    if problems_list:
        problems_cache.insert_many(problems_list)


# -------------------------
# Get cached problems
# -------------------------
def get_cached_problems():
    return list(problems_cache.find({}, {"_id": 0}))


# -------------------------
# Save today's selected problem
# -------------------------
def save_to_history(slug, title, difficulty):
    today = datetime.now().strftime("%Y-%m-%d")

    entry = {
        "date": today,
        "slug": slug,
        "title": title,
        "difficulty": difficulty
    }

    daily_history.insert_one(entry)

    # Keep only last 100 records
    count = daily_history.count_documents({})
    if count > 100:
        oldest = list(daily_history.find().sort("date", 1).limit(count - 100))
        for doc in oldest:
            daily_history.delete_one({"_id": doc["_id"]})


# -------------------------
# Get last N days history
# -------------------------
def get_last_n_history(n=100):
    return list(
        daily_history.find({}, {"_id": 0})
        .sort("date", -1)
        .limit(n)
    )
