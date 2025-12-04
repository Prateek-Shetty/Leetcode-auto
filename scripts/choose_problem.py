import random
from scripts.db import get_cached_problems, get_last_n_history


def choose_today_problem():
    """
    Choose today's problem with priority:
    EASY → MEDIUM → HARD
    Excludes paid problems and last 60 days' problems.
    """

    # Load cached problems and history
    problems = get_cached_problems()
    history_entries = get_last_n_history(60)

    # Convert history to a set of slugs
    history_slugs = {entry["slug"] for entry in history_entries}

    if not problems:
        print("No problems in cache.")
        return None

    # Remove paid-only problems
    problems = [p for p in problems if not p.get("paidOnly", False)]

    # Remove problems used in last 60 days
    problems = [p for p in problems if p["slug"] not in history_slugs]

    if not problems:
        print("All problems are used in last 60 days.")
        return None

    # Priority: EASY → MEDIUM → HARD
    priority = ["EASY", "MEDIUM", "HARD"]

    for diff in priority:
        candidates = [
            p for p in problems
            if p.get("difficulty", "").upper() == diff
        ]
        if candidates:
            return random.choice(candidates)

    # Fallback if none match difficulty (unlikely)
    return random.choice(problems)
