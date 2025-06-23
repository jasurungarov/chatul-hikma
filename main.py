import os
import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from registration import register_user
from openai_handler import answer_question
from prayer_times import get_today_prayer_times
from daily_scheduler import schedule_daily_messages
from translations import translate
from database import init_db, get_user_by_chat_id
import nest_asyncio


load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
user_data = {}
languages = {'🇺🇿 O‘zbek': 'uz', '🇷🇺 Русский': 'ru', '🇬🇧 English': 'en', '🇰🇬 Кыргызча': 'kg'}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(lang)] for lang in languages]
    await update.message.reply_text("Tilni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text
    if text in languages:
        lang_code = languages[text]
        user_data[chat_id] = {'lang': lang_code}
        await update.message.reply_text(translate("intro", lang_code))
        keyboard = [[KeyboardButton("🕌 Savol berish")], [KeyboardButton("📍 Joylashuv yuborish", request_location=True)]]
        await update.message.reply_text(translate("choose_action", lang_code), reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    elif "🕌" in text:
        await update.message.reply_text(translate("send_question", user_data[chat_id]['lang']))
    else:
        lang = user_data.get(chat_id, {}).get("lang", "uz")
        response = await answer_question(text, lang)
        await update.message.reply_text(response)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    loc = update.message.location
    name = update.effective_user.full_name
    register_user(chat_id, name, {"lat": loc.latitude, "lon": loc.longitude})
    await update.message.reply_text("Joylashuv saqlandi. Har kuni bomdoddan oldin sizga xabar yuboramiz.")

async def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    schedule_daily_messages(app)
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())