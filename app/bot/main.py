import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.bot.handlers import router


load_dotenv()


async def main():

    token = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )

    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set"
        )

    bot = Bot(
        token=token
    )

    dp = Dispatcher()

    dp.include_router(
        router
    )

    print(
        "Bot started..."
    )

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":
    asyncio.run(main())
