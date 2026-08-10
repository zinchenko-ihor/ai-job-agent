from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def main_keyboard() -> ReplyKeyboardMarkup:

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🔎 Вакансії"
                ),
                KeyboardButton(
                    text="👤 Мій профіль"
                ),
            ],
            [
                KeyboardButton(
                    text="🔄 Оновити вакансії"
                ),
                KeyboardButton(
                    text="🧹 Очистити"
                ),
            ],
        ],
        resize_keyboard=True,
    )
