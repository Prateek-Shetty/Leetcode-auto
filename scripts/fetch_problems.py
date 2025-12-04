import os
import requests
from scripts.db import save_problems_cache

GRAPHQL_QUERY_PATH = "notes/graphql_query.txt"
LEETCODE_ENDPOINT = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com"
}


def load_graphql_query():
    """
    Load GraphQL query text from file.
    """
    with open(GRAPHQL_QUERY_PATH, "r") as f:
        return f.read().strip()


def fetch_problems_from_leetcode():
    """
    Fetch LeetCode problems using problemsetQuestionListV2.
    Returns cleaned list or None on failure.
    """

    query = load_graphql_query()

    payload = {
        "query": query,
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": 3000,     # fetch everything
            "filters": {}
        }
    }

    try:
        response = requests.post(
            LEETCODE_ENDPOINT,
            json=payload,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:
            print("HTTP Error:", response.status_code, response.text)
            return None

        data = response.json()

        # Correct structure:
        block = (
            data.get("data", {})
            .get("problemsetQuestionListV2")
        )

        if not block:
            print("Invalid response structure:", data)
            return None

        questions = block.get("questions", [])

        cleaned = []
        for q in questions:
            cleaned.append({
                "slug": q.get("titleSlug"),
                "title": q.get("title"),
                "difficulty": q.get("difficulty"),
                "paidOnly": q.get("paidOnly", False)
            })

        # REMOVE PAID PROBLEMS
        cleaned = [p for p in cleaned if not p["paidOnly"]]

        save_problems_cache(cleaned)

        return cleaned

    except Exception as e:
        print("Fetch failed:", e)
        return None
