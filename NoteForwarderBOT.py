import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonCommands
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os
import threading
from flask import Flask
import sqlite3
import html

load_dotenv()
# Enable logging
logging.basicConfig(level=logging.INFO)

# Replace with your bot's token
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Replace with your channel's chat ID (must be negative)
CHANNEL_ID = os.getenv("CHANNEL_ID")

ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

def init_db():
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            first_name TEXT,
            username TEXT,
            phone_number TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# File dictionary with Telegram file IDs instead of local paths
file_dict = {
    "SCHEME & SYLLABUS": {
        "message_id": 10  # Replace with actual file_id
    },
    "1st Sem": {
        "C Programming": {
            "Books": [14, 15],
            "Notes": [17],
            "PYQs": [70]
        },
        "Calculus": {
            "Books": [20, 21, 22],
            "Notes": [23, 24, 25],
            "PYQs": [70],
            "Assignments": [27, 28, 29, 30, 31, 32, 33, 34]
        },
        "Quantum Physics": {
            "Books": [38, 39, 40, 41, 42],
            "Notes": [43, 44, 45, 46, 47, 48, 49, 50],
            "PYQs": [70],
            "Assignments": [51, 52, 53, 54]
        },
        "Intro to IT": {
            "Books": [60],
            "Notes": [62, 63, 64, 65, 66, 67, 68],
            "PYQs": [70]
        },
        "Workshop": {
            "Lab File": [56, 57, 58],
        }
    },
    "2nd Sem": {
        "Differential Equations": {
            "Books": [73, 74],
            "Notes": [77, 78, 79, 76],
            "Assignments": [81, 82, 83, 84, 85, 86, 87, 88, 89]
        },
        "OOPS using C++": {
            "Books": [],
            "Notes": [91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103],
            "PYQs": [105],
            "Assignments": [107, 108, 109],
            "Practical File": [111]
        },
        "Chemistry": {
            "Book Notes": [115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126],
            "Notes": [127, 128, 129, 130, 131],
            "PYQs": [132],
            "Assignment": [134],
            "Practical Manual":[136]
        },
        "Professional Communication": {
            "Book Notes": [138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 149, 150, 151, 152],
            "Handwritten Notes": [173, 174, 175, 176, 177],
            "PPTs": [159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171]
        },
        "BITC": {
            "Notes": [179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 188, 189, 190, 191],
            "Practical File": [196],
            "Assignment": [193, 194]
        },
        "Web Development": {
            "Practical File": [198]
        }
    },
    "3rd Sem": {
        "Data Structures": {
            "Books": [201, 202],
            "Notes": [204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214],
            "PYQs": [313],
            "DSA Lab Files":[216, 217],
            "Tutorials": [219, 220, 221, 222, 223]
        },
        "Linear Algebra & Probability": {
            "Books": [225, 226],
            "Notes": [228, 229, 230, 231, 232, 233, 234],
            "PYQs": [313],
            "Assignments": [235]
        },
        "Digital Electronics": {
            "Notes": [237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251],
            "PYQs": [313],
            "Practical File":[253],
            "Tutorials": [258, 259, 260, 261, 262, 263, 264, 265, 266, 267],
            "Assignments": [255, 256]
        },
        "DBMS": {
            "Books": [269],
            "Notes": [271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292],
            "PYQs": [313],
            "Assignments": [294],
            "Practical File": [296]
        },
        "Computer Architecture": {
            "Books": [298],
            "Notes": [300, 301, 302, 303],
            "PYQs": [313],
            "Tutorials": [305, 306, 307, 308, 309, 310]
        },
        "Minors & Majors": {
            "Minors": [314],
            "Majors": [313]
        }
    },
    "4th Sem": {
        "Computer Networks": {
            "Notes": [319, 320, 321, 322],
            "PYQs": [326],
            "Practical File":[],
            "Assignments": [324]
        },
        "Discrete Structures": {
            "Books": [328, 329, 330, 331],
            "Notes": [333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344],
            "PYQs": [347],
            "Assignments": [345]
        },
        "Operating system": {
            "Books": [349, 350, 351],
            "Notes": [353, 354, 355, 356],
            "PYQs": [361],
            "Lab File":[358, 359]
        },
        "Microprocessor": {
            "Books": [371],
            "Notes": [373, 374, 375, 376, 377],
            "PYQs": [382],
            "Practical File": [379, 380]
        },
        "Economics": {
            "Books": [363],
            "Notes": [365, 366],
            "PYQs": [368]
        }
    },
    "5th Sem": {
        "Design & Analysis of Algorithms": {
            "Books": [388],
            "Notes": [390, 391, 392, 393],
            "PYQs": [400, 401, 402],
            "Practical File":[398],
            "Assignments": [395, 396]
        },
        "Artificial Intelligence": {
            "Books": [405, 406, 407],
            "Notes": [409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419],
            "PYQs": [425, 426, 427, 428],
            "Assignments": [421],
            "Practical File":[423]
        },
        "Python": {
            "Books": [431],
            "Notes": [433, 434, 435, 436],
            "PYQs": [444, 445, 446, 447, 448],
            "Practical File":[441],
            "Assignments": [438, 439]
        },
        "Network Security": {
            "Books": [451, 452],
            "Notes": [454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468],
            "PYQs": [484, 485, 486, 487, 488, 489, 490],
            "Practical File": [472],
            "Assignments": [470],
            "Tutorials": [474, 475, 476, 477, 478, 479, 480, 481, 482]
        },
        "Cyber laws & IPR": {
            "Notes": [493, 494, 495],
            "PYQs": [500, 501, 502],
            "Assignments": [497, 498]
        }
    }
}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.message.chat_id
    first_name = user.first_name
    username = user.username or "Unknown"

    # Store user in SQLite
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO users (chat_id, first_name, username) VALUES (?, ?, ?)",
                       (chat_id, first_name, username))
        conn.commit()

    conn.close()

    await update.message.reply_text(
        f"\U0001F44B Hello {update.effective_user.first_name}!\n"
        "\U0001F4DA I provide notes, assignments, books, lab files, and PYQs for all subjects semester-wise for the <b>BE-IT</b> curriculum.\n"
        "\U0001F4CC <b>Select your semester or view the scheme & syllabus:</b>",
        parse_mode="HTML",
        reply_markup=semester_keyboard()
    )
    await context.bot.set_my_commands([("start", "Start the bot"), ("help", "View help instructions")])
    await context.bot.set_chat_menu_button(update.message.chat_id, MenuButtonCommands())

def semester_keyboard():
    keyboard = [
        [InlineKeyboardButton("📜 SCHEME OF EXAMINATION & SYLLABUS", callback_data="scheme_syllabus")],
        [InlineKeyboardButton("📕 IT 1st Sem", callback_data="sem:1st Sem")],
        [InlineKeyboardButton("📗 IT 2nd Sem", callback_data="sem:2nd Sem")],
        [InlineKeyboardButton("📘 IT 3rd Sem", callback_data="sem:3rd Sem")],
        [InlineKeyboardButton("📙 IT 4th Sem", callback_data="sem:4th Sem")],
        [InlineKeyboardButton("📔 IT 5th Sem", callback_data="sem:5th Sem")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def send_scheme_syllabus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    message_id = file_dict["SCHEME & SYLLABUS"]["message_id"]
    
    await context.bot.forward_message(
        chat_id=query.message.chat_id,  # Forward to the user
        from_chat_id=CHANNEL_ID,  # Forward from your channel
        message_id=message_id  # Forward the correct file
    )

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="\U0001F3E0 Send <b>/start</b> to return to the main menu.",
        parse_mode="HTML"
    )


async def semester_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    semester = query.data.split(":")[1]
    context.user_data["semester"] = semester

    await query.edit_message_text(
        text=f"\U0001F4DA <b>Choose a subject from {semester}:</b>",
        parse_mode="HTML",
        reply_markup=subject_keyboard(semester)
    )

def subject_keyboard(semester):
    subjects = list(file_dict.get(semester, {}).keys())
    keyboard = [[InlineKeyboardButton(f"📖 {subject}", callback_data=f"subj:{subject}")] for subject in subjects]
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back:semesters")])
    return InlineKeyboardMarkup(keyboard)

async def subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    subject = query.data.split(":")[1]
    context.user_data["subject"] = subject

    await query.edit_message_text(
        text=f"\U0001F4C2 <b>Select the resource type for {subject}:</b>",
        parse_mode="HTML",
        reply_markup=resource_keyboard(context.user_data["semester"], subject)
    )

def resource_keyboard(semester, subject):
    resources = list(file_dict.get(semester, {}).get(subject, {}).keys())
    keyboard = [[InlineKeyboardButton(f"📌 {resource}", callback_data=f"res:{resource}")] for resource in resources]
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back:subjects")])
    return InlineKeyboardMarkup(keyboard)

async def send_resource(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    semester = context.user_data.get("semester")
    subject = context.user_data.get("subject")
    resource_type = query.data.split(":")[1]

    message_ids = file_dict.get(semester, {}).get(subject, {}).get(resource_type, [])

    if not message_ids:
        await query.edit_message_text(
            text=f"\u26A0 <b>No {resource_type} available for {subject}.</b>\n"
                 "I'll ask my creator to upload the required materials. \U0001F4E4",
            parse_mode="HTML"
        )
        return

    await query.edit_message_text(
        text="\U0001F50D Fetching your files from the UIET IT channel... Please wait ⏳",
        parse_mode="HTML"
    )

    for message_id in message_ids:
        await context.bot.forward_message(
            chat_id=query.message.chat_id,  # Send to user
            from_chat_id=CHANNEL_ID,  # Fetch from UIET IT channel
            message_id=message_id  # Use correct message ID
        )

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="✅ <b>All requested files have been forwarded successfully!</b>\n"
             "\U0001F3E0 Send <b>/start</b> to return to the main menu.",
        parse_mode="HTML"
    )


async def back_to_semesters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("\U0001F4CC <b>Select your semester:</b>", parse_mode="HTML", reply_markup=semester_keyboard())

async def back_to_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    semester = context.user_data.get("semester")
    await query.edit_message_text(f"\U0001F4DA <b>Choose a subject from {semester}:</b>", parse_mode="HTML", reply_markup=subject_keyboard(semester))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "\u2753 <b>Help Section</b> \u2753\n\n"
        "\U0001F4CC <b>How to use this bot?</b>\n"
        "1️⃣ Start with <b>/start</b>\n"
        "2️⃣ Select your <b>semester</b>\n"
        "3️⃣ Select the <b>subject</b>\n"
        "4️⃣ Choose the <b>resource type</b> (Books, Notes, PYQs, etc.)\n"
        "5️⃣ Bot will send the required files \U0001F4C2\n\n"
        "💡 Need more help? Request to join our channel:\n<a href='https://t.me/+J8zLk2dQb301OGE1'>Click here</a>",
        parse_mode="HTML"
    )

