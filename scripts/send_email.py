import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_USER = os.getenv("SMTP_USER")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)
EMAIL_TO = os.getenv("EMAIL_TO")


def send_email_message(title, slug):
    """
    Sends formatted daily LeetCode problem through Gmail SMTP.
    """

    if not SMTP_USER or not SMTP_APP_PASSWORD or not EMAIL_TO:
        print("Email credentials missing!")
        return False

    problem_url = f"https://leetcode.com/problems/{slug}/"

    # Email content
    subject = f"Today's LeetCode Problem: {title}"

    body = (
        f"Today's LeetCode Problem: {title}\n"
        f"{problem_url}\n\n"
        f"Dear students, please find the daily challenge posted for today ☝"
    )

    try:
        # Construct MIME message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SMTP_USER, SMTP_APP_PASSWORD)

        # Send email
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()

        print("Email: Sent successfully.")
        return True

    except Exception as e:
        print("Email Error:", e)
        return False
