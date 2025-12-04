import random
from datetime import datetime
from scripts.db import get_cached_problems, get_last_n_history


# ------------------------------
# Weighted difficulty selection
# ------------------------------
def pick_difficulty():
    # Easy 50%, Medium 40%, Hard 10%
    choices = ["Easy", "Medium", "Hard"]
    weights = [0.50, 0.40, 0.10]
    return random.choices(choices, weights)[0]


# ------------------------------
# Main problem selection logic
# ------------------------------
def choose_today_problem():
    # Load cached problems from MongoDB
    problems = get_cached_problems()
    if not problems:
        print("No cached problems found!")
        return None

    # Separate by difficulty
    easy = [p for p in problems if p["difficulty"] == "Easy"]
    medium = [p for p in problems if p["difficulty"] == "Medium"]
    hard = [p for p in problems if p["difficulty"] == "Hard"]

    # Choose a difficulty
    difficulty = pick_difficulty()

    if difficulty == "Easy":
        pool = easy
    elif difficulty == "Medium":
        pool = medium
    else:
        pool = hard

    if not pool:
        print(f"No problems available for difficulty: {difficulty}")
        return None

    # ---------------------------------------
    # Seed randomness using today's date  
    # Ensures deterministic daily choice
    # ---------------------------------------
    today_seed = int(datetime.now().strftime("%Y%m%d"))
    random.seed(today_seed)

    # Pick a random problem
    selected = random.choice(pool)

    # ---------------------------------------
    # 100-day no-repeat logic
    # ---------------------------------------
    recent = get_last_n_history(100)
    recent_slugs = [p["slug"] for p in recent]

    if selected["slug"] in recent_slugs:
        print("Duplicate detected, choosing next available problem...")
        
        # Pick next problem in the pool list
        # Rotate through until we find a non-duplicate
        for p in pool:
            if p["slug"] not in recent_slugs:
                selected = p
                break
        # If everything is a duplicate (rare), just allow
        # But this will almost never happen because LeetCode has 2,500+ problems

    # ---------------------------------------
    # Return final selected problem
    # ---------------------------------------
    return {
        "slug": selected["slug"],
        "title": selected["title"],
        "difficulty": selected["difficulty"]
    }
