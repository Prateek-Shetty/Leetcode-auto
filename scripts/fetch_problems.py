import requests

from scripts.db import save_problems_cache


GRAPHQL_QUERY_PATH = "notes/graphql_query.txt"
LEETCODE_ENDPOINT = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com"
}

PAGE_SIZE = 100
MAX_PROBLEMS = 3000


def load_graphql_query():
    """
    Load GraphQL query from file.
    """
    with open(GRAPHQL_QUERY_PATH, "r") as f:
        return f.read().strip()


def fetch_problems_from_leetcode():
    """
    Fetch LeetCode problems using pagination.

    LeetCode returns approximately 100 questions per request,
    so we fetch multiple pages until we reach MAX_PROBLEMS
    or there are no more questions.
    """

    query = load_graphql_query()

    all_questions = []
    skip = 0

    try:

        while skip < MAX_PROBLEMS:

            print(
                f"Fetching LeetCode problems "
                f"{skip + 1} - {skip + PAGE_SIZE}..."
            )

            payload = {
                "query": query,
                "variables": {
                    "categorySlug": "",
                    "skip": skip,
                    "limit": PAGE_SIZE
                }
            }

            response = requests.post(
                LEETCODE_ENDPOINT,
                json=payload,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code != 200:
                print(
                    "HTTP Error:",
                    response.status_code,
                    response.text
                )
                return None

            data = response.json()

            # Check GraphQL errors
            if data.get("errors"):
                print(
                    "GraphQL Error:",
                    data["errors"]
                )
                return None

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

            questions = block.get("questions", [])

            if not questions:
                print("No more questions found.")
                break

            all_questions.extend(questions)

            print(
                f"Received {len(questions)} questions."
            )

            # If fewer than PAGE_SIZE were returned,
            # we've reached the end.
            if len(questions) < PAGE_SIZE:
                break

            skip += PAGE_SIZE

        # Remove duplicates using titleSlug
        unique_questions = {}

        for q in all_questions:
            slug = q.get("titleSlug")

            if slug:
                unique_questions[slug] = q

        # Clean the data
        cleaned = []

        for q in unique_questions.values():

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

        # Remove paid problems
        cleaned = [
            p for p in cleaned
            if not p.get("paidOnly", False)
        ]

        print(
            f"\nTotal free problems fetched: "
            f"{len(cleaned)}"
        )

        # Show how many have topics
        with_topics = [
            p for p in cleaned
            if p.get("topicTags")
        ]

        print(
            f"Problems with topic tags: "
            f"{len(with_topics)}"
        )

        # Save to MongoDB
        save_problems_cache(cleaned)

        print(
            f"Saved {len(cleaned)} free problems "
            f"to cache."
        )

        return cleaned

    except Exception as e:

        print(
            "Fetch failed:",
            e
        )

        return None