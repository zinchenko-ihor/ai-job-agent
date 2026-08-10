import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.bot.handlers import router as handlers_router
from app.bot.resume_handler import router as resume_router


load_dotenv()


async def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set"
        )

    bot = Bot(token=token)

    dp = Dispatcher()

    # Основні команди
    dp.include_router(handlers_router)

    # Обробка резюме
    dp.include_router(resume_router)

    print("Telegram bot started...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
