import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from dotenv import load_dotenv

load_dotenv()

from scripts.fetch_problems import fetch_problems_from_leetcode
from scripts.choose_problem import (
    choose_today_problem,
    choose_third_semester_problem
)
from scripts.send_telegram import send_telegram_message
from scripts.send_email import send_email_message
from scripts.db import save_to_history


def main():

    print("\n===== LeetCode Daily Automation Started =====\n")

    # =========================================================
    # STEP 1 — FETCH ALL PROBLEMS
    # =========================================================

    print("Fetching problems from LeetCode...")

    problems = fetch_problems_from_leetcode()

    if not problems:
        print("Failed to fetch problems. Exiting.")
        return

    print(f"Fetched {len(problems)} problems successfully.\n")


    # =========================================================
    # STEP 2 — SELECT 5th & 7th SEMESTER PROBLEM
    # =========================================================

    print("Selecting problem for 5th & 7th semester...")

    problem_57 = choose_today_problem()

    if not problem_57:
        print("5th & 7th semester problem selection failed.")
        return

    slug_57 = problem_57["slug"]
    title_57 = problem_57["title"]
    difficulty_57 = problem_57["difficulty"]

    print(
        f"5th & 7th Semester: "
        f"{title_57} ({difficulty_57})"
    )
    print(f"Slug: {slug_57}\n")


    # =========================================================
    # STEP 3 — SELECT 3rd SEMESTER PROBLEM
    # =========================================================

    print("Selecting Easy problem for 3rd semester...")

    problem_3 = choose_third_semester_problem()

    if not problem_3:
        print("3rd semester problem selection failed.")
        return

    slug_3 = problem_3["slug"]
    title_3 = problem_3["title"]
    difficulty_3 = problem_3["difficulty"]

    print(
        f"3rd Semester: "
        f"{title_3} ({difficulty_3})"
    )
    print(f"Slug: {slug_3}\n")


    # =========================================================
    # STEP 4 — SAVE BOTH PROBLEMS TO HISTORY
    # =========================================================

    save_to_history(
        slug_57,
        title_57,
        difficulty_57,
        semester="5_7"
    )

    save_to_history(
        slug_3,
        title_3,
        difficulty_3,
        semester="3"
    )

    print("Both problems saved to history.\n")


    # =========================================================
    # STEP 5 — DELIVERY MODE
    # =========================================================

    delivery = os.getenv("DELIVERY", "both").lower()

    print(f"Delivery mode: {delivery}\n")


    # =========================================================
    # STEP 6 — TELEGRAM
    # =========================================================

    if delivery in ["both", "telegram"]:

        print("Sending Telegram message for 5th & 7th semester...")

        send_telegram_message(
            f"🎓 5th & 7th Semester\n\n"
            f"📌 {title_57}\n"
            f"Difficulty: {difficulty_57}",
            slug_57
        )


        print("Sending Telegram message for 3rd semester...")

        send_telegram_message(
            f"🎓 3rd Semester\n\n"
            f"📌 {title_3}\n"
            f"Difficulty: {difficulty_3}",
            slug_3
        )


    # =========================================================
    # STEP 7 — EMAIL
    # =========================================================

    if delivery in ["both", "email"]:

        print("Sending Email for 5th & 7th semester...")

        send_email_message(
            title_57,
            slug_57
        )


        print("Sending Email for 3rd semester...")

        send_email_message(
            title_3,
            slug_3
        )


    print("\n===== Daily Automation Completed Successfully =====\n")


if __name__ == "__main__":
    main()