async def user_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    conn.close()

    await update.message.reply_text(f"📊 <b>Total Users: {user_count}</b>", parse_mode="HTML")

async def user_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    # Connect to SQLite database
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, username, chat_id FROM users")
    users = cursor.fetchall()
    conn.close()

    user_count = len(users)

    if not users:
        message = "No users found."
    else:
        def escape_html(text):
            """Escape special characters for Telegram HTML formatting"""
            return html.escape(text)

        user_list = "\n".join([
            f"🔹 <b>{escape_html(first_name)}</b> (@{escape_html(username)}) - <code>{chat_id}</code>" 
            if username else 
            f"🔹 <b>{escape_html(first_name)}</b> - <code>{chat_id}</code>"
            for first_name, username, chat_id in users
        ])
        
        message = f"📊 <b>Total Unique Users:</b> <b>{user_count}</b>\n\n{user_list}"

    await update.message.reply_text(message, parse_mode="HTML")



def run_bot():
    init_db()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler("user_count", user_count))  # Admin-only command
    application.add_handler(CommandHandler("user_list", user_list))  # Admin-only command
    application.add_handler(CallbackQueryHandler(send_scheme_syllabus, pattern="^scheme_syllabus$"))
    application.add_handler(CallbackQueryHandler(semester_selection, pattern="^sem:"))
    application.add_handler(CallbackQueryHandler(subject_selection, pattern="^subj:"))
    application.add_handler(CallbackQueryHandler(send_resource, pattern="^res:"))
    application.add_handler(CallbackQueryHandler(back_to_semesters, pattern="^back:semesters$"))
    application.add_handler(CallbackQueryHandler(back_to_subjects, pattern="^back:subjects$"))

    print("Bot is starting...")
    application.run_polling()


app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    run_bot()  # Runs bot concurrently with Flask