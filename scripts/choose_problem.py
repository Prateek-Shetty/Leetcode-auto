import random
from scripts.db import get_cached_problems, get_last_n_history


# Topics suitable for 3rd semester students
# We only select EASY questions from these topics.
BASIC_TOPICS = {
    "array",
    "string",
    "math",
    "hash table",
    "two pointers",
    "sorting",
    "binary search",
    "linked list",
}


def get_problem_topics(problem):
    """
    Return normalized topic names for a problem.
    """
    topics = problem.get("topicTags", [])

    if not topics:
        return set()

    return {
        topic.get("name", "").strip().lower()
        for topic in topics
        if topic.get("name")
    }


def choose_today_problem():
    """
    Choose today's problem for 5th & 7th semester.

    Existing logic:
    EASY → MEDIUM → HARD

    Excludes:
    - Paid problems
    - Problems used recently
    """

    problems = get_cached_problems()
    history_entries = get_last_n_history(60)

    history_slugs = {
        entry["slug"]
        for entry in history_entries
        if entry.get("slug")
    }

    if not problems:
        print("No problems in cache.")
        return None

    # Remove paid-only problems
    problems = [
        p for p in problems
        if not p.get("paidOnly", False)
    ]

    # Remove recently used problems
    problems = [
        p for p in problems
        if p.get("slug") not in history_slugs
    ]

    if not problems:
        print("All problems are used in recent history.")
        return None

    # Existing priority:
    # EASY → MEDIUM → HARD
    priority = ["EASY", "MEDIUM", "HARD"]

    for difficulty in priority:
        candidates = [
            p for p in problems
            if p.get("difficulty", "").upper() == difficulty
        ]

        if candidates:
            return random.choice(candidates)

    return random.choice(problems)


def choose_third_semester_problem():
    """
    Choose an Easy LeetCode problem for 3rd semester students.

    Only EASY problems from basic topics are considered.

    Basic topics:
    - Array
    - String
    - Math
    - Hash Table
    - Two Pointers
    - Sorting
    - Binary Search
    - Linked List
    """

    problems = get_cached_problems()
    history_entries = get_last_n_history(60)

    history_slugs = {
        entry["slug"]
        for entry in history_entries
        if entry.get("slug")
    }

    if not problems:
        print("No problems in cache.")
        return None

    # Only free problems
    problems = [
        p for p in problems
        if not p.get("paidOnly", False)
    ]

    # Only EASY problems
    problems = [
        p for p in problems
        if p.get("difficulty", "").upper() == "EASY"
    ]

    # Remove recently used problems
    problems = [
        p for p in problems
        if p.get("slug") not in history_slugs
    ]

    # Only basic/simple topics
    basic_candidates = []

    for problem in problems:
        problem_topics = get_problem_topics(problem)

        if problem_topics & BASIC_TOPICS:
            basic_candidates.append(problem)

    if not basic_candidates:
        print("No suitable 3rd semester Easy problem found.")
        return None

    return random.choice(basic_candidates)