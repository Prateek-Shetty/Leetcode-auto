import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from scripts.fetch_problems import fetch_problems_from_leetcode
from scripts.choose_problem import choose_today_problem
from scripts.send_telegram import send_telegram_message
from scripts.send_email import send_email_message
from scripts.db import save_to_history


def main():
    print("\n===== LeetCode Daily Automation Started =====\n")

    # STEP 1 — FETCH ALL PROBLEMS
    print("Fetching problems from LeetCode...")
    problems = fetch_problems_from_leetcode()

    if not problems:
        print("Failed to fetch problems. Exiting.")
        return

    print(f"Fetched {len(problems)} problems successfully.\n")

    # STEP 2 — CHOOSE TODAY'S PROBLEM
    print("Selecting today's problem...")
    today_problem = choose_today_problem()

    if not today_problem:
        print("Problem selection failed. Exiting.")
        return

    slug = today_problem["slug"]
    title = today_problem["title"]
    difficulty = today_problem["difficulty"]

    print(f"Selected: {title} ({difficulty})")
    print(f"Slug: {slug}\n")

    # STEP 3 — SAVE HISTORY
    save_to_history(slug, title, difficulty)
    print("Saved to 100-day history.\n")

    # STEP 4 — DELIVERY MODE
    DELIVERY = os.getenv("DELIVERY", "both").lower()
    print(f"Delivery mode: {DELIVERY}\n")

    # STEP 5 — TELEGRAM
    if DELIVERY in ["both", "telegram"]:
        print("Sending Telegram message...")
        send_telegram_message(title, slug)

    # STEP 6 — EMAIL
    if DELIVERY in ["both", "email"]:
        print("Sending Email message...")
        send_email_message(title, slug)

    print("\n===== Daily Automation Completed Successfully =====\n")


if __name__ == "__main__":
    main()
