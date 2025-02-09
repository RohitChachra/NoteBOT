import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonCommands
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()
# Enable logging
logging.basicConfig(level=logging.INFO)

# Replace with your bot's token
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Replace with your channel's chat ID (must be negative)
CHANNEL_ID = os.getenv("CHANNEL_ID")

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
    }
}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"👋 Hello {update.effective_user.first_name}!\n"
        "📚 I provide notes, assignments, books, lab files, and PYQs for all subjects semester-wise for the **BE-IT** curriculum.\n"
        "📌 **Select your semester or view the scheme & syllabus:**",
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
        text="🏠 Send **/start** to return to the main menu."
    )


async def semester_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    semester = query.data.split(":")[1]
    context.user_data["semester"] = semester

    await query.edit_message_text(
        text=f"📚 **Choose a subject from {semester}:**",
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
        text=f"📂 **Select the resource type for {subject}:**",
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
            text=f"⚠️ **No {resource_type} available for {subject}.**\n"
                 "I'll ask my creator to upload the required materials. 📤"
        )
        return

    await query.edit_message_text(text=f"🔍 Fetching your files from the UIET IT channel... Please wait ⏳")

    for message_id in message_ids:
        await context.bot.forward_message(
            chat_id=query.message.chat_id,  # Send to user
            from_chat_id=CHANNEL_ID,  # Fetch from UIET IT channel
            message_id=message_id  # Use correct message ID
        )

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="✅ **All requested files have been forwarded successfully!**\n"
             "🏠 Send **/start** to return to the main menu."
    )


async def back_to_semesters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📌 **Select your semester:**", reply_markup=semester_keyboard())

async def back_to_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    semester = context.user_data.get("semester")
    await query.edit_message_text(f"📚 **Choose a subject from {semester}:**", reply_markup=subject_keyboard(semester))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "❓ **Help Section** ❓\n\n"
        "📌 **How to use this bot?**\n"
        "1️⃣ Start with `/start`\n"
        "2️⃣ Select your **semester**\n"
        "3️⃣ Select the **subject**\n"
        "4️⃣ Choose the **resource type** (Books, Notes, PYQs, etc.)\n"
        "5️⃣ Bot will send the required files 📂\n\n"
        "💡 Need more help? Request to join our channel:\nhttps://t.me/+J8zLk2dQb301OGE1"
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CallbackQueryHandler(send_scheme_syllabus, pattern="^scheme_syllabus$"))
    application.add_handler(CallbackQueryHandler(semester_selection, pattern="^sem:"))
    application.add_handler(CallbackQueryHandler(subject_selection, pattern="^subj:"))
    application.add_handler(CallbackQueryHandler(send_resource, pattern="^res:"))
    application.add_handler(CallbackQueryHandler(back_to_semesters, pattern="^back:semesters$"))
    application.add_handler(CallbackQueryHandler(back_to_subjects, pattern="^back:subjects$"))
    application.run_polling()

if __name__ == '__main__':
    main()
