
import logging
import asyncio
import sqlite3
from dns import update
from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext.filters import Caption

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "YOUR_TOKEN"
SOURCE_CHANNEL_ID = -1002282698270
REQUIRED_CHANNELS = {
    "public_channels": [
        "@THE_GODS_NETWORK",
        "@GOD_TERMINATORS"
    ],
    "private_channels": [
        {"name": "Otaku Heavens", "invite_link": "https://t.me/+xxxxxxxxx"},
        {"name": "Manga No Kami", "invite_link": "https://t.me/+xxxxxxxxx"}
    ]
}

OWNER_ID = 715958xxxx
DB_FILE = "users.db"




ANIME_EPISODES = {
    "Sᴏʟᴏ Lᴇᴠᴇʟɪɴɢ S𝟸": {
        "image": "https://files.catbox.moe/oxlmds.jpg",
        "caption": "⚔️Sᴏʟᴏ Lᴇᴠᴇʟɪɴɢ Sᴇᴀsᴏɴ 𝟸 -{𝗪𝗵𝗲𝗻 𝘁𝗵𝗲 𝗼𝗻𝗹𝘆 𝘄𝗮𝘆 𝘁𝗼 𝘀𝘂𝗿𝘃𝗶𝘃𝗲 𝗶𝘀 𝘁𝗼 𝗯𝗲𝗰𝗼𝗺𝗲 𝘂𝗻𝘀𝘁𝗼𝗽𝗽𝗮𝗯𝗹𝗲.}",
        "episodes": {
            "Eᴘɪsᴏᴅᴇ 𝟷": 13,
            "Eᴘɪsᴏᴅᴇ 𝟸": 14,
            "Eᴘɪsᴏᴅᴇ 𝟹": 15,
            "Eᴘɪsᴏᴅᴇ 𝟺": 16,
            "Eᴘɪsᴏᴅᴇ 𝟻": 17,
            "Eᴘɪsᴏᴅᴇ 𝟼": 18,
            "Eᴘɪsᴏᴅᴇ 𝟽": 19,

        }
    },
    "Demon Slayer": {
        "image": "https://files.catbox.moe/yy5xr1.jpg",
        "caption": "🔥Demon Slayer - A story of demons and hunters in a world of bloodshed.",
        "episodes": {
            "1️⃣ Episode 1": 10,
            "2️⃣ Episode 2": 11,
        }
    }
}

caption = ANIME_EPISODES["Sᴏʟᴏ Lᴇᴠᴇʟɪɴɢ S𝟸"]["caption"]




def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, approved INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def is_user_approved(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT approved FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1  # Returns True if approved


async def check_subscription(user_id: int, context: CallbackContext) -> bool:
    for channel in REQUIRED_CHANNELS["public_channels"]:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"Error checking public channel {channel} for {user_id}: {e}")
            return False

    for channel in REQUIRED_CHANNELS["private_channels"]:
        try:
            if "id" in channel:
                member = await context.bot.get_chat_member(chat_id=channel["id"], user_id=user_id)
                if member.status not in ["member", "administrator", "creator"]:
                    return False
        except Exception as e:
            print(f"Error checking private channel for {user_id}: {e}")
            return False

    return True


#  Function to Send Subscription Prompt
IMAGE_URL = "https://files.catbox.moe/o9qzow.jpg"  # Replace with your actual image URL

# Dictionary to map channel usernames to button names
CUSTOM_BUTTON_NAMES = {
    "@THE_GODS_NETWORK": "Tʜᴇ Gᴏᴅs Nᴇᴛᴡᴏʀᴋ",
    "@GOD_TERMINATORS": "Gᴏᴅ Tᴇʀᴍɪɴᴀᴛᴏʀs",
    "private_channel_1": "𝖬𝖺𝗇𝗀𝖺 𝖭𝗈 𝖪𝖺𝗆𝗂۝"
}

