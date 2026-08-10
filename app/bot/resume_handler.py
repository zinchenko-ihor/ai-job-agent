from pathlib import Path

from aiogram import Router
from aiogram.types import Message

router = Router()

RESUME_DIR = Path("storage/resumes")
RESUME_DIR.mkdir(parents=True, exist_ok=True)


@router.message(lambda message: message.document is not None)
async def handle_pdf(message: Message) -> None:
    document = message.document

    filename = document.file_name or ""

    # Приймаємо тільки PDF
    if not filename.lower().endswith(".pdf"):
        await message.answer(
            "❌ Будь ласка, надішли резюме у форматі PDF."
        )
        return

    user_id = message.from_user.id

    user_dir = RESUME_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    file_path = user_dir / "resume.pdf"

    try:
        # Завантажуємо файл через aiogram
        await message.bot.download(
            document,
            destination=file_path,
        )

        await message.answer(
            "✅ Резюме отримано!\n\n"
            f"📄 Файл: {filename}\n\n"
            "Наступний крок — проаналізувати резюме "
            "та визначити твій професійний профіль."
        )

        print(
            f"Resume saved: {file_path}"
        )

    except Exception as exc:
        print(
            f"Failed to download resume: {exc}"
        )

        await message.answer(
            "❌ Не вдалося зберегти резюме. "
            "Спробуй надіслати PDF ще раз."
        )
