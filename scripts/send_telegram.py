import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


def send_telegram_message(title, slug):
    """
    Sends formatted LeetCode daily challenge message to Telegram.
    """

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing!")
        return False

    problem_url = f"https://leetcode.com/problems/{slug}/"

    text = (
        f"Today's LeetCode Problem: {title}\n"
        f"{problem_url}\n\n"
        f"Dear students, please find the daily challenge posted for today ☝"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(SEND_MESSAGE_URL, json=payload)
        if response.status_code == 200:
            print("Telegram: Message sent successfully.")
            return True
        else:
            print("Telegram Error:", response.text)
            return False

    except Exception as e:
        print("Telegram Exception:", e)
        return False
