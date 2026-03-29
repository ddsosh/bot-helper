from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_all_subscriptions, mark_reminded_5, mark_reminded_1, get_user_by_id
from keyboards.menu import get_label

scheduler = AsyncIOScheduler()

def start_scheduler(bot):
    scheduler.add_job(
        check_subscriptions,
        trigger='cron',
        hour=12,
        args=(bot,)
    )
    scheduler.start()

async def check_subscriptions(bot):
    today = datetime.today().date()
    subs = await get_all_subscriptions()

    for sub in subs:
        sub_id = sub[0]
        user_id = sub[1]
        title = sub[2]
        end_date = sub[4]
        reminded_5_days = sub[5]
        reminded_1_day = sub[6]

        user = await get_user_by_id(user_id)
        if not user:
            continue
        lang = user[2] if len(user) > 2 and user[2] else "ru"

        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        days_left = (end - today).days

        if days_left < 0:
            continue

        if days_left == 5 and not reminded_5_days:
            await bot.send_message(
                chat_id=user[1],
                text=get_label(lang, "reminder_5_days", title=title)
            )

            await mark_reminded_5(sub_id)

        if days_left == 1 and not reminded_1_day:
            await bot.send_message(
                chat_id=user[1],
                text=get_label(lang, "reminder_1_day", title=title)
            )

            await mark_reminded_1(sub_id)
