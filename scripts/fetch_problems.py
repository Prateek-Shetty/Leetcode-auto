import requests

from scripts.db import save_problems_cache


GRAPHQL_QUERY_PATH = "notes/graphql_query.txt"

LEETCODE_ENDPOINT = "https://leetcode.com/graphql"


HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com"
}


# =========================================================
# LOAD GRAPHQL QUERY
# =========================================================

def load_graphql_query():
    """
    Load GraphQL query from file.
    """

    with open(
        GRAPHQL_QUERY_PATH,
        "r"
    ) as f:

        return f.read().strip()


# =========================================================
# FETCH LEETCODE PROBLEMS
# =========================================================

def fetch_problems_from_leetcode():
    """
    Fetch LeetCode problems using GraphQL.

    Returns:
        cleaned list of problems
        or None if request fails.
    """

    query = load_graphql_query()


    payload = {
        "query": query,
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": 3000,
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


        # =================================================
        # HTTP ERROR
        # =================================================

        if response.status_code != 200:

            print(
                "HTTP Error:",
                response.status_code,
                response.text
            )

            return None


        data = response.json()


        # =================================================
        # GET PROBLEM LIST
        # =================================================

        block = (
            data
            .get("data", {})
            .get("problemsetQuestionListV2")
        )


        if not block:

            print(
                "Invalid response structure:",
                data
            )

            return None


        questions = block.get(
            "questions",
            []
        )


        # =================================================
        # CLEAN DATA
        # =================================================

        cleaned = []


        for q in questions:

            cleaned.append(
                {
                    "slug": q.get("titleSlug"),

                    "title": q.get("title"),

                    "difficulty": q.get("difficulty"),

                    "paidOnly": q.get(
                        "paidOnly",
                        False
                    ),

                    "topicTags": q.get(
                        "topicTags",
                        []
                    )
                }
            )


        # =================================================
        # REMOVE PAID PROBLEMS
        # =================================================

        cleaned = [
            problem
            for problem in cleaned
            if not problem.get(
                "paidOnly",
                False
            )
        ]


        # =================================================
        # SAVE TO MONGODB
        # =================================================

        save_problems_cache(cleaned)


        print(
            f"Saved {len(cleaned)} free problems to cache."
        )


        return cleaned


    except Exception as e:

        print(
            "Fetch failed:",
            e
        )

        return None