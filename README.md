# 🚀 LeetCode Daily Automation

Automated system that fetches daily LeetCode problems, stores them in MongoDB, selects one question for the day, and sends it to Telegram and Email using **GitHub Actions** — every morning at **7:00 AM IST**.

---

## 📌 Features

- Fetches **ALL LeetCode problems** using GraphQL
- Removes **paid-only questions**
- Saves problem list to **MongoDB Atlas**
- **Smart daily problem selector**
- Keeps **100-day history**
- Sends daily problem to:
  - **Telegram** (groups or private chat)
  - **Email**
- Fully automated with **GitHub Actions (Cron job)**
- Can run manually anytime

---

## 🏗️ Project Structure

```
Leetcode-auto/
│
├── scripts/
│   ├── daily_runner.py
│   ├── fetch_problems.py
│   ├── choose_problem.py
│   ├── send_telegram.py
│   ├── send_email.py
│   ├── db.py
│
├── notes/
│   └── graphql_query.txt
│
├── .github/
│   └── workflows/
│       └── daily.yml
│
├── requirements.txt
├── .env  (local only)
├── README.md
```

---

## ⚙️ Setup Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/Leetcode-auto.git
cd Leetcode-auto
```

### 2️⃣ Set Up MongoDB Atlas

- Go to: https://www.mongodb.com/cloud/atlas
- Create a **free cluster**
- Create a **Database User**
- **Network Access → Allow 0.0.0.0/0**
- Get connection string:

  ```
  mongodb+srv://<USER>:<PASS>@cluster.mongodb.net/leetcode_daily
  ```
  Save for GitHub secrets.

### 3️⃣ Create Your Telegram Bot

- Open Telegram
- Search `@BotFather`
- Run: `/newbot`
- Save the **BOT TOKEN**

**Get Chat / Group ID:**

- After adding the bot to your group:
- Open:
  ```
  https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
  ```
- Look for:
  ```
  "chat": { "id": -100xxxxxx }
  ```
  That id = `TELEGRAM_CHAT_ID`

### 4️⃣ Enable Gmail SMTP (If Using Email)

- Enable **2-Step Verification**  
- Create a **Gmail App Password**  
- Save it as `EMAIL_PASSWORD`

**SMTP config:**

- Host: `smtp.gmail.com`
- Port: `587`

### 5️⃣ Add GitHub Secrets

Go to:
- GitHub → Settings → Secrets → Actions → New repository secret

Add the following:

| Secret Name         | Example                        |
|---------------------|-------------------------------|
| MONGODB_URI         | mongodb+srv://…                |
| TELEGRAM_BOT_TOKEN  | 83713xxxxxx:ABC…               |
| TELEGRAM_CHAT_ID    | -1003268496696                 |
| EMAIL_FROM          | your_email@gmail.com           |
| EMAIL_TO            | receiver_email@gmail.com       |
| EMAIL_PASSWORD      | Gmail app password             |
| DELIVERY            | both / telegram / email        |
| SMTP email          | your_email@gmail.com           |
---

TELEGRAM_TOKEN
TELEGRAM_CHAT_ID
SMTP_USER
SMTP_APP_PASSWORD
EMAIL_TO
EMAIL_FROM
DELIVERY
MONGODB_URI



## 🔄 GitHub Actions Workflow

**File:** `.github/workflows/daily.yml`

Runs daily 07:00 AM IST:

```yaml
# Run every day at 07:00 AM IST
on:
  schedule:
    - cron: "30 1 * * *"
  workflow_dispatch:

jobs:
  run-daily-task:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install --no-cache-dir -r requirements.txt

      - name: Run daily script
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          SMTP_USER: ${{ secrets.EMAIL_FROM }}
          SMTP_APP_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          DELIVERY: ${{ secrets.DELIVERY }}
          MONGODB_URI: ${{ secrets.MONGODB_URI }}
        run: python scripts/daily_runner.py
```

---

## ▶️ Running Locally (Optional)

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run:**

```bash
python scripts/daily_runner.py
```

---

## 🧠 How the Automation Works

1. **Fetch Problems**
   - Uses LeetCode GraphQL
   - Saves to MongoDB `problems_cache`

2. **Choose Today's Problem**
   - Loads cache
   - Avoids duplicates for 100 days
   - Randomly selects one

3. **Save to Daily History**
   - Stores latest problem
   - Keeps last 100 only

4. **Send Notifications**
   - Telegram message
   - Email message
   - Based on your DELIVERY mode

5. **GitHub Actions Executes Daily**
   - No PC needed
   - Serverless automation

---

## 🧪 Testing Telegram Bot

- Send a message in the group.
- Refresh:
  ```
  https://api.telegram.org/bot<token>/getUpdates
  ```
- Ensure bot is **admin**.

---

## ❗ Troubleshooting

**Bot not sending messages?**

- Bot must be **admin** in group
- Chat ID must be correct
- Check getUpdates output

**GitHub action fails?**

- Check Actions → Logs
- Ensure all secrets exist
- Ensure requirements installed

**MongoDB errors?**

- Allow IP: 0.0.0.0/0
- Check password
- Check cluster is active

---

## ✨ Future Enhancements

- Multi-group broadcast
- Support Discord / Slack
- Difficulty-based schedule
- Dashboard of daily problems

---

## 🎉 Final Notes

Once everything is set:

- ✔ NO PC needed
- ✔ NO manual execution
- ✔ NO dependency on local machine
- ✔ Fully cloud-driven

Your daily **LeetCode problem** will now appear **every morning at 7 AM IST** in your **Telegram group** + **Email** (if enabled).

---