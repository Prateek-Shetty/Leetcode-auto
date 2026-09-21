import random
from scripts.db import get_cached_problems, get_last_n_history


# Basic topics suitable for 3rd semester
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

    Priority:
    EASY → MEDIUM → HARD

    Excludes:
    - Paid problems
    - Problems used in the last 120 history records
    """

    problems = get_cached_problems()
    history_entries = get_last_n_history(120)

    history_slugs = {
        entry["slug"]
        for entry in history_entries
        if entry.get("slug")
    }

    if not problems:
        print("No problems in cache.")
        return None

    # Remove paid problems
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
        print("All problems were recently used.")
        return None

    # Existing priority
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
    Choose a problem for 3rd semester.

    Selection priority:

    1. Easy + basic topic
    2. Any Easy problem
    3. Any unused problem

    This guarantees that we return a problem as long
    as there is at least one unused problem available.
    """

    problems = get_cached_problems()
    history_entries = get_last_n_history(120)

    history_slugs = {
        entry["slug"]
        for entry in history_entries
        if entry.get("slug")
    }

    if not problems:
        print("No problems in cache.")
        return None

    # -----------------------------------------------------
    # Remove paid problems
    # -----------------------------------------------------

    problems = [
        p for p in problems
        if not p.get("paidOnly", False)
    ]

    # -----------------------------------------------------
    # Remove recently used problems
    # -----------------------------------------------------

    unused_problems = [
        p for p in problems
        if p.get("slug") not in history_slugs
    ]

    if not unused_problems:
        print(
            "No completely unused problems found. "
            "Using available problems as fallback."
        )

        unused_problems = problems

    # -----------------------------------------------------
    # PRIORITY 1
    # Easy + basic topic
    # -----------------------------------------------------

    easy_basic = []

    for problem in unused_problems:

        difficulty = problem.get(
            "difficulty",
            ""
        ).upper()

        if difficulty != "EASY":
            continue

        topics = get_problem_topics(problem)

        if topics & BASIC_TOPICS:
            easy_basic.append(problem)

    if easy_basic:

        selected = random.choice(easy_basic)

        print(
            "3rd semester selection: "
            "Easy + basic topic"
        )

        return selected

    # -----------------------------------------------------
    # PRIORITY 2
    # Any Easy problem
    # -----------------------------------------------------

    easy_problems = [
        p for p in unused_problems
        if p.get("difficulty", "").upper() == "EASY"
    ]

    if easy_problems:

        selected = random.choice(easy_problems)

        print(
            "3rd semester selection: "
            "Fallback to any Easy problem"
        )

        return selected

    # -----------------------------------------------------
    # PRIORITY 3
    # Any unused problem
    # -----------------------------------------------------

    if unused_problems:

        selected = random.choice(unused_problems)

        print(
            "3rd semester selection: "
            "Fallback to any unused problem"
        )

        return selected

    # -----------------------------------------------------
    # Final fallback
    # -----------------------------------------------------

    if problems:

        selected = random.choice(problems)

        print(
            "3rd semester selection: "
            "Final fallback"
        )

        return selected

    print("No problem available.")

    return None