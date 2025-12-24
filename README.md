# 🎌 Anime Episode Provider Telegram Bot

A simple and basic  lightweight **Telegram bot** that provides **anime episodes** to users after verifying required channel subscriptions.  
The bot is designed to be fast, easy to manage, and suitable for small to medium anime communities.

---

## 📌 About the Bot

This bot allows users to:
- Start the bot using `/start`
- Subscribe to required channels
- Browse available anime
- Select and receive anime episodes directly in chat
- Get media with proper captions and buttons

It also includes **admin features** such as broadcasting messages and viewing statistics.

---

## ⚙️ Core Configuration

The bot uses the following constants for setup and control:

- `BOT_TOKEN` – Telegram bot token
- `OWNER_ID` – Bot owner/admin ID
- `SOURCE_CHANNEL_ID` – Channel where episodes are sourced from
- `REQUIRED_CHANNELS` – Channels users must join
- `DB_FILE` – Database file for storing user data
- `ANIME_EPISODES` – Anime episode mapping
- `IMAGE_URL` – Welcome or anime banner image
- `CUSTOM_BUTTON_NAMES` – Button labels for UI

---

## 🧠 Main Features

- ✅ Subscription verification system  
- 🎥 Anime episode selection menu  
- 🔁 Retry option if user is not subscribed  
- 🧾 User database management  
- 📊 Admin statistics command  
- 📢 Broadcast messages to users  
- 🖼️ Handles image-based interactions  
- ⏱️ Auto-delete messages after delay  

---

## 🧩 Functions Overview

### Database & User Management
- `setup_database()` – Initializes the database  
- `add_user()` – Adds new user  
- `remove_user()` – Removes a user  
- `get_all_users()` – Fetches all users  
- `get_blocked_users()` – Returns blocked users  
- `is_user_approved()` – Checks user access  

---

### Subscription Handling
- `check_subscription()` – Verifies required channel join  
- `send_subscription_prompt()` – Asks user to subscribe  
- `try_again()` – Retry subscription check  

---

### Bot Interaction
- `send_welcome_message()` – Sends start message  
- `handle_start()` – Handles `/start` command  
- `retry_start()` – Retry start logic  
- `show_anime_selection()` – Displays anime list  
- `send_episode_menu()` – Shows episode buttons  
- `send_episode()` – Sends selected episode  
- `delete_after_delay()` – Auto delete messages  
- `handle_picture()` – Handles image messages  

---

### Admin Commands
- `stats()` – Shows bot usage statistics  
- `broadcast()` – Sends message to all users  

---

## ▶️ How to Run the Bot

1️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

## 2️⃣ Set required constants in the code
``` bash
BOT_TOKEN = "your_bot_token"
OWNER_ID = 123456789
```

## 3️⃣ Run the bot
---
python bot.py
---

### 📁 Project Structure
``` bash
anime-episode-bot/
│
├── bot.py
├── database.db
├── requirements.txt
└── README.md
```
## 🔐 Permissions & Safety
---
Users must join required channels before accessing content
Admin-only commands are restricted using OWNER_ID
Database ensures controlled access
---

## 🛠️ Future Improvements
---
Add more anime categories
Pagination for large episode lists
Search feature
Inline query support
---
