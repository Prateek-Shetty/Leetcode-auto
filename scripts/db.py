import os
from datetime import datetime
from pymongo import MongoClient


# =========================================================
# MONGODB CONNECTION
# =========================================================

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client["leetcode_daily"]


# =========================================================
# COLLECTIONS
# =========================================================

problems_cache = db["problems_cache"]

daily_history = db["daily_history"]


# =========================================================
# SAVE ALL PROBLEMS TO CACHE
# =========================================================

def save_problems_cache(problems_list):
    """
    Replace the entire problems cache with fresh data.
    """

    problems_cache.delete_many({})

    if problems_list:
        problems_cache.insert_many(problems_list)


# =========================================================
# GET CACHED PROBLEMS
# =========================================================

def get_cached_problems():
    """
    Return all cached LeetCode problems.
    """

    return list(
        problems_cache.find(
            {},
            {"_id": 0}
        )
    )


# =========================================================
# SAVE SELECTED PROBLEM TO HISTORY
# =========================================================

def save_to_history(
    slug,
    title,
    difficulty,
    semester=None
):
    """
    Save selected problem to daily history.

    semester:
        5_7 = 5th & 7th semester
        3   = 3rd semester
    """

    today = datetime.now().strftime("%Y-%m-%d")

    entry = {
        "date": today,
        "slug": slug,
        "title": title,
        "difficulty": difficulty,
        "semester": semester
    }

    daily_history.insert_one(entry)


    # =====================================================
    # KEEP ONLY LAST 100 RECORDS
    # =====================================================

    count = daily_history.count_documents({})

    if count > 120:

        oldest = list(
            daily_history
            .find()
            .sort("date", 1)
            .limit(count - 120)
        )

        for doc in oldest:
            daily_history.delete_one(
                {
                    "_id": doc["_id"]
                }
            )


# =========================================================
# GET LAST N HISTORY RECORDS
# =========================================================

def get_last_n_history(n=100):
    """
    Return the latest N history records.
    """

    return list(
        daily_history
        .find(
            {},
            {"_id": 0}
        )
        .sort("date", -1)
        .limit(n)
    )