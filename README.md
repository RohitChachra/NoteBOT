# 📚 Telegram Academic Resource Bot

A Telegram bot designed to help IT students access semester-wise academic resources like notes, books, assignments, and PYQs in a well-organized and user-friendly manner. Built using Python and the `python-telegram-bot` library, with SQLite for tracking user data.

## 🚀 Features

- 🎓 Semester-wise menu for quick resource access
- 🗂️ Categorized resources: Notes, Books, PYQs, Assignments
- 👥 User tracking (name, username, chat ID) stored in SQLite
- 🧠 Smart inline buttons for a seamless experience
- 📊 Admin-only logs for monitoring bot usage
- ☁️ Deployed on [Render](https://render.com)



## 🛠️ Tech Stack

- **Backend:** Python
- **Telegram Bot Framework:** `python-telegram-bot` (v20+)
- **Database:** SQLite
- **Deployment:** Render



## 👉 Try it Out Now

- ### **Telegram Bot:** https://t.me/ITnotes_bot

## 📦 Setup Locally

### 1. Clone the repository
```bash
git clone https://github.com/RohitChachra/Telegram-NoteBOT.git
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Bot Token
```bash
Create a .env file and add your bot token:
BOT_TOKEN=your_telegram_bot_token

Or, set it directly in your script securely.
```

### 5. Run the Bot
```bash
python main.py
```