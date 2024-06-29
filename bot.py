import asyncio

from aiogram import Bot, Dispatcher

from config_reader import config
from db.connector import setup_get_pool
from functions.const import ADMIN_CHAT_ID
from handlers import (
    answer,
    file_id
)
from middlewares.db import DbSessionMiddleware
from middlewares.throttling import ThrottlingMiddleware


async def main():
    bot = Bot(
        token=config.bot_token.get_secret_value(), parse_mode="HTML"
    )
    dp = Dispatcher()
    dp.message.middleware(ThrottlingMiddleware(1))
    dp.message.middleware(DbSessionMiddleware(session_pool=await setup_get_pool()))

    dp.include_routers(
        answer.router,
        file_id.router,
    )

    try:
        await bot.send_message(ADMIN_CHAT_ID, "Бот запущен")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.send_message(ADMIN_CHAT_ID, "Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
