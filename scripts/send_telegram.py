import os
import requests


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SEND_MESSAGE_URL = (
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
)


def send_telegram_message(title, slug):
    """
    Send a LeetCode problem to Telegram.
    """

    # -----------------------------------------------------
    # Check credentials
    # -----------------------------------------------------

    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN is missing.")
        return False

    if not TELEGRAM_CHAT_ID:
        print("ERROR: TELEGRAM_CHAT_ID is missing.")
        return False

    print("Telegram credentials found.")
    print(f"Telegram Chat ID: {TELEGRAM_CHAT_ID}")

    # -----------------------------------------------------
    # Build LeetCode URL
    # -----------------------------------------------------

    problem_url = (
        f"https://leetcode.com/problems/{slug}/"
    )

    # -----------------------------------------------------
    # Message
    # -----------------------------------------------------

    text = (
        f"{title}\n\n"
        f"🔗 {problem_url}\n\n"
        f"Dear students, please find the daily challenge "
        f"posted for today ☝"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    # -----------------------------------------------------
    # Send message
    # -----------------------------------------------------

    try:

        print("Sending message to Telegram...")

        response = requests.post(
            SEND_MESSAGE_URL,
            json=payload,
            timeout=20
        )

        print(
            f"Telegram HTTP Status: "
            f"{response.status_code}"
        )

        print(
            f"Telegram Response: "
            f"{response.text}"
        )

        if response.status_code == 200:

            result = response.json()

            if result.get("ok") is True:
                print(
                    "Telegram: Message sent successfully."
                )
                return True

            print(
                "Telegram API returned ok=false."
            )
            return False

        print(
            "Telegram Error: "
            f"{response.text}"
        )

        return False

    except requests.exceptions.RequestException as e:

        print(
            "Telegram Request Exception:",
            e
        )

        return False

    except Exception as e:

        print(
            "Telegram Exception:",
            e
        )

        return False