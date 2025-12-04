import os
import requests
from scripts.db import save_problems_cache
import json

# Load GraphQL query from notes/graphql_query.txt
GRAPHQL_QUERY_PATH = "notes/graphql_query.txt"

LEETCODE_ENDPOINT = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com"
}


def load_graphql_query():
    """
    Load the GraphQL query string from file.
    """
    with open(GRAPHQL_QUERY_PATH, "r") as f:
        return f.read().strip()


def fetch_problems_from_leetcode():
    """
    Fetch all problems from LeetCode GraphQL.
    Returns cleaned list of problems or None if request fails.
    """
    query = load_graphql_query()

    payload = {
        "query": query,
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": 3000,          # fetch everything
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
            print("GraphQL error:", response.text)
            return None

        data = response.json()

        # Path depends on your query structure
        # Most problem lists come as problemsetQuestionList.questions
        questions = data.get("data", {}) \
                        .get("problemsetQuestionList", {}) \
                        .get("questions", [])

        cleaned = []
        for q in questions:
            cleaned.append({
                "slug": q.get("titleSlug"),
                "title": q.get("title"),
                "difficulty": q.get("difficulty"),
                "paidOnly": q.get("paidOnly", False)
            })

        # Remove paid problems
        cleaned = [p for p in cleaned if p["paidOnly"] is False]

        # Save to MongoDB
        save_problems_cache(cleaned)

        return cleaned

    except Exception as e:
        print("Failed to fetch from GraphQL:", e)
        return None
