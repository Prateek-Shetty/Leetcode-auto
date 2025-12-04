
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.fetch_problems import fetch_problems_from_leetcode
from scripts.choose_problem import choose_today_problem
from scripts.send_telegram import send_telegram_message
from scripts.send_email import send_email_message
from scripts.db import save_to_history


def main():
    print("\n===== LeetCode Daily Automation Started =====\n")

    # -------------------------------
    # Step 1: Fetch problems from LeetCode
    # -------------------------------
    print("Fetching problems from LeetCode...")
    problems = fetch_problems_from_leetcode()

    if not problems:
        print("Failed to fetch problems. Exiting.")
        return

    print(f"Fetched {len(problems)} problems successfully.\n")

    # -------------------------------
    # Step 2: Select today's problem
    # -------------------------------
    print("Selecting today's problem...")
    today_problem = choose_today_problem()

    if not today_problem:
        print("Problem selection failed. Exiting.")
        return

    slug = today_problem["slug"]
    title = today_problem["title"]
    difficulty = today_problem["difficulty"]

    print(f"Selected problem: {title} ({difficulty})")
    print(f"Slug: {slug}\n")

    # -------------------------------
    # Step 3: Save today's problem to history
    # -------------------------------
    save_to_history(slug, title, difficulty)
    print("Saved to 100-day history.\n")

    # -------------------------------
    # Step 4: Determine delivery mode
    # -------------------------------
    DELIVERY = os.getenv("DELIVERY", "both").lower()
    print(f"Delivery mode: {DELIVERY}\n")

    # -------------------------------
    # Step 5: Send Telegram
    # -------------------------------
    if DELIVERY in ["both", "telegram"]:
        print("Sending message to Telegram...")
        send_telegram_message(title, slug)

    # -------------------------------
    # Step 6: Send Email
    # -------------------------------
    if DELIVERY in ["both", "email"]:
        print("Sending message to Email...")
        send_email_message(title, slug)

    print("\n===== Daily Automation Completed Successfully =====\n")


if __name__ == "__main__":
    main()