async def send_subscription_prompt(update: Update, context: CallbackContext, user_id: int):
    """Sends an image with a subscription prompt, caption, and custom join buttons."""

    keyboard = []

    # Add public channel join buttons
    public_buttons = [
        InlineKeyboardButton(
            CUSTOM_BUTTON_NAMES.get(channel.strip(), f"📢 {channel.replace('@', '')}"),
            url=f"https://t.me/{channel.strip()[1:]}"
        ) for channel in REQUIRED_CHANNELS["public_channels"]
    ]

    if len(public_buttons) == 2:
        keyboard.append(public_buttons)  # Adds both buttons in one row
    else:
        for button in public_buttons:
            keyboard.append([button])  # Keep individual rows if only one button

    #  Add private buttons for "Otaku Heavens" and "Manga No Kami"
    private_channels = REQUIRED_CHANNELS["private_channels"]
    otaku_heavens = next((ch["invite_link"] for ch in private_channels if ch["name"] == "Otaku Heavens"), None)
    manga_no_kami = next((ch["invite_link"] for ch in private_channels if ch["name"] == "Manga No Kami"), None)

    if otaku_heavens:
        keyboard.append([InlineKeyboardButton("𝐎𝐓𝐀𝐊𝐔 天国 𝐇𝐞𝐚𝐯𝐞𝐧𝐬 ⛩", url=otaku_heavens)])

    if manga_no_kami:
        keyboard.append([InlineKeyboardButton("𝖬𝖺𝗇𝗀𝖺 𝖭𝗈 𝖪𝖺𝗆𝗂۝", url=manga_no_kami)])

    #  "Try Again" button
    keyboard.append([InlineKeyboardButton("🔄 Tʀʏ Aɢᴀɪɴ", callback_data="retry_start")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_photo(
            chat_id=user_id,
            photo=IMAGE_URL,
            caption="*🎌 Wᴀɪᴛ ᴀ sᴇᴄ! (≧◡≦)*\n\n"
                    "*⚠️ Yᴏᴜ’ʀᴇ ᴍɪssɪɴɢ sᴏᴍᴇᴛʜɪɴɢ ɪᴍᴘᴏʀᴛᴀɴᴛ! "
                    "Jᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ, ᴏ-ᴏᴋᴀʏ? (｡•́︿•̀｡)*\n\n"
                    "*✅ Cʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴀɴᴅ ᴅᴏ ɪᴛ ᴘʀᴏᴘᴇʀʟʏ, ᴏᴋᴀʏ?*\n"
                    "*🔄 Oɴᴄᴇ ʏᴏᴜ’ʀᴇ ᴅᴏɴᴇ, ᴘʀᴇss [Tʀʏ Aɢᴀɪɴ]! I’ʟʟ ʙᴇ ᴡᴀɪᴛɪɴɢ… (//ω//)*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"Error sending message: {e}")



#  Function to Send Miku Nakano Welcome Message
async def send_welcome_message(update: Update, context: CallbackContext, user_id: int):
    """Sends the Miku Nakano-themed welcome message with a clickable Best Friend link."""

    # Ensure callback queries are answered to prevent timeout issues
    if update.callback_query:
        await update.callback_query.answer()

    best_friend = f'<a href="https://t.me/THE_GOD_OF_SKY">𓆰 𝙕𝙀𝙐𝙎⚡️❰ ⏤͟͞𝐆𝐎𝐃𝐒 ༒ ❱</a>'

    miku_nakano = f'<a href="https://t.me/NakanoXmiku_bot">❍-𝗡ᴀᴋᴀɴᴏ 𝗠ɪᴋᴜ (っ◔◡◔)っ</a>'

    welcome_message = f"""❍ 𝘼𝙝… 𝙪𝙢… 𝙬𝙚𝙡𝙘𝙤𝙢𝙚 💘{update.effective_user.mention_html()} 
    ⧫━━━━━━━━━━━━━━━━━━━━━⧫  
    ❍ Hᴇʏ-Iᴛ's ᴍᴇ… 𓂃 『 {miku_nakano} 』🎧\n
    ➥ -Iᴛ's ɴᴏᴛ ʟɪᴋᴇ I ᴡᴀs ᴡᴀɪᴛɪɴɢ ғᴏʀ ʏᴏᴜ ᴏʀ ᴀɴʏᴛʜɪɴɢ… ʙ-ʙᴜᴛ ɴᴏᴡ ᴛʜᴀᴛ ʏᴏᴜ'ʀᴇ ʜᴇʀᴇ,
    ➥  ʏᴏᴜ ᴄᴀɴ ᴡᴀᴛᴄʜ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ᴀɴɪᴍᴇ ᴇᴘɪsᴏᴅᴇs ᴀɴʏᴛɪᴍᴇ. I’ʟʟ ᴛʀʏ ᴍʏ ʙᴇsᴛ ᴛᴏ ʜᴇʟᴘ…
      sᴏ, ᴘʟᴇᴀsᴇ ʙᴇ ᴘᴀᴛɪᴇɴᴛ ᴡɪᴛʜ ᴍᴇ. (//ω//)\n
    ┏━━━━━━━━━━━━━━━━━━━━⧫
    ┠ ◆ 𝐌𝐲 𝐁𝐞𝐬𝐭 💕𝐅𝐫𝐢𝐞𝐧𝐝 𝐈𝐬 :- {best_friend}
    ┠ ◆ 𝗧𝗮𝗽 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝗲𝘅𝗽𝗹𝗼𝗿𝗲 𝗮𝗻𝗶𝗺𝗲 𝗲𝗽𝗶𝘀𝗼𝗱𝗲𝘀!🎬
    ┠ ◆ 𝗗-𝗗𝗼 𝘆𝗼𝘂 𝗹𝗼𝘃𝗲 𝗮𝗻𝗶𝗺𝗲… 𝗹𝗶𝗸𝗲 𝗜 𝗱𝗼? (´・ω・｀)
    ┗━━━━━━━━━━━━━━━━━━━━⧫"""

    image_url = "https://files.catbox.moe/2bvr5z.jpg"  

    keyboard = [[InlineKeyboardButton(" 「 Anime 」", callback_data="anime_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=user_id,
        photo=image_url,
        caption=welcome_message,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

    print(f" Sent welcome message to {user_id}")






#  Handling the "Try Again" Button
async def try_again(update: Update, context: CallbackContext):
    """Handles the 'Try Again' button to recheck subscription and send appropriate messages."""
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()  # Acknowledge button press

    is_subscribed = await check_subscription(user_id, context)

    if is_subscribed:
        await send_welcome_message(update, context, user_id)  # Send welcome if subscribed
    else:
        await send_subscription_prompt(update, context, user_id)  # Resend join message
        await context.bot.send_message(
            chat_id=user_id,
            text="⚠️ *You have to join all channels first before trying again!*",
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_start(update: Update, context: CallbackContext):
    """Handles the /start command, checking subscription before welcoming."""
    user_id = update.message.from_user.id
    print(f"/start triggered by {user_id}")

    if await check_subscription(user_id, context):
        print(f"User {user_id} is verified. Sending welcome message.")
        await send_welcome_message(user_id, context)
    else:
        print(f"User {user_id} is not verified. Sending subscription prompt.")
        await send_subscription_prompt(user_id, context)  # Pass only 2 arguments


async def retry_start(update: Update, context: CallbackContext):
    """Handles the 'Try Again' button to recheck subscription and send appropriate messages."""

    query = update.callback_query  # Get callback query
    user_id = query.from_user.id  # Extract user ID

    await query.answer()  # Acknowledge button press to avoid stuck UI

    # Recheck subscription status
    is_subscribed = await check_subscription(user_id, context)

    if is_subscribed:
        print(f"✅ User {user_id} is subscribed. Sending welcome message.")
        await send_welcome_message(update, context, user_id)
    else:
        print(f"❌ User {user_id} is NOT subscribed. Sending join prompt again.")
        await send_subscription_prompt(update, context, user_id)

        # Inform the user they still need to join channels
        await context.bot.send_message(
            chat_id=user_id,
            text=" 💖 * Nʏᴀᴀ~! Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ Jᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ғɪʀsᴛ ʙᴇғᴏʀᴇ ᴛʀʏɪɴɢ ᴀɢᴀɪɴ!\n "
                 "Hᴜʀʀʏ, ʜᴜʀʀʏ~! Tʜᴇɴ ᴡᴇ ᴄᴀɴ ʜᴀᴠᴇ ʟᴏᴛs ᴏғ ғᴜɴ ᴛᴏɢᴇᴛʜᴇʀ! (≧ω≦)*🎀",
            parse_mode=ParseMode.MARKDOWN
        )


async def start(update: Update, context: CallbackContext):
    """Handles /start and checks subscriptions."""

    print("Start command received")  # Debugging output

    user_id = update.effective_chat.id
    print(f"User ID: {user_id}")  # Debugging output

    add_user(user_id)

    if user_id == OWNER_ID:
        await update.message.reply_text("👑𝗪𝗲𝗹𝗰𝗼𝗺𝗲, 𝗔𝗻𝘀𝗵-𝗸𝘂𝗻! 🌸🎶 𝗟𝗲𝘁’𝘀 𝗵𝗮𝘃𝗲 𝗮 𝗳𝘂𝗻 𝘁𝗶𝗺𝗲 𝘁𝗼𝗴𝗲𝘁𝗵𝗲𝗿! 🎤💖...")
        return

    # Subscription Check
    is_subscribed = await check_subscription(user_id, context)

    if not is_subscribed:
        print(f"❌ User {user_id} is not subscribed. Sending join prompt.")
        await send_subscription_prompt(update, context, user_id)
        return

    print(f"✅ User {user_id} is subscribed. Sending welcome message.")
    await send_welcome_message(update, context, user_id)  # ✅ Pass user_id properly


async def show_anime_selection(update: Update, context: CallbackContext):
    """Displays the anime selection menu when the 'Anime' button is clicked."""
    query = update.callback_query
    await query.answer()

    # Generate anime selection buttons
    keyboard = [[InlineKeyboardButton(name, callback_data=f"anime_{name}")] for name in ANIME_EPISODES.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_caption(
        caption="H-Hᴇʏ, ʙᴀᴋᴀ! (≧◡≦)~ W-Wʜʏ ᴀʀᴇ ʏᴏᴜ Jᴜsᴛ sᴛᴀɴᴅɪɴɢ ᴛʜᴇʀᴇ? \n"
                "P-Pɪᴄᴋ ᴀɴ ᴀɴɪᴍᴇ ᴀʟʀᴇᴀᴅʏ! I-I ᴅᴏɴ'ᴛ ᴄᴀʀᴇ ᴡʜᴀᴛ ʏᴏᴜ ᴄʜᴏᴏsᴇ… (//ω//)\n\n"
    "💞 S-Sᴏ, ᴡ-ᴡʜɪᴄʜ ᴏɴᴇ ᴡɪʟʟ ʏᴏᴜ ᴄʜᴏᴏsᴇ? HURRY UP! I-I’ᴍ ɴᴏᴛ ʙʟᴜsʜɪɴɢ, ᴏᴋᴀʏ?!(ノωヽ)",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def send_episode_menu(update: Update, context: CallbackContext):
    """Sends the episode selection menu for a chosen anime."""
    query = update.callback_query
    anime_name = query.data.split("_")[1]  # Extract anime name
    await query.answer()

    # Ensure the anime exists
    if anime_name not in ANIME_EPISODES:
        await query.message.reply_text("❌ Anime not found.")
        return

    anime_data = ANIME_EPISODES[anime_name]  # Get anime details

    # Generate episode selection buttons
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"episode_{anime_name}_{msg_id}")]
        for name, msg_id in anime_data["episodes"].items()
    ]
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="anime_menu")])  # Back button for episodes
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ensure caption is sent correctly
    await query.message.edit_media(
        media={"type": "photo", "media": anime_data["image"], "caption": f"{anime_data['caption']}"},
        reply_markup=reply_markup,
    )


async def send_episode(update: Update, context: CallbackContext):
    """Sends the requested episode."""
    query = update.callback_query
    _, anime_name, episode_id = query.data.split("_")
    episode_id = int(episode_id)
    await query.answer()

    try:
        sent_msg = await context.bot.copy_message(
            chat_id=query.from_user.id,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=episode_id
        )
        warning_msg = await context.bot.send_message(
            query.from_user.id,
            " 🪽💫Tʜɪs ᴇᴘɪsᴏᴅᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ 𝟸 ᴍɪɴᴜᴛᴇs! ✨ Fᴏʀᴡᴀʀᴅ ɪᴛ ɴᴏᴡ! ɪɴ Sᴏᴍᴇᴡʜᴇʀᴇ ᴇʟsᴇ ᴄʜᴀᴛ"
        )

        asyncio.create_task(delete_after_delay(context, query.from_user.id, [sent_msg.message_id, warning_msg.message_id]))
    except Exception as e:
        await context.bot.send_message(
            query.from_user.id,
            f"❌ 𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗳𝗲𝘁𝗰𝗵 𝗲𝗽𝗶𝘀𝗼𝗱𝗲. 𝗜𝘁 𝗺𝗮𝘆 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝗱𝗲𝗹𝗲𝘁𝗲𝗱.(=①︿①=) {str(e)}"
        )


async def delete_after_delay(context: CallbackContext, chat_id, message_ids, delay=120):
    """Deletes messages after a delay."""
    await asyncio.sleep(delay)
    for msg_id in message_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass

async def get_blocked_users(context: CallbackContext):
    """Checks how many users have blocked the bot by testing a simple message send."""
    users = get_all_users()
    blocked_users = 0

    for user_id in users:
        try:
            # Try sending a simple message action (like "typing")
            await context.bot.send_chat_action(chat_id=user_id, action="typing")
        except Exception as e:
            if "bot was blocked by the user" in str(e) or "Forbidden" in str(e):
                blocked_users += 1  # Count user as blocked

    return blocked_users


async def stats(update: Update, context: CallbackContext):
    """Sends the number of unique users and blocked users. Only the owner can use it."""
    user_id = update.effective_chat.id

    # Check if the user is the owner
    if user_id != OWNER_ID:
        await context.bot.send_message(user_id, "🚫 𝗡𝘆𝗮𝗮~! 𝗬𝗼𝘂’𝗿𝗲 𝗻𝗼𝘁 𝗮𝗹𝗹𝗼𝘄𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱! (≧◡≦)")
        return

    total_users = len(get_all_users())
    blocked_users = await get_blocked_users(context)  # ✅ Call the async function properly

    # Stats message
    stats_message = (
        "📊 **𝐁\\-𝐛𝐨𝐭 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬, 𝐝𝐞𝐬𝐮\\~** \\(≧◡≦\\)\n\n"
        f"👤 **𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿𝘀:** `{total_users}`\n\n"
        f"🚫 **𝗕𝗹𝗼𝗰𝗸𝗲𝗱 𝗨𝘀𝗲𝗿𝘀:** `{blocked_users}`\n\n"
        "❍ 𝗧\\-𝘁𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝘂𝘀𝗶𝗻𝗴 𝗺𝗲\\ 𝗜’𝗹𝗹 𝗸𝗲𝗲𝗽 𝗱𝗼𝗶𝗻𝗴 𝗺𝘆 𝗯𝗲𝘀𝘁\\~ \\(//ω//\\) 💙"
    )
    await context.bot.send_message(
        user_id,
        stats_message,
        parse_mode=ParseMode.MARKDOWN_V2
    )
def remove_user(user_id):
    """Removes a user from the database (if they block the bot)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    """Fetch all users from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users



async def broadcast(update: Update, context: CallbackContext):
    """Broadcasts a message to all stored users, supporting text, captions, and images, with a result summary."""
    user_id = update.effective_chat.id
    if user_id != OWNER_ID:
        await context.bot.send_message(user_id, "🚫 𝗡𝘆𝗮𝗮~! 𝗬𝗼𝘂’𝗿𝗲 𝗻𝗼𝘁 𝗮𝗹𝗹𝗼𝘄𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱! (≧◡≦)")
        return

    # Detect if the bot is replying to a message
    if update.message.reply_to_message:
        replied_message = update.message.reply_to_message
        text = replied_message.text if replied_message.text else None
        caption = replied_message.caption if replied_message.caption else None
        photo = replied_message.photo[-1].file_id if replied_message.photo else None
    else:
        # If no reply, check if user provided text with /broadcast command
        if not context.args:
            await context.bot.send_message(user_id, "💌 𝗛𝗲𝗲𝗲𝘆, 𝗺𝗮𝘀𝘁𝗲𝗿-𝘀𝗮𝗺𝗮~! (⁄ ⁄>⁄ω⁄<⁄ ⁄) 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗠𝗲 𝗔 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 .𝗦𝗼..𝗧𝗵𝗮𝘁 𝗜 𝗪𝗶𝗹𝗹 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗜𝗧")
            return
        text = " ".join(context.args)
        caption = None
        photo = None

    users = get_all_users()
    sent_count, failed_count = 0, 0

    # Loop through each user and send the message
    for user in users:
        try:
            if photo:
                await context.bot.send_photo(user, photo=photo, caption=caption)
            elif text:
                await context.bot.send_message(user, text)
            sent_count += 1  # Increment sent count if successful
        except Exception:
            failed_count += 1  # User may have blocked bot or deleted account

    # **Broadcast Summary Message**
    image_url = "https://files.catbox.moe/w5vu0y.jpg"  # Use a static image for confirmation

    stats_message = f"""📊 **𝐁\\-𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐑𝐞𝐬𝐮𝐥𝐭, 𝐧𝐲𝐚\\~** \\(≧◡≦\\)\n\n
    ✨ **𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗦𝗲𝗻𝘁:** `{sent_count}` 🎶\n
    💔 **𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗿𝗲𝗮𝗰𝗵:** `{failed_count}` \\(𝗕𝗹𝗼𝗰𝗸𝗲𝗱 𝗼𝗿 𝗶𝗻𝗮𝗰𝘁𝗶𝘃𝗲 𝘂𝘀𝗲𝗿𝘀\\)\n\n
     ➥ 𝗧\\-𝘁𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝘂𝘀𝗶𝗻𝗴 𝗺𝗲\\! 𝗜’𝗹𝗹 𝗸𝗲𝗲𝗽 𝗱𝗼𝗶𝗻𝗴 𝗺𝘆 𝗯𝗲𝘀𝘁\\~ \\(//ω//\\)💙
    """

    # Send the message along with the image
    await context.bot.send_photo(
        chat_id=user_id,
        photo=image_url,
        caption=stats_message,
        parse_mode=ParseMode.MARKDOWN_V2  # Ensure correct Markdown format
    )

    # Escape special characters for MarkdownV2
    stats_message = stats_message.replace("-", "\\-").replace("(", "\\(").replace(")", "\\)")

    try:
        await context.bot.send_photo(
            user_id,
            photo=image_url,
            caption=stats_message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception:
        # If sending image fails, send text instead
        await context.bot.send_message(user_id, stats_message, parse_mode=ParseMode.MARKDOWN_V2)


# Handler for receiving pictures (optional)
async def handle_picture(update: Update, context: CallbackContext):
    """Handle images sent by the user and broadcast them."""
    user_id = update.effective_chat.id
    if user_id != OWNER_ID:
        await context.bot.send_message(user_id, "🚫 You are not authorized to send this.")
        return

    # If the user sends a picture, we handle it here
    if update.message.photo:
        # Get the highest quality photo
        photo = update.message.photo[-1].file_id
        caption = "This is your broadcast image."

        # Send the photo with the caption
        await context.bot.send_photo(
            user_id,
            photo=photo,  # Send the image the user uploaded
            caption=caption,  # Caption you want to send with the image
            parse_mode='MarkdownV2'
        )


# Main function to run the bot
def main():
    setup_database()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_anime_selection, pattern="anime_menu"))
    app.add_handler(CallbackQueryHandler(send_episode_menu, pattern="anime_"))
    app.add_handler(CallbackQueryHandler(send_episode, pattern="episode_"))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(retry_start, pattern="^retry_start$"))

    app.run_polling()

if __name__ == "__main__":
    main()


