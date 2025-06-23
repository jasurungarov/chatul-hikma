from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_all_users
from prayer_times import get_today_prayer_times
from openai_handler import answer_question

def schedule_daily_messages(app):
    scheduler = AsyncIOScheduler()

    async def send_daily():
        for user in get_all_users():
            lat = user['location']['lat']
            lon = user['location']['lon']
            prayers = get_today_prayer_times(lat, lon)
            hadis = await answer_question("Menga sahih hadisdan tavsiya bering.", lang="uz")
            try:
                await app.bot.send_message(user['chat_id'], f"🕋 Bugungi namoz vaqtlari:\n{prayers}\n\n📜 Hadis: {hadis}")
            except:
                pass

    scheduler.add_job(send_daily, 'cron', hour=4, minute=30)
    scheduler.start